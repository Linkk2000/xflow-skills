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

## Next Step
- <requested reviewer action or follow-up>
```

## approvals/local-review.md

`approvals/local-review.md` is the active local approval file. It binds one
approved action to one exact file hash.

```markdown
# Local Review Approval

Issue: <draft|id>
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
