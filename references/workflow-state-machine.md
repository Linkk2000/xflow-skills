# XFlow Main Workflow State Machine

This state machine is for the generic `main` product line. It prevents AI
assistants from treating an issue-driven workflow as a loose checklist.

## States

```text
S0_REQUEST
S1_LOCAL_ISSUE_DRAFT
G1_APPROVE_ISSUE_CREATE
S2_REMOTE_ISSUE_CREATED
G2_APPROVE_DEVELOPMENT_START
S3_TASK_BRANCH_STARTED
S4_TDD_AND_IMPLEMENTATION
S5_LOCAL_VERIFICATION
G3_APPROVE_RESULT
S6_PREPARE_COMMIT_AND_MR_DRAFT
G4_APPROVE_REMOTE_WRITE
S7_PUSH_BRANCH
G5_APPROVE_MR_CREATE
S8_CREATE_REMOTE_MR
S9_REMOTE_REVIEW_AND_CI
G6_APPROVE_CLEANUP
S10_DONE
```

`S*` states are machine/AI work states. `G*` states are local human gates.
The AI may prepare evidence for a gate, but must not approve the gate.

## Current Task File

Each active task should have `.xflow/current-task.md`. It records the current
issue, state, allowed actions, and forbidden actions. It is an execution guard,
not a replacement for human review.

Run this before local approval, commit, push, MR/PR creation, and cleanup:

```bash
devctl check current-task --issue <id>
```

If a PR/MR has just been created, `devctl` writes
`.xflow/issues/issue-<id>/state-update-suggestion.md`, updates local XFlow task
state with the PR number/URL, creates a metadata-only state backfill commit,
and pushes that commit to the same branch. This post-MR push is part of the
`git-mr` approval scope and must not include business code.

## Gate Meaning

- `G1_APPROVE_ISSUE_CREATE`: human approves the issue body before remote issue
  creation. If approved non-image attachments are referenced, the human also
  approves the attachment manifest and rendered public URLs. Issue/comment
  images cannot be approved for remote upload under the current policy.
- `G2_APPROVE_DEVELOPMENT_START`: human accepts the created issue and intended
  task branch before implementation starts.
- `G3_APPROVE_RESULT`: human reviews local evidence, test results, scope, and
  generated artifacts before commit or remote publication.
- `G4_APPROVE_REMOTE_WRITE`: human approves the exact evidence file before
  `devctl git push`. If the body contains attachment-derived links, the
  approval also covers the attachment manifest hash.
- `G5_APPROVE_MR_CREATE`: human approves creating the remote PR/MR after target
  branch synchronization evidence is available. This approval also covers the
  metadata-only state backfill commit and push created after the PR/MR number
  and URL are known.
- `G6_APPROVE_CLEANUP`: human confirms cleanup, issue close, or archival
  actions after remote review finishes.

## Pre-Merge Synchronization Checkpoint

Before `G5_APPROVE_MR_CREATE`, the task branch must be synchronized with the
current target branch:

1. Fetch the target branch.
2. Record the target branch SHA.
3. Merge `origin/<base>` into the current task branch by default.
4. Resolve conflicts only under the approved conflict strategy.
5. Rerun relevant checks.
6. Record the sync result in the MR/PR draft or local task evidence.

Do not create an MR/PR if this checkpoint has not completed. Rebase is allowed
only when the user or project policy explicitly prefers it and the AI previews
the strategy first.

## AI Constraints

- Do not edit an approval file to set `Approved: yes`.
- Do not skip a `G*` state because tests pass.
- Do not skip target branch synchronization before MR/PR creation.
- Do not rely on memory. Read `.xflow/current-task.md` and run
  `devctl check current-task --issue <id>`.
- If the state file is stale, prepare a proposed update and ask the human to
  confirm before continuing remote-write work.
