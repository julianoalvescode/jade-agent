#!/usr/bin/env bash

set -euo pipefail

target_agent="${1:-claude-code}"

case "$target_agent" in
  claude-code|codex|cursor|github-copilot|windsurf|gemini-cli|cline|universal)
    ;;
  *)
    echo "Agente não suportado: $target_agent" >&2
    echo "Use: claude-code, codex, cursor, github-copilot, windsurf, gemini-cli, cline ou universal." >&2
    exit 2
    ;;
esac

if ! command -v node >/dev/null 2>&1 || ! command -v npx >/dev/null 2>&1; then
  echo "Node.js e npx são necessários para instalar as skills." >&2
  exit 1
fi

export DISABLE_TELEMETRY="${DISABLE_TELEMETRY:-1}"

install_from_repo() {
  local repository="$1"
  shift

  local arguments=(--yes skills@latest add "$repository" --agent "$target_agent" --copy --yes)
  local skill_name

  for skill_name in "$@"; do
    arguments+=(--skill "$skill_name")
  done

  npx "${arguments[@]}"
}

install_from_repo "https://github.com/anthropics/skills" \
  frontend-design \
  webapp-testing

install_from_repo "https://github.com/hersti/ui-engineering" \
  ui-recon

install_from_repo "https://github.com/thrillmade/agent-skills" \
  spacing-system

install_from_repo "https://github.com/figma/mcp-server-guide" \
  figma-design-to-code

install_from_repo "https://github.com/vercel-labs/agent-skills" \
  vercel-react-best-practices \
  vercel-composition-patterns \
  web-design-guidelines

install_from_repo "https://github.com/mattpocock/skills" \
  domain-modeling \
  tdd

install_from_repo "https://github.com/addyosmani/agent-skills" \
  api-and-interface-design \
  code-review-and-quality

install_from_repo "https://github.com/wshobson/agents" \
  javascript-testing-patterns

install_from_repo "https://github.com/claude-dev-suite/claude-dev-suite" \
  typescript-quality

install_from_repo "https://github.com/currents-dev/playwright-best-practices-skill" \
  playwright-best-practices

install_from_repo "https://github.com/asyrafhussin/agent-skills" \
  state-management

install_from_repo "https://github.com/pproenca/dot-skills" \
  react-hook-form

install_from_repo "https://github.com/sergiodxa/agent-skills" \
  owasp-security-check

install_from_repo "https://github.com/obra/superpowers" \
  systematic-debugging \
  verification-before-completion

echo "Skills instaladas para $target_agent no projeto atual. Reinicie o agente para carregá-las."
