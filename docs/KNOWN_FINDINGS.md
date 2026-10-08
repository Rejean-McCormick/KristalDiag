# Known findings

Historical findings recorded against earlier v9/v10 snapshots are not automatically asserted against `10.0.0-draft.2`; they must be reproduced on the exact subject before being treated as current.

KristalDiag 1.0 adds regression checks for several earlier defect classes: unsupported v10 roles, null binding references, malformed directory collections, non-byte-verifiable publication resources and tampered publication bundle bytes.

The examiner pin is recorded in `kristaldiag/resources/locks/framework-v10.json`. If the Framework commit changes, the v10 examiner resources and regression results must be reviewed and repinned rather than silently following a branch.
