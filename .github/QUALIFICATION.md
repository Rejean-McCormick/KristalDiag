# GitHub qualification model

KristalDiag is an **independent examiner**, not the normative Kristal Standard.

## Automatic gates

The automatic workflow has two layers:

1. KristalDiag self-tests on Python 3.11, 3.12 and 3.13 and requires its built-in `V9-Full` corpus to pass.
2. It checks out Kristal-Framework independently and applies `V9-Full`, retaining the exact resolved SHA and evidence bundle.

During draft development the Framework job may resolve a moving branch such as `main`, but the resolved commit is always recorded. RC/final qualification should pin an immutable Framework commit/tag.

## Independence boundary

KristalDiag's v9 commitment implementation is Python code under `kristaldiag/v9.py`. It does not import or execute the Framework JavaScript commitment implementation. Agreement is established through the normative prose and golden vectors.

## Inherited substrate

Historical `V7-*` profiles remain available with their previous KristalDiag fixtures. For v9, K24 uses a distinct exact baseline under:

`kristaldiag/resources/baseline/9.0.0-draft.1/`

That baseline mirrors the v6/v7/v8 substrate pinned by the Framework v9 compatibility lock.

## Known inherited finding

Independent qualification of the supplied `9.0.0-draft.1` Framework snapshot fails `K24-IDENTITY-003` for:

- `tck/v7/vectors/v6-compatible-projection.example.json`

The artifact retains the base v6 `state_id` / `content_hash` after adding `extensions.kristal_v7`. Under the frozen v6 identity rule, only `state_id`, `content_hash`, and `signatures` are excluded from the hash target, so the extension changes the expected identity.

Observed declared state ID:

`sha256:534d57141a4d1c982e2ddb25abfda19be7d63234667542dd3eea6acc5cf6b759`

Independent expected state ID:

`sha256:9f3fdad6b298e47a3f8750f418899f9208c4e3691f20233648abde2e2188bd79`

This disagreement is intentionally **not suppressed**. It must be resolved explicitly before final v9 qualification.
