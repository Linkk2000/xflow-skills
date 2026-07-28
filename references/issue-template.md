# XFlow Issue, MR, And Local Review Templates

These templates are for the generic `main` product line. They are not
academic-specific and must not contain academic-only fields.

Remote-published body files are sent to GitHub or Gitee verbatim. Do not
include internal-only visible titles such as `# Issue Draft`, `# MR Draft`,
`# PR Draft`, or `# Merge Request Draft`. Use hidden `xflow` comments for
machine anchors and public-facing Markdown headings for human reviewers.
Do not include internal-only visible titles in files passed to `--body-file`.

## issue-draft.md

Use this shape when converting an oral request into a remote issue. Store the
file at `.xflow/issues/issue-draft/issue-draft.md` before `devctl issue create`.

```markdown
<!-- xflow: issue-draft -->

## Background
<why this task is needed>

## Problem
<current behavior, gap, or pain point>

## Goal
<what should be true when the task is complete>

## Scope
- Includes:
- Excludes:
- Affected paths:

## Acceptance Criteria
- [ ] <machine-checkable or human-reviewable criterion>

## Verification Plan
- <commands or manual checks>

## Attachments
- <none, or published URLs rendered from the approved attachment manifest>
```

Before remote creation, also propose:

- issue kind: `feature`, `fix`, `docs`, `test`, or `chore`
- issue key preview: `feature/<issue-id>-<short-slug>` or `fix/<issue-id>-<short-slug>`
- final branch name after issue creation
- labels as comma-separated values for `devctl issue create --labels`

## mr-draft.md

Use this shape for PR/MR creation. Store the file at
`.xflow/issues/issue-<id>/mr-draft.md` before `devctl git mr`.

```markdown
<!-- xflow: mr-draft -->

Closes #<issue>

## Summary
- <what changed>

## Test Plan
- [x] <failing test or acceptance check first>
- [x] <focused validation command>
- [x] <manual/browser check if applicable>

## Risk
- <remaining risk or "low: ...">

## Review Request
- Please review the implementation, evidence, and local approval record.
```

## comment-draft.md

Use this shape for remote issue comments. Store the file at
`.xflow/issues/issue-<id>/comment-draft.md` before `devctl issue comment`.

```markdown
## Progress
- <what changed or what was found>

## Evidence
- <command, commit, or file reference>
- <optional published attachment URL from the approved attachment manifest>

## Next Step
- <requested reviewer action or follow-up>
```

## .xflow/current-task.md

Use this file as the live state guard for the active task. It should exist
before local approvals, implementation commits, pushes, PR/MR creation, and
cleanup. The state values are defined in `references/workflow-state-machine.md`.

```markdown
# XFlow Current Task

Issue: <draft|id>
State: <S0_REQUEST|S1_LOCAL_ISSUE_DRAFT|...|S10_DONE>
Branch: <branch name or pending>
Base: <main|master|other>

## Allowed Actions
- <what the AI may do in the current state>

## Forbidden Actions
- <what the AI must not do until the next human gate is approved>

## Human Gate
- Reviewer:
- Required Approval:
- Evidence File:

## Notes
<brief local state notes>
```

Run this check before sensitive transitions:

```bash
devctl check current-task --issue <id>
```

After PR/MR creation, devctl writes
`.xflow/issues/issue-<id>/state-update-suggestion.md`, records the PR number
and URL in task state, creates a metadata-only state backfill commit, and
pushes that commit to the same branch under the `git-mr` approval scope. It
must not create a second PR only to record metadata after the original PR has
merged.

## Issue Workspace Evidence

Files under `.xflow/issues/issue-<id>/` and `.xflow/issues/issue-draft/` are
local evidence and approval state. They may reference repository-local evidence
files, but must not contain COS/OSS URLs, object-storage URLs, or non-null
`publishedUrl` values. Store rendered remote bodies and published attachment
manifests under `.xflow/publish/issues/issue-<id>/`.

## gap-analysis.md

Use this shape when the user orally reports a problem or gap. Store it at
`.xflow/issues/issue-draft/gap-analysis.md` before issue creation, or at
`.xflow/issues/issue-<id>/gap-analysis.md` for an existing issue. AI must stop
for human recognition before implementation.

```markdown
# Problem/Gap Analysis

## User Original Statement
<verbatim or faithful summary of the user's oral problem/gap>

## Clarified Problem Or Gap
<the clarified problem, discrepancy, missing behavior, or workflow gap>

## Gap Analysis
- <what is missing or wrong>
- <why this matters>

## Evidence
- [local evidence](evidence/<small-file-or-log>)

## Evidence-Backed Findings

### Finding F-001: <short observable discrepancy>

#### Finding Type
ui|non-ui

#### Observation
<what was directly observed and how it was reproduced>

#### User Impact
<why this discrepancy matters>

#### Evidence
- [direct local artifact](evidence/<screenshots|dom|logs|fixtures>/<file>)

#### Analysis
<proven cause, supported hypothesis, or explicit unknown>

#### Proposed Change
<smallest change that addresses the finding>

#### Acceptance
- [ ] <observable acceptance condition>

#### Human Review
- [ ] Confirm the observation, evidence, and proposed change.

## Scope Boundaries
- Includes:
- Excludes:

## Proposed Modification Plan
- [ ] <planned change>

## Acceptance Criteria
- [ ] <machine-checkable or human-reviewable criterion>

## Human Recognition
Recognized: no
Reviewer:
Notes:
```

