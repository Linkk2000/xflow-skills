# Devctl Contract

## Entrypoints

- Windows: repository-local `.\devctl.ps1`
- POSIX: repository-local `./devctl`
- Both entrypoints must route normal XFlow commands to `python -m xflow`.
  POSIX shell scripts may remain only as compatibility helpers. Windows
  validation must not invoke bare `bash`, Git Bash, or WSL.
- No global devctl entrypoint is required. Do not rely on a user-level
  `%USERPROFILE%\.codex\xflow\bin\devctl.ps1` or PATH shim for repository work.

Search anchor: Windows validation must not invoke bare `bash`.

## Project-Local Compatibility Gate

This file is a cross-version Skill contract. Before using newer commands or
options such as `unattended`, `check dependencies`, or the extended
`check commit-msg`, inspect the project-local `devctl help` output (on Windows,
`.\devctl.ps1 help`; on POSIX, `./devctl help`) and the relevant subcommand
help. If support is absent, stop and update or restore the project-local devctl
from the project's configured XFlow source before continuing. AI must not probe by trying commands or pretend the capability is available.

Do not permanently label these commands unimplemented: availability depends on
the project-local devctl version. Project-local help is authoritative for the
current repository.

## Default Variable Locations

- XFlow Skill source: `git@github.com:Linkk2000/xflow-skills.git`
- devctl source: `git@github.com:Linkk2000/xflow-devctl.git`
- Project skill/workflow source path: `.xflow/ops/workflow`
- Project devctl source path: `.xflow/ops/devctl`
- `XFLOW_ENV_FILE`: optional unified env file.
- `GITEE_ENV_FILE`: defaults to `~/gitee.env.local`.
- `GITHUB_TOKEN`: GitHub token from environment or env file.
- `GITEE_TOKEN`: Gitee token from environment or env file.
- `XFLOW_PLATFORM`: `github` or `gitee`, otherwise inferred from `origin`.
  Avoid setting it in user-level `~/.xflow/env.local` when working across
  both GitHub and Gitee projects; use project-local `.xflow/local/env.local`
  or explicit `XFLOW_ENV_FILE` for project-specific overrides.
- `GITHUB_API_BASE`: optional GitHub API base override.
- `GITEE_API_BASE`: optional Gitee v5 API base override; default is `https://gitee.com/api/v5`.
- `XFLOW_ATTACHMENT_BACKEND`: optional attachment backend selector; use
  `aliyun-oss` for the shared object storage backend.
- `ALIYUN_OSS_BUCKET`, `ALIYUN_OSS_REGION`, `ALIYUN_OSS_ACCESS_KEY_ID`,
  `ALIYUN_OSS_ACCESS_KEY_SECRET`: Aliyun OSS upload config. Store shared values
  in `%USERPROFILE%\.xflow\env.local` on Windows or `~/.xflow/env.local` on
  POSIX; store project overrides in `.xflow/local/env.local`.
- `ALIYUN_OSS_ENDPOINT`, `ALIYUN_OSS_PUBLIC_BASE_URL`, `ALIYUN_OSS_PREFIX`:
  optional Aliyun OSS endpoint, public URL, and object key prefix.
- `DEVCTL_REPO_ROOT`: target repository root.
- `DEVCTL_TOOL_ROOT`: devctl installation root.
- `DEVCTL_BASE_BRANCH`: default base branch, otherwise auto-detect `master` then `main`.
- `DEVCTL_BRANCH_PREFIX`: default `feature`.

## Command Semantics

- `devctl init`: bootstrap a repository with XFlow project rules, cross-agent adapters, local devctl entrypoints, project-local `.xflow/ops/` tool binding metadata, and default config templates. This is local-only and must not create issues, branches, commits, pushes, or MR/PRs.
- `devctl restore`: rehydrate an existing XFlow repository on a new machine from `.xflow/xflow.json`. It restores project-local `.xflow/ops/` tools, local devctl entrypoints, and `.xflow/devctl`. This is local-only and must not create issues, branches, commits, pushes, or MR/PRs.
- `devctl issue create`: create issue only after duplicate check.
- `devctl git push`: push current branch only after `Approved Action: git-push`.
- `devctl git mr`: create MR/PR only, after push has already been approved or
  completed. It must not push task code implicitly. After the provider returns
  a PR/MR number and URL, it may create and push one metadata-only state
  backfill commit containing XFlow PR number/URL state.
