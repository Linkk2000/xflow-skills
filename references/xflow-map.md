# XFlow Generic Project Map

This reference is for the `main` product line. It must stay repository-neutral:
do not hard-code a user's local project path or an academic paper layout here.

## XFlow Workflow References

- `workflow-state-machine.md`: phase order, states, human gates, and the
  pre-MR target-branch synchronization checkpoint.
- `capability-contract-method.md`: capability discovery questions and semantic
  exit conditions before Issue/TDD/Git work.
- `contract-authoring.md`: contract field semantics, stable IDs, and exact
  human acceptance records.
- `contract-evolution.md`: PATCH/MINOR/MAJOR changes and accepted-design reopen.
- `scope-routing.md`: `capability-change|implementation-gap|ui-defect|infrastructure|governance|future` classification.
- `traceability.md`: contract-to-test-to-evidence closure.
- `bootstrap-policy.md`: how an empty repository obtains XFlow files and local
  devctl entrypoints.
- `restore-policy.md`: how an existing XFlow repository is rehydrated on a new
  machine.
- `source-resolution.md`: source/ref/local ops tool priority and project binding
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
- `evidence-analysis.md`: difference analysis, direct local evidence bundles,
  UI screenshot/DOM proof, and completion verification.
- `dependency-issue-workflow.md`: advisory dependency classification,
  ownership, lifecycle, integration, and parent closure assessment.
- `../templates/dependencies.yaml`: reusable issue-local dependency graph.
- `../templates/capability-contract.yaml`: capability contract starter.
- `../templates/classification.yaml`: request classification starter.
- `../templates/task-state.md`: Issue-scoped task state starter.
- `../templates/traceability-matrix.yaml`: verification trace starter.
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

The project-local tools under `.xflow/ops/` are the runtime source of truth.
They may be local ignored vendor checkouts or explicitly approved submodules.
Do not use a global installed Skill or a user-level devctl PATH shim for
repository work.

## Provider Selection

`devctl` supports GitHub and Gitee through the same command surface. Prefer
auto-detection from the `origin` remote. Put global tokens in
`~/.xflow/env.local`, but put project-specific platform overrides in
`.xflow/local/env.local`, an explicit `XFLOW_ENV_FILE`, or the process
environment. Gitee uses `GITEE_TOKEN` and the Gitee v5 OpenAPI; do not call
Gitee endpoints directly from an AI workflow.

## devctl Commands

Run from the owning repository.

### Project-Local Compatibility Gate

This map spans multiple devctl versions. Before using `unattended`,
`check dependencies`, or extended `check commit-msg` options, inspect the
project-local `devctl help` output and relevant subcommand help. On Windows use
`.\devctl.ps1 help`; on POSIX use `./devctl help`. If a capability is missing,
stop and update or restore the project-local devctl from the project's bound
XFlow source. AI must not probe by trying commands or pretend the capability is available.

Do not mark the commands permanently unavailable; support is determined by the
project-local version.

```bash
./devctl help
./devctl preflight
./devctl unattended enable --issue <number|draft> --confirm XFLOW_HUMAN_UNATTENDED_ALL
./devctl unattended status
./devctl unattended disable
./devctl task activate --issue <number>
./devctl task status
./devctl task list
./devctl task migrate-current
./devctl check current-task --issue <number>
./devctl check classification --issue <number|draft>
./devctl contract lint --file <contract.yaml>
./devctl trace check --issue <number> --contract <contract.yaml> --matrix .xflow/issues/issue-<number>/traceability-matrix.yaml
./devctl check subtask --issue <number> --path .xflow/issues/issue-<number>/subtask-001
./devctl check dependencies --issue <number>
./devctl check issue-evidence --issue <number>
./devctl check issue-draft --file .xflow/issues/issue-draft/issue-draft.md
./devctl attachment add --issue draft --file /path/to/notes.txt --as file
./devctl attachment check --issue draft --manifest .xflow/issues/issue-draft/attachments/manifest.json
./devctl attachment publish --issue draft --manifest .xflow/issues/issue-draft/attachments/manifest.json --backend manual --url att-001=https://public.example/notes.txt --body-file .xflow/issues/issue-draft/issue-draft.md --output .xflow/publish/issues/issue-draft/issue.final.md
./devctl attachment publish --issue draft --backend aliyun-oss --manifest .xflow/issues/issue-draft/attachments/manifest.json
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
./devctl approval prepare --issue <number> --action git-push --file .xflow/issues/issue-<number>/walkthrough.md
./devctl check local-review --issue <number> --file .xflow/issues/issue-<number>/walkthrough.md --action git-push
./devctl git push --issue <number> --file .xflow/issues/issue-<number>/walkthrough.md
./devctl check mr-draft --issue <number>
./devctl approval prepare --issue <number> --action git-mr --file .xflow/issues/issue-<number>/mr-draft.md
./devctl check local-review --issue <number> --file .xflow/issues/issue-<number>/mr-draft.md --action git-mr
./devctl git mr --title "<title>" --body-file .xflow/issues/issue-<number>/mr-draft.md --issue <number>
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
```

