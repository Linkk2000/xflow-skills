#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

require_ref() {
  local file="$1" ref="$2"
  grep -Fq "$ref" "$ROOT/$file" || {
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

echo "academic entrypoint ok"
