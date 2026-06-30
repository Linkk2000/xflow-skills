# Devctl Contract

## Entrypoints

- Windows: `devctl.ps1`
- POSIX: `devctl`
- Both entrypoints must route normal XFlow commands to `python -m xflow`.
  POSIX shell scripts may remain only as compatibility helpers. Windows
  validation must not invoke bare `bash`, Git Bash, or WSL.

Search anchor: Windows validation must not invoke bare `bash`.

## Default Variable Locations

- XFlow Skill source: `git@github.com:Linkk2000/xflow-skills.git`
- devctl source: `git@github.com:Linkk2000/xflow-devctl.git`
- Windows global source root: `%USERPROFILE%\.codex\xflow\repos`
- POSIX global source root: `~/.codex/xflow/repos`
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
- `DEVCTL_REPO_ROOT`: target repository root.
- `DEVCTL_TOOL_ROOT`: devctl installation root.
- `DEVCTL_BASE_BRANCH`: default base branch, otherwise auto-detect `master` then `main`.
- `DEVCTL_BRANCH_PREFIX`: default `feature`.

## Command Semantics

- `devctl init`: bootstrap a repository with XFlow project rules, cross-agent adapters, local devctl entrypoints, source/ref binding metadata, and default config templates. This is local-only and must not create issues, branches, commits, pushes, or MR/PRs.
- `devctl restore`: rehydrate an existing XFlow repository on a new machine from `.xflow/xflow.json`. It restores cache/submodule sources, local devctl entrypoints, and `.xflow/devctl`. This is local-only and must not create issues, branches, commits, pushes, or MR/PRs.
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
- `devctl check branch-scope`: validate current branch is issue-bound.
- `devctl issue create --attachments <manifest>`: create issue only after the
  body file and attachment manifest have both passed review and all attachment
  non-image placeholders have been replaced with approved published URLs.
  Image MIME types or Markdown image attachments fail before remote writes.
- `devctl issue create --attach-file <path> --upload-attachments github`:
  legacy generic-file path. It must not be used for images or screenshots;
  issue creation rejects image attachments before any GitHub issue or release
  upload request.
- `devctl issue create --no-local-review`: create an issue without attachments
  when the current user explicitly requested unattended operation for that exact
  command.
- `devctl issue comment --attachments <manifest>`: comment only after the body
  file and attachment manifest have both passed review. Image MIME types or
  Markdown image attachments fail before remote writes.
- `devctl issue comment --attach-file <path> --upload-attachments github`:
  legacy generic-file path. It must not be used for images or screenshots.
- `devctl issue comment --no-local-review`: comment without attachments when
  explicitly authorized by the current user for that exact command.
- `devctl attachment add`: register or copy a pasted file/image into the
  XFlow attachment directory and update the manifest.
- `devctl attachment check`: verify manifest hashes, MIME/size metadata,
  placeholder usage, and final-body publication guards.
- `devctl attachment publish`: publish manifest items to the configured backend
  and record reviewed URLs.
  On GitHub, `--backend github` uses the legacy `xflow-attachments` release by
  default and records each asset's GitHub `browser_download_url`. It rejects
  image attachments; do not use that backend as an issue/comment image store.
- `devctl attachment render`: render a final body file by replacing reviewed
  attachment placeholders with published URLs.

## AI Call Recipes

Use these recipes as the normal command surface. Do not probe by retrying
random flag combinations after an error; read the remote state or run the
matching check command first.

Plain unattended issue:

```text
devctl issue create "<title>" --body-file issue.md --no-local-review
```

Plain unattended comment:

```text
devctl issue comment <number> --body-file comment.md --no-local-review
```

Approved branch push:

```text
devctl approval prepare --issue <number> --action git-push --file .xflow/issues/issue-<number>/walkthrough.md
devctl check local-review --issue <number> --file .xflow/issues/issue-<number>/walkthrough.md --action git-push
devctl git push --issue <number> --file .xflow/issues/issue-<number>/walkthrough.md
```

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
devctl attachment publish --issue draft --backend manual --url att-001=https://public.example/notes.txt --body-file issue.md --output issue.final.md
devctl approval prepare --issue draft --action issue-create --file issue.final.md --attachments .xflow/issues/issue-draft/attachments/manifest.json
devctl check local-review --issue draft --file issue.final.md --action issue-create --attachments .xflow/issues/issue-draft/attachments/manifest.json
devctl issue create "<title>" --body-file issue.final.md --attachments .xflow/issues/issue-draft/attachments/manifest.json
```

Issue/comment image attachments are disabled. Do not use GitHub release assets
as an issue image store. `--attach-file` with an image MIME type or Markdown
image attachment fails before issue/comment remote writes. Non-image files use
normal Markdown links after an approved URL is recorded. `GITHUB_TOKEN` is
required for GitHub issue/comment remote writes.
If there are no attachments, omit all attachment flags.

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