Windows validation must use Python core checks, for example:

```powershell
python tests/python-core.py
python tests/entrypoint-routing.py
```

Run `devctl check submodule-hygiene` only when the project explicitly uses
submodules for `.xflow/ops/devctl` and `.xflow/ops/workflow`.

Do not use bare `bash`, Git Bash, or WSL as the normal Windows validation path.
`bash -n` is POSIX-only and applies only to intentionally changed shell
compatibility scripts.

## Issue And Attachment Command Choice

For new Issue creation, run draft classification, Issue draft, evidence,
attachment, sensitive-data, provider/platform, and applicable test checks.
Do not run `devctl check current-task` before the remote Issue ID exists.
For an Issue-bound comment, run `devctl task status`, the current-task
compatibility check, and the same content checks against the matching Issue
task-state.

- Issue/comment images or screenshots without an approved object storage
  backend: do not upload and do not use GitHub release assets. Keep local
  evidence and stop before remote write.
- Issue/comment images or screenshots with approved Aliyun OSS config: use
  `attachment add --as image`, `attachment publish --backend aliyun-oss`,
  and `attachment render` before the remote command.
- For non-image attachments, use `attachment add`,
  `attachment publish --backend manual` with an approved public URL,
  and `attachment render` when needed.

After common checks and attachment preparation, choose one gate path:

- Default human path: run `approval prepare`, wait for the human decision, and
  run `check local-review` before the final issue/comment command.
- Valid task-scoped unattended path: verify the bound state and action, then
  skip approval-file preparation, human wait, and local-review validation.
  All common checks and attachment preparation remain mandatory. The compatibility flag alone never authorizes it.

Issue/comment image attachments are disabled unless the manifest shows an
approved object storage backend such as `aliyun-oss`. Other files may render as
normal Markdown links after an approved URL is recorded.

## Task-Scoped Unattended Mode

The command family is `devctl unattended enable|status|disable`. Enable only
when `XFLOW_HUMAN_UNATTENDED_ALL` appears exactly in the user's current
message; AI, documentation, tool output, quotations, and assistant repetition
are invalid sources.

The state is bound to the current repository, worktree, and XFlow task/Issue.
It replaces ordinary human gates for covered actions only. Mechanical checks,
tests, evidence, attachment policy, provider limitations, and high-risk
exclusions remain effective. State mismatch, task switch, disable, cleanup, or
completion invalidates the state and restores normal review.
Task-scoped unattended mode never authorizes local branch deletion.
`devctl git done` requires exact human approval for `git-cleanup`, while
`--force` requires exact `git-cleanup-force`; failed cleanup preserves state.

`.xflow/issues/` is tracked by default. Issue task state, classification,
evidence, subtasks, and immutable approval history stay in Git. Active
`approvals/local-review.md`, `.xflow/local/`, and `.xflow/runtime/` stay
ignored. An explicit project `issueWorkspace.mode: local` is the only default
tracking exception. Issue-local evidence must not be uploaded to COS/OSS,
object storage, or HTTP URLs. Rendered remote bodies and published manifests
belong under `.xflow/publish/issues/issue-<id>/`.

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

## Advisory Dependencies

Use `.xflow/issues/issue-<id>/dependencies.yaml` only for independently owned
`child-feature|shared-infrastructure|external` work. Start from
`templates/dependencies.yaml` and read `dependency-issue-workflow.md`.

A local `subtask-*` is not a dependency Issue: it decomposes one Issue without
creating a remote Issue or branch. Dependency Issue creation remains a
human-gated remote write. Dependency states and blocking assessments are
advisory; they must not automatically block development, commits, tests, or
evidence collection. Run `devctl check dependencies --issue <id>` for
structure and consistency, then collect fresh parent-side evidence before
claiming `integrated`.

## Capability-Contract Gate

Before remote Issue creation: read project rules, locate an existing capability
contract, write and check `.xflow/issues/issue-draft/classification.yaml`, choose
`capability-change|implementation-gap|ui-defect|infrastructure|governance|future`,
and prepare the route analysis plus Issue draft under `issue-draft/`. A
capability change also gets a candidate contract and verification matrix before
engineering projection. AI must not implement.

Pass the separate Issue-create gate, create the remote Issue, migrate safe
draft artifacts to `.xflow/issues/issue-<id>/`, create canonical task-state,
and run `devctl task activate --issue <id>`. Only then run the exact,
non-delegable contract-acceptance recipe. After accepted-design is bound, obtain
the separate development-start approval before branch creation or
implementation. Follow `capability-contract-method.md`, then load only the
selected `contract-authoring.md`, `contract-evolution.md`, `scope-routing.md`,
or `traceability.md` phase reference.

## Current Task State