- `devctl git start/status/commit-msg/done`: Git lifecycle commands implemented
  by Python core for normal Windows/POSIX use.
- `devctl app start-frontend/status/stop-frontend`: App helper commands
  implemented by Python core for normal Windows/POSIX use.
- `devctl doctor`: check environment health.
- `devctl check encoding`: check UTF-8/LF and shell syntax health.
- `devctl check commit-msg`: validate commit message against project rules.
- `devctl check commit-msg --file <path> --issue <id>`: validate a prepared
  feature-branch commit message, including direct-owner Issue linkage, before
  commit.
- `devctl check dependencies --issue <id>`: validate dependency YAML structure,
  enums, required fields, evidence paths, and integration consistency. Results
  are structural warnings/checks, not business blocking decisions; dependency
  state alone does not block development, commits, tests, or evidence.
- `devctl check branch-scope`: validate current branch is issue-bound.
- `devctl unattended enable --issue <id|draft> --confirm XFLOW_HUMAN_UNATTENDED_ALL`:
  enable task-scoped unattended state only after the Skill has verified that
  the exact safety word came from the user's current message.
- `devctl unattended status`: report active, inactive, or invalid state without
  exposing credentials or the safety word.
- `devctl unattended disable`: idempotently remove the local state and restore
  ordinary human gates.
- `devctl check issue-evidence --issue <id> [--publish-root .xflow/publish/issues/issue-<id>]`:
  validate that `.xflow/issues/issue-<id>/` remains a local evidence workspace
  without COS/OSS published URLs or non-null `publishedUrl` values.
- `devctl check subtask --issue <id> [--path .xflow/issues/issue-<id>/subtask-001]`:
  validate local subtask directory naming, README sections, source file, local
  evidence links, and conclusion status.
- `devctl check gap-analysis --issue draft|<id> [--file .xflow/issues/issue-<id>/gap-analysis.md]`:
  validate the Problem/Gap Closure Loop analysis before implementation. It
  requires sections for user statement, clarified gap, analysis, local
  evidence, scope, proposed plan, acceptance criteria, and `Recognized: yes`.
- `devctl check resolution-report --issue <id> [--file .xflow/issues/issue-<id>/resolution-report.md]`:
  validate the completion report after implementation. It requires local
  evidence, actual changes, `resolved|reduced|blocked` conclusion, self-review,
  remaining risks, and human review request. `resolved` and `reduced` reports
  must not contain unchecked AI self-review items.
- `devctl issue create --attachments <manifest>`: create issue only after the
  body file and attachment manifest have both passed review and all attachment
  placeholders have been replaced with approved published URLs. Image MIME
  types or Markdown image attachments require an approved object storage
  backend such as `aliyun-oss`; otherwise they fail before remote writes.
- `devctl issue create --attach-file <path> --upload-attachments github`:
  legacy generic-file path. It must not be used for images or screenshots;
  issue creation rejects image attachments before any GitHub issue or release
  upload request.
- `devctl issue create --no-local-review`: compatibility flag accepted only
  when a valid task-scoped unattended state covers the current Issue and
  action. The flag alone is invalid. Search anchor: create an issue without
  attachments.
- `devctl issue comment --attachments <manifest>`: comment only after the body
  file and attachment manifest have both passed review. Image MIME types or
  Markdown image attachments require an approved object storage backend such as
  `aliyun-oss`; otherwise they fail before remote writes.
- `devctl issue comment --attach-file <path> --upload-attachments github`:
  legacy generic-file path. It must not be used for images or screenshots.
- `devctl issue comment --no-local-review`: compatibility flag accepted only
  when a valid task-scoped unattended state covers the current Issue and
  action. The flag alone is invalid.
- `devctl attachment add`: register or copy a pasted file/image into the
  XFlow attachment directory and update the manifest.
- `devctl attachment check`: verify manifest hashes, MIME/size metadata,
  placeholder usage, and final-body publication guards.
- `devctl attachment publish`: publish manifest items to the configured backend
  and record reviewed URLs in `.xflow/publish/issues/issue-<id>/`, not in
  `.xflow/issues/issue-<id>/`.
  On GitHub, `--backend github` uses the legacy `xflow-attachments` release by
  default and records each asset's GitHub `browser_download_url`. It rejects
  image attachments; do not use that backend as an issue/comment image store.
  With `--backend aliyun-oss`, devctl uploads manifest files to Aliyun OSS using
  env-file credentials and records `backend`, `provider`, `bucket`,
  `objectKey`, and `publishedUrl`. AccessKey values must not be written to
  manifests.
