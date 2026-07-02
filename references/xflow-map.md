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
- `attachment-policy.md`: pasted files, screenshots, image manifests, backend
  publishing, and placeholder guards for issue/comment/MR bodies.
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

The project-local tool submodules are the runtime source of truth. Do not use a
global installed Skill or a user-level devctl PATH shim for repository work.
Developer checkouts are maintenance workspaces only.

## Provider Selection

`devctl` supports GitHub and Gitee through the same command surface. Prefer
auto-detection from the `origin` remote. Put global tokens in
`~/.xflow/env.local`, but put project-specific platform overrides in
`.xflow/local/env.local`, an explicit `XFLOW_ENV_FILE`, or the process
environment. Gitee uses `GITEE_TOKEN` and the Gitee v5 OpenAPI; do not call
Gitee endpoints directly from an AI workflow.

## devctl Commands

Run from the owning repository.

```bash
./devctl help
./devctl preflight
./devctl check current-task --issue <number>
./devctl check subtask --issue <number> --path .xflow/issues/issue-<number>/subtask-001
./devctl check issue-evidence --issue <number>
./devctl check issue-draft --file .xflow/issues/issue-draft/issue-draft.md
./devctl attachment add --issue draft --file /path/to/notes.txt --as file
./devctl attachment check --issue draft --manifest .xflow/issues/issue-draft/attachments/manifest.json
./devctl attachment publish --issue draft --manifest .xflow/issues/issue-draft/attachments/manifest.json --backend manual --url att-001=https://public.example/notes.txt --body-file .xflow/issues/issue-draft/issue-draft.md --output .xflow/publish/issues/issue-draft/issue.final.md
./devctl attachment publish --issue draft --backend aliyun-oss --manifest .xflow/issues/issue-draft/attachments/manifest.json
./devctl approval prepare --issue draft --action issue-create --file .xflow/issues/issue-draft/issue-draft.md
./devctl check local-review --issue draft --file .xflow/issues/issue-draft/issue-draft.md --action issue-create
./devctl issue create "<title>" --body-file .xflow/issues/issue-draft/issue-draft.md --labels "tdd,backend"
./devctl issue create "<title>" --body-file .xflow/issues/issue-draft/issue-draft.md --no-local-review
./devctl issue list --state open --limit 20
./devctl issue show <number>
./devctl issue comment <number> --body-file .xflow/issues/issue-<number>/comment-draft.md
./devctl issue close <number>
./devctl git start <slug> --issue <number>
./devctl git status
./devctl git commit-msg -a
./devctl approval prepare --issue <number> --action git-push --file .xflow/issues/issue-<number>/walkthrough.md
./devctl check local-review --issue <number> --file .xflow/issues/issue-<number>/walkthrough.md --action git-push
./devctl git push --issue <number> --file .xflow/issues/issue-<number>/walkthrough.md
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

Windows validation must use Python core checks, for example:

```powershell
python tests/python-core.py
python tests/entrypoint-routing.py
```

Do not use bare `bash`, Git Bash, or WSL as the normal Windows validation path.
`bash -n` is POSIX-only and applies only to intentionally changed shell
compatibility scripts.

## Issue And Attachment Command Choice

For issue/comment creation, choose a single path before running commands:

- No attachments and user explicitly authorized unattended remote write:
  `devctl issue create "<title>" --body-file issue.md --no-local-review`.
- Issue/comment images or screenshots without an approved object storage
  backend: do not upload and do not use GitHub release assets. Keep local
  evidence and stop before remote write.
- Issue/comment images or screenshots with approved Aliyun OSS config: use
  `attachment add --as image`, `attachment publish --backend aliyun-oss`,
  `attachment render`, `approval prepare`, `check local-review`, then the
  final `issue create` or `issue comment` command with
  `--attachments manifest.json`.
- Non-image attachments and normal human gate required: use `attachment add`,
  `attachment publish --backend manual` with an approved public URL,
  `attachment render` when needed, `approval prepare`, `check local-review`,
  then the final `issue create` or `issue comment` command with
  `--attachments manifest.json`.

Issue/comment image attachments are disabled unless the manifest shows an
approved object storage backend such as `aliyun-oss`. Other files may render as
normal Markdown links after an approved URL is recorded.

`.xflow/issues/issue-<id>/` is local evidence and approval state only. It must
not contain COS/OSS URLs, object-storage URLs, or non-null `publishedUrl`
values. Rendered remote bodies and published manifests belong under
`.xflow/publish/issues/issue-<id>/`.

## Local Subtasks

Large issues may be split into local subtask directories:

```text
.xflow/issues/issue-<id>/subtask-001/README.md
.xflow/issues/issue-<id>/subtask-001/evidence/
```

Each README records Source, Purpose, Implementation Plan, Evidence, AI Review
Checkpoints, Human Review Checkpoints, and Conclusion. Run
`devctl check subtask --issue <id> --path .xflow/issues/issue-<id>/subtask-001`
before using the subtask as workflow evidence.

Subtask evidence must stay in the repository under `subtask-001/evidence/`.
Do not upload subtask evidence to COS/OSS or object storage. Object storage is
only for rendered remote issue/comment/PR bodies.

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

`devctl git push --issue <number>` only publishes the current task branch.
`devctl git mr` must not push task code implicitly; it requires an upstream and
no unpushed task commits. After PR/MR creation, devctl records the PR number
and URL, creates a metadata-only state backfill commit, and pushes that commit
to the same branch under the `git-mr` approval scope.

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

If the body refers to pasted files, screenshots, or images, use
`attachment-policy.md`. Local drafts may contain `xflow-attachment://`
placeholders, but issue/comment images must be published only through an
approved object storage backend. Remote-published bodies must contain only
reviewed public URLs for approved attachments. Do not publish `C:\...`,
`/tmp/...`, `.xflow/...`, `file://...`, or WSL mount paths as attachment links.

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
