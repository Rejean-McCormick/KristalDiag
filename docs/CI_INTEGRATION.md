# CI integration

Recommended pull-request gate:

```bash
python -m pip install -e . --no-build-isolation
kristaldiag doctor
kristaldiag conform . --profile V7-Projection --control-dir "$RUNNER_TEMP/kristaldiag"
kristaldiag verify-run "$RUNNER_TEMP/kristaldiag/current/summary.json"
```

Recommended release-candidate gate:

```bash
kristaldiag run release . --control-dir "$RUNNER_TEMP/kristaldiag-release"
kristaldiag verify-run "$RUNNER_TEMP/kristaldiag-release/current/summary.json"
```

If native validators are intentionally declared, add `--allow-exec` only in a reviewed isolated CI job.
