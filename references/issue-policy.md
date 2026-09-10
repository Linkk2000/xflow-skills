# Issue Policy

## Creation History And Branch Start

After a provider-confirmed Issue creation, migrate ordinary draft materials
(classification, proposal, candidate contract, matrix, body and evidence) to
the numbered Issue workspace. Do not move the entire draft directory over an
already-created numbered directory: tooling may already have written history there.

The numbered Issue's successful issue-create record can reference its original
claim, reviewed approval and approved-body snapshot under
`.xflow/issues/issue-draft/approvals/history/`. Preserve these files and their
references byte-for-byte at their original paths. Their historical draft
identity is intentional; do not replace it with the new number.

At task-branch-start, compatible devctl versions admit only those exact paths
after validating the completed claim, provider-confirmed Issue, current
repository/worktree, canonical paths and sealed digests. This is not a blanket
exception for issue-draft and is not a reusable approval. Unrelated drafts,
tampered or missing history, and another Issue/worktree's records remain rejected.
The issue-create branch is historical; it is not the new task branch identity.

After the separately approved final branch is created, include these validated,
trackable issue-create history files in the Early artifact commit alongside the
numbered Issue workspace. Do not include active approvals or local runtime
receipts. Do not ignore, delete, relocate, or hand-edit history to satisfy a
branch check. If the installed runtime rejects its own valid creation history,
report its version and exact failure; update through an authorized tool fix.

This exception does not replace task-branch-start approval, contract acceptance,
or development-start permission. Each remains a separate decision.

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
