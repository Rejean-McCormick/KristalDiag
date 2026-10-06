# Architecture

KristalDiag is an independent examiner. It is intentionally not linked into the Kristal Framework implementation.

```text
             Kristal Framework / target
                      │
                untrusted input
                      │
                      ▼
       discovery + JSON/schema validation
                      │
       ┌──────────────┴──────────────┐
       ▼                             ▼
 historical substrate          v9 examiner
 K00–K13                      K15–K24
                                     │
                                     ├─ independent Python commitments
                                     ├─ frozen compatibility baseline
                                     ├─ polymorphic workloads
                                     └─ adversarial corpus
       └──────────────┬──────────────┘
                      ▼
                 K14 final gate
                      │
                      ▼
             signed/hashable evidence
```

## Independent commitment implementation

`kristaldiag/v9.py` implements the normative v9 logical projections, ordering, domain separators, JCS and SHA-256 in Python. It does not call `reference/js/src/v9/*` from the Framework. K16 compares the result with the normative golden vectors, while K23 checks invariants that are easy for two implementations to accidentally interpret differently.

## Dual historical baselines

The repo intentionally retains the older v6/v7 fixtures used by historical `V7-*` profiles. Separately, `kristaldiag/resources/baseline/9.0.0-draft.1/` is an exact copy of the inherited v6/v7/v8 substrate pinned by the v9 Standard. K24 uses that baseline for v9 compatibility qualification.

## Isolation

Selected levels execute in fresh Python processes by default. Dependencies are explicit and independent levels can run concurrently. The parent process owns ordering, dependency blocking, timeouts, evidence collection, mutation detection and the K14 gate.

## Authority boundary

Target JSON is data. Target source code is not imported. No discovered instruction can grant KristalDiag permission to execute or mutate the target. Execution is opt-in through a narrow driver or explicitly declared validator and `--allow-exec`.
