---
name: xflow-tdd-workflow
description: Generic Git, Issue, TDD, local-review, pre-merge synchronization, and PR/MR workflow for software-development repositories. Use when an AI assistant must turn a user request into a reviewed issue-driven branch workflow with local human approval before remote writes.
---

# XFlow TDD Workflow

This is the generic `main` product line. It is for software-development work.
Domain-specific workflows, external domain skill catalogs, delegated specialist
task packages, and paper-specific templates belong on specialized branches such
as `academic`, not here.

## Load Order

1. Read the current user request.
2. Read repository-local rules first: `AGENTS.md`, `.cursorrules`,
   `CLAUDE.md`, `GEMINI.md`, `README.md`, and `.xflow/current-task.md` when
   present.
3. Apply precedence: current user instruction > nearest project rule >
   project-bound XFlow submodule/config > agent defaults.
4. Stop and ask the user before irreversible action if rules conflict.
5. On Windows prefer `devctl.ps1`; do not use PowerShell-to-WSL-to-Bash chains
   for normal XFlow commands.

## Required References

This is a phase-selected reference index. If unsure which file applies, read
`references/xflow-map.md` first, then read the phase-specific reference below.

- Start or unsure: `references/xflow-map.md`
- Empty repository or missing local workflow files: `references/bootstrap-policy.md`
- Existing XFlow repository on a new machine: `references/restore-policy.md`
- XFlow source, ref, submodule, and project binding precedence: `references/source-resolution.md`
- Phase order and human gates: `references/workflow-state-machine.md`
- Rule precedence and project overrides: `references/priority-and-overrides.md`
- Issue creation and comments: `references/issue-policy.md`
- Pasted files, screenshots, images, and comment attachments:
  `references/attachment-policy.md`
- Branch, commit, push, MR, merge, conflict handling: `references/git-policy.md`
- `devctl` command semantics and default variables: `references/devctl-contract.md`
- Windows, PowerShell, WSL, UTF-8, LF/CRLF: `references/platform-adapters.md`
- Operational incidents and recovery patterns: `references/ops-lessons.md`
- Final self-evaluation: `references/scoring-rubric.md`

## Hard Rules

1. Use repository-local `devctl` or `devctl.ps1` when available.
2. Treat `devctl` / `devctl.ps1` as the only supported workflow entrypoints.
   They may route to `python -m xflow`, but AI assistants must not import
   provider modules directly or call GitHub/Gitee APIs outside devctl.
   Do not use a globally installed XFlow Skill or user-level devctl PATH shim
   as a runtime fallback for project repositories.
3. Do not create remote Issues, comments, PRs/MRs, pushes, branch publication,
   or remote metadata changes before local human review approves the exact
   body/evidence file, unless the current user explicitly authorizes an
   unattended issue/comment command and devctl is invoked with
   `--no-local-review` for that exact action. If issue/comment images or
   screenshots are present, publish them only through an approved object
   storage backend such as `aliyun-oss`; otherwise keep them as local evidence
   and stop.
4. Maintain `.xflow/current-task.md` for active tasks and run
   `devctl check current-task --issue <id>` before local approval, commit,
   push, MR/PR creation, and cleanup.
5. Never create MR/PR before synchronizing the task branch with the target
   branch and recording the sync evidence.
6. The active approval file is always
   `.xflow/issues/issue-<id>/approvals/local-review.md`; for issue creation use
   `.xflow/issues/issue-draft/approvals/local-review.md`.
7. Do not invent alternate active approval names such as
   `local-review-mr.md`. Historical approvals may be archived under
   `approvals/history/`, but only `approvals/local-review.md` satisfies the
   gate.
8. Use `--body-file` for Issue bodies, comments, and PR/MR bodies. Do not pass
   multiline Markdown, fenced code, JSON, shell snippets, backticks, or `$()`
   through inline command arguments.
