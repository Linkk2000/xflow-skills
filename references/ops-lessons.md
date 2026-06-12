# Ops Lessons

## Ambiguous Remote Write

Symptom: local command fails but remote issue or MR was created.
Rule: read remote state before retry.

## Windows Shell Boundary

Symptom: quoting, EOF, CRLF, or mojibake failures.
Rule: use native PowerShell command path on Windows.

## Context Drift

Symptom: commit or issue ignores project language rules.
Rule: re-read project rules or run checks before lifecycle actions.
