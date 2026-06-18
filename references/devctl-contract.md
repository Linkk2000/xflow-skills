# Devctl Contract

## Entrypoints

- Windows: `devctl.ps1`
- POSIX: `devctl`

## Default Variable Locations

- XFlow Skill source: `https://github.com/Linkk2000/xflow-skills`
- devctl source: `https://github.com/Linkk2000/xflow-devctl`
- Windows source cache root: `%USERPROFILE%\.xflow\sources`
- POSIX source cache root: `~/.xflow/sources`
- `XFLOW_ENV_FILE`: optional unified env file.
- `GITEE_ENV_FILE`: defaults to `~/gitee.env.local`.
- `GITHUB_TOKEN`: GitHub token from environment or env file.
- `GITEE_TOKEN`: Gitee token from environment or env file.
- `XFLOW_PLATFORM`: `github` or `gitee`, otherwise inferred from `origin`.
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
- `devctl doctor`: check environment health.
- `devctl check encoding`: check UTF-8/LF and shell syntax health.
- `devctl check commit-msg`: validate commit message against project rules.
- `devctl check branch-scope`: validate current branch is issue-bound.

## Provider Semantics

- GitHub provider calls use JSON bodies and GitHub REST repository paths.
- Gitee provider calls use the Gitee v5 OpenAPI shape and form/query
  parameters. For example, issue creation uses
  `POST /v5/repos/{owner}/issues` with `repo` in form data, while PR creation
  uses `POST /v5/repos/{owner}/{repo}/pulls`.
- Agents must call these providers only through `devctl`; direct imports of
  `xflow.providers` or direct GitHub/Gitee API calls are not normal workflow
  entrypoints.

## Canonical Sources

- XFlow Skill source: `https://github.com/Linkk2000/xflow-skills`
- devctl source: `https://github.com/Linkk2000/xflow-devctl`

Agents should not ask the user to paste long workflow text when these sources or local copies are available. For an empty repository, obtain or locate `xflow-devctl`, ask the source strategy gate if the project has no binding yet, then run `devctl init --target <repo>` with the selected source/ref/mode and stop for review.
