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

require_ref "references/issue-template.md" "<!-- xflow: issue-draft -->"
require_ref "references/issue-template.md" "<!-- xflow: mr-draft -->"
require_ref "references/issue-template.md" "# Local Review Approval"
require_ref "references/issue-template.md" "Approved Action: <issue-create|issue-comment|issue-close|git-mr|remote-write>"
require_ref "references/issue-template.md" "Do not include internal-only visible titles"
require_ref "references/xflow-map.md" "devctl check issue-draft"
require_ref "references/xflow-map.md" "devctl check mr-draft"
require_ref "references/xflow-map.md" "devctl check local-review"
require_ref "references/xflow-map.md" 'devctl git mr --title "<title>" --body-file'
require_ref "SKILL.md" "Core Remote Write Review Gate"
require_ref "SKILL.md" "issue-create"
require_ref "SKILL.md" "git-mr"

reject_ref "references/xflow-map.md" 'devctl git mr --title "<title>" --body "<body>"'

echo "main entrypoint ok"
