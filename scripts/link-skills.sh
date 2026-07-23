#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/link-skills.sh [--apply] [--agent claude|codex]...
                              [--home DIR] [--codex-home DIR]

Preview or create development symlinks for this repository's skills.

The default is a dry run for both Claude Code and Codex. Nothing is written
unless --apply is present. Existing files, directories, and symlinks pointing
somewhere else are treated as collisions and are never moved or overwritten.

Options:
  --apply            Create the planned directories and symlinks.
  --agent NAME       Limit the operation to an agent (repeatable).
  --home DIR         Home used for agent directories (default: current home).
  --codex-home DIR   Override the Codex directory (default: HOME/.codex or
                     the existing CODEX_HOME when --home is not supplied).
  -h, --help         Show this help.
EOF
}

die() {
  echo "error: $*" >&2
  exit 1
}

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
apply=false
home_root="${HOME:-}"
home_overridden=false
codex_root=""
agents=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --apply)
      apply=true
      shift
      ;;
    --agent)
      [ "$#" -ge 2 ] || die "--agent requires claude or codex"
      case "$2" in
        claude|codex) agents="${agents}${agents:+ }$2" ;;
        *) die "unsupported agent '$2' (expected claude or codex)" ;;
      esac
      shift 2
      ;;
    --home)
      [ "$#" -ge 2 ] || die "--home requires a directory"
      home_root="$2"
      home_overridden=true
      shift 2
      ;;
    --codex-home)
      [ "$#" -ge 2 ] || die "--codex-home requires a directory"
      codex_root="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument '$1'"
      ;;
  esac
done

[ -n "$agents" ] || agents="claude codex"

needs_home=false
selects_codex=false
for agent in $agents; do
  case "$agent" in
    claude) needs_home=true ;;
    codex) selects_codex=true ;;
  esac
done

if [ "$selects_codex" = true ] && [ -z "$codex_root" ]; then
  if [ "$home_overridden" = false ] && [ -n "${CODEX_HOME:-}" ]; then
    codex_root="$CODEX_HOME"
  else
    needs_home=true
  fi
fi

if [ "$needs_home" = true ]; then
  [ -n "$home_root" ] || die "HOME must be set or --home must be provided for the selected agent destinations"
  case "$home_root" in
    /*) ;;
    *) die "HOME and --home must be absolute paths" ;;
  esac
fi

if [ "$selects_codex" = true ]; then
  [ -n "$codex_root" ] || codex_root="$home_root/.codex"
  case "$codex_root" in
    /*) ;;
    *) die "--codex-home and CODEX_HOME must be absolute paths" ;;
  esac
fi

skill_count=0
for skill_md in "$repo_root"/skills/*/SKILL.md; do
  [ -f "$skill_md" ] || continue
  [ ! -L "$skill_md" ] || die "skill manifests may not be symlinks: $skill_md"
  skill_dir="$(dirname "$skill_md")"
  [ ! -L "$skill_dir" ] || die "skill directories may not be symlinks: $skill_dir"
  skill_count=$((skill_count + 1))
done
[ "$skill_count" -gt 0 ] || die "no skills found under $repo_root/skills"

destination_for() {
  case "$1" in
    claude) printf '%s\n' "$home_root/.claude/skills" ;;
    codex) printf '%s\n' "$codex_root/skills" ;;
    *) return 1 ;;
  esac
}

# Validate the complete plan before creating anything. This prevents a
# collision in one destination from leaving the other destination half-linked.
collision=false
for agent in $agents; do
  destination="$(destination_for "$agent")"
  if [ -L "$destination" ] || { [ -e "$destination" ] && [ ! -d "$destination" ]; }; then
    echo "error: destination must be a real directory: $destination" >&2
    collision=true
    continue
  fi

  for skill_md in "$repo_root"/skills/*/SKILL.md; do
    [ -f "$skill_md" ] || continue
    source_dir="$(dirname "$skill_md")"
    skill_name="$(basename "$source_dir")"
    target="$destination/$skill_name"

    if [ -L "$target" ]; then
      if [ "$(readlink "$target")" != "$source_dir" ]; then
        echo "error: refusing to replace symlink $target -> $(readlink "$target")" >&2
        collision=true
      fi
    elif [ -e "$target" ]; then
      echo "error: refusing to move or replace existing path $target" >&2
      collision=true
    fi
  done
done

[ "$collision" = false ] || exit 1

for agent in $agents; do
  destination="$(destination_for "$agent")"
  if [ "$apply" = true ]; then
    mkdir -p "$destination"
  fi

  for skill_md in "$repo_root"/skills/*/SKILL.md; do
    [ -f "$skill_md" ] || continue
    source_dir="$(dirname "$skill_md")"
    skill_name="$(basename "$source_dir")"
    target="$destination/$skill_name"

    if [ -L "$target" ]; then
      echo "unchanged [$agent] $skill_name -> $source_dir"
    elif [ "$apply" = true ]; then
      ln -s "$source_dir" "$target"
      echo "linked [$agent] $skill_name -> $source_dir"
    else
      echo "would link [$agent] $skill_name -> $source_dir"
    fi
  done
done

if [ "$apply" = false ]; then
  echo "Dry run only; re-run with --apply to create these links."
fi
