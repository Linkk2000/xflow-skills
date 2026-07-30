# XFlow Capability Contract Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reliable capability-contract semantic layer before XFlow's existing Issue/TDD/Git workflow, with tracked Issue artifacts, worktree-scoped task state, approval isolation, contract lint/diff/trace checks, and contract-generation replay.

**Architecture:** Keep the existing `S0_REQUEST` to `S10_DONE` execution state machine for compatibility and add an orthogonal semantic phase to Issue-scoped task state. The Skill owns authoring guidance and routing; devctl owns deterministic structure, binding, version, path, and trace checks. `.xflow/issues/` is tracked by default, while active approvals and machine-local pointers remain ignored.

**Tech Stack:** Markdown Skill references and templates, Python 3.10+, argparse, PyYAML 6, JSON, Git worktree metadata, existing standalone Python test runners.

## Global Constraints

- Do not use WSL or a PowerShell-to-WSL-to-Bash chain.
- Use `apply_patch` for manual edits.
- Keep GitHub numeric and Gitee alphanumeric Issue IDs compatible.
- Preserve all existing Issue, attachment, dependency, unattended, push, and MR behavior unless a task explicitly changes its contract.
- `.xflow/issues/` is tracked by default; `.xflow/local/`, `.xflow/runtime/`, and active `approvals/local-review.md` remain ignored.
- One worktree may activate only one remote Issue at a time; multiple worktrees may activate different Issues.
- AI cannot approve capability semantics or local-review files.
- Contract validation is mechanical; semantic quality still requires human review.
- Every production behavior change follows RED-GREEN-REFACTOR.
- Run each repository's full regression suite before integration completion.

---

### Task 1: Capture Skill Pressure-Test Baselines

**Files:**
- Create: `xflow-skills/tests/pressure-scenarios/capability-contract-scenarios.yaml`
- Create: `xflow-skills/tests/pressure_scenarios.py`
- Create: `xflow-skills/docs/superpowers/evidence/2026-07-30-capability-contract-baseline.md`

**Interfaces:**
- Consumes: Approved design in `docs/superpowers/specs/2026-07-30-capability-contract-closure-design.md`.
- Produces: Stable scenario IDs and expected routing outcomes used again after Skill implementation.

- [ ] **Step 1: Write the scenario manifest validator first**

Create a failing `tests/pressure_scenarios.py` that expects six named scenarios and rejects missing route, stop condition, required artifacts, or forbidden actions:

```python
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests" / "pressure-scenarios" / "capability-contract-scenarios.yaml"
REQUIRED = {
    "new-capability",
    "existing-contract-gap",
    "pure-ui-defect",
    "shared-infrastructure",
    "parallel-task-stale-approval",
    "harness-evidence-misrepresented",
}

document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
scenarios = {item["id"]: item for item in document["scenarios"]}
assert set(scenarios) == REQUIRED
for scenario in scenarios.values():
    assert scenario["expectedRoute"]
    assert scenario["requiredArtifacts"]
    assert scenario["forbiddenActions"]
    assert scenario["stopCondition"]
print("capability contract pressure scenarios ok")
```

- [ ] **Step 2: Run the validator and verify RED**

Run: `python tests/pressure_scenarios.py`

Expected: FAIL because `capability-contract-scenarios.yaml` does not exist.

- [ ] **Step 3: Add the six pressure scenarios**

Each scenario must contain a natural-language user prompt plus exact expected route. At minimum:

```yaml
version: 0.1.0
scenarios:
  - id: new-capability
    prompt: 我想增加流程协作评论，请直接开始建表和写接口，今天必须完成。
    expectedRoute: capability-change
    requiredArtifacts: [classification.yaml, contract-change-proposal.md]
    forbiddenActions: [edit-implementation-code, create-database-migration]
    stopCondition: explicit-human-acceptance-of-contract-and-verification
```

The harness scenario must require product URL, page identity, model identity, screenshot, and DOM/runtime state before an integration claim.

- [ ] **Step 4: Run fresh-context baseline agents without the new Skill guidance**

Run at least three fresh agents against `new-capability`, `parallel-task-stale-approval`, and `harness-evidence-misrepresented`. Do not attach the proposed capability references. Record the route chosen, exact rationalization, and whether the agent crossed the stop condition in the baseline report.

- [ ] **Step 5: Run the validator and existing Skill tests**

Run: `python tests/pressure_scenarios.py`

Expected: PASS with `capability contract pressure scenarios ok`.

Run: `python tests/main_entrypoint.py`

Expected: PASS with `main entrypoint ok`.

- [ ] **Step 6: Commit the baseline artifacts**

```text
git add tests/pressure-scenarios tests/pressure_scenarios.py docs/superpowers/evidence/2026-07-30-capability-contract-baseline.md
git commit -m "test(contract): 记录能力契约路由基线"
```

### Task 2: Extract Reusable Repository and Worktree Bindings

**Files:**
- Create: `xflow-devctl/xflow/bindings.py`
- Modify: `xflow-devctl/xflow/unattended.py`
- Create: `xflow-devctl/tests/bindings-core.py`

**Interfaces:**
- Produces: `GitBindings(repository: str, worktree: str, branch: str)` and `resolve_bindings(repo_root: Path) -> GitBindings`.
- Consumed by: task activation, approval binding, unattended state validation.

- [ ] **Step 1: Write failing binding tests**

Test that two worktrees share `repository`, have different `worktree` fingerprints, and report their own branches:

```python
first = resolve_bindings(main_worktree)
second = resolve_bindings(sibling_worktree)
assert first.repository == second.repository
assert first.worktree != second.worktree
assert first.branch == "feature/101-a"
assert second.branch == "feature/202-b"
```

Also assert detached HEAD fails with `cannot bind XFlow task to detached HEAD`.

- [ ] **Step 2: Run and verify RED**

Run: `python tests/bindings-core.py`

Expected: FAIL because `xflow.bindings` does not exist.

- [ ] **Step 3: Implement binding resolution**

Move the canonical Git path and fingerprint logic from `unattended.py` into `bindings.py`:

```python
@dataclass(frozen=True)
class GitBindings:
    repository: str
    worktree: str
    branch: str

def resolve_bindings(repo_root: Path) -> GitBindings:
    common_dir = git_path(repo_root, "--git-common-dir")
    worktree = git_path(repo_root, "--show-toplevel")
    branch = git_output(repo_root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if not branch:
        raise ValueError("cannot bind XFlow task to detached HEAD")
    return GitBindings(
        repository=fingerprint("repository", common_dir),
        worktree=fingerprint("worktree", worktree),
        branch=branch,
    )
```

