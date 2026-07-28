# XFlow Cross-Agent Rulebook

This is the canonical rulebook for XFlow agents. Tool-specific files must import or point here rather than redefining independent rules.

## Precedence

User instructions and repository-local files take precedence. When XFlow behavior is needed, read this file first, then consult `references/workflow-state-machine.md` and `references/devctl-contract.md`.

## Required Workflow

Follow the XFlow state machine for issue, branch, commit, push, PR/MR, conflict handling, close, and cleanup work. Do not skip states or infer approval from earlier steps.

## Human Gates

Stop for explicit human approval before each exact action:

- Issue creation.
- Entering development.
- Branch push.
- MR/PR creation.
- Non-trivial conflict resolution strategy.
- Issue close and local cleanup.

## Devctl

Use the project devctl adapter for workflow operations. On Windows, use `devctl.ps1`. On POSIX, use `devctl`.

## Checks

- Before commit: re-read project rules and run relevant tests/checks or `devctl check commit-msg` when available.
- Advisory Dependency Issue Workflow: keep in-scope work on the main feature branch; use local subtasks only for local decomposition; classify independently owned work as `child-feature|shared-infrastructure|external`; retain the remote Issue creation human gate; treat dependency state as advisory; and require fresh parent-side evidence before `integrated`.
- Commit messages must be portable, scoped, Chinese-dominant, multi-line, and issue-linked. Use `type(scope): 中文核心摘要[#Issue编号]`; ordinary commits use one direct-owner Issue, while explicit integration commits may use parent and dependency Issue IDs. Avoid AI-client trailers, local absolute paths, or provider-only metadata.
- Before push: run branch scope and verification checks.
- Before MR/PR: fetch the target branch, merge it into the task branch by default, resolve approved conflicts if any, rerun relevant checks, record the target branch SHA and sync result, then preview title/body, link issue, and list verification evidence.
- Before final delivery: report checks run and any skipped verification with reasons.

## Tool Repository Maintenance Exception

When the user explicitly requests maintenance of `xflow-skills` or
`xflow-devctl`, direct work on that tool repository's `main` branch and local
commits do not require a fabricated downstream Issue ID. This exception does
not apply to repositories consuming XFlow.
