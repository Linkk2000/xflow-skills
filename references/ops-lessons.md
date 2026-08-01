# XFlow Operations Lessons

## Ambiguous Remote Write

- Symptom: a local command fails, but a remote issue, comment, or MR/PR may
  already have been created.
- Rule: read remote state before retrying. Never retry ambiguous failed remote
  writes blindly.

## PowerShell And Native Commands

- A single native command is usually safe. Most failures come from composing
  native commands with PowerShell redirection, pipelines, command substitution,
  or nested quoting.
- Avoid using `2>&1 | Out-String` as the control path for `git`, `devctl`, or
  other native commands. It can turn normal stderr progress into a PowerShell
  `NativeCommandError` and hide the real exit-code semantics.
- For reviewed GitHub/Gitee text, write UTF-8 Markdown files and pass them with
  `--body-file`.
- Inspect `$LASTEXITCODE` immediately after a native command when the result
  matters.

## Windows, WSL, And Encoding

- Do not assume WSL is available. If WSL is broken or unavailable, use
  PowerShell plus `devctl.ps1`.
- Do not use bare `bash`, Git Bash, or WSL as the default Windows validation
  path. Run Python core checks instead.
- Do not use mojibake terminal output as a patch anchor. Match ASCII anchors,
  file names, hidden comments, or nearby structure.
- Prefer Python core checks for cross-platform behavior.
- Preserve `PYTHONDONTWRITEBYTECODE=1` for devctl calls to avoid `__pycache__`.

## Remote Issues And PR/MR Bodies

- Issue bodies, issue comments, and PR/MR bodies must be complete Markdown
  files before remote publication.
- Remote-published files must not include visible internal titles such as
  `# Issue Draft`, `# MR Draft`, `# PR Draft`, or `# Merge Request Draft`.
- Use hidden anchors such as `<!-- xflow: issue-draft -->`.
- PR/MR bodies should not claim work that has not been implemented, verified,
  or synchronized with the target branch.

## Git Hygiene

- Run `git status --short --branch` before committing.
- Keep generated temporary files under `.xflow/local/` when they are not meant
  for Git.
- Project-local tools belong under `.xflow/ops/devctl` and
  `.xflow/ops/workflow`. If they are local ignored vendor checkouts, the parent
  repository must ignore them. If they are explicit submodules, their generated
  byproducts must not appear as parent-repository changes.
- Run `devctl check submodule-hygiene` only for projects that intentionally use
  submodules.

## Context Drift

- Symptom: the AI ignores project language rules, stale state files, or the
  latest human gate.
- Rule: re-read project rules, run `devctl task status`, verify the
  worktree-local pointer, and open the matching
  `.xflow/issues/issue-<id>/task-state.md` before lifecycle actions. Mention
  legacy `.xflow/current-task.md` only when explicitly running
  `devctl task migrate-current`; it is not active authority.
- Treat push approval and MR/PR approval as separate gates.
