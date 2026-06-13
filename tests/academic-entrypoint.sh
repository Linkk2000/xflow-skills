#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

require_ref() {
  local file="$1" ref="$2"
  grep -Fq -- "$ref" "$ROOT/$file" || {
    echo "missing reference '$ref' in $file" >&2
    exit 1
  }
}

reject_ref() {
  local file="$1" ref="$2"
  if grep -Fq -- "$ref" "$ROOT/$file"; then
    echo "obsolete reference '$ref' in $file" >&2
    exit 1
  fi
}

for ref in \
  "references/academic-workflow.md" \
  "references/academic-templates.md" \
  "references/academic-schema-contract.md"
do
  require_ref "SKILL.md" "$ref"
  require_ref "references/xflow-map.md" "$ref"
done

require_ref "SKILL.md" "PowerShell Native Command Safety"
require_ref "SKILL.md" "Invoke-XFlowGit -GitArguments @(...)"
require_ref ".gitignore" "__pycache__/"
require_ref ".gitignore" "*.py[cod]"
require_ref ".gitignore" ".pytest_cache/"
require_ref ".gitignore" "*.tmp"
require_ref "templates/cursorrules.academic" "devctl claude doctor"
require_ref "templates/cursorrules.academic" "devctl claude run --issue <id>"
require_ref "templates/cursorrules.academic" "--body-file"
require_ref "templates/cursorrules.academic" "fetch, pin reviewed SHA, test, human review, then commit"
require_ref "templates/cursorrules.academic" 'Do not pipe native Git commands through `2>&1 | Out-String`'
require_ref "templates/cursorrules.academic" '$LASTEXITCODE'
require_ref "templates/cursorrules.academic" ".xflow/tools/xflow-powershell-native.ps1"
require_ref "templates/cursorrules.academic" "Do not combine multiple native commands in one PowerShell line"
require_ref "templates/cursorrules.academic" "PowerShell check scripts must use ASCII terminal output"
require_ref "templates/cursorrules.academic" "Initialize-XFlowPowerShellEncoding"
require_ref "templates/cursorrules.academic" "Write-XFlowStatus"
require_ref "templates/cursorrules.academic" "Git-facing text only"
require_ref "templates/cursorrules.academic" "commit messages, remote Issue titles/bodies, and MR/PR"
require_ref "templates/cursorrules.academic" "titles/bodies should follow the user's language"
require_ref "templates/cursorrules.academic" "Chinese, use Chinese as the primary language"
require_ref "templates/cursorrules.academic" "apply to non-Git artifacts"
require_ref "templates/cursorrules.academic" "ignore = untracked"
require_ref "templates/cursorrules.academic" "devctl check submodule-hygiene"
require_ref "templates/cursorrules.academic" "Workflow Product Line"
require_ref "templates/cursorrules.academic" "Paper Base Branch"
require_ref "templates/cursorrules.academic" "Task Branch"
require_ref "templates/cursorrules.academic" 'Do not create or push an `academic` branch in the paper repository'
require_ref "templates/xflow-powershell-native.ps1" "function Invoke-XFlowNative"
require_ref "templates/xflow-powershell-native.ps1" "function Invoke-XFlowGit"
require_ref "templates/xflow-powershell-native.ps1" "function Initialize-XFlowPowerShellEncoding"
require_ref "templates/xflow-powershell-native.ps1" "function Write-XFlowStatus"
require_ref "templates/xflow-powershell-native.ps1" "GitArguments"
require_ref "templates/xflow-powershell-native.ps1" "Start-Process"
require_ref "templates/xflow-powershell-native.ps1" "ExitCode"
require_ref "references/academic-workflow.md" "templates/cursorrules.academic"
require_ref "references/academic-workflow.md" "templates/xflow-powershell-native.ps1"
require_ref "references/academic-workflow.md" "Already-initialized paper repositories must not silently track the latest"
require_ref "references/academic-workflow.md" "manuscript/"
require_ref "references/academic-workflow.md" "assets/"
require_ref "references/academic-workflow.md" ".xflow/ops/devctl"
require_ref "references/academic-workflow.md" ".xflow/ops/workflow"
require_ref "references/academic-workflow.md" ".xflow/issues/issue-<id>/"
require_ref "references/academic-workflow.md" ".xflow/local/"
require_ref "references/academic-workflow.md" "git -C .xflow/ops/devctl fetch origin academic"
require_ref "references/academic-workflow.md" "pin reviewed SHA"
require_ref "references/academic-workflow.md" "commit the submodule pointer"
require_ref "references/academic-workflow.md" "ignore = untracked"
require_ref "references/academic-workflow.md" "devctl check submodule-hygiene"
require_ref "references/academic-workflow.md" "PowerShell Native Git Rule"
require_ref "references/academic-workflow.md" "GitHub Issue And PR Provider"
require_ref "references/academic-workflow.md" "GITHUB_TOKEN"
require_ref "references/academic-workflow.md" "devctl git mr --title"
require_ref "references/academic-workflow.md" 'Do not use `2>&1 | Out-String` for `git submodule add`, `git clone`, `git fetch`, or `git checkout`'
require_ref "references/academic-workflow.md" "Do not combine multiple native commands in one PowerShell line"
require_ref "references/academic-workflow.md" "Branch Semantics Rule"
require_ref "references/academic-workflow.md" "Workflow Product Line: academic"
require_ref "references/academic-workflow.md" "Paper Base Branch:"
require_ref "references/academic-workflow.md" "Task Branch:"
require_ref "references/academic-schema-contract.md" "templates/cursorrules.academic"
require_ref "references/academic-schema-contract.md" "Pinned Update Contract"
require_ref "references/academic-schema-contract.md" "fetch -> pin reviewed SHA -> test -> human review -> commit"
require_ref "references/academic-schema-contract.md" "PowerShell Native Command Contract"
require_ref "references/academic-schema-contract.md" "A native Git command is failed only when its process exit code is non-zero"
require_ref "references/academic-schema-contract.md" "PowerShell helper template"
require_ref "references/academic-schema-contract.md" "native command composition"
require_ref "references/academic-schema-contract.md" "Submodule Hygiene Contract"
require_ref "references/academic-schema-contract.md" "devctl check submodule-hygiene"
require_ref "references/academic-schema-contract.md" ".xflow/ops/devctl"
require_ref "references/academic-schema-contract.md" ".xflow/ops/workflow"
require_ref "references/academic-schema-contract.md" ".xflow/issues/issue-<id>/"
require_ref "references/academic-schema-contract.md" "Branch Semantics Contract"
require_ref "references/academic-schema-contract.md" "GitHub Issue And PR Provider Contract"
require_ref "references/academic-schema-contract.md" '`devctl git mr` in academic Python mode must'
require_ref "templates/cursorrules.academic" "For GitHub PR creation"
require_ref "templates/cursorrules.academic" 'devctl git mr --title "<title>" --body-file <file> --base <paper-base> --issue <id>'
require_ref "references/academic-schema-contract.md" 'If `XFLOW_PLATFORM=gitee`, the Python academic provider must fail closed'
require_ref "references/academic-schema-contract.md" '`Target Branch: academic` is invalid'
require_ref "references/academic-templates.md" "Workflow Product Line: academic"
require_ref "references/academic-templates.md" "Paper Base Branch: <main|master|user-defined>"
require_ref "references/academic-templates.md" "Task Branch: <feature/<issue>-<slug>|review/<issue>-<slug>|chore/update-academic-xflow-<date>>"

reject_ref "references/academic-templates.md" "Target Branch: academic"
reject_ref "templates/cursorrules.academic" "Target Branch: academic"
reject_ref "references/academic-workflow.md" "_ops/"
reject_ref "templates/cursorrules.academic" "_ops/"
reject_ref "references/academic-templates.md" ".xflow/issue-<id>/"

echo "academic entrypoint ok"
