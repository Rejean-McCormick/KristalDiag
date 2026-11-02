# Changelog

## 1.0.0-alpha.4 — evidence/CI alignment

- Corrected the persisted level-result schema to allow K25–K32.
- Hardened offline verification of relative evidence paths, symlinks and manifest hashes.
- Added `verify-run --require-pass` for CI conformance gates.
- Required a full immutable Framework commit SHA for manual release audit input.
- Clarified the C1/C2/C3 boundary: no signed qualification, grants or publication.
- Retained the exact `10.0.0-draft.3.1` Framework contract pin and v9 semantics.

## 2026-11-01 — Local maintenance overlay N03/N06

- N03 distinguishes committed/canonical, derived/cache, archived external acquisitions, and unclassified oversized files; the warning remains unless every large file has an exact SHA-256 pinned, locally approved exception.
- N06 adds third-party HTML/MHTML candidate context without downgrading a potential secret, and records skipped oversized text/limited coverage.
- No changes to frozen Framework contract set, check IDs, or conformance qualification semantics.
