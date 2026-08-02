# Capability Contract Residual Remediation - Final Fix Report

Date: 2026-08-03

## Result

All findings in `final-review.md` (C1, I1, I2, I3, I4, M1) are remediated.
The implementation used direct failing regression tests before production changes, followed by focused GREEN runs and complete required regression suites. The two repositories were committed independently. No existing history was rewritten and nothing was pushed.

## Commits

- Devctl base: `46e1e9bfe60bc760c3abd9b88104730b094d3c27`
- Devctl fix: `9e0c958336c8291651633d0a36a14fdb17582c90`
- Skills base: `5947c957e44a084057b39d94ac2cca8327a4b72a`
- Skills documentation/test fix: `b94f17a09aad6465817eda2cdf1106516847d629`
- This report is committed separately after the implementation commits so it can cite both stable implementation SHAs.

## C1 - Scope-Wide Pending MR Claim Arbitration

### RED

Command: `python tests\approval-binding.py` after registering the new direct cases.

Observed failures:

- `reserved + replacement approval` reached `[INFO] PR #42 created`; the expected failure return code was not produced and the provider call count increased.
- `outcome-unknown + replacement approval` likewise reached the provider.
- A `remote-confirmed + unresolved` mixture selected the confirmed claim instead of failing closed.

Direct tests:

- `test_reserved_mr_claim_blocks_replacement_approval_provider_call`
- `test_unknown_mr_claim_blocks_replacement_approval_provider_call`
- `test_confirmed_mr_claim_is_not_selected_while_an_unresolved_claim_exists`
- `test_human_confirmed_no_effect_allows_replacement_mr_approval`

### Fix

`xflow/approval.py` now scans every canonical remote claim in the exact repository/worktree/branch/Issue/action scope. Arbitration occurs at the MR entry before fresh body/review/provider work and is repeated under the stable remote-claim scope lock before reservation mutation.

- Any `reserved` or `outcome-unknown` claim blocks all new provider mutation.
- Exactly one `post-effects-pending` or `remote-confirmed` claim, with no unresolved claim, is eligible for sealed replay.
- Multiple confirmed claims and confirmed/unresolved mixtures fail closed.
- A `retryable` claim is ignored only after the existing exact human reconciliation records `no-effect`.

Files: `xflow/approval.py`, `tests/approval-binding.py`.

### GREEN

Focused cases returned the scope-wide reconciliation error without incrementing provider calls; the human-confirmed `no-effect` case invoked the provider exactly once for the replacement approval. Final full output: `approval binding ok` (exit 0).

## I1 - Supplied Contract Evolution and TOCTOU

### RED

Command: `python tests\trace-core.py` after registering the supplied-contract cases.

Observed failures:

- A breaking object change with only a root MINOR bump returned success.
- A replacement verification without a one-to-one `supersedes` relation returned success.
- Mutating the supplied file between validation and closure did not raise `ValueError`.

Direct tests:

- `test_historical_contract_trace_rejects_breaking_change_with_minor_bump`
- `test_historical_contract_trace_rejects_replacement_without_supersedes`
- `test_historical_contract_trace_rejects_human_review_ambiguity`
- `test_supplied_contract_is_revalidated_at_trace_closure`
- `test_historical_contract_trace_allows_same_version_status_lifecycle`

### Fix

`xflow/traceability.py` now validates sealed-to-supplied evolution with the existing `diff_contracts` and `contract_diff_exit_code` rules. Any `[ERROR]` result or `human-review` ambiguity fails closed because an explicit supplied file is not new acceptance authority. Same ID, non-regressing version, accepted status, and same-version status-only lifecycle checks remain enforced.

`_load_context` captures the exact supplied path, bytes, hash and parsed `ContractDocument`, verifies them against the caller's object, adds the file to tracked snapshots, and revalidates it at closure.

Files: `xflow/traceability.py`, `tests/trace-core.py`.

### GREEN

All direct negative cases now raise the intended evolution/closure errors; the same-version status-only positive case remains accepted. Final full output: `trace core ok` (exit 0). `contract diff ok` also passed.

## I2 - Force-Pushed Base and Human Claim Retirement

### RED

Command: `python tests\task-state.py` after registering force-push, unreachable-SHA and retirement cases.

Observed failures:

- A force-replaced remote base continued through `[INFO] create branch ...` and `[INFO] ready`.
- An unreachable sealed SHA left the old claim shadowing a new human approval.
- The required retirement CLI was absent (`invalid choice: supersede-branch-start`).

