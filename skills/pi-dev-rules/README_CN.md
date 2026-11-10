# pi-dev-rules

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Agents365-ai/pi-dev-rules?style=flat&logo=github)](https://github.com/Agents365-ai/pi-dev-rules/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Agents365-ai/pi-dev-rules?style=flat&logo=github)](https://github.com/Agents365-ai/pi-dev-rules/network/members)
[![Latest Release](https://img.shields.io/github/v/release/Agents365-ai/pi-dev-rules?logo=github)](https://github.com/Agents365-ai/pi-dev-rules/releases/latest)
[![Last Commit](https://img.shields.io/github/last-commit/Agents365-ai/pi-dev-rules?logo=github)](https://github.com/Agents365-ai/pi-dev-rules/commits/main)

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-2ea44f)](https://agentskills.io)

中文 · [English](README.md)

一个编程助手技能，将指定版本的 [Pi](https://pi.dev) 文档（`@earendil-works/pi-coding-agent`）
打包为按需参考库，让助手无需重新抓取文档即可安装、配置、运行和**扩展 Pi**。

本地技能修订版 **0.1.5**，于 **2026-11-10** 使用本机官方 Pi **1.5.0** 安装包刷新，涵盖全部 42 篇 Markdown 文档、包 README 和最近 12 个版本的更新记录。原技能仓库在更新时返回 HTTP 404，因此这是本地刷新，并非上游发布版。npm 包目录保留 2026-07-17 的快照（5,249 个包）。

适用于 Claude Code、Cursor、Codex、Copilot、Windsurf、Cline / Roo Code、Gemini CLI、
Aider、Zed、OpenCode、OpenClaw / ClawHub、Hermes、pi-mono — 以及主流国产编程助手
（Trae、Qwen Code / 通义灵码、百度 Comate、CodeGeeX）— 和任何支持 `AGENTS.md`
或 [Agent Skills](https://agentskills.io) 格式的工具。

<p align="center">
  <img src="assets/workflow-zh.png" width="700" alt="pi-dev-rules 工作流程">
</p>

## 包含内容

- `SKILL.md` — 概述、使用时机、速查表、硬性规则、参考索引。
- `references/cli-and-usage.md` — 安装、认证、CLI 参数、斜杠命令、消息队列、上下文
  文件、环境变量、会话、快捷键。
- `references/providers-and-models.md` — 提供商（30+）、`auth.json`（+ scoped `env`）、云
  提供商、自定义 `models.json`、`compat`、自定义提供商扩展。
- `references/settings-and-compaction.md` — `settings.json`（trust/analytics/retry/transport）、
  自动/手动压缩、分支摘要。
- `references/extending-pi.md` — 扩展 API、技能（SKILL.md）、提示模板、主题、包。
- `references/mcp.md` — 内置 MCP、配置、OAuth、资源和 SDK 集成。
- `references/codemode.md` — QuickJS 工具脚本、结构化返回值、分类与图像生成。
- `references/virtual-models.md` — 虚拟模型注册与路由。
- `references/local-models.md` — llama.cpp 和 NVIDIA RTX 配置。
- `references/how-pi-works.md` — 运行架构与请求流程。
- `references/tui-components.md` — 自定义扩展/工具 UI 的 TUI 组件系统。
- `references/security-and-containerization.md` — 项目信任模型、无内置沙箱、Gondolin
  微型虚拟机、Docker、OpenShell。
- `references/session-format.md` — 会话 JSONL 架构、消息/条目类型、SessionManager API。
- `references/programmatic.md` — SDK、RPC 模式、JSON 事件流模式。
- `references/platform-setup.md` — Windows、Termux、tmux、终端设置、shell 别名、
  从源码构建。
- `references/development.md` — 官方包 README、源码构建和仓库检查。
- `references/changelog.md` — 本机 Pi 包中最近 12 个版本的更新记录，从 1.5.0 开始。
- `references/packages-catalog.md` + `references/pi-packages.csv` — 完整的 pi.dev 包目录
  （5,249 个包）作为可查询清单，以及 `scripts/fetch-pi-packages.py` 用于刷新。

## 安装

| 平台 | 路径 |
| ------ | ------ |
| Claude Code（全局） | `~/.claude/skills/pi-dev-rules/` |
| Claude Code（项目） | `.claude/skills/pi-dev-rules/` |
| OpenClaw（全局） | `~/.openclaw/skills/pi-dev-rules/` |
| Pi（全局） | `~/.pi/agent/skills/pi-dev-rules/` |
| Pi（项目） | `.pi/skills/pi-dev-rules/` |

```bash
cp -r pi-dev-rules ~/.claude/skills/      # 示例：Claude Code，全局
```

## 更新

运行 `bash scripts/refresh.sh`，从 PATH 中的 `pi` 定位已安装的包并离线生成参考文档；也可显式传入包根目录或 `docs/` 目录。脚本在写入前检查所有必需输入，相对文档链接会转换为对应版本的源文件 URL。审阅差异后，将 `SKILL.md` 中的 `metadata.docVersion`、`metadata.docsRefreshed`、概述以及中英文 README 的版本和日期与来源对齐。

npm 包目录单独刷新：运行 `python3 scripts/fetch-pi-packages.py`，成功后更新 `SKILL.md`、`references/packages-catalog.md` 和中英文 README 中的目录日期及数量。离线文档刷新会保留包目录文件。

## 许可证

[MIT](LICENSE)
