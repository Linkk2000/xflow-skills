# Issue Policy

- Draft issue title/body/labels in Chinese unless project rules say otherwise.
- Use `references/issue-template.md`.
- Use `--body-file` for multiline or shell-sensitive Markdown.
- Do not probe by retrying random flag combinations. If unsure, read
  `references/attachment-policy.md` and `references/devctl-contract.md`, then
  choose the matching AI call recipe.
- If the issue or comment references pasted files, screenshots, or images, read
  `references/attachment-policy.md` and create an attachment manifest before
  approval.
- Issue/comment image attachments are disabled unless the manifest shows an
  approved object storage backend. Do not use `--upload-attachments github` or
  GitHub release assets to publish screenshots or images into issues/comments.
- For screenshots or images that must appear in GitHub/Gitee, use the approved object storage backend:
  `devctl attachment publish --issue draft --backend aliyun-oss`.
- For non-image attachments, use a reviewed manifest and an approved public URL
  plan before the remote write.
- Object storage credentials such as `ALIYUN_OSS_ACCESS_KEY_SECRET` belong in
  user or project env files and must not appear in issues, comments, commits,
  Markdown guides, or manifests.
- Task-Scoped Unattended Mode may replace the ordinary Issue approval gate only
  when a valid repository/worktree/task-bound state covers the current action.
  `--no-local-review` alone is invalid and cannot create that state.
- Unattended mode does not bypass issue structure, duplicate detection,
  attachment, sensitive-data, evidence, provider, or platform checks.
- If an issue is too large, create local subtasks under
  `.xflow/issues/issue-<id>/subtask-001/` and run
  `devctl check subtask --issue <id>`. Subtask evidence must stay in the
  repository and must not be uploaded to COS/OSS.
- `.xflow/issues/` is tracked by default. Only an explicit project
  `issueWorkspace.mode: local` may opt out. Track Issue task state,
  classification, plans, evidence, reports, subtasks, and immutable approval
  history; ignore active `approvals/local-review.md`.
- Do not move Issue-local evidence to COS/OSS/object storage or HTTP URLs, and
  do not store non-null `publishedUrl` values in it. Put rendered remote bodies
  and published manifests under `.xflow/publish/issues/issue-<id>/`.
- One worktree may activate only one remote Issue. Use a separate branch and
  worktree for each independently active remote Issue.
- Do not publish local file paths, chat-client temp paths, `.xflow/` paths, or
  unresolved `xflow-attachment://` placeholders in remote bodies.
- Before creating, check for an open issue with the same exact title.
- If the title was edited after a failed attempt, manually review recent open issues for near duplicates before retrying.
- If creation command fails after a network call may have happened, list/show remote issues before retrying.
