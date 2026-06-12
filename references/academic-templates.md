# Academic XFlow Templates

These templates are the canonical local artifacts for `academic` product-line
tasks. Keep headings stable because `devctl check` validates them.

## issue-draft.md

```markdown
# Academic Issue Draft

Task Type: <translation|polish|review|survey|submission|tooling>
Target Branch: academic
Target Artifacts:
- <paper.md or tool path>

## Background
<why this academic task is needed>

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

## Claude Delegation
- Required: <yes|no>
- AcademicForge Skill:
- Input files:
- Output files:

## Human Review Gate
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

## claude-task.md

```markdown
# Claude Task Package

Issue: <id>
AcademicForge Skill: <skill name and version/source>
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
- Summary:
- Proposed changes:
- Risks:
- Questions:

## Human Review Requirement
Claude output must be reviewed by the human reviewer before use.
```

## claude-result.md

```markdown
# Claude Result

Issue: <id>
AcademicForge Skill: <skill name and version/source>
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
# MR Draft

Issue: <id>
Target Branch: academic

## Summary
- <change summary>

## Evidence
- TDD Result: .xflow/issue-<id>/tdd-result.md
- Claude Result: .xflow/issue-<id>/claude-result.md
- Local Review: .xflow/issue-<id>/approvals/local-review.md

## Verification
- <commands run>

## Remote Actions Requested
- push current branch
- create MR
```

## approvals/local-review.md

```markdown
# Local Review Approval

Issue: <id>
Reviewer: <human reviewer>
Approved At: <ISO-8601 time>
Approved Action: <issue-create|issue-comment|issue-close|git-mr|remote-write>
Approved File: <path>
Approved SHA256: <sha256>

## Decision
Approved: yes

## Notes
<review notes and constraints>
```
