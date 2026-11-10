# scripts/

个人工具脚本，按使用场景分类。

## rclone 挂载

| 脚本 | 用途 | 用法 |
|------|------|------|
| `rclone.sh` | Linux 下挂载 OpenList | 配置 rclone 的 `alist:` 远程，创建 `~/rclone/alist` 目录后运行；脚本检查本机 5244 端口并在前台挂载 |
| `rclone.ps1` | Windows 下挂载 alist | 配置 `alist:` 远程后运行，挂载为 `Z:`，缓存放在 `D:\alist-cache` |

挂载路径和远程名称目前在脚本中配置，使用前按本机环境调整。Windows restic 配置可能依赖 `Z:` 挂载，修改时需同步核对。

## 安装工具

| 脚本 | 用途 | 用法 |
|------|------|------|
| `install-mouseless.sh` | 安装 Mouseless 并启用系统服务 | `bash install-mouseless.sh`；支持通过 `BIN_DIR`、`SERVICE_DIR`、`CONFIG` 指定安装和配置路径，下载 Linux amd64 版本 |

## Shell 工具函数

| 脚本 | Shell | 功能 |
|------|-------|------|
| `custom.nu` | Nushell | 在 Windows 下将 Docker context 指向 WSL 中的 Docker，并设置使用 Scoop cwrsync SSH 的 `rsync` 别名 |

## 依赖

- `rclone.sh`：rclone、xh、umount，以及可访问的本机 OpenList 服务。
- `rclone.ps1`：PowerShell、rclone 及其 Windows 挂载依赖。
- `install-mouseless.sh`：curl、tar、sudo、systemd。
- `custom.nu`：Nushell、WSL、Docker CLI、Scoop cwrsync。

Arch Linux 软件包清单位于 [`../packages/pkglist-all.txt`](../packages/pkglist-all.txt)。
