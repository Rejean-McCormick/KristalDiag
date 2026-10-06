# Conformance model

KristalDiag separates diagnostic campaigns from semantic conformance profiles. A required `SKIP` becomes `BLOCKED` at K14; missing evidence never becomes a pass.

## Kristal v9 profiles

### V9-State-Reader

Requires K15, K16, K17, K22 and K23 plus the neutral read-only harness. It validates the v9 machine contracts, independently reproduces golden commitments, checks state pinning, exercises the polymorphic workload corpus and runs commitment-invariance/adversarial cases.

### V9-Builder

Includes `V9-State-Reader` and K18. Derivations must bind exact logical inputs/outputs and deterministic claims must not silently rely on mutable selectors.

### V9-Materializer

Includes `V9-State-Reader` and K19. Materializations must bind exact source commitments and declare lossless reconstructability under the baseline v9 contract.

### V9-Publisher

Includes `V9-State-Reader` and K21. The examiner qualifies activation records and independently tests monotonic/compare-and-swap lifecycle behavior. Testing an external publisher implementation may additionally use an explicit driver with `--allow-exec`.

### V9-Full

Requires all v9 surfaces: reader, builder, materializer, Exchange, publisher and K24 inherited compatibility qualification.

## Historical profiles

The following remain supported and keep their pre-v9 meaning:

- `V7-Reader`
- `V7-Mesh`
- `V7-Projection`
- `V7-Kristall`

KristalDiag does not redefine these profiles merely because the tool now targets v9.

## Campaigns

- `baseline`: neutral read-only repository diagnostics;
- `standard`: historical v7 reader/canonicalization diagnostics;
- `deep`: neutral + all historical and v9 semantic checks;
- `v9`: neutral + all K15–K24 v9 checks;
- `release`: deep + R00–R04 release-engineering evidence.

## Qualification boundary

A PASS means the observed evidence satisfies the selected checks. It does not confer epistemic authority, operational authorization, deployment authority, recognition or factual truth.
