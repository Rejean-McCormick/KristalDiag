# N03/N06 — fichiers volumineux, captures HTML et exceptions vérifiables

Cette modification garde **N03** (taille) distinct de **N06** (motifs potentiellement sensibles). Elle ne modifie pas le canon et **n'exempte jamais automatiquement une correspondance N06**.

## N03-LARGE-003

Chaque fichier supérieur à `scan.large_file_bytes` est accompagné d'un rôle **indicatif** :

- `canonical_or_committed` : `canon/`, `knowledge-base/corpus/`, `.kristal/v9/`, `.kristal/v11/`, `state/`, portable state v8. **Attendu possible, jamais une preuve de validité.**
- `derived_or_cache` : `derived/`, `.kristal/v8/index/`, `build/`, `runtime/`, etc. **Ne pas supprimer sans reconstruction vérifiée.**
- `external_source_archive` : capture tierce conservée pour provenance, pouvant contenir du HTML/MHTML volumineux ou des scripts embarqués. Revue spécifique avant diffusion.
- `unclassified` : source inconnue, revue requise.

Le statut est `WARN` s'il reste au moins un fichier volumineux **sans exception approuvée et vérifiée**. L'exception est un enregistrement local de politique d'hygiène, pas une validation normative. Pour une exemption explicite, ajouter à `kristaldiag.config.local.json` **dans le dépôt KristalDiag** (ne pas le committer par défaut) :

```json
{
  "large_files": {
    "exceptions": [
      {
        "path": "canon/domain/large-graph.json",
        "bytes": 12582912,
        "sha256": "sha256:<64 CARACTÈRES HEXADÉCIMAUX RÉELS>",
        "status": "approved",
        "reviewed_by": "responsable-local",
        "reason": "Artefact canonique conservé après contrôle documentaire"
      }
    ]
  }
}
```

**Exemple non exécutable tel quel** : taille et hash doivent être réels. L'exception expire automatiquement si les octets changent. Les paramètres de contrôle sont externes aux Kristals examinés et leurs références doivent être conservées en dehors des sources.

## N06-SECRETS-002

Une correspondance dans une page HTML potentiellement archivée reçoit `file_kind`, `third_party_archive_candidate`, `requires_review`, `assessment`, `values_included=false`. Ces champs précisent le **contexte**, pas le risque réel. L'alerte reste `WARN`, y compris pour une clé `apiKey` au sein d'un script de site tiers. Les valeurs détectées ne sont pas recopiées dans les preuves.

Les fichiers non textuels ou dépassant `scan.max_file_bytes` sont exclus de l'analyse regex. Cela **limite la couverture** : le résultat ne prétend pas vérifier des fichiers géants, ni la validité d'une clé détectée.

## Manager

Le nouveau `scan-global` offre un tableau **des déclarations présentes et manquantes** pour chaque Kristal, y compris les références canoniques cassées. `PRESENT` ou `DECLARED_UNVERIFIED` ne vaut pas certification.
