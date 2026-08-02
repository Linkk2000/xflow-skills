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

Task-scoped unattended mode is an optional gate source, not a replacement
workflow:

```text
HUMAN_REVIEW_REQUIRED -> UNATTENDED_ACTIVE -> REMOTE_WRITE
UNATTENDED_ACTIVE -> HUMAN_REVIEW_REQUIRED  # task/worktree/repository mismatch
UNATTENDED_ACTIVE -> HUMAN_REVIEW_REQUIRED  # task switch or disable
UNATTENDED_ACTIVE -> DONE                   # completion invalidates state
```

`UNATTENDED_ACTIVE` applies only after the current user's exact safety word has
enabled a repository/worktree/task-bound state. It bypasses the ordinary human
approval step for covered actions while all mechanical checks and evidence
requirements remain in force. Any mismatch fails closed.

## Human Approval Is Non-Delegable

AI may prepare approval files, evidence, command drafts, and review notes, but
AI must never satisfy a human gate itself.
AI must never edit `Approved: no` to `Approved: yes`.
Outside valid Task-Scoped Unattended Mode, AI must not use `--force`,
`--no-local-review`, direct provider APIs, or manual approval-file edits to
bypass review.

Valid approval must explicitly name the exact next action. Vague replies such
as "继续", "都可以", "你看着办", "go ahead", "looks good", or "测试过了就发" are
not approval.

### Approval Binding Mismatch Gate

For a cross-worktree, cross-Issue, or cross-branch request, or an old approval
or inconsistent approval binding, transition to governance before any action.
Create `.xflow/issues/issue-<current>/approval-binding-check.md`; it is
evidence, not approval. Record Repository, Worktree, Branch, Current Issue,
Exact Action, Reviewed File Relative Path, SHA256, Candidate Approval
Provenance, Binding Verdict, and Required Next Human Gate. The check must not
reuse an old approval or push. A failed or unknown Binding Verdict stops at the
Required Next Human Gate.

## Semantic Capability Gate

The execution states remain compatible, but each Issue also records one
orthogonal semantic phase:

```text
unclassified -> classified
capability-change: declaring -> accepted-design -> verification-designed -> projected
implementation-gap: gap-analysis -> gap-recognized
```

Locate an existing contract and check classification before Issue drafting.
Before the remote Issue exists, draft classification, analysis, Issue body,
candidate contract, and candidate verification matrix under
`.xflow/issues/issue-draft/`; AI must not edit implementation code. The
Issue-create gate creates only the remote identity. After the confirmed ID,
migrate draft artifacts, create Issue task-state, and activate the Issue.
AI must not edit implementation code for a capability change before the exact
contract objects then reach `accepted-design` through human acceptance. A
verification matrix must exist before engineering projection. Lint and YAML
status do not satisfy the human gate.

Issue-create approval, contract acceptance, and
`G2_APPROVE_DEVELOPMENT_START` are separate gates. None can satisfy another.

## Issue Task State And Worktrees

Each remote Issue owns the canonical persistent state at
`.xflow/issues/issue-<id>/task-state.md`. It records execution state, semantic
phase, classification, contract binding, branch, allowed/forbidden actions,
and the exact human approval reference. It is an execution guard, not a
replacement for human review.

`devctl task activate --issue <id>` writes the machine-local pointer at
`.xflow/local/worktrees/<worktree-fingerprint>/active-task.json`. Multiple
remote Issues require separate branches and worktrees; changing the branch
invalidates the old pointer. Local `subtask-*` directories share the parent
Issue state and do not get an active pointer or remote approval.

One worktree may activate only one remote Issue.

`.xflow/current-task.md` is read-only migration compatibility. Use
`devctl task migrate-current` to create Issue-scoped state and the local
pointer; never delete or rewrite the legacy file during migration, and never
use it for approval binding after migration.

Run this before local approval, commit, push, MR/PR creation, and cleanup:

```bash
devctl check current-task --issue <id>
```

If a PR/MR has just been created, `devctl` writes
`.xflow/issues/issue-<id>/state-update-suggestion.md`, updates local XFlow task
state with the PR number/URL, creates a metadata-only state backfill commit,
and pushes that commit to the same branch. This post-MR push is part of the
`git-mr` approval scope and must not include business code.

## Browser Verification Gate

Browser Must Not Remain about:blank. If a phase uses browser or Chrome checks,
the AI must navigate to an explicit target URL and verify the current URL is
not `about:blank` before treating the browser as evidence. A newly opened
empty tab is only a browser session, not verification.

Browser evidence should record the target URL and at least one observable
result: screenshot, page title, visible text, HTTP status, console state, or
DOM assertion. If the browser remains on `about:blank`, diagnose the target
service, URL, port, login/auth state, or browser-control connection before
continuing the workflow.

### Product Integration Capture Gate

