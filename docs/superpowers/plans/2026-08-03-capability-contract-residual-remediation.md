# Capability Contract Residual Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the three remaining load-bearing gaps in historical contract tracing, merge-request recovery, and approved task-branch creation.

**Architecture:** Historical validation must derive its authority from immutable acceptance artifacts rather than the mutable current contract. Remote MR creation and task-branch creation must use durable state machines whose terminal state is reached only after required local effects are complete; replay must resume local effects without repeating a confirmed external effect. All exact-effect operations revalidate approved byte snapshots immediately before their irreversible boundary.

**Tech Stack:** Python 3 standard library, PyYAML, native Git for Windows, existing XFlow approval/task-state/traceability modules and script-style integration tests.

## Global Constraints

- Work only in the existing `feature/capability-contract-closure` isolated worktrees.
- Do not use WSL.
- Follow red-green-refactor: every production behavior change starts with a failing regression test whose failure is observed.
- Human approval remains non-delegable; no new bypass flag or implicit approval path may be introduced.
- Persist operational claims under the existing repository-local runtime/approval storage conventions; do not add tracked mutable runtime files.
- A provider-confirmed remote effect must never be repeated during replay.
- A historical Issue must remain auditable after the current contract becomes `active`, advances to a new version at the same path, moves, or is deleted.
- Do not push. Local merge is allowed only after all tests and the final whole-change review pass.

---

### Task 1: Build historical trace context from the sealed acceptance

**Files:**
- Modify: `xflow-devctl/xflow/traceability.py`
- Modify if a focused shared helper is required: `xflow-devctl/xflow/contracts.py`
- Test: `xflow-devctl/tests/trace-core.py`

**Interfaces:**
- Consumes: `approval.validate_contract_acceptance_history(..., return_snapshots=True)` and the sealed contract snapshot already archived by contract acceptance.
- Produces: a trace context whose `ContractDocument` and path/version/hash/object registry come from the sealed acceptance record, while mutable current-contract data is optional and non-authoritative for historical checks.

- [ ] **Step 1: Add failing historical trace regressions**

Add focused cases that first create and validate a `0.1.0` accepted-design contract and Issue trace, then independently:

```python
# Case A: lifecycle advance without semantic replacement.
current_contract["status"] = "active"

# Case B: same logical path now contains a later version.
current_contract["version"] = "0.2.0"
current_contract["status"] = "accepted-design"

# Case C: the mutable current contract file no longer exists.
contract_path.unlink()
```

In every case, `check_traceability(repo, issue, None, matrix_path)` for the old Issue must pass by validating the sealed accepted bytes. Add negative coverage proving a tampered acceptance snapshot or a matrix that differs from the accepted id/version/file still fails.

- [ ] **Step 2: Run the focused test and observe RED**

Run: `python tests/trace-core.py`

Expected: the new lifecycle/version/deletion cases fail because `_load_context` loads `state.contract_file` from the mutable working tree and compares the acceptance/matrix against it.

- [ ] **Step 3: Introduce one sealed-contract loader for historical acceptance**

After validating the acceptance history, locate exactly one supporting snapshot whose path and SHA match the record's archived contract snapshot fields. Decode those exact bytes with the existing contract parser and build the `ContractDocument` from that snapshot. Reject missing, duplicate, non-canonical, path-mismatched, hash-mismatched, or semantically incompatible snapshots.

For a `contract-acceptance` reference:

```text
historical authority = acceptance record + sealed contract snapshot
current contract file = optional evolution input only
matrix binding = accepted contract id/version/original file identity
```

Do not require the mutable file to exist or still have `accepted-design` status. Continue revalidating every sealed supporting snapshot at closure.

- [ ] **Step 4: Keep non-acceptance routes unchanged and run GREEN**

Run: `python tests/trace-core.py`

Expected: all trace tests pass, including tamper failures and the three historical evolution cases.

- [ ] **Step 5: Run the directly coupled suites and commit**

Run:

```powershell
python tests/contract-core.py
python tests/task-state.py
git diff --check
```

