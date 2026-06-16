---
name: xflow-tdd-workflow
description: Git, Issue, branch, TDD, human-gated PR/MR workflow for AI coding agents. Use when the user asks to clarify a requirement, create or manage an issue, start issue-bound development, enforce project AGENTS.md rules, run devctl checks, commit, push, create MR/PR, resolve conflicts, or close an issue through the XFlow workflow.
---

# XFlow TDD Workflow

## Load Order

1. Read the current user request.
2. Read project-level instructions before work: `AGENTS.md`, then tool-specific adapters if present.
3. Apply precedence: current user instruction > nearest project rule > global XFlow Skill > agent defaults.
4. Stop and ask the user before irreversible action if rules conflict.
5. On Windows prefer `devctl.ps1`; do not use PowerShell-to-WSL-to-Bash chains for normal XFlow commands.

## Required References

This is a phase-selected reference index. If unsure which file applies, read `references/xflow-map.md` first, then read the phase-specific reference below.

- Start or unsure: `references/xflow-map.md`
- Empty repository or missing local workflow files: `references/bootstrap-policy.md`
- Existing XFlow repository on a new machine: `references/restore-policy.md`
- XFlow source, ref, submodule, and global-vs-project precedence: `references/source-resolution.md`
- Phase order and human gates: `references/workflow-state-machine.md`
- Rule precedence and project overrides: `references/priority-and-overrides.md`
- Issue creation and comments: `references/issue-policy.md`
- Branch, commit, push, MR, merge, conflict handling: `references/git-policy.md`
- `devctl` command semantics and default variables: `references/devctl-contract.md`
- Windows, PowerShell, WSL, UTF-8, LF/CRLF: `references/platform-adapters.md`
- Operational incidents and recovery patterns: `references/ops-lessons.md`
- Final self-evaluation: `references/scoring-rubric.md`

## Non-Negotiables

- Use Chinese for issue bodies, commit summaries, PR/MR bodies, progress notes, and final delivery unless the user explicitly asks otherwise.
- If a repository lacks `AGENTS.md` or local `devctl` entrypoints, enter XFlow bootstrap first. Do not start feature work until bootstrap has completed and the user has reviewed the result.
- Never create issue, push branch, create PR/MR, close issue, delete branches, or resolve conflicts without the required human gate.
- Never retry ambiguous failed remote writes without reading remote state first.
- Never use `devctl git mr` when the user only approved push.
- Never create MR/PR before synchronizing the task branch with the target branch and recording the sync evidence.
- Before commit, push, MR, and completion, re-read project rules or run matching `devctl check`.

## Core Remote Write Review Gate

- Core remote writes are `issue-create`, `issue-comment`, `issue-close`, and `git-mr`.
- Prepare remote body files before running remote-write commands:
  - `.xflow/issues/issue-draft/issue-draft.md`
  - `.xflow/issues/issue-<id>/comment-draft.md`
  - `.xflow/issues/issue-<id>/mr-draft.md`
  - `.xflow/issues/issue-<id>/walkthrough.md` for issue close evidence
- Run `devctl check issue-draft`, `devctl check mr-draft`, and `devctl check local-review` before remote writes.
- The active approval file is `.xflow/issues/issue-<id>/approvals/local-review.md`; use `.xflow/issues/issue-draft/approvals/local-review.md` before creating a remote issue.
- `Approved Action` must be one of `issue-create`, `issue-comment`, `issue-close`, `git-mr`, or `remote-write`.
- Use `--body-file` for Issue, comment, and MR/PR bodies. Do not pass long Markdown through inline command arguments.
- Remote-published body files must not include internal-only visible titles such as `# Issue Draft`, `# MR Draft`, `# PR Draft`, or `# Merge Request Draft`.

## Git Commit Attribution Rule

- Do not add Cursor co-author trailers.
- Do not append `Co-authored-by: Cursor <cursoragent@cursor.com>` to commit messages.
- Do not use `git commit --trailer` to add Cursor, cursoragent, or AI-client co-author metadata.
- Keep commit attribution limited to the repository's configured Git author unless the human reviewer explicitly requests otherwise.
