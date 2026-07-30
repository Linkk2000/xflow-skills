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
