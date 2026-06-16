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
  - `devctl check scope --issue <id> --mode review-only`
  - `devctl check current-task --issue <id>`
  - `devctl approval prepare --issue <id> --action <action> --file <artifact>`
  - `devctl check submodule-hygiene`

## Runtime Contract

- Required runtime: Python 3.10 or newer.
- Initial dependency policy: Python standard library only.
- Missing Python behavior: fail closed and provide a reviewable installation
  recommendation.
- Python bytecode policy: launchers must set `PYTHONDONTWRITEBYTECODE=1` before
  invoking the Python core.
- Windows academic operation must not require WSL. PowerShell plus Python
  devctl is the default Windows execution surface; WSL is a developer
  compatibility path for tool-repository tests and legacy Bash fallback.
- devctl wrapper, helper, and fallback status/error lines should use ASCII.
  Non-ASCII academic content belongs in UTF-8 artifact files.
- Pre-Issue draft location: `.xflow/issues/issue-draft/`.
- Workflow-local scratch location: `.xflow/local/`.
- Tool submodule locations: `.xflow/ops/devctl` and `.xflow/ops/workflow`.
- Task artifact location: `.xflow/issues/issue-<id>/`.
- Scope policy extension location: `.xflow/scope-policy.json`.
- Active task-state board: `.xflow/current-task.md`.

## Scope Check Contract

`devctl check scope --issue <id> --mode review-only` must validate changed
files against an allowlist. The issue id is a variable expanded from the command
argument; templates must not hard-code example issue numbers.

Default `review-only` allowlist:

- `.xflow/issues/issue-<id>/**`
- `.xflow/local/**`
- `reviews/issue-<id>/**`
- `review/issue-<id>/**`

Default supporting allowlist:

- `.xflow/scope-policy.json`
- `AGENTS.md`
- `.cursorrules`
- `.cursor/rules/**`

The project may extend the allowlist through `.xflow/scope-policy.json` using
the `review_only` key. Supported fields are `allow`, `allow_supporting`, and
`protected_hints`; each value must be a list of glob patterns. The `<id>` token
must be expanded to the active issue id before matching.

Protected hints such as `manuscript/**`, `paper/**`, `*.tex`, and `*.bib` must
not be the primary enforcement model. They only improve error messages when a
changed file is outside the allowlist and appears to be manuscript content.

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

## AI Rule Entrypoint Contract

Codex is not a runtime dependency. Cursor or another upper AI may operate the
academic workflow when it can access:

- `xflow-devctl@academic`
- `xflow-skills@academic`
- the user's paper repository

The upper AI must use repository-local files and `devctl` commands as the
source of truth. It must not require Codex skill installation.

AI-client rule files are declared by:

```text
.xflow/ops/workflow/templates/ai-rules.json
```

At minimum, the manifest must expose these entrypoints:

```text
codex -> AGENTS.md
cursor -> .cursorrules
```

`devctl rules list` must read that manifest, and `devctl rules sync <id>` must
copy the requested template into the paper repository root. This allows a
repository initialized by one AI tool to add another AI tool's rule file later.

`devctl rules sync` must not overwrite an existing different file unless
`--force` is supplied after local human review. These root rule files are
guardrails, not replacements for executable `devctl` checks.

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
- copied guardrails such as `SKILL.md`, `AGENTS.md`, and `.cursorrules` are
  synced from the reviewed `.xflow/ops/workflow` commit.
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

The Claude task package must include these fields:

- `Claude Skill:`
- `Skill Source:`
- `Invocation:`

When `Skill Source:` is `AcademicForge`, `Invocation:` must name a command from
`references/academicforge-skill-catalog.md`. `xflow-devctl@academic` must reject
unknown commands such as `/paper-review` and must reject the obsolete
`AcademicForge Skill:` field.

The `Invocation:` line may include skill arguments after the verified command.
`xflow-devctl@academic` must preserve the complete invocation line in the
Claude prompt while validating only the leading command name against the
catalog. Claude CLI arguments belong in `DEVCTL_CLAUDE_ARGS`, not in the skill
command field.

Before invoking Claude for an AcademicForge task, `xflow-devctl@academic` must
verify that the exact requested command is installed in a Claude-resolvable flat
skill path such as `.claude/skills/peer-review/SKILL.md`. Passing catalog
validation alone is not enough to execute, and an official nested source clone
under `.claude/skills/academic-forge/skills/...` is not sufficient by itself.

`devctl claude skills` must list the verified AcademicForge command catalog so
upper AIs can query available commands before writing `claude-task.md`.

Claude output must be validated before writing `claude-result.md`. A zero exit
code from the Claude CLI is insufficient by itself. `xflow-devctl@academic` must
reject empty output, `Unknown command` output, and obvious generic replies that
ask for the task again. It must not hard-code one academic output format because
individual Forge skills may return their own valid structures.

Claude readiness is exposed through:

```bash
devctl claude doctor
```

If no AcademicForge-derived skill is available in a Claude-resolvable flat path,
`doctor` must report checked skill roots such as `.claude/skills` and perform no
installation.
Any Claude skill installation or global configuration write requires explicit
human approval.

## Body File Contract

Remote-write commands that accept Markdown bodies must support file-based body
input. Use inline `--body` only for short single-line plain text. Multi-line
Markdown, fenced code, inline backticks, JSON, shell snippets, or text
containing `$()` must be written to a file and passed with `--body-file`.

Remote-published body files must be publish-ready Markdown. `issue-draft.md`
must include `<!-- xflow: academic-issue-draft -->`; `mr-draft.md` must include
`<!-- xflow: academic-mr-draft -->`. Internal-only visible headings such as
`# Academic Issue Draft`, `# Issue Draft`, `# MR Draft`, and `# PR Draft` are
invalid in remote-published bodies because they appear on GitHub Issue or PR
pages.

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

`devctl approval prepare` must prefill the active approval file with:

- issue id;
- reviewer placeholder;
- current timestamp;
- approved action;
- approved file;
- lowercase SHA256 of the approved file;
- suggested command when provided or inferable.

The generated approval file must keep `Approved: no`. AI clients may update
mechanical fields by rerunning `devctl approval prepare`, but must not set
`Approved: yes` or forge reviewer identity. `devctl check local-review` and
remote-write gates must reject unresolved placeholders, accept upper- or
lowercase SHA256 text, and compare the hash against the exact reviewed file.

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
- write the returned PR URL to local git config `devctl.pr-url` when GitHub
  returns one;
- write `.xflow/issues/issue-<id>/state-update-suggestion.md` with the PR
  number, optional URL, and suggested `State: S9_REMOTE_REVIEW_AND_CI`;
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

`devctl check current-task --issue <id>` must:

- read `.xflow/current-task.md`;
- require a `State:` field;
- verify the optional `Issue:` field matches the requested issue id;
- fail when local PR metadata such as git config `devctl.pr` exists but the
  current task board still describes a pre-PR state or contains forbidden
  push/PR/MR actions;
- point the AI to `.xflow/issues/issue-<id>/state-update-suggestion.md` when a
  stale board is detected.

## Approved Action Values

`Approved Action` is machine-checked by `xflow-devctl@academic`. Use one of:

- `issue-create`: allow remote issue creation.
- `issue-comment`: allow a remote issue comment.
- `issue-close`: allow remote issue close.
- `git-mr`: allow branch push performed by `devctl git mr` and MR/PR creation.
- `remote-write`: broad approval for remote writes tied to the reviewed file.

Prefer specific actions. `remote-write` should be used only when the reviewed
artifact intentionally authorizes more than one remote write.
