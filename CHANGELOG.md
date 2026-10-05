# Changelog

## 0.7.0 — 2026-10-02

- Consolidated `levelupdiag_kristal` 0.6.0 and KristalDiag 0.2.0 into one Kristal v7 diagnostic product.
- Added neutral harness levels N00–N06 for diagnostic integrity, target context, bounded inventory, repository hygiene, tooling discovery, explicitly declared validators and conservative security hygiene.
- Preserved Kristal semantic conformance levels K00–K14 and all v7 profiles (`V7-Reader`, `V7-Mesh`, `V7-Projection`, `V7-Kristall`).
- Added release-engineering levels R00–R04 for docs/link integrity, deterministic snapshots/manifests, Git/release identity, signature/trust surfaces and contract/TCK/profile consistency.
- Added dependency-aware bounded parallel scheduling with fresh-process isolation for each selected N/K/R level.
- Added campaign surface: `baseline`, `standard`, `deep`, `release`.
- Added `--jobs` and `--fail-fast` scheduling controls.
- Added LevelUpDiag compatibility shim for `doctor`, `list`, `show-config`, `run`, and `verify-run` workflows.
- Unified LevelUpDiag-style declared validators with KristalDiag's explicit `--allow-exec` trust boundary.
- Extended verdict model with `INFRA_ERROR`.
- Extended evidence schemas to N/K/R level IDs while keeping offline evidence verification and read-only mutation detection.
- Added release/campaign/config/CI/consolidation documentation.
- Qualified Kristal Standard 7.0.0-draft.2 as `V7-Projection: PASS` with the consolidated harness.
- Ran the new `release` campaign against the Standard: all selected checks passed or were non-applicable except K11 interoperability, yielding the intended `PARTIAL` ratification signal until independent A→B→A evidence exists.

## 0.2.0 — 2026-10-02

- Hardened read-only qualification with complete target-tree fingerprinting.
- Added offline evidence hash/schema verification.
- Made required `SKIP` fail closed at explicit profile gates.

## 0.1.0 — 2026-10-02

- Initial independent Kristal v7 diagnostic/conformance suite.
- K00–K14 levels and v7 profiles.
