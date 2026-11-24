<!-- kOA Doc Server · Docs IA · lot 02 · rédaction dérivée d’une capture, à valider par le propriétaire -->
# Navigation IA — KristalDiag

**Rôle observé :** Examinateur indépendant de diagnostic, conformité et qualification de builds Kristal.

**Autorité :** Les résultats se rapportent au build et au Framework épinglés; le propriétaire reste responsable des décisions de publication.

**Provenance :** `SmartDump_20261120_221507.zip` → `KristalDiag_Code_snapshot.zip` (20 novembre 2026). Cette capture ne prouve ni la présence actuelle du dossier Windows, ni un déploiement, ni une qualification.

## Ordre de lecture fondé sur les sources

1. [`README.md`](../../README.md) — source propriétaire présente dans le snapshot.
2. [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) — source propriétaire présente dans le snapshot.
3. [`docs/CI_INTEGRATION.md`](../../docs/CI_INTEGRATION.md) — source propriétaire présente dans le snapshot.
4. [`docs/SECURITY.md`](../../docs/SECURITY.md) — source propriétaire présente dans le snapshot.
5. [`docs/C1_C2_C3_HANDOFF.md`](../../docs/C1_C2_C3_HANDOFF.md) — source propriétaire présente dans le snapshot.
6. [`docs/CONFIG_REFERENCE.md`](../../docs/CONFIG_REFERENCE.md) — source propriétaire présente dans le snapshot.
7. [`docs/CONFORMANCE.md`](../../docs/CONFORMANCE.md) — source propriétaire présente dans le snapshot.
8. [`docs/CONSOLIDATION.md`](../../docs/CONSOLIDATION.md) — source propriétaire présente dans le snapshot.

## Pour une intervention IA

1. Définir le changement envisagé et relire les documents propriétaires ci-dessus.
2. Épingler la révision, configurer le diagnostic, produire un rapport reproductible et distinguer observations, limites et recevabilité.
3. Identifier les tests de la révision locale et préserver les traces avant de proposer une modification.
4. Présenter les limites de couverture et demander l’accord du propriétaire avant une opération à effet.

## Limites à ne pas perdre

- Un test local ne démontre ni mise en service C3 ni qualification d'une autre révision.
- L’overlay ne certifie pas le produit et n’autorise pas une écriture distante.
- Les contrats et `AGENTS.md` propriétaires priment sur cet index dérivé.
- Le Framework Kristal v11 est une cible documentaire facultative; toute adoption exige un profil explicitement épinglé.

## Aides complémentaires

- [`AI_CONTEXT.md`](AI_CONTEXT.md) — workflow et frontières de confiance propres au dépôt.
- `PROFIL_INGENIERIE.md` — facultatif, mesuré par RepoSurveyor sur le checkout local avec confirmation.

## Procédure opérationnelle proposée (lot 04)

- [`OPERATIONS.md`](OPERATIONS.md) — parcours concret et points de contrôle à vérifier avant tout effet.
