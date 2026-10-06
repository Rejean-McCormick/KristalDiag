# CI integration

KristalDiag CI has two roles.

## Self qualification

The Python matrix runs unit tests and `kristaldiag self-test`. The self-test builds a clean v9 fixture from vendored vectors/workloads and requires `V9-Full` PASS without importing Framework code.

## Independent Framework gate

A separate job checks out KristalDiag and Kristal-Framework independently, records both exact commits, then runs:

```bash
kristaldiag conform Kristal-Framework \
  --profile V9-Full \
  --control-dir "$RUNNER_TEMP/kristaldiag-v9"
```

Evidence is verified with `verify-run` before upload.

During draft development the workflow may track a branch such as `main`, but it records the resolved Framework SHA. Before an RC/final release, the Framework reference should be pinned to an immutable commit/tag.

## Release audit

The manual release audit runs the broad `release` campaign, verifies evidence integrity and retains the complete evidence bundle. A disagreement between Framework native CI and KristalDiag must remain visible; neither side silently converts the other into a warning merely to obtain a green release.
