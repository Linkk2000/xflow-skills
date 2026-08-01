# Gemini XFlow Adapter

Read `AGENTS.md`, then `.xflow/ops/workflow/SKILL.md` and only its selected
phase references.

## Capability-Contract Gate

- Locate an existing capability contract before classifying the request.
- AI must not edit implementation code before accepted-design.
- Verification matrix must exist before engineering projection.
- .xflow/issues/ is tracked by default.
- One worktree may activate only one remote Issue.
- Human Approval Is Non-Delegable; AI must never satisfy a human gate.

Keep Task-Scoped Unattended Mode exclusions, commit format, and browser rules
from `AGENTS.md`; this adapter does not redefine them.