Commit only the Task 1 files with a scoped Chinese commit message.

---

### Task 2: Make MR local post-effects replayable after remote confirmation

**Files:**
- Modify: `xflow-devctl/xflow/approval.py`
- Modify: `xflow-devctl/xflow/cli.py`
- Test: `xflow-devctl/tests/approval-binding.py`
- Test: `xflow-devctl/tests/python-core.py`
- Modify if command semantics need clarification: `xflow-devctl/README.md`, `xflow-devctl/help.txt`

**Interfaces:**
- Consumes: existing remote claim, immutable approved body snapshot, provider receipt, and `confirm_remote_action`.
- Produces: a two-phase local completion contract for MR creation: provider confirmation is durable before local backfill, and terminal completion occurs only after PR metadata/state suggestion/current task/backfill accounting are applied idempotently.

- [ ] **Step 1: Add failing post-provider crash regressions**

Inject a failure after the provider result is durably confirmed but before `set_branch_meta(..., "pr", ...)`. Assert the first run calls the provider once and leaves a resumable non-terminal claim. Replay the exact approved command and assert:

```text
provider call count remains 1
branch pr/pr-url metadata is written
state update suggestion and current task backfill are present
backfill result is recorded once
approval history is published once
claim reaches completed only after all mandatory local effects
```

Add a second injection after part of the local metadata is already written to prove replay is idempotent. Preserve existing `outcome-unknown` reconciliation tests.

- [ ] **Step 2: Run focused suites and observe RED**

Run:

```powershell
python tests/approval-binding.py
python tests/python-core.py
```

Expected: replay is rejected as already consumed, or local MR metadata remains incomplete.

- [ ] **Step 3: Separate provider confirmation from terminal completion**

Use an explicit durable post-effect phase, or equivalent claim fields with the same semantics:

```text
reserved -> remote-confirmed/post-effects-pending -> completed
reserved -> outcome-unknown -> reconciled remote-confirmed/post-effects-pending
reserved -> retryable -> reserved
```

`begin_remote_action` must return the sealed provider receipt for the post-effect phase without calling the provider. MR creation applies idempotent local post-effects from that receipt, then invokes terminal completion. Other remote commands with no deferred local effects may still complete immediately through a clearly named helper.

- [ ] **Step 4: Make MR backfill effects idempotent and run GREEN**

Repeated writes must converge on the same PR number/URL and exact suggestion content. A conflicting existing PR identity must fail closed. A completed claim remains consumed after all local effects are known complete.

Run:

```powershell
python tests/approval-binding.py
python tests/python-core.py
python tests/entrypoint-routing.py
git diff --check
```

- [ ] **Step 5: Update operator-facing contract if needed and commit**

Document only externally relevant recovery behavior. Do not expose internal fault-injection hooks as user-facing API. Commit only the Task 2 files with a scoped Chinese commit message.

---

### Task 3: Add an exact-effect, crash-recoverable task-branch-start claim

**Files:**
- Modify: `xflow-devctl/xflow/approval.py`
- Modify: `xflow-devctl/xflow/cli.py`
- Modify if needed: `xflow-devctl/xflow/task_state.py`
- Test: `xflow-devctl/tests/task-state.py`
- Modify: `xflow-devctl/README.md`
- Modify: `xflow-devctl/help.txt`
- Modify if high-frequency guidance changes: `xflow-skills/SKILL.md`, `xflow-skills/references/devctl-contract.md`, `xflow-skills/templates/codex-agents.main.md`, `xflow-skills/templates/cursorrules.main`
- Test if skills change: `xflow-skills/tests/main_entrypoint.py`

**Interfaces:**
- Consumes: exact `task-state.md` bytes, exact `local-review.md` bytes, repository/worktree/base/target branch bindings, and the base commit selected after `pull --ff-only`.
- Produces: a persistent one-time branch-start reservation with replay-safe states and activation based on the approved task-state snapshot, never on a later mutable reread.

- [ ] **Step 1: Add failing exact-byte and crash-recovery tests**

