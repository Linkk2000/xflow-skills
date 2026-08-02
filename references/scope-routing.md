# Scope Routing

## Classification Consistency

Before a remote Issue exists, create
`.xflow/issues/issue-draft/classification.yaml` and run:

```text
devctl check classification --issue draft
```

Draft the route's next artifact under `.xflow/issues/issue-draft/`. After the
separately approved Issue-create action returns a confirmed ID, migrate the
draft artifacts to `.xflow/issues/issue-<id>/`, replace draft placeholders,
create canonical task state, run `devctl task activate --issue <id>`, and check
the migrated classification again. Do not run contract acceptance for `draft`.

The document is version `0.1.0` and includes `request.originalStatement`,
`contractSearch.status`, `contractSearch.refs`, `classification`,
`contractChangeRequired`, `reason`, `nextArtifact`, and `decisionSource`.
`contractSearch.status` is exactly `found|not-found`.

| Classification | Required | Next artifact |
| --- | --- | --- |
| `capability-change` | `contractChangeRequired: true`; found or not-found | `contract-change-proposal.md` |
| `implementation-gap` | `false`; found contract | `gap-analysis.md` |
| `ui-defect` | `false`; contract-search evidence | lightweight classification stop |
| `infrastructure` | `false`; found or not-found | `dependency-issue-proposal.md` |
| `governance` | `false`; found or not-found | `issue-draft.md` |
| `future` | `false`; found or not-found | `futureCapabilitiesOutOfScope` or `future-task-proposal.md` |

For `found`, refs must be non-empty; for `not-found`, refs must be empty.
Changing implementation because it violates an existing contract is an
`implementation-gap`: write and obtain human recognition of `gap-analysis.md`
before implementation. Changing the participant-visible promise is a
`capability-change`: author and obtain human acceptance of a contract first.
Issue creation approval and contract acceptance are separate gates; neither
approves entering development.

## Lightweight UI Defect Route

A request that is explicitly a visual, styling, or contrast defect and does
not change existing behavior or capability semantics is classified as
`ui-defect`; retain that route. The only required core artifact is
`classification.yaml`: record contract-search evidence and
`contractChangeRequired: false`. If no applicable contract is found, fail
closed by requesting additional contract-search evidence while retaining
`ui-defect`; must not require capability-contract creation or establish a
capability baseline. This route must not require `issue-draft.md`,
`gap-analysis.md`, `task-state.md`, `resolution-report.md`, or G1/G2 as a
precondition. Stop when lightweight classification and acceptance evidence
recorded. Later delivery follows the ordinary Issue/Git workflow, but this
does not rewrite this routing stop condition. `ui-defect` must not make
capability semantic changes.

## Dependency Issue Boundary

Use a local subtask for work owned by the same feature branch. Use a dependency
Issue only for independently owned work, classifying it as
`child-feature|shared-infrastructure|external`. A dependency proposal is not a
remote Issue. Human approval remains required before remote dependency Issue
creation unless a valid task-scoped unattended state covers that remote action.
For `shared-infrastructure`, the generic exception does not replace or satisfy
the separate human semantic decision, and the parent Issue's approval or
unattended state must not be reused to authorize the dependency.

Record dependency work in the tracked Issue workspace:
`.xflow/issues/issue-<id>/dependencies.yaml`. `discovered` belongs in analysis
before the remote identity exists; it must not appear in the ledger. Ledger
status is `active|available|integrated|superseded`. `active` and `available`
are advisory and must not automatically block development, commits, tests, or
evidence collection. `integrated` requires fresh parent-side verification and
repository-local evidence, not a dependency's completion statement.

```text
devctl check dependencies --issue <id>
devctl check issue-evidence --issue <id>
```

Issue-level evidence and approvals stay under `.xflow/issues/issue-<id>/`;
published remote bodies belong under `.xflow/publish/issues/issue-<id>/`.

## Shared Infrastructure Approval Isolation

`shared-infrastructure` is a separate dependency Issue and must not reuse the
parent Issue, branch, or worktree's approval, task-scoped unattended state, or
development authorization. Before dependency Issue creation or
shared-infrastructure implementation, a human must separately accept the
dependency scope and named parent integration target. This semantic decision
is separate from issue-create approval; Issue-create approval cannot substitute
for it. Dependency state remains advisory, and `integrated` still requires
fresh parent-side integration evidence.

Only after that human semantic decision may the dependency use its own
issue-create gate. Any generic Issue flow or unattended path is subordinate to
this branch and cannot be used to skip it.
