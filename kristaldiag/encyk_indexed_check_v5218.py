"""Independent verification of output scope, cache bytes and lexical projection."""
import gzip,hashlib,json,sqlite3,re
from pathlib import Path
from contextlib import closing

def need(x,m):
    if not x:raise ValueError(m)
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def j(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def ro(p):return sqlite3.connect(Path(p).resolve().as_uri()+'?mode=ro',uri=True)
def verify(out,scan,base):
    out=Path(out);r=json.loads((out/'report.json').read_bytes());p=out/'indexed.sqlite';need(sha(p)==r['database_sha256'] and sha(scan)==r['maintenance_sha256'] and sha(base)==r['baseline_sha256'],'Receipt mismatch')
    with closing(ro(p)) as c,closing(ro(scan)) as m:
        need(c.execute('PRAGMA integrity_check').fetchone()==('ok',),'Integrity check failed');ids={v[0] for v in m.execute('SELECT wid FROM alias_target UNION SELECT external_id FROM ambiguous')};pairs=set(m.execute('SELECT wid,lang,occurrences FROM alias_target'));need(set(c.execute('SELECT * FROM target'))=={(w,'item' if w.startswith('Q') else 'property') for w in ids},'Target scope');need(set(c.execute('SELECT * FROM alias_target'))==pairs,'Alias scope')
        qs={w for w in ids if w.startswith('Q')};obs={w:json.loads(raw) for w,raw in c.execute('SELECT * FROM indexed_entity')};compact={w:json.loads(raw) for w,raw in c.execute('SELECT * FROM compact_entity')};need(set(obs)<=qs and set(compact)<=ids-set(obs),'Observation scope')
        covered=set();found=set();batch_count=0
        for name,raw in c.execute('SELECT * FROM batch_receipt ORDER BY batch'):
            b=json.loads(raw);need(re.fullmatch('batch_[0-9]{5}',name) and b['batch']==name,'Batch name');folder=Path(r['cache_path'])/name
            need(sha(folder/'entities.jsonl.gz')==b['gzip_sha256'] and sha(folder/'entities.jsonl.gz.reader.json')==b['worker_manifest_sha256'],'Cache bytes drift');targets=set(b['requested']);need(not targets&covered and targets<=qs,'Batch scope');covered|=targets;seen=set()
            manifest=json.loads((folder/'entities.jsonl.gz.reader.json').read_bytes());need(manifest['sha256']==b['gzip_sha256'] and manifest['scan_entire_dump'] is False and manifest['source_modified'] is False and manifest['backend']['random_access'] is True,'Cache manifest contract')
            for k,v in [('source_dump','dump'),('index_locator','locator'),('compression_index','compression')]:need(manifest[k]==r['source_binding'][v],'Cache source mismatch')
            with gzip.open(folder/'entities.jsonl.gz','rb') as f:
                for line in f:
                    obj=json.loads(line);w=obj['id'];need(w in targets and w not in seen and w in obs and obj['type']=='item','Entity mismatch');seen.add(w);d=obs[w]
                    need(d['wid']==w and d['revision']==obj['lastrevid'] and type(d['revision']) is int and d['revision']>0 and d['source_authenticated'] is False and d['entity_sha256']==hashlib.sha256(j(obj).encode()).hexdigest(),'Entity receipt mismatch')
                    for k in ('labels','descriptions','aliases'):
                        v=obj.get(k);expected=None if v is None else {lang:([x['value'] for x in rows] if k=='aliases' else rows['value']) for lang,rows in v.items()}
                        need(d[k]==expected,'Lexical projection mismatch')
                        if v is not None:
                            for lang,rows in v.items():need(all(x['language']==lang for x in (rows if k=='aliases' else [rows])),'Source language mismatch')
            missing=set(b['unlocated']);rejected={x['qid'] for x in b['rejected']};need(not(seen&missing or seen&rejected or missing&rejected) and seen|missing|rejected==targets and len(seen)==b['found'],'Batch accounting');need(manifest['requested']==len(targets) and manifest['found']==len(seen) and set(manifest['unlocated_qids'])==missing and manifest['rejected']==b['rejected'],'Batch manifest count');found|=seen;batch_count+=1
        need(covered==qs and found==set(obs),'Batch completeness')
        for w,d in compact.items():need(d['wid']==w and d['kind']==('item' if w in qs else 'property'),'Compact identity mismatch')
        rows=list(c.execute('SELECT * FROM pair_observation'));need({(w,l) for w,l,*_ in rows}=={(w,l) for w,l,n in pairs},'Pair coverage');aliases=labels=0
        for w,l,status,rev,label,raw in rows:
            d=obs.get(w);v=compact.get(w,{});expected=('NO_EXACT_OBSERVATION',None,None,None)
            if l=='und':expected=('UNDETERMINED_LANGUAGE',None,None,None)
            elif d:
                a=(d['aliases'] or {}).get(l);t=(d['labels'] or {}).get(l);expected=('INDEXED_DUMP_LANGUAGE_OBSERVATION' if a is not None or t is not None else 'NO_EXPLICIT_LANGUAGE_IN_DUMP',d['revision'],t,a)
            elif l in ('fr','en') and v.get('label_'+l):expected=('COMPACT_LABEL_REVISION_UNKNOWN',None,v['label_'+l],None)
            need((status,rev,label,json.loads(raw) if raw is not None else None)==expected,'Pair projection mismatch');aliases+=raw is not None;labels+=bool(label)
        expected={'targets':len(ids),'qid_targets':len(qs),'pid_targets':len(ids-qs),'indexed_qids':len(obs),'compact_fallback_ids':len(compact),'observed_ids':len(obs)+len(compact),'unobserved_ids':len(ids)-len(obs)-len(compact),'alias_pairs':len(pairs),'pairs_with_explicit_alias_list':aliases,'pairs_with_exact_label':labels,'und_pairs':sum(l=='und' for w,l,n in pairs),'batches':batch_count}
        need(all(r['counts'][k]==v for k,v in expected.items()) and 0<=r['counts']['reused_batches']<=batch_count,'Counts mismatch');need(all(r['policy'][k] is False for k in ('network_used','full_dump_scan','index_rebuilt','canonical_modified','public_modified','source_authenticated')) and r['policy']['new_accepted_links']==r['policy']['historical_aliases_repaired']==0,'Policy mismatch')
    return {'status':'PASS_INDEXED_PRIVATE_SCOPE','database_sha256':r['database_sha256'],'cached_entity_records_checked':len(obs),'source_authentication_checked':False,'original_dump_bytes_rechecked':False}