Add tests that:

1. approve canonical task-state bytes, mutate those bytes after approval validation but before branch creation while preserving parsed branch/base values, and require failure before branch mutation;
2. mutate `local-review.md` over the same boundary and require failure;
3. inject a crash immediately after branch creation but before metadata/activation/consumption, then replay and require the existing exact target branch to resume rather than fail `branch already exists`;
4. inject a crash after activation but before terminal consumption and require replay to converge without a second branch or duplicate history;
5. reject an existing target branch that does not match the claim's exact expected base commit or branch identity.

- [ ] **Step 2: Run `python tests/task-state.py` and observe RED**

Expected: mutable bytes can be activated after the approval check, and a post-creation crash cannot resume.

- [ ] **Step 3: Persist a branch-start claim before Git mutation**

Capture and seal both approved files, bindings, target branch, base branch, and the post-pull base commit. Revalidate task-state and review snapshots after pull and immediately before branch creation. Use a durable state machine with equivalent semantics to:

```text
reserved -> branch-created -> activated -> completed
```

Transitions must be atomic under an approval-identity lock. `activate_task` must consume the sealed approved task-state bytes or a parsed object built from them; it must not reread a mutable task-state path for the activation decision.

- [ ] **Step 4: Implement fail-closed replay**

When the exact target branch already exists:

- resume only when the persistent claim exists;
- verify its commit ancestry/start point and exact branch/base/Issue bindings;
- restore or validate branch metadata idempotently;
- activate the approved snapshot and publish one approval history record;
- reject unrelated or conflicting pre-existing branches.

No implicit recovery is allowed without the exact claim and approval identity.

- [ ] **Step 5: Run focused and cross-repository GREEN suites**

Run in `xflow-devctl`:

```powershell
python tests/task-state.py
python tests/approval-binding.py
python tests/python-core.py
python tests/entrypoint-routing.py
git diff --check
```

If Skill guidance changed, run in `xflow-skills`:

```powershell
python tests/main_entrypoint.py
python tests/pressure_scenarios.py
git diff --check
```

- [ ] **Step 6: Commit Task 3 changes**

Commit each repository independently with scoped Chinese commit messages. Do not push.

---

### Task 4: Whole-change verification and review

**Files:**
- Create in this plan's ignored SDD workspace: task briefs, review reports, final review package, and final review report.
- Modify only if review findings require one bounded final fix wave: files named by the finding.

**Interfaces:**
- Consumes: Tasks 1-3 commits and this plan's SDD ledger.
- Produces: full test evidence, a fresh whole-change review, and either a clean local integration candidate or an explicit blocked finding.

- [ ] **Step 1: Run the complete devctl suite**

Run every script below with native Windows Python:

```powershell
python tests/bindings-core.py
python tests/task-state.py
python tests/approval-binding.py
python tests/project-config.py
python tests/classification-core.py
python tests/contract-core.py
python tests/contract-diff.py
python tests/trace-core.py
python tests/python-core.py
python tests/entrypoint-routing.py
git diff --check
```

- [ ] **Step 2: Run the complete skills suite**

```powershell
python tests/main_entrypoint.py
python tests/pressure_scenarios.py
git diff --check
```

- [ ] **Step 3: Dispatch a fresh whole-change reviewer**

Review from skills base `14be33d6a5044ce4aa61fc294139ab8278c95dca` and devctl base `00720f2c9ae43b7e989da4af283569af9ce50da8` through the new heads. The reviewer must explicitly audit the three original failure scenarios, exact-byte authority, provider non-repetition, replay idempotence, lock/state transition safety, and missing negative tests.

- [ ] **Step 4: Apply at most one bounded final fix wave and re-review**

If findings remain, fix only those findings with new failing regressions first, rerun all affected suites, and dispatch one scoped re-review. A residual load-bearing finding blocks integration.

- [ ] **Step 5: Finish locally without pushing**

When review is clean and both worktrees are clean, prepare the local-main merge using the existing feature branch history. Do not push; the user will push manually.
