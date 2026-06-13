# Academic XFlow Workflow

This file defines the Academic XFlow product line for the `academic` branch.
The `main` branch remains the general code-development workflow. The
`academic` branch is a long-lived product branch for academic research,
paper writing, translation, polishing, review, submission, and academic
skill orchestration.

## Core Principle

Academic XFlow uses two review layers:

1. Local human review confirms that the AI or Claude result is useful,
   directionally correct, and worth publishing to the remote platform.
2. Remote MR/PR review provides formal audit, CI, reviewer discussion,
   and merge protection.

TDD or verification output never replaces human judgement. It only proves
that the basic, machine-checkable target has been reached.

## Python Runtime Preflight

Academic devctl uses a Python 3.10+ core for UTF-8, path, template, and approval
gate handling. Before remote writes or local installer actions, AI assistants
must run `devctl preflight` and record the result in the TDD result sheet.

If Python 3.10+ is missing, devctl must fail closed. AI assistants must not
silently install Python. Installation requires a local human review approval
that names the installer command and the reason it is needed.

## Required Local Artifacts

Each academic task must keep auditable files under:

```text
.xflow/issue-<id>/
  issue-draft.md
  implementation_plan.md
  task.md
  tdd-result.md
  claude-task.md
  claude-result.md
  mr-draft.md
  walkthrough.md
  approvals/
    local-review.md
```

`claude-task.md` and `claude-result.md` are required only when Claude or
AcademicForge skills are used.

## State Machine

```text
S0_REQUEST
S1_LOCAL_ISSUE_DRAFT
G1_LOCAL_APPROVE_ISSUE
S2_CREATE_REMOTE_ISSUE
G2_APPROVE_DEVELOPMENT
S3_START_ACADEMIC_BRANCH
S4_EXECUTE_AI_OR_CLAUDE_TASK
S5_WRITE_TDD_RESULT
G3_LOCAL_REVIEW_RESULT
S6_PREPARE_COMMIT_AND_MR_DRAFT
G4_LOCAL_APPROVE_REMOTE_WRITE
S7_PUSH_BRANCH
G5_LOCAL_APPROVE_MR
S8_CREATE_REMOTE_MR
S9_REMOTE_REVIEW_AND_CI
G6_APPROVE_CLEANUP
S10_CLOSE_AND_ARCHIVE
```

## Gates

- `G1_LOCAL_APPROVE_ISSUE`: required before creating a remote issue.
- `G2_APPROVE_DEVELOPMENT`: required before creating or switching to a task branch.
- `G3_LOCAL_REVIEW_RESULT`: required after TDD/verify and before any remote write.
- `G4_LOCAL_APPROVE_REMOTE_WRITE`: required before pushing, commenting, or closing.
- `G5_LOCAL_APPROVE_MR`: required before creating an MR/PR.
- `G6_APPROVE_CLEANUP`: required before closing issues or deleting local branches.

Approval for one gate authorizes only the next action. It does not authorize
later remote writes.

Use machine-readable approval actions in `approvals/local-review.md`:
`issue-create`, `issue-comment`, `issue-close`, `git-mr`, or `remote-write`.

## Approval Hash Rule

Local approvals must bind to the reviewed artifact by hash. The approval
record must include:

- reviewer
- approval time
- approved action
- approved file
- approved SHA256

If the approved file changes, the approval is invalid and must be repeated.

## Claude Delegation Rule

Claude is a controlled academic sub-executor. The upper-level AI may call the
local Claude installation automatically, but only through a task package.

Claude output is never final by itself. It must be archived as a reviewable
artifact, checked by `devctl`, and approved by the human reviewer before it can
be used in final documents or remote MR/PRs.

## Required Checks

Use these checks before local approval or remote writes:

```bash
devctl check academic-issue --issue <id>
devctl check tdd-result --issue <id>
devctl check claude-package --issue <id>
devctl check academic-mr --issue <id>
devctl check local-review --issue <id> --file <approved-file>
```

The exact command availability is defined by `xflow-devctl@academic`.
