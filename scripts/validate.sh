#!/usr/bin/env bash
set -euo pipefail

SKILL_VALIDATOR_VERSION="1.5.6"
ACTIONLINT_VERSION="1.7.12"

usage() {
  cat <<'EOF'
Usage: ./scripts/validate.sh [--repo-root DIR] [--skip-linker]

Run the deterministic validation suite used by CI. Pinned validator binaries
are downloaded to a temporary directory only when the exact expected version
is not already installed.

Options:
  --repo-root DIR  Validate another checkout as data.
  --skip-linker    Do not execute the isolated linker behavior test. This is
                   required when an untrusted pull-request tree is the target.
  -h, --help       Show this help.
EOF
}

die() {
  echo "error: $*" >&2
  exit 1
}

script_dir="$(cd "$(dirname "$0")" && pwd -P)"
trusted_repo_root="$(cd "$script_dir/.." && pwd -P)"
repo_root="$trusted_repo_root"
skip_linker=false

while [ "$#" -gt 0 ]; do
  case "$1" in
    --repo-root)
      [ "$#" -ge 2 ] || die "--repo-root requires a directory"
      repo_root="$2"
      shift 2
      ;;
    --skip-linker)
      skip_linker=true
      shift
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

[ -d "$repo_root" ] || die "repository root is not a directory: $repo_root"
repo_root="$(cd "$repo_root" && pwd -P)"
if [ "$skip_linker" = false ] && [ "$repo_root" != "$trusted_repo_root" ]; then
  die "--skip-linker is required when --repo-root targets another checkout"
fi

for required_command in curl tar python3 shellcheck gh; do
  command -v "$required_command" >/dev/null 2>&1 || die "$required_command is required"
done
python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' || \
  die "Python 3.10 or newer is required"
gh skill publish --help >/dev/null 2>&1 || die "this GitHub CLI does not provide 'gh skill publish'"

tool_tmp="$(mktemp -d "${TMPDIR:-/tmp}/skills-validation.XXXXXX")"
cleanup() {
  if [ -n "${tool_tmp:-}" ] && [ -d "$tool_tmp" ]; then
    rm -rf -- "$tool_tmp"
  fi
}
trap cleanup EXIT HUP INT TERM

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    die "sha256sum or shasum is required to verify downloaded tools"
  fi
}

platform_asset() {
  os_name="$(uname -s)"
  machine="$(uname -m)"
  case "$os_name" in
    Darwin) os_name="darwin" ;;
    Linux) os_name="linux" ;;
    *) die "unsupported validation host: $os_name" ;;
  esac
  case "$machine" in
    x86_64|amd64) machine="amd64" ;;
    arm64|aarch64) machine="arm64" ;;
    *) die "unsupported validation architecture: $machine" ;;
  esac
  printf '%s_%s\n' "$os_name" "$machine"
}

expected_checksum() {
  tool_name="$1"
  asset_platform="$2"
  case "$tool_name:$asset_platform" in
    skill-validator:darwin_amd64) echo "c66c10f70244ce6a87c6db0f122d72a6d85f7691c094240cd58a3c952f743ec6" ;;
    skill-validator:darwin_arm64) echo "38f838c4103e0fd1897154ba0236ce59218011ba2c639c0cadf9f36e4e7a6572" ;;
    skill-validator:linux_amd64) echo "c97faee388056023c616e312927faffd07e028bcd76d799e42da612dad7972df" ;;
    skill-validator:linux_arm64) echo "62c1ae0aaf5c0892ac7f1f04864f5b7cd13d6b1e7d268129e44fb87d067ee238" ;;
    actionlint:darwin_amd64) echo "5b44c3bc2255115c9b69e30efc0fecdf498fdb63c5d58e17084fd5f16324c644" ;;
    actionlint:darwin_arm64) echo "aba9ced2dee8d27fecca3dc7feb1a7f9a52caefa1eb46f3271ea66b6e0e6953f" ;;
    actionlint:linux_amd64) echo "8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8" ;;
    actionlint:linux_arm64) echo "325e971b6ba9bfa504672e29be93c24981eeb1c07576d730e9f7c8805afff0c6" ;;
    *) die "no checksum is pinned for $tool_name on $asset_platform" ;;
  esac
}

