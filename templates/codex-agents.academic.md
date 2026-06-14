# Academic XFlow Codex Instructions

You are operating an Academic XFlow paper repository.

Read these files before acting:

- `SKILL.md`
- `.xflow/ops/workflow/references/academic-workflow.md`
- `.xflow/ops/workflow/references/academic-templates.md`
- `.xflow/ops/workflow/references/academic-schema-contract.md`
- `.xflow/ops/workflow/references/academicforge-skill-catalog.md`
- `.xflow/ops/workflow/references/ops-lessons.md`
- `README.md` when present

Runtime rules:

- Use repository-local `devctl` or `devctl.ps1` from the paper repository root.
- Default to PowerShell plus Python devctl on Windows. Do not switch to WSL
  unless the human reviewer explicitly requests it or the task is a
  tool-repository compatibility test that cannot run through PowerShell.
- Treat WSL as a developer compatibility path, not as a normal academic user
  prerequisite.
- Treat `.xflow/ops/devctl` and `.xflow/ops/workflow` as reviewed tool
  submodules. Do not write logs, caches, Claude outputs, or review artifacts
  inside `.xflow/ops/*`.
- Treat `academic` as the XFlow tool product line only. Do not create or push
  an `academic` branch in the paper repository unless the human reviewer
  explicitly approves that repository policy.
- Remote writes require local human review of the exact artifact and command.
  This includes Issue creation, Issue comments, Issue close, branch push, and
  MR/PR creation.
- Use `.xflow/issues/issue-<id>/approvals/local-review.md` as the active
  approval file. Do not invent active approval filenames such as
  `local-review-mr.md`.
- TDD output is required, but it never replaces human judgement.
- Git-facing text only: commit messages, remote Issue titles/bodies, and MR/PR
  titles/bodies should follow the user's language; when the user works in
  Chinese, use Chinese as the primary language.
- Do not add AI-client co-author trailers. Do not append
  `Co-authored-by: Cursor <cursoragent@cursor.com>` or use
  `git commit --trailer` for Cursor, cursoragent, or AI-client metadata.
- Use body files for long or shell-sensitive Issue, comment, and MR/PR content.
  Do not pass multiline Markdown, fenced code, inline backticks, JSON, shell
  snippets, or text containing `$()` through inline `--body`.
- Avoid complex PowerShell command composition. Run one native Git command,
  inspect its exit code, then run the next command.
- Keep terminal status lines ASCII. Write Chinese, long Markdown, Issue/MR
  bodies, Claude results, and review details to UTF-8 files.
- Before Claude delegation, run `devctl claude doctor`, choose verified
  commands with `devctl claude skills`, write `claude-task.md`, and execute
  through `devctl claude run --issue <id>`. Do not ask the user to manually
  copy prompts into Claude during normal workflow execution.
- To add another AI client's rule entrypoint after initialization, run
  `devctl rules list` and then `devctl rules sync <id>` after reviewing the
  target file that will be created or overwritten.