Direct tests:

- `test_task_branch_start_rejects_force_pushed_remote_before_effect`
- `test_human_supersede_unblocks_new_approval_after_sealed_sha_is_unreachable`
- `test_task_branch_supersede_requires_exact_confirmation_and_no_effects`
- Existing ordinary-forward test: `test_task_branch_start_replays_the_first_sealed_remote_tip`

### Fix

`xflow/cli.py` now reads the current `origin/<base>` tip, fetches that exact current ref into `FETCH_HEAD`, verifies the advertised/fetched identity, verifies the sealed SHA is reachable, and requires the sealed SHA to be an ancestor of the current remote tip. Ordinary forward advancement therefore still creates from the first sealed SHA; replacement, rewind, deletion or unreachable history fails before target-branch creation, with a second check immediately before `checkout -b`.

`xflow/approval.py` adds a persistent canonical `superseded` terminal state for an old `reserved` branch-start claim. The explicit CLI requires `--issue`, `--approval-id`, an auditable reason and exact confirmation phrase. It rejects wrong confirmation, non-reserved state, target branch presence locally or remotely, Devctl branch metadata, task activation/authority, history, or changed sealed task-state. Superseded claims remain on disk for audit and no longer shadow a fresh approval. Claim deletion is not a recovery protocol.

Human Approval Is Non-Delegable is stated in parser help, README and `help.txt`: AI must never run this transition or provide its confirmation phrase.

Files: `xflow/approval.py`, `xflow/cli.py`, `README.md`, `help.txt`, `tests/task-state.py`, `tests/entrypoint-routing.py`.

### GREEN

Force-push and unreachable-SHA cases fail before target branch creation. Wrong confirmation and pre-existing branch effects are rejected. The simulated human-retired claim remains persisted as `superseded`, after which a new approval starts from the replacement remote history. Ordinary forward advancement still starts from the first sealed SHA. Final full output: `task state ok` (exit 0).

## I3 - Canonical Branch-Start History

### RED

Command: `python tests\task-state.py` with `test_task_branch_completion_rejects_noncanonical_history_paths` registered.

Observed failure: cross-Issue, wrong-filename and arbitrary safe in-repository `historyFile` variants were accepted; the route reached `[INFO] ready` and could complete the claim.

### Fix

`complete_task_branch_start` recomputes the only valid `_history_path` from claim `approvalIssue`, action, canonical `recordedAt` and `approvalId`. Both the exact relative `historyFile` string and resolved path must match before any history write or completed transition.

Files: `xflow/approval.py`, `tests/task-state.py`.

### GREEN

All three redirected-path variants now fail; no redirected history is written and the claim remains non-completed. Final full output is included in `task state ok`.

## I4 - Stable Claim Lock Inode

### RED

Command: `python tests\approval-binding.py` and `python tests\task-state.py` after changing cleanup assertions to stable-lock reacquisition semantics.

Observed failure: the previous release path unlinked the lock, so the expected stable `claims.lock` inode was absent in both remote and branch scopes. That design permits POSIX waiter/new-opener inode divergence.

### Fix

`_approval_claim_lock` now uses one permanent `claims.lock` inode per git-common-dir/runtime-scope/worktree. Release only unlocks and closes it. `remote-approvals` and `task-branch-start` remain separate scopes while all transitions inside each scope serialize on one lock.

Tests now require successful release, same-process and cross-process reacquisition, and no temporary owner artifacts. A POSIX-only A/B/C regression holds A, queues B, releases A, then proves C cannot enter while B owns the original inode.

Files: `xflow/approval.py`, `tests/approval-binding.py`, `tests/task-state.py`.

### GREEN

On this Windows host, stable lock existence, release, repeat acquisition, cross-process acquisition and absence of temporary owner files all passed in both scopes. Final outputs: `approval binding ok` and `task state ok`.

The POSIX three-process case is present and registered but intentionally skips on Windows; it still requires execution in POSIX CI before claiming platform execution evidence.

## M1 - Trace Documentation

### RED

Commands: `python tests\entrypoint-routing.py` and `python tests\main_entrypoint.py` after adding documentation anchors.

Observed failures: README/help and the Skills trace reference lacked the sealed-authority recipe, non-authoritative explicit-input wording, and non-acceptance requirement.

### Fix

README, `help.txt`, CLI option help, and `xflow-skills/references/traceability.md` now state:

- Sealed acceptance history is authoritative and allows omission of `--contract`.
- Explicit `--contract` is only non-authoritative mechanical fail-closed evolution input.
- It cannot create or replace acceptance authority.
- Non-acceptance routes still require `--contract`.

Skills changes are limited to the existing trace reference and a `main_entrypoint.py` anchor; the main `SKILL.md` flow was not expanded.

Files: Devctl `README.md`, `help.txt`, `xflow/cli.py`, `tests/entrypoint-routing.py`; Skills `references/traceability.md`, `tests/main_entrypoint.py`.

### GREEN

Final outputs: `entrypoint routing ok`, `main entrypoint ok`, and `capability contract pressure scenarios ok` (all exit 0).

## Final Verification

All commands below ran against the final implementation content before commit:

| Repository | Command | Result | Wall time |
| --- | --- | --- | --- |
| Devctl | `python tests\approval-binding.py` | `approval binding ok`, exit 0 | 478.0 s |
| Devctl | `python tests\task-state.py` | `task state ok`, exit 0 | 359.7 s |
| Devctl | `python tests\contract-diff.py` | `contract diff ok`, exit 0 | 33.3 s |
| Devctl | `python tests\trace-core.py` | `trace core ok`, exit 0 | 516.0 s |
| Devctl | `python tests\python-core.py` | `python core ok`, exit 0 | 446.3 s |
| Devctl | `python tests\entrypoint-routing.py` | `entrypoint routing ok`, exit 0 | 30.3 s |
| Devctl | `git diff --check` | clean, exit 0 | 1.6 s |
| Skills | `python tests\main_entrypoint.py` | `main entrypoint ok`, exit 0 | 1.9 s |
| Skills | `python tests\pressure_scenarios.py` | `capability contract pressure scenarios ok`, exit 0 | 1.6 s |
| Skills | `git diff --check` | clean, exit 0 | 1.6 s |

The initial sandboxed `entrypoint-routing.py` attempt encountered the Git-for-Windows fixture error `sh.exe: couldn't create signal pipe, Win32 error 5`. The required rerun outside the restricted sandbox passed. This was an execution-environment failure, not a product RED.

`python-core.py` emitted the known fixture warning `remote HEAD refers to nonexistent ref, unable to checkout`; the script completed with exit 0. Its relevant fixtures explicitly create or select the required branches.

## Additional Regression Evidence

- Completed/consumed uniqueness: `test_consumed_record`, MR terminal-gate/unique subordinate-effect cases, completed branch-claim reuse rejection, and full `approval-binding.py`/`task-state.py` passed.
- Claim lock cleanup/reacquisition: remote and branch stable-lock checks passed on Windows, including cross-process acquisition; the POSIX three-process test is registered for POSIX execution.
- Ordinary Issue/comment/push/MR/merge behavior: full `approval-binding.py` and `python-core.py` passed, including issue comment exact-byte consumption, push/backfill, MR replay and PR merge identity checks.
- Task activation and Git start: full `task-state.py` passed, including ordinary activation, first capability branch start, forward remote advance, branch-created recovery and activation recovery.
- Contract diff and historical trace routes: full `contract-diff.py` and `trace-core.py` passed.

## Self-Review

- Re-read the complete production diffs and `final-review.md` after GREEN.
- Confirmed scope arbitration occurs before fresh MR body/review/provider logic and repeats under the scope lock.
- Confirmed no supersede path deletes claims or accepts a non-reserved/effected claim.
- Confirmed canonical history validation occurs before history write and before `completed`.
- Confirmed supplied contract snapshot participates in closure revalidation.
- Confirmed remote and branch claim lock scopes remain separate.
- Confirmed Skills did not change `SKILL.md` or widen its primary workflow.
- Confirmed only expected files were committed in each repository.

## Residual Risk

1. The POSIX A/B/C lock regression was added but not executed on this Windows host. POSIX CI must run `tests/approval-binding.py` to provide platform evidence for the inode-race scenario.
2. A remote base can change at any instant because Git servers provide no transaction spanning `ls-remote`, fetch and local branch creation. The implementation fails closed on advertised/fetched mismatch and validates containment twice, including immediately before target branch creation, which reduces the remaining race to the unavoidable external-ref change after the final observation.
3. Human branch-claim retirement intentionally relies on an exact, non-delegable human confirmation plus fail-closed checks of observable local/remote effects. It cannot establish facts about effects that an operator has deliberately erased outside the protocol; claims must therefore never be manually edited or deleted.

No other known residual correctness issue remains from C1/I1/I2/I3/I4/M1.