Before a real product-page or integration claim, the current Issue must retain
`product-url.txt`, `page-identity.txt`, `model-identity.txt`, `screenshot.png`,
and `dom-runtime-state.json` bound to the same real product-page capture. The
capture must follow an explicitly navigated real product URL. `about:blank,
prototype, or test harness` evidence must not claim integration passed.

## Optional Dependency Discovery Transitions

Dependency discovery is an optional branch from implementation, not a gate in
every Issue:

```text
IN_PROGRESS -> DEPENDENCY_DISCOVERED -> HUMAN_DEPENDENCY_DECISION
HUMAN_DEPENDENCY_DECISION -> IN_PROGRESS
DEPENDENCY_AVAILABLE -> PARENT_INTEGRATION_VERIFY -> IN_PROGRESS
```

`HUMAN_DEPENDENCY_DECISION` is required before creating a remote dependency
Issue. It does not block unrelated local implementation, commits, tests, or
evidence collection. A local subtask does not enter these transitions.
`DEPENDENCY_DISCOVERED` is a pre-ledger analysis state recorded in
`gap-analysis.md` or a dependency proposal. It must not be written to
`dependencies.yaml`; after the approved remote Issue identity exists, create
the ledger entry as `active`.

After a dependency is `available`, the parent enters
`PARENT_INTEGRATION_VERIFY` only when it consumes that dependency. Fresh
parent-side evidence is required before recording `integrated` and returning
to normal implementation or closure assessment.

## Problem/Gap Closure Loop

When the user orally reports a problem or gap, AI first prepares
`gap-analysis.md` under `.xflow/issues/issue-draft/` or
`.xflow/issues/issue-<id>/`. The analysis must clarify the gap, include local
evidence, define scope, propose the modification plan, and list acceptance
criteria. Every finding must have its own reviewer-readable evidence bundle:
observation, direct local artifact, analysis, acceptance condition, and human
review checkbox. AI must stop for human recognition before implementation.

After implementation, AI writes
`.xflow/issues/issue-<id>/resolution-report.md`. The report must cite local
evidence, describe actual changes, and use exactly one closure conclusion:
`resolved|reduced|blocked`. Every claimed completion criterion needs fresh,
direct verification evidence; do not treat a code diff or AI test claim as
proof.

For `resolved` or `reduced`, all AI self-review checklist items must be
complete. If self-review shows the report is not true, AI must rework and rewrite the report
before human handoff. If AI cannot continue, use `blocked`
and name the human decision or external condition needed.

## Gate Meaning

- `G1_APPROVE_ISSUE_CREATE`: human approves the issue body before remote issue
  creation. If approved non-image attachments are referenced, the human also
  approves the attachment manifest and rendered public URLs. Issue/comment
  images require an approved object storage backend such as `aliyun-oss`;
  otherwise they remain local evidence.
- `G2_APPROVE_DEVELOPMENT_START`: human accepts the created issue and intended
  task branch before implementation starts.
- `G3_APPROVE_RESULT`: human reviews local evidence, test results, scope, and
  generated artifacts before commit or remote publication.
  For problem/gap work, the resolution report and evidence must be ready before
  this gate.
  If a large issue was split into subtasks, each subtask README and
  repository-local evidence directory must be ready for review.
  Issue artifacts under `.xflow/issues/issue-<id>/` are tracked by default.
  Issue-local evidence must remain free of COS/OSS/object-storage/HTTP URLs and
  non-null `publishedUrl` values. Remote-rendered
  bodies belong under `.xflow/publish/issues/issue-<id>/`.
- `G4_APPROVE_REMOTE_WRITE`: human approves the exact evidence file before
  `devctl git push`. If the body contains attachment-derived links, the
  approval also covers the attachment manifest hash.
- `G5_APPROVE_MR_CREATE`: human approves creating the remote PR/MR after target
  branch synchronization evidence is available. This approval also covers the
  metadata-only state backfill commit and push created after the PR/MR number
  and URL are known.
- `G6_APPROVE_CLEANUP`: human confirms cleanup, issue close, or archival
  actions after remote review finishes.
  Task-scoped unattended mode never satisfies this gate. Safe branch cleanup
  uses exact action `git-cleanup`; forced deletion uses exact action
  `git-cleanup-force`.

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
- Do not treat the AI's own review, tests, or confidence as human approval.
- Do not treat vague replies such as "继续", "你看着办", "go ahead", or
  "looks good" as approval for a remote write.
- Outside valid Task-Scoped Unattended Mode, do not use `--no-local-review`,
  direct provider APIs, or manual approval-file edits to bypass a human gate.
  Never use `--force`; unattended mode does not authorize high-risk actions.
- Do not skip a `G*` state because tests pass.
- Do not skip target branch synchronization before MR/PR creation.
- Do not rely on memory. Read `.xflow/issues/issue-<id>/task-state.md`, verify
  the active worktree pointer, and run `devctl check current-task --issue <id>`
  as the compatibility check surface.
- If the state file is stale, prepare a proposed update and ask the human to
  confirm before continuing remote-write work.