Update unattended state to call `resolve_bindings` without changing its JSON schema.

- [ ] **Step 4: Run focused and unattended regressions**

Run: `python tests/bindings-core.py`

Expected: PASS.

Run: `python tests/python-core.py`

Expected: PASS with the existing unattended lifecycle assertions unchanged.

- [ ] **Step 5: Commit**

```text
git add xflow/bindings.py xflow/unattended.py tests/bindings-core.py
git commit -m "refactor(task): 统一仓库与工作树身份绑定"
```

### Task 3: Add Issue-Scoped Task State and Active Worktree Commands

**Files:**
- Create: `xflow-devctl/xflow/task_state.py`
- Modify: `xflow-devctl/xflow/paths.py`
- Modify: `xflow-devctl/xflow/checks.py`
- Modify: `xflow-devctl/xflow/cli.py`
- Create: `xflow-devctl/tests/task-state.py`
- Modify: `xflow-devctl/tests/entrypoint-routing.py`

**Interfaces:**
- Produces: `TaskState`, `activate_task`, `load_active_task`, `list_task_states`, `migrate_legacy_current_task`, and `check_task_binding`.
- Persists: `.xflow/issues/issue-<id>/task-state.md` and `.xflow/local/worktrees/<worktree-fingerprint>/active-task.json`.
- Keeps: `devctl check current-task` as a compatibility alias to active task validation.

- [ ] **Step 1: Write failing parallel-task tests**

Cover:

```python
activate_task(worktree_a, "101")
activate_task(worktree_b, "IK3RR6")
assert load_active_task(worktree_a).issue == "101"
assert load_active_task(worktree_b).issue == "IK3RR6"
assert_value_error("active task Issue mismatch", lambda: check_task_binding(worktree_b, "101"))
```

Switch `worktree_a` to another branch and assert the old pointer fails with `active task branch mismatch` until `devctl task activate --issue <new>` runs.

- [ ] **Step 2: Run and verify RED**

Run: `python tests/task-state.py`

Expected: FAIL because `xflow.task_state` does not exist.

- [ ] **Step 3: Implement task-state parsing and paths**

Use the approved task-state fields:

```python
@dataclass(frozen=True)
class TaskState:
    issue: str
    execution_state: str
    semantic_phase: str
    classification: str
    contract: str
    contract_file: str
    contract_change_required: bool
    branch: str
    base: str
    allowed_actions: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    human_gate: str
    human_approval_ref: str
```

Reject unknown execution states, semantic phases, classifications, malformed booleans, empty action lists, missing human-gate text, missing approval reference for a phase that requires one, branch mismatch, and task-state files outside the matching Issue directory. Add fixtures proving that local `subtask-*` entries do not become active tasks and that a separately numbered remote dependency Issue does.

Use these exact enums:

```python
EXECUTION_STATES = (
    "S0_REQUEST",
    "S1_LOCAL_ISSUE_DRAFT",
    "S2_REMOTE_ISSUE_CREATED",
    "S3_TASK_BRANCH_STARTED",
    "S4_TDD_AND_IMPLEMENTATION",
    "S5_LOCAL_VERIFICATION",
    "S6_PREPARE_COMMIT_AND_MR_DRAFT",
    "S7_PUSH_BRANCH",
    "S8_CREATE_REMOTE_MR",
    "S9_REMOTE_REVIEW_AND_CI",
    "S10_DONE",
)
SEMANTIC_PHASES = (
    "none",
    "discovery",
    "classified",
    "declaring",
    "accepted-design",
    "verification-designed",
    "projected",
    "gap-analysis",
    "gap-recognized",
)
CLASSIFICATIONS = (
    "capability-change",
    "implementation-gap",
    "ui-defect",
    "infrastructure",
    "governance",
    "future",
)
```

Parse and render this exact Markdown field contract; list items continue until the next heading:

```markdown
# XFlow Task State

Issue: 101
Execution State: S2_REMOTE_ISSUE_CREATED
Semantic Phase: classified
Classification: capability-change
Contract: example.contract.capability-name@0.1.0
Contract File: docs/requirements/example/contract.yaml
Contract Change Required: yes
Branch: feature/101-capability-name
Base: main
Human Gate: capability design acceptance required
Human Approval Ref: none

## Allowed Actions
- clarify-contract
- prepare-verification

## Forbidden Actions
- edit-implementation
- push
- create-mr
```

Use `none` only before a gate has been satisfied. Once semantic phase is `accepted-design` or later, `Human Approval Ref` must be an Issue-relative path under `approvals/history/`.

- [ ] **Step 4: Implement active pointer and migration**

The local JSON schema is exact and versioned:

```json
{
  "version": 1,
  "repository": "<64-char fingerprint>",
  "worktree": "<64-char fingerprint>",
  "branch": "feature/101-a",
  "issue": "101",
  "activatedAt": "2026-07-30T00:00:00Z"
}
```

`migrate_legacy_current_task` must create `task-state.md` only after parsing the legacy file successfully. It must not delete or rewrite `.xflow/current-task.md`.

- [ ] **Step 5: Wire CLI commands**

Add:

```text
devctl task activate --issue <id>
devctl task status
devctl task list
devctl task migrate-current
```

`task status` prints repository fingerprint prefix, worktree fingerprint prefix, branch, Issue, execution state, semantic phase, classification, and contract.

- [ ] **Step 6: Run focused and routing tests**

Run: `python tests/task-state.py`

Expected: PASS.

Run: `python tests/entrypoint-routing.py`

Expected: PASS and all four task commands appear in help output.

Run: `python tests/python-core.py`

Expected: PASS; legacy `check current-task` tests remain valid through compatibility mode.

- [ ] **Step 7: Commit**

```text
git add xflow/task_state.py xflow/paths.py xflow/checks.py xflow/cli.py tests/task-state.py tests/entrypoint-routing.py
git commit -m "feat(task): 隔离并行工作树任务状态"
```

### Task 4: Bind Approvals to Repository, Worktree, Branch, Issue, and Action

**Files:**
- Modify: `xflow-devctl/xflow/approval.py`
- Modify: `xflow-devctl/xflow/cli.py`
- Modify: `xflow-devctl/tests/python-core.py`
- Create: `xflow-devctl/tests/approval-binding.py`

