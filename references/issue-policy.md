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
- Issue/comment image attachments are disabled. Do not use
  `--upload-attachments github` or GitHub release assets to publish screenshots
  or images into issues/comments.
- For non-image attachments, use a reviewed manifest and an approved public URL
  plan before the remote write.
- If there are no attachments, `devctl issue create ... --no-local-review`
  remains valid when the current user explicitly authorized unattended issue
  creation for that exact command.
- Do not publish local file paths, chat-client temp paths, `.xflow/` paths, or
  unresolved `xflow-attachment://` placeholders in remote bodies.
- Before creating, check for an open issue with the same exact title.
- If the title was edited after a failed attempt, manually review recent open issues for near duplicates before retrying.
- If creation command fails after a network call may have happened, list/show remote issues before retrying.
