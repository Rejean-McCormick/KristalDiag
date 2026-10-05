# Conformance model

KristalDiag distinguishes **diagnostic campaigns** from **Kristal v7 conformance profiles**.

## Profiles

`V7-Reader`, `V7-Mesh`, `V7-Projection`, and `V7-Kristall` are semantic qualification claims. Each profile requires the neutral N00/N01/N02/N03/N04/N06 evidence plus its K-level semantics. N05 and R-levels are intentionally excluded from the semantic definition.

A required `SKIP` becomes `BLOCKED` at K14. Missing evidence never becomes a pass.

`V7-Kristall` includes K11 interoperability. If independent interop evidence is unavailable, the result may be `PARTIAL` or `BLOCKED` depending on release policy.

## Campaigns

Campaigns answer operational questions rather than semantic profile claims:

- `baseline`: neutral read-only repo diagnostics;
- `standard`: baseline plus reader/canonicalization checks;
- `deep`: neutral + all semantic checks;
- `release`: deep + R00–R04 ratification evidence.

## Qualification boundary

Every conformance artifact declares:

```json
{
  "qualification_only": true,
  "authority_granted": false
}
```

A PASS means the observed evidence satisfies the selected checks/profile. It does not authorize mutation, execution, deployment, or semantic promotion.
