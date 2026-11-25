# KristalDiag — scoped v11/diK diagnostic evidence

**Documentation-only coordination, 24 November 2026.** A diagnostic must
report the exact source revision, namespace and file digests it validated.
Tests of a single v11 build cannot assert that another graph, a missing
artifact, or a public release is qualified. A code snapshot is not a live
canonical truth source.

When consuming diK derived-index evidence, treat `(namespace_id, KQ/KP)`
as the local key and Wikidata Q/P as typed external crosswalk references.
`SINGLE_DECLARED_DERIVED_VIEW` and `OPERATOR_PINNED_DERIVED_VIEW` do **not**
establish Framework authority. New diK decision profile `/0.2` pins the
inspected graph hash in addition to index, registry, crosswalk and catalog.
An incomplete or multirevision ambiguity must remain visible as blocked.

This document does not add a KristalDiag certification mode, modify prior
reports or authorize a C1/C2/C3 promotion. Run an actual pinned diagnostic
separately and preserve its observed failure states.
