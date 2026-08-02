# Contract Generation Evaluation

## Status And Scope

`HUMAN_SEMANTIC_ACCEPTANCE_COMPLETED / IMPLEMENTATION_EVIDENCE_NOT_RUN`.

This is Task 13 evidence for contract semantics and verification design. It
does not implement, execute, or prove project initialization or recovery. All
implementation runtime evidence remains `NOT_RUN`; planned `verifyBy` targets
are future engineering evidence, not results from an initialization, restore,
Git, fetch, or ignore-rule run.

The accepted baseline is
`.xflow/issues/issue-contract-evaluation/evidence/contract.generated.yaml`.
The associated immutable acceptance history, claim, and consumed review are
under `.xflow/issues/issue-contractevaluation/approvals/history/`. Reviewer
identity is intentionally not reproduced here.

## Discovery Replay: D01-D22

The replay began with natural-language input only, searched repository rules,
existing contract material, bootstrap and restore policy, templates, schemas,
tests, and the devctl surface, then stopped before contract generation or
implementation. It found generic contract support but no accepted,
request-specific bootstrap/recovery contract. The following is the concise
decision overview; the full questions, options, recommendations, and adopted
answers are in the Task 13 discovery record.

| Decisions | Adopted boundary |
| --- | --- |
| D01-D03 | A bootstrap-only entry leaves the authority chain after project tools are verified; Git routing distinguishes non-Git, no/empty-remote Git, and established-remote Git; safe independent local work may continue while conflicting targets remain unchanged and block development. |
| D04-D06 | Each tool restores a recorded resolved commit, workflow and devctl may use independently recorded modes, and only known managed rule blocks may change. |
| D07-D09 | “Enable XFlow” authorizes only local inspection and safe initialization/recovery at a confirmed contained root; sources must be project-bound, explicitly supplied, or allowlisted, never global fallbacks. |
| D10-D12 | Missing machine prerequisites are reported rather than installed; the bootstrap hands execution to project-local devctl; managed configuration fields reconcile without replacing project-owned fields. |
| D13-D15 | Only missing or clean matching tool directories may be aligned; ignore rules are exact and effective-ignore checked; existing Issue, task, approval, and evidence material is preserved byte-for-byte. |
| D16-D18 | Only missing or known generated wrappers may be restored; business Git state is preserved with only necessary read-only remote inspection; preparation produces a candidate list, checks, and draft rather than stage or commit. |
| D19-D22 | Historical approval is never inherited; readiness requires coherent tool bindings, compatibility, wrappers, adapter, ignores, and no blocking conflict; results contain an audit; the next workflow action requires its own human gate. |

The contract captures stable IDs, failure preservation, verification before
engineering projection, blockers, and future scope. Its semantic rubric passed
for purpose quality, testable constraints, success/failure completeness,
authority versus projection, future separation, and stable IDs. Lint is
supporting structure evidence only, not semantic acceptance or runtime proof.

## Human Acceptance Binding

The immutable accepted record binds exactly one `contract-acceptance` action
for contract ID `xflow.contract.project-local-initialization-recovery`, version
`0.1.0`, SHA-256
`deef597c50a40694143dd4b38a03196f3869c8e52fe38ef40bc3e4957eb5c729`, and
the complete ordered set of 51 accepted object IDs. The immutable history,
claim, and consumed review agree on the contract digest, object set,
repository/worktree/branch context, action, and non-reusable consumption.

Five pre-acceptance checks failed closed:

| Check | Result |
| --- | --- |
| `Approved: no` | Rejected; AI/tooling cannot convert a negative local review into approval. |
| Unattended/no-local-review attempt | Rejected (`--no-local-review` is not accepted; exit 2). |
| Changed contract hash | Rejected on hash mismatch (exit 1); restored baseline bytes retained the accepted digest. |
| Wrong detached worktree | Rejected because the task cannot bind to detached HEAD (exit 1). |
| Omitted accepted object ID | Rejected on complete-set mismatch (exit 1). |

After a human changed the review to approval, the complete acceptance command
succeeded once (exit 0). A later history-reuse attempt was also rejected as
already consumed (exit 1). This is semantic acceptance only: it grants neither
development authorization nor evidence that initialization or recovery ran.

## Version-Evolution Replay

Each candidate was linted and then diffed against the accepted `0.1.0`
baseline. All lint and diff commands returned exit code 0.

| Variant | Required / actual result | Stable-ID and review result |
| --- | --- | --- |
| PATCH `0.1.1` | `patch / patch` | Only the root note changed; no IDs were added or removed, and every non-root accepted object remained `0.1.0`. |
| MINOR `0.2.0` | `minor / minor` | No accepted object changed or was removed. Six self-contained optional read-only explanation objects began at `0.1.0`. |
| MAJOR `1.0.0` | `human-review / major` | The local Git initialization constraint was replaced by an inspection-and-authorization constraint with `supersedes`; affected objects became `1.0.0`, all others stayed stable. Two warnings require fresh semantic review; there were no errors. |

The synthetic implementation-gap observation reports both tools as `vendor`
while reporting aggregate `mixed`. That violates
`xflow.constraint.tool-binding-reproducibility`; it is an implementation gap,
not a contract change. The scratch comparison had the same accepted SHA-256 and
root version `0.1.0`, so the correct outcome is to fix and test implementation
without changing contract IDs or versions. It is not runtime evidence.

## Pressure Replay And Closure

Three replay rounds were evaluated: the initial six-scenario corpus in
`.superpowers/sdd/2026-07-30-capability-contract-closure-implementation/pressure/`,
the R2 replay, and the final independent R3 review. The following commits close
the discovered parsing, route, approval-binding, and evidence-provenance gaps:

| Commit | Closure |
| --- | --- |
| `2860cb6` | Approval binding and real-product evidence requirements. |
| `0523c48` | Evidence-rule structural assertions. |
| `8575ef0` | Code-fence pseudo-rule exclusion. |
| `96d44ae` | Variable-length fence parsing. |
| `d8531f0` | Nested-fence coverage. |
| `8f27c29` | Lightweight UI and shared-infrastructure gates. |

An initial feedback reference to `contract-routing.md` was a filename
misjudgment. The authoritative routing source is
`references/scope-routing.md`; R3 explicitly used that file and did not consult
the misidentified name.

| Scenario | Final R3 result |
| --- | --- |
| `new-capability` | PASS |
| `existing-contract-gap` | PASS |
| `pure-ui-defect` | PASS |
| `shared-infrastructure` | PASS |
| `parallel-task-stale-approval` | PASS |
| `harness-evidence-misrepresented` | PASS |

R3 verdict: `ALL_PASS`; no remaining loopholes or recommended fixes. In every
scenario the expected route, exact required artifacts, forbidden actions, stop
condition, human-judgeable evidence, and pressure-rationalization refusal were
checked. This validates semantic routing and verification design, not the
unimplemented bootstrap/recovery runtime.

## Current Mechanical Evidence

- `python tests/main_entrypoint.py` is the required entrypoint replay.
- `python tests/pressure_scenarios.py` is the required pressure-manifest replay.
- `git diff --check` is the required whitespace validation.

Their current execution results are recorded in the Task 13 completion report.
