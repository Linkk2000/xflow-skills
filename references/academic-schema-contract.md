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
- Pre-Issue draft location: `.xflow/issue-draft/`.

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
_ops/workflow/templates/cursorrules.academic -> .cursorrules
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

- `_ops/devctl` points to a human-reviewed `xflow-devctl@academic` commit.
- `_ops/workflow` points to a human-reviewed `xflow-skills@academic` commit.
- `.gitmodules` uses `ignore = untracked` for `_ops/devctl` and
  `_ops/workflow`.
- copied guardrails such as `SKILL.md` and `.cursorrules` are synced from the
  reviewed `_ops/workflow` commit.
- local checks have been run and recorded in the task's TDD result or update
  review record.
- the human reviewer approves the exact submodule pointer changes and copied
  guardrail changes before any remote paper-repository push.

AI assistants must not run silent update commands such as automatic submodule
tracking, recursive checkout to an unreviewed HEAD, or installer-like update
steps without a local human review gate.

## Submodule Hygiene Contract

Tool submodules are read-only from the parent paper repository. Generated
artifacts must not be written under `_ops/devctl` or `_ops/workflow`.

`devctl check submodule-hygiene` is responsible for checking that:

- `_ops/devctl` and `_ops/workflow` do not contain tracked modifications.
- common byproducts such as `__pycache__/`, `*.pyc`, `.pytest_cache/`, `*.tmp`,
  and `*.log` are absent from tool submodules.
- `.gitmodules` sets `ignore = untracked` for `_ops/devctl` and
  `_ops/workflow`.

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
  `Test-Path .\.gitmodules`, and the expected `_ops/*` paths.

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

## Approved Action Values

`Approved Action` is machine-checked by `xflow-devctl@academic`. Use one of:

- `issue-create`: allow remote issue creation.
- `issue-comment`: allow a remote issue comment.
- `issue-close`: allow remote issue close.
- `git-mr`: allow branch push performed by `devctl git mr` and MR/PR creation.
- `remote-write`: broad approval for remote writes tied to the reviewed file.

Prefer specific actions. `remote-write` should be used only when the reviewed
artifact intentionally authorizes more than one remote write.
