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