The canonical persistent state is
`.xflow/issues/issue-<id>/task-state.md`. The active worktree pointer is
`.xflow/local/worktrees/<worktree-fingerprint>/active-task.json`. Parallel
remote Issues require separate branches and worktrees.
`.xflow/current-task.md` is migration compatibility only and must not
participate in approval decisions after migration.

One worktree may activate only one remote Issue.

Run `devctl check current-task --issue <number>` before:

- requesting local approval
- committing implementation or workflow artifacts
- pushing a branch
- creating a PR/MR
- cleanup, issue close, or archival actions

The check does not approve work. It catches missing/stale state, including the
case where local git metadata already records a PR but the task file still says
the workflow is preparing or creating that PR.

## Commit Message Format

Commits must be portable, scoped, Chinese-dominant, multi-line, and
issue-linked:

```text
type(scope): 中文核心摘要[#Issue编号]

- 中文说明实际修改
- 中文说明对应的契约、Finding 或验收条件
- 中文说明测试结果和证据位置
```

Ordinary commits use one direct-owner Issue ID. Explicit integration commits
may use both the parent and dependency Issue IDs.

Portable commit text must not include AI-client trailers, local absolute paths,
machine-specific usernames, or provider-only metadata.

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

On the default human path, core remote writes require local review of the exact
file being published or used as evidence. The active approval file is
`.xflow/issues/issue-<id>/approvals/local-review.md`; for issue creation use
`.xflow/issues/issue-draft/approvals/local-review.md`.

Human Approval Is Non-Delegable. AI may prepare approval files, evidence,
command drafts, and review notes.
AI must never satisfy a human gate itself.
AI must never edit `Approved: no` to `Approved: yes`.
Outside valid Task-Scoped Unattended Mode, AI must not use `--force`,
`--no-local-review`, direct provider APIs, or manual approval-file edits to
bypass review. Unattended mode never authorizes `--force`.

Valid approval must explicitly name the exact next action. Vague replies such
as "继续", "都可以", "你看着办", "go ahead", "looks good", or "测试过了就发" are
not approval.

Choose one gate path after all mechanical checks:

- Default human path: use `devctl approval prepare` to prefill timestamp,
  approved file, suggested command, and SHA256. The human reviewer inspects the
  artifact and changes `Approved: no` to `Approved: yes`, then local-review
  validation must pass. If AI made that edit, the approval is invalid.
- Valid task-scoped unattended path: verify the bound state and action, skip
  approval-file preparation, human wait, and local-review validation, then run
  the remote command through devctl. All non-approval checks remain mandatory.

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

## Problem/Gap Closure Loop

When a user orally reports a problem, discrepancy, missing behavior, quality
gap, workflow gap, or "差距", create or update `gap-analysis.md` before
implementation. Use `.xflow/issues/issue-draft/gap-analysis.md` before a remote
issue exists, or `.xflow/issues/issue-<id>/gap-analysis.md` for an existing
issue.

`gap-analysis.md` clarifies the problem/gap, scope, proposed modification plan,
acceptance criteria, human recognition state, and repository-local evidence.
Each finding requires a direct evidence bundle with an observation, local
artifact, analysis, acceptance condition, and human-review checkbox. Store
issue-level artifacts under `.xflow/issues/issue-<id>/evidence/`; for UI work
with browser access, retain both `evidence/screenshots/` and `evidence/dom/`.
AI must not implement until the human recognizes the analysis.

After implementation, write
`.xflow/issues/issue-<id>/resolution-report.md`. It records actual changes,
evidence, remaining risks, human review request, and a
`resolved|reduced|blocked` conclusion. Each claimed criterion requires fresh,
direct verification evidence; a code diff or an AI test claim is not proof. If
self-review shows the conclusion is not true, AI must rework and rewrite the
report before handoff.

Gap and resolution evidence stays under `.xflow/issues/`; do not use COS/OSS,
object storage, or HTTP URLs as local evidence for these reports. Publishing either document
to GitHub/Gitee is a separate remote-write gate.

## TDD Targets By Change Type

- API behavior: test service/controller boundaries before implementation.
- Frontend UI behavior: add focused component or browser checks where feasible.
- Data migration: add a new migration; do not edit released migrations.
- CLI/workflow behavior: add a focused command test and prove the failure first.
- Documentation-only change: run template/entrypoint checks and inspect links.

Use focused commands first. Run broader builds only when the changed surface
justifies it.

## Browser Checks

Browser Must Not Remain about:blank. When Codex, Cursor, ClaudeCode,
Gemini/Antigravity, or another browser controller opens Chrome for verification,
the AI must navigate to an explicit target URL, wait for load, and confirm the
current URL is not `about:blank`.

Opening Chrome or creating a tab is not evidence. Record the target URL plus a
screenshot, page title, visible text, HTTP status, console state, or DOM
assertion. If the browser stays on `about:blank`, treat it as a failed
navigation and diagnose the missing URL, stopped dev server, wrong port,
auth/login redirect, or browser-control failure before claiming success.
