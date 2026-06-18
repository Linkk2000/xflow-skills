# PowerShell Native Command Notes

Use this guidance when an AI assistant must run XFlow commands on Windows.

- Prefer direct native commands:
  `git status --short --branch`
- Avoid native-command pipelines when exit code matters:
  do not use `git ... 2>&1 | Out-String` as the control path.
- If output must be captured, run the command first and inspect
  `$LASTEXITCODE` immediately.
- For long Markdown, JSON, commit bodies, Issue bodies, comments, or PR/MR
  bodies, write a UTF-8 file and pass the path with `--body-file` or `-F`.
- Keep temporary files under `.xflow/local/` when they are not meant for Git.
- Preserve `PYTHONDONTWRITEBYTECODE=1` for devctl Python calls to avoid
  `__pycache__`.
