#!/usr/bin/env bash
# Ask before destructive shell commands in the docs repo.
set -euo pipefail

input=$(cat)
command=""
if command -v jq >/dev/null 2>&1; then
  command=$(echo "$input" | jq -r '.command // empty')
else
  command=$(python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("command",""))' <<<"$input" 2>/dev/null || true)
fi

if [[ -z "$command" ]]; then
  echo '{ "permission": "allow" }'
  exit 0
fi

if [[ "$command" =~ rm[[:space:]]+-rf|git[[:space:]]+reset[[:space:]]+--hard|git[[:space:]]+clean[[:space:]]+-fd ]]; then
  cat <<EOF
{
  "permission": "ask",
  "user_message": "This command can delete or reset repo content. Review before continuing.",
  "agent_message": "A project hook flagged a potentially destructive shell command in documents/."
}
EOF
  exit 0
fi

echo '{ "permission": "allow" }'
exit 0