- `devctl attachment render`: render a final body file by replacing reviewed
  attachment placeholders with published URLs. Rendered remote bodies must be
  written under `.xflow/publish/issues/issue-<id>/`.

## AI Call Recipes

Use these recipes as the normal command surface. Do not probe by retrying
random flag combinations after an error; read the remote state or run the
matching check command first.

Human Approval Is Non-Delegable. AI may prepare approval files, evidence,
command drafts, and review notes.
AI must never satisfy a human gate itself.
AI must never edit `Approved: no` to `Approved: yes`.
Outside valid Task-Scoped Unattended Mode, AI must not use `--force`,
`--no-local-review`, direct provider APIs, or manual approval-file edits to
bypass review.

Task-scoped unattended commands:

```text
devctl unattended enable --issue IK152D --confirm XFLOW_HUMAN_UNATTENDED_ALL
devctl unattended status
devctl unattended disable
```

The enable command is valid only when the exact safety word came from the
user's current message. State is stored in ignored
`.xflow/local/unattended.json` and bound to repository, worktree, and
task/Issue. It contains no safety word or credentials. A `draft` state migrates
atomically only after confirmed Issue creation. Any mismatch or invalid state
fails closed; task switch, completion, cleanup, and `devctl git done` remove or
invalidate it.

Covered actions skip ordinary human gates only after their normal mechanical
checks pass. Evidence, tests, attachment and sensitive-data checks, provider
limitations, branch protection, and platform policy remain mandatory. Force
push, history rewrite, destructive deletion, and secret or permission changes
remain excluded.
Task-scoped unattended mode never authorizes local branch deletion. Run
`devctl git done --issue <id> --file <resolution-report.md>` only after exact
human approval for `git-cleanup`; `--force` requires exact
`git-cleanup-force` approval. Failed cleanup must not disable the state.

Each valid bypass prints:

```text
[UNATTENDED] Human approval gate bypassed for current task IK152D.
```

The audit line identifies approval provenance only; it is not proof that any
business, evidence, attachment, test, or provider check passed.

Approved branch push:

```text
devctl approval prepare --issue <number> --action git-push --file .xflow/issues/issue-<number>/walkthrough.md
devctl check local-review --issue <number> --file .xflow/issues/issue-<number>/walkthrough.md --action git-push
devctl git push --issue <number> --file .xflow/issues/issue-<number>/walkthrough.md
```

Portable scoped commit message:

```text
type(scope): 中文核心摘要[#Issue编号]

- 中文说明实际修改
- 中文说明对应的契约、Finding 或验收条件
- 中文说明测试结果和证据位置
```

Feature branches run:

```text
devctl check commit-msg --file .xflow/local/commit-message.txt --issue IK152D
```

`devctl git commit-msg` should generate or accept messages in this shape.
Do not add AI-client co-author trailers, local absolute paths, or provider-only
metadata to commit messages.

Advisory dependency check:

```text
devctl check dependencies --issue IK152D
```

This check validates structure and consistency. It must not decide whether
development should pause or treat `active` or `available` as a business hard
block. `discovered` is a pre-ledger analysis stage; after remote Issue identity
creation, the first YAML status is `active`.

Local subtask check:

```text
devctl check subtask --issue <number> --path .xflow/issues/issue-<number>/subtask-001
```

Subtask evidence must stay in the repository under the current subtask's
`evidence/` directory. Do not store subtask evidence in COS/OSS or object
storage; object storage is only for rendered remote issue/comment/PR bodies.

Issue workspace evidence check:

```text
devctl check issue-evidence --issue <number>
```

`.xflow/issues/issue-<number>/` is local evidence and approval state only.
Published attachment manifests and rendered remote bodies belong under
`.xflow/publish/issues/issue-<number>/`.

Problem/Gap Closure Loop:

```text
devctl check gap-analysis --issue <number>
devctl check resolution-report --issue <number>
```

`gap-analysis.md` is created before implementation from the user's oral problem
or gap report. It must contain local evidence and human recognition. After
implementation, `resolution-report.md` records actual changes, local evidence,
and a `resolved|reduced|blocked` conclusion. If AI self-review finds the report
is not true, AI must rework and rewrite the report before human handoff.
Gap/resolution evidence must remain under `.xflow/issues/issue-<number>/`, not
in COS/OSS or object storage.

