<!-- xflow: approval-policy-dispatch -->
## Approval policy dispatch

New Task-Scoped Unattended Mode uses [MR-only policy](.xflow/ops/workflow/references/unattended-mr-only.md):
`approvalPolicy: mr-only-v1`. Read it before any gate decision.
It is the authoritative exception to the manual and legacy rules below:
ordinary task steps are automatic; the sole human approval is review of the
published MR before merge. Earlier remote-write-only exceptions below describe
legacy mode, not additional MR-only gates. Mechanical checks and task scope
remain mandatory. Unsupported runtimes must report incompatibility, not
silently fall back to repeated approvals.
<!-- /xflow: approval-policy-dispatch -->

# Gemini XFlow Adapter

Read `AGENTS.md`, then `.xflow/ops/workflow/SKILL.md` and only its selected
phase references.

## Capability-Contract Gate

- Locate an existing capability contract before classifying the request.
- AI must not edit implementation code before accepted-design.
- implementation-gap requires an immutable human gap-recognition record; contract acceptance cannot satisfy it.
- Verification matrix must exist before engineering projection.
- .xflow/issues/ is tracked by default.
- Early XFlow artifact commit: after `git start` and semantic gates (contract/gap/task-branch-start), commit those artifacts alone before implementation; does not authorize push/MR. Remote-write receipts stay under `.xflow/local/` — do not commit them or re-approve `git-push` for them.
- Post-merge Issue residual discard: after PR merge, discard that Issue's process residuals at cleanup; do not stash them onto main or propose feature-branch commits afterward.
- One worktree may activate only one remote Issue.
- Human Approval Is Non-Delegable; AI must never satisfy a human gate.

Keep Task-Scoped Unattended Mode exclusions, commit format, and browser rules
from `AGENTS.md`, including the separate human semantic decision required for
`shared-infrastructure`; this adapter does not redefine them.
