# CI integration

The supplied CI has two layers:

1. Python 3.11/3.12/3.13 unit tests plus the built-in independent `V10-Full` fixture.
2. A pinned external qualification of `Rejean-McCormick/KristalV10` at commit `27c0c7db3d79a4597c1c964fe8281fa35b5f858a`.

The Framework checkout is immutable by default; CI does not qualify floating `main` while claiming a pinned baseline.

For release audit, `framework-release-audit.yml` accepts an explicit ref, runs `V10-Full`, then the broader release campaign, and verifies the produced evidence manifest.
