---
name: pi-dev-rules
version: 0.1.5
description: Versioned reference for Pi (@earendil-works/pi-coding-agent). Use when installing, configuring, running, or extending Pi; answering questions about CLI commands, models/providers/auth, settings, sessions/compaction, trust, MCP, codemode, classifier/image models, virtual/local models, extensions, skills, prompts, themes, packages, TUI, SDK, RPC, or JSON streaming.
license: MIT
metadata: {"source":"installed @earendil-works/pi-coding-agent documentation","docVersion":"1.5.0","docsRefreshed":"2026-11-10","packagesRefreshed":"2026-07-17","upstreamStatus":"original skill repository returned HTTP 404 on 2026-11-10"}
---

# Pi Dev Rules

Pi is an extensible terminal coding harness. Package: `@earendil-works/pi-coding-agent` (MIT).
This local skill revision bundles all 42 Markdown documentation pages from the installed
Pi **1.5.0** package, plus its README and the 12 most recent releases in its changelog. It is a versioned
snapshot, not a claim to mirror the newest online release. The original skill repository
(`Agents365-ai/pi-dev-rules`) returned HTTP 404 during this update.

## Workflow

1. Establish the target Pi version using `pi --version` or its installed `package.json`.
2. Load only the relevant references below. For implementation, read the relevant official
   page in full and inspect the matching installed `examples/` and type declarations.
3. Prefer documentation shipped with the target version over this snapshot if versions differ.
   Locate the package through the resolved `pi` executable; its root contains `docs/`,
   `examples/`, `dist/`, `schemas/`, `README.md`, and `CHANGELOG.md`. Do not hardcode a
   package-manager installation path.
4. Verify CLI flags with `pi --help` or the subcommand's `--help`. Check extension/SDK
   symbols against installed declarations and examples before using them.
5. Validate the change with checks appropriate to the affected configuration or code.

## Reference index — load the file you need

| File | Covers |
| ------ | -------- |
| `references/cli-and-usage.md` | Getting started, usage, complete CLI and slash commands, sessions, keybindings, environment variables |
| `references/providers-and-models.md` | Providers/auth, selecting chat/classifier/image models, `models.json` schema, compatible endpoints, custom providers |
| `references/settings-and-compaction.md` | Configuration locations and context files, settings schema, compaction and branch summaries |
| `references/extending-pi.md` | Extensions API/events/tools/UI, skills, prompt templates, themes, package manifests and changelogs |
| `references/mcp.md` | Built-in MCP: `mcp.json`, CLI, OAuth, exposure, resources, extension and SDK integration |
| `references/codemode.md` | QuickJS scripts, tool discovery/calls, structured results, storage, classifiers, image generation, limits |
| `references/virtual-models.md` | Registering virtual models, routing, request and response behavior |
| `references/local-models.md` | llama.cpp setup, local models, NVIDIA RTX guidance |
| `references/tui-components.md` | Components, overlays, editors, rendering, performance and keybinding hints |
| `references/security-and-containerization.md` | Project trust, context-loading exceptions, permissions, containers/VMs and isolation limits |
| `references/session-format.md` | Session JSONL entries, message types, trees/context and SessionManager |
| `references/programmatic.md` | Choosing an integration, SDK, RPC commands/UI, JSON event stream |
| `references/platform-setup.md` | Windows, Termux, tmux, terminals and shell aliases |
| `references/development.md` | Official package README, source build and repository checks |
| `references/how-pi-works.md` | Runtime architecture and request flow |
| `references/packages-catalog.md` + `references/pi-packages.csv` | Historical npm gallery: 5,249 packages, last refreshed 2026-07-17 |
| `references/changelog.md` | 12 recent releases from the installed package, starting at 1.5.0 (2026-11-02) |

## Cheat sheet

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
# Node.js >=22.19; the pi.dev installer is another supported installation method.
cd /path/to/project && pi
# Use /login in-session to configure a provider.

pi --version
pi --help
pi update                                 # update Pi itself
pi update --extensions                    # update installed packages
pi update --models                        # refresh model catalogs
pi list                                   # list configured packages
pi config                                 # choose enabled package resources

