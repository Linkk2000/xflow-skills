# Advisory Dependency Issue Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend XFlow Skill so downstream AI can classify newly discovered work, record advisory dependency Issues, choose the correct branch integration path, and apply the agreed Chinese scoped Issue-linked commit format without turning dependency state into a hard development gate.

**Architecture:** Keep semantic guidance in one canonical reference and route to it from high-frequency AI entrypoints. Add a reusable YAML template for the issue-local dependency graph, update closure and evidence references to consume that graph, and use the existing static anchor test to prevent Codex, Cursor, ClaudeCode, and Gemini-facing instructions from drifting apart.

**Tech Stack:** Markdown, YAML, Python 3 standard-library static tests, Git.

## Global Constraints

- Work only in `D:\04-code\020-skill-dev\xflow-skills`.
- This repository defines rules for downstream repositories; its own maintenance commits use the repository's current contribution conventions and do not need a fabricated downstream Issue ID.
- Dependency state is advisory during development, local commit, test, and evidence collection. Never describe `discovered`, `active`, or `available` as an automatic stop condition.
- Creating a remote dependency Issue remains a non-delegable human-gated remote write.
- A simple main Issue may stay on its main feature branch without a child Issue or child branch.
- `subtask-*` remains a local work breakdown; `dependencies.yaml` records independently owned Issues or external dependencies. Do not merge these concepts.

---

### Task 1: Lock the new vocabulary into the static contract

**Files:**
- Modify: `tests/main_entrypoint.py`

- [ ] **Step 1: Add failing anchors**

Add `require(...)` assertions for these exact strings before changing documentation:

```python
require("SKILL.md", "Advisory Dependency Issue Workflow")
require("SKILL.md", "dependencies.yaml")
require("SKILL.md", "child-feature|shared-infrastructure|external")
require("SKILL.md", "must not automatically block development, commits, tests, or evidence collection")
require("references/dependency-issue-workflow.md", "discovered -> active -> available -> integrated")
require("references/dependency-issue-workflow.md", "A local subtask is not a dependency Issue")
require("references/git-policy.md", "type(scope): 中文核心摘要[#Issue编号]")
require("templates/codex-agents.main.md", "Advisory Dependency Issue Workflow")
require("templates/cursorrules.main", "Advisory Dependency Issue Workflow")
require("templates/dependencies.yaml", "blockingAssessment: partial")
```

Replace old assertions that require `` `type(scope): 中文摘要` `` and `` `关联 issue: #<id>` `` with assertions for the new subject-line association rule.

- [ ] **Step 2: Run the static test and confirm it fails**

Run: `python tests/main_entrypoint.py`

Expected: non-zero exit because `references/dependency-issue-workflow.md` and `templates/dependencies.yaml` do not exist yet.

- [ ] **Step 3: Keep the failing test uncommitted**

Do not commit a deliberately red repository state. Continue directly to Task 2; its passing commit includes `tests/main_entrypoint.py` with the two new canonical files.

---

### Task 2: Add the canonical dependency workflow and YAML template

**Files:**
- Create: `references/dependency-issue-workflow.md`
- Create: `templates/dependencies.yaml`
- Test: `tests/main_entrypoint.py`

- [ ] **Step 1: Write the canonical workflow reference**

Create `references/dependency-issue-workflow.md` with these executable sections:

```markdown
# Advisory Dependency Issue Workflow

## Classification
## Local Subtask Versus Dependency Issue
## Human Gate for Remote Issue Creation
## Advisory Blocking Assessment
## Lifecycle
## Branch and Integration Paths
## Parent Closure Assessment
## Evidence and Traceability
## Commit Ownership
## devctl Checks
```

Specify exactly:

- Keep work in the main Issue when it has no independent delivery boundary.
- `child-feature`: branch from the parent feature branch and merge back into it.
- `shared-infrastructure`: branch from target mainline, merge independently, then sync the parent feature branch and re-verify.
- `external`: record provider/version/entry point without inventing local commits.
- Lifecycle is `discovered -> active -> available -> integrated`, with `superseded` as an explicit alternative.
- `blockingAssessment` is `none|partial|full`; `decision` is `continue|pause-affected-scope|wait|use-temporary-adapter`.
- These fields record developer judgment and must not automatically block development, commits, tests, or evidence collection.
- `available` proves only that the dependency can be consumed; the parent must gather fresh integration evidence before `integrated`.
- A local subtask is not a dependency Issue and does not require a remote Issue or branch.

- [ ] **Step 2: Add the reusable YAML template**

Create `templates/dependencies.yaml` using concrete example IDs and all agreed fields:

```yaml
version: 0.1.0
issue: IK152D
dependencies:
  - issue: IK17AW
    repository: xflow-web
    type: shared-infrastructure
    requiredFor:
      - xflow.verify.case.stable-edge-anchor
    integrationTarget: mainline
    status: integrated
    blockingAssessment: partial
    decision: continue
    rationale: 属性编辑可继续，最终画布验证依赖统一端点能力。
    delivery:
      branch: fix/IK17AW-canonical-endpoints
      commit: abc1234
      mergeRequest: "56"
    integration:
      commit: def5678
      verifiedBy:
        - C-004
      evidence:
        - evidence/logs/c-004-integration-tests.txt
    closureAssessment:
      affectsClosure: true
      decision: integrated
      rationale: 相关验收已在主功能分支重新验证。
```

Add comments listing every enum and explaining that evidence paths are relative to `.xflow/issues/issue-IK152D/` and must stay in the repository.

- [ ] **Step 3: Run the static test**

Run: `python tests/main_entrypoint.py`

Expected: it still fails only on entrypoints not yet updated; the two new files satisfy their anchors.

- [ ] **Step 4: Commit the canonical reference and template**

```powershell
git add references/dependency-issue-workflow.md templates/dependencies.yaml tests/main_entrypoint.py
git commit -m "docs(dependency): 定义建议性依赖 Issue 工作流"
```

---

### Task 3: Route dependency discovery through the main Skill flow

**Files:**
- Modify: `SKILL.md`
- Modify: `references/workflow-state-machine.md`
- Modify: `references/xflow-map.md`
- Modify: `references/issue-template.md`
- Test: `tests/main_entrypoint.py`

- [ ] **Step 1: Add a high-frequency hard rule to `SKILL.md`**

Add `Advisory Dependency Issue Workflow` near the existing Problem/Gap and subtask rules. The rule must tell AI to:

1. Compare discovered work with the accepted main Issue scope.
2. Keep ordinary in-scope work on the main feature branch.
3. Use a local subtask only for local decomposition and repository-owned evidence.
4. Propose a dependency Issue only for independently owned work.
5. Prepare analysis and remote Issue material, then wait for exact human approval before creation.
6. Update `dependencies.yaml` after the dependency identity is known.
7. Treat dependency state as advisory until final closure analysis.
8. Require parent-side integration evidence before claiming `integrated`.

Use the literal classification string `child-feature|shared-infrastructure|external` and the literal warning `must not automatically block development, commits, tests, or evidence collection` so all agents receive the same wording.

- [ ] **Step 2: Extend the state machine**

In `references/workflow-state-machine.md`, add transitions for dependency discovery and integration without inserting a mandatory dependency gate into every Issue:

```text
IN_PROGRESS -> DEPENDENCY_DISCOVERED -> HUMAN_DEPENDENCY_DECISION
HUMAN_DEPENDENCY_DECISION -> IN_PROGRESS
DEPENDENCY_AVAILABLE -> PARENT_INTEGRATION_VERIFY -> IN_PROGRESS
```

Clarify that `HUMAN_DEPENDENCY_DECISION` is required only before the remote dependency Issue write, not before unrelated local implementation.

- [ ] **Step 3: Update maps and templates**

- Add the new reference and YAML template to `references/xflow-map.md`.
- In `references/issue-template.md`, show `dependencies.yaml` as an optional issue-level artifact.
- Explicitly distinguish optional `subtask-001/` from optional remote dependency entries.
- Add parent closure examples for `affectsClosure: false`, `integrated`, and approved `superseded`.

