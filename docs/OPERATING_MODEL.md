# Operating model

## Diagnostic mode

Use campaigns when asking “is this repository healthy and well-formed?”

```bash
kristaldiag run baseline TARGET
kristaldiag run standard TARGET
kristaldiag run deep TARGET
kristaldiag run release TARGET
```

## Conformance mode

Use profiles when making a Kristal Standard claim:

```bash
kristaldiag conform TARGET --profile V7-Reader
kristaldiag conform TARGET --profile V7-Mesh
kristaldiag conform TARGET --profile V7-Projection
kristaldiag conform TARGET --profile V7-Kristall --interop-evidence evidence.json
```

A conformance verdict is evidence-bound and non-authoritative.

## Triage mode

```bash
kristaldiag triage-current TARGET
kristaldiag verify-run TARGET/.kristaldiag/current/summary.json
```

## Execution mode

`--allow-exec` is a trust decision, not a convenience switch. Without it, N05 validators and implementation driver actions cannot run.
