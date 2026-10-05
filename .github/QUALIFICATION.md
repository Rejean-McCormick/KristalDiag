# GitHub qualification model

KristalDiag is an **independent examiner**, not the normative Kristal Standard.

## Automatic gates

The automatic workflow has two layers:

1. KristalDiag tests itself on Python 3.11, 3.12 and 3.13.
2. After those self-tests pass, it checks out a pinned Kristal-Framework commit
   and runs the `V7-Projection` profile against the Framework's frozen v6/v7
   substrate.

The Framework commit is intentionally pinned:

`00a00e061dd216a9bcdb281cf1eeef80ce61410e`

Update that SHA deliberately when changing the examined Standard subject.

## v8 boundary

KristalDiag 0.7.0 currently targets Kristal v7. It must not claim complete
Kristal v8 conformance. Native v8 conformance remains in Kristal-Framework's
own TCK and validation tooling.

## Known finding in the supplied snapshots

The independent `V7-Projection` run currently fails K02 for:

- `tck/v7/vectors/v6-compatible-projection.example.json`
- `examples/v7/v6-compatible-projection.example.json`

The files retain the base v6 `state_id` / `content_hash` after adding
`extensions.kristal_v7`. KristalDiag computes the v6 hash target by excluding
only `state_id`, `content_hash`, and `signatures`, so the extension changes the
expected digest.

This is deliberately left as a failing gate rather than suppressed. Resolve
the rule explicitly and keep the resulting test as regression evidence.
