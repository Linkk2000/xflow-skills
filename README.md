# XFlow Skills

This repository contains the generic XFlow workflow rules and templates.

Workflow policy includes Advisory Dependency Issue Workflow and
Task-Scoped Unattended Mode. Read `SKILL.md` and `references/human-gates.md` for the
canonical safety-word, scope, invalidation, mechanical-check, and high-risk
exclusion rules before changing generated AI entrypoints.

For a normal project that should use XFlow locally without committing the tool
repositories, give the downstream AI this prompt:

- `templates/xflow-local-ignored-vendor-init-prompt.md`

That prompt covers empty directories, non-empty directories, empty Git
repositories, and existing Git projects. It uses project-local
`.xflow/ops/workflow` and `.xflow/ops/devctl` in `local-ignored-vendor` mode.
