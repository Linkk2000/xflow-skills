# Advisory Dependency Issue Workflow

Use this workflow when implementation or verification discovers work that may
sit outside the accepted scope or ownership of the main Issue. Dependency state
is advisory during development; it does not replace evidence or human review.

## Classification

Compare the discovered work with the accepted main Issue scope before splitting
anything:

- Keep work in the main Issue when it has no independent delivery boundary,
  owner, branch, review, or resolution report.
- Use `child-feature` for independently deliverable work inside the parent
  capability.
- Use `shared-infrastructure` for reusable infrastructure owned independently
  of the parent feature.
- Use `external` for work supplied by another repository, service, team,
  permission boundary, or external condition.

The canonical classification set is
`child-feature|shared-infrastructure|external`.

## Local Subtask Versus Dependency Issue

A local subtask is not a dependency Issue. A `subtask-*` directory is only a
local decomposition of one Issue and keeps repository-owned evidence under its
own `evidence/` directory. It does not require a remote Issue or branch.

A dependency Issue has independent ownership or delivery boundaries. Record it
in `.xflow/issues/issue-<id>/dependencies.yaml` after its identity is known.

## Lightweight UI Defect Route

A request that is explicitly a visual, styling, or contrast defect and does
not change existing behavior or capability semantics is classified as
`ui-defect`; retain that route. The only required core artifact is
`classification.yaml`: record contract-search evidence and
`contractChangeRequired: false`. Set `nextArtifact: lightweight-route-complete`
for both `found` and `not-found`; this is a terminal sentinel, not a file. If no applicable contract is found, fail
closed by requesting additional contract-search evidence while retaining
`ui-defect`; must not require capability-contract creation or establish a
capability baseline. This route must not require `issue-draft.md`,
`gap-analysis.md`, `task-state.md`, `resolution-report.md`, or G1/G2 as a
precondition. Stop when lightweight classification and acceptance evidence
recorded. Later delivery follows the ordinary Issue/Git workflow, but this
does not rewrite this routing stop condition. `ui-defect` must not make
capability semantic changes.

## Shared Infrastructure Approval Isolation

`shared-infrastructure` is a separate dependency Issue and must not reuse the
parent Issue, branch, or worktree's approval, task-scoped unattended state, or
development authorization. Before dependency Issue creation or
shared-infrastructure implementation, a human must separately accept the
dependency scope and named parent integration target. This semantic decision
is separate from issue-create approval; Issue-create approval cannot substitute
for it. Dependency state remains advisory, and `integrated` still requires
fresh parent-side integration evidence.

## Human Gate for Remote Issue Creation

AI may prepare classification analysis, Issue text, traceability, and approval
material. Creating a remote dependency Issue remains a remote write protected
by Human Approval Is Non-Delegable by default. After running current-task,
Issue draft structure, evidence, attachment, provider/platform, and applicable
test checks, choose exactly one path:

- Default human path: prepare the approval file, wait for exact human approval,
  and validate it with `devctl check local-review` before Issue creation.
- Valid task-scoped unattended path: verify the bound state and covered action,
  then skip approval-file preparation, human wait, and local-review validation.
  For `shared-infrastructure`, this path does not replace or satisfy the
  separate human semantic decision, and the parent Issue's approval or
  unattended state must not be reused to authorize dependency Issue creation
  or implementation. Only after the human accepts the dependency scope and
  named parent integration target may the dependency's own issue-create gate
  be selected. The current-task, draft structure, evidence, attachment, provider/platform, and test checks still run.

## Advisory Blocking Assessment

Every dependency records its development decision:

- `blockingAssessment`: `none|partial|full`
- `decision`: `continue|pause-affected-scope|wait|use-temporary-adapter`
- `rationale`: the developer's current reasoning

These fields record developer judgment and must not automatically block
development, commits, tests, or evidence collection. Mechanical checks may
warn about missing or inconsistent dependency data, but devctl does not decide
whether product work should stop. A temporary adapter must include a recorded
removal condition.

## Lifecycle

Before a remote Issue identity exists, record discovery, classification,
evidence, and the proposed split in `gap-analysis.md` or a dependency proposal.
This is the pre-ledger `discovered` stage and must not write `discovered` to `dependencies.yaml`.
Once the approved remote Issue identity is known, add the
ledger entry with `status: active`.

The normal lifecycle is:

```text
pre-ledger discovered -> active -> available -> integrated
```

`superseded` is an explicit alternative when an approved design change removes
the dependency. `available` proves only that the dependency can be consumed.
The parent must gather fresh integration evidence before setting `integrated`.

## Branch and Integration Paths

- `child-feature`: branch from the parent feature branch, complete the child
  Issue, merge it back into the parent feature branch, then re-verify there.
- `shared-infrastructure`: branch from the target mainline, merge independently
  into mainline, then synchronize the parent feature branch and re-verify.
- `external`: record provider, version, entry point, status, and evidence. Do
  not invent local branches or commits.

Simple in-scope work stays directly on the main feature branch.

## Parent Closure Assessment

Each dependency records `closureAssessment.affectsClosure`, closure `decision`
(`integrated|not-required|superseded`), and `rationale`:

- An unintegrated dependency may support `resolved` only when
  `affectsClosure: false` uses `decision: not-required` with sufficient evidence
  and rationale.
- An unintegrated dependency affecting some acceptance conditions keeps the
  parent conclusion at `reduced`.
- A dependency preventing all useful progress may support `blocked`.
- `affectsClosure: true` supports `resolved` only after `integrated` or an
  approved `superseded` decision.

## Evidence and Traceability

The dependency Issue owns its analysis, implementation, tests, evidence, and
resolution report. The parent records the split decision and fresh evidence
from consuming the dependency. Dependency completion evidence can establish
`available`; it cannot substitute for parent-side integration evidence.

All evidence paths in `dependencies.yaml` are relative to the parent Issue
directory and must remain inside the repository.

## Commit Ownership

Direct parent-feature commits use the parent Issue ID. Child-feature and
shared-infrastructure commits use their direct dependency Issue ID and link
the parent or known consumers in the body. Ordinary commits have one direct
owner Issue. Only a `merge(...)` integration commit may include the parent and
dependency IDs.

## devctl Checks

Run:

```text
devctl check dependencies --issue <id>
```

The check validates YAML structure, enums, required fields, evidence paths,
and integration consistency. It may emit structural warnings, but dependency
state alone must not automatically block development, commits, tests, or
evidence collection. Human reviewers still assess business meaning and
evidence sufficiency.
