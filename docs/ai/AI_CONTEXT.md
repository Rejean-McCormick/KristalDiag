<!-- kOA Doc Server · Docs IA · lot 02 · rédaction dérivée d’une capture, à valider par le propriétaire -->
# Navigation IA — KristalDiag

**Rôle observé :** Examinateur indépendant de diagnostic, conformité et qualification de builds Kristal.

**Autorité :** Les résultats se rapportent au build et au Framework épinglés; le propriétaire reste responsable des décisions de publication.

**Provenance :** `SmartDump_20261120_221507.zip` → `KristalDiag_Code_snapshot.zip` (20 novembre 2026). Cette capture ne prouve ni la présence actuelle du dossier Windows, ni un déploiement, ni une qualification.

## Objet et état de cette fiche

La description ci-dessous est rattachée au `README.md` du snapshot; vérifier le code actif sur le poste. Cette fiche est un **guide de navigation**, non une spécification normative ni une validation de maturité.

## Processus conseillé

1. **Identifier la source et le profil.** Épingler la révision, configurer le diagnostic, produire un rapport reproductible et distinguer observations, limites et recevabilité.
2. **Contrôler l’autorité.** Les résultats se rapportent au build et au Framework épinglés; le propriétaire reste responsable des décisions de publication.
3. **Préparer un environnement de test.** Utiliser les fichiers réels de la révision étudiée et des données fictives ou autorisées.
4. **Vérifier sans promouvoir.** Documenter commandes, périmètre, résultat, chemins et empreintes; ne jamais transformer une observation locale en preuve historique validée.
5. **Revue propriétaire.** Une publication, activation, import ou effet externe nécessite l’accord du propriétaire et les gates correspondants.

## Garde-fous particuliers

- Un test local ne démontre ni mise en service C3 ni qualification d'une autre révision.
- N’inclure aucun secret, donnée personnelle, sauvegarde privée ou sortie de diagnostic non autorisée dans les exports Doc Server.
- Préserver l’intégrité des sources et des états historiques; éviter toute réécriture automatique des références.

## Sources d’orientation vérifiables dans le snapshot

1. [`README.md`](../../README.md) — source propriétaire présente dans le snapshot.
2. [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) — source propriétaire présente dans le snapshot.
3. [`docs/CI_INTEGRATION.md`](../../docs/CI_INTEGRATION.md) — source propriétaire présente dans le snapshot.
4. [`docs/SECURITY.md`](../../docs/SECURITY.md) — source propriétaire présente dans le snapshot.
5. [`docs/C1_C2_C3_HANDOFF.md`](../../docs/C1_C2_C3_HANDOFF.md) — source propriétaire présente dans le snapshot.
6. [`docs/CONFIG_REFERENCE.md`](../../docs/CONFIG_REFERENCE.md) — source propriétaire présente dans le snapshot.
7. [`docs/CONFORMANCE.md`](../../docs/CONFORMANCE.md) — source propriétaire présente dans le snapshot.
8. [`docs/CONSOLIDATION.md`](../../docs/CONSOLIDATION.md) — source propriétaire présente dans le snapshot.

## Compatibilité Framework

S’il y a une dépendance Kristal, lire la révision du Framework et le profil **effectivement adoptés** par ce dépôt. Les nouvelles conventions v11 (identités sémantiques, dictionnaires séparés, provenance) servent de référence lorsque compatibles; **ne pas bloquer** la navigation IA ni imposer la migration de données historiques pour cette seule raison.
