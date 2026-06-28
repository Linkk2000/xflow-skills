# Issue Policy

- Draft issue title/body/labels in Chinese unless project rules say otherwise.
- Use `references/issue-template.md`.
- Use `--body-file` for multiline or shell-sensitive Markdown.
- If the issue or comment references pasted files, screenshots, or images, read
  `references/attachment-policy.md` and create an attachment manifest before
  approval.
- Do not publish local file paths, chat-client temp paths, `.xflow/` paths, or
  unresolved `xflow-attachment://` placeholders in remote bodies.
- Before creating, check for an open issue with the same exact title.
- If the title was edited after a failed attempt, manually review recent open issues for near duplicates before retrying.
- If creation command fails after a network call may have happened, list/show remote issues before retrying.