pi -c                                     # continue most recent session for this directory
pi -r                                     # browse/resume sessions
pi --session <path-or-id>                  # open specific session
pi --fork <path-or-id>                     # fork a session
pi --no-session                           # do not persist session
pi --approve                              # trust protected project resources for this run
pi --no-approve                           # skip protected project resources for this run

pi -p "Summarize this codebase"            # run once and print final assistant text
pi @README.md "Summarize this"             # attach a file
cat file | pi -p "Summarize the input"     # pipe stdin
pi --model sonnet:high "Explain this code" # model pattern and thinking level
pi --no-mcp --tools read,grep,find,ls -p "Review" # inspect with built-in read tools
pi --mode json "Inspect this repository"  # JSONL event stream
pi --mode rpc                             # JSONL protocol over stdin/stdout
pi mcp list                               # built-in MCP; no adapter required
```

In the editor: `@file`, `!cmd`, `!!cmd`, `/command`; Ctrl+L selects a model,
Shift+Tab cycles thinking, Ctrl+X copies a message. Enter steers during a run;
Alt+Enter queues a follow-up (platform defaults can differ). Use `/hotkeys` for active
bindings and `/reload` after editing settings, keybindings, instructions, or resources.

## Implementation rules

- Use the exact package name `@earendil-works/pi-coding-agent`; normal npm installation
  uses `--ignore-scripts`. Check Node.js requirements for the target Pi version.
- Pi 1.5.0 includes MCP support and codemode. Check built-in features before recommending
  plugins; install community packages only when the task calls for them.
- Configuration lives in `<agent-dir>` (default `~/.pi/agent`, overridden by
  `PI_CODING_AGENT_DIR`) and project `.pi/`. Files have different scopes; consult the
  configuration tables before creating a project `auth.json`, `models.json`, or keybindings file.
- Context instructions include `AGENTS.override.md`, `AGENTS.md`, and `CLAUDE.md`.
  An override replaces other context files only in the same directory. Context discovery
  does not require project trust; `--no-context-files` disables it.
- Project trust controls protected resource loading, including `.pi/mcp.json` and project
  `.agents/skills`. It does not restrict tools' operating-system permissions. `sessionDir`
  is read before trust resolution. See the security reference for exact behavior.
- Extensions run in the Pi process with its permissions. Respect the user's authorized scope;
  use the documented trust/tool events when implementing permission controls.
- Custom tool errors can be signaled by throwing **or returning `isError: true`**.
  Use `outputSchema` with matching `structuredContent` for structured data. Returning a
  flagged result preserves data for scripts and renderers; throwing does not.
- In codemode, text-only tools return text; tools with an output schema return structured data.
  Structured error results and MCP `CallToolResult` values can resolve without rejection:
  inspect error/status fields as described by each tool. Calls still running when the script
  ends are cancelled, so await all work that should finish.
- Limit model-facing tool output using the exported truncation helpers (default 50KB or
  2000 lines). Preserve full output in a file when necessary.
- Use `StringEnum` from `@earendil-works/pi-ai` for portable string enums. In Pi 1.5.0,
  tool validation uses `@earendil-works/pi-schema`; TypeBox-only refinements/codecs do not
  apply to tool arguments. Follow the installed extension documentation.
- Protect credentials and never print secret values during diagnostics. Credential lookup
  normally uses runtime `--api-key`, then stored `auth.json`, then `models.json` `apiKey`,
  then environment or ambient cloud credentials. Provider extensions can define their own
  behavior. Use `/login` and provider-specific documentation for setup.
- Skill names: 1–64 lowercase letters, digits, or hyphens; no leading/trailing/repeated hyphens.
  Descriptions must explain when to load the skill and contain at most 1024 characters.

## Refresh this snapshot

Run from the skill root:

```bash
bash scripts/refresh.sh                    # discover installed Pi through pi on PATH
bash scripts/refresh.sh /path/to/pi-package # explicit package root (or its docs directory)
```

The builder validates all required source files before writing, pins source links to the
package version, and refreshes the documentation and package changelog without network access.
After reviewing the diff, align `metadata.docVersion`, `metadata.docsRefreshed`, the overview,
and both README files with the source. It preserves the independently dated gallery files.
For a gallery refresh, run `python3 scripts/fetch-pi-packages.py` separately and update its
snapshot date/count only after success. `scripts/fetch-changelog.py` remains available for
an online news/RSS snapshot; that feed has a different provenance from the installed changelog.
