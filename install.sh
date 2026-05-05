#!/usr/bin/env bash
set -euo pipefail

REPO_OWNER="${AGENT_ROUTER_REPO_OWNER:-st-devl}"
REPO_NAME="${AGENT_ROUTER_REPO_NAME:-Global_Router_codex}"
REPO_BRANCH="${AGENT_ROUTER_REPO_BRANCH:-main}"
INSTALL_DIR="${AGENT_ROUTER_HOME:-$HOME/.agent-router}"
ZSHRC="${ZDOTDIR:-$HOME}/.zshrc"

log() {
  printf '%s\n' "$*"
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$1" >&2
    exit 1
  fi
}

find_source_dir() {
  local script_dir=""

  if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$script_dir/router.py" ] && [ -d "$script_dir/skills" ] && [ -d "$script_dir/bin" ]; then
      printf '%s\n' "$script_dir"
      return 0
    fi
  fi

  require_cmd curl
  require_cmd tar

  local tmp_dir
  tmp_dir="$(mktemp -d)"
  AGENT_ROUTER_TMP_DIR="$tmp_dir"
  export AGENT_ROUTER_TMP_DIR

  local archive_url="https://github.com/${REPO_OWNER}/${REPO_NAME}/archive/refs/heads/${REPO_BRANCH}.tar.gz"
  curl -fsSL "$archive_url" | tar -xz -C "$tmp_dir" --strip-components=1
  printf '%s\n' "$tmp_dir"
}

cleanup() {
  if [ -n "${AGENT_ROUTER_TMP_DIR:-}" ] && [ -d "$AGENT_ROUTER_TMP_DIR" ]; then
    rm -rf "$AGENT_ROUTER_TMP_DIR"
  fi
}
trap cleanup EXIT

install_files() {
  local source_dir="$1"

  install -d "$INSTALL_DIR"
  install -d "$INSTALL_DIR/bin"
  install -d "$INSTALL_DIR/skills"
  install -d "$INSTALL_DIR/templates"
  install -d "$INSTALL_DIR/tests"

  install -m 0755 "$source_dir/router.py" "$INSTALL_DIR/router.py"

  if [ -f "$source_dir/VERSION" ]; then
    install -m 0644 "$source_dir/VERSION" "$INSTALL_DIR/VERSION"
  else
    printf 'unknown\n' > "$INSTALL_DIR/VERSION"
  fi

  local command_file
  for command_file in "$source_dir"/bin/*; do
    [ -f "$command_file" ] || continue
    install -m 0755 "$command_file" "$INSTALL_DIR/bin/$(basename "$command_file")"
  done

  install -m 0644 "$source_dir/templates/PROJECT_AGENTS_SHORT.md" "$INSTALL_DIR/templates/PROJECT_AGENTS_SHORT.md"

  if [ -d "$source_dir/tests" ]; then
    local test_file
    for test_file in "$source_dir"/tests/*; do
      [ -f "$test_file" ] || continue
      install -m 0644 "$test_file" "$INSTALL_DIR/tests/$(basename "$test_file")"
    done
  fi

  local skill_dir
  for skill_dir in "$source_dir"/skills/*; do
    [ -d "$skill_dir" ] || continue
    install -d "$INSTALL_DIR/skills/$(basename "$skill_dir")"
    install -m 0644 "$skill_dir/SKILL.md" "$INSTALL_DIR/skills/$(basename "$skill_dir")/SKILL.md"
  done
}

install_shell_block() {
  require_cmd python3
  touch "$ZSHRC"

  local block
  block='# >>> Agent Router >>>
export AGENT_ROUTER_HOME="${AGENT_ROUTER_HOME:-$HOME/.agent-router}"
case ":$PATH:" in
  *":$AGENT_ROUTER_HOME/bin:"*) ;;
  *) export PATH="$AGENT_ROUTER_HOME/bin:$PATH" ;;
esac
# <<< Agent Router <<<'

  AGENT_ROUTER_BLOCK="$block" AGENT_ROUTER_ZSHRC="$ZSHRC" python3 - <<'PY'
import os
import re
from pathlib import Path

zshrc = Path(os.environ["AGENT_ROUTER_ZSHRC"])
block = os.environ["AGENT_ROUTER_BLOCK"].rstrip() + "\n"
begin = "# >>> Agent Router >>>"
end = "# <<< Agent Router <<<"

text = zshrc.read_text(encoding="utf-8") if zshrc.exists() else ""
pattern = re.compile(r"# >>> Agent Router >>>.*?# <<< Agent Router <<<\n?", re.S)

if pattern.search(text):
    text = pattern.sub(block, text)
elif begin in text or end in text:
    raise SystemExit("Found a partial Agent Router shell block. Please inspect ~/.zshrc manually.")
else:
    if text and not text.endswith("\n"):
        text += "\n"
    text += "\n" + block

zshrc.write_text(text, encoding="utf-8")
PY
}

main() {
  require_cmd python3

  local source_dir
  source_dir="$(find_source_dir)"

  install_files "$source_dir"
  install_shell_block

  log "Agent Router installed into: $INSTALL_DIR"
  log "Commands installed into: $INSTALL_DIR/bin"
  log "Shell PATH block updated in: $ZSHRC"
  log "Run: source ~/.zshrc"
}

main "$@"
