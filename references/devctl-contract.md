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
- `devctl git push`: push current branch only.
- `devctl git mr`: create MR/PR only, after push has already been approved or completed.
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
  placeholders have been replaced with approved published URLs.
- `devctl issue create --attach-file <path> --upload-attachments github`:
  register a pasted file or image, upload it to GitHub release assets, render a
  final body with GitHub URLs, and create the issue. `--no-local-review` is
  allowed only when the current user explicitly requested unattended operation
  for that exact command.
- `devctl issue create --no-local-review`: create an issue without attachments
  when the current user explicitly requested unattended operation for that exact
  command.
- `devctl issue comment --attachments <manifest>`: comment only after the body
  file and attachment manifest have both passed review.
- `devctl issue comment --attach-file <path> --upload-attachments github`:
  same attachment upload and render flow for an issue comment.
- `devctl issue comment --no-local-review`: comment without attachments when
  explicitly authorized by the current user for that exact command.
- `devctl attachment add`: register or copy a pasted file/image into the
  XFlow attachment directory and update the manifest.
- `devctl attachment check`: verify manifest hashes, MIME/size metadata,
  placeholder usage, and final-body publication guards.
- `devctl attachment publish`: publish manifest items to the configured backend
  and record reviewed URLs.
  On GitHub, `--backend github` uses the `xflow-attachments` release by default
  and records each asset's GitHub `browser_download_url`.
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

Unattended GitHub attachment issue:

```text
devctl issue create "<title>" --body-file issue.md --attach-file screenshot.png --attach-file notes.txt --upload-attachments github --no-local-review
```

Unattended GitHub attachment comment:

```text
devctl issue comment <number> --body-file comment.md --attach-file screenshot.png --attach-file notes.txt --upload-attachments github --no-local-review
```

Reviewed issue with attachments:

```text
devctl attachment add --issue draft --file screenshot.png --as auto
devctl attachment publish --issue draft --backend github --body-file issue.md --output issue.final.md
devctl approval prepare --issue draft --action issue-create --file issue.final.md --attachments .xflow/issues/issue-draft/attachments/manifest.json
devctl check local-review --issue draft --file issue.final.md --action issue-create --attachments .xflow/issues/issue-draft/attachments/manifest.json
devctl issue create "<title>" --body-file issue.final.md --attachments .xflow/issues/issue-draft/attachments/manifest.json
```

`--attach-file` accepts any file. Image MIME types render as Markdown images;
other files render as links. `--upload-attachments github` uploads files to
the `xflow-attachments` GitHub release by default and writes a rendered final
body file next to the input body unless `--rendered-body-file` is provided.
`GITHUB_TOKEN` is required for GitHub uploads and issue/comment remote writes.
If there are no attachments, omit all attachment flags.

Plain text search anchors for agents: --attach-file accepts any file.
GITHUB_TOKEN is required for GitHub uploads.

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
