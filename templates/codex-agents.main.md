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
- Do not put `XFLOW_PLATFORM` in user-level `~/.xflow/env.local` when working
  across both GitHub and Gitee projects. Use project-local
  `.xflow/local/env.local`, explicit `XFLOW_ENV_FILE`, or the process
  environment for platform overrides.
- Use `XFLOW_PLATFORM=github|gitee` only to select devctl's provider. Do not
  call GitHub or Gitee APIs directly from the AI workflow.
- Maintain `.xflow/current-task.md` for active tasks and run
  `devctl check current-task --issue <id>` before local approval, commit,
  push, PR/MR creation, and cleanup.
- Do not perform remote writes before local human review approves the exact
  file being published or used as evidence.
- Human Approval Is Non-Delegable. AI may prepare approval files, evidence,
  command drafts, and review notes. AI must never satisfy a human gate itself.
  AI must never edit `Approved: no` to `Approved: yes`. AI must not
  treat vague replies such as "继续", "都可以", "你看着办", "go ahead", or
  "looks good" as approval unless the user explicitly names the exact action.
  AI must not use `--force`, `--no-local-review`, direct provider APIs, or
  manual approval-file edits to bypass review.
- Active approval file:
  `.xflow/issues/issue-<id>/approvals/local-review.md`.
- For issue creation, use:
  `.xflow/issues/issue-draft/approvals/local-review.md`.
- Do not create alternate active approval files such as `local-review-mr.md`.
- Use `--body-file` for Issue, comment, and PR/MR bodies.
- Run `git status --short --branch` before committing and include only
  task-related files.
- Advisory Dependency Issue Workflow: compare discovered work with the accepted
  main Issue scope. Keep in-scope work on the main feature branch and local
  subtasks as local decomposition. Use `child-feature|shared-infrastructure|external`
  only for independently owned dependencies, retain exact human approval for
  remote dependency Issue creation, treat dependency state as advisory, and
  require fresh parent-side evidence before `integrated`.
- Commit messages must be portable, scoped, Chinese-dominant, multi-line, and
  issue-linked. Use `type(scope): 中文核心摘要[#Issue编号]`; ordinary commits
  use one direct-owner Issue, while explicit integration commits may use the
  parent and dependency Issue IDs. Use Chinese bullet lines for changes,
  acceptance conditions, tests, and evidence. Do not include local absolute
  paths, provider-only metadata, or AI-client signatures.
- Browser Must Not Remain about:blank. When browser or Chrome validation is
  required, identify the exact target URL, navigate to that URL, wait for load,
  and verify the current URL is not `about:blank`. Opening Chrome alone is not
  verification; if navigation fails, diagnose the service, URL, port, auth
  state, or browser-control connection before claiming UI verification.
- Problem/Gap Closure Loop. When the user orally reports a problem or gap,
  create or update `.xflow/issues/issue-draft/gap-analysis.md` or
  `.xflow/issues/issue-<id>/gap-analysis.md`, add evidence, clarify scope and
  acceptance criteria, then stop for human recognition before implementation.
  AI must not skip gap-analysis human approval. After implementation, write
  `.xflow/issues/issue-<id>/resolution-report.md` with evidence and a
  `resolved|reduced|blocked` conclusion. If self-review finds the report is
  not true, AI must rework and rewrite the report before human handoff.
- Evidence must be reviewable, not merely asserted. Read
  `references/evidence-analysis.md`: every gap-analysis finding and completion
  criterion needs its own local evidence bundle under the relevant `evidence/`
  directory, with observation, direct artifact, analysis/result, and a human
  review checkbox. For UI work with browser access, retain both a live
  screenshot and DOM observation. A code diff or "tests passed" statement is
  not completion evidence.
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
   If AI changes `Approved: no` to `Approved: yes`, the approval is invalid.
7. Run `devctl check local-review --issue <id> --file <file> --action <action>`.
8. Run the approved remote-write command.

Push and PR/MR creation are separate gates. Use `devctl git push` only after
`Approved Action: git-push`; use `devctl git mr` only after separate
`Approved Action: git-mr`. After PR/MR creation, devctl may create and push one
metadata-only state backfill commit containing the PR number/URL. Do not create
another PR only to commit post-merge state metadata.

Use the user's language for Git-related public text: commit messages, remote
Issue text, remote PR/MR text, review comments, and branch task summaries.
