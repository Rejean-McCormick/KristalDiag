# KristalDiag v9

[![KristalDiag CI](https://github.com/Rejean-McCormick/KristalDiag/actions/workflows/ci.yml/badge.svg)](https://github.com/Rejean-McCormick/KristalDiag/actions/workflows/ci.yml)

**KristalDiag is the independent diagnostic, conformance and release-qualification suite for Kristal.**

Current target: **Kristal `9.0.0-draft.1`**. It preserves the existing v7 qualification profiles and adds an independent Python qualification surface for Kristal v9 Semantic State Architecture.

```text
Kristal Framework = normative specification + reference implementation
KristalDiag        = independent examiner
```

The v9 commitment implementation in KristalDiag does **not** import or execute the Framework JavaScript commitment code. It independently implements the normative projection, domain separation, JCS and SHA-256 rules and compares its results with the normative golden vectors.

## Quick start

```bash
python -m pip install -e .

kristaldiag doctor --target .
kristaldiag self-test

# Kristal v9
kristaldiag conform /path/to/Kristal-Framework --profile V9-State-Reader
kristaldiag conform /path/to/Kristal-Framework --profile V9-Full

# Historical v7 profiles remain available
kristaldiag conform /path/to/target --profile V7-Projection

# Operational campaigns
kristaldiag run baseline /path/to/target
kristaldiag run v9 /path/to/target
kristaldiag run release /path/to/target
```

## V9 profiles

| Profile | Qualification surface |
|---|---|
| `V9-State-Reader` | schemas, independent commitments, snapshots, polymorphism, negative corpus |
| `V9-Builder` | State Reader + derivations/reproducibility |
| `V9-Materializer` | State Reader + materialization binding |
| `V9-Publisher` | State Reader + Build/Publish/Activate semantics |
| `V9-Full` | Builder + Materializer + Exchange + Publisher + inherited v6/v7/v8 compatibility |

A required `SKIP` is fail-closed by the K14 gate. Qualification never grants execution authority, publication authority, epistemic authority or truth.

## V9 levels

KristalDiag keeps K00–K13 for the historical v6/v7 substrate and K14 as the final gate. V9 adds K15–K24:

```text
K15  machine contracts
K16  independent logical commitments
K17  state snapshot semantics
K18  derivations and reproducibility
K19  materialization binding
K20  exchange binding
K21  build / publish / activate
K22  polymorphic workload corpus
K23  negative and invariance corpus
K24  inherited v6/v7/v8 compatibility substrate
```

## Independent frozen baseline

KristalDiag contains two intentionally separate contract sets:

- its legacy v6/v7 fixtures, retained so historical `V7-*` profiles remain stable;
- `kristaldiag/resources/baseline/9.0.0-draft.1/`, an exact examiner copy of the v6/v7/v8 substrate pinned by Kristal v9's compatibility lock.

This prevents upgrading KristalDiag to v9 from silently rewriting what its older v7 profiles meant.

## Read-only boundary

KristalDiag fingerprints the target before and after qualification. Target code is not imported. Target commands are never guessed. Driver commands execute only with `--allow-exec`, use argv arrays with `shell=False`, and run under bounded timeouts.

Every conformance verdict states:

```json
{
  "qualification_only": true,
  "authority_granted": false
}
```

## Evidence

Each run produces a verifiable evidence bundle under `.kristaldiag/` (or the selected `--control-dir`):

```text
current/
├── effective_config.json
├── levels/<ID>/result.json
├── summary.json
├── summary.txt
├── report.md
├── conformance-verdict.json
└── evidence-manifest.json
```

Verify it independently with:

```bash
kristaldiag verify-run /path/to/current/summary.json
```

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/LEVELS.md`](docs/LEVELS.md)
- [`docs/CONFORMANCE.md`](docs/CONFORMANCE.md)
- [`docs/CI_INTEGRATION.md`](docs/CI_INTEGRATION.md)
- [`docs/DRIVER.md`](docs/DRIVER.md)
- [`docs/SECURITY.md`](docs/SECURITY.md)
- [`docs/REPORTING.md`](docs/REPORTING.md)
- [`docs/CONFIG_REFERENCE.md`](docs/CONFIG_REFERENCE.md)
- [`docs/OPERATING_MODEL.md`](docs/OPERATING_MODEL.md)
- [`docs/KNOWN_FINDINGS.md`](docs/KNOWN_FINDINGS.md)
