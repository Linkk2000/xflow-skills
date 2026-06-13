# Academic Schema Contract

This contract links `xflow-skills@academic` and `xflow-devctl@academic`.

## Current Version

- Academic schema: `academic-xflow/v1`
- Required devctl checks:
  - `devctl check academic-issue`
  - `devctl check tdd-result`
  - `devctl check claude-package`
  - `devctl check academic-mr`
  - `devctl check local-review`
  - `devctl check submodule-hygiene`

## Runtime Contract

- Required runtime: Python 3.10 or newer.
- Initial dependency policy: Python standard library only.
- Missing Python behavior: fail closed and provide a reviewable installation
  recommendation.
- Python bytecode policy: launchers must set `PYTHONDONTWRITEBYTECODE=1` before
  invoking the Python core.
- Pre-Issue draft location: `.xflow/issues/issue-draft/`.
- Workflow-local scratch location: `.xflow/local/`.
- Tool submodule locations: `.xflow/ops/devctl` and `.xflow/ops/workflow`.
- Task artifact location: `.xflow/issues/issue-<id>/`.

## Branch Semantics Contract

`academic` identifies the XFlow product line for the tool repositories. It must
not be used as the default paper repository branch by template convention.

Academic issue and MR templates must include hidden machine anchors:

- `<!-- workflow-product-line: academic -->`
- `<!-- paper-base-branch:`
- `<!-- task-branch:`

`Target Branch: academic` is invalid because it conflates the tool product line
with the paper repository's base or task branch. `xflow-devctl@academic` must
reject that obsolete field in academic issue and MR checks.

## Cursor Compatibility Contract

Codex is not a runtime dependency. Cursor or another upper AI may operate the
academic workflow when it can access:

- `xflow-devctl@academic`
- `xflow-skills@academic`
- the user's paper repository

The upper AI must use repository-local files and `devctl` commands as the
source of truth. It must not require Codex skill installation.

Cursor initialization must copy:

```text
.xflow/ops/workflow/templates/cursorrules.academic -> .cursorrules
```

The `.cursorrules` file is a Cursor guardrail, not a replacement for executable
`devctl` checks.

## Pinned Update Contract

Already-initialized paper repositories must update Academic XFlow by pinned
submodule commits, not by silently following latest remote branch heads.

The required update chain is:

```text
fetch -> pin reviewed SHA -> test -> human review -> commit
```

The parent paper repository update is valid only when:

- `.xflow/ops/devctl` points to a human-reviewed `xflow-devctl@academic` commit.
- `.xflow/ops/workflow` points to a human-reviewed `xflow-skills@academic` commit.
- `.gitmodules` uses `ignore = untracked` for `.xflow/ops/devctl` and
  `.xflow/ops/workflow`.
- copied guardrails such as `SKILL.md` and `.cursorrules` are synced from the
  reviewed `.xflow/ops/workflow` commit.
- local checks have been run and recorded in the task's TDD result or update
  review record.
- the human reviewer approves the exact submodule pointer changes and copied
  guardrail changes before any remote paper-repository push.

AI assistants must not run silent update commands such as automatic submodule
tracking, recursive checkout to an unreviewed HEAD, or installer-like update
steps without a local human review gate.

## Submodule Hygiene Contract

Tool submodules are read-only from the parent paper repository. Generated
artifacts must not be written under `.xflow/ops/devctl` or `.xflow/ops/workflow`.

`devctl check submodule-hygiene` is responsible for checking that:

- `.xflow/ops/devctl` and `.xflow/ops/workflow` do not contain tracked modifications.
- common byproducts such as `__pycache__/`, `*.pyc`, `.pytest_cache/`, `*.tmp`,
  and `*.log` are absent from tool submodules.
- `.gitmodules` sets `ignore = untracked` for `.xflow/ops/devctl` and
  `.xflow/ops/workflow`.

The parent repository may intentionally commit submodule pointer changes after
human review, but it must not hide tracked tool modifications with
`ignore = all`.

## PowerShell Native Command Contract

A native Git command is failed only when its process exit code is non-zero.
AI assistants must not classify Git stderr text alone as a failure.

On Windows PowerShell:

- the PowerShell helper template must be copied from
  `templates/xflow-powershell-native.ps1` to
  `.xflow/tools/xflow-powershell-native.ps1` during initialization;
- reusable scripts should dot-source the PowerShell helper template and use
  `Invoke-XFlowNative` or `Invoke-XFlowGit`;
- native command composition must be explicit: run one native command, store
  its result object or exit code, inspect it, and only then run the next native
  command;
- do not pipe native Git commands through `2>&1 | Out-String`;
- invoke Git directly and inspect `$LASTEXITCODE`;
- when output capture is needed, write to a temporary log file and inspect
  `$LASTEXITCODE` immediately after the native command;
- verify Git side effects with `git status --short`, `git submodule status`,
  `Test-Path .\.gitmodules`, and the expected `.xflow/ops/*` paths.

## Claude Delegation Contract

Claude delegation is exposed through:

```bash
devctl claude run --issue <id> [--file F] [--output F] [--dry-run]
```

