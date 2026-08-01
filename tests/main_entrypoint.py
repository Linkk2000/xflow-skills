from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_CONTRACT_SCHEMA_SHA256 = "15cd0caf488c2ffbf5488ff8bf2b362dc9db77204089945f7788ecebe44e2a6f"
CAPABILITY_CONTRACT_TEMPLATE_SHA256 = "8dd258230cc6605ec03614305bb54247d847443751ac3d8dfc888e8077c65cbf"

CAPABILITY_ENTRYPOINTS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "templates/codex-agents.main.md",
    "templates/cursorrules.main",
    "templates/claude.main.md",
    "templates/gemini.main.md",
    "templates/cursor-workflow.main.mdc",
    "templates/antigravity-xflow-workflow.main.md",
    ".cursor/rules/xflow-workflow.mdc",
)

CAPABILITY_ENTRYPOINT_ANCHORS = (
    "Capability-Contract Gate",
    "Locate an existing capability contract before classifying the request",
    "AI must not edit implementation code before accepted-design",
    "Verification matrix must exist before engineering projection",
    ".xflow/issues/ is tracked by default",
    "One worktree may activate only one remote Issue",
)

CAPABILITY_METHOD_LINKS = (
    "references/capability-contract-method.md",
    "references/contract-authoring.md",
    "references/contract-evolution.md",
    "references/scope-routing.md",
    "references/traceability.md",
    "templates/capability-contract.yaml",
    "templates/classification.yaml",
    "templates/task-state.md",
    "templates/traceability-matrix.yaml",
)

AI_RULE_MAPPINGS = (
    ("codex", "AGENTS.md", "codex-agents.main.md"),
    ("cursor", ".cursorrules", "cursorrules.main"),
    ("cursor-mdc", ".cursor/rules/xflow-workflow.mdc", "cursor-workflow.main.mdc"),
    ("claude", "CLAUDE.md", "claude.main.md"),
    ("gemini", "GEMINI.md", "gemini.main.md"),
    ("antigravity-agent", ".agents/agents.md", "antigravity-agents.main.md"),
    ("antigravity-skill", ".agents/skills/xflow-workflow.md", "antigravity-xflow-workflow.main.md"),
    ("antigravity-start", ".agents/workflows/xflow-start.md", "antigravity-xflow-start.main.md"),
)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(relative: str, needle: str) -> None:
    text = read(relative)
    if needle not in text:
        raise AssertionError(f"missing {needle!r} in {relative}")


def reject(relative: str, needle: str) -> None:
    text = read(relative)
    if needle in text:
        raise AssertionError(f"obsolete {needle!r} in {relative}")


def reject_tree(roots: tuple[str, ...], needle: str) -> None:
    for root in roots:
        path = ROOT / root
        candidates = [path] if path.is_file() else path.rglob("*")
        for candidate in candidates:
            if candidate.is_file() and needle in candidate.read_text(encoding="utf-8"):
                raise AssertionError(f"obsolete {needle!r} in {candidate.relative_to(ROOT)}")


def require_all(relative: str, needles: tuple[str, ...]) -> None:
    text = read(relative)
    for needle in needles:
        if needle not in text:
            raise AssertionError(f"missing {needle!r} in {relative}")


def require_sha256(relative: str, expected: str) -> None:
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    if actual != expected:
        raise AssertionError(f"SHA-256 drift in {relative}: expected {expected}, found {actual}")


def require_capability_entrypoints() -> None:
    forbidden_default_local_claims = (
        ".xflow/issues/ is ignored",
        ".xflow/issues/ remains ignored",
        ".xflow/issues/ is local-only",
        ".xflow/issues/ is a local evidence workspace",
        ".xflow/issues/ is local evidence and approval state only",
        "ignore `.xflow/issues/`",
    )
    for relative in CAPABILITY_ENTRYPOINTS:
        require_all(relative, CAPABILITY_ENTRYPOINT_ANCHORS)
        for claim in forbidden_default_local_claims:
            reject(relative, claim)


def require_ai_rule_mappings() -> None:
    payload = json.loads(read("templates/ai-rules.json"))
    actual = [
        (rule.get("id"), rule.get("target"), rule.get("template"))
        for rule in payload.get("rules", [])
    ]
    if len(actual) != len(AI_RULE_MAPPINGS):
        raise AssertionError(
            f"templates/ai-rules.json must contain exactly {len(AI_RULE_MAPPINGS)} rules, found {len(actual)}"
        )
    for expected in AI_RULE_MAPPINGS:
        if actual.count(expected) != 1:
            raise AssertionError(
                f"templates/ai-rules.json must contain exactly one mapping {expected!r}, found {actual.count(expected)}"
            )


