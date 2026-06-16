# XFlow Project Rules

Use this repository's local XFlow workflow. Do not rely on a global temporary
development checkout as the workflow source.

Hard rules:

- Read this file, `README.md`, `.cursorrules`, and `.xflow/current-task.md`
  when present before acting.
- Use repository-local `devctl` or `devctl.ps1` from the project root.
- Do not perform remote writes before local human review approves the exact
  file being published or used as evidence.
- Active approval file:
  `.xflow/issues/issue-<id>/approvals/local-review.md`.
- For issue creation, use:
  `.xflow/issues/issue-draft/approvals/local-review.md`.
- Do not create alternate active approval files such as `local-review-mr.md`.
- Use `--body-file` for Issue, comment, and PR/MR bodies.
- Run `git status --short --branch` before committing and include only
  task-related files.
- Do not add AI-client co-author trailers, including
  `Co-authored-by: Cursor <cursoragent@cursor.com>`.

Remote-write checklist:

1. Create the body/evidence file.
2. Run the matching `devctl check ...` command.
3. Run `devctl approval prepare --issue <id> --action <action> --file <file>`.
4. Stop for human review.
5. Continue only after the human sets `Approved: yes`.
6. Run `devctl check local-review --issue <id> --file <file> --action <action>`.
7. Run the approved remote-write command.

Use the user's language for Git-related public text: commit messages, remote
Issue text, remote PR/MR text, review comments, and branch task summaries.
