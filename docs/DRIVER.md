# Implementation driver

Artifact validation is fully read-only. Runtime interoperability needs a narrow opt-in bridge.

A target may provide `kristaldiag-driver.json`:

```json
{
  "schema": "kristaldiag.driver.v1",
  "implementation": "My implementation",
  "claimed_profile": "V7-Kristall",
  "actions": {
    "self_test": {"argv": ["python", "-m", "myimpl", "self-test"]}
  }
}
```

KristalDiag never invokes these actions unless `--allow-exec` is supplied. Commands are direct argv arrays; shell interpolation is not supported.

The driver boundary is designed to grow toward full A->B->A cross-implementation exchange tests without making arbitrary target execution the default.

## Independent A -> B -> A interop

Two implementations can be tested directly:

```bash
kristaldiag interop ./impl-a ./impl-b --allow-exec --output interop.json
kristaldiag conform ./impl-a --profile V7-Kristall --interop-evidence interop.json
```

Both drivers must expose `interop_export` and `interop_import`. `interop_export` emits either a raw JSON artifact, `{ "artifact": {...} }`, or `{ "artifact_path": "..." }`. `interop_import` receives the artifact path through `KRISTALDIAG_INPUT`.

KristalDiag validates both exported artifacts against the vendored v6/v7 schemas and requires the A->B->A round trip to preserve artifact type, schema version, and semantic identity.
