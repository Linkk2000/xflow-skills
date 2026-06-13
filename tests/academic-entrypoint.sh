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
require_ref "templates/cursorrules.academic" "devctl claude doctor"
require_ref "templates/cursorrules.academic" "devctl claude run --issue <id>"
require_ref "templates/cursorrules.academic" "--body-file"
require_ref "templates/cursorrules.academic" "fetch, pin reviewed SHA, test, human review, then commit"
require_ref "templates/cursorrules.academic" 'Do not pipe native Git commands through `2>&1 | Out-String`'
require_ref "templates/cursorrules.academic" '$LASTEXITCODE'
require_ref "templates/cursorrules.academic" ".xflow/tools/xflow-powershell-native.ps1"
require_ref "templates/cursorrules.academic" "Do not combine multiple native commands in one PowerShell line"
require_ref "templates/xflow-powershell-native.ps1" "function Invoke-XFlowNative"
require_ref "templates/xflow-powershell-native.ps1" "function Invoke-XFlowGit"
require_ref "templates/xflow-powershell-native.ps1" "GitArguments"
require_ref "templates/xflow-powershell-native.ps1" "Start-Process"
require_ref "templates/xflow-powershell-native.ps1" "ExitCode"
require_ref "references/academic-workflow.md" "templates/cursorrules.academic"
require_ref "references/academic-workflow.md" "templates/xflow-powershell-native.ps1"
require_ref "references/academic-workflow.md" "Already-initialized paper repositories must not silently track the latest"
require_ref "references/academic-workflow.md" "git -C _ops/devctl fetch origin academic"
require_ref "references/academic-workflow.md" "pin reviewed SHA"
require_ref "references/academic-workflow.md" "commit the submodule pointer"
require_ref "references/academic-workflow.md" "PowerShell Native Git Rule"
require_ref "references/academic-workflow.md" 'Do not use `2>&1 | Out-String` for `git submodule add`, `git clone`, `git fetch`, or `git checkout`'
require_ref "references/academic-workflow.md" "Do not combine multiple native commands in one PowerShell line"
require_ref "references/academic-schema-contract.md" "templates/cursorrules.academic"
require_ref "references/academic-schema-contract.md" "Pinned Update Contract"
require_ref "references/academic-schema-contract.md" "fetch -> pin reviewed SHA -> test -> human review -> commit"
require_ref "references/academic-schema-contract.md" "PowerShell Native Command Contract"
require_ref "references/academic-schema-contract.md" "A native Git command is failed only when its process exit code is non-zero"
require_ref "references/academic-schema-contract.md" "PowerShell helper template"
require_ref "references/academic-schema-contract.md" "native command composition"

echo "academic entrypoint ok"