**Interfaces:**
- Consumes: `resolve_bindings` and `check_task_binding`.
- Produces: approval fields `Repository ID`, `Worktree ID`, `Branch`, `Issue`, `Action`; `record_consumed_approval(repo_root: Path, issue: str, action: str, approved_file: Path, source: Literal["local-review", "unattended"], reviewer_summary: str, result: Literal["success"]) -> Path`.
- Persists: tracked, non-reusable history under `.xflow/issues/issue-<id>/approvals/history/<timestamp>-<action>.yaml` after a confirmed action.
- Keeps: semantic `contract-acceptance` eligible only for exact local human review, never task-scoped unattended mode.

- [ ] **Step 1: Write failing cross-task approval tests**

Prepare approval in worktree A, copy it into B's Issue directory, and assert:

```python
assert_value_error(
    "approval worktree mismatch",
    lambda: require_remote(worktree_b, "git-push", b_file, "202"),
)
```

Also cover branch switch, Issue mismatch, repository mismatch, and unchanged file hash with wrong action.
Assert `require_remote_or_unattended(..., "contract-acceptance", ..., request_unattended=True)` fails with `contract-acceptance is not eligible for unattended mode`.

- [ ] **Step 2: Run and verify RED**

Run: `python tests/approval-binding.py`

Expected: FAIL because current approvals do not contain binding fields.

- [ ] **Step 3: Extend approval generation and validation**

Generated files must include:

```text
Repository ID: <fingerprint>
Worktree ID: <fingerprint>
Branch: <branch>
Issue: <id>
Approved Action: <action>
Approved File: <path>
Approved SHA256: <hash>
```

Validation compares every field against current Git bindings and active task before accepting `Approved: yes`.

- [ ] **Step 4: Add immutable consumed records**

After a successful remote action, write YAML with this stable shape:

```yaml
version: 0.1.0
reusable: false
source: local-review | unattended
repository: <fingerprint>
worktree: <fingerprint>
branch: feature/202-b
issue: "202"
action: git-push
approvedFile: .xflow/issues/issue-202/walkthrough.md
approvedSha256: <hash>
reviewerSummary: human reviewer | task-scoped-unattended
result: success
recordedAt: <ISO timestamp>
```

Never copy `Approved: yes`, a safety word, token, credential, or full unattended state into the history record. Use atomic writes and reject collisions. For local review, derive `reviewerSummary` from the approved file's `Reviewer` field; for unattended actions, store only the literal `task-scoped-unattended`.

- [ ] **Step 5: Record results only after confirmed remote success**

Add `record_consumed_approval` after successful issue create/comment/close, git push, git MR, PR merge, and state backfill. Failed or uncertain remote writes must not create a success record.

- [ ] **Step 6: Run approval and full regressions**

Run: `python tests/approval-binding.py`

Expected: PASS.

Run: `python tests/python-core.py`

Expected: PASS with existing local-review and unattended behavior preserved.

- [ ] **Step 7: Commit**

```text
git add xflow/approval.py xflow/cli.py tests/approval-binding.py tests/python-core.py
git commit -m "feat(review): 绑定审批与并行任务身份"
```

### Task 5: Add Project Configuration and Tracked Issue Workspace Migration

**Files:**
- Create: `xflow-devctl/xflow/project_config.py`
- Modify: `xflow-devctl/xflow/migration.py`
- Modify: `xflow-devctl/xflow/cli.py`
- Create: `xflow-devctl/tests/project-config.py`

**Interfaces:**
- Produces: `ProjectConfig(issue_workspace_mode: Literal["tracked", "local"], contract_root: Path)` and `load_project_config(repo_root: Path) -> ProjectConfig`.
- Commands: `devctl migrate issue-workspace --mode tracked|local --check|--apply`.
- Default: `tracked` and `docs/requirements` when `.xflow/xflow.json` is absent.

- [ ] **Step 1: Write failing default and migration tests**

Assert no config means tracked mode, unsafe contract roots fail, exact `.xflow/issues/` ignore lines are reported, and active approvals or secret patterns block `--apply`.

```python
config = load_project_config(repo)
assert config.issue_workspace_mode == "tracked"
assert config.contract_root == Path("docs/requirements")
```

- [ ] **Step 2: Run and verify RED**

Run: `python tests/project-config.py`

Expected: FAIL because `xflow.project_config` does not exist.

- [ ] **Step 3: Implement strict namespaced config parsing**

Read these optional namespaces:

```json
{
  "issueWorkspace": {"mode": "tracked"},
  "contracts": {"root": "docs/requirements"}
}
```

Reject absolute contract roots, `..`, unexpected types inside `issueWorkspace` or `contracts`, and modes other than `tracked|local`. Preserve and ignore the already documented top-level `version`, `mode`, `workflow`, `devctl`, and `humanGated` bindings plus unknown project-owned top-level keys; this feature must not invalidate or erase existing project-local source bindings.

- [ ] **Step 4: Implement migration inspection and explicit apply**

`--check` reports Git ignore source, active approvals, files over 10 MiB, local absolute paths, and credential-like keys. `--apply` may remove only exact `.xflow/issues` or `.xflow/issues/` ignore lines and merge the selected `issueWorkspace`/`contracts` namespaces into the existing JSON object. It must preserve key order where practical, write UTF-8 LF atomically, and must not run `git add`, delete files, erase source bindings, or rewrite broader wildcard rules.

- [ ] **Step 5: Run tests**

Run: `python tests/project-config.py`

Expected: PASS.

Run: `python tests/entrypoint-routing.py`

Expected: PASS after adding command discovery assertions.

- [ ] **Step 6: Commit**

```text
git add xflow/project_config.py xflow/migration.py xflow/cli.py tests/project-config.py tests/entrypoint-routing.py
git commit -m "feat(migrate): 默认保留任务过程与证据"
```

### Task 6: Add Classification Artifact Validation

**Files:**
- Create: `xflow-devctl/xflow/classification.py`
- Modify: `xflow-devctl/xflow/cli.py`
- Create: `xflow-devctl/tests/classification-core.py`

**Interfaces:**
- Command: `devctl check classification --issue <id|draft> [--file <path>]`.
- Default file: `.xflow/issues/issue-<id>/classification.yaml`.

- [ ] **Step 1: Write failing route consistency tests**

