# Diagnostic levels

## Neutral harness — N00–N06

| Level | Purpose |
|---|---|
| N00 | diagnostic integrity, Python/runtime and evidence schemas |
| N01 | target context, platform, VCS and evidence placement |
| N02 | bounded repository inventory |
| N03 | repository hygiene, broken symlinks, merge markers, large files |
| N04 | tooling/manifests discovery without execution |
| N05 | explicitly declared validators; requires `--allow-exec` |
| N06 | conservative secret/security hygiene scan without copying secret values |

## Kristal semantic conformance — K00–K14

| Level | Purpose |
|---|---|
| K00 | v6/v7 discovery and control boundary |
| K01 | JSON/static integrity and Standard repo surface |
| K02 | `kristal_state/6.0` schema and identity |
| K03 | Kristall v7 manifests/registries/schema coherence |
| K04 | RFC8785/JCS canonicalization and identity |
| K05 | KA assertion families |
| K06 | typed Mesh integrity |
| K07 | KQ axes and subjects |
| K08 | Surface/projection readiness |
| K09 | v6-compatible projection + v7 lineage |
| K10 | semantic resonance boundaries |
| K11 | independent implementation interoperability |
| K12 | determinism and reproducibility |
| K13 | negative/adversarial TCK |
| K14 | conformance/release evidence gate |

## Release engineering — R00–R04

| Level | Purpose |
|---|---|
| R00 | local Markdown links and optional strict MkDocs build |
| R01 | deterministic diagnostic repository snapshot and optional manifest verification |
| R02 | Git cleanliness/tag/version release identity when applicable |
| R03 | signature/trust surface inspection without inventing cryptographic authority |
| R04 | diagnostic contract mirror and profile-level consistency |

R levels are not members of `V7-*` semantic profiles. They are selected by the `release` campaign.
