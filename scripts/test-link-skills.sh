#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
linker="$repo_root/scripts/link-skills.sh"
test_root="$(mktemp -d "${TMPDIR:-/tmp}/skills-link-test.XXXXXX")"

cleanup() {
  if [ -n "${test_root:-}" ] && [ -d "$test_root" ]; then
    rm -rf -- "$test_root"
  fi
}
trap cleanup EXIT HUP INT TERM

preview_home="$test_root/preview-home"
env -u HOME "$linker" --home "$preview_home" >/dev/null
[ ! -e "$preview_home" ] || {
  echo "error: linker dry run wrote to $preview_home" >&2
  exit 1
}

codex_only_root="$test_root/codex-only"
env -u HOME "$linker" --agent codex --codex-home "$codex_only_root" >/dev/null
[ ! -e "$codex_only_root" ] || {
  echo "error: Codex-only linker dry run wrote to $codex_only_root" >&2
  exit 1
}

apply_home="$test_root/apply-home"
"$linker" --apply --home "$apply_home" >/dev/null
"$linker" --apply --home "$apply_home" >/dev/null

for skill_md in "$repo_root"/skills/*/SKILL.md; do
  [ -f "$skill_md" ] || continue
  source_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$source_dir")"
  for target in \
    "$apply_home/.claude/skills/$skill_name" \
    "$apply_home/.codex/skills/$skill_name"; do
    [ -L "$target" ] || {
      echo "error: linker did not create $target" >&2
      exit 1
    }
    [ "$(readlink "$target")" = "$source_dir" ] || {
      echo "error: linker created the wrong target for $target" >&2
      exit 1
    }
  done
done

collision_home="$test_root/collision-home"
first_skill_md=""
for skill_md in "$repo_root"/skills/*/SKILL.md; do
  [ -f "$skill_md" ] || continue
  first_skill_md="$skill_md"
  break
done
[ -n "$first_skill_md" ] || {
  echo "error: no skill available for collision test" >&2
  exit 1
}
first_skill="$(basename "$(dirname "$first_skill_md")")"
mkdir -p "$collision_home/.claude/skills/$first_skill"

if "$linker" --apply --home "$collision_home" >/dev/null 2>&1; then
  echo "error: linker accepted an existing destination collision" >&2
  exit 1
fi
[ ! -e "$collision_home/.codex" ] || {
  echo "error: linker wrote a partial plan before reporting a collision" >&2
  exit 1
}

echo "Linker behavior passed in an isolated home."