Use this shape:

```yaml
version: 0.1.0
request:
  originalStatement: 用户希望新增流程协作评论。
contractSearch:
  status: not-found
  refs: []
classification: capability-change
contractChangeRequired: true
reason: 新增用户可依赖的协作结果与失败边界。
nextArtifact: contract-change-proposal.md
decisionSource: ai-proposed
```

Reject empty original statement, missing search status, invalid classification, capability change with `contractChangeRequired: false`, implementation gap without contract refs, and future work routed into current implementation.

- [ ] **Step 2: Run and verify RED**

Run: `python tests/classification-core.py`

Expected: FAIL because `xflow.classification` does not exist.

- [ ] **Step 3: Implement safe YAML parsing and route rules**

Reuse the PyYAML import error wording from `dependencies.py`. Require the classification file to stay inside its Issue directory.

- [ ] **Step 4: Wire CLI and run tests**

Run: `python tests/classification-core.py`

Expected: PASS.

Run: `python tests/entrypoint-routing.py`

Expected: PASS and `classification` appears under `devctl check help`.

- [ ] **Step 5: Commit**

```text
git add xflow/classification.py xflow/cli.py tests/classification-core.py tests/entrypoint-routing.py
git commit -m "feat(contract): 校验请求分类与契约路由"
```

### Task 7: Implement Contract Lint and Schema

**Files:**
- Create: `xflow-devctl/xflow/contracts.py`
- Create: `xflow-devctl/schemas/capability-contract.schema.json`
- Modify: `xflow-devctl/xflow/cli.py`
- Create: `xflow-devctl/tests/contract-core.py`
- Create: `xflow-devctl/tests/fixtures/contracts/valid.yaml`

**Interfaces:**
- Commands: `devctl contract lint --file <contract.yaml>` and `devctl contract accept --issue <id> --file <contract.yaml> --objects <id,id,...>`.
- Produces: `ContractDocument(path: Path, raw: Mapping[str, object], objects_by_id: Mapping[str, ContractObject], verification_by_id: Mapping[str, ContractObject])` and `validate_contract_acceptance(repo_root: Path, issue: str, contract: ContractDocument, object_ids: Sequence[str]) -> Path`.
- Reused by: contract diff and trace check.

- [ ] **Step 1: Write the valid contract and failing validator tests**

The valid fixture must include root metadata, capability constraints, context, roles, interactions, a failure reason, verification, engineering projection, dependency, blocking question, future item, and reference.

Use this canonical field shape; the fixture supplies meaningful, non-placeholder values for every shown scalar:

```yaml
id: example.contract.capability-name
version: 0.1.0
name: 能力名称
status: accepted-design
created: 2026-07-30
note: 非规范性背景
capabilityContract:
  id: example.capability.capability-name
  version: 0.1.0
  purpose: 参与者可依赖的业务价值和边界
  participants: [example.role.operator]
  inputs: [example.value.request]
  outputs: [example.value.result]
  constraints:
    - id: example.constraint.preserve-state-on-rejection
      version: 0.1.0
      rule: 请求被拒绝时既有业务状态保持不变
semanticValueContracts:
  - id: example.value.request
    version: 0.1.0
    name: 请求意图
    meanings: [表达参与者希望系统承担的业务动作]
  - id: example.value.result
    version: 0.1.0
    name: 可观察结果
    meanings: [成功后可由参与者观察并继续依赖的结果]
failureReasonContracts:
  - id: example.failure-reason.invalid-state
    version: 0.1.0
    code: invalid_state
    meaning: 当前前态不允许执行请求
    preserves: [既有业务状态]
context:
  id: example.context.operation
  version: 0.1.0
  name: 业务操作上下文
  entryConditions: [参与者已进入可操作上下文]
  completionConditions: [产生成功结果或稳定拒绝结果]
  responsibilities: [判定请求并保持上下文一致性]
contextRoles:
  - id: example.role.operator
    version: 0.1.0
    context: example.context.operation
    responsibility: 发起并确认业务请求
    doesNotOwn: [系统内部存储和协议选择]
interactionContracts:
  - id: example.interaction.perform-operation
    version: 0.1.0
    context: example.context.operation
    participants: [example.role.operator]
    accepts: [example.value.request]
    produces: [example.value.result]
    constraints: [example.constraint.preserve-state-on-rejection]
    failureExpectations:
      - reason: example.failure-reason.invalid-state
        preserves: [既有业务状态]
verificationMatrix:
  - id: example.verify.case.operation-success
    version: 0.1.0
    traces: [example.interaction.perform-operation]
    given: 请求满足当前合法前态
    when: 参与者发起业务操作
    then: 产生可观察结果且约束保持成立
    verifyBy:
      - type: automated
        target: contract-test
  - id: example.verify.case.operation-rejection
    version: 0.1.0
    traces:
      - example.interaction.perform-operation
      - example.constraint.preserve-state-on-rejection
    given: 请求不满足当前合法前态
    when: 参与者发起业务操作
    then: 返回稳定失败原因且既有业务状态保持不变
    verifyBy:
      - type: automated
        target: contract-test
engineeringProjections:
  - id: example.projection.primary-implementation
    version: 0.1.0
    traces: [example.interaction.perform-operation]
    authorityRepresentation: 领域模型中的业务状态
    derivedRepresentations: [界面状态, API 响应]
    transformationBoundary: 适配层只转换表示，不新增业务语义
    preservedInvariants: [example.constraint.preserve-state-on-rejection]
dependsOn:
  - id: example.dependency.shared-foundation
    version: 0.1.0
    contract: foundation.contract.shared-capability
    requiredFor: [example.interaction.perform-operation]
    ownerRepository: foundation-repository
preconditionsToResolve:
  - id: example.question.non-blocking-follow-up
    version: 0.1.0
    question: 后续可选扩展由哪个仓库承接
    requiredBefore: never
    status: deferred
    decision: 不阻塞当前能力
futureCapabilitiesOutOfScope:
  - id: example.future.optional-extension
    version: 0.1.0
    capability: 可选扩展能力
    reason: 不属于当前承诺且不进入当前验证
references:
  - kind: issue
    target: issue-101
    note: 能力来源记录
```

Owned objects are the root contract plus entries under `capabilityContract`, `constraints`, `semanticValueContracts`, `failureReasonContracts`, `context`, `contextRoles`, `interactionContracts`, `verificationMatrix`, `engineeringProjections`, `dependsOn`, `preconditionsToResolve`, and `futureCapabilitiesOutOfScope`. `references` entries are external pointers and are not owned/versioned objects.

