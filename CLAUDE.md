@AGENTS.md

Claude must treat `AGENTS.md` as the canonical XFlow rulebook. For Git, issue, branch, push, and MR/PR work, read `references/workflow-state-machine.md` and `references/devctl-contract.md` before acting.

## Capability-Contract Gate

Read project-local `SKILL.md` and its phase-specific references.
Locate an existing capability contract before classifying the request.
AI must not edit implementation code before accepted-design.
implementation-gap requires an immutable human gap-recognition record; contract acceptance cannot satisfy it.
Verification matrix must exist before engineering projection.
.xflow/issues/ is tracked by default.
Early XFlow artifact commit: after `git start` and each major gate that writes trackable process files, commit those artifacts alone before implementation; does not authorize push/MR.
One worktree may activate only one remote Issue.
