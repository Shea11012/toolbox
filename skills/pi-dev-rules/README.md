# pi-dev-rules

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Agents365-ai/pi-dev-rules?style=flat&logo=github)](https://github.com/Agents365-ai/pi-dev-rules/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Agents365-ai/pi-dev-rules?style=flat&logo=github)](https://github.com/Agents365-ai/pi-dev-rules/network/members)
[![Latest Release](https://img.shields.io/github/v/release/Agents365-ai/pi-dev-rules?logo=github)](https://github.com/Agents365-ai/pi-dev-rules/releases/latest)
[![Last Commit](https://img.shields.io/github/last-commit/Agents365-ai/pi-dev-rules?logo=github)](https://github.com/Agents365-ai/pi-dev-rules/commits/main)

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-2ea44f)](https://agentskills.io)

**English** · [中文](README_CN.md)

A coding-agent skill that packages **versioned [Pi](https://pi.dev) documentation**
(`@earendil-works/pi-coding-agent`) as an on-demand reference, so an agent can install, configure,
run, and **extend Pi** without re-fetching the docs.

Local skill revision **0.1.5**, refreshed **2026-11-10** from the installed official Pi **1.5.0** package. Includes all 42 Markdown documentation pages, the package README, and 12 recent releases from its changelog. The original skill repository returned HTTP 404 during this update; this is a local refresh, not an upstream release. The npm gallery remains the 2026-07-17 snapshot (5,249 packages).

Works with Claude Code, Cursor, Codex, Copilot, Windsurf, Cline / Roo Code, Gemini CLI,
Aider, Zed, OpenCode, OpenClaw / ClawHub, Hermes, pi-mono — plus major Chinese agents
(Trae, Qwen Code / Tongyi Lingma, Baidu Comate, CodeGeeX) — and any agent that reads
`AGENTS.md` or the [Agent Skills](https://agentskills.io) format.

<p align="center">
  <img src="assets/workflow-en.png" width="700" alt="pi-dev-rules workflow">
</p>

## What's inside

- `SKILL.md` — overview, when-to-use, cheat sheet, hard rules, reference index.
- `references/cli-and-usage.md` — install, auth, CLI flags, slash commands, message queue, context
  files, env vars, sessions, keybindings.
- `references/providers-and-models.md` — providers (30+), `auth.json` (+ scoped `env`), cloud
  providers, custom `models.json`, `compat`, custom-provider extensions.
- `references/settings-and-compaction.md` — `settings.json` (trust/analytics/retry/transport),
  auto/manual compaction, branch summaries.
- `references/extending-pi.md` — extensions API, skills (SKILL.md), prompt templates, themes, packages.
- `references/mcp.md` — built-in MCP servers, configuration, OAuth, resources, and SDK integration.
- `references/codemode.md` — QuickJS tool scripts, structured results, classifiers, image generation.
- `references/virtual-models.md` — virtual model routing and registration.
- `references/local-models.md` — llama.cpp and NVIDIA RTX setup.
- `references/how-pi-works.md` — runtime architecture and request flow.
- `references/tui-components.md` — TUI component system for custom extension/tool UIs.
- `references/security-and-containerization.md` — project-trust model, no built-in sandbox, Gondolin
  micro-VM, Docker, OpenShell.
- `references/session-format.md` — session JSONL schema, message/entry types, SessionManager API.
- `references/programmatic.md` — SDK, RPC mode, JSON event-stream mode.
- `references/platform-setup.md` — Windows, Termux, tmux, per-terminal setup, shell aliases,
  build-from-source.
- `references/development.md` — official package README, source build and repository checks.
- `references/changelog.md` — 12 recent releases from the installed Pi package, starting at 1.5.0.
- `references/packages-catalog.md` + `references/pi-packages.csv` — full pi.dev package gallery
  (5,249 packages) as a queryable manifest, plus `scripts/fetch-pi-packages.py` to refresh it.

## Install

| Platform | Path |
| ---------- | ------ |
| Claude Code (global) | `~/.claude/skills/pi-dev-rules/` |
| Claude Code (project) | `.claude/skills/pi-dev-rules/` |
| OpenClaw (global) | `~/.openclaw/skills/pi-dev-rules/` |
| Pi (global) | `~/.pi/agent/skills/pi-dev-rules/` |
| Pi (project) | `.pi/skills/pi-dev-rules/` |

```bash
cp -r pi-dev-rules ~/.claude/skills/      # example: Claude Code, global
```

## Updating

Run `bash scripts/refresh.sh` to rebuild references from the installed `pi` on PATH, or pass its package root (or `docs/` directory) explicitly. This runs offline and validates required inputs before writing. Review the diff and align `metadata.docVersion`, `metadata.docsRefreshed`, the overview, and both README files with the source version/date. Relative documentation links are resolved to versioned source URLs.

The gallery is independent: run `python3 scripts/fetch-pi-packages.py` to refresh it, then update its date/count in `SKILL.md`, `references/packages-catalog.md`, and both README files. The offline documentation refresh preserves gallery files.

## License

[MIT](LICENSE)
