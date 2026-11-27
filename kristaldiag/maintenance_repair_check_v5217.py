"""Independent verifier for the effective private dictionary and graph scope."""
import hashlib,json,sqlite3,zipfile,stat
from pathlib import Path,PurePosixPath
from contextlib import closing

def need(x,m):
    if not x:raise ValueError(m)
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def ro(p):return sqlite3.connect(p.resolve().as_uri()+'?mode=ro',uri=True)
def ptr(d,p):
    for x in p.split('/')[1:]:
        x=x.replace('~1','/').replace('~0','~');d=d[int(x)] if isinstance(d,list) else d[x]
    return d

def verify(out,base,scan,root):
    out,base,scan,root=map(Path,(out,base,scan,root));r=json.loads((out/'report.json').read_bytes());p=out/'repair.sqlite';b=base/'active.sqlite';m=scan/'maintenance.sqlite'
    need(digest(p)==r['database_sha256'] and digest(b)==r['baseline_sha256'] and digest(m)==r['maintenance_sha256'],'Digest mismatch')
    z=zipfile.ZipFile(root) if root.is_file() else None
    def read(rel):
        q=PurePosixPath(rel);need(not q.is_absolute() and '..' not in q.parts and '\\' not in rel and ':' not in rel,'Unsafe evidence path')
        if z:
            i=z.getinfo(rel);need(not stat.S_ISLNK(i.external_attr>>16),'Linked evidence');return z.read(i)
        f=root.joinpath(*q.parts)
        for x in [*f.absolute().parents,f.absolute()]:
            s=x.lstat();need(not stat.S_ISLNK(s.st_mode) and not getattr(s,'st_file_attributes',0)&0x400,'Linked evidence')
        return f.read_bytes()
    try:
        with closing(ro(p)) as c:
            c.execute('ATTACH DATABASE ? AS b',(b.resolve().as_uri()+'?mode=ro',));c.execute('ATTACH DATABASE ? AS m',(m.resolve().as_uri()+'?mode=ro',))
            need(c.execute('pragma integrity_check').fetchone()==('ok',),'DB integrity')
            def same(a,b,msg):
                for x,y in [(a,b),(b,a)]:need(not c.execute(x+' EXCEPT '+y+' LIMIT 1').fetchone(),msg)
            same("SELECT ns,sid,lang,term FROM effective WHERE status='ACTIVE_CANONICAL'",'SELECT namespace_id,semantic_id,language_tag,preferred_term FROM b.lexical','Active cells changed')
            same("SELECT ns,sid,kind FROM display_ref", "SELECT i.namespace_id,i.semantic_id,i.kind FROM b.identity i JOIN b.workspace w ON i.owner_slug=w.slug WHERE w.active=1 AND i.kind IN ('entity','property')",'Display scope mismatch')
            same("SELECT ns,sid,lang,term FROM effective WHERE status='RECOVERED_EXACT_PRIVATE'", "SELECT e.ns,e.sid,e.lang,min(e.term) FROM evidence e WHERE NOT EXISTS(SELECT 1 FROM b.lexical l WHERE l.namespace_id=e.ns AND l.semantic_id=e.sid AND l.language_tag=e.lang) GROUP BY 1,2,3 HAVING count(DISTINCT e.term)=1",'Recovery consensus mismatch')
            need(not c.execute('SELECT ns,sid,lang,term,path,sha256,pointer,method FROM m.observation EXCEPT SELECT * FROM evidence LIMIT 1').fetchone(),'Prior observation lost')
            same('SELECT slug,ns,status,record_json FROM graph_scope','SELECT slug,namespace_id,status,report_json FROM b.v52161_active_graph','Graph scope mismatch')
            same('SELECT ns,sid,kind FROM unresolved', 'SELECT ns,sid,kind FROM display_ref d WHERE NOT EXISTS(SELECT 1 FROM effective e WHERE e.ns=d.ns AND e.sid=d.sid)','Unresolved scope mismatch')
            need(not c.execute('SELECT 1 FROM evidence e LEFT JOIN m.target t ON e.ns=t.ns AND e.sid=t.sid WHERE t.sid IS NULL LIMIT 1').fetchone(),'Evidence outside missing targets')
            maps={};checked=0
            for path,h in c.execute('SELECT DISTINCT path,sha256 FROM evidence'):
                raw=read(path);need(hashlib.sha256(raw).hexdigest()==h,'Source drift '+path);doc=json.loads(raw.decode('utf-8-sig'))
                for ns,sid,lang,term,pointer,method,owner,kind in c.execute('SELECT e.ns,e.sid,e.lang,e.term,e.pointer,e.method,w.local_directory,t.kind FROM evidence e JOIN m.target t ON e.ns=t.ns AND e.sid=t.sid JOIN b.workspace w ON t.slug=w.slug WHERE e.path=? AND e.sha256=?',(path,h)):
                    need(path.startswith(owner+'/'),'Wrong owner');v=ptr(doc,pointer)
                    if method=='SCOPED_HISTORICAL_DICTIONARY':
                        row=ptr(doc,pointer.rsplit('/',1)[0]);need(doc['artifact_type']=='kristal_curated_dictionary' and doc['namespace_id']==ns and doc['language']==lang and row['semantic_id']==sid and v==term,'Scoped record mismatch')
                    else:
                        if owner not in maps:maps[owner]=json.loads(read(owner+'/.kristal/v11/identity-migration-map.json').decode('utf-8-sig'))
                        a=maps[owner];need(a['namespace_id']==ns and a['format']=='dik.bulk-secondpass/2','Map namespace')
                        if method=='LEGACY_V8':
                            row=ptr(doc,pointer.rsplit('/',1)[0]);native=row['semantic_ref']['id'];need(row['semantic_ref']['identity_space']=='kristal_v6' and doc['language']==lang and v==term,'V8 mismatch')
                        elif method=='NATIVE_REGISTRY':
                            row=ptr(doc,'/'.join(pointer.split('/')[:3]));keys={row[k] for k in ('id','ref','referent_id') if isinstance(row.get(k),str) and row[k]};need(len(keys)==1,'Native identity ambiguous');native=next(iter(keys))
                            if isinstance(v,dict):need(v.get('lang',v.get('language'))==lang and v.get('text',v.get('value'))==term,'Native term mismatch')
                            else:need(v==term and (pointer.endswith('/label_'+lang) or pointer.split('/')[-2:]==['labels',lang]),'Native language mismatch')
                        else:raise ValueError('Unknown evidence method')
                        need(a['by_kind']['Q' if kind=='entity' else 'P'].get(native)==sid,'Anchor mismatch')
                        opposite=a['by_kind']['P' if kind=='entity' else 'Q'].get(native);need(opposite is None or opposite==sid,'Ambiguous anchor')
                    checked+=1
            # Identifier fallbacks must be exact migration-map references, never manufactured labels.
            for owner,ns in c.execute("SELECT local_directory,namespace_id FROM b.workspace WHERE active=1"):
                mp=owner+'/.kristal/v11/identity-migration-map.json'; pin=c.execute("SELECT sha256 FROM scanned WHERE path=? AND status='ANCHOR'",(mp,)).fetchone()
                expected={}
                if pin:
                    raw=read(mp);need(hashlib.sha256(raw).hexdigest()==pin[0],'Fallback map drift');a=json.loads(raw.decode('utf-8-sig'));need(a['namespace_id']==ns and a['format']=='dik.bulk-secondpass/2','Fallback map scope')
                    for prefix,kind in [('Q','entity'),('P','property')]:
                        for native,sid in a['by_kind'][prefix].items():
                            if c.execute('SELECT 1 FROM display_ref WHERE ns=? AND sid=? AND kind=?',(ns,sid,kind)).fetchone():expected.setdefault(native,[]).append(sid)
                refs={}
                for native,ids in expected.items():
                    if len(set(ids))==1:refs.setdefault(ids[0],[]).append(native)
                for sid,rj in c.execute('SELECT sid,native_json FROM display_ref WHERE ns=?',(ns,)):need(json.loads(rj)==sorted(refs.get(sid,[])),'Fallback reference mismatch')
            # Verify graph reports' exact selected live bytes again.
            for slug,raw in c.execute('SELECT slug,record_json FROM graph_scope'):
                g=json.loads(raw);owner=c.execute('SELECT local_directory FROM b.workspace WHERE slug=?',(slug,)).fetchone()[0]
                need(g['core_graph_registry_crosswalk_qualified'],'Unqualified graph')
                gp=PurePosixPath(g['graph_path']);need(not gp.is_absolute() and '..' not in gp.parts and ':' not in str(gp) and '\\' not in str(gp),'Unsafe graph copy path');copy=base.joinpath(*gp.parts);need(digest(copy)==g['graph_sha256'],'Private graph copy drift '+slug)
                graph=json.loads(copy.read_bytes());ns=c.execute('SELECT ns FROM graph_scope WHERE slug=?',(slug,)).fetchone()[0];rows=list(c.execute('SELECT semantic_id,json_pointer FROM b.v52161_active_assertion WHERE slug=? AND namespace_id=?',(slug,ns)));need(len(rows)==g['assertions']==len(graph['assertions']),'Graph assertion count mismatch')
                for sid,loc in rows:need(ptr(graph,loc).get('id')==sid,'Graph assertion pointer mismatch')
                for rel,h in g['source_pins'].items():need(hashlib.sha256(read(owner+'/'+rel)).hexdigest()==h,'Graph source drift '+slug+'/'+rel)
            need(not c.execute("SELECT 1 FROM alias_review WHERE status<>'HISTORICAL_ALIAS_UNKNOWN' LIMIT 1").fetchone(),'Alias claim not supported')
    finally:
        if z:z.close()
    return {'status':'PASS_PRIVATE_OPERATIONAL_SCOPE','database_sha256':r['database_sha256'],'evidence_pointers_checked':checked,'canonical_qualification_granted':False,'external_authentication_checked':False}
