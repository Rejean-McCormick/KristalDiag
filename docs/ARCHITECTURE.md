# Architecture

KristalDiag is an **external, independent, read-only examiner**.

```text
KristalV10 / Local Kristal / publication bundle
                    │
                    ▼ read only
               KristalDiag
                    │
                    ▼
          qualification evidence
```

It is deliberately outside the lifecycle ownership chain:

```text
Kristal Manager          -> local inventory + backup
Kristal GitHub Setup     -> bootstrap + qualify/publish/activate
Kompiler                 -> optional context compilation
KristalDiag               -> independent examination only
```

## Examiner independence

The target's own `schemas/` are inventory/audit evidence, not the schemas used to qualify that target. SchemaStore uses frozen packaged examiner contracts. The exact examiner resources are protected by `contract-manifest.json`.

V9 commitments are recomputed by the Python implementation in `kristaldiag/v9.py`. V10 publication identity and bundle byte bindings are independently recomputed by `kristaldiag/v10.py`.

## v10 boundary

KristalDiag enforces the architectural split:

```text
SEMANTIC STATE != HOSTING != PUBLICATION LOCATION != DISCOVERY DIRECTORY
```

A host move or backup visibility change is not a semantic revision. A directory is not semantic authority. A publication binds exact state identity plus retrievable bytes, while activation remains a distinct lifecycle decision.

## Scheduling and evidence

Levels normally execute in isolated Python worker processes under bounded timeouts. The parent runner fingerprints the target before/after and emits an evidence manifest covering every result artifact.