9. Do not publish local file paths or unresolved `xflow-attachment://`
   placeholders in remote Issues, comments, or PR/MR bodies. If a pasted file
   or image is referenced, use `references/attachment-policy.md`. Issue/comment
   image attachments are currently disabled unless an approved object storage
   backend published reviewed URLs; never use GitHub release assets as an
   issue/comment image store.
10. Use the user's language for Git-related public text: commit messages,
   remote Issue text, remote PR/MR text, review comments, and branch task
   summaries. Do not expand this rule to unrelated source code or docs.
11. Do not add AI-client co-author trailers. In particular, never add
    `Co-authored-by: Cursor <cursoragent@cursor.com>`.

## Required Flow

1. Clarify the request only when required for safety or scope.
2. Draft `.xflow/issues/issue-draft/issue-draft.md` from
   `references/issue-template.md`.
3. Create or update `.xflow/current-task.md` using the state machine in
   `references/workflow-state-machine.md`.
4. Run `devctl check issue-draft --file .xflow/issues/issue-draft/issue-draft.md`
   and `devctl check current-task`.
5. Prepare approval with
   `devctl approval prepare --issue draft --action issue-create --file .xflow/issues/issue-draft/issue-draft.md`.
6. Stop for human review. The human reviewer must inspect the file and change
   `Approved: no` to `Approved: yes` before any remote write.
7. Create the remote issue only after approval:
   `devctl issue create "<title>" --body-file .xflow/issues/issue-draft/issue-draft.md`.
8. Start the task branch from the repository's base branch.
9. Follow TDD: write or identify a failing test/check first, then implement the
   smallest change to pass it.
10. Record work evidence in `.xflow/issues/issue-<id>/walkthrough.md`.
11. Before commit, push, PR/MR creation, or cleanup, run
    `devctl check current-task --issue <id>`.
12. Before requesting MR/PR approval, fetch the target branch, merge
    `origin/<base>` into the task branch by default, resolve approved
    conflicts, rerun relevant checks, and record the target branch SHA plus
    sync result.
13. Prepare `Approved Action: git-push`, stop for human review, then run
    `devctl git push --issue <id> --file .xflow/issues/issue-<id>/walkthrough.md`.
14. Draft `.xflow/issues/issue-<id>/mr-draft.md`, run
    `devctl check mr-draft --issue <id>`, prepare `Approved Action: git-mr`,
    stop for human review, then run `devctl git mr --body-file ... --issue <id>`.
    After PR/MR creation, devctl records the PR number/URL, creates a
    metadata-only state backfill commit, and pushes that commit to the same
    branch under the `git-mr` approval scope.

## Core Remote Write Review Gate

Core remote writes are:

- `issue-create`
- `issue-comment`
- `issue-close`
- `git-push`
- `git-mr`
- other remote metadata writes that publish or mutate remote state

Before each remote write:

- The exact file to be published or used as evidence must exist locally.
- If the body references pasted files, screenshots, or images, read
  `references/attachment-policy.md` before any remote write. Issue/comment
  image attachments require an approved object storage backend such as
  `aliyun-oss`; otherwise they must stay local as evidence. Other attachments
  require a reviewed manifest and approved public URL plan.
- If the current user explicitly requests no-human issue/comment handling, use
  devctl's unattended flow only for the exact no-attachment command or a
  supported attachment path. Image attachments still fail closed unless the
  approved object storage flow has already produced reviewed public URLs.
- `devctl approval prepare` should prefill the action, path, timestamp, and
  SHA256.
- The human reviewer only needs to make a judgement and set `Approved: yes`.
- `devctl check local-review --issue <id> --file <file> --action <action>` must
  pass.

## Template Files

