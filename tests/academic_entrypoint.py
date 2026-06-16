from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_ref(file_name: str, ref: str) -> None:
    path = ROOT / file_name
    text = path.read_text(encoding="utf-8")
    if ref not in text:
        raise AssertionError(f"missing reference {ref!r} in {file_name}")


def reject_ref(file_name: str, ref: str) -> None:
    path = ROOT / file_name
    text = path.read_text(encoding="utf-8")
    if ref in text:
        raise AssertionError(f"obsolete reference {ref!r} in {file_name}")


def main() -> int:
    for ref in (
        "references/academic-workflow.md",
        "references/academic-templates.md",
        "references/academic-schema-contract.md",
        "references/academicforge-skill-catalog.md",
    ):
        require_ref("SKILL.md", ref)
        require_ref("references/xflow-map.md", ref)

    for file_name, refs in {
        "SKILL.md": (
            "PowerShell Native Command Safety",
            "Windows users should default to PowerShell plus Python devctl",
            "WSL is a developer compatibility path",
            "Invoke-XFlowGit -GitArguments @(...)",
            "AI Rule Entrypoint Safety",
            "devctl rules sync <id>",
            "templates/ai-rules.json",
            "Legacy `_ops` Migration Safety",
            "devctl migrate inspect",
            "devctl migrate wrappers",
            "python -m xflow",
            "Review-Only Scope Safety",
            "devctl check scope --issue <id> --mode review-only",
            ".xflow/scope-policy.json",
            "Approval And PR Sealing Safety",
            "devctl approval prepare --issue <id> --action <action> --file <artifact>",
            "devctl check current-task --issue <id>",
            "After the PR is merged, seal the task board",
            "Remote Published Body Safety",
        ),
        ".gitignore": ("__pycache__/", "*.py[cod]", ".pytest_cache/", "*.tmp"),
        "templates/ai-rules.json": (
            '"schema": "academic-xflow/ai-rules/v1"',
            '"id": "codex"',
            '"target": "AGENTS.md"',
            '"template": "codex-agents.academic.md"',
            '"id": "cursor"',
            '"target": ".cursorrules"',
            '"template": "cursorrules.academic"',
        ),
        "templates/codex-agents.academic.md": (
            "devctl rules list",
            "devctl rules sync <id>",
            "Default to PowerShell plus Python devctl on Windows",
            "Do not switch to WSL",
            "devctl migrate inspect",
            "devctl migrate wrappers",
            "python -m xflow",
            "must not call Bash, WSL, Claude, AcademicForge, or any installer",
            "Do not invent active approval filenames",
            "Do not add AI-client co-author trailers",
            "devctl check scope --issue <id> --mode review-only",
            "devctl approval prepare --issue <id> --action <action> --file <artifact>",
            "devctl check current-task --issue <id>",
        ),
        "templates/cursorrules.academic": (
            "Default to PowerShell plus Python devctl on Windows",
            "Do not switch to WSL",
            "devctl claude doctor",
            "devctl claude run --issue <id>",
            "devctl claude skills",
            "devctl rules list",
            "devctl rules sync <id>",
            "devctl migrate inspect",
            "devctl migrate wrappers",
            "python -m xflow",
            "must not call Bash, WSL, Claude, AcademicForge, or any installer",
            "academicforge-skill-catalog.md",
            "checked `.claude/skills` roots",
            "Claude Skill:",
            "Invocation:",
            "/peer-review",
            "DEVCTL_CLAUDE_ARGS",
            "focus=methodology severity=major",
            "successful CLI exit code alone is not enough",
            "generic reply asking",
            "Claude-resolvable flat skill directory",
            "nested official source path",
            "--body-file",
            "fetch, pin reviewed SHA, test, human review, then commit",
            "Do not pipe native Git commands through `2>&1 | Out-String`",
            "$LASTEXITCODE",
            ".xflow/tools/xflow-powershell-native.ps1",
            "Do not combine multiple native commands in one PowerShell line",
            "PowerShell check scripts must use ASCII terminal output",
            "Initialize-XFlowPowerShellEncoding",
            "Write-XFlowStatus",
            "Git-facing text only",
            "Co-authored-by: Cursor <cursoragent@cursor.com>",
            "Approved Action: git-mr",
            "devctl approval prepare --issue <id> --action <action> --file <artifact>",
            "devctl check current-task --issue <id>",
            "Do not create or push an `academic` branch in the paper repository",
            "devctl check scope --issue <id> --mode review-only",
        ),
        "templates/xflow-powershell-native.ps1": (
            "function Invoke-XFlowNative",
            "function Invoke-XFlowGit",
            "function Initialize-XFlowPowerShellEncoding",
            "function Write-XFlowStatus",
            "GitArguments",
            "Start-Process",
            "ExitCode",
        ),
        "references/academic-workflow.md": (
            "templates/ai-rules.json",
            "devctl rules list",
            "devctl rules sync cursor",
            "AGENTS.md",
            "templates/xflow-powershell-native.ps1",
            "Windows users should default to PowerShell plus Python devctl",
            "WSL is a developer compatibility path",
            "PowerShell Native Git Rule",
            "GitHub Issue And PR Provider",
            "GITHUB_TOKEN",
            "devctl git mr --title",
            "devctl issue list --state open --limit 20",
            "devctl issue comment <id> --body-file",
            "devctl git pr-get <number>",
            "devctl approval prepare --issue <id> --action <action> --file <reviewed-artifact>",
            "state-update-suggestion.md",
            "Branch Semantics Rule",
            "<!-- workflow-product-line: academic -->",
            "<!-- paper-base-branch:",
            "<!-- task-branch:",
            "After the PR is merged, the task is sealed",
            "Do not invent active approval filenames",
            "Remote-published body files",
            "review-only",
            "Legacy `_ops` Migration",
            "devctl migrate inspect",
            "devctl migrate wrappers",
            "python -m xflow",
            "must not call Bash, WSL, Claude, or any installer",
            ".xflow/issues/issue-<id>/**",
            ".xflow/local/**",
            ".xflow/scope-policy.json",
            "protected hints",
        ),
        "references/academic-schema-contract.md": (
            "templates/ai-rules.json",
            "devctl rules list",
            "devctl rules sync <id>",
            "codex -> AGENTS.md",
            "cursor -> .cursorrules",
            "must not overwrite an existing different file",
            "Windows academic operation must not require WSL",
            "PowerShell Native Command Contract",
            "A native Git command is failed only when its process exit code is non-zero",
            "Legacy Layout Migration Contract",
            "devctl migrate inspect",
            "devctl migrate wrappers",
            "python -m xflow",
            "must not call Bash, WSL, Claude, AcademicForge, or any installer",
            "GitHub Issue And PR Provider Contract",
            "`devctl git mr` in academic Python mode must",
            "metadata writeback must not require a second approval",
            "the task is sealed",
            "devctl check scope --issue <id> --mode review-only",
            "devctl approval prepare --issue <id> --action <action> --file <artifact>",
            "devctl check current-task --issue <id>",
            "devctl.pr-url",
            ".xflow/scope-policy.json",
            "allowlist",
        ),
        "references/academic-templates.md": (
            "<!-- xflow: academic-issue-draft -->",
            "<!-- xflow: academic-mr-draft -->",
            "Claude Skill:",
            "Skill Source:",
            "Invocation:",
            "optional skill arguments",
            "Return Markdown with these exact section headings:",
            "## Proposed Changes",
            "Do not create alternate",
            "Approved: no",
            "## Suggested Command",
            "## .xflow/current-task.md",
            "State Update Suggestion:",
        ),
        "references/academicforge-skill-catalog.md": (
            "/peer-review",
            "/ppw-reviewer-simulation",
            "Scanned `SKILL.md` files: 274",
        ),
    }.items():
        for ref in refs:
            require_ref(file_name, ref)

    for file_name, refs in {
        "references/academic-templates.md": (
            "Target Branch: academic",
            "# Academic Issue Draft",
            "# MR Draft",
            "AcademicForge Skill:",
            ".xflow/issue-<id>/",
        ),
        "references/academic-workflow.md": ("claude mcp add academicforge",),
        "templates/cursorrules.academic": (
            "claude mcp add academicforge",
            "Target Branch: academic",
            "local-review-mr.md` as the active",
        ),
    }.items():
        for ref in refs:
            reject_ref(file_name, ref)

    print("academic entrypoint ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
