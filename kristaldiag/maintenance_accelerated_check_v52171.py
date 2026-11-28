"""Independent scope and receipt validation; source authenticity is not asserted."""
import hashlib,json,sqlite3
from pathlib import Path
from contextlib import closing

def need(x,m):
    if not x:raise ValueError(m)
def sha(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def ro(p):return sqlite3.connect(Path(p).resolve().as_uri()+'?mode=ro',uri=True)
def verify(out,maintenance):
    out=Path(out);p=out/'accelerated.sqlite';r=json.loads((out/'report.json').read_bytes());need(sha(p)==r['database_sha256'] and sha(maintenance)==r['maintenance_sha256'],'Receipt digest mismatch')
    with closing(ro(p)) as c,closing(ro(maintenance)) as m:
        need(c.execute('pragma integrity_check').fetchone()==('ok',),'Integrity check failed')
        ids={v[0] for v in m.execute('SELECT wid FROM alias_target UNION SELECT external_id FROM ambiguous')};pairs=set(m.execute('SELECT wid,lang,occurrences FROM alias_target'))
        need(ids=={v[0] for v in c.execute('SELECT wid FROM target')},'Target mismatch');need(pairs==set(c.execute('SELECT * FROM alias_target')),'Pair mismatch')
        sources={k:json.loads(v) for k,v in c.execute('SELECT * FROM source')};need(sources=={v['source_id']:v for v in r['sources']},'Source receipt mismatch')
        obs={};indexed={};partial={}
        for s,w,raw in c.execute('SELECT * FROM observation ORDER BY source_id,wid'):
            need(w in ids and s in sources,'Observation out of scope');d=json.loads(raw);obs.setdefault(s,{})[w]=d
            if s=='partial_dump':need(d['external_id']==w and d['source_authenticated'] is False and d['historical_equivalence_claimed'] is False,'Partial scope');partial[w]=d
            else:need(d['wid']==w and d['kind']==('item' if w.startswith('Q') else 'property'),'External scope');need(w not in indexed,'Repeated index lookup');indexed[w]=d
        for s,v in sources.items():need(v['observed_ids']==len(obs.get(s,{})),'Source count mismatch')
        count=0;labels=0;pair_keys={(a,b) for a,b,_ in pairs}
        for w,l,status,rev,label,aliases in c.execute('SELECT * FROM alias_observation'):
            need((w,l) in pair_keys,'Alias pair outside scope');d=partial.get(w);v=indexed.get(w,{})
            if d and l!='und' and l in d['aliases']:
                need(status=='DUMP_REVISION_OBSERVATION_ONLY' and rev==d['source_revision'] and label==d['labels'].get(l,{}).get('value') and json.loads(aliases)==[x['value'] for x in d['aliases'][l]],'Dump alias mismatch');count+=1
            else:
                expected=v.get('label_'+l) if l in ('fr','en') else None;need(rev is None and aliases is None and label==expected and status==('EXACT_LABEL_ONLY' if expected else 'NO_EXACT_ALIAS_EVIDENCE'),'Inferred alias or language')
            labels+=bool(label)
        need(c.execute('SELECT count(*) FROM alias_observation').fetchone()[0]==len(pairs),'Missing pair')
        expected={'distinct_targets':len(ids),'alias_pairs':len(pairs),'partial_dump_ids':len(partial),'indexed_ids':len(indexed),'observed_ids':len(set(partial)|set(indexed)),'unobserved_ids':len(ids-(set(partial)|set(indexed))),'pairs_with_dump_alias_observation':count,'pairs_with_exact_label':labels,'historical_aliases_repaired':0}
        need(r['counts']==expected,'Count mismatch');need(all(r['policy'][k] is False for k in ('dump_stream_read','network_used','canonical_modified','public_modified','historical_aliases_invented','source_authenticated')) and r['policy']['new_accepted_links']==0,'Policy mismatch')
    return {'status':'PASS_ACCELERATED_PRIVATE_SCOPE','database_sha256':r['database_sha256'],'source_authentication_checked':False,'dump_source_lines_rechecked':False}
