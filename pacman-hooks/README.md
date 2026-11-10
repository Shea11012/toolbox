# Pacman hooks

- `99-check-orphans.hook`：升级或卸载后列出孤儿包。
- `99-pacdiff.hook`：升级后列出待处理的 `.pacnew`、`.pacsave` 等文件，需要安装 `pacman-contrib`。

缓存清理由 `pacman-contrib` 提供的 `paccache.timer` 每周执行：

```bash
sudo systemctl enable --now paccache.timer
```

## 同步到系统

从任意工作目录运行脚本，预览或安装本目录的全部 `.hook` 文件：

```bash
~/workspace/mxy/toolbox/pacman-hooks/sync.sh --dry-run
~/workspace/mxy/toolbox/pacman-hooks/sync.sh
```

脚本按需调用 `sudo`，将文件安装到 `/etc/pacman.d/hooks/`，所有者为 `root:root`，权限为 `0644`。同名文件会被覆盖，其他文件保留，无需修改 `pacman.conf`。

删除或重命名仓库中的 hook 后，需要手动删除系统目录中对应的旧文件。