- [ ] **Step 4: Run tests**

Run: `python tests/main_entrypoint.py`

Expected: failures now concern commit policy or AI templates only.

- [ ] **Step 5: Commit the Skill routing changes**

```powershell
git add SKILL.md references/workflow-state-machine.md references/xflow-map.md references/issue-template.md
git commit -m "docs(skill): 接入依赖发现与集成闭环"
```

---

### Task 4: Publish the branch and commit ownership rules to every AI entrypoint

**Files:**
- Modify: `references/git-policy.md`
- Modify: `references/devctl-contract.md`
- Modify: `templates/codex-agents.main.md`
- Modify: `templates/cursorrules.main`
- Modify: `AGENTS.md`
- Test: `tests/main_entrypoint.py`

- [ ] **Step 1: Replace the old commit format**

Document the required downstream feature-branch format:

```text
type(scope): 中文核心摘要[#IK152D]

- 中文说明实际修改
- 中文说明对应的契约、Finding 或验收条件
- 中文说明测试结果和证据位置
```

State that:

- Direct main-feature commits use the main Issue ID.
- Child-feature and shared-infrastructure commits use their direct dependency Issue ID and link the parent or known consumers in the body.
- Ordinary subjects contain one direct-owner Issue ID.
- An explicit integration commit may contain two IDs, for example `merge(canvas): 集成统一容器事务能力[#IK152D][#IK17AW]`.
- Both GitHub numeric IDs and Gitee alphanumeric IDs are valid.
- The body is Chinese-dominant and multi-line; no AI trailers, absolute local paths, or provider-only metadata.

- [ ] **Step 2: Update the devctl contract**

Add these command contracts:

```text
devctl check dependencies --issue IK152D
devctl check commit-msg --file .xflow/local/commit-message.txt --issue IK152D
```

Describe dependency checks as structural warnings/checks, not business blocking decisions. Describe commit checks as a feature-branch policy gate before commit.

- [ ] **Step 3: Mirror concise rules into AI templates**

Add `Advisory Dependency Issue Workflow` to both `templates/codex-agents.main.md` and `templates/cursorrules.main`. Keep the compact entrypoint version to classification, human remote-write approval, advisory state, integration evidence, and commit ownership.

Update root `AGENTS.md` only where it serves as this repository's distributed template source; retain its tool-repository maintenance exception.

- [ ] **Step 4: Run the static test**

Run: `python tests/main_entrypoint.py`

Expected: exit code 0 and `main entrypoint checks passed`.

- [ ] **Step 5: Commit the cross-agent policy update**

```powershell
git add references/git-policy.md references/devctl-contract.md templates/codex-agents.main.md templates/cursorrules.main AGENTS.md tests/main_entrypoint.py
git commit -m "docs(git): 统一依赖分支提交与人工门禁"
```

---

### Task 5: Verify Skill consistency and hand off to devctl

**Files:**
- Verify: all files changed above

- [ ] **Step 1: Run the full Skill verification**

Run: `python tests/main_entrypoint.py`

Expected: exit code 0.

Run: `git diff --check HEAD~3..HEAD`

Expected: no whitespace errors.

- [ ] **Step 2: Search for obsolete policy wording**

Run:

```powershell
rg -n 'type\(scope\): 中文摘要|关联 issue: #<id>|dependency.*hard block|依赖.*自动.*阻塞' SKILL.md AGENTS.md references templates tests
```

Expected: no obsolete commit template; any occurrence of hard blocking appears only in a prohibition against it.

- [ ] **Step 3: Inspect repository state**

Run: `git status --short`

Expected: clean except for intentionally uncommitted implementation-plan documents.

- [ ] **Step 4: Record the handoff**

In the implementation summary, list the exact devctl behavior still required: YAML parsing, dependency consistency checks, closure integration, commit-message validation, and updated generated/backfill commits. Do not claim full feature completion until the separate devctl plan passes.