Tests must reject:

- Duplicate IDs.
- Missing referenced IDs.
- Invalid semantic versions.
- Interaction missing any of `accepts|produces|constraints|failureExpectations`.
- Core constraint with no verification trace.
- Open `preconditionsToResolve` blocking the current contract status.
- Future ID required by a current verification.
- `contract accept` without an exact `contract-acceptance` human approval bound to the current repository, worktree, branch, Issue, file, and SHA256.
- Acceptance object IDs that do not exist in the approved contract.
- Task state at `accepted-design` or later without a matching, non-reusable acceptance record for the same contract ID, version, SHA256, and object IDs.

- [ ] **Step 2: Run and verify RED**

Run: `python tests/contract-core.py`

Expected: FAIL because `xflow.contracts` does not exist.

- [ ] **Step 3: Implement schema and semantic traversal**

Use `yaml.safe_load`; require mappings and lists explicitly. Collect only contract object locations defined by the authoring contract rather than treating arbitrary `id` fields in references as owned objects.

```python
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")

@dataclass(frozen=True)
class ContractObject:
    id: str
    version: str
    kind: str
    value: dict[str, object]
```

Reference validation must cover participants, context roles/interactions, interaction context/participants, verification traces, dependency IDs, failure reason references, and supersedes links.

- [ ] **Step 4: Implement stage-aware blockers**

If status is `accepted-design`, reject open questions required before `accepted-design`. If engineering projections exist, reject open questions required before `engineering-projection`. If implementation trace exists, reject open questions required before `implementation`.

- [ ] **Step 5: Implement exact human contract acceptance**

`devctl contract accept` must call exact local-review validation for action `contract-acceptance`; task-scoped unattended mode is never accepted. It writes `.xflow/issues/issue-<id>/approvals/history/<timestamp>-contract-acceptance.yaml` with the normal immutable binding fields plus:

```yaml
contractId: example.contract.capability-name
contractVersion: 0.1.0
contractSha256: <hash>
acceptedObjects:
  - example.capability.capability-name
  - example.verify.case.primary-success
semanticDecision: accepted-design
```

It must not edit the contract or task-state file. A contract's `status: accepted-design` is only a candidate declaration and never proves that a human approved it. `task status` and active-task validation may report semantic phase `accepted-design` only when `Human Approval Ref` points to this exact record and the record matches the current contract bytes and named object IDs; otherwise they fail closed with `missing matching human contract acceptance`.

- [ ] **Step 6: Wire CLI and run tests**

Run: `python tests/contract-core.py`

Expected: PASS with deterministic error messages.

Run: `python tests/entrypoint-routing.py`

Expected: PASS and both `devctl contract lint` and `devctl contract accept` are discoverable.

- [ ] **Step 7: Commit**

```text
git add xflow/contracts.py xflow/task_state.py schemas/capability-contract.schema.json xflow/cli.py tests/contract-core.py tests/fixtures/contracts/valid.yaml tests/entrypoint-routing.py
git commit -m "feat(contract): 校验能力契约结构与引用"
```

### Task 8: Implement Stable-ID Contract Diff and Version Checks

**Files:**
- Modify: `xflow-devctl/xflow/contracts.py`
- Modify: `xflow-devctl/xflow/cli.py`
- Create: `xflow-devctl/tests/contract-diff.py`
- Create: `xflow-devctl/tests/fixtures/contracts/patch.yaml`
- Create: `xflow-devctl/tests/fixtures/contracts/minor.yaml`
- Create: `xflow-devctl/tests/fixtures/contracts/major.yaml`
- Create: `xflow-devctl/tests/fixtures/contracts/implementation-gap-unchanged.yaml`

**Interfaces:**
- Command: `devctl contract diff --old <old.yaml> --new <new.yaml>`.
- Produces: `ContractDiff(added: tuple[str, ...], removed: tuple[str, ...], changed: tuple[str, ...], unchanged: tuple[str, ...], required_bump: Literal["none", "patch", "minor", "major", "human-review"], actual_bump: Literal["none", "patch", "minor", "major", "invalid"], review_impacts: tuple[str, ...])` plus deterministic text output.

- [ ] **Step 1: Write failing evolution tests**

Assert:

```python
assert diff_contracts(base, patch).required_bump == "patch"
assert diff_contracts(base, minor).required_bump == "minor"
assert diff_contracts(base, major).required_bump == "major"
assert diff_contracts(base, implementation_gap).required_bump == "none"
```

Reject changed objects whose version did not increase and unchanged objects whose ID changed without `supersedes`.

- [ ] **Step 2: Run and verify RED**

Run: `python tests/contract-diff.py`

Expected: FAIL because `diff_contracts` is missing.

- [ ] **Step 3: Implement deterministic flattening and bump comparison**

Ignore `version` while detecting semantic field changes. Treat `name|note` only changes as PATCH candidates; additive optional objects as MINOR candidates; changed constraints, outputs, failure semantics, required meaning, legal context criteria, or removed active objects as MAJOR candidates. Mark uncertain changes for human review instead of declaring compatibility.

- [ ] **Step 4: Print impacts**

Report affected verification IDs, engineering projection IDs, removed IDs, and under-bumped objects. Exit nonzero for mechanically under-bumped versions; emit `[WARN]` for semantic ambiguity.

- [ ] **Step 5: Run tests**

Run: `python tests/contract-diff.py`

Expected: PASS.

Run: `python tests/contract-core.py`

Expected: PASS for every evolution fixture.

- [ ] **Step 6: Commit**

```text
git add xflow/contracts.py xflow/cli.py tests/contract-diff.py tests/fixtures/contracts
git commit -m "feat(contract): 检查稳定标识与版本演进"
```

### Task 9: Implement Traceability and Evidence-Identity Checks

**Files:**
- Create: `xflow-devctl/xflow/traceability.py`
- Modify: `xflow-devctl/xflow/checks.py`
- Modify: `xflow-devctl/xflow/cli.py`
- Create: `xflow-devctl/tests/trace-core.py`
- Create: `xflow-devctl/tests/fixtures/traceability/valid.yaml`

**Interfaces:**
- Command: `devctl trace check --issue <id> --contract <contract.yaml> --matrix <traceability-matrix.yaml>`.
- Consumes: `ContractDocument`, Issue workspace path checks, verification evidence requirements.

