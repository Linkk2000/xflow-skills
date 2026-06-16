# Academic XFlow Templates

These templates are the canonical local artifacts for `academic` product-line
tasks. Keep headings and hidden anchors stable because `devctl check` validates
them.

Remote-published body files such as `issue-draft.md` and `mr-draft.md` must be
ready to publish as GitHub Issue or PR bodies. Do not include internal-only
visible titles such as `Academic Issue Draft` or `MR Draft`; use hidden
`xflow` comments for machine-readable anchors instead.

## issue-draft.md

```markdown
<!-- xflow: academic-issue-draft -->
<!-- task-type: <translation|polish|review|survey|submission|tooling> -->
<!-- workflow-product-line: academic -->
<!-- paper-base-branch: <main|master|user-defined> -->
<!-- task-branch: <feature/<issue>-<slug>|review/<issue>-<slug>|chore/update-academic-xflow-<date>> -->

## Background 🧩
<why this academic task is needed>

## Goal 🎯
<what should be true when the task is complete>

## Scope 📌
- Includes:
- Excludes:
- Affected paths:

## Target Artifacts 📁
- <paper.md or tool path>

## Acceptance Criteria ✅
- [ ] <machine-checkable or human-reviewable criterion>

## Verification Plan 🧪
- <commands or manual checks>

## Claude Delegation 🤖
- Required: <yes|no>
- Claude Skill: <verified command name, for example peer-review>
- Skill Source: <AcademicForge|local|other>
- Invocation: /<verified command name>
- Input files:
- Output files:

## Human Review Gate 🧑‍⚖️
- Reviewer:
- Review focus:
- Remote action allowed after approval: <issue-create|issue-comment|issue-close|git-mr|remote-write|none>
```

## tdd-result.md

```markdown
# TDD Result

Issue: <id>
Branch: <branch>
Verified At: <ISO-8601 time>
Executor: <agent or person>

## Verification Scope
- Includes:
- Excludes:

## Commands
- <command>

## Results
- Passed:
- Failed:
- Skipped:

## Risks
- <remaining risk or "none">

## Human Review Entry
- Basic target reached: <yes|no>
- Ready for local review: <yes|no>
```

## .xflow/current-task.md

`.xflow/current-task.md` is the active local state board. Keep it short and
machine-checkable. Run `devctl check current-task --issue <id>` before local
approval, commit, push, or MR/PR creation.

```markdown
# Current Task

Issue: <id>
State: <S0_REQUEST|S1_LOCAL_ISSUE_DRAFT|G1_LOCAL_APPROVE_ISSUE|S2_CREATE_REMOTE_ISSUE|G2_APPROVE_DEVELOPMENT|S3_START_TASK_BRANCH|S4_EXECUTE_AI_OR_CLAUDE_TASK|S5_WRITE_TDD_RESULT|G3_LOCAL_REVIEW_RESULT|S6_PREPARE_COMMIT_AND_MR_DRAFT|G4_LOCAL_APPROVE_REMOTE_WRITE|S7_PUSH_BRANCH|G5_LOCAL_APPROVE_MR|S8_CREATE_REMOTE_MR|S9_REMOTE_REVIEW_AND_CI|G6_APPROVE_CLEANUP|S10_CLOSE_AND_ARCHIVE>
Branch: <branch>
PR: <number-or-empty>

## Allowed Actions
- <next allowed local action>

## Forbidden Actions
- <remote write or content write that is not currently approved>

## Evidence
- TDD Result: .xflow/issues/issue-<id>/tdd-result.md
- Local Review: .xflow/issues/issue-<id>/approvals/local-review.md
- State Update Suggestion: .xflow/issues/issue-<id>/state-update-suggestion.md
```

## claude-task.md

```markdown
# Claude Task Package

Issue: <id>
Claude Skill: <verified command name from academicforge-skill-catalog.md>
Skill Source: AcademicForge
Invocation: /<verified command name> [optional skill arguments]
Input Files:
- <path and hash>
Output File: <path>

## Objective
<specific task for Claude>

## Constraints
- Do not overwrite final documents.
- Return reviewable output only.
- Preserve citations and terminology unless instructed otherwise.

## Required Output Format
Return Markdown with these exact section headings:

## Summary

## Proposed Changes

## Risks

## Questions

## Human Review Requirement
Claude output must be reviewed by the human reviewer before use.
```

## claude-result.md

```markdown
# Claude Result

Issue: <id>
Claude Skill: <verified command name>
Skill Source: AcademicForge
Invocation: /<verified command name>
Executed At: <ISO-8601 time>
Input Hashes:
- <path>: <sha256>
Output Hash: <sha256>
Retry Count: <number>

## Summary
<what Claude produced>

## Proposed Changes
<reviewable changes or references to output files>

## Risks
<academic, citation, translation, or prompt-injection risks>

## Questions
<items requiring human decision>
```

## mr-draft.md

```markdown
<!-- xflow: academic-mr-draft -->
<!-- issue: <id> -->
<!-- workflow-product-line: academic -->
<!-- paper-base-branch: <main|master|user-defined> -->
<!-- task-branch: <feature/<issue>-<slug>|review/<issue>-<slug>|chore/update-academic-xflow-<date>> -->

Closes #<id>

## Summary 🧭
- <change summary>

## Evidence 🔎
- TDD Result: .xflow/issues/issue-<id>/tdd-result.md
- Claude Result: .xflow/issues/issue-<id>/claude-result.md
- Local Review: .xflow/issues/issue-<id>/approvals/local-review.md

## Verification ✅
- <commands run>

## Risks ⚠️
- <remaining risk or "none">

## Review Request 🚀
- Please review scope, evidence, verification result, and local approval record.
```

## approvals/local-review.md

`approvals/local-review.md` is the active approval file. Do not create alternate
active approval names such as `local-review-mr.md`. Archive superseded approval
records under `approvals/history/`. Generate or refresh this file with
`devctl approval prepare --issue <id> --action <action> --file <artifact>`.
The AI may prefill mechanical fields, but only the human reviewer may change
`Approved: no` to `Approved: yes`.

```markdown
# Local Review Approval

Issue: <id>
Reviewer: <human reviewer>
Approved At: <ISO-8601 time>
Approved Action: <issue-create|issue-comment|issue-close|git-mr|remote-write>
Approved File: <path>
Approved SHA256: <lowercase sha256>

## Decision
Approved: no

## Suggested Command
Suggested Command: <exact remote-write command>

## Expected Effect
- Authorizes exactly one remote write after the human changes `Approved: no` to `Approved: yes`.
- If the approved file changes, rerun `devctl approval prepare` before any remote write.

## Notes
- Human reviewer must inspect the approved file, the action, and the suggested command before approving.
```
