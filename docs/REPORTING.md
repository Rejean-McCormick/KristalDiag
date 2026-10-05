# Reporting and evidence

Each run writes an immutable-style evidence tree under `.kristaldiag/current/` and copies it to `.kristaldiag/runs/<run_id>/`.

```text
current/
├── effective_config.json
├── levels/<level-id>/result.json
├── summary.json
├── summary.txt
├── report.md
├── conformance-verdict.json
└── evidence-manifest.json
```

`summary.json` aggregates level status. `conformance-verdict.json` is the bounded qualification statement. `evidence-manifest.json` hashes every other persisted evidence file.

`verify-run` performs offline verification of schemas, run identifiers, level/verdict consistency and SHA-256 evidence hashes.

Verdicts: `PASS`, `WARN`, `FAIL`, `SKIP`, `BLOCKED`, `PARTIAL`, `ERROR`, `INFRA_ERROR`, `CONFIG_ERROR`.

An optional level that executes and observes a real `FAIL` still fails the diagnostic campaign. “Optional” changes completeness requirements, not observed truth.