download_tool() {
  tool_name="$1"
  version="$2"
  repository="$3"
  asset_platform="$(platform_asset)"
  destination_dir="$tool_tmp/$tool_name"
  archive_name="${tool_name}_${version}_${asset_platform}.tar.gz"
  archive_path="$tool_tmp/$archive_name"
  checksum="$(expected_checksum "$tool_name" "$asset_platform")"

  mkdir -p "$destination_dir"
  curl --disable --fail --silent --show-error --location \
    --proto '=https' \
    --proto-redir '=https' \
    --connect-timeout 10 \
    --max-time 60 \
    "https://github.com/$repository/releases/download/v$version/$archive_name" \
    --output "$archive_path"
  actual_checksum="$(sha256_file "$archive_path")"
  [ "$actual_checksum" = "$checksum" ] || \
    die "checksum mismatch for $archive_name (expected $checksum, got $actual_checksum)"
  tar -xzf "$archive_path" -C "$destination_dir"
  [ -x "$destination_dir/$tool_name" ] || die "$archive_name did not contain $tool_name"
  printf '%s\n' "$destination_dir/$tool_name"
}

skill_validator_bin=""
if command -v skill-validator >/dev/null 2>&1 && \
  skill-validator --version 2>&1 | grep -Eq "(^|[^0-9])v?${SKILL_VALIDATOR_VERSION}([^0-9]|$)"; then
  skill_validator_bin="$(command -v skill-validator)"
else
  skill_validator_bin="$(download_tool \
    skill-validator \
    "$SKILL_VALIDATOR_VERSION" \
    agent-ecosystem/skill-validator)"
fi

actionlint_bin=""
if command -v actionlint >/dev/null 2>&1 && \
  actionlint -version 2>&1 | grep -Eq "^${ACTIONLINT_VERSION}([[:space:]]|$)"; then
  actionlint_bin="$(command -v actionlint)"
else
  actionlint_bin="$(download_tool actionlint "$ACTIONLINT_VERSION" rhysd/actionlint)"
fi

echo "==> Tool versions"
"$skill_validator_bin" --version
"$actionlint_bin" -version | sed -n '1p'
shellcheck --version | sed -n '1,2p'
python3 --version
gh --version | sed -n '1p'

echo "==> Strict Agent Skills structure (agents/ intentionally allowlisted)"
NO_COLOR=1 "$skill_validator_bin" validate structure \
  --strict \
  --allow-dirs=agents \
  "$repo_root/skills"

echo "==> GitHub skill publisher dry run (warnings are failures)"
publisher_output="$tool_tmp/gh-skill-publish.txt"
if ! (cd "$repo_root" && NO_COLOR=1 GH_PAGER=cat gh skill publish --dry-run .) \
  >"$publisher_output" 2>&1; then
  sed -n '1,240p' "$publisher_output" >&2
  die "gh skill publish --dry-run failed"
fi
sed -n '1,240p' "$publisher_output"
if grep -Eiq '(^|[[:space:]])warning[[:space:]]' "$publisher_output"; then
  die "gh skill publish --dry-run emitted a warning"
fi

echo "==> Catalog, references, OpenAI manifests, and workflow security"
python3 "$script_dir/check-repository.py" "$repo_root"

echo "==> Python scripts (compile-only; never imported)"
python3 -I "$script_dir/check-python-syntax.py" "$repo_root/scripts"

echo "==> Python syntax negative fixture"
python3 -I "$script_dir/test-python-syntax.py"

echo "==> Workflow security negative fixtures"
PYTHONDONTWRITEBYTECODE=1 python3 "$script_dir/test-repository-checks.py"

echo "==> External-link SSRF negative fixtures"
PYTHONDONTWRITEBYTECODE=1 python3 "$script_dir/test-external-link-safety.py"

echo "==> Shell scripts (analyzed, never sourced)"
if [ -d "$repo_root/scripts" ]; then
  find "$repo_root/scripts" -type f -name '*.sh' -exec shellcheck --severity=style {} +
fi

echo "==> GitHub Actions syntax"
workflow_count="$(find "$repo_root/.github/workflows" -type f \( -name '*.yml' -o -name '*.yaml' \) | wc -l | tr -d ' ')"
[ "$workflow_count" -gt 0 ] || die "no GitHub Actions workflows found"
find "$repo_root/.github/workflows" -type f \( -name '*.yml' -o -name '*.yaml' \) \
  -exec "$actionlint_bin" -shellcheck="$(command -v shellcheck)" {} +

if [ "$skip_linker" = false ]; then
  echo "==> Linker behavior (isolated temporary home)"
  "$script_dir/test-link-skills.sh"
else
  echo "==> Linker behavior skipped for untrusted data tree"
fi

echo "All deterministic validation passed."
