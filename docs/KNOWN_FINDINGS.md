# Known findings

## KF-001 — inherited v7 portable projection carries a stale v6 identity

Status: **open in the supplied `9.0.0-draft.1` Framework snapshot**.

KristalDiag K24 independently recomputes the frozen v6 identity of:

`TCK/v7/vectors/v6-compatible-projection.example.json`

The artifact declares:

```text
sha256:534d57141a4d1c982e2ddb25abfda19be7d63234667542dd3eea6acc5cf6b759
```

After applying the frozen v6 hash boundary — exclude only `state_id`, `content_hash` and `signatures`, then RFC 8785/JCS + SHA-256 — KristalDiag obtains:

```text
sha256:9f3fdad6b298e47a3f8750f418899f9208c4e3691f20233648abde2e2188bd79
```

The difference is explained by `extensions.kristal_v7`: the projection retained the base state identity after adding the extension. Under the current frozen v6 identity rule, the extension is inside the hash target.

KristalDiag deliberately reports this as `K24-IDENTITY-003 FAIL`. It does not choose a new rule on behalf of the Standard. The Framework must resolve the inconsistency explicitly before final v9 qualification, then preserve the chosen behavior with a regression vector.
