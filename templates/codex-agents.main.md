# XFlow Project Rules

Use this repository's local XFlow workflow. Do not rely on a global temporary
development checkout as the workflow source.

Hard rules:

- Read this file, `README.md`, `.cursorrules`, and `.xflow/current-task.md`
  when present before acting.
- Use repository-local `devctl` or `devctl.ps1` from the project root.
- Treat `devctl` / `devctl.ps1` as the only supported workflow entrypoints.
  Do not import or call `xflow.providers` directly, and do not call GitHub or
  Gitee APIs outside devctl during normal workflow execution.
- `devctl` may route to `python -m xflow`; shell scripts are compatibility
  fallback, not the preferred implementation layer for remote writes.
- User-level parameters belong in `~/.xflow/env.local`. Legacy
  `~/gitee.env.local` may be read for compatibility. Never print token values.
- Use `XFLOW_PLATFORM=github|gitee` only to select devctl's provider. Do not
  call GitHub or Gitee APIs directly from the AI workflow.
- Maintain `.xflow/current-task.md` for active tasks and run
  `devctl check current-task --issue <id>` before local approval, commit,
  push, PR/MR creation, and cleanup.
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
- Direct `main` maintenance is an exception only for the `xflow-devctl` and
  `xflow-skills` tool repositories when the user explicitly requests it. Do
  not apply that exception to ordinary user projects.

Remote-write checklist:

1. Create the body/evidence file.
2. Run `devctl check current-task --issue <id>`.
3. Run the matching `devctl check ...` command.
4. Run `devctl approval prepare --issue <id> --action <action> --file <file>`.
5. Stop for human review.
6. Continue only after the human sets `Approved: yes`.
7. Run `devctl check local-review --issue <id> --file <file> --action <action>`.
8. Run the approved remote-write command.

After PR/MR creation, use the local `state-update-suggestion.md` only to update
local task state. Do not create another PR only to commit post-merge state
metadata.

Use the user's language for Git-related public text: commit messages, remote
Issue text, remote PR/MR text, review comments, and branch task summaries.
