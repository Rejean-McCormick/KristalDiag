# KristalDiag 0.7.0 — Validation report

Date: 2026-10-02  
Target standard: Kristal Standard `7.0.0-draft.2`

## Consolidation scope

This release consolidates the mature external-harness mechanisms from `levelupdiag_kristal` 0.6.0 with the v7 semantic examiner introduced by KristalDiag 0.2.0.

The resulting level space is:

- N00–N06 neutral harness/repository diagnostics;
- K00–K14 Kristal semantic conformance;
- R00–R04 release-engineering evidence.

## Automated release checks

The source tree was validated with:

- Python bytecode compilation;
- 21 pytest tests;
- byte-for-byte verification of vendored Kristal contracts/TCK mirrors;
- local Markdown link verification;
- built-in self-test using the default isolated-process scheduler;
- process-isolation scheduler regression coverage;
- campaign/profile and LevelUpDiag compatibility tests;
- generated repository SHA-256 manifest.

All automated release checks passed.

## Standard v7 qualification

The consolidated tool was run against the packaged Kristal Standard `7.0.0-draft.2` repository.

### `V7-Projection`

Result: **PASS**.

Neutral levels N00/N01/N02/N03/N04/N06 and required semantic levels K00–K10/K12/K13 passed. K14 therefore issued a `PASS` `V7-Projection` qualification.

The evidence tree subsequently passed `kristaldiag verify-run`.

### `release` campaign

Result: **PARTIAL**.

Observed results:

- N00–N06: PASS;
- K00–K10, K12, K13: PASS;
- K11 interoperability: PARTIAL (no independent A→B→A execution evidence supplied);
- R00 documentation/link integrity: PASS;
- R01 snapshot/manifest reproducibility: PASS;
- R02 Git/release identity: SKIP for the extracted release archive (not a Git worktree);
- R03 signature/trust surface: SKIP where no signed portable state is present;
- R04 contract/TCK/profile consistency: PASS.

The `PARTIAL` release verdict is intentional: the suite does not promote an otherwise healthy release to full ratification while independent interoperability evidence is still absent.

## Evidence integrity

Both persisted Standard-v7 evidence trees passed offline `verify-run` validation, including schema coherence, run/level identity checks and all evidence-manifest SHA-256 hashes.

## Security / authority boundary

KristalDiag remains read-oriented and emits:

```json
{
  "qualification_only": true,
  "authority_granted": false
}
```

Target execution requires explicit `--allow-exec`; target mutation is detected by full-tree fingerprinting and invalidates the run unless mutation was explicitly configured for a diagnostic validator.
