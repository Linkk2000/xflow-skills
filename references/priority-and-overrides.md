<!-- xflow: approval-policy-dispatch -->
## Approval policy dispatch

New Task-Scoped Unattended Mode uses [MR-only policy](unattended-mr-only.md):
`approvalPolicy: mr-only-v1`. Read it before any gate decision.
It is the authoritative exception to the manual and legacy rules below:
ordinary task steps are automatic; the sole human approval is review of the
published MR before merge. Earlier remote-write-only exceptions below describe
legacy mode, not additional MR-only gates. Mechanical checks and task scope
remain mandatory. Unsupported runtimes must report incompatibility, not
silently fall back to repeated approvals.
<!-- /xflow: approval-policy-dispatch -->

# Priority And Overrides

Apply rules in this order:

1. Current explicit user instruction.
2. Nearest project `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/*.mdc`, or Antigravity `.agents/*` rule.
3. Global XFlow Skill.
4. Agent defaults.

Project rules may override language, commit format, test commands, directory layout, and build commands.

Project rules must not remove human gates for remote writes, destructive actions, or issue/MR lifecycle actions unless the user explicitly confirms in the current conversation.
