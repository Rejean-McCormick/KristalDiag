from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

from . import REPORT_SCHEMA, SUMMARY_SCHEMA, VERDICT_SCHEMA
from .utils import read_json, sha256_file


def _schema(repo_root: Path, name: str) -> dict[str, Any]:
    return read_json(repo_root / 'schemas' / name)


def _validate(schema: dict[str, Any], payload: Any) -> list[str]:
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    out: list[str] = []
    for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.absolute_path)):
        path = '/' + '/'.join(str(x) for x in err.absolute_path) if err.absolute_path else '/'
        out.append(f'{path}: {err.message}')
    return out


def verify_run(summary_path: Path, repo_root: Path) -> tuple[bool, dict[str, Any]]:
    """Verify a persisted KristalDiag evidence tree without executing the target."""
    summary_path = summary_path.resolve()
    root = summary_path.parent
    problems: list[dict[str, Any]] = []

    try:
        summary = read_json(summary_path)
    except Exception as exc:
        return False, {'valid': False, 'problems': [{'kind': 'summary-read', 'detail': f'{type(exc).__name__}: {exc}'}]}

    if summary.get('schema') != SUMMARY_SCHEMA:
        problems.append({'kind': 'summary-schema-id', 'expected': SUMMARY_SCHEMA, 'observed': summary.get('schema')})
    for err in _validate(_schema(repo_root, 'summary.schema.json'), summary):
        problems.append({'kind': 'summary-schema', 'detail': err})

    run_id = summary.get('run_id')
    level_schema = _schema(repo_root, 'level-result.schema.json')
    for row in summary.get('levels', []):
        rel = row.get('result')
        if not isinstance(rel, str) or not rel:
            problems.append({'kind': 'level-result-path', 'level': row.get('id')})
            continue
        p = root / rel
        if not p.is_file():
            problems.append({'kind': 'missing-level-result', 'path': rel})
            continue
        try:
            payload = read_json(p)
        except Exception as exc:
            problems.append({'kind': 'level-read', 'path': rel, 'detail': f'{type(exc).__name__}: {exc}'})
            continue
        if payload.get('schema') != REPORT_SCHEMA:
            problems.append({'kind': 'level-schema-id', 'path': rel, 'expected': REPORT_SCHEMA, 'observed': payload.get('schema')})
        for err in _validate(level_schema, payload):
            problems.append({'kind': 'level-schema', 'path': rel, 'detail': err})
        if payload.get('run_id') != run_id:
            problems.append({'kind': 'run-id-mismatch', 'path': rel, 'expected': run_id, 'observed': payload.get('run_id')})
        if payload.get('level_id') != row.get('id'):
            problems.append({'kind': 'level-id-mismatch', 'path': rel, 'expected': row.get('id'), 'observed': payload.get('level_id')})
        if payload.get('verdict') != row.get('verdict'):
            problems.append({'kind': 'level-verdict-mismatch', 'path': rel, 'expected': row.get('verdict'), 'observed': payload.get('verdict')})

    verdict_path = root / 'conformance-verdict.json'
    if not verdict_path.is_file():
        problems.append({'kind': 'missing-conformance-verdict', 'path': 'conformance-verdict.json'})
    else:
        try:
            verdict = read_json(verdict_path)
            if verdict.get('schema') != VERDICT_SCHEMA:
                problems.append({'kind': 'verdict-schema-id', 'expected': VERDICT_SCHEMA, 'observed': verdict.get('schema')})
            for err in _validate(_schema(repo_root, 'conformance-verdict.schema.json'), verdict):
                problems.append({'kind': 'verdict-schema', 'detail': err})
            if verdict.get('run_id') != run_id:
                problems.append({'kind': 'verdict-run-id-mismatch', 'expected': run_id, 'observed': verdict.get('run_id')})
            if verdict.get('verdict') != summary.get('verdict'):
                problems.append({'kind': 'summary-verdict-mismatch', 'summary': summary.get('verdict'), 'conformance': verdict.get('verdict')})
        except Exception as exc:
            problems.append({'kind': 'verdict-read', 'detail': f'{type(exc).__name__}: {exc}'})

    manifest_path = root / 'evidence-manifest.json'
    if not manifest_path.is_file():
        problems.append({'kind': 'missing-evidence-manifest', 'path': 'evidence-manifest.json'})
    else:
        try:
            manifest = read_json(manifest_path)
            if manifest.get('schema') != 'kristaldiag.evidence-manifest.v1':
                problems.append({'kind': 'evidence-manifest-schema', 'observed': manifest.get('schema')})
            if manifest.get('run_id') != run_id:
                problems.append({'kind': 'manifest-run-id-mismatch', 'expected': run_id, 'observed': manifest.get('run_id')})
            files = manifest.get('files') or {}
            if not isinstance(files, dict):
                problems.append({'kind': 'manifest-files-type'})
                files = {}
            for rel, expected in sorted(files.items()):
                p = root / rel
                if not p.is_file():
                    problems.append({'kind': 'manifest-missing-file', 'path': rel})
                    continue
                observed = sha256_file(p)
                if observed != expected:
                    problems.append({'kind': 'manifest-hash-mismatch', 'path': rel, 'expected': expected, 'observed': observed})
            actual = {
                p.relative_to(root).as_posix()
                for p in root.rglob('*')
                if p.is_file() and p.name != 'evidence-manifest.json'
            }
            declared = set(files)
            for rel in sorted(actual - declared):
                problems.append({'kind': 'manifest-untracked-file', 'path': rel})
            for rel in sorted(declared - actual):
                if not any(x.get('kind') == 'manifest-missing-file' and x.get('path') == rel for x in problems):
                    problems.append({'kind': 'manifest-missing-file', 'path': rel})
        except Exception as exc:
            problems.append({'kind': 'manifest-read', 'detail': f'{type(exc).__name__}: {exc}'})

    return not problems, {'valid': not problems, 'run_id': run_id, 'problems': problems}
