"""Policy contract checks only; this does NOT prove devctl runtime support."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
policy = json.loads((ROOT / "references/unattended-mr-only-policy.json").read_text())
auto, human, excluded = (set(policy[k]) for k in ("automaticActions", "humanActions", "excludedActions"))
assert not (auto & human or auto & excluded or human & excluded)
assert human == {"mr-review"}
assert {"task-branch-start", "contract-acceptance", "gap-recognition", "development-start", "git-mr", "git-push"} <= auto
assert "git-pr-merge" not in auto
assert policy["semanticRecordSource"] == "unattended"
assert set(policy["preservedTransitions"]) & set(policy["retiredTransitions"]) == set()

# A complete declared delivery path has precisely one human review point.
delivery = ["issue-create", "task-branch-start", "contract-acceptance",
            "development-start", "commit", "sync-base", "git-push", "git-mr",
            "mr-review", "issue-close", "safe-merged-cleanup"]
assert [action for action in delivery if action in human] == ["mr-review"]
assert all(action in auto | human for action in delivery)
# Gap work has the same gate count without pretending the gap was human-approved.
delivery[2] = "gap-recognition"
assert sum(action in human for action in delivery) == 1

requirements = set(policy["merge"]["requires"])
assert requirements == {"human-reviewed-current-head", "matching-target",
                        "required-checks-passed", "explicit-merge-scope"}
for missing in requirements:
    assert not requirements <= requirements - {missing}

paths = [
  "SKILL.md",
  "AGENTS.md",
  "CLAUDE.md",
  "GEMINI.md",
  ".cursor/rules/xflow-workflow.mdc",
  ".agents/agents.md",
  ".agents/skills/xflow-workflow.md",
  "templates/codex-agents.main.md",
  "templates/cursorrules.main",
  "templates/cursor-workflow.main.mdc",
  "templates/claude.main.md",
  "templates/gemini.main.md",
  "templates/antigravity-agents.main.md",
  "templates/antigravity-xflow-workflow.main.md",
  "references/workflow-state-machine.md",
  "references/human-gates.md",
  "references/git-policy.md",
  "references/devctl-contract.md",
  "references/contract-authoring.md",
  "references/scope-routing.md",
  "references/issue-policy.md",
  "references/dependency-issue-workflow.md",
  "references/evidence-analysis.md",
  "references/capability-contract-method.md",
  "references/xflow-map.md",
  "references/priority-and-overrides.md"
]
for relative in paths:
    content = (ROOT / relative).read_text()
    assert content.count("<!-- xflow: approval-policy-dispatch -->") == 1, relative
    assert "mr-only-v1" in content, relative
    # Generated adapters resolve in the consumer, direct references in the skill.
    target = "unattended-mr-only.md" if relative.startswith("references/") else "references/unattended-mr-only.md"
    assert target in content, relative
assert (ROOT / "references/unattended-mr-only.md").is_file()
print("MR-only policy contract: delivery/gap paths, gate set, merge requirements and adapter routing passed")
print("Runtime end-to-end validation is pending the devctl implementation.")

