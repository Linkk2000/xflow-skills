@AGENTS.md

# Claude XFlow Adapter

Read `.xflow/ops/workflow/SKILL.md` and only its phase-specific references.

## Capability-Contract Gate

- Locate an existing capability contract before classifying the request.
- AI must not edit implementation code before accepted-design.
- implementation-gap requires an immutable human gap-recognition record; contract acceptance cannot satisfy it.
- Verification matrix must exist before engineering projection.
- .xflow/issues/ is tracked by default.
- Early XFlow artifact commit: after `git start` and each major gate that writes trackable process files, commit those artifacts alone before implementation; does not authorize push/MR.
- One worktree may activate only one remote Issue.
- Human Approval Is Non-Delegable; AI must never satisfy a human gate.

Keep Task-Scoped Unattended Mode exclusions, commit format, and browser rules
from `AGENTS.md`, including the separate human semantic decision required for
`shared-infrastructure`; this adapter does not redefine them.
