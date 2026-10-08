from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from .jcs import canonicalize
from .v9 import verify_declared_state

PUBLICATION_BUNDLE_PROFILE = 'kristal.publication-bundle/1.0'
DIGEST_PREFIX = 'sha256:'


def sha256_bytes(data: bytes) -> str:
    return DIGEST_PREFIX + hashlib.sha256(data).hexdigest()


def publication_identity(*, node_id: str, binding_id: str, state: dict[str, Any], bundle_manifest_digest: str) -> str:
    projection = {
        'node_id': node_id,
        'binding_id': binding_id,
        'state': copy.deepcopy(state),
        'bundle_manifest_digest': bundle_manifest_digest,
    }
    hx = hashlib.sha256(canonicalize(projection).encode('utf-8')).hexdigest()
    return f'urn:kristal:publication:sha256:{hx}'


def _safe_relative(raw: Any) -> bool:
    if not isinstance(raw, str) or not raw:
        return False
    p = Path(raw)
    return not p.is_absolute() and '..' not in p.parts


def _issue(issues: list[dict[str, str]], path: str, code: str, message: str) -> None:
    issues.append({'path': path, 'code': code, 'message': message})


def find_publication_bundles(root: Path, *, max_depth: int = 6) -> list[Path]:
    root = root.resolve()
    if root.is_file():
        root = root.parent
    out: list[Path] = []
    seen: set[Path] = set()
    for pub in root.rglob('publication.json'):
        try:
            rel = pub.relative_to(root)
        except ValueError:
            continue
        if len(rel.parts) > max_depth + 1:
            continue
        bundle = pub.parent.resolve()
        if bundle in seen:
            continue
        if (bundle / 'bundle-manifest.json').is_file() and (bundle / 'state-snapshot.json').is_file():
            seen.add(bundle)
            out.append(bundle)
    return sorted(out, key=lambda p: p.as_posix())


