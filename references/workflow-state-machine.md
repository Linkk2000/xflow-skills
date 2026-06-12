# XFlow Workflow State Machine

## States

1. `S0_REQUEST`: user gives oral or written request.
2. `S1_DRAFT_ISSUE`: agent summarizes request and drafts issue.
3. `G1_APPROVE_ISSUE`: human approves issue title/body/labels.
4. `S2_CREATE_ISSUE`: agent creates issue.
5. `G2_APPROVE_DEVELOPMENT`: human explicitly asks to begin development.
6. `S3_START_BRANCH`: agent creates issue-bound branch.
7. `S4_TDD_IMPLEMENT`: agent writes failing test, implements, verifies.
8. `G3_APPROVE_PUSH`: human approves branch push.
9. `S5_PUSH_BRANCH`: agent pushes branch only.
10. `G4_APPROVE_MR`: human approves MR title/body.
11. `S6_CREATE_MR`: agent creates MR/PR.
12. `G5_APPROVE_CLEANUP`: human confirms merge/close/cleanup status.
13. `S7_CLEANUP`: agent closes issue if needed and cleans local branch.

## Gates

- `G1_APPROVE_ISSUE`: required before creating a remote issue.
- `G2_APPROVE_DEVELOPMENT`: required before creating or switching to an issue-bound development branch.
- `G3_APPROVE_PUSH`: required before pushing the current branch.
- `G4_APPROVE_MR`: required before creating an MR/PR.
- `G5_APPROVE_CLEANUP`: required before closing an issue or deleting/cleaning local branches.

## Transition Rule

Do not skip gates. If the user authorizes one gate, only the next state is authorized.
