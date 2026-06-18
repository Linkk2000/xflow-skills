from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


def main() -> None:
    require("SKILL.md", "This is the generic `main` product line")
    require("SKILL.md", "Core Remote Write Review Gate")
    require("SKILL.md", "Do not add AI-client co-author trailers")
    require("SKILL.md", "devctl approval prepare")
    require("SKILL.md", "devctl check current-task --issue <id>")
    require("SKILL.md", "references/workflow-state-machine.md")
    require("SKILL.md", "~/.xflow/env.local")
    require("SKILL.md", "Do not put `XFLOW_PLATFORM` in user-level")
    require("SKILL.md", ".xflow/local/env.local")
    require("SKILL.md", "Gitee uses `GITEE_TOKEN`")
    require("SKILL.md", "Tool Repository Maintenance Exception")
    require("SKILL.md", "repositories that consume XFlow")
    require("SKILL.md", "Do not import provider modules directly")
    require("SKILL.md", "python -m xflow")
    require("templates/ai-rules.json", '"id": "codex"')
    require("templates/ai-rules.json", '"id": "cursor"')
    require("templates/codex-agents.main.md", "Do not perform remote writes before local human review")
    require("templates/codex-agents.main.md", "devctl check current-task --issue <id>")
    require("templates/codex-agents.main.md", "Co-authored-by: Cursor <cursoragent@cursor.com>")
    require("templates/codex-agents.main.md", "Do not import or call `xflow.providers` directly")
    require("templates/codex-agents.main.md", "XFLOW_PLATFORM=github|gitee")
    require("templates/codex-agents.main.md", "project-local")
    require("templates/codex-agents.main.md", "ordinary user projects")
    require("templates/codex-agents.main.md", "~/.xflow/env.local")
    require("templates/cursorrules.main", "Use the user's language for Git-related public text")
    require("templates/cursorrules.main", "devctl check current-task --issue <id>")
    require("templates/cursorrules.main", "Avoid `git ... 2>&1 | Out-String`")
    require("templates/cursorrules.main", "Do not import or call `xflow.providers` directly")
    require("templates/cursorrules.main", "XFLOW_PLATFORM=github|gitee")
    require("templates/cursorrules.main", "project-local")
    require("templates/cursorrules.main", "ordinary user projects")
    require("templates/cursorrules.main", "~/.xflow/env.local")
    require(".gitignore", "__pycache__/")
    require(".gitignore", "*.py[cod]")
    require(".gitignore", ".pytest_cache/")
    require("templates/powershell-native-command.md", "PowerShell Native Command Notes")
    require("references/issue-template.md", "<!-- xflow: issue-draft -->")
    require("references/issue-template.md", "<!-- xflow: mr-draft -->")
    require("references/issue-template.md", ".xflow/current-task.md")
    require("references/issue-template.md", "git config user.name")
    require("references/issue-template.md", "--reviewer")
    require("references/workflow-state-machine.md", "S0_REQUEST")
    require("references/workflow-state-machine.md", "G3_APPROVE_RESULT")
    require("references/workflow-state-machine.md", "Do not edit an approval file to set `Approved: yes`")
    require("references/xflow-map.md", "devctl check current-task --issue <number>")
    require("references/xflow-map.md", "devctl check local-review")
    require("references/xflow-map.md", "devctl approval prepare")
    require("references/xflow-map.md", "Gitee v5")
    require("references/xflow-map.md", ".xflow/local/env.local")
    require("references/devctl-contract.md", "POST /v5/repos/{owner}/issues")
    require("references/devctl-contract.md", "GITEE_API_BASE")
    require("references/xflow-map.md", ".\\devctl.ps1 preflight")
    require("references/ops-lessons.md", "devctl.ps1")
    require("references/issue-template.md", "Approved: no")
    reject("references/xflow-map.md", "D:\\")
    reject("SKILL.md", "devctl claude")
    reject("templates/codex-agents.main.md", "AcademicForge")
    print("main entrypoint ok")


if __name__ == "__main__":
    main()