AI may prepare this file, collect evidence, and ask clarifying questions. AI
must not treat the analysis as approved until the human explicitly recognizes
the gap and intended direction. Read `evidence-analysis.md`: every finding
needs a direct evidence bundle. For `ui`, include both a live screenshot under
`evidence/screenshots/` and a DOM observation under `evidence/dom/` when a
browser is available.

## resolution-report.md

Use this shape after implementation. Store it at
`.xflow/issues/issue-<id>/resolution-report.md`. It explains whether the
problem was solved or the gap was reduced, with evidence.

```markdown
# Resolution Report

## Source Problem Or Gap
- gap-analysis.md

## Actual Changes
- <what changed>

## Evidence Index
- [local evidence](evidence/<small-file-or-log>)

## Completion Verification

### Criterion C-001: <acceptance criterion being verified>

#### Verification Type
ui|non-ui

#### Expected Result
<the observable result that would satisfy the criterion>

#### Evidence
- [fresh post-change artifact](evidence/<screenshots|dom|logs|fixtures>/<file>)

#### Actual Result
<what the linked evidence shows>

#### Human Review
- [ ] Confirm the evidence supports this result.

## Closure Conclusion
resolved|reduced|blocked: <reason>

## AI Self-Review Result
- [x] <criterion satisfied>

## Remaining Risks
- <none, or remaining risk>

## Human Review Request
- Please review the report, evidence, and conclusion.
```

Allowed conclusions are exactly `resolved|reduced|blocked`. For `resolved` and
`reduced`, every AI self-review item must be checked. If self-review finds the
report is not true, AI must rework and rewrite the report before handoff. If AI
cannot continue, use `blocked` and state the human decision or external
condition needed.

Read `evidence-analysis.md` before declaring `resolved` or `reduced`. Each
completion criterion needs fresh, local, reviewer-readable evidence; a code
diff or the AI's own test claim is not enough.

## dependencies.yaml

This optional issue-level artifact records independently owned dependency
Issues or external dependencies. Start from `templates/dependencies.yaml` and
validate it with `devctl check dependencies --issue <id>`. It is separate from
the optional `subtask-001/` local decomposition below: a local subtask does not
create a remote Issue or branch.

Parent closure examples:

```yaml
# Dependency does not affect the accepted completion criteria.
closureAssessment:
  affectsClosure: false
  decision: continue
  rationale: 未覆盖当前 Issue 的验收条件，后续独立交付。

# Parent consumed the dependency and gathered fresh integration evidence.
closureAssessment:
  affectsClosure: true
  decision: integrated
  rationale: 已在主功能分支完成联合验证。

# An approved design decision removed the dependency.
closureAssessment:
  affectsClosure: true
  decision: superseded
  rationale: 经人工审核的设计调整已移除该依赖。
```

Dependency delivery evidence establishes `available`, not `integrated`.
`integrated` requires fresh evidence from the parent branch after consumption.

## subtask-001/README.md

Use this shape when a large issue needs local subtasks. Store each subtask
under `.xflow/issues/issue-<id>/subtask-001/`, `subtask-002/`, and so on.
This is local repository evidence only; it does not create GitHub/Gitee
sub-issues.

```markdown
# Subtask <001>

## Source
- <issue directory file such as walkthrough.md, mr-draft.md, comment-draft.md>

## Purpose
<why this subtask exists>

## Implementation Plan
- [ ] <planned local step>

## Evidence
- [local evidence](evidence/<small-file-or-image>)

## AI Review Checkpoints
- [ ] <AI self-check before handoff>

## Human Review Checkpoints
- [ ] <human review point>

## Conclusion
<success|blocked|superseded-by-human>: <reason and final state>
```

Run:

```bash
devctl check subtask --issue <id> --path .xflow/issues/issue-<id>/subtask-001
```

Subtask evidence belongs under `subtask-001/evidence/` and must stay in the
repository, not in COS/OSS or any object storage backend.

## approvals/local-review.md

`approvals/local-review.md` is the active local approval file. It binds one
approved action to one exact file hash.

Prefer generating it with `devctl approval prepare`. The tool should prefill
mechanical fields such as `Approved At`, `Approved File`, `Approved SHA256`,
`Reviewer`, and the suggested command. By default, `Reviewer` comes from
`git config user.name` and `git config user.email` when available; pass
`--reviewer` to override it. The human reviewer should inspect the referenced
artifact and then change `Approved: no` to `Approved: yes`.
AI may prepare this file but must never make that approval edit. If AI changes
`Approved: no` to `Approved: yes`, the approval is invalid.

```markdown
# Local Review Approval

Issue: <draft|id>
Reviewer: <human reviewer>
Approved At: <ISO-8601 time>
Approved Action: <issue-create|issue-comment|issue-close|git-mr|remote-write>
Approved File: <path>
Approved SHA256: <sha256>
Attachment Manifest: <none|path>
Attachment Manifest SHA256: <none|sha256>

## Decision
Approved: no

## Human Gate
Prepared by AI or tooling does not mean approved.
Only the human reviewer may change Approved: no to Approved: yes.
If this file was approved by the AI, the approval is invalid.

## Notes
<review notes and constraints>
```

## Label Hints

Use comma-separated labels for `devctl issue create --labels`.

- `frontend`
- `backend`
- `api`
- `runtime`
- `bug`
- `enhancement`
- `tdd`
- `test`
- `docs`
- `chore`

## Clarifying Questions

Ask only when the issue would otherwise be unsafe or unclear:

- Is this a bug fix or a new capability?
- What is the smallest useful scope?
- Which module or repository owns the change?
- What verification evidence should reviewers expect?