def verify_publication_bundle(bundle_dir: Path) -> dict[str, Any]:
    """Independent Python verification of the non-normative v10 bundle tool format.

    This intentionally does not execute the Kristal JavaScript reference implementation.
    JSON Schema validation of the Publication Record/State is performed by the v10 checks;
    this function verifies byte binding, publication identity, and v9 state commitment.
    """
    bundle = bundle_dir.resolve()
    issues: list[dict[str, str]] = []

    def read_json_file(name: str) -> dict[str, Any] | None:
        p = bundle / name
        try:
            value = json.loads(p.read_text(encoding='utf-8'))
        except Exception as exc:
            _issue(issues, name, 'MISSING_OR_INVALID_RESOURCE', str(exc))
            return None
        if not isinstance(value, dict):
            _issue(issues, name, 'INVALID_TYPE', 'document must be object')
            return None
        return value

    pub = read_json_file('publication.json')
    manifest = read_json_file('bundle-manifest.json')
    state = read_json_file('state-snapshot.json')
    if pub is None or manifest is None or state is None:
        return {'ok': False, 'issues': issues}

    if manifest.get('artifact_type') != 'kristal_publication_bundle_manifest' or manifest.get('profile') != PUBLICATION_BUNDLE_PROFILE:
        _issue(issues, 'bundle-manifest.json', 'UNSUPPORTED_PROFILE', f'expected {PUBLICATION_BUNDLE_PROFILE}')

    payloads = manifest.get('payloads')
    if not isinstance(payloads, list):
        _issue(issues, 'bundle-manifest.json.payloads', 'INVALID_TYPE', 'payloads must be array')
        payloads = []
    for i, resource in enumerate(payloads):
        path = f'bundle-manifest.json.payloads[{i}]'
        if not isinstance(resource, dict):
            _issue(issues, path, 'INVALID_TYPE', 'payload must be object')
            continue
        raw = resource.get('path')
        if not _safe_relative(raw):
            _issue(issues, path + '.path', 'INVALID_PATH', 'payload path must be relative and contained')
            continue
        file = (bundle / str(raw)).resolve()
        try:
            file.relative_to(bundle)
        except ValueError:
            _issue(issues, path + '.path', 'INVALID_PATH', 'payload escapes bundle')
            continue
        if not file.is_file():
            _issue(issues, str(raw), 'MISSING_RESOURCE', 'payload missing')
            continue
        data = file.read_bytes()
        if resource.get('size') != len(data):
            _issue(issues, str(raw), 'SIZE_MISMATCH', f"expected {resource.get('size')}, got {len(data)}")
        got = sha256_bytes(data)
        if resource.get('blob_digest') != got:
            _issue(issues, str(raw), 'DIGEST_MISMATCH', f"expected {resource.get('blob_digest')}, got {got}")

    manifest_bytes = (bundle / 'bundle-manifest.json').read_bytes()
    manifest_digest = sha256_bytes(manifest_bytes)
    extensions = pub.get('extensions') if isinstance(pub.get('extensions'), dict) else {}
    bundle_ext = extensions.get('bundle') if isinstance(extensions.get('bundle'), dict) else {}
    if bundle_ext.get('manifest_blob_digest') != manifest_digest:
        _issue(issues, 'publication.json.extensions.bundle.manifest_blob_digest', 'DIGEST_MISMATCH', 'publication does not bind exact bundle manifest bytes')

    try:
        expected_id = publication_identity(
            node_id=str(pub.get('node_id') or ''),
            binding_id=str(pub.get('binding_id') or ''),
            state=pub.get('state') if isinstance(pub.get('state'), dict) else {},
            bundle_manifest_digest=manifest_digest,
        )
        if pub.get('publication_id') != expected_id:
            _issue(issues, 'publication.json.publication_id', 'DIGEST_MISMATCH', 'publication_id does not match publication identity projection')
    except Exception as exc:
        _issue(issues, 'publication.json.publication_id', 'IDENTITY_ERROR', str(exc))
        expected_id = None

    resources = pub.get('resources')
    if isinstance(resources, list):
        for i, resource in enumerate(resources):
            if not isinstance(resource, dict):
                continue
            locator = resource.get('locator')
            if not isinstance(locator, str) or not locator.startswith('bundle://'):
                continue
            rel = locator[len('bundle://'):]
            if not _safe_relative(rel):
                _issue(issues, f'publication.json.resources[{i}].locator', 'INVALID_PATH', 'bundle locator invalid')
                continue
            file = (bundle / rel).resolve()
            try:
                file.relative_to(bundle)
            except ValueError:
                _issue(issues, f'publication.json.resources[{i}].locator', 'INVALID_PATH', 'bundle locator escapes bundle')
                continue
            if not file.is_file():
                _issue(issues, rel, 'MISSING_RESOURCE', 'publication resource missing')
                continue
            data = file.read_bytes()
            if resource.get('size') != len(data):
                _issue(issues, rel, 'SIZE_MISMATCH', f"expected {resource.get('size')}, got {len(data)}")
            got = sha256_bytes(data)
            if resource.get('blob_digest') != got:
                _issue(issues, rel, 'DIGEST_MISMATCH', f"expected {resource.get('blob_digest')}, got {got}")

    declared_state = pub.get('state') if isinstance(pub.get('state'), dict) else {}
    manifest_state = manifest.get('state') if isinstance(manifest.get('state'), dict) else {}
    snapshot_ref = {
        'state_ref': state.get('state_ref'),
        'logical_commitment': state.get('logical_commitment'),
    }
    if declared_state != manifest_state:
        _issue(issues, 'publication.json.state', 'STATE_BINDING_MISMATCH', 'publication state does not match bundle manifest state')
    if declared_state != snapshot_ref:
        _issue(issues, 'state-snapshot.json', 'STATE_BINDING_MISMATCH', 'publication state does not match bundled state snapshot')

    ok_state, actual_state, state_errors = verify_declared_state(state)
    if not ok_state:
        _issue(issues, 'state-snapshot.json.logical_commitment', 'STATE_COMMITMENT_MISMATCH', '; '.join(state_errors))
    elif declared_state.get('logical_commitment') != actual_state:
        _issue(issues, 'publication.json.state.logical_commitment', 'STATE_COMMITMENT_MISMATCH', 'publication does not bind independently recomputed v9 state commitment')

    return {
        'ok': not issues,
        'issues': issues,
        'publication_id': pub.get('publication_id'),
        'expected_publication_id': expected_id,
        'bundle_manifest_digest': manifest_digest,
        'state': declared_state,
    }
