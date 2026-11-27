"""Independent read-only check of the maintenance receipt and exact scoped anchors."""
import sys,sqlite3,json,hashlib,zipfile,stat
from pathlib import Path,PurePosixPath
from contextlib import closing

def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def exact_pointer(doc,pointer):
    for token in pointer.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        doc=doc[int(token)] if isinstance(doc,list) else doc[token]
    return doc

def check_sources(db,root):
    root=Path(root);z=zipfile.ZipFile(root) if root.is_file() else None
    try:
        def read(rel):
            p=PurePosixPath(rel)
            require(not p.is_absolute() and '..' not in p.parts and '\\' not in rel and ':' not in rel,'Unsafe source path')
            if z:
                i=z.getinfo(rel);require(not stat.S_ISLNK(i.external_attr>>16),'Linked ZIP member');return z.read(i)
            path=root.joinpath(*p.parts)
            for x in [*path.absolute().parents,path.absolute()]:
                st=x.lstat();require(not stat.S_ISLNK(st.st_mode) and not getattr(st,'st_file_attributes',0)&0x400,'Linked source path')
            return path.read_bytes()
        for path,sha in db.execute('SELECT path,sha256 FROM source'):
            raw=read(path);require(hashlib.sha256(raw).hexdigest()==sha,'Source digest drift: '+path);doc=json.loads(raw.decode('utf-8-sig'))
            for ns,native,sid,kind in db.execute('SELECT a.ns,a.native_id,a.sid,t.kind FROM anchor a JOIN target t ON t.ns=a.ns AND t.sid=a.sid WHERE a.path=?',(path,)):
                require(doc['namespace_id']==ns and doc['by_kind']['Q' if kind=='entity' else 'P'][native]==sid,'Map scope or identity mismatch')
            for ns,sid,lang,term,native,pointer,method in db.execute('SELECT ns,sid,lang,term,native_id,pointer,method FROM observation WHERE path=?',(path,)):
                value=exact_pointer(doc,pointer)
                if method=='LEGACY_V8':
                    row=exact_pointer(doc,pointer.rsplit('/',1)[0]);require(row['semantic_ref']['id']==native and row['semantic_ref']['identity_space']=='kristal_v6' and doc['language']==lang and value==term,'Legacy lexical pointer mismatch')
                elif method=='NATIVE_REGISTRY':
                    row=exact_pointer(doc,'/'.join(pointer.split('/')[:3]));keys={row[k] for k in ('id','ref','referent_id') if isinstance(row.get(k),str) and row[k]};require(keys=={native},'Native referent mismatch')
                    if isinstance(value,dict):require(value.get('lang',value.get('language'))==lang and value.get('text',value.get('value'))==term,'Native label mismatch')
                    else:require(value==term and (pointer.endswith('/label_'+lang) or pointer.split('/')[-2:] == ['labels',lang]),'Native label language mismatch')
                else:raise ValueError('Unknown method')
    finally:
        if z:z.close()

def check(output,base,root=None):
    output,base=Path(output),Path(base);r=json.loads((output/'report.json').read_bytes());dbp=output/'maintenance.sqlite';src=base/'active.sqlite'
    require(r['maintenance_database_sha256']==digest(dbp),'Maintenance database drift');require(r['base_database_sha256']==digest(src),'Baseline drift')
    with closing(sqlite3.connect(dbp.resolve().as_uri()+'?mode=ro',uri=True)) as db:
        db.execute('ATTACH DATABASE ? AS base',(src.resolve().as_uri()+'?mode=ro',))
        require(db.execute('PRAGMA integrity_check').fetchone()==('ok',),'SQLite integrity')
        q="SELECT namespace_id,semantic_id,owner_slug,kind FROM base.identity i WHERE kind IN ('entity','property') AND NOT EXISTS(SELECT 1 FROM base.lexical l WHERE l.namespace_id=i.namespace_id AND l.semantic_id=i.semantic_id)"
        for a,b in [('SELECT ns,sid,slug,kind FROM target',q),(q,'SELECT ns,sid,slug,kind FROM target')]:require(not db.execute(a+' EXCEPT '+b+' LIMIT 1').fetchone(),'Target scope drift')
        require(not db.execute('SELECT 1 FROM observation o LEFT JOIN anchor a ON a.ns=o.ns AND a.sid=o.sid AND a.native_id=o.native_id LEFT JOIN source s ON s.path=o.path AND s.sha256=o.sha256 LEFT JOIN target t ON t.ns=o.ns AND t.sid=o.sid WHERE a.sid IS NULL OR s.path IS NULL OR t.sid IS NULL LIMIT 1').fetchone(),'Observation lacks exact scoped anchor')
        require(not db.execute('SELECT 1 FROM anchor a LEFT JOIN source s ON s.path=a.path AND s.sha256=a.sha256 LEFT JOIN target t ON t.ns=a.ns AND t.sid=a.sid WHERE s.path IS NULL OR t.sid IS NULL LIMIT 1').fetchone(),'Anchor source or target missing')
        for table in ('anchor','observation'):
            require(not db.execute(f"SELECT 1 FROM {table} a JOIN target t ON t.ns=a.ns AND t.sid=a.sid JOIN base.workspace w ON w.slug=t.slug WHERE substr(a.path,1,length(w.local_directory)+1)<>w.local_directory||'/' LIMIT 1").fetchone(),'Source outside owning workspace')
        actual={}
        for ns,sid,lang,terms in db.execute('SELECT ns,sid,lang,json_group_array(DISTINCT term) FROM observation GROUP BY ns,sid,lang'):
            v=sorted(json.loads(terms));actual[(ns,sid,lang)]=('PRIVATE_EXACT_ANCHOR_CONSENSUS' if len(v)==1 else 'CONFLICT',v[0] if len(v)==1 else None,v)
        rows={(ns,sid,lang):(status,term,json.loads(v)) for ns,sid,lang,status,term,v in db.execute('SELECT * FROM resolution')}
        require(rows==actual,'Resolution does not preserve exact variants')
        require(r['counts']['targets']==db.execute('SELECT count(*) FROM target').fetchone()[0],'Target count mismatch')
        require(r['counts']['observations']==db.execute('SELECT count(*) FROM observation').fetchone()[0],'Observation count mismatch')
        if root is not None:check_sources(db,root)
        require(all(r['policy'][k] in (False,0) for k in ('canonical_modified','public_modified','external_links_accepted','labels_promoted','network_used','historical_aliases_invented')),'Policy mismatch')
    return {'status':'PASS_PRIVATE_RECEIPT_SCOPE','source_bytes_and_pointers_checked':root is not None,'scope':'SQLite integrity, target set, anchor linkage, exact consensus and receipt hashes; not semantic approval','database_sha256':r['maintenance_database_sha256']}
if __name__=='__main__':
    report=check(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else None);p=Path(sys.argv[1])/'diagnostic.json';p.write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report))
