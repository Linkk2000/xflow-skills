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

require_ref "templates/cursorrules.academic" "devctl claude doctor"
require_ref "templates/cursorrules.academic" "devctl claude run --issue <id>"
require_ref "templates/cursorrules.academic" "--body-file"
require_ref "references/academic-workflow.md" "templates/cursorrules.academic"
require_ref "references/academic-schema-contract.md" "templates/cursorrules.academic"

echo "academic entrypoint ok"
