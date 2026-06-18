# XFlow Generic Project Map

This reference is for the `main` product line. It must stay repository-neutral:
do not hard-code a user's local project path or an academic paper layout here.

## XFlow Workflow References

- `workflow-state-machine.md`: phase order, states, human gates, and the
  pre-MR target-branch synchronization checkpoint.
- `bootstrap-policy.md`: how an empty repository obtains XFlow files and local
  devctl entrypoints.
- `restore-policy.md`: how an existing XFlow repository is rehydrated on a new
  machine.
- `source-resolution.md`: source/ref/submodule priority and project binding
  rules.
- `human-gates.md`: valid and invalid human approval wording.
- `priority-and-overrides.md`: rule precedence and project override boundaries.
- `platform-adapters.md`: Windows/POSIX command and encoding expectations.
- `devctl-contract.md`: devctl entrypoints, environment variables, and command
  semantics.
- `git-policy.md`: Git action matrix, branch, commit, issue, MR/PR, and
  conflict rules.
- `issue-policy.md`: issue drafting, duplicate checks, body-file usage, and
  retry safety.
- `scoring-rubric.md`: 100-point effectiveness rubric and hard-fail conditions.
- `ops-lessons.md`: concise operational lessons for remote writes, shell
  boundaries, and context drift.

## Tool Layers

1. Project repository: the user's current Git repository.
2. Project-local tools:
   - `.xflow/ops/devctl`
   - `.xflow/ops/workflow`
3. Project rule files:
   - `AGENTS.md`
   - `.cursorrules`
   - optional future entries such as `CLAUDE.md` or `GEMINI.md`

The project-local tool submodules are the runtime source of truth. Global
checkouts are only bootstrap/update sources.

## Provider Selection

`devctl` supports GitHub and Gitee through the same command surface. Set
`XFLOW_PLATFORM=github` or `XFLOW_PLATFORM=gitee` when auto-detection from the
`origin` remote is not enough. Gitee uses `GITEE_TOKEN` and the Gitee v5
OpenAPI; do not call Gitee endpoints directly from an AI workflow.

## devctl Commands

Run from the owning repository.

```bash
./devctl help
./devctl preflight
./devctl check current-task --issue <number>
./devctl check issue-draft --file .xflow/issues/issue-draft/issue-draft.md
./devctl approval prepare --issue draft --action issue-create --file .xflow/issues/issue-draft/issue-draft.md
./devctl check local-review --issue draft --file .xflow/issues/issue-draft/issue-draft.md --action issue-create
./devctl issue create "<title>" --body-file .xflow/issues/issue-draft/issue-draft.md --labels "tdd,backend"
./devctl issue list --state open --limit 20
./devctl issue show <number>
./devctl issue comment <number> --body-file .xflow/issues/issue-<number>/comment-draft.md
./devctl issue close <number>
./devctl git start <slug> --issue <number>
./devctl git status
./devctl git commit-msg -a
./devctl check mr-draft --issue <number>
./devctl approval prepare --issue <number> --action git-mr --file .xflow/issues/issue-<number>/mr-draft.md
./devctl check local-review --issue <number> --file .xflow/issues/issue-<number>/mr-draft.md --action git-mr
./devctl git mr --title "<title>" --body-file .xflow/issues/issue-<number>/mr-draft.md --issue <number>
./devctl check submodule-hygiene
./devctl rules list
./devctl rules sync codex
./devctl rules sync cursor
./devctl migrate inspect
./devctl git done
```

On Windows, prefer:

```powershell
.\devctl.ps1 preflight
.\devctl.ps1 check current-task --issue <number>
.\devctl.ps1 check submodule-hygiene
```

## Current Task State

Active tasks should keep `.xflow/current-task.md` in sync with
`references/workflow-state-machine.md`.

Run `devctl check current-task --issue <number>` before:

- requesting local approval
- committing implementation or workflow artifacts
- pushing a branch
- creating a PR/MR
- cleanup, issue close, or archival actions

The check does not approve work. It catches missing/stale state, including the
case where local git metadata already records a PR but the task file still says
the workflow is preparing or creating that PR.

## Pre-MR Target Branch Synchronization

Before MR/PR creation, fetch the target branch and merge `origin/<base>` into
the current task branch by default. Record:

- target branch name
- target branch SHA before merge
- merge command and result
- conflict files and approved conflict strategy, if any
- checks rerun after synchronization

Rebase is allowed only when the user or project policy explicitly prefers it
and the AI previews the strategy first. Push approval and MR/PR approval remain
separate human gates.

## Remote-Write Gate

Core remote writes require local review of the exact file being published or
used as evidence. The active approval file is
`.xflow/issues/issue-<id>/approvals/local-review.md`; for issue creation use
`.xflow/issues/issue-draft/approvals/local-review.md`.

Use `devctl approval prepare` to prefill mechanical fields such as timestamp,
approved file, suggested command, and SHA256. The human reviewer inspects the
artifact and changes `Approved: no` to `Approved: yes`.

## Body Files

For issue creation, comments, and MR/PR descriptions, use `--body-file`.
Multi-line Markdown, fenced code, inline backticks, JSON, or shell snippets
must be written to a file so shells do not reinterpret the content.

Remote-published body files must be public-facing Markdown. Use hidden
`<!-- xflow: ... -->` anchors for machine checks, and do not include internal
draft headings such as `# Issue Draft`, `# MR Draft`, or `# PR Draft`.

## TDD Targets By Change Type

- API behavior: test service/controller boundaries before implementation.
- Frontend UI behavior: add focused component or browser checks where feasible.
- Data migration: add a new migration; do not edit released migrations.
- CLI/workflow behavior: add a focused command test and prove the failure first.
- Documentation-only change: run template/entrypoint checks and inspect links.

Use focused commands first. Run broader builds only when the changed surface
justifies it.
