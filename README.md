# XFlow Skills

This repository contains the generic XFlow workflow rules and templates.

Workflow policy includes Advisory Dependency Issue Workflow and
Task-Scoped Unattended Mode. Read `SKILL.md` and `references/human-gates.md` for the
canonical safety-word, scope, invalidation, mechanical-check, and high-risk
exclusion rules before changing generated AI entrypoints.

Capability-contract routing is defined in
`references/capability-contract-method.md` and linked phase references.
`.xflow/issues/` is tracked by default; canonical task state is
`.xflow/issues/issue-<id>/task-state.md`, while machine-local pointers, runtime
files, and active approvals remain ignored. One worktree may activate only one
remote Issue.

For a normal project that should use XFlow locally without committing the tool
repositories, give the downstream AI this prompt:

- `templates/xflow-local-ignored-vendor-init-prompt.md`

That prompt covers empty directories, non-empty directories, empty Git
repositories, and existing Git projects. It uses project-local
`.xflow/ops/workflow` and `.xflow/ops/devctl` in `local-ignored-vendor` mode.
It installs or merges every adapter declared by `templates/ai-rules.json` and
reports project-text conflicts instead of overwriting them.