The command must validate the Claude task package before execution, use the
local Claude CLI, write the result to a repository-local output file, and leave
remote-write approval gates unchanged.

Claude readiness is exposed through:

```bash
devctl claude doctor
```

If AcademicForge is missing, `doctor` must report the recommended registration
command and perform no installation. Any global Claude configuration write
requires explicit human approval.

## Body File Contract

Remote-write commands that accept Markdown bodies must support file-based body
input. Use inline `--body` only for short single-line plain text. Multi-line
Markdown, fenced code, inline backticks, JSON, shell snippets, or text
containing `$()` must be written to a file and passed with `--body-file`.

Remote-published body files must be publish-ready Markdown. `issue-draft.md`
must include `<!-- xflow: academic-issue-draft -->`; `mr-draft.md` must include
`<!-- xflow: academic-mr-draft -->`. Internal-only visible headings such as
`# Academic Issue Draft` and `# MR Draft` are invalid in remote-published
bodies because they appear on GitHub Issue or PR pages.

## Compatibility Rule

Any change to required template headings must update:

1. `references/academic-templates.md`
2. `references/academic-workflow.md`
3. `xflow-devctl@academic` template checks
4. tests covering those checks

Rules and executable checks must not drift. If the skill requires a field that
devctl does not check, the field is advisory only. If devctl checks a field not
documented here, the check is invalid and must be fixed.

## Remote Write Rule

Remote writes require local review evidence. At minimum, the relevant reviewed
file must have a matching approval record with `Approved SHA256`.

Remote writes include:

- remote issue creation
- branch push
- issue comments
- MR/PR creation
- issue close
- branch cleanup when tied to a closed remote task

The active approval file is always
`.xflow/issues/issue-<id>/approvals/local-review.md`. AI clients must not
invent alternate active approval filenames. Superseded approvals may be
preserved under `.xflow/issues/issue-<id>/approvals/history/`, but history files
are audit records and do not satisfy the active remote-write gate by
themselves.

## GitHub Issue And PR Provider Contract

`devctl issue create` in academic Python mode must:

- require `--body-file`;
- validate the local review approval before any network request;
- read `GITHUB_TOKEN` or one of its supported aliases;
- resolve the repository from `DEVCTL_OWNER`/`DEVCTL_REPO` or `origin`;
- create the GitHub Issue with the reviewed body file and comma-separated
  labels;
- print the remote Issue number and URL returned by GitHub.

`devctl issue list` and `devctl issue show` in academic Python mode must:

- read `GITHUB_TOKEN` or one of its supported aliases;
- resolve the repository from `DEVCTL_OWNER`/`DEVCTL_REPO` or `origin`;
- perform read-only GitHub API requests;
- require no local approval gate because they do not write remote state.

`devctl issue comment` in academic Python mode must:

- reject inline `--body`;
- use `--body-file` or `.xflow/issues/issue-<id>/comment-draft.md`;
- validate `Approved Action: issue-comment` before any network request;
- post the reviewed body as a GitHub Issue comment;
- print the remote comment URL when GitHub returns one.

`devctl issue close` in academic Python mode must:

- validate `Approved Action: issue-close` against
  `.xflow/issues/issue-<id>/walkthrough.md` unless
  `DEVCTL_ACADEMIC_APPROVED_FILE` is set;
- close the GitHub Issue only after the approval gate passes;
- print the remote Issue number and URL returned by GitHub.

If `XFLOW_PLATFORM=gitee`, the Python academic provider must fail closed until
Gitee is explicitly ported.

`devctl git mr` in academic Python mode must:

- reject inline `--body`;
- use `--body-file` or `.xflow/issues/issue-<id>/mr-draft.md`;
- validate the local review approval before push or network request;
- push the current task branch unless `DEVCTL_SKIP_PUSH=1`;
- create the GitHub PR with the reviewed body file, current branch as `head`,
  and requested or detected paper base branch as `base`;
- write the returned PR number to local git config `devctl.pr`;
- print the remote PR number and URL returned by GitHub.

`Approved Action: git-mr` covers the PR publication sequence: branch push, PR
creation, PR number/URL metadata writeback, and one metadata-only follow-up
push to the same task branch before remote review starts. The PR/MR number/URL
metadata writeback must not require a second approval. After the PR is merged,
the task is sealed; optional manual Issue close is a separate `issue-close` remote write
and must not require another PR just to update local task-board records.

`devctl git pr-get` in academic Python mode must:

- read a GitHub PR by number;
- perform no remote write;
- require no local approval gate.

## Approved Action Values

`Approved Action` is machine-checked by `xflow-devctl@academic`. Use one of:

- `issue-create`: allow remote issue creation.
- `issue-comment`: allow a remote issue comment.
- `issue-close`: allow remote issue close.
- `git-mr`: allow branch push performed by `devctl git mr` and MR/PR creation.
- `remote-write`: broad approval for remote writes tied to the reviewed file.

Prefer specific actions. `remote-write` should be used only when the reviewed
artifact intentionally authorizes more than one remote write.
