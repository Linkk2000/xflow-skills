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

## Claude Delegation Contract

Claude delegation is exposed through:

```bash
devctl claude run --issue <id> [--file F] [--output F] [--dry-run]
```

The command must validate the Claude task package before execution, use the
local Claude CLI, write the result to a repository-local output file, and leave
remote-write approval gates unchanged.

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
