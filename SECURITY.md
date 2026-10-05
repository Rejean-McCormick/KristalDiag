# Security policy

KristalDiag is a diagnostic and qualification harness, not an authority engine.

Do not attach live credentials, private keys or confidential Kristal contents to public issue reports.

Target execution is disabled by default. Treat `--allow-exec` as an explicit trust decision. Even with execution enabled, KristalDiag uses direct argv arrays (`shell=False`), bounded timeouts, bounded output capture and evidence redaction.

The target is fingerprinted before and after qualification. Unexpected mutation causes an `ERROR` verdict. Security hygiene findings are conservative indicators, not a security audit.
