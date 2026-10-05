# Architecture

KristalDiag v7 combines the external-harness model of LevelUpDiag with the normative v7 examiner built in KristalDiag.

```text
CLI / compatibility shim
        |
        v
campaign / profile selector
        |
        v
manifest + dependency DAG
        |
        +---- bounded scheduler ----+
        |                            |
    fresh worker                 fresh worker
    process N/K/R                process N/K/R
        |                            |
        +-------------+--------------+
                      v
               persisted evidence
                      |
                      v
              K14 conformance gate
                      |
                      v
       summary + report + evidence hashes
```

## Dependency direction

```text
KristalDiag source/resources
        ↓
read-only target discovery
        ↓
N-level generic diagnostics
        ↓
K-level Kristal semantics
        ↓
optional R-level release evidence
        ↓
K14 qualification verdict
```

The harness is not an implementation of Kristal. When implementation execution is needed, it occurs only through explicit configured validators or `kristaldiag-driver.json` actions with `--allow-exec`.

## Process isolation

N00–N06, K00–K13 and R00–R04 run in separate processes by default. The parent scheduler owns ordering, dependency blocking, timeouts, evidence collection, mutation detection and K14.

`parallel_safe=false` levels execute exclusively. Presentation order is not dependency semantics; `depends_on` is.

## Evidence trust boundary

Vendored schemas/TCK resources are hashed by `contract-manifest.json`. Target files are untrusted input. Target Python/JS code is never imported. The target tree is content-fingerprinted before and after qualification.

## Semantic versus release evidence

V7 profiles depend on N + K levels only. R levels can block a release campaign without changing whether an artifact satisfies the semantic profile itself.