Approved MR/PR creation:

```text
devctl approval prepare --issue <number> --action git-mr --file .xflow/issues/issue-<number>/mr-draft.md
devctl check local-review --issue <number> --file .xflow/issues/issue-<number>/mr-draft.md --action git-mr
devctl git mr --title "<title>" --body-file .xflow/issues/issue-<number>/mr-draft.md --issue <number>
```

`devctl git mr` fails if the current branch has no upstream or has unpushed
task commits. The only push it performs is the post-create metadata-only state
backfill commit after the PR/MR number and URL are known.

Reviewed non-image attachment issue:

```text
devctl attachment add --issue draft --file notes.txt --as file
devctl attachment publish --issue draft --backend manual --url att-001=https://public.example/notes.txt --body-file issue.md --output .xflow/publish/issues/issue-draft/issue.final.md
devctl approval prepare --issue draft --action issue-create --file .xflow/publish/issues/issue-draft/issue.final.md --attachments .xflow/publish/issues/issue-draft/attachments/manifest.json
devctl check local-review --issue draft --file .xflow/publish/issues/issue-draft/issue.final.md --action issue-create --attachments .xflow/publish/issues/issue-draft/attachments/manifest.json
devctl issue create "<title>" --body-file .xflow/publish/issues/issue-draft/issue.final.md --attachments .xflow/publish/issues/issue-draft/attachments/manifest.json
```

Reviewed Aliyun OSS image issue:

```text
devctl attachment add --issue draft --file screenshot.png --as image
devctl attachment publish --issue draft --backend aliyun-oss --manifest .xflow/issues/issue-draft/attachments/manifest.json
devctl attachment render --issue draft --manifest .xflow/publish/issues/issue-draft/attachments/manifest.json --input issue.md --output .xflow/publish/issues/issue-draft/issue.final.md
devctl approval prepare --issue draft --action issue-create --file .xflow/publish/issues/issue-draft/issue.final.md --attachments .xflow/publish/issues/issue-draft/attachments/manifest.json
devctl check local-review --issue draft --file .xflow/publish/issues/issue-draft/issue.final.md --action issue-create --attachments .xflow/publish/issues/issue-draft/attachments/manifest.json
devctl issue create "<title>" --body-file .xflow/publish/issues/issue-draft/issue.final.md --attachments .xflow/publish/issues/issue-draft/attachments/manifest.json
```

Issue/comment image attachments are disabled unless the manifest shows an
approved object storage backend such as `aliyun-oss`. Do not use GitHub release
assets as an issue image store. `--attach-file` with an image MIME type or
Markdown image attachment fails before issue/comment remote writes unless the
image was first published through the approved attachment flow. Non-image files
use normal Markdown links after an approved URL is recorded. `GITHUB_TOKEN` is
required for GitHub issue/comment remote writes.
If there are no attachments, omit all attachment flags.

`--no-local-review` must not be used for push, MR/PR creation, merge, issue
close, branch deletion, conflict resolution, or any destructive action.

Plain text search anchors for agents: Issue/comment image attachments are disabled.
Do not use GitHub release assets as an issue image store.

## Provider Semantics

- GitHub provider calls use JSON bodies and GitHub REST repository paths.
- Gitee provider calls use the Gitee v5 OpenAPI shape and form/query
  parameters. For example, issue creation uses
  `POST /v5/repos/{owner}/issues` with `repo` in form data, while PR creation
  uses `POST /v5/repos/{owner}/{repo}/pulls`.
- Agents must call these providers only through `devctl`; direct imports of
  `xflow.providers` or direct GitHub/Gitee API calls are not normal workflow
  entrypoints.
- If attachment commands are not implemented in the local `devctl`, agents
  must stop and ask for a supported backend or tool update. They must not
  bypass the contract by uploading files manually through provider APIs.

## Canonical Sources

- XFlow Skill source: `git@github.com:Linkk2000/xflow-skills.git`
- devctl source: `git@github.com:Linkk2000/xflow-devctl.git`

Agents should not ask the user to paste long workflow text when these sources or local copies are available. For an empty repository, obtain or locate `xflow-devctl`, ask the source strategy gate if the project has no binding yet, then run `devctl init --target <repo>` with the selected source/ref/mode and stop for review.