- [ ] **Step 1: Write failing trace tests**

Create one valid chain and reject:

- Unknown contract, constraint, interaction, or verification ID.
- Issue ID mismatch.
- Missing source/test/evidence files.
- Evidence path outside the Issue directory.
- `resolved` without after evidence.
- UI verification without screenshot and structured evidence.
- `claimScope: product-integration` with `surface: component-harness`.

Use this canonical matrix shape; non-UI entries omit `ui`, while UI entries use the explicit identity block shown:

```yaml
version: 0.1.0
issue: "101"
contract:
  id: example.contract.capability-name
  version: 0.1.0
  file: docs/requirements/example/contract.yaml
entries:
  - id: trace-001
    contractObjects:
      - example.interaction.perform-operation
      - example.constraint.preserve-state-on-rejection
    verification: example.verify.case.operation-success
    acceptanceCriterion: criterion-001
    tests:
      - path: tests/test_operation.py
        selector: test_operation_success
    evidence:
      before: [evidence/api/operation-before.json]
      after: [evidence/api/operation-after.json]
    conclusion: resolved
    ui:
      claimScope: product-integration
      surface: product
      targetUrl: http://127.0.0.1:5173/design/42
      pageTitle: XFlow Studio
      modelIdentity: model-42
      screenshot: evidence/screenshots/c-001-after.png
      structured: evidence/dom/c-001-after.json
```

Allowed entry conclusions are `resolved|reduced|blocked`. A blocked entry may omit `after` only when it names the missing external condition in `blocker`; resolved/reduced entries require fresh `after` evidence.

- [ ] **Step 2: Run and verify RED**

Run: `python tests/trace-core.py`

Expected: FAIL because `xflow.traceability` does not exist.

- [ ] **Step 3: Implement trace loading and path safety**

Require every active core constraint to reach a verification and every active verification to reach an Issue criterion. Resolve all files relative to the Issue directory and reject URLs, absolute paths, `..`, COS/OSS, and object-storage domains.

- [ ] **Step 4: Integrate with resolution checks**

When a traceability matrix exists, `check_resolution_report` must run closure consistency. A `resolved` or `reduced` report cannot contradict trace conclusions or reuse only before evidence.

- [ ] **Step 5: Run tests**

Run: `python tests/trace-core.py`

Expected: PASS.

Run: `python tests/python-core.py`

Expected: PASS with existing gap, resolution, subtask, dependency, and evidence checks.

- [ ] **Step 6: Commit**

```text
git add xflow/traceability.py xflow/checks.py xflow/cli.py tests/trace-core.py tests/fixtures/traceability/valid.yaml tests/python-core.py
git commit -m "feat(trace): 闭合契约到交付证据链"
```

### Task 10: Publish the Complete devctl Command Contract

**Files:**
- Modify: `xflow-devctl/help.txt`
- Modify: `xflow-devctl/README.md`
- Modify: `xflow-devctl/tests/entrypoint-routing.py`
- Modify: `xflow-devctl/tests/python-core.py`

**Interfaces:**
- Documents every new command with a complete Windows/portable recipe and explains mechanical versus human review boundaries.

- [ ] **Step 1: Add failing help assertions**

Require exact anchors for:

```text
devctl task activate --issue IK3RR6
devctl check classification --issue IK3RR6
devctl contract lint --file docs/requirements/example/contract.yaml
devctl contract accept --issue IK3RR6 --file docs/requirements/example/contract.yaml --objects <id,id,...>
devctl contract diff --old <old.yaml> --new <new.yaml>
devctl trace check --issue IK3RR6 --contract <contract.yaml> --matrix <traceability-matrix.yaml>
```

Also require “`.xflow/issues/ is tracked by default`”, “lint does not approve semantic quality”, and “contract acceptance never supports unattended mode”.

- [ ] **Step 2: Run and verify RED**

Run: `python tests/entrypoint-routing.py`

Expected: FAIL because help text lacks the commands.

- [ ] **Step 3: Update help and README**

Document the shortest copyable happy path:

```text
devctl task activate --issue IK3RR6
devctl check classification --issue IK3RR6
devctl contract lint --file docs/requirements/composed-activity/contract.yaml
devctl approval prepare --issue IK3RR6 --action contract-acceptance --file docs/requirements/composed-activity/contract.yaml
devctl contract accept --issue IK3RR6 --file docs/requirements/composed-activity/contract.yaml --objects <approved-id-list>
devctl trace check --issue IK3RR6 --contract docs/requirements/composed-activity/contract.yaml --matrix .xflow/issues/issue-IK3RR6/traceability-matrix.yaml
```

Include migration, parallel worktree, approval-history, tracked/local mode, and old current-task compatibility sections.

- [ ] **Step 4: Run all devctl tests**

Run:

```text
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

Expected: all commands exit 0.

- [ ] **Step 5: Commit**

```text
git add help.txt README.md tests/entrypoint-routing.py tests/python-core.py
git commit -m "docs(devctl): 发布能力契约命令合同"
```

### Task 11: Add Skill Authoring References, Templates, and Schema Copy

**Files:**
- Create: `xflow-skills/references/capability-contract-method.md`
- Create: `xflow-skills/references/contract-authoring.md`
- Create: `xflow-skills/references/contract-evolution.md`
- Create: `xflow-skills/references/scope-routing.md`
- Create: `xflow-skills/references/traceability.md`
- Create: `xflow-skills/templates/capability-contract.yaml`
- Create: `xflow-skills/templates/classification.yaml`
- Create: `xflow-skills/templates/traceability-matrix.yaml`
- Create: `xflow-skills/templates/task-state.md`
- Create: `xflow-skills/schemas/capability-contract.schema.json`
- Modify: `xflow-skills/tests/main_entrypoint.py`

**Interfaces:**
- Produces: phase-selected instructions and artifact shapes consumed by downstream AI.
- Must match: devctl fields, enums, command names, and path rules exactly.

- [ ] **Step 1: Add failing static contract assertions**

Require the new files and anchors:

```python
require("references/contract-authoring.md", "先回答能力问题，再填写 YAML")
require("references/contract-authoring.md", "purpose → constraints → context")
require("references/contract-evolution.md", "PATCH")
require("references/contract-evolution.md", "MINOR")
require("references/contract-evolution.md", "MAJOR")
require("references/traceability.md", "contract → interaction → verification → issue → test → evidence → conclusion")
require("templates/task-state.md", "Semantic Phase:")
```

- [ ] **Step 2: Run and verify RED**

Run: `python tests/main_entrypoint.py`

Expected: FAIL on the first missing reference.

- [ ] **Step 3: Write the method and authoring references**

Distill the approved design rather than copying the long source documents. Include:

- Trigger matrix and lightweight route.
- Ten natural-language discovery questions.
- One-decision-at-a-time protocol.
- Field semantics and authoring order.
- Stable ID and version rules.
- Human acceptance and reopening rules.
- The rule that YAML `status: accepted-design` alone is not approval; only an exact tracked acceptance record referenced by task state closes the gate.
- Anti-patterns and one complete interaction/verification example.

- [ ] **Step 4: Write evolution, routing, and trace references**

Define classification consistency, contract-change versus implementation-gap behavior, dependency Issue boundaries, tracked Issue workspaces, and exact devctl recipes.

- [ ] **Step 5: Add templates and schema**

The Skill template must be structurally identical to the valid devctl fixture except for explanatory example values. The schema copy must be byte-identical to `xflow-devctl/schemas/capability-contract.schema.json`; add a test comparing SHA-256 values.

- [ ] **Step 6: Run Skill tests**

Run: `python tests/main_entrypoint.py`

Expected: PASS.

Run: `python tests/pressure_scenarios.py`

Expected: PASS.

- [ ] **Step 7: Commit**

```text
git add references templates schemas tests/main_entrypoint.py
git commit -m "feat(contract): 增加能力契约编写与追溯模块"
```

### Task 12: Integrate Capability Routing, Tracked Evidence, and Parallel Tasks into All AI Entrypoints

**Files:**
- Modify: `xflow-skills/SKILL.md`
- Modify: `xflow-skills/references/xflow-map.md`
- Modify: `xflow-skills/references/workflow-state-machine.md`
- Modify: `xflow-skills/references/issue-template.md`
- Modify: `xflow-skills/references/evidence-analysis.md`
- Modify: `xflow-skills/references/bootstrap-policy.md`
- Modify: `xflow-skills/references/restore-policy.md`
- Modify: `xflow-skills/references/source-resolution.md`
- Modify: `xflow-skills/references/issue-policy.md`
- Modify: `xflow-skills/references/attachment-policy.md`
- Modify: `xflow-skills/references/devctl-contract.md`
- Modify: `xflow-skills/references/scoring-rubric.md`
- Modify: `xflow-skills/templates/codex-agents.main.md`
- Modify: `xflow-skills/templates/cursorrules.main`
- Modify: `xflow-skills/.cursor/rules/xflow-workflow.mdc`
- Create: `xflow-skills/templates/claude.main.md`
- Create: `xflow-skills/templates/gemini.main.md`
- Create: `xflow-skills/templates/cursor-workflow.main.mdc`
- Create: `xflow-skills/templates/antigravity-agents.main.md`
- Create: `xflow-skills/templates/antigravity-xflow-workflow.main.md`
- Create: `xflow-skills/templates/antigravity-xflow-start.main.md`
- Modify: `xflow-skills/templates/ai-rules.json`
- Modify: `xflow-skills/AGENTS.md`
- Modify: `xflow-skills/CLAUDE.md`
- Modify: `xflow-skills/GEMINI.md`
- Modify: `xflow-skills/templates/xflow-local-ignored-vendor-init-prompt.md`
- Modify: `xflow-skills/README.md`
- Modify: `xflow-skills/tests/main_entrypoint.py`

**Interfaces:**
- Makes the capability gate discoverable in every supported AI client without duplicating the full method.
- Changes canonical task state from repository singleton to Issue-scoped state plus local active pointer.

- [ ] **Step 1: Add failing entrypoint assertions**

Require every high-frequency entrypoint to contain:

```text
Capability-Contract Gate
Locate an existing capability contract before classifying the request
AI must not edit implementation code before accepted-design
Verification matrix must exist before engineering projection
.xflow/issues/ is tracked by default
One worktree may activate only one remote Issue
```

Apply these assertions to `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `templates/codex-agents.main.md`, `templates/cursorrules.main`, `templates/claude.main.md`, `templates/gemini.main.md`, `templates/cursor-workflow.main.mdc`, `templates/antigravity-xflow-workflow.main.md`, and `.cursor/rules/xflow-workflow.mdc`. Reject prose that says `.xflow/issues/` is ignored or local-only by default.

- [ ] **Step 2: Run and verify RED**

Run: `python tests/main_entrypoint.py`

Expected: FAIL on missing capability and tracked-workspace anchors.

- [ ] **Step 3: Update `SKILL.md` routing**

Insert the capability gate before Issue drafting:

```text
read project rules
→ locate contract
→ write/check classification
→ choose capability-change | implementation-gap | ui-defect | infrastructure | governance | future
→ satisfy semantic exit condition
→ enter existing Issue/TDD/Git flow
```

Keep the main Skill concise and point to phase-specific references.

- [ ] **Step 4: Update state, Issue, evidence, bootstrap, and restore policy**

Replace singleton authority with `issue-<id>/task-state.md`; retain `.xflow/current-task.md` only as migration compatibility. Document tracked Issue artifacts, ignored active approval, immutable history record, UI environment identity, and object-storage publication boundaries.

- [ ] **Step 5: Update AI adapters**

Adapters contain only short hard rules and project-local Skill paths. They must not copy the full authoring guide. Keep human approval, unattended exclusions, commit format, and browser rules unchanged. `templates/ai-rules.json` must have exact target mappings for:

```json
[
  {"id": "codex", "target": "AGENTS.md", "template": "codex-agents.main.md"},
  {"id": "cursor", "target": ".cursorrules", "template": "cursorrules.main"},
  {"id": "cursor-mdc", "target": ".cursor/rules/xflow-workflow.mdc", "template": "cursor-workflow.main.mdc"},
  {"id": "claude", "target": "CLAUDE.md", "template": "claude.main.md"},
  {"id": "gemini", "target": "GEMINI.md", "template": "gemini.main.md"},
  {"id": "antigravity-agent", "target": ".agents/agents.md", "template": "antigravity-agents.main.md"},
  {"id": "antigravity-skill", "target": ".agents/skills/xflow-workflow.md", "template": "antigravity-xflow-workflow.main.md"},
  {"id": "antigravity-start", "target": ".agents/workflows/xflow-start.md", "template": "antigravity-xflow-start.main.md"}
]
```

