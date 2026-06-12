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
- Before push: run branch scope and verification checks.
- Before MR/PR: preview title/body, link issue, and list verification evidence.
- Before final delivery: report checks run and any skipped verification with reasons.
