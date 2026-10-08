# GitHub qualification model

KristalDiag is an **independent examiner**, not the normative Kristal Standard and not the GitHub lifecycle controller.

## Automatic gates

1. KristalDiag self-tests on Python 3.11, 3.12 and 3.13 and requires its built-in `V10-Full` corpus to pass.
2. It checks out `Rejean-McCormick/KristalV10` at the immutable baseline commit `27c0c7db3d79a4597c1c964fe8281fa35b5f858a` and applies `V10-Standard`.
3. Release audit also runs the broad `release` campaign and verifies evidence-manifest integrity.

## Independence boundary

The v9 commitment implementation is Python under `kristaldiag/v9.py`; v10 publication/bundle identity checks are Python under `kristaldiag/v10.py`. The examiner does not execute the Framework JavaScript verifier to manufacture agreement.

SchemaStore uses frozen examiner copies rather than target-provided schemas. `kristaldiag/resources/locks/framework-v10.json` records the upstream Framework commit and Git blob identities used for the draft.2 examiner capture.

## Inherited substrate

Historical `V7-*` and v9 profiles remain available. K24 continues to use the frozen inherited baseline under `kristaldiag/resources/baseline/9.0.0-draft.1/`; v10 does not silently rewrite historical commitment meaning.

## Lifecycle boundary

Kristal GitHub Setup/Bootstrap owns provisioning, qualification dispatch, publication and activation. KristalDiag may independently examine the resulting repository descriptors, downloaded publication bundles and evidence, but does not mutate those surfaces.