def main() -> None:
    require_capability_entrypoints()
    require_ai_rule_mappings()
    for relative in ("SKILL.md", "references/xflow-map.md"):
        require_all(relative, CAPABILITY_METHOD_LINKS)
    require_all(
        "SKILL.md",
        (
            "read project rules",
            "locate contract",
            "write/check classification",
            "capability-change | implementation-gap | ui-defect | infrastructure | governance | future",
            "satisfy semantic exit condition",
            "enter existing Issue/TDD/Git flow",
            ".xflow/issues/issue-<id>/task-state.md",
            ".xflow/local/worktrees/<worktree-fingerprint>/active-task.json",
            "`.xflow/current-task.md` is migration compatibility only",
            "issueWorkspace.mode: local",
        ),
    )
    for relative in (
        "references/workflow-state-machine.md",
        "references/issue-template.md",
        "references/devctl-contract.md",
        "references/xflow-map.md",
    ):
        require(relative, ".xflow/issues/issue-<id>/task-state.md")
        require(relative, "One worktree may activate only one remote Issue")
    require_all(
        "references/issue-template.md",
        (
            ".xflow/issues/issue-<id>/approvals/history/<timestamp>-<action>.yaml",
            "immutable",
            "reusable: false",
            "UI Environment Identity",
        ),
    )
    require_all(
        "references/evidence-analysis.md",
        (
            "UI Environment Identity",
            "product URL",
            "page identity",
            "model identity",
            "worktree",
            "Do not move Issue-local evidence to COS/OSS/object storage or HTTP URLs.",
        ),
    )
    require_all(
        "templates/xflow-local-ignored-vendor-init-prompt.md",
        (
            ".xflow/runtime/",
            ".xflow/issues/**/approvals/local-review.md",
            '"mode": "tracked"',
            "templates/ai-rules.json",
            "报告冲突",
            "不得覆盖项目自有文本",
            "不得将 `.xflow/issues/` 加入 `.gitignore`",
        ),
    )
    require("references/contract-authoring.md", "先回答能力问题，再填写 YAML")
    require("references/contract-authoring.md", "purpose → constraints → context")
    require("references/contract-evolution.md", "PATCH")
    require("references/contract-evolution.md", "MINOR")
    require("references/contract-evolution.md", "MAJOR")
    require("references/traceability.md", "contract → interaction → verification → issue → test → evidence → conclusion")
    require("templates/task-state.md", "Semantic Phase:")
    require_all(
        "references/capability-contract-method.md",
        (
            "1. Which participant gains or loses a dependable outcome?",
            "2. What purpose does that participant rely on, without naming a technical solution?",
            "3. What request/value enters the interaction?",
            "4. What observable value or stable refusal must leave it?",
            "5. Which state, permission, ordering, or safety rule must remain true?",
            "6. In what context is the interaction allowed to begin and complete?",
            "7. Which role owns the decision, and what explicitly does that role not own?",
            "8. Which failure reasons are distinguishable, and what does each preserve?",
            "9. What Given/When/Then observation can prove success and rejection?",
            "10. Which dependency, unanswered precondition, or future capability is outside this commitment?",
            "Do not ask a stakeholder to approve a large YAML blob.",
            "See `contract-authoring.md`, `scope-routing.md`, and `traceability.md` before",
        ),
    )
    require_all(
        "references/contract-authoring.md",
        (
            "Never reuse an ID for a different meaning.",
            "`MAJOR.MINOR.PATCH` versioning.",
            "YAML `status: accepted-design` alone is not approval.",
            "exact tracked acceptance record under",
            "`.xflow/issues/issue-<id>/approvals/history/`",
            "repository, worktree/recorded branch, Issue, approved file, contract ID and",
            "`semanticDecision: accepted-design`",
            "`source: local-review`, `action: contract-acceptance`",
            "normalized existing",
            "`acceptedObjects`",
            "Human Approval Is Non-Delegable.",
        ),
    )
    require_all(
        "references/scope-routing.md",
        (
            "| `capability-change` | `contractChangeRequired: true`; found or not-found | `contract-change-proposal.md` |",
            "| `implementation-gap` | `false`; found contract | `gap-analysis.md` |",
            "| `ui-defect` | `false`; found contract | `issue-draft.md` |",
            "| `infrastructure` | `false`; found or not-found | `dependency-issue-proposal.md` |",
            "| `governance` | `false`; found or not-found | `issue-draft.md` |",
            "| `future` | `false`; found or not-found | `futureCapabilitiesOutOfScope` or `future-task-proposal.md` |",
            "`child-feature|shared-infrastructure|external`",
            "Use a local subtask for work owned by the same feature branch.",
            "`.xflow/issues/issue-<id>/dependencies.yaml`",
            "must not automatically block development, commits, tests, or",
            "repository-local evidence, not a dependency's completion statement.",
        ),
    )
    require_all(
        "references/traceability.md",
        (
            "`contract → interaction → verification → issue → test → evidence → conclusion`",
            "`.xflow/issues/issue-<id>/traceability-matrix.yaml`",
            "`contractObjects` must exactly match the verification's `traces`",
            "Every active contract verification has",
            "`resolved|reduced` entries require fresh non-empty `evidence.after`",
            "Do not move local evidence to COS/OSS/object storage or HTTP URLs.",
            "A code diff or an AI statement that tests",
        ),
    )
    require_all(
        "templates/traceability-matrix.yaml",
        (
            "# Paths below are relative to that Issue directory and must stay in the repository.",
            "contractObjects:",
            "acceptanceCriterion:",
            "evidence:",
        ),
    )
    require_sha256("schemas/capability-contract.schema.json", CAPABILITY_CONTRACT_SCHEMA_SHA256)
    require_sha256("templates/capability-contract.yaml", CAPABILITY_CONTRACT_TEMPLATE_SHA256)
    require("SKILL.md", "This is the generic `main` product line")
    require("SKILL.md", "default local human approval or valid task-scoped unattended authorization before remote writes")
    require("SKILL.md", "Core Remote Write Review Gate")
    require("SKILL.md", "Human Approval Is Non-Delegable")
    require("SKILL.md", "AI must never satisfy a human gate itself")
    require("SKILL.md", "AI must never edit `Approved: no` to `Approved: yes`")
    require("SKILL.md", "Outside valid Task-Scoped Unattended Mode, AI must not use `--force`")
    require("SKILL.md", "继续")
    require("SKILL.md", "你看着办")
    require("SKILL.md", "Do not add AI-client co-author trailers")
    require("SKILL.md", "Commit messages must be portable, scoped, Chinese-dominant, multi-line")
    require("SKILL.md", "Advisory Dependency Issue Workflow")
    require("SKILL.md", "dependencies.yaml")
    require("SKILL.md", "child-feature|shared-infrastructure|external")
    require("SKILL.md", "must not automatically block development, commits, tests, or evidence collection")
    require("SKILL.md", "type(scope): 中文核心摘要[#Issue编号]")
    require("SKILL.md", "Task-Scoped Unattended Mode")
    require("SKILL.md", "XFLOW_HUMAN_UNATTENDED_ALL")
    require("SKILL.md", "user's current message")
    require("SKILL.md", "current repository, worktree, and XFlow task/Issue")
    require("SKILL.md", "mechanical checks, evidence requirements, attachment policy, and provider limitations remain mandatory")
    require("SKILL.md", "force push, history rewrite, destructive deletion, and secret or permission changes remain excluded")
    require("SKILL.md", "Task-scoped unattended mode never authorizes local branch deletion")
    require("SKILL.md", "git-cleanup-force")
    require("SKILL.md", "Default human path")
    require("SKILL.md", "Valid task-scoped unattended path")
    require("SKILL.md", "skip `devctl approval prepare`, human wait, and `devctl check local-review`")
    require("SKILL.md", "current-task, draft structure, evidence, attachment, provider/platform, and test checks still run")
    require("SKILL.md", "devctl approval prepare")
    require("SKILL.md", "devctl check current-task --issue <id>")
    require("SKILL.md", "devctl git push")
    require("SKILL.md", "state backfill commit")
    require("SKILL.md", "references/workflow-state-machine.md")
    require("SKILL.md", "references/attachment-policy.md")
    require("SKILL.md", "references/evidence-analysis.md")
    require("SKILL.md", "xflow-attachment://")
    require("SKILL.md", "image attachments are currently disabled")
    require("SKILL.md", "never use GitHub release assets as")
    require("SKILL.md", "`--no-local-review` alone is invalid")
    require("SKILL.md", "subtask-001")
    require("SKILL.md", "Subtask evidence must stay under that subtask's `evidence/` directory")
    require("SKILL.md", ".xflow/issues/ is tracked by default")
    require("SKILL.md", ".xflow/publish/issues/")
    require("SKILL.md", "~/.xflow/env.local")
    require("SKILL.md", "Do not put `XFLOW_PLATFORM` in user-level")
    require("SKILL.md", ".xflow/local/env.local")
    require("SKILL.md", "Gitee uses `GITEE_TOKEN`")
    require("SKILL.md", "Tool Repository Maintenance Exception")
    require("SKILL.md", "repositories that consume XFlow")
    require("SKILL.md", "xflow-skills and xflow-devctl maintenance commits")
    require("SKILL.md", "Do not import provider modules directly")
    require("SKILL.md", "python -m xflow")
    require("SKILL.md", "python tests/python-core.py")
    require("SKILL.md", "bare `bash`, Git Bash, or WSL")
    require("SKILL.md", "Browser Must Not Remain about:blank")
    require("SKILL.md", "navigate to an explicit target URL")
    require("SKILL.md", "verify the current URL is not `about:blank`")
    require("SKILL.md", "Problem/Gap Closure Loop")
    require("SKILL.md", "gap-analysis.md")
    require("SKILL.md", "resolution-report.md")
    require("SKILL.md", "resolved|reduced|blocked")
    require("SKILL.md", "AI must rework and rewrite the report")
    require("SKILL.md", "Each finding needs its own observation, direct evidence, analysis")
    require("SKILL.md", "live screenshot and DOM observation")
    require("SKILL.md", "templates/xflow-local-ignored-vendor-init-prompt.md")
    require("README.md", "templates/xflow-local-ignored-vendor-init-prompt.md")
    require("README.md", "local-ignored-vendor")
    require("README.md", "Task-Scoped Unattended Mode")
    require("templates/xflow-local-ignored-vendor-init-prompt.md", "无 git 空目录")
    require("templates/xflow-local-ignored-vendor-init-prompt.md", "无 git 非空目录")
    require("templates/xflow-local-ignored-vendor-init-prompt.md", "有 git 空仓库")
    require("templates/xflow-local-ignored-vendor-init-prompt.md", "有 git 已有项目")
    require("templates/xflow-local-ignored-vendor-init-prompt.md", "不使用 git submodule")
    require("templates/xflow-local-ignored-vendor-init-prompt.md", ".xflow/ops/workflow")
    require("templates/xflow-local-ignored-vendor-init-prompt.md", ".xflow/ops/devctl")
    require("templates/ai-rules.json", '"id": "codex"')
    require("templates/ai-rules.json", '"id": "cursor"')
    require("AGENTS.md", "Commit messages must be portable, scoped, Chinese-dominant, multi-line")
    require("AGENTS.md", "type(scope): 中文核心摘要[#Issue编号]")
    require("AGENTS.md", "Advisory Dependency Issue Workflow")
    require("AGENTS.md", "Task-Scoped Unattended Mode")
    require("AGENTS.md", "XFLOW_HUMAN_UNATTENDED_ALL")
    require("AGENTS.md", "sole exception to ordinary remote-write")
    require("AGENTS.md", "It never replaces human gates for entering development")
    require("templates/codex-agents.main.md", "Outside valid Task-Scoped Unattended Mode, do not perform remote writes before local human review")
    require("templates/codex-agents.main.md", "Advisory Dependency Issue Workflow")
    require("templates/codex-agents.main.md", "Task-Scoped Unattended Mode")
    require("templates/codex-agents.main.md", "XFLOW_HUMAN_UNATTENDED_ALL")
    require("templates/codex-agents.main.md", "user's current message")
    require("templates/codex-agents.main.md", "AI-generated or quoted safety word is invalid")
    require("templates/codex-agents.main.md", "current repository, worktree, and XFlow task/Issue")
    require("templates/codex-agents.main.md", "It never replaces human gates for entering development")
    require("templates/codex-agents.main.md", "default exact human gate or a valid task-scoped unattended")
    require("templates/codex-agents.main.md", "mechanical checks and evidence requirements remain mandatory")
    require("templates/codex-agents.main.md", "force push, history rewrite, destructive deletion, and secret or permission changes remain excluded")
    require("templates/codex-agents.main.md", "Task-scoped unattended mode never authorizes local branch deletion")
    require("templates/codex-agents.main.md", "Default human path")
    require("templates/codex-agents.main.md", "Valid task-scoped unattended path")
    require("templates/codex-agents.main.md", "skip approval-file prepare, human wait, and local-review check")
    require("templates/codex-agents.main.md", "current-task, draft structure, evidence, attachment, provider/platform, and test checks still run")
    require("templates/codex-agents.main.md", "On the default human path, push and PR/MR creation are separate human gates")
    require("templates/codex-agents.main.md", "Under valid task-scoped unattended mode, each push or PR/MR action must be covered by the bound state and pass its mechanical checks")
    require("templates/codex-agents.main.md", "Human Approval Is Non-Delegable")
    require("templates/codex-agents.main.md", "AI must never satisfy a human gate itself")
    require("templates/codex-agents.main.md", "AI must never edit `Approved: no` to `Approved: yes`")
    require("templates/codex-agents.main.md", "Outside valid Task-Scoped Unattended Mode, AI must not use `--force`")
    require("templates/codex-agents.main.md", "devctl check current-task --issue <id>")
    require("templates/codex-agents.main.md", "Co-authored-by: Cursor <cursoragent@cursor.com>")
    require("templates/codex-agents.main.md", "Commit messages must be portable, scoped, Chinese-dominant, multi-line")
    require("templates/codex-agents.main.md", "type(scope): 中文核心摘要[#Issue编号]")
    require("templates/codex-agents.main.md", "Do not import or call `xflow.providers` directly")
    require("templates/codex-agents.main.md", "XFLOW_PLATFORM=github|gitee")
    require("templates/codex-agents.main.md", "project-local")
    require("templates/codex-agents.main.md", "ordinary user projects")
    require("templates/codex-agents.main.md", "~/.xflow/env.local")
    require("templates/codex-agents.main.md", "Browser Must Not Remain about:blank")
    require("templates/codex-agents.main.md", "verify the current URL is not `about:blank`")
    require("templates/codex-agents.main.md", "Problem/Gap Closure Loop")
    require("templates/codex-agents.main.md", "AI must not skip gap-analysis human approval")
    require("templates/codex-agents.main.md", "AI must rework and rewrite the report")
    require("templates/codex-agents.main.md", "Evidence must be reviewable, not merely asserted")
    require("templates/codex-agents.main.md", "A code diff or \"tests passed\" statement is")
    require("templates/cursorrules.main", "Use the user's language for Git-related public text")
    require("templates/cursorrules.main", "Advisory Dependency Issue Workflow")
    require("templates/cursorrules.main", "Task-Scoped Unattended Mode")
    require("templates/cursorrules.main", "XFLOW_HUMAN_UNATTENDED_ALL")
    require("templates/cursorrules.main", "user's current message")
    require("templates/cursorrules.main", "AI-generated or quoted safety word is invalid")
    require("templates/cursorrules.main", "current repository, worktree, and XFlow task/Issue")
    require("templates/cursorrules.main", "It never replaces human gates for entering development")
    require("templates/cursorrules.main", "default exact human gate or a valid")
    require("templates/cursorrules.main", "mechanical checks and evidence requirements remain mandatory")
    require("templates/cursorrules.main", "force push, history rewrite, destructive deletion, and secret or permission changes remain excluded")
    require("templates/cursorrules.main", "Task-scoped unattended mode never authorizes local branch deletion")
    require("templates/cursorrules.main", "Default human path")
    require("templates/cursorrules.main", "Valid task-scoped unattended path")
    require("templates/cursorrules.main", "skip approval-file prepare, human wait, and local-review check")
    require("templates/cursorrules.main", "current-task, draft structure, evidence, attachment, provider/platform, and test checks still run")
    require("templates/cursorrules.main", "On the default human path, run `devctl check local-review` before remote writes")
    require("templates/cursorrules.main", "On the default human path, push and PR/MR creation are separate human gates")
    require("templates/cursorrules.main", "Under valid task-scoped unattended mode, each push or PR/MR action must be covered by the bound state and pass its mechanical checks")
    require("templates/cursorrules.main", "Human Approval Is Non-Delegable")
    require("templates/cursorrules.main", "AI must never satisfy a human gate itself")
    require("templates/cursorrules.main", "AI must never edit `Approved: no` to `Approved: yes`")
    require("templates/cursorrules.main", "Outside valid Task-Scoped Unattended Mode, AI must not use `--force`")
    require("templates/cursorrules.main", "devctl check current-task --issue <id>")
    require("templates/cursorrules.main", "Avoid `git ... 2>&1 | Out-String`")
    require("templates/cursorrules.main", "Do not import or call `xflow.providers` directly")
    require("templates/cursorrules.main", "XFLOW_PLATFORM=github|gitee")
    require("templates/cursorrules.main", "project-local")
    require("templates/cursorrules.main", "ordinary user projects")
    require("templates/cursorrules.main", "~/.xflow/env.local")
    require("templates/cursorrules.main", "Browser Must Not Remain about:blank")
    require("templates/cursorrules.main", "verify the current URL is not `about:blank`")
    require("templates/cursorrules.main", "Problem/Gap Closure Loop")
    require("templates/cursorrules.main", "AI must not skip gap-analysis human approval")
    require("templates/cursorrules.main", "AI must rework and rewrite the report")
    require("templates/cursorrules.main", "Evidence must be reviewable, not merely asserted")
    require("templates/cursorrules.main", "A code diff or \"tests passed\" statement is")
    require("templates/cursorrules.main", "Commit messages must be portable, scoped, Chinese-dominant, multi-line")
    require("templates/cursorrules.main", "type(scope): 中文核心摘要[#Issue编号]")
    require(".cursor/rules/xflow-workflow.mdc", "It never replaces human gates for entering development")
    require(".cursor/rules/xflow-workflow.mdc", "Issue create/comment/close, Git push, PR/MR create/merge")
    reject("templates/codex-agents.main.md", "retain exact human approval for")
    reject("templates/cursorrules.main", "retain exact human approval for")
    require("templates/dependencies.yaml", "blockingAssessment: partial")
    require("templates/dependencies.yaml", "development decision: continue | pause-affected-scope | wait | use-temporary-adapter")
    require("templates/dependencies.yaml", "closure decision: integrated | not-required | superseded")
    require(".gitignore", "__pycache__/")
    require(".gitignore", "*.py[cod]")
    require(".gitignore", ".pytest_cache/")
    require("templates/powershell-native-command.md", "PowerShell Native Command Notes")
    require("references/issue-template.md", "<!-- xflow: issue-draft -->")
    require("references/issue-template.md", "<!-- xflow: mr-draft -->")
    require("references/issue-template.md", ".xflow/current-task.md")
    require("references/issue-template.md", "git config user.name")
    require("references/issue-template.md", "--reviewer")
    require("references/issue-template.md", "Attachment Manifest SHA256")
    require("references/issue-template.md", "## subtask-001/README.md")
    require("references/issue-template.md", "## AI Review Checkpoints")
    require("references/issue-template.md", "## Human Review Checkpoints")
    require("references/issue-template.md", "success|blocked|superseded-by-human")
    require("references/issue-template.md", "## gap-analysis.md")
    require("references/issue-template.md", "## resolution-report.md")
    require("references/issue-template.md", "## Evidence-Backed Findings")
    require("references/issue-template.md", "## Completion Verification")
    require("references/issue-template.md", "#### Finding Type")
    require("references/issue-template.md", "#### Verification Type")
    require("references/issue-template.md", "resolved|reduced|blocked")
    require("references/issue-template.md", "## dependencies.yaml")
    require("references/issue-template.md", "affectsClosure: false")
    require("references/issue-template.md", "decision: integrated")
    require("references/issue-template.md", "decision: superseded")
    require("references/issue-template.md", "affectsClosure: false\n  decision: not-required")
    require("references/dependency-issue-workflow.md", "Default human path")
    require("references/dependency-issue-workflow.md", "Valid task-scoped unattended path")
    require("references/dependency-issue-workflow.md", "skip approval-file preparation, human wait, and local-review validation")
    require("references/dependency-issue-workflow.md", "current-task, draft structure, evidence, attachment, provider/platform, and test checks still run")
    require("references/dependency-issue-workflow.md", "pre-ledger discovered -> active -> available -> integrated")
    require("references/dependency-issue-workflow.md", "must not write `discovered` to `dependencies.yaml`")
    require("references/dependency-issue-workflow.md", "A local subtask is not a dependency Issue")
    require("references/attachment-policy.md", "# Attachment Policy")
    require("references/attachment-policy.md", "publishedUrl")
    require("references/attachment-policy.md", "github-release")
    require("references/attachment-policy.md", "Issue/comment image attachments are currently disabled")
    require("references/attachment-policy.md", "GitHub release assets are not an approved issue image store")
    require("references/attachment-policy.md", "Aliyun OSS attachment backend")
    require("references/attachment-policy.md", "devctl attachment publish --issue draft --backend aliyun-oss")
    require("references/attachment-policy.md", "ALIYUN_OSS_ACCESS_KEY_SECRET")
    require("references/attachment-policy.md", "must not be written to attachment manifests")
    require("references/attachment-policy.md", "Subtask evidence must stay in the repository")
    require("references/attachment-policy.md", ".xflow/issues/ is tracked by default")
    require("references/attachment-policy.md", ".xflow/publish/issues/")
    require("references/attachment-policy.md", "not in COS/OSS")
    require("references/attachment-policy.md", "Required Checks")
    require("references/attachment-policy.md", "AI Decision Table")
    require("references/attachment-policy.md", "Task-scoped unattended issue or comment")
    require("references/attachment-policy.md", "The mode replaces only the ordinary human gate")
    require("references/attachment-policy.md", "Reviewed non-image issue attachment")
    require("references/attachment-policy.md", "Reviewed Aliyun OSS image issue")
    require("references/devctl-contract.md", "AI Call Recipes")
    require("references/devctl-contract.md", "Issue/comment image attachments are disabled")
    require("references/devctl-contract.md", "Do not use GitHub release assets as an issue image store")
    require("references/devctl-contract.md", "devctl attachment publish --issue draft --backend aliyun-oss")
    require("references/devctl-contract.md", "%USERPROFILE%\\.xflow\\env.local")
    require("references/devctl-contract.md", "devctl check subtask --issue")
    require("references/devctl-contract.md", "devctl check issue-evidence --issue")
    require("references/devctl-contract.md", "devctl check gap-analysis --issue")
    require("references/devctl-contract.md", "devctl check resolution-report --issue")
    require("references/devctl-contract.md", "Problem/Gap Closure Loop")
    require("references/devctl-contract.md", "under the current subtask's")
    require("references/devctl-contract.md", "`evidence/` directory")
    require("references/issue-policy.md", "Do not probe by retrying random flag combinations")
    require("references/issue-policy.md", "approved object storage backend")
    require("references/workflow-state-machine.md", "S0_REQUEST")
    require("references/workflow-state-machine.md", "G3_APPROVE_RESULT")
    require("references/workflow-state-machine.md", "subtask README")
    require("references/workflow-state-machine.md", "Do not edit an approval file to set `Approved: yes`")
    require("references/workflow-state-machine.md", "state backfill commit")
    require("references/workflow-state-machine.md", "Browser Must Not Remain about:blank")
    require("references/workflow-state-machine.md", "explicit target URL")
    require("references/workflow-state-machine.md", "Problem/Gap Closure Loop")
    require("references/workflow-state-machine.md", "AI must rework and rewrite the report")
    require("references/workflow-state-machine.md", "reviewer-readable evidence bundle")
    require("references/workflow-state-machine.md", "IN_PROGRESS -> DEPENDENCY_DISCOVERED -> HUMAN_DEPENDENCY_DECISION")
    require("references/workflow-state-machine.md", "DEPENDENCY_AVAILABLE -> PARENT_INTEGRATION_VERIFY -> IN_PROGRESS")
    require("references/workflow-state-machine.md", "HUMAN_REVIEW_REQUIRED -> UNATTENDED_ACTIVE -> REMOTE_WRITE")
    require("references/xflow-map.md", "devctl check current-task --issue <number>")
    require("references/xflow-map.md", "devctl check local-review")
    require("references/xflow-map.md", "devctl approval prepare")
    require("references/xflow-map.md", "devctl git push --issue")
    require("references/xflow-map.md", "state backfill commit")
    require("references/xflow-map.md", "Gitee v5")
    require("references/xflow-map.md", ".xflow/local/env.local")
    require("references/xflow-map.md", "devctl attachment check")
    require("references/xflow-map.md", "devctl check subtask --issue")
    require("references/xflow-map.md", "subtask-001/evidence/")
    require("references/xflow-map.md", ".xflow/publish/issues/")
    require("references/xflow-map.md", "devctl attachment publish --issue draft --backend aliyun-oss")
    require("references/xflow-map.md", "type(scope): 中文核心摘要[#Issue编号]")
    require("references/xflow-map.md", "--backend manual")
    require("references/xflow-map.md", "--no-local-review")
    require("references/xflow-map.md", "The compatibility flag alone never authorizes it")
    require("references/xflow-map.md", "xflow-attachment://")
    require("references/xflow-map.md", "Issue/comment image attachments are disabled")
    require("references/xflow-map.md", "Windows validation must use Python core checks")
    require("references/xflow-map.md", "Browser Must Not Remain about:blank")
    require("references/xflow-map.md", "about:blank")
    require("references/xflow-map.md", "Problem/Gap Closure Loop")
    require("references/xflow-map.md", "gap-analysis.md")
    require("references/xflow-map.md", "resolution-report.md")
    require("references/xflow-map.md", "evidence-analysis.md")
    require("references/xflow-map.md", "dependency-issue-workflow.md")
    require("references/xflow-map.md", "templates/dependencies.yaml")
    require("references/xflow-map.md", "devctl unattended enable|status|disable")
    require("references/xflow-map.md", "Project-Local Compatibility Gate")
    require("references/xflow-map.md", "project-local `devctl help`")
    require("references/xflow-map.md", "stop and update or restore the project-local devctl")
    require("references/xflow-map.md", "must not probe by trying commands or pretend the capability is available")
    require("references/xflow-map.md", "Default human path")
    require("references/xflow-map.md", "Valid task-scoped unattended path")
    require("references/xflow-map.md", "skip approval-file preparation, human wait, and local-review validation")
    require("references/devctl-contract.md", "POST /v5/repos/{owner}/issues")
    require("references/devctl-contract.md", "GITEE_API_BASE")
    require("references/devctl-contract.md", "git@github.com:Linkk2000/xflow-skills.git")
    require("references/devctl-contract.md", "devctl attachment check")
    require("references/devctl-contract.md", "Portable scoped commit message")
    require("references/devctl-contract.md", "devctl check dependencies --issue IK152D")
    require("references/devctl-contract.md", "devctl check commit-msg --file .xflow/local/commit-message.txt --issue IK152D")
    require("references/devctl-contract.md", "type(scope): 中文核心摘要[#Issue编号]")
    require("references/devctl-contract.md", "devctl unattended enable --issue IK152D --confirm XFLOW_HUMAN_UNATTENDED_ALL")
    require("references/devctl-contract.md", "devctl unattended status")
    require("references/devctl-contract.md", "devctl unattended disable")
    require("references/devctl-contract.md", "[UNATTENDED] Human approval gate bypassed for current task IK152D.")
    require("references/devctl-contract.md", "Project-Local Compatibility Gate")
    require("references/devctl-contract.md", "project-local `devctl help`")
    require("references/devctl-contract.md", "`.\\devctl.ps1 help`")
    require("references/devctl-contract.md", "stop and update or restore the project-local devctl")
    require("references/devctl-contract.md", "must not probe by trying commands or pretend the capability is available")
    require("references/devctl-contract.md", "browser_download_url")
    require("references/devctl-contract.md", "The flag alone is invalid")
    require("references/devctl-contract.md", "backfill commit")
    require("references/devctl-contract.md", "Git lifecycle commands implemented")
    require("references/devctl-contract.md", "Windows validation must not invoke bare `bash`")
    reject("references/attachment-policy.md", "Unattended GitHub attachment issue")
    reject("references/devctl-contract.md", "Unattended GitHub attachment issue")
    reject("references/xflow-map.md", "authorized unattended GitHub upload")
    require("references/platform-adapters.md", "Avoid bare `bash` or Git Bash")
    require("references/platform-adapters.md", "Run `bash -n` only for changed POSIX shell compatibility scripts")
    require("references/scoring-rubric.md", "Generic Skill Evaluation Matrix")
    require("references/scoring-rubric.md", "Score Bands")
    require("references/scoring-rubric.md", "Hard Fail Gates")
    require("references/scoring-rubric.md", "Evaluator Workflow")
    require("references/scoring-rubric.md", "Evidence Checklist")
    require("references/scoring-rubric.md", "Evidence Reviewability")
    require("references/evidence-analysis.md", "Evidence-Backed Gap Analysis And Completion Verification")
    require("references/evidence-analysis.md", "one direct evidence bundle per finding")
    require("references/evidence-analysis.md", "evidence/screenshots/")
    require("references/evidence-analysis.md", "evidence/dom/")
    require("references/evidence-analysis.md", "a code diff or an AI statement")
    require("references/scoring-rubric.md", "Pressure Test Suite")
    require("references/scoring-rubric.md", "Tool Contract Consistency")
    require("references/scoring-rubric.md", "Project Override Compliance")
    require("references/source-resolution.md", "git@github.com:Linkk2000/xflow-devctl.git")
    require("references/source-resolution.md", "Project-local `.xflow/ops/` tools are the runtime source of truth")
    require("references/source-resolution.md", "local-ignored-vendor")
    require("references/source-resolution.md", ".xflow/ops/devctl")
    require("references/source-resolution.md", ".xflow/ops/workflow")
    require("references/bootstrap-policy.md", "Local ignored vendor mode is the default")
    require("references/restore-policy.md", "Do not fall back to a global installed skill")
    require("references/devctl-contract.md", "No global devctl entrypoint is required")
    require("references/xflow-map.md", ".\\devctl.ps1 preflight")
    require("references/ops-lessons.md", "devctl.ps1")
    require("references/issue-template.md", "Approved: no")
    require("references/issue-template.md", "Only the human reviewer may change Approved: no to Approved: yes")
    require("references/human-gates.md", "Human Approval Is Non-Delegable")
    require("references/human-gates.md", "AI must never satisfy a human gate itself")
    require("references/human-gates.md", "AI must never edit `Approved: no` to `Approved: yes`")
    require("references/human-gates.md", "继续")
    require("references/human-gates.md", "你看着办")
    require("references/human-gates.md", "go ahead")
    require("references/human-gates.md", "`--no-local-review` must not be used for push")
    require("references/human-gates.md", "Task-Scoped Unattended Mode")
    require("references/human-gates.md", "`--no-local-review` alone is invalid")
    require("references/git-policy.md", "type(scope): 中文核心摘要[#Issue编号]")
    require("references/git-policy.md", "merge(canvas): 集成统一容器事务能力[#IK152D][#IK17AW]")
    require("references/git-policy.md", "one direct-owner Issue ID")
    require("references/git-policy.md", "Only `merge(...)` integration subjects may contain two Issue IDs")
    require("references/git-policy.md", "Task-scoped unattended mode never satisfies `git-cleanup` or `git-cleanup-force`")
    require("references/git-policy.md", "GitHub numeric IDs and Gitee alphanumeric IDs")
    reject("references/xflow-map.md", "D:\\")
    reject("references/devctl-contract.md", "https://github.com/Linkk2000")
    reject("references/source-resolution.md", "https://github.com/Linkk2000")
    reject("references/source-resolution.md", "Default global source root")
    reject("references/source-resolution.md", ".xflow/sources")
    reject("references/bootstrap-policy.md", ".xflow/sources")
    reject("references/restore-policy.md", ".xflow/sources")
    reject("references/devctl-contract.md", "Windows global source root")
    reject("references/bootstrap-policy.md", "global default")
    reject("references/source-resolution.md", ".codex\\xflow\\repos")
    reject("references/source-resolution.md", ".codex/xflow/repos")
    reject("templates/dependencies.yaml", "status: discovered")
    require("templates/dependencies.yaml", "status: active | available | integrated | superseded")
    require(".cursor/rules/xflow-workflow.mdc", "Task-Scoped Unattended Mode")
    require(".cursor/rules/xflow-workflow.mdc", "XFLOW_HUMAN_UNATTENDED_ALL")
    require(".cursor/rules/xflow-workflow.mdc", "never authorizes local branch deletion")
    require(".cursor/rules/xflow-workflow.mdc", "mechanical checks and evidence requirements remain mandatory")
    require("docs/superpowers/plans/2026-07-28-task-scoped-unattended-skill-implementation.md", "main entrypoint ok")
    reject("references/restore-policy.md", ".codex\\xflow\\repos")
    reject("references/restore-policy.md", ".codex/xflow/repos")
    reject("SKILL.md", "devctl claude")
    reject("templates/codex-agents.main.md", "AcademicForge")
    reject_tree(
        ("SKILL.md", "references", "templates"),
        "current-turn explicit human authorization for this exact no-attachment",
    )
    reject_tree(
        ("SKILL.md", "references", "templates"),
        "current user explicitly authorized this exact unattended",
    )
    reject_tree(
        ("SKILL.md", "references", "templates"),
        "explicitly authorizes an unattended issue/comment command",
    )
    print("main entrypoint ok")


if __name__ == "__main__":
    main()
