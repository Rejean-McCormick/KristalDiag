# Diagnostic levels

## Neutral harness — N00–N06

| Level | Purpose |
|---|---|
| N00 | diagnostic integrity, runtime and evidence schemas |
| N01 | target context, platform, VCS and evidence placement |
| N02 | bounded repository inventory |
| N03 | repository hygiene, merge markers, symlink and large-file checks |
| N04 | tooling/manifests discovery without execution |
| N05 | explicitly declared validators; requires `--allow-exec` |
| N06 | conservative secret/security hygiene scan |

## Historical Kristal substrate — K00–K13

| Level | Purpose |
|---|---|
| K00 | control boundary, examiner resource integrity and discovery |
| K01 | JSON/static integrity and Standard repository surface |
| K02 | `kristal_state/6.0` schema and canonical identity |
| K03 | Kristall v7 manifests/registries/schema coherence |
| K04 | RFC8785/JCS canonicalization and identity |
| K05 | assertion families |
| K06 | typed Mesh integrity |
| K07 | axes and subjects |
| K08 | Surface/projection readiness |
| K09 | v6-compatible projection and v7 lineage |
| K10 | semantic-resonance boundaries |
| K11 | external implementation interoperability |
| K12 | determinism and reproducibility |
| K13 | historical negative/adversarial corpus |

## Final gate — K14

K14 is produced by the parent runner after all selected levels. It fail-closes required `SKIP` evidence and also enforces the read-only target fingerprint guard.

## Kristal v9 — K15–K24

| Level | Purpose |
|---|---|
| K15 | validate all discovered v9 machine contracts and capabilities |
| K16 | independently reproduce v9 artifact/state commitments and golden vectors |
| K17 | immutable State Snapshot membership, pinning and commitment semantics |
| K18 | derivation binding and reproducibility claims |
| K19 | materialization/source commitment binding and reconstructability |
| K20 | Exchange-to-State binding |
| K21 | activation/lifecycle consistency and independent CAS corpus |
| K22 | polymorphic workload gate: relation, DAG, multiplex graph, AST, epistemic corpus, federation |
| K23 | negative/invariance corpus for included/excluded commitment fields and ordering |
| K24 | exact inherited v6/v7/v8 compatibility baseline + Standard compatibility-lock audit |

## Release engineering — R00–R04

| Level | Purpose |
|---|---|
| R00 | local Markdown links and optional strict MkDocs build |
| R01 | deterministic diagnostic snapshot and repository manifest verification |
| R02 | Git cleanliness/tag/version release identity |
| R03 | signature/trust surface inspection without inventing authority |
| R04 | vendored contract/TCK integrity and profile-level consistency |
