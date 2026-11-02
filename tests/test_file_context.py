from pathlib import Path
from types import SimpleNamespace
from kristaldiag.config import load_config
from kristaldiag.neutral import n03,n06
from kristaldiag.file_context import classify_large_file,approved_exception
from hashlib import sha256

ROOT=Path(__file__).resolve().parents[1]

def ctx_for(path,**config):
    cfg=load_config(ROOT,path,control_dir=path.parent/'logs')
    cfg.data['scan'].update({'large_file_bytes':10,'max_file_bytes':2048,'max_security_files':20})
    cfg.data.update(config)
    return SimpleNamespace(scan_root=path,target=path,config=cfg)

def finding(result,ident):
    return next(f for f in result.findings if f.id==ident)

def test_role_classifications_no_guessing():
    assert classify_large_file('canon/domain/graph.json')['role']=='canonical_or_committed'
    assert classify_large_file('derived/wikidata/read.sqlite3')['role']=='derived_or_cache'
    assert classify_large_file('knowledge-base/corpus/large.json')['role']=='canonical_or_committed'
    assert classify_large_file('.kristal/v8/portable-state.kristal-state.json')['role']=='canonical_or_committed'
    assert classify_large_file('external-source-library/snapshots/x/page.mhtml')['role']=='external_source_archive'
    assert classify_large_file('unknown/large.bin')['role']=='unclassified'

def test_large_warning_retained_without_strict_exception(tmp_path):
    root=tmp_path/'workspace';(root/'canon').mkdir(parents=True)
    (root/'derived').mkdir()
    (root/'canon/graph.json').write_text('x'*100)
    (root/'derived/read.sqlite3').write_text('x'*120)
    result=n03(ctx_for(root));entry=finding(result,'N03-LARGE-003')
    assert entry.verdict=='WARN'
    assert {item['role'] for item in entry.evidence}=={'canonical_or_committed','derived_or_cache'}
    assert result.metadata['large_files_pending_review']==2

def test_sha_pinned_exception_and_mutation_reverts_to_warn(tmp_path):
    root=tmp_path/'workspace';root.mkdir()
    file=root/'big.json';file.write_text('abc'*40)
    digest=sha256(file.read_bytes()).hexdigest()
    policy={'exceptions':[{'path':'big.json','status':'approved','bytes':file.stat().st_size,
                           'sha256':'sha256:'+digest,'reason':'Verified source backup retained',
                           'reviewed_by':'quality-reviewer'}]}
    config=ctx_for(root,large_files=policy)
    assert finding(n03(config),'N03-LARGE-003').verdict=='PASS'
    file.write_text('def'*40)
    assert finding(n03(config),'N03-LARGE-003').verdict=='WARN'

def test_html_context_warns_without_exposing_key(tmp_path):
    root=tmp_path/'workspace';(root/'archive').mkdir(parents=True)
    secret='A'*40
    (root/'archive/third-party.html').write_text('<html><script>apiKey="'+secret+'"</script></html>')
    result=n06(ctx_for(root));finding_n06=finding(result,'N06-SECRETS-002')
    assert finding_n06.verdict=='WARN'
    entry=finding_n06.evidence[0]
    assert entry['third_party_archive_candidate'] is True
    assert entry['values_included'] is False
    assert secret not in str(finding_n06.to_dict())


def test_security_coverage_is_explicit_when_huge_file_skipped(tmp_path):
    root=tmp_path/'workspace';root.mkdir()
    (root/'large.html').write_text('x'*5000)
    result=n06(ctx_for(root))
    assert result.metadata['text_skipped_oversized']==1
    assert result.metadata['coverage_limited'] is True
    assert finding(result,'N06-SECRETS-002').verdict=='PASS'