- Issue draft: `.xflow/issues/issue-draft/issue-draft.md`
- Issue comment draft: `.xflow/issues/issue-<id>/comment-draft.md`
- Attachment manifest: `.xflow/issues/issue-<id>/attachments/manifest.json`
- MR/PR draft: `.xflow/issues/issue-<id>/mr-draft.md`
- Walkthrough/evidence: `.xflow/issues/issue-<id>/walkthrough.md`
- Active local approval: `.xflow/issues/issue-<id>/approvals/local-review.md`
- Current task state: `.xflow/current-task.md`
- PR/MR state suggestion: `.xflow/issues/issue-<id>/state-update-suggestion.md`

Remote-published body files must not contain visible internal titles such as
`# Issue Draft`, `# MR Draft`, `# PR Draft`, or `# Merge Request Draft`. Use
hidden anchors such as `<!-- xflow: issue-draft -->` instead.

## Project-Local Tool Layout

Preferred v2 layout:

```text
.xflow/ops/devctl
.xflow/ops/workflow
```

These tool repos are usually submodules. Their generated byproducts must not
pollute the parent project. Run `devctl check submodule-hygiene` after updates.

## Python Core And Environment

`devctl` and `devctl.ps1` are launchers. The generic main workflow should move
actual workflow behavior into `python -m xflow` over time. Shell scripts may
remain as compatibility fallback, but remote writes, approval checks, provider
calls, Git/app lifecycle commands, and rule synchronization must be routed
through devctl. Windows validation should use Python core checks such as
`python tests/python-core.py` and `python tests/entrypoint-routing.py`, not
bare `bash`, Git Bash, or WSL.

Use `~/.xflow/env.local` as the preferred user-level parameter file. It may
contain values such as:

```text
GITHUB_TOKEN=...
GITEE_TOKEN=...
ALIYUN_OSS_BUCKET=...
ALIYUN_OSS_REGION=...
ALIYUN_OSS_ACCESS_KEY_ID=...
ALIYUN_OSS_ACCESS_KEY_SECRET=...
```

`~/gitee.env.local` is a legacy compatibility path. `XFLOW_ENV_FILE` may point
to an explicit env file for a single run. Never print token values; preflight
may only print whether a token is `SET` or `UNSET`.

Object storage credentials are runtime secrets. Do not write
`ALIYUN_OSS_ACCESS_KEY_SECRET` or other credentials into manifests, issues,
comments, commits, or Markdown guides.

Do not put `XFLOW_PLATFORM` in user-level `~/.xflow/env.local` when working
across both GitHub and Gitee projects. Let devctl infer the platform from the
repository `origin` remote. For unusual projects, set `XFLOW_PLATFORM` in
project-local `.xflow/local/env.local`, an explicit `XFLOW_ENV_FILE`, or the
process environment.

The Python provider supports GitHub and Gitee. Gitee uses `GITEE_TOKEN` and the
Gitee v5 OpenAPI shape; `GITEE_API_BASE` is only for tests or custom hosts.

Do not import provider modules directly, for example `xflow.providers`, from an
AI task. Provider modules are internal implementation details behind devctl.

## Tool Repository Maintenance Exception

The `xflow-devctl` and `xflow-skills` repositories may be maintained directly
on their own `main` branches when the user explicitly asks for that maintenance
mode. This exception is limited to those two tool repositories. It does not
apply to repositories that consume XFlow, and it must not weaken user-project
issue, branch, local human review, or MR/PR gates.

## PowerShell And Encoding

- Prefer `devctl.ps1` on Windows.
- For long commit messages, Issue bodies, PR/MR bodies, JSON, or Markdown,
  write a UTF-8 file and pass the file path to the tool.
- Avoid composing multiple native commands in one PowerShell pipeline when a
  native command's exit code matters. Run the native command directly, then
  inspect `$LASTEXITCODE`.
- Set or preserve `PYTHONDONTWRITEBYTECODE=1` for devctl Python calls.

## References

- `references/issue-template.md`
- `references/workflow-state-machine.md`
- `references/xflow-map.md`
- `references/git-policy.md`
- `references/ops-lessons.md`
