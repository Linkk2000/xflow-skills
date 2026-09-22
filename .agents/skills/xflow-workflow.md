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

# XFlow Workflow

Read `AGENTS.md` first. Follow `references/workflow-state-machine.md` for all XFlow state transitions.

Use `devctl.ps1` on Windows and `devctl` on POSIX. Stop at every human gate, including issue creation, entering development, branch push, MR/PR creation, non-trivial conflict resolution strategy, issue close, and local cleanup.
