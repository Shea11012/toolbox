#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法: sync.sh [--dry-run]

将脚本所在目录的 *.hook 安装到 /etc/pacman.d/hooks/。
仅覆盖同名文件，保留目标目录中的其他 hook。

选项:
  -n, --dry-run  预览待同步文件，不写入，也不请求 sudo 权限
  -h, --help     显示帮助
EOF
}

dry_run=false
for arg in "$@"; do
  case "$arg" in
    -n|--dry-run) dry_run=true ;;
    -h|--help) usage; exit 0 ;;
    *) printf '未知参数: %s\n' "$arg" >&2; usage >&2; exit 1 ;;
  esac
done

source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
target_dir=/etc/pacman.d/hooks
shopt -s nullglob
hooks=("$source_dir"/*.hook)

if (( ${#hooks[@]} == 0 )); then
  printf '没有找到 hook 文件: %s\n' "$source_dir" >&2
  exit 1
fi

for hook in "${hooks[@]}"; do
  if [[ ! -f "$hook" || ! -r "$hook" ]]; then
    printf 'hook 不是可读的普通文件: %s\n' "$hook" >&2
    exit 1
  fi
  printf '%s -> %s/%s\n' "$hook" "$target_dir" "${hook##*/}"
done

if "$dry_run"; then
  exit 0
fi

privilege=()
if (( EUID != 0 )); then
  privilege=(sudo)
fi

"${privilege[@]}" install -d -o root -g root -m 0755 -- "$target_dir"
for hook in "${hooks[@]}"; do
  "${privilege[@]}" install -T -o root -g root -m 0644 -- "$hook" "$target_dir/${hook##*/}"
done
printf '已同步 %d 个 hook。\n' "${#hooks[@]}"
