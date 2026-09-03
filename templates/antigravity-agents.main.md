# Antigravity XFlow Agent Rules

Read `.xflow/ops/workflow/SKILL.md` and
`.agents/skills/xflow-workflow.md`. Project rules and project-local XFlow tools
are authoritative; there is no user-level or global XFlow fallback.

Human Approval Is Non-Delegable. Preserve the Task-Scoped Unattended Mode
exclusions, including the separate human semantic decision required for
`shared-infrastructure`, plus the commit format and browser rules from the
project-local Skill.

Early XFlow artifact commit: after `git start` and each major gate that writes
trackable process files, commit those artifacts alone before implementation;
does not authorize push/MR.
