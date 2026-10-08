from __future__ import annotations
import copy,json,shutil
from pathlib import Path

from kristaldiag.config import load_config
from kristaldiag.runner import run
from kristaldiag.schemas import SchemaStore
from kristaldiag.v10 import publication_identity, verify_publication_bundle

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'kristaldiag'/'resources'


def _fixture(tmp_path:Path)->Path:
    target=tmp_path/'v10';target.mkdir()
    for q in sorted((RES/'tck/v9/vectors').glob('*.json')):
        if q.name!='logical-commitment-vectors.json':shutil.copy2(q,target/q.name)
    for q in sorted((RES/'tck/v9/workloads').glob('*.json')):shutil.copy2(q,target/q.name)
    kr=target/'.kristal';(kr/'bindings').mkdir(parents=True)
    shutil.copy2(RES/'tck/v10/vectors/node-manifest.example.json',kr/'node.json')
    shutil.copy2(RES/'tck/v10/vectors/github-binding.example.json',kr/'bindings/github.json')
    shutil.copy2(RES/'tck/v10/vectors/v10-capabilities.example.json',kr/'capabilities.json')
    shutil.copy2(RES/'tck/v10/vectors/directory.example.json',kr/'directory.json')
    shutil.copytree(RES/'tck/v10/bundle',target/'publication')
    return target


def test_v10_vectors_validate_against_examiner_contracts():
    store=SchemaStore(ROOT)
    for p in sorted((ROOT/'tck/v10/vectors').glob('*.json')):
        d=json.loads(p.read_text())
        ok,errors=store.validate_v10(d)
        assert ok,(p.name,errors)
        if d.get('artifact_type')=='kristal_host_binding':
            ok,errors=store.validate_github_binding(d);assert ok,errors


def test_v10_bundle_verifies_and_tamper_is_detected(tmp_path):
    src=RES/'tck/v10/bundle';dst=tmp_path/'bundle';shutil.copytree(src,dst)
    good=verify_publication_bundle(dst);assert good['ok'],good
    (dst/'state-snapshot.json').write_bytes((dst/'state-snapshot.json').read_bytes()+b' ')
    bad=verify_publication_bundle(dst)
    assert not bad['ok']
    assert any(x['code'] in {'DIGEST_MISMATCH','SIZE_MISMATCH','STATE_COMMITMENT_MISMATCH'} for x in bad['issues'])


def test_publication_identity_binds_bundle_manifest_digest():
    pub=json.loads((RES/'tck/v10/bundle/publication.json').read_text())
    state=pub['state']
    a=publication_identity(node_id=pub['node_id'],binding_id=pub['binding_id'],state=state,bundle_manifest_digest='sha256:'+'1'*64)
    b=publication_identity(node_id=pub['node_id'],binding_id=pub['binding_id'],state=state,bundle_manifest_digest='sha256:'+'2'*64)
    assert a!=b


def test_negative_contract_cases_fail_structured_validation():
    store=SchemaStore(ROOT)
    node=json.loads((ROOT/'tck/v10/vectors/node-manifest.example.json').read_text());node['roles']=['bad'];node['bindings']=[None]
    ok,errors=store.validate_v10(node);assert not ok and errors
    pub=json.loads((ROOT/'tck/v10/vectors/publication.example.json').read_text());pub['resources']=[{}]
    ok,errors=store.validate_v10(pub);assert not ok and errors
    directory=json.loads((ROOT/'tck/v10/vectors/directory.example.json').read_text());directory['entries']={}
    ok,errors=store.validate_v10(directory);assert not ok and errors


def test_v10_full_reference_fixture_passes(tmp_path,monkeypatch):
    monkeypatch.setenv('KRISTALDIAG_TEST_IN_PROCESS','1')
    target=_fixture(tmp_path);cfg=load_config(ROOT,target,control_dir=tmp_path/'evidence')
    summary,code,current=run(target,cfg,profile='V10-Full',repo_root=ROOT)
    assert code==0, (summary,(current/'summary.txt').read_text())
    assert summary['verdict']=='PASS'
    ids={x['id'] for x in summary['levels']}
    for lid in ('K25','K26','K27','K28','K30','K31'):assert lid in ids


def test_v10_github_host_reference_fixture_passes(tmp_path,monkeypatch):
    monkeypatch.setenv('KRISTALDIAG_TEST_IN_PROCESS','1')
    target=_fixture(tmp_path);cfg=load_config(ROOT,target,control_dir=tmp_path/'evidence')
    summary,code,current=run(target,cfg,profile='V10-GitHub-Host',repo_root=ROOT)
    assert code==0,(summary,(current/'summary.txt').read_text())
    assert next(x for x in summary['levels'] if x['id']=='K29')['verdict']=='PASS'

def test_v10_standard_profile_checks_release_contract_set(tmp_path,monkeypatch):
    monkeypatch.setenv('KRISTALDIAG_TEST_IN_PROCESS','1')
    target=_fixture(tmp_path)
    contracts=target/'contracts';contracts.mkdir()
    shutil.copy2(RES/'locks/release.json',contracts/'release.json')
    shutil.copy2(RES/'locks/contract-set.json',contracts/'contract-set.json')
    cfg=load_config(ROOT,target,control_dir=tmp_path/'evidence-standard')
    summary,code,current=run(target,cfg,profile='V10-Standard',repo_root=ROOT)
    assert code==0,(summary,(current/'summary.txt').read_text())
    assert next(x for x in summary['levels'] if x['id']=='K32')['verdict']=='PASS'