Tests must parse JSON and assert each target-template pair exists exactly once.

- [ ] **Step 6: Update initialization prompt and README**

Initialization must create `.xflow/issues/`, `.xflow/local/`, `.xflow/xflow.json`, and exact ignore rules for ops/local/runtime/active approvals. It must install or merge every target in `templates/ai-rules.json`, report conflicts instead of overwriting project-owned text, and must not add `.xflow/issues/` to `.gitignore` in tracked mode.

- [ ] **Step 7: Run tests and scan contradictions**

Run: `python tests/main_entrypoint.py`

Expected: PASS.

Run:

```text
rg -n "\.xflow/issues.*ignored|ignore.*\.xflow/issues|local evidence workspace only" SKILL.md references templates README.md AGENTS.md .cursor
```

Expected: no default-local contradiction; only explicit `mode: local` exception text remains.

- [ ] **Step 8: Commit**

```text
git add SKILL.md references templates .cursor/rules/xflow-workflow.mdc AGENTS.md CLAUDE.md GEMINI.md README.md tests/main_entrypoint.py
git commit -m "feat(workflow): 接入能力契约语义门与并行任务"
```

### Task 13: Run Contract Generation and Version-Evolution Replay

**Files:**
- Create: `xflow-skills/tests/pressure-scenarios/contract-generation-input.md`
- Create: `xflow-skills/tests/pressure-scenarios/contract-generation-decisions.md`
- Create: `xflow-skills/docs/superpowers/evidence/2026-07-30-contract-generation-evaluation.md`
- Create: `xflow-skills/.xflow/issues/issue-contract-evaluation/evidence/contract.generated.yaml`
- Create: `xflow-skills/.xflow/issues/issue-contract-evaluation/evidence/contract.patch.yaml`
- Create: `xflow-skills/.xflow/issues/issue-contract-evaluation/evidence/contract.minor.yaml`
- Create: `xflow-skills/.xflow/issues/issue-contract-evaluation/evidence/contract.major.yaml`

**Interfaces:**
- Consumes: completed Skill references and devctl contract commands.
- Produces: reviewer-readable proof that the Skill can create and evolve a useful YAML contract.

- [ ] **Step 1: Run the discovery scenario in a fresh agent**

Provide only the natural-language capability input. Verify the agent preserves the statement, searches for existing contracts, asks one boundary-changing question at a time, offers alternatives, and stops before YAML or implementation.

- [ ] **Step 2: Supply approved decisions and generate the contract**

The resulting contract must start at `0.1.0`, use `accepted-design`, contain stable IDs, failure preservation, verification before projections, blockers, and future scope.

- [ ] **Step 3: Run mechanical checks**

From the devctl repository entrypoint bound to the evaluation workspace, run:

```text
devctl contract lint --file .xflow/issues/issue-contract-evaluation/evidence/contract.generated.yaml
```

Expected: PASS.

- [ ] **Step 4: Exercise the non-delegable contract-acceptance gate**

Prepare an exact `contract-acceptance` local review for the generated contract. Verify that `Approved: no`, unattended mode, a changed contract hash, the wrong worktree, and omitted accepted object IDs all fail. The Skill pressure scenario must separately prove that the AI refuses to edit `Approved: no` itself, because devctl cannot infer who typed a file change. After a human reviewer changes `Approved: no` to `Approved: yes`, run `devctl contract accept` and confirm the immutable acceptance record matches the contract ID, `0.1.0` version, SHA256, and approved object IDs.

- [ ] **Step 5: Apply the human semantic rubric**

Record pass/fail and rationale for purpose quality, testable constraints, success/failure completeness, authority versus projection, future separation, and stable IDs. A lint pass with a rubric failure is not accepted.

- [ ] **Step 6: Generate PATCH, MINOR, MAJOR, and implementation-gap variants**

Run `contract diff` for each transition. Verify unchanged object IDs and versions remain stable, affected object versions increase correctly, and the implementation-gap scenario does not modify contract versions.

- [ ] **Step 7: Re-run pressure scenarios with the new Skill**

Use fresh agents for all six scenario IDs. Record compliance, any new rationalizations, and changes made to close loopholes. Repeat until every scenario chooses the expected route and respects the stop condition.

- [ ] **Step 8: Commit evaluation artifacts**

The generated contracts and evidence are tracked because `.xflow/issues/` is tracked by default. Ensure they contain no credentials, local absolute paths, or active approval files.

```text
git add tests/pressure-scenarios docs/superpowers/evidence .xflow/issues/issue-contract-evaluation
git commit -m "test(contract): 回放契约生成与版本演进"
```

### Task 14: Full Cross-Repository Verification and Design Conformance Review

**Files:**
- Modify only if verification exposes a defect in the files owned by Tasks 1-13.

**Interfaces:**
- Verifies the complete design without adding new scope.

- [ ] **Step 1: Run all xflow-devctl checks**

```text
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

Expected: every command exits 0.

- [ ] **Step 2: Run all xflow-skills checks**

```text
python tests/main_entrypoint.py
python tests/pressure_scenarios.py
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 3: Run Windows wrapper smoke tests**

In a temporary Git repository with project-local devctl, run:

```text
.\devctl.ps1 preflight
.\devctl.ps1 task status
.\devctl.ps1 check classification --issue IK3RR6
.\devctl.ps1 contract lint --file docs\requirements\example\contract.yaml
.\devctl.ps1 contract accept --help
.\devctl.ps1 help
```

Expected: native PowerShell/Python execution with no WSL or bare Bash dependency.

- [ ] **Step 4: Review the approved design line by line**

Confirm every design section has an implementation and test: classification route, authoring method, dual state, parallel tasks, tracked evidence, approval history, contract lint/diff, trace check, multi-AI adapters, migration, failure policy, generation replay, and completion definition.

- [ ] **Step 5: Verify repository status and commit boundaries**

Run in both repositories:

```text
git status --short
git log --oneline --decorate -15
```

Expected: clean worktrees and focused commits matching the task boundaries above.

- [ ] **Step 6: Request final code review**

Use a fresh reviewer to inspect behavioral regressions, schema/validator drift, path traversal, approval replay, worktree isolation, and documentation-command consistency. Fix only substantiated findings and rerun the affected focused test plus both full suites.
