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
    require("templates/ai-rules.json", '"id": "codex"')
    require("templates/ai-rules.json", '"id": "cursor"')
    require("templates/codex-agents.main.md", "Do not perform remote writes before local human review")
    require("templates/codex-agents.main.md", "Co-authored-by: Cursor <cursoragent@cursor.com>")
    require("templates/cursorrules.main", "Use the user's language for Git-related public text")
    require("templates/cursorrules.main", "Avoid `git ... 2>&1 | Out-String`")
    require("templates/powershell-native-command.md", "PowerShell Native Command Notes")
    require("references/issue-template.md", "<!-- xflow: issue-draft -->")
    require("references/issue-template.md", "<!-- xflow: mr-draft -->")
    require("references/xflow-map.md", "devctl check local-review")
    require("references/xflow-map.md", "devctl approval prepare")
    require("references/xflow-map.md", ".\\devctl.ps1 preflight")
    require("references/ops-lessons.md", "devctl.ps1")
    require("references/issue-template.md", "Approved: no")
    reject("references/xflow-map.md", "D:\\")
    reject("SKILL.md", "devctl claude")
    reject("templates/codex-agents.main.md", "AcademicForge")
    print("main entrypoint ok")


if __name__ == "__main__":
    main()
