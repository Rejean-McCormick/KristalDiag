# KristalDiag v10

[![KristalDiag CI](https://github.com/Rejean-McCormick/KristalDiag/actions/workflows/ci.yml/badge.svg)](https://github.com/Rejean-McCormick/KristalDiag/actions/workflows/ci.yml)

**KristalDiag is the independent diagnostic, conformance and release-qualification examiner for Kristal.**

Current target: **Kristal `10.0.0-draft.2`**, pinned to Framework repository `Rejean-McCormick/KristalV10` commit `27c0c7db3d79a4597c1c964fe8281fa35b5f858a`.

```text
KristalV10              = normative specification + reference implementation
KristalDiag              = independent examiner
Kristal Manager          = local inventory + backup
Kristal GitHub Setup     = bootstrap + qualify/publish/activate
Kompiler                 = optional read-only context compiler
```

KristalDiag does **not** manage Local Kristals, perform backups, publish releases or activate channels. It examines artifacts and evidence produced by those systems.

## What changed in v10

KristalDiag keeps its independent v9 commitment implementation and adds independent v10 checks for:

- node manifests and capability descriptors;
- generic host bindings and `kristal.host/github/1.0`;
- node/binding relational coherence;
- Publication Records and exact state references;
- byte-verifiable `kristal.publication-bundle/1.0` bundles;
- publication identity binding to the exact bundle manifest;
- directory/discovery semantics;
- the invariant `SEMANTIC STATE != HOSTING != PUBLICATION LOCATION != DISCOVERY DIRECTORY`;
- malformed v10 contracts and tampered publication bytes;
- Standard `release.json` / `contract-set.json` alignment.

The examiner uses its own frozen contracts. It does not validate a target using schemas supplied by that target.

## Quick start

```bash
python -m pip install -e .

kristaldiag doctor --target .
kristaldiag self-test

# Generic hosted-network conformance
kristaldiag conform /path/to/target --profile V10-Node-Reader
kristaldiag conform /path/to/target --profile V10-Full

# GitHub host profile
kristaldiag conform /path/to/hosted-node --profile V10-GitHub-Host

# Campaigns
kristaldiag run v10 /path/to/target
kristaldiag run release /path/to/KristalV10
```

## V10 profiles

| Profile | Qualification surface |
|---|---|
| `V10-Node-Reader` | v10 contracts, node/binding relations, separation, negative corpus |
| `V10-Publisher` | inherited v9 reader/publisher + verified v10 publication bundles |
| `V10-Directory` | Node Reader + directory/discovery semantics |
| `V10-GitHub-Host` | Node Reader + GitHub reference host profile |
| `V10-Full` | inherited V9-Full semantics + generic v10 node/publisher/directory checks |
| `V10-Standard` | normative Framework repository: inherited compatibility + v10 contracts/regressions + release/contract-set alignment |

`V10-Full` intentionally does **not** require GitHub. GitHub is a reference host profile, not semantic identity.

## Diagnostic levels

V10 adds K25–K32:

```text
K25  machine contracts & capabilities
K26  node / binding relations
K27  Publication Record + bundle integrity
K28  directory & discovery semantics
K29  GitHub host profile
K30  semantic / hosting separation
K31  negative & adversarial corpus
K32  Standard / contract-set alignment
```

K14 remains the final fail-closed gate.

## Independent publication verification

For a local or downloaded publication bundle containing:

```text
publication.json
bundle-manifest.json
state-snapshot.json
```

KristalDiag independently recomputes:

1. the v9 State Snapshot commitment;
2. payload sizes and SHA-256 byte digests;
3. the manifest byte digest;
4. the v10 `publication_id` identity projection;
5. the binding between Publication Record, manifest and exact state.

It does not call the Framework JavaScript verifier for this check.

## Frozen examiner provenance

`kristaldiag/resources/locks/framework-v10.json` records the pinned Framework commit and upstream Git blob identities used to capture the v10 examiner fixtures. Vendored examiner copies are integrity-hashed by `contract-manifest.json`.

## Read-only boundary

KristalDiag fingerprints the target before and after qualification. Target code is not imported. Target commands execute only through an explicit trusted driver with `--allow-exec`; ordinary qualification is static/read-only.

Every conformance verdict remains qualification evidence only:

```json
{
  "qualification_only": true,
  "authority_granted": false
}
```

## Evidence

Each run produces a verifiable evidence bundle under `.kristaldiag/` or the selected `--control-dir`. Verify it with:

```bash
kristaldiag verify-run /path/to/current/summary.json
```

See `docs/LEVELS.md`, `docs/CONFORMANCE.md`, `docs/ARCHITECTURE.md` and `docs/CI_INTEGRATION.md`.
