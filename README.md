# XFlow Skills

This repository contains the generic XFlow workflow rules and templates.

For a normal project that should use XFlow locally without committing the tool
repositories, give the downstream AI this prompt:

- `templates/xflow-local-ignored-vendor-init-prompt.md`

That prompt covers empty directories, non-empty directories, empty Git
repositories, and existing Git projects. It uses project-local
`.xflow/ops/workflow` and `.xflow/ops/devctl` in `local-ignored-vendor` mode.

