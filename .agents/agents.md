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

# Antigravity XFlow Agents

`AGENTS.md` is canonical. These roles point to it rather than redefining XFlow rules.

## Product Manager

Clarifies requests, drafts issues, applies the issue template, and stops at human gates.

## Engineer

Implements approved development work through the XFlow workflow, devctl commands, and required checks.

## Reviewer

Reviews changes against the approved issue, workflow gates, devctl contract, and repository checks.
