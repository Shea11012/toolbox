# Pi — Changelog

> Official @earendil-works/pi-coding-agent 1.5.0 documentation.
> Refreshed from the installed package on 2026-11-10; not a live `latest` mirror.

Source: <https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/CHANGELOG.md>

Recent releases from the installed package; newer releases have not been checked.

## [1.5.0] - 2026-11-02

### New Features

- **Extension update changelogs**: see what changed in installed extension packages on the next fresh launch after an update. Package authors can choose the changelog path, and `collapseChangelog` condenses the notices. See [Show a changelog](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/packages.md#show-a-changelog).
- **Faster streaming**: large tool calls are parsed incrementally, and code-heavy answers and tool rows reuse highlighting and rendered Markdown instead of repeating the work on every update. See [Keep rendering responsive](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/tui.md#keep-rendering-responsive).
- **Custom self-update commands**: use `PI_SELF_UPDATE_COMMAND` or `selfUpdateCommand` to update pi through a wrapper or another package manager. See [Custom update command](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/cli.md#custom-update-command).
- **GPT-6.1 Terra**: available through OpenAI, Azure OpenAI Responses, and OpenAI Codex, with tool search, mid-conversation thinking-level changes, and thinking `off`. Codex offers a 500K context window. See [Models](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/cli.md#models).

### Breaking Changes

- Tool argument validation runs on `@earendil-works/pi-schema`. TypeBox features outside JSON Schema (`Type.Refine()`, `Type.BigInt()`, `Type.Undefined()`, codecs, `Format.Set()` formats) no longer apply to tool arguments; see [Tool parameter schemas and TypeBox](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/extensions.md#tool-parameter-schemas-and-typebox). Plain JSON Schema tools, including MCP tools, now get the same coercion as TypeBox tools, such as converting numeric strings and wrapping a single value into an array. Validation failures the model sees list pi-schema's messages (`- path: missing`, `- limit: expected number, got string`) instead of TypeBox's (`must have required properties path`, `must be number`).

### Added

- Extension packages can now show their changelog after an update. Pi reads `pi.changelogPath` from the package's `package.json`, or `CHANGELOG.md` in the package root, and on the next fresh launch shows entries newer than the last seen version under "Extension Updates". The `collapseChangelog` setting condenses this to one line per package ([#5958](https://github.com/earendil-works/pi/issues/5958), [#8790](https://github.com/earendil-works/pi/pull/8790))
- `pi.exec()` accepts a `maxBuffer` option that limits stdout and stderr combined, and its result has a `truncated` field that is true when output exceeded the limit ([#11360](https://github.com/earendil-works/pi/issues/11360))
- Device-code login (for example GitHub Copilot) now opens the verification page and copies the code when you press Enter. Providers can turn either action off with `openBrowserOnConfirm: false` or `copyCodeOnConfirm: false` ([#9282](https://github.com/earendil-works/pi/issues/9282), [#9301](https://github.com/earendil-works/pi/pull/9301))
- `pi update` can update Pi through a wrapper or another package manager. Set `PI_SELF_UPDATE_COMMAND` (for example `mise use -g npm:{packageName}@{version}`) or the global `selfUpdateCommand` setting; `pi update` runs it when pi.dev reports a newer release and fills `{packageName}`, `{version}`, and `{installSpec}` from that release. See [Custom update command](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/cli.md#custom-update-command) ([#7756](https://github.com/earendil-works/pi/issues/7756), [#5607](https://github.com/earendil-works/pi/issues/5607))
- Extensions can format the user's configured keybindings with `keyText()` and `keyHint()` from the tool render context and the message and entry renderer options. Importing these functions from `@earendil-works/pi-coding-agent` can resolve the extension's own copy of the package, which does not see pi's keybindings, so hints such as `keyHint("app.tools.expand", "to expand")` rendered without the key. The docs now recommend the injected functions ([#4748](https://github.com/earendil-works/pi/issues/4748))
- Added persisted session-entry `messageId` and ISO `timestamp` to `MarkdownTransformContext`. They are available when rendering saved entries and undefined for live rendering ([#7952](https://github.com/earendil-works/pi/pull/7952) by [@vipentti](https://github.com/vipentti))
- Added a `blocked` option to inline `ctx.ui.custom()` components so approval prompts and other custom dialogs can report that pi is waiting for user input. Overlays ignore the option. See [Custom screens and overlays](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/tui.md#use-custom-screens-and-overlays) ([#11428](https://github.com/earendil-works/pi/issues/11428))
- Added `Usage.cost.totalFromProvider` to distinguish billed totals from catalog estimates in SDK and extension usage data; combined usage is marked provider-reported only when every part is ([#11178](https://github.com/earendil-works/pi/pull/11178))
- Added concrete `responseModel` metadata to messages from pi-messages providers such as Radius, including when a virtual model is requested. See [AssistantMessage](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/message-types.md#assistantmessage) ([#11265](https://github.com/earendil-works/pi/pull/11265))
- Added GPT-6.1 Terra for OpenAI, Azure OpenAI Responses, and OpenAI Codex, with tool search and mid-conversation thinking-level changes. It supports thinking `off`; Codex offers a 500K context window

### Changed

- Extensions keep importing `Type`, `Static` and `TSchema` from `@earendil-works/pi-ai`: Pi maps that import to pi-ai's compat entry plus the TypeBox it bundles, now that pi-ai itself no longer re-exports TypeBox, and its `StringEnum` there stays a TypeBox `TUnsafe<T>`. The built-in tool factories (`createReadTool()` and the others) return `TypeBoxAgentTool<typeof schema>`, which keeps `params` typed for TypeBox.
- Tightened system prompt
- `pi update` for installs from the pi.dev installer no longer passes `--min-release-age=0` to `npm ci`. The release lockfile pins every package, so the flag had no effect, and security scanners that block it stopped the update ([#11262](https://github.com/earendil-works/pi/issues/11262))
- `/model` and `/scoped-models` now show a model's name next to its ID when the name adds words the ID lacks, such as a renamed `models.json` override ([#5916](https://github.com/earendil-works/pi/issues/5916), [#11347](https://github.com/earendil-works/pi/pull/11347))
- MCP OAuth sign-in now uses pi's Client ID Metadata Document by default when the authorization server supports it for public clients, and registers a client dynamically otherwise, like Codex, Claude Code, and opencode. Clients registered before stay in use while their redirect URI matches. The new default `oauth.clientRegistration: "auto"` registers when `clientName` or a non-default `callbackUrl` is set; `"dcr"` always registers. `pi mcp add --oauth-client-registration` sets the mode ([#11426](https://github.com/earendil-works/pi/issues/11426))
- Changed the default OpenAI model from `gpt-5.5` to `gpt-6.1-sol`, including after ChatGPT sign-in when no model is selected ([#11442](https://github.com/earendil-works/pi/issues/11442))
- Updated the built-in model catalog to models.dev v2. Realtime and image-only models are no longer offered as chat models; newer OpenAI and Google chat models are included

### Fixed

- Updated glob matching to prevent denial of service from amplified glob patterns.
- Fixed a saved "Do not trust" decision being ignored for projects without trust-requiring resources, for example a folder with only `AGENTS.md`. pi auto-trusted such projects, so `ctx.isProjectTrusted()` returned true and package commands treated them as trusted. A saved decision in `trust.json` now takes precedence; auto-trust applies only when no decision is saved ([#10947](https://github.com/earendil-works/pi/issues/10947))
- Fixed `Shift+Enter` queueing a follow-up instead of inserting a newline in Apple Terminal setups that send `ESC` + Return. pi now checks the local Shift key state for that sequence, as it already did for plain Return; `Alt+Enter` without Shift still queues a follow-up ([#11559](https://github.com/earendil-works/pi/issues/11559))
- Fixed the working status (OSC 7501) disappearing in Rex and iTerm2 during runs in regular TUI mode. Rendered messages wrote OSC 133 prompt markers to the terminal, which the terminal treats as a new shell prompt; regular mode no longer writes them ([#11519](https://github.com/earendil-works/pi/issues/11519))
- Fixed compaction, branch summaries, and bug-report summaries in SDK sessions passing the stored OAuth token back to the model runtime as an explicit API key. Provider auth that treats explicit keys differently from stored OAuth now sees the OAuth login, as normal prompts do ([#11520](https://github.com/earendil-works/pi/issues/11520))
- Fixed a redundant system prompt update (tools, rules) when an extension set the same active tools in a different order, for example a reversed `pi.setActiveTools()` list. Tools that stay active now keep their order and newly activated tools are appended ([#11495](https://github.com/earendil-works/pi/issues/11495))
- Fixed `pi.exec()` crashing pi with `RangeError: Invalid string length` when a command printed more output than fits in a string. The default output cap is the smaller of 256 MiB and the runtime string limit; past the cap, the command is terminated and the result has `truncated: true` and a nonzero exit code ([#11360](https://github.com/earendil-works/pi/issues/11360))
- Fixed `pi.exec()` never returning when a command ignored SIGTERM after a timeout or abort. pi now sends SIGKILL 5 seconds later, as intended
- Fixed `pi install` and `pi remove` adding ever deeper nested entries to the npm `package-lock.json` when the agent directory is reached through a symlink, such as `~/.pi` linked into a dotfiles repo. pi now passes the resolved real path to npm ([#11358](https://github.com/earendil-works/pi/issues/11358))
- MCP sign-in now rejects authorization endpoints and other OAuth metadata URLs that are not `http:` or `https:`. Before, a malicious MCP server could supply a `file:` or custom protocol URL, which pi passed to the platform URL handler.
- Automatic `fd` and `rg` downloads no longer fetch x86-64 binaries on ARM32 and other architectures without a prebuilt release. pi now warns and recommends installing the tool with the system package manager ([#11209](https://github.com/earendil-works/pi/issues/11209))
- Fixed `/model` search ranking letters scattered over an earlier part of an entry above a real match, for example `opus` listing `gpt-oss-120b` and `claude-sonnet-4.5` before `claude-opus-4.1` ([#11220](https://github.com/earendil-works/pi/issues/11220), [#11296](https://github.com/earendil-works/pi/pull/11296))
- Fixed `/resume` search matching scattered letters anywhere in session messages and IDs, for example `1024` matching inside a session UUID. Session names and working directories still match fuzzily; IDs and message text now match only as exact substrings ([#11220](https://github.com/earendil-works/pi/issues/11220), [#11024](https://github.com/earendil-works/pi/issues/11024), [#11296](https://github.com/earendil-works/pi/pull/11296))
- Fixed HTML export showing a blank page for sessions with thousands of entries ([#11225](https://github.com/earendil-works/pi/issues/11225), [#11293](https://github.com/earendil-works/pi/pull/11293))
- Fixed HTML export not showing system messages: the system prompt and tools, and later section updates such as after `/reload`. `pi --export` now includes the system prompt and tools too ([#11261](https://github.com/earendil-works/pi/issues/11261), [#3464](https://github.com/earendil-works/pi/issues/3464), [#11290](https://github.com/earendil-works/pi/pull/11290))
- Fixed aborting a bash command on macOS sometimes running the next command of a list such as `long_step; next_step`. pi now stops the process group before killing it ([#11252](https://github.com/earendil-works/pi/issues/11252), [#11289](https://github.com/earendil-works/pi/pull/11289))
- Fixed large streamed tool calls taking excessive CPU time and memory because every delta re-parsed the accumulated arguments. Providers and agent proxy streams now parse each delta once, grammar tools no longer copy their entire input per delta, and interactive tool renderers run at most once per frame ([#9265](https://github.com/earendil-works/pi/issues/9265))
- Fixed the login dialog opening sign-in URLs that are not web URLs, and printing control characters from sign-in, device-code, and info URLs, which could end a terminal hyperlink and send escape sequences to the terminal
- Fixed `tui.select.pageUp` and `tui.select.pageDown` being ignored in slash command and file autocomplete, `/settings`, and the model, scoped models, login, fork, `/mcp`, and llama.cpp selectors. In fullscreen mode, PageUp/PageDown now move an open list or autocomplete menu instead of scrolling the transcript, and a page key bound to Ctrl+V pages autocomplete instead of pasting an image ([#7629](https://github.com/earendil-works/pi/issues/7629), based on [#7680](https://github.com/earendil-works/pi/pull/7680) by [@muyiyr](https://github.com/muyiyr))
- Fixed tool output and `!` command output showing the parameters of control sequences with a `<`, `=` or `>` prefix as text, for example `35;59;1M` from a mouse report `ESC[<35;59;1M` or `0;276;0c` from a terminal reply `ESC[>0;276;0c`. Text after the keypad-mode sequences `ESC=` and `ESC>` is still kept ([#11377](https://github.com/earendil-works/pi/issues/11377))
- Fixed `pi -e npm:<pkg>` staying on the version from the first download. On each start and `/reload`, pi now reinstalls an `-e` npm package without an exact version when the registry has a newer matching version. `pi -e git:<repo>@<branch>` likewise stayed on its first checkout and is now fetched and reset to the branch; a commit-hash ref that is already checked out is not fetched. Offline mode and failed checks keep the cached copy ([#11375](https://github.com/earendil-works/pi/issues/11375), [#11590](https://github.com/earendil-works/pi/pull/11590))
- Fixed Windows paths being compared case-sensitively. When the working directory and home directory differed only in drive-letter casing (`c:\Users\me` vs `C:\Users\me`), skills in `~/.agents/skills` loaded twice, as project and user skills, and were reported as name collisions. The same mismatch also re-asked for saved project trust, hid sessions in a custom session directory from `--continue` and `/resume`, and stopped `pi remove` from matching configured local packages ([#10488](https://github.com/earendil-works/pi/issues/10488))
- Fixed paths next to the home directory being shown with a broken `~` prefix, for example `/home/me2/project` shown as `~2/project` when home is `/home/me`
- Fixed `pi mcp login -l` and `pi mcp logout -l` failing with `Unknown option --local.` although `pi mcp add` and `pi mcp remove` accept `-l`. With `-l`, they now require the server to be a project server. Unknown options are now reported as typed, and a mistyped server name gets a suggestion, for example `Did you mean "gurker"?`
- Fixed `pi update` naming pnpm for installs that only live under `PNPM_HOME`, for example a wrapper under `$PNPM_HOME/global-nub/`. pi said "not managed by a global pnpm install"; it now names the package manager only when that manager owns the install ([#7756](https://github.com/earendil-works/pi/issues/7756))
- Fixed image paste, copy, and opening the browser for sign-in failing silently on WSL when the working directory is deep. Windows programs such as `powershell.exe` and `explorer.exe` cannot start from a directory whose `\\wsl.localhost\...` path exceeds 260 characters; pi now starts these helpers from `/` ([#11592](https://github.com/earendil-works/pi/issues/11592))
- Fixed the external editor failing silently, for example when the editor command is wrong or a Windows editor cannot start from a deep WSL directory. pi now shows a status message such as `External editor exited with code 1; prompt unchanged` ([#11592](https://github.com/earendil-works/pi/issues/11592))
- Fixed `tool_search` and codemode `searchTools()` ranking a tool below tools that only mention its name in their descriptions, for example `peekaboo app` ranking `mcp__peekaboo__app` 14th. A tool matching more of the query's words now ranks above one matching fewer, a query word in a tool's name scores more than any number of mentions in its description, a tool whose whole name is in the query gets a large bonus, and long server instructions no longer lower the scores of that server's tools ([#11331](https://github.com/earendil-works/pi/issues/11331))
- Fixed `tool_search` and codemode `searchTools()` finding nothing for Chinese, Japanese, Thai, and other non-ASCII queries, because the tokenizer kept only ASCII letters and digits. Words in any script now match, text without spaces between words such as `搜索记录` is split into words, and canonically equivalent text such as `café` and `cafe\u0301` matches ([#10816](https://github.com/earendil-works/pi/issues/10816), [#11037](https://github.com/earendil-works/pi/pull/11037) by [@haoqixu](https://github.com/haoqixu))
- Fixed `pi update` stopping with `git clean -fdx failed with code 1` on Windows when another pi session had a git extension's native module or executable open. Windows cannot delete such files, so the update left the new code with the old dependencies. pi now warns, installs the dependencies anyway, and retries the clean on the next update ([#11597](https://github.com/earendil-works/pi/issues/11597))
- Fixed tool rows and streamed answers highlighting the same code again on every redraw. A running codemode row highlighted its whole script on every progress update and timer tick, a complete `write` row its whole file on every update and expand toggle, a streamed `write` its first 50 lines on every delta, and a streamed answer every earlier code block on every delta. Rows now reuse their last highlighting until the code, theme, or loaded grammars change, and assistant messages keep their rendered Markdown blocks while streaming ([#10971](https://github.com/earendil-works/pi/issues/10971))
- Fixed resized photos being sent as multi-megabyte PNGs even when JPEG was much smaller, causing large requests to fail or time out. Image resizing now tries the smaller encoding first ([#11551](https://github.com/earendil-works/pi/issues/11551))
- Fixed `pi update --extensions` reporting success without warning when npm's stale registry metadata left a package at its old version. pi now reports the installed and expected versions ([#11536](https://github.com/earendil-works/pi/issues/11536))
- Fixed skill validation warnings being labeled `[Skill conflicts]` even when there was no name collision. They are now shown under `[Skill warnings]` ([#11521](https://github.com/earendil-works/pi/issues/11521))
- Fixed codemode tool descriptions including entire union and multi-line output types in every request. Object unions now summarize their fields and discriminators; other multi-line types point to `describeTool()` for the full declaration ([#11501](https://github.com/earendil-works/pi/issues/11501))
- Fixed the model-scope startup notice being left in the shell after exiting fullscreen mode. It now appears inside pi's fullscreen header ([#11508](https://github.com/earendil-works/pi/issues/11508))
- Fixed startup from a deleted working directory crashing with an uncaught `uv_cwd` stack trace. pi now asks the user to change to an existing directory ([#11509](https://github.com/earendil-works/pi/issues/11509))
- Fixed failed session writes leaving entries in memory that were absent from disk, so later entries pointed to missing parents and resumed sessions lost earlier history and tools ([#11460](https://github.com/earendil-works/pi/issues/11460))
- Fixed `/tree` branch summaries ignoring the session's thinking level, which could make reasoning models reject summary requests with an unsupported `none` effort ([#11444](https://github.com/earendil-works/pi/issues/11444))
- Fixed hidden thinking with an empty hidden-thinking label still adding blank rows before answers and tool calls ([#11402](https://github.com/earendil-works/pi/issues/11402))
- Fixed package installation and removal printing npm audit and funding advice, including `npm audit fix` instructions that could install a second copy of pi into the package directory ([#11409](https://github.com/earendil-works/pi/issues/11409))
- Fixed replacing an extension editor while a dialog was open hiding the dialog and leaving it unanswerable. The new editor now appears after the dialog closes ([#11431](https://github.com/earendil-works/pi/issues/11431))
- Fixed `grep` context lines being offset from ripgrep's match line numbers when a file contains a lone carriage return ([#11398](https://github.com/earendil-works/pi/issues/11398))
- Fixed `--model <provider>/<id>` failing for provider IDs containing slashes, such as URL-derived llama.cpp provider IDs ([#11394](https://github.com/earendil-works/pi/issues/11394))
- Fixed slow session forking on filesystems where opening files is expensive by writing the fork through one file handle ([#11253](https://github.com/earendil-works/pi/issues/11253))
- Fixed `pi.exec()` corrupting UTF-8 characters split across stdout or stderr chunks ([#11312](https://github.com/earendil-works/pi/issues/11312))
- Fixed `pi.exec()` returning empty stderr when a command could not be spawned, such as a missing executable. It now preserves the spawn error message ([#11257](https://github.com/earendil-works/pi/pull/11257) by [@muyiyr](https://github.com/muyiyr))
- Fixed a configured package failing to install crashing startup. pi now skips the package, reports an extension warning, and retries on the next start or `/reload`; explicit install and update commands still fail with a nonzero exit ([#11304](https://github.com/earendil-works/pi/pull/11304) by [@Lincoln504](https://github.com/Lincoln504))
- Fixed the todo extension example crashing the TUI when a tool call failed argument validation ([#8057](https://github.com/earendil-works/pi/pull/8057) by [@cyzlmh](https://github.com/cyzlmh))
- Updated `undici` to 8.12.3 and the Gondolin extension example to 0.14.0 for security advisories
- Fixed OpenRouter cost totals using catalog estimates instead of reported billing for Chat Completions and Anthropic Messages. BYOK totals include both OpenRouter charges and reported upstream costs; component costs remain catalog estimates ([#9980](https://github.com/earendil-works/pi/issues/9980))
- Fixed OpenCode Zen and OpenCode Go requests using shared endpoints instead of their protocol-specific OpenAI, Anthropic, Google, and System One endpoints ([#11434](https://github.com/earendil-works/pi/pull/11434) by [@vimtor](https://github.com/vimtor))
- Fixed Zhipu/Z.ai usage-limit errors (code `1308`) being treated as transient HTTP 429 errors, causing automatic retries that cannot succeed until the usage cap resets ([#11537](https://github.com/earendil-works/pi/issues/11537))
- Fixed LiteLLM's `ContextWindowExceededError` not being recognized as context overflow ([#11492](https://github.com/earendil-works/pi/issues/11492))
- Fixed Gemini tool schemas sending unsupported `const` keywords. They are now converted to single-value `enum` schemas without rewriting literal data in defaults, examples, or enum values, or losing properties named `__proto__` ([#11308](https://github.com/earendil-works/pi/issues/11308))
- Fixed the faux provider counting simulated cache-write tokens as both input and cache writes
- Fixed Orca terminals falling back to text for inline images. Orca is now recognized as supporting true color and hyperlinks, and Kitty images when it advertises `ORCA_IMAGE_PROTOCOL=kitty` ([#9329](https://github.com/earendil-works/pi/pull/9329) by [@XRX193](https://github.com/XRX193))
- Fixed bare Markdown URLs swallowing following CJK punctuation and text; explicit Markdown links and angle autolinks are unchanged ([#10934](https://github.com/earendil-works/pi/pull/10934) by [@haoqixu](https://github.com/haoqixu))
- Fixed Kitty-protocol F1–F12 shortcuts, including modified function keys, not being recognized, and F13+ and other functional keys inserting invisible private-use characters into the editor ([#11419](https://github.com/earendil-works/pi/issues/11419), [#11345](https://github.com/earendil-works/pi/issues/11345))
- Fixed Kitty images inside padded or colored boxes disappearing when their first row scrolled above the fullscreen viewport. Partially visible images are now cropped correctly, including beside other text
- Fixed deeply nested Markdown blockquotes producing exponentially many lines, hanging or crashing rendering once their borders exhausted the available width ([#11272](https://github.com/earendil-works/pi/issues/11272))
- Fixed Claude sessions failing with `role 'system' must precede an 'assistant' message` when a system update was followed by an empty or reasoning-only assistant reply ([#11091](https://github.com/earendil-works/pi/issues/11091))
- Fixed Claude mid-conversation thinking-level changes failing with `Invalid effort level` on accounts whose organization caps effort below `high` ([#10063](https://github.com/earendil-works/pi/issues/10063))
- Fixed Kimi K3.1 Pro models using Kimi K2 request settings on Kimi Coding, Moonshot, and OpenCode Go. They now send the correct reasoning effort, preserve earlier thinking, accept tools added mid-conversation, and use K3-family pricing
- Fixed OpenCode DeepSeek V4.1 Flash requests failing when long cache retention sent the unsupported `prompt_cache_retention` parameter
- Fixed GPT-5.4 and GPT-5.5 failing with `Missing namespace for function_call` after switching from a model that had called tools ([#11415](https://github.com/earendil-works/pi/issues/11415))
- Fixed Bedrock Claude requests failing when preferred strict tools exceed the provider's strict-tool limits. Requests now retry once with preferred tools non-strict while keeping required strict tools strict ([#11416](https://github.com/earendil-works/pi/issues/11416))
- Fixed OpenRouter's `~anthropic/claude-*-latest` aliases losing earlier thinking after tool calls by using the Anthropic Messages API ([#9534](https://github.com/earendil-works/pi/issues/9534))
- Fixed terminal titles containing control characters being able to inject terminal escape sequences, and pi-messages streams accepting invalid content-block indices
- Fixed fullscreen double-click selection splitting paths and tokens at `~`, `.`, `\`, and `+`; word characters now match iTerm2's defaults ([#10980](https://github.com/earendil-works/pi/issues/10980))
- Fixed display math wider than the content area being split apart by line wrapping; it now falls back to raw LaTeX ([#11483](https://github.com/earendil-works/pi/issues/11483))
- Fixed styled words ending exactly at the wrap width adding a leading space on the next line, and strikethrough leaking into wrapped-line padding ([#10925](https://github.com/earendil-works/pi/issues/10925))
- Fixed `/tree` branch summaries including failed assistant replies and original content that context edits had hidden or replaced. Summaries now honor the same context edits as live requests and compaction ([#11602](https://github.com/earendil-works/pi/issues/11602))

### Removed

- Removed the native OS `sandbox/` extension example and its dependency. Use the [Gondolin example](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/examples/extensions/gondolin/) or the [containerization guide](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/containerization.md).

## [1.4.0] - 2026-10-21

### New Features

- **Image input for classifiers**: codemode `models.classify()` accepts `images` for TypeSafe's Jev and Cloudflare's Clef models on `typesafe`, `cloudflare-workers-ai`, and OpenRouter. See [Use classifier models](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md#use-classifier-models) and [Codemode](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/codemode.md#models).
- **Models Configuration reference**: every provider, model, model override, and compatibility field of `models.json`, generated from its schema. See [Models Configuration](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models-configuration.md).
- **Summaries without a fixed output cap**: compaction and branch summaries use the model's output limit, so long reasoning no longer makes them fail. See [Compaction](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/compaction.md#compaction).
- **Codemode waits for a free worker**: parallel scripts and in-process subagents queue instead of failing, and `PI_CODEMODE_MAX_WORKERS` raises the limit. See [Codemode limits](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/codemode.md#limits).
- **Rex terminal support**: OSC 8 hyperlinks, truecolor, and inline images.

### Added

- Added a Models Configuration reference generated from the `models.json` schema, listing all provider, model, model override, and compatibility fields ([#10790](https://github.com/earendil-works/pi/issues/10790))
- Codemode `models.classify()` now accepts `images` for TypeSafe's Jev and Cloudflare's Clef models on `typesafe`, `cloudflare-workers-ai`, and OpenRouter, and lists Clef Omni and Jev 1.14 on Workers AI.
- Provider-level `compat` in `models.json` now also applies to classifier models, with the System One fields `imageInput` and `sendImageOptInHeader` for proxies that serve another service's classifiers. Extension classifier models accept `compat` too.
- Added `MiniMax-M3.1-Flash` to the `minimax` and `minimax-cn` providers, with thinking levels low through max ([#11121](https://github.com/earendil-works/pi/issues/11121))
- Added support for the Rex terminal: OSC 8 hyperlinks, truecolor, and inline images ([#11131](https://github.com/earendil-works/pi/issues/11131), [#11150](https://github.com/earendil-works/pi/pull/11150) by [@petrroll](https://github.com/petrroll), [#11183](https://github.com/earendil-works/pi/pull/11183) by [@nihaals](https://github.com/nihaals))

### Changed

- Provider attribution headers now come from pi-ai's client identity. Extensions' `before_provider_headers` handlers no longer see the OpenRouter, NVIDIA NIM, and OpenCode attribution headers; returning `null` for one still removes it. Cloudflare requests send pi's detailed `User-Agent` instead of `pi-coding-agent`, as do GitHub release checks for tool downloads, and OpenCode requests send `x-opencode-client` whenever attribution is enabled, not only with a session.
- `generateSummary()` and `generateSummaryWithUsage()` now ignore their `reserveTokens` parameter. Summary requests use the model's output limit instead.
- Changed the default GitHub Copilot model from `gpt-5.4`, which Copilot retired, to `gpt-6.1-sol`.
- Changed the default NVIDIA model to `nvidia/nemotron-3.5-super-vl-120b-a12b` ([#10910](https://github.com/earendil-works/pi/pull/10910) by [@cv](https://github.com/cv))
- Changed the default Xiaomi model to `mimo-v2.6-pro` for the `xiaomi` and Xiaomi Token Plan providers, since `mimo-v2.5-pro` left the catalog.
- Grok 4.3 and Grok 4.5 on the `xai` provider now offer the `xhigh` thinking level.
- Sign in with ChatGPT: ChatGPT Business workspace usage-limit errors are not retried and tell the user to ask their workspace admin to increase the limit.

### Fixed

- Fixed compaction and branch summaries failing with "generation hit the token cap" when reasoning used most of the fixed summary output limit. Summaries now use the model's output limit, and `compaction.reserveTokens` only controls when compaction starts ([#9512](https://github.com/earendil-works/pi/issues/9512), [#9075](https://github.com/earendil-works/pi/issues/9075)).
- Fixed `models.schema.json` missing descriptions for provider and model fields, so editors showed no hints for them ([#10790](https://github.com/earendil-works/pi/issues/10790))
- Fixed `pi update` failing with "Managed install marker is missing or invalid" when `managed-install.json` starts with a UTF-8 BOM, which Windows PowerShell 5.1 adds when it rewrites the file.
- Fixed HTML export showing literal asterisks for Markdown bold and italic next to CJK punctuation ([#3353](https://github.com/earendil-works/pi/issues/3353), [#10154](https://github.com/earendil-works/pi/issues/10154))
- Fixed the terminal staying in mouse-tracking, focus-reporting, Kitty keyboard, and alternate-screen modes when pi exits without its normal terminal teardown, which flooded the shell prompt with escape sequences ([#11170](https://github.com/earendil-works/pi/issues/11170))
- Fixed concurrent extension `select`/`confirm`/`input`/`editor` dialogs and inline `custom()` components in interactive mode: a second dialog replaced the first and the first promise never settled; closing the visible dialog now shows the previous one again ([#11166](https://github.com/earendil-works/pi/issues/11166), [#9909](https://github.com/earendil-works/pi/issues/9909))
- Fixed pasting in the shell hanging after copying text in pi and suspending it with Ctrl+Z on Linux: the background `wl-copy`/`xclip`/`xsel` process that keeps serving the clipboard was suspended along with pi ([#11179](https://github.com/earendil-works/pi/issues/11179))
- Fixed codemode scripts failing immediately when both codemode workers are busy, for example with parallel codemode calls or in-process subagents. Scripts now wait up to 60 seconds for a free worker, and `PI_CODEMODE_MAX_WORKERS` raises the limit of two workers ([#11184](https://github.com/earendil-works/pi/issues/11184))
- Fixed extensions failing to load when importing `@earendil-works/pi-ai/models` (e.g. for `clampThinkingLevel`) by exposing the subpath through the extension loader aliases and virtual modules ([#11156](https://github.com/earendil-works/pi/issues/11156))
- Fixed `mcp.json` files that start with a UTF-8 BOM failing to parse, which skipped all their MCP servers and made `pi mcp add`/`pi mcp remove` fail ([#11191](https://github.com/earendil-works/pi/issues/11191))
- Fixed `/compact <instructions>` ignoring the instructions when summarizing the start of a turn that compaction splits. When the split turn was the only new content since the last compaction, the instructions were ignored entirely ([#11058](https://github.com/earendil-works/pi/issues/11058))
- Fixed resumed sessions and `/tree` navigation leaving extension tools inactive when the branch recorded its tools before they were registered, such as tools from extensions installed after the session started. Extension tools the branch never added or removed are now active unless they are registered with `defaultActive: false` ([#11062](https://github.com/earendil-works/pi/issues/11062), [#11075](https://github.com/earendil-works/pi/issues/11075))
- Fixed sessions breaking after recovery from a response cut off at the output limit: the truncated tool call was omitted but its tool results were kept, so providers rejected every later request ([#11227](https://github.com/earendil-works/pi/issues/11227), [#11233](https://github.com/earendil-works/pi/pull/11233) by [@petrroll](https://github.com/petrroll))
- Fixed the `grep` tool following `RIPGREP_CONFIG_PATH`, where options such as `--fixed-strings` silently changed regex searches into literal ones. The tool now runs `rg --no-config` ([#11203](https://github.com/earendil-works/pi/issues/11203), [#11230](https://github.com/earendil-works/pi/pull/11230) by [@petrroll](https://github.com/petrroll))
- Fixed Windows shell detection rejecting runnable Microsoft Store shell aliases ([#9504](https://github.com/earendil-works/pi/pull/9504) by [@petrroll](https://github.com/petrroll))
- Fixed Windows shell detection missing PowerShell outside `PATH` and the legacy WSL `bash.exe` launcher when Windows is not installed in `C:\Windows`. pi now checks `%ProgramFiles%\PowerShell\7`, `%SystemRoot%\System32\WindowsPowerShell\v1.0`, and `%SystemRoot%` ([#9501](https://github.com/earendil-works/pi/pull/9501) by [@petrroll](https://github.com/petrroll))
- Fixed GitHub Copilot sessions with large request bodies, such as many images, failing with HTTP 413 `failed to parse request` instead of compacting and retrying ([#11016](https://github.com/earendil-works/pi/pull/11016) by [@petrroll](https://github.com/petrroll))
- Fixed the `openai-codex` provider offering `gpt-5.5` and `gpt-5.3-codex-spark`, which always fail for ChatGPT accounts ([#11173](https://github.com/earendil-works/pi/pull/11173) by [@lucasmeijer](https://github.com/lucasmeijer))
- Fixed whitespace-only tool output (for example a bare `\r\n` from bash) making OpenAI Completions, OpenAI Responses, and Google requests fail with a 400 ([#8720](https://github.com/earendil-works/pi/issues/8720))
- Fixed automatic retry not triggering for more gateway upstream failures, `stream disconnected before completion` errors relayed by Codex CLI proxies, and transient Google Vertex OAuth token refresh failures, and retrying errors because of digits inside request ids or byte counts ([#10920](https://github.com/earendil-works/pi/issues/10920), [#11057](https://github.com/earendil-works/pi/issues/11057), [#10996](https://github.com/earendil-works/pi/issues/10996))
- Fixed OpenAI Responses models losing the prompt cache on every deferred tool load after a tool was removed ([#10940](https://github.com/earendil-works/pi/issues/10940))
- Fixed Cloudflare Workers AI classifier pricing: Clef Flash costs $0.038 and Jev $0.042 per million input tokens instead of Jev being listed as free.
- Fixed an unclosed `$$` display-math block swallowing or corrupting every Markdown table after it ([#11159](https://github.com/earendil-works/pi/issues/11159))
- Fixed Markdown bold and italic not rendering next to CJK punctuation ([#10730](https://github.com/earendil-works/pi/pull/10730) by [@theBucky](https://github.com/theBucky))
- Fixed `@` file autocomplete returning no results for queries containing regex metacharacters such as `[` or `(` ([#10972](https://github.com/earendil-works/pi/issues/10972))

## [1.3.0] - 2026-10-15

### New Features

- **Choose where `/share` uploads**: `sessionShareDestination` selects `auto`, `gist`, or `radius`. See [Sessions and context](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/settings.md#sessions-and-context) and [Export or share a session](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/sessions.md#export-or-share-a-session).
- **Cache-preserving thinking level changes on OpenAI GPT-6**: changing the thinking level mid-session with an API key keeps the prompt cache.
- **Kimi Code over Chat Completions**: tools added mid-conversation no longer invalidate the prompt cache. `models.json` base URL overrides must now include `/v1`. See [Providers](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/providers.md).
- **Clean model switching**: thinking from a previous model is dropped instead of being shown to the new model as text.
- **Resumed sessions keep their active tools**: `--tools +name`/`-name` applies on top of them. See [Tools](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/settings.md#tools).

### Added

- Changing the thinking level mid-session on OpenAI GPT-6 models (API key) now keeps the prompt cache ([#10853](https://github.com/earendil-works/pi/issues/10853))
- Added the `sessionShareDestination` setting to choose automatic, GitHub gist, or Radius uploads for `/share` ([#10870](https://github.com/earendil-works/pi/issues/10870) by [@vegarsti](https://github.com/vegarsti))

### Changed

- Changed the `kimi-coding` provider to use OpenAI Chat Completions at `https://api.kimi.com/coding/v1`, the protocol used by the official Kimi Code client. K3, K3-256K, and Kimi For Coding now accept tools added mid-conversation without invalidating the prompt cache. `models.json` overrides of the `kimi-coding` base URL must now include `/v1` ([#10720](https://github.com/earendil-works/pi/issues/10720))
- Changed model switching to drop thinking blocks from earlier assistant messages produced by a different model, instead of sending them as plain text. The new model previously saw the old model's reasoning as part of its replies and could start writing its own reasoning into the visible answer ([#10995](https://github.com/earendil-works/pi/issues/10995))

### Fixed

- Pinned internal Pi dependencies to exact release versions to prevent fresh installs from mixing incompatible packages ([#10865](https://github.com/earendil-works/pi/issues/10865))
- Fixed resumed sessions dropping tools activated during the session. Resume now restores the session's active tools, with `--tools +name`/`-name` entries applied to them, unless `--tools` with tool names, `--no-tools`, or `--no-builtin-tools` selects tools explicitly ([#10785](https://github.com/earendil-works/pi/issues/10785))
- Fixed stopping a codemode script or reaching its deadline waiting for a non-interruptible built-in to return on Bun ([#10748](https://github.com/earendil-works/pi/issues/10748))
- Fixed repeated codemode timeouts or aborts accumulating surviving workers; admission now limits live workers to two across sessions, counting cancelled workers until actual exit ([#10748](https://github.com/earendil-works/pi/issues/10748))
- Fixed `--model` choosing a provider by catalog order when several providers offer the match; Pi now prefers the provider with credentials and otherwise reports the ambiguity. `--models` and `enabledModels` add a model for each provider that offers it and warn about the ambiguity ([#10160](https://github.com/earendil-works/pi/issues/10160))
- Fixed `read` line-range labels for numeric-string or null arguments in the TUI, session tree, HTML exports, and examples ([#9887](https://github.com/earendil-works/pi/issues/9887))
- Fixed the Nix flake build failing when a provider switched APIs: the model catalog pin is now refreshed from the newest published catalog when its model API groups differ, and releases pin the newest catalog and build with it before tagging ([#10985](https://github.com/earendil-works/pi/issues/10985))
- Fixed the Nix package putting its Node.js first on `PATH`, which made bash tool shells use Pi's Node instead of the user's `node`/`npm`. Pi's Node is now only a fallback ([#10519](https://github.com/earendil-works/pi/issues/10519))
- Fixed prompt templates dropping empty quoted arguments (`""` or `''`), which shifted later positional arguments and prevented positional defaults from applying ([#10867](https://github.com/earendil-works/pi/issues/10867))
- Fixed the Nix package build failing in its install check because it still expected chord and esbuild, which Pi no longer depends on
- Fixed tool-call argument parsing dropping fields when a string contains an invalid `\u` escape such as `\usepackage` ([#10868](https://github.com/earendil-works/pi/issues/10868))
- Fixed Anthropic and Bedrock Claude requests failing with a 400 when an error tool result contains images; the images are now sent after the tool results of the turn, so the model still sees them ([#10794](https://github.com/earendil-works/pi/issues/10794))
- Fixed OpenCode Go Gemini models failing with a 404 by moving OpenCode Zen and OpenCode Go to the `opencode.ai/inference` endpoints, and added Google Generative AI support to the OpenCode Go provider
- Fixed OpenCode Go MiniMax M2.7 failing with "Model does not support this protocol" by using the Anthropic Messages API
- Fixed automatic retry not triggering for gateway `Unable to forward upstream stream` errors ([#10920](https://github.com/earendil-works/pi/issues/10920))
- Fixed automatic retry not triggering for `The service is temporarily unavailable` errors, which also made compaction fail on the first attempt ([#10965](https://github.com/earendil-works/pi/issues/10965))
- Fixed OpenAI-compatible responses showing thinking after the answer when a proxy such as LiteLLM sends reasoning and content in the same stream chunk ([#10926](https://github.com/earendil-works/pi/issues/10926))
- Fixed Gemini 4 Argon requests on Google Vertex failing with "Thinking budget is not supported", and its thinking level being ignored on the Gemini API ([#10890](https://github.com/earendil-works/pi/issues/10890))
- Fixed Xiaomi MiMo models failing with a 400 at the `minimal` thinking level; they now expose only the `off` and `high` levels ([#10818](https://github.com/earendil-works/pi/issues/10818))
- Fixed `openai-codex/gpt-6.1-sol` using a 272K context window instead of the 500K window Codex now provides ([#10840](https://github.com/earendil-works/pi/issues/10840))
- Fixed tool calls whose final arguments are malformed JSON silently running with only the fields parsed before the error; they now fail validation and show the model the raw arguments it sent ([#10897](https://github.com/earendil-works/pi/issues/10897))
- Fixed Claude Haiku 5.5 and Claude Opus 5 not supporting the `off` thinking level ([#10753](https://github.com/earendil-works/pi/issues/10753))
- Fixed `done()` of an extension's `ctx.ui.custom({ overlay: true })` closing the topmost overlay instead of its own, which left the finished overlay on screen and another extension's dialog unresolved ([#10648](https://github.com/earendil-works/pi/issues/10648), [#10999](https://github.com/earendil-works/pi/pull/10999) by [@masonc15](https://github.com/masonc15))

## [1.2.0] - 2026-10-12

### New Features

- **Per-key OpenRouter model lists**: with an OpenRouter key, Pi lists only the models that key may use, with the key's context size, max output, and prices, including regional endpoints set in `models.json`. See [OpenRouter](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/providers.md#openrouter).
- **Published configuration schemas**: add `$schema` to `settings.json`, `models.json`, keybindings, and themes for editor validation and completion. See [Settings](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/settings.md), [Models](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md), [Keybindings](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/keybindings.md), and [Themes](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/themes.md).
- **Clipboard copies over remote sessions**: `PI_CLIPBOARD_OSC52=1` sends copied text to a remote client's clipboard when Pi cannot detect the remote session, such as a multiplexer attached from another machine. See [Pi Process Configuration](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/environment-variables.md#pi-process-configuration).
- **Codemode improvements**: tool declarations show input constraints such as integer, minimum/maximum, and default, and codemode rows show elapsed and total time. See [Codemode](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/codemode.md).
- **`before_agent_start` for extension-triggered runs**: runs started by `pi.sendMessage(..., { triggerTurn: true })` go through the same setup as prompts. See [Events and concurrency](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/extensions.md#events-and-concurrency).

### Breaking Changes

- Published generated configuration schemas for models, settings, keybindings, and themes at `https://pi.dev/schemas/*.schema.json`. The theme schema moved to `https://pi.dev/schemas/theme.schema.json`; themes loaded during startup now receive the same schema validation as later reloads. Update theme `$schema` references, define reusable colors under `vars`, and remove unsupported metadata ([#9880](https://github.com/earendil-works/pi/pull/9880), [#10751](https://github.com/earendil-works/pi/pull/10751) by [@christianklotz](https://github.com/christianklotz))
- Changed `before_agent_start` to also fire for runs started by `pi.sendMessage(..., { triggerTurn: true })` while idle. `BeforeAgentStartEvent` is now a union on `messageType`: `"user"` events carry `prompt` and `images`, and `"custom"` events carry the starting `message` and no `prompt`. Messages returned by handlers are added to both kinds of run, and pending `deliverAs: "nextTurn"` messages are delivered with the custom-message run. Handlers that should act only on user prompts must check `event.messageType === "user"` ([#10267](https://github.com/earendil-works/pi/issues/10267), [#5581](https://github.com/earendil-works/pi/issues/5581), [#10739](https://github.com/earendil-works/pi/pull/10739) by [@davidbrai](https://github.com/davidbrai))
- Changed the session to count as busy while a run starts, including during `before_agent_start` handlers: `ctx.isIdle()` is false, `pi.sendMessage()` queues into the starting run instead of starting a second run that failed with "Agent is already processing", `pi.sendUserMessage()` requires `deliverAs`, and an abort requested meanwhile aborts the run once it starts ([#10739](https://github.com/earendil-works/pi/pull/10739) by [@davidbrai](https://github.com/davidbrai))
- Changed `pi mcp list --json` to report `resources: true` for servers that offer resources instead of `resources` and `resourceTemplates` counts; Pi no longer lists resources when connecting ([#10526](https://github.com/earendil-works/pi/issues/10526))

### Added

- Added `reachesTools` to tool definitions, so tools that reach other tools (such as `codemode` and `tool_search`) declare which tools a call may reach; the MCP extension uses it to wait for the servers a call needs and to decide whether a replacement `codemode` or `tool_search` tool can reach MCP tools
- Added `aliases` to tool namespaces; codemode's `describeNamespace()` and the `namespace` option of `searchTools()` match them, and MCP namespaces use the server name
- Added per-key OpenRouter model lists: with an OpenRouter key, Pi lists only the chat models that key may use, with the key's context size, max output, and prices, including guardrails and regional endpoints set as the base URL in `models.json`. The list is saved and used offline ([#10353](https://github.com/earendil-works/pi/issues/10353), [#10672](https://github.com/earendil-works/pi/pull/10672) by [@davidbrai](https://github.com/davidbrai))
- Added `PI_CLIPBOARD_OSC52=1` to send copied text to the terminal with OSC 52 after the local clipboard write, so copies reach a remote client's clipboard when Pi cannot detect the remote session, such as multiplexer attaches from another machine or remote IDE daemons ([#10826](https://github.com/earendil-works/pi/issues/10826), [#10835](https://github.com/earendil-works/pi/issues/10835), [#10114](https://github.com/earendil-works/pi/issues/10114))
- Added elapsed time while a codemode script runs and its total time once finished to the codemode tool row, like bash rows ([#10708](https://github.com/earendil-works/pi/issues/10708))

### Changed

- Changed the `showHardwareCursor` setting to use only the terminal cursor instead of also drawing Pi's reverse-video cursor
- Changed codemode tool declarations to show input constraints such as integer, minimum/maximum, length, pattern, and default as `@` tags on property comments, so scripts see them without the tool repeating them in descriptions ([#10707](https://github.com/earendil-works/pi/issues/10707))
- Changed codemode declarations of MCP tools to spell out the result type (`content`, `structuredContent`, `isError`) instead of referring to `CallToolResult<T>`, which `describeTool()`, `searchTools()`, and `ALL_TOOLS` showed without defining it; the codemode description no longer includes the shared MCP types
- Changed `serializeConversation()` (compaction, branch summaries, bug reports) to omit thinking blocks; replayed thinking is often not in the live context, so including it could make a summarization request larger than the context it summarizes and fail

### Fixed

- Fixed codemode ignoring a `// @options:` line that is not the first line of the script, which ran the script without the requested `timeout_ms`; the call now fails with an error before the script runs ([#10631](https://github.com/earendil-works/pi/issues/10631))
- Fixed Mistral streams being aborted mid-generation (e.g. during long thinking) after the request timeout; the timeout now applies only to waiting for response headers ([#10609](https://github.com/earendil-works/pi/issues/10609))
- Fixed a symlinked `AGENTS.md` in a git worktree nested inside its main repo causing no project context file to load ([#10681](https://github.com/earendil-works/pi/issues/10681))
- Fixed the code mode tool description claiming every failed tool call rejects; a tool that declares an output schema resolves with its value on failure too (e.g. `bash` with a nonzero exit)
- Fixed runs started by `pi.sendMessage(..., { triggerTurn: true })` removing system prompt sections added in `before_agent_start` after their first tool call, which changed the prompt mid-run and broke the provider prompt cache twice per run ([#10267](https://github.com/earendil-works/pi/issues/10267), [#10739](https://github.com/earendil-works/pi/pull/10739) by [@davidbrai](https://github.com/davidbrai))
- Fixed codemode blocking the process for seconds to minutes after scripts with many `text()` calls; joining the output items was quadratic ([#10678](https://github.com/earendil-works/pi/issues/10678))
- Fixed print mode (`-p`) exiting 0 without a warning when the final response was cut off at the model's output token limit; it now prints the partial text, writes a warning to stderr, and exits 1 ([#10799](https://github.com/earendil-works/pi/issues/10799))
- Fixed `pi mcp login --help` and the CLI docs describing `--timeout` as only the wait for the browser; it limits the whole sign-in ([#10636](https://github.com/earendil-works/pi/issues/10636))
- Fixed `~` not being expanded in `!pattern`, `+path`, and `-path` entries of the `extensions`, `skills`, `prompts`, and `themes` settings, so entries like `!~/skills/pdf` matched nothing ([#10765](https://github.com/earendil-works/pi/issues/10765))
- Fixed MCP servers with resources registering no tools until every resource was listed; Pi no longer lists resources when connecting, so `/mcp` and `pi mcp list` show that a server offers resources instead of counting them ([#10526](https://github.com/earendil-works/pi/issues/10526))
- Fixed MCP tool calls failing when the server returns structured content that is not an object (an array, `null`, or a primitive, as MCP 2026-07-28 allows); codemode declarations of MCP tools without an output schema now type `structuredContent` as `unknown` instead of an object ([#10416](https://github.com/earendil-works/pi/issues/10416))
- Fixed reading or writing `auth.json` on Windows failing with `EPERM` when the previous lock folder was still being deleted; Pi now retries briefly before reporting the error ([#10801](https://github.com/earendil-works/pi/issues/10801))
- Fixed OpenRouter router models such as `openrouter/auto` showing a cost of -$1,000,000 per 1M tokens; OpenRouter's negative placeholder prices are now 0 ([#10672](https://github.com/earendil-works/pi/pull/10672) by [@davidbrai](https://github.com/davidbrai))
- Fixed Anthropic requests failing when the provider rejects the strict tool set for grammar size, tool count, or union limits; Pi now retries once with preferred tools non-strict ([#10409](https://github.com/earendil-works/pi/issues/10409))
- Fixed "The upstream provider returned an error" not being retried as a transient provider error ([#10842](https://github.com/earendil-works/pi/issues/10842))
- Fixed focused fullscreen overlays blocking mouse-wheel scrolling of the transcript ([#10769](https://github.com/earendil-works/pi/issues/10769))
- Fixed fragmented terminal color replies leaking hex values into the prompt and opening the external editor (related reports: [#10256](https://github.com/earendil-works/pi/issues/10256), [#10657](https://github.com/earendil-works/pi/issues/10657))
- Fixed inline images not rendering in Herdr since 1.1.0 ([#10774](https://github.com/earendil-works/pi/pull/10774) by [@ogulcancelik](https://github.com/ogulcancelik))
- Fixed key bindings that name a shifted symbol, such as `+` or `ctrl++`, not matching under the Kitty keyboard protocol or modifyOtherKeys ([#9880](https://github.com/earendil-works/pi/pull/9880) by [@christianklotz](https://github.com/christianklotz))
- Fixed the compaction status indicator embedded in a custom editor using the default muted colors instead of the editor border or thinking-level color, as the working indicator does ([#10809](https://github.com/earendil-works/pi/issues/10809), [#10810](https://github.com/earendil-works/pi/pull/10810) by [@Jay-Madden](https://github.com/Jay-Madden))
- Fixed MCP tool calls that were cancelled or timed out while waiting for an OAuth refresh still being sent to the server once the refresh finished ([#10598](https://github.com/earendil-works/pi/issues/10598))
- Fixed MCP OAuth sign-in accepting an authorization response with an `iss` parameter that could not be checked because no authorization server metadata was discovered; sign-in now fails with an issuer mismatch. Reported by [@AizenvoltPrime](https://github.com/AizenvoltPrime)
- Fixed codemode failing with a broken bridge error when Pi runs under `node --watch` on Node 24 or 26 ([#10725](https://github.com/earendil-works/pi/issues/10725))

### Removed

- Removed the unreleased experimental server, client, and plugin stack (`src/experimental`, `src/cli/experimental`) and its source-only `./client` and `./experimental/plugin` exports; none of it was part of the published package. The `@earendil-works/pi-client`, `@earendil-works/pi-protocol`, and `@earendil-works/pi-server` packages it used are removed and no longer released
- Removed the dependency on `@earendil-works/chord`

## [1.1.0] - 2026-10-07

### New Features

- **Program status reporting**: terminals and agent dashboards that support OSC 7501 see whether Pi is working, blocked on a dialog or login, done, or failed. See [Program status](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/terminal-setup.md#program-status).
- **Claude Haiku 5.5**: `anthropic/claude-haiku-5-5`, with adaptive thinking up to `xhigh`/`max` effort.
- **Adjust default tools with `+name`/`-name`**: `--tools` entries like `pi -t +codemode,-write` change the default selection instead of replacing it. See [Tools](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/cli.md#tools).
- **GPT-6 Luna and image classification**: OpenAI's GPT-6 Luna is available as a classifier model through the Decisions API, and codemode's `models.classify()` accepts images for classifiers that support them. See [Use classifier models](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md#use-classifier-models).
- **Native llama.cpp decision models**: Julia-1, Laya, Kev, lev, and OpenJev served by llama.cpp 0.6.0 or later run natively as classifiers through `/v1/systemone`. See [Classification](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/llama-cpp.md#classification).

### Added

- Added `+name` and `-name` entries to `--tools`, which change the default tool selection instead of replacing it, for example `pi -t +codemode`
- Added `durationMs` to the tool render context and to `tool_execution_end` extension events: the recorded execution time of a final tool result ([#10549](https://github.com/earendil-works/pi/issues/10549))
- Added `outputPad` to the tool render context ([#10557](https://github.com/earendil-works/pi/pull/10557) by [@rwachtler](https://github.com/rwachtler))
- Added OpenAI's GPT-6 Luna as a classifier model through the Decisions API, available with `OPENAI_API_KEY` (see [Use classifier models](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md#use-classifier-models))
- Added `images` to codemode's `models.classify()` context, so classifiers that accept images, such as GPT-6 Luna, can judge them
- Added program status reporting with OSC 7501: terminals and agent dashboards that support it see whether Pi is working, blocked on a dialog or login, done, or failed. `PI_PROGRAM_STATUS=1|0` overrides detection (see [Terminal setup](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/terminal-setup.md#program-status)) ([#10607](https://github.com/earendil-works/pi/issues/10607))
- Added `aborted` to `agent_settled` session, extension, and JSON events, so integrations can tell a cancelled run from a finished one ([#10607](https://github.com/earendil-works/pi/issues/10607))
- Added Claude Haiku 5.5 (`anthropic/claude-haiku-5-5`), with adaptive thinking up to `xhigh`/`max` effort and prompt caching on Bedrock
- Added native llama.cpp decision models: Julia-1, Laya, Kev, lev, and OpenJev served by llama.cpp 0.6.0 or later are listed only as classifiers through `/v1/systemone` instead of as chat models (see [Classification](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/llama-cpp.md#classification)) ([#10382](https://github.com/earendil-works/pi/pull/10382))

### Changed

- Changed `outputPad` to also apply to `!` command output, tool output, and summary blocks ([#9946](https://github.com/earendil-works/pi/issues/9946), [#10557](https://github.com/earendil-works/pi/pull/10557) by [@rwachtler](https://github.com/rwachtler))
- Changed `pi mcp login --timeout` to limit the whole sign-in, including requests to the authorization server, instead of only the wait for the browser ([#10565](https://github.com/earendil-works/pi/issues/10565))

### Fixed

- Fixed bash and PowerShell results losing `Took` after reloading a session, and the live `Took` including wall-clock steps; both now show the recorded execution time ([#10549](https://github.com/earendil-works/pi/issues/10549))
- Fixed managed installs keeping every old release; `pi update` now keeps only the new release and the one it updated from ([#10392](https://github.com/earendil-works/pi/issues/10392), [#10511](https://github.com/earendil-works/pi/pull/10511) by [@davidbrai](https://github.com/davidbrai))
- Fixed standalone binaries loading `.env`, `.env.local`, and `.env.development` from the launch directory into Pi's environment ([#10473](https://github.com/earendil-works/pi/issues/10473))
- Fixed `!!` command headers losing their dim color once output arrives ([#10557](https://github.com/earendil-works/pi/pull/10557) by [@rwachtler](https://github.com/rwachtler))
- Fixed the codemode description not marking `searchTools()`, `describeTool()`, and `describeNamespace()` as async, which led models to serialize the unawaited promise as `{}` ([#10555](https://github.com/earendil-works/pi/issues/10555))
- Fixed codemode output items running together, so models could not tell where one `text()` or `console.log()` output ended and the next began. With several text items, each now starts with a `==> text N/M <==` line, and `console` calls follow the other output in one `<console_output>` block with one line per call
- Fixed `/mcp` waiting for all servers to connect before opening; the manager now updates live and remains usable while enabling, reconnecting, or disabling servers ([#10562](https://github.com/earendil-works/pi/issues/10562))
- Fixed images being dropped as "could not be resized" when running under `node --watch` on Node 24.19+ and 26.x, where Node posts its own messages on the image resize worker channel ([#10527](https://github.com/earendil-works/pi/issues/10527))
- Fixed clipboard paste doing nothing in Termux, and failed copies there omitting the Termux:API install hint ([#10391](https://github.com/earendil-works/pi/issues/10391))
- Fixed `!` and RPC `bash` output keeping fragments of color codes, such as a stray `m`, when a code was split across output chunks ([#10504](https://github.com/earendil-works/pi/issues/10504))
- Fixed MCP OAuth sign-ins that could not be cancelled while waiting on the authorization server and kept running after the session ended. The sign-in screen now cancels with Esc at every step, session shutdown aborts a running sign-in, and each request to the authorization server times out after 15 seconds ([#10565](https://github.com/earendil-works/pi/issues/10565))
- Fixed shutdown waiting up to 15 seconds to refresh an MCP OAuth token that was about to expire, only to close the server's session ([#10565](https://github.com/earendil-works/pi/issues/10565))
- Fixed the fullscreen text selection surviving session switches and other transcript rebuilds, which highlighted unrelated text in the new transcript ([#9311](https://github.com/earendil-works/pi/issues/9311), [#10567](https://github.com/earendil-works/pi/pull/10567) by [@christianklotz](https://github.com/christianklotz))
- Fixed OpenAI models on Bedrock ignoring the thinking level and always running at Bedrock's default reasoning effort ([#9331](https://github.com/earendil-works/pi/issues/9331), [#10142](https://github.com/earendil-works/pi/pull/10142) by [@jsanter27](https://github.com/jsanter27))
- Fixed model `headers` in `models.json` not overriding the `originator` and `User-Agent` headers of Codex requests ([#10429](https://github.com/earendil-works/pi/pull/10429) by [@lucasmeijer](https://github.com/lucasmeijer))
- Fixed `server_busy` and `servers are currently busy` provider errors ending the turn instead of being retried ([#10543](https://github.com/earendil-works/pi/issues/10543))
- Fixed Mistral responses that end with `finish_reason: "error"` not being retried ([#10487](https://github.com/earendil-works/pi/issues/10487))
- Reduced context-limit request failures by estimating input at 3.5 characters per token instead of 4 when calculating output limits ([#10497](https://github.com/earendil-works/pi/issues/10497))
- Fixed Radius models disabled by an organization owner still being listed
- Fixed Anthropic browser login failing with "localhost refused to connect" when port 53692 is reserved or in use, for example by Hyper-V/WSL port exclusions on Windows: login now falls back to a free loopback port ([#10571](https://github.com/earendil-works/pi/issues/10571))
- Fixed session costs undercounting long prompts on models with prompt-length pricing tiers, such as Claude Haiku 5.5, Gemini 3.1 Pro, and GPT-5.4, through OpenCode, OpenCode Go, OpenRouter, Vercel AI Gateway, Google, MiniMax, and other providers
- Fixed Markdown links not being clickable in Herdr ([#10573](https://github.com/earendil-works/pi/issues/10573))

## [1.0.4] - 2026-10-05

### New Features

- **Tool patterns and `--no-mcp`**: `--tools` and `--exclude-tools` accept `*` patterns, for example `--tools read,codemode,'mcp__radius__*'` keeps only one MCP server's tools. `--tools` now keeps MCP tools unless an entry starts with `mcp__`, and `--no-mcp` turns off MCP for one run. See [Tools](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/cli.md#tools) and [MCP tools](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/cli.md#mcp-tools).
- **Codemode persists images**: `tools.read()` on an image file now gives back an image block that `image()` can show. See [Call tools](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/codemode.md#call-tools).

### Added

- Added `*` patterns to `--tools` and `--exclude-tools`, for example `--tools read,codemode,'mcp__radius__*'`
- Added `--no-mcp` to disable the built-in MCP support for one run

### Fixed

- Fixed syntax highlighting losing colors after the first line of multiline strings and comments in fenced code blocks ([#10143](https://github.com/earendil-works/pi/issues/10143))
- Fixed codemode scripts not receiving images from `read`: `tools.read()` now resolves to an image block for image files, which `image()` shows ([#10251](https://github.com/earendil-works/pi/issues/10251))
- Fixed MCP OAuth sign-in failing with `invalid_redirect_uri` on servers with OpenID Connect client registration, such as `mcp.modem.dev`: pi now registers as a native client ([#10493](https://github.com/earendil-works/pi/issues/10493))
- Fixed `--tools` removing MCP tools, which left `pi --tools codemode` without any MCP servers. `--tools` now keeps MCP tools unless an entry starts with `mcp__`
- Fixed MCP session shutdown returning while a server was still connecting, leaving its transport open until the server answered or timed out ([#10249](https://github.com/earendil-works/pi/issues/10249))
- Fixed system prompt rules and the skills hint naming tools hidden by `prepareLoadout`. Hidden tools are left out of the rules, the skills hint names no tool when the file reader is hidden, and `codemode` shows each tool's prompt guidelines with its declaration; `ToolLoadout` gains `getPromptGuidelines()` ([#10343](https://github.com/earendil-works/pi/issues/10343))
- Fixed Bedrock requests that fail with `The pending stream has been canceled` after a stalled HTTP/2 connection not being retried automatically ([#10379](https://github.com/earendil-works/pi/issues/10379))
- Fixed codemode scripts that patch built-ins (for example `Array.prototype.toJSON = ...`) crashing pi and leaving the tool call unsettled. Built-ins are now frozen before the script runs, so such patches have no effect ([#10444](https://github.com/earendil-works/pi/issues/10444))

## [1.0.3] - 2026-10-05

### New Features

- **Azure Foundry Chat Completions** — The `azure` provider (renamed from `azure-openai-responses`) now also serves Foundry Chat Completions deployments, starting with `azure/deepseek-v4-pro`. See [Azure OpenAI](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/providers.md#azure-openai).
- **Codemode images saved to files** — `image()` also writes each image to a temp file and names the path in the result, so later turns can copy or move generated images. See [Generate images](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/codemode.md#generate-images).

### Breaking Changes

- Renamed the Azure provider from `azure-openai-responses` to `azure`. Rename the provider key in `auth.json` (or run `/login` again), in `models.json`, and in `settings.json` (`defaultProvider`, `enabledModels` patterns, and `modelThinkingLevels` keys). Sessions that used the old provider fall back to another model when resumed, and their prompt cache is not reused. The `AZURE_OPENAI_*` environment variables are unchanged ([#9714](https://github.com/earendil-works/pi/pull/9714) by [@jsanter27](https://github.com/jsanter27))

### Added

- Added Azure Foundry Chat Completions deployments, starting with `azure/deepseek-v4-pro` ([#9645](https://github.com/earendil-works/pi/issues/9645), [#9714](https://github.com/earendil-works/pi/pull/9714) by [@jsanter27](https://github.com/jsanter27))

### Changed

- Codemode `image()` now also saves each image to a temp file and names the path in the result, so later turns can copy or move generated images ([#10310](https://github.com/earendil-works/pi/issues/10310))
- Output files (full text of truncated tool output, binary MCP resources, codemode images) are now readable only by the user
- `Home`/`End` now always move the editor cursor to the line start/end; fullscreen transcript top/bottom moved to `Ctrl+Home`/`Ctrl+End`, which no longer move the editor cursor ([#10314](https://github.com/earendil-works/pi/issues/10314))

### Fixed

- Fixed subscription logins such as Sign in with ChatGPT failing with `refresh_token_invalidated` after a request was cancelled during an OAuth token refresh
- Fixed codemode failing for the rest of a session after a pnpm global update removed the running install, and added a restart hint when errors occur after pi was updated or removed on disk ([#10439](https://github.com/earendil-works/pi/issues/10439))
- Fixed interactive sessions reporting a `read EIO` or `setRawMode EIO` crash (and asking to run /bug) when the terminal went away, e.g. after closing the window or resuming a suspended pi in a closed terminal

## [1.0.2] - 2026-10-04

### New Features

- **Sampling by thinking level** — `samplingParamsByThinkingLevel` in `models.json` sets sampling parameters such as `temperature` and `top_p` for each thinking level on OpenAI-compatible APIs. See [Configure sampling by thinking level](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md#configure-sampling-by-thinking-level).

### Added

- Added `samplingParamsByThinkingLevel` to `models.json` for per-thinking-level sampling parameter overrides on OpenAI-compatible APIs. See [Configure sampling by thinking level](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md#configure-sampling-by-thinking-level) ([#9776](https://github.com/earendil-works/pi/pull/9776) by [@mrexodia](https://github.com/mrexodia))

## [1.0.1] - 2026-10-03

### New Features

- **Nix flake** — `nix run github:earendil-works/pi/stable` runs the latest release, and `nix profile add github:earendil-works/pi/stable` installs it. See [Install pi](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/quickstart.md#1-install-pi).
- **Project overrides for MCP servers** — `.pi/mcp.json` and `/mcp` can enable, disable, or change the exposure of a user-level server for one project. See [Configure servers](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/mcp.md#configure-servers).
- **MCP Client ID Metadata Documents** — `oauth.clientRegistration: "cimd"` lets authorization servers allow pi by its document URL instead of dynamic registration. See [Authenticate with OAuth](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/mcp.md#authenticate-with-oauth).
- **Tool renderers for any tool** — `pi.registerToolRenderer()` draws calls to tools that are not registered yet, such as MCP tools in resumed sessions. See [Tool rendering](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/extensions.md#tool-rendering).
- **Cloudflare Clef classifiers** — `@cf/cloudflare/clef` and `@cf/cloudflare/clef-flash` are usable from codemode scripts and extensions. See [Use classifier models](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md#use-classifier-models).

### Added

- Added a copy key (`app.message.copy`, default `ctrl+x`) to OAuth sign-in screens in `/login`, `/mcp`, and `/mcp login`, which copies the sign-in URL when the browser cannot be opened or the wrapped link cannot be selected.
- Added `oauth.clientRegistration: "cimd"` for MCP servers, which identifies pi with its Client ID Metadata Document on pi.dev instead of dynamic client registration, so authorization servers can allow pi by URL ([#10302](https://github.com/earendil-works/pi/issues/10302))
- Added project overrides for user-level MCP servers: a `.pi/mcp.json` entry without `command` or `url` sets only `enabled`, `exposure`, and `toolExposure` of the user-level server, and `/mcp` can enable or disable a server for the current project ([#10277](https://github.com/earendil-works/pi/issues/10277))
- Added Cloudflare's Clef and Clef Flash classifier models to `cloudflare-workers-ai`, usable from codemode scripts and extensions ([#10316](https://github.com/earendil-works/pi/pull/10316) by [@ndisidore](https://github.com/ndisidore), [#10322](https://github.com/earendil-works/pi/pull/10322) by [@RealAlexandreAI](https://github.com/RealAlexandreAI))
- Added `pi.registerToolRenderer()`, which chooses how calls to a tool are drawn, including tools that are not registered ([#10285](https://github.com/earendil-works/pi/issues/10285))
- Added a Nix flake for macOS and Linux: `nix run github:earendil-works/pi/stable` runs the latest release, and `nix profile add github:earendil-works/pi/stable` installs it. See [Install pi](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/quickstart.md#1-install-pi) ([#9137](https://github.com/earendil-works/pi/pull/9137))

### Changed

- `pi update` on global npm installations now recommends migrating to the managed installation from the pi.dev installer, which pins all dependencies.
- Anthropic tools added or redefined mid-conversation are now defined inline in the conversation, so redefining a tool under the same name keeps the prompt cache instead of resending the full tool list.

### Fixed

- Fixed installations resolving vulnerable `brace-expansion` 5.0.9 by pinning `brace-expansion` 5.0.12 as a direct dependency (GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-6j4f-fj2g-mc7p) ([#10288](https://github.com/earendil-works/pi/issues/10288))
- Fixed a trailing comma in `--models` adding an extra model to the model cycle ([#10334](https://github.com/earendil-works/pi/issues/10334))
- Fixed a `codemode` script that prints in a loop crashing pi by running out of memory: a script fails once its output passes 16 Mi characters or 100000 items ([#10283](https://github.com/earendil-works/pi/issues/10283))
- Fixed JPEG, GIF, and WebP images rendered by extensions through `Image` not appearing in Kitty, Ghostty, WezTerm, and Warp ([#10292](https://github.com/earendil-works/pi/issues/10292))
- Fixed MCP tool calls in resumed sessions and HTML exports rendering fully expanded until their server connected, or for good if it never did ([#10285](https://github.com/earendil-works/pi/issues/10285))
- Fixed fullscreen Kitty images collapsing to a one-row strip after scrolling in WezTerm ([#10319](https://github.com/earendil-works/pi/issues/10319))
- Fixed "Selected model is at capacity" provider errors ending the turn instead of being retried ([#10278](https://github.com/earendil-works/pi/issues/10278))
- Fixed Cloudflare AI Gateway Claude models failing with a 404 by using dashed model IDs (`claude-opus-5-5` instead of `claude-opus-5.5`)
- Fixed Sign in with ChatGPT continuing when its callback port is taken by another login, which made the browser show "OAuth state mismatch"; it now fails with a port-in-use error ([#10265](https://github.com/earendil-works/pi/issues/10265))
- Fixed Amazon Bedrock OpenAI models costing requests above 272k input tokens at the short-context rate; Bedrock models now include the pricing tiers listed on models.dev ([#10326](https://github.com/earendil-works/pi/issues/10326))
- Fixed Amazon Bedrock Claude requests failing with "Invalid `signature` in `thinking` block" after the system prompt or tools changed ([#10324](https://github.com/earendil-works/pi/issues/10324))
- Fixed Together DeepSeek V4 Pro losing its thinking level controls after Together renamed it to `deepseek-ai/DeepSeek-V4-Pro-0813` ([#10336](https://github.com/earendil-works/pi/pull/10336) by [@cv](https://github.com/cv))
- Fixed the default NVIDIA model pointing at `nvidia/nemotron-3-super-120b-a12b`, which NVIDIA no longer serves; the default is now `nvidia/nemotron-3-ultra-550b-a55b`

### Removed

- Removed `npm-shrinkwrap.json` from the published package. npm installations no longer pin transitive dependencies, and library consumers can now override them. Use the pi.dev installer for pinned installations ([#5653](https://github.com/earendil-works/pi/issues/5653))

## [1.0.0] - 2026-10-01

### New Features

- **Fullscreen by default** — The TUI now runs fullscreen. Set `tuiMode` to `"regular"` to keep the terminal's normal scrollback. See [Terminal and display](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/settings.md#terminal-and-display).
- **Leaner codemode** — About 40% fewer prompt tokens, and errors that tell the model how to recover. See [Codemode](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/codemode.md).
- **Image generation in codemode** — Scripts call `models.generateImages()` with the session's credentials. See [Generate images](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/codemode.md#generate-images) and [Use image models](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md#use-image-models).
- **Radius in `/login`** — Sign in with Radius and set up its MCP server in one step. See [Radius](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/providers.md#radius).
- **Anthropic copy code login** — Sign in when the browser runs on another machine. See [Authenticate interactively](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/providers.md#authenticate-interactively).
- **MCP OAuth hardening** — `oauth.authServerMetadataUrl`, RFC 9207 `iss` checks, credentials per server, and step-up sign-in that keeps granted scopes. See [Authenticate with OAuth](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/mcp.md#authenticate-with-oauth).
- **Header-only quiet startup** — `quietStartup: "header"` keeps the version and key hints and hides the rest. See [Terminal and display](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/settings.md#terminal-and-display).

### Added

- Added an `oauth.authServerMetadataUrl` setting for MCP servers that advertise a wrong OAuth authorization server or none. Pi uses the configured metadata document instead of discovery ([#10172](https://github.com/earendil-works/pi/issues/10172)).
- Added `quietStartup: "header"`, which keeps the startup header with version and key hints but hides the model scope line and loaded-resource listing.
- Added `models.generateImages()` to codemode scripts. It runs image models such as OpenRouter's with the session's credentials and returns base64 image blocks that `image()` attaches to the result; usage counts toward the session cost like `models.classify()`. Extensions can call `ctx.modelRegistry.generateImages()`. See [Use image models](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md#use-image-models).
- Added a copy code login method to Anthropic `/login` for headless setups where the browser runs on another machine ([#10194](https://github.com/earendil-works/pi/pull/10194) by [@lucasmeijer](https://github.com/lucasmeijer)).

### Changed

- Changed the default TUI mode to fullscreen. Set `tuiMode` to `"regular"` or pass `--tui-mode regular` to keep the terminal's normal scrollback.
- `/login` now offers "Sign in with Radius" at the top level, as the last option, with its status. After a Radius sign-in, `/login` offers to configure the Radius MCP server in the global `mcp.json` with `"auth": { "provider": "radius" }` and reloads. Cancelling a login returns to the menu it was started from.
- The provider docs page is renamed to [Providers](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/providers.md), its "Cloud Providers" section is now "Provider Specific Config", and it documents Radius first.
- MCP OAuth credentials are now stored per server name and URL, so MCP servers with the same URL can sign in with different accounts. Credentials stored by URL alone move to the first server that uses them ([#10252](https://github.com/earendil-works/pi/issues/10252)).
- Codemode costs far fewer prompt tokens: with the default tools and codemode active, a GPT-5.6 request shrinks from about 5,300 to 3,300 tokens. The `codemode` description lists the script globals in one line each and points to the new [Codemode](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/codemode.md) reference for the `models` API, which the model reads when it needs it. Declared tools say in one line how scripts call them and what the call resolves to, instead of repeating their full declaration, and the system prompt's codemode guidance and MCP server section are shorter.
- Codemode errors now say how to recover: reading a tool or `models` member that does not exist names the close matches (`tools.Bash` suggests `tools.bash`), `models.classify()` and `models.generateImages()` reject malformed arguments with the expected shape, an unknown model points to `models.getAvailableOfType()`, an oversized `store()` value explains what the store is for, and a script that generates images without showing them gets a note. Scripts that probed for a tool with `typeof tools.name` must use `"name" in tools`.
- `/login` and `/logout` now label providers without credentials as "not configured" instead of "unconfigured".
- OAuth browser pages now show the color Pi logo.

### Fixed

- Fixed MCP OAuth sign-in accepting an authorization response whose `iss` parameter names another authorization server; the code is now rejected before it is exchanged (RFC 9207).
- Fixed MCP OAuth sign-in failing with `Invalid scope` when the token response contains `"scope": ""`, and similar failures for other empty or `null` optional OAuth fields ([#10266](https://github.com/earendil-works/pi/issues/10266)).
- Fixed the sign-in URL printed by `/mcp login` not being clickable when it wraps ([#10186](https://github.com/earendil-works/pi/issues/10186)).
- Fixed `--provider` without `--model` being silently ignored and running the default model from another provider; it now fails with an error ([#10236](https://github.com/earendil-works/pi/issues/10236)).
- Fixed MCP servers that ask for more scope (`insufficient_scope`) requesting sign-in over and over. The new sign-in requested only the missing scopes, so the new token lost access the previous one had; it now keeps the granted scopes.
- Fixed user messages in the transcript keeping two full-width copies of every rendered line; they keep one, with identical output.
- Fixed `/login` and `/logout` labeling every OAuth sign-in, including Radius, as a subscription; only subscription-backed providers say "subscription", other OAuth sign-ins say "account".
- Fixed the startup header logo rendering with gaps in Apple Terminal; it now shows a colored "Pi" with the version instead.
- Fixed deferred MCP tools that `tool_search` loaded being dropped on resume and `/reload` even when their server reconnected before the next prompt, because the session restored its tools before the MCP servers reconnected.
- Fixed the system theme making pastel palettes such as Catppuccin Frappe much more vivid; palette colors now keep their chroma ([#10255](https://github.com/earendil-works/pi/issues/10255), [#10293](https://github.com/earendil-works/pi/pull/10293) by [@dgtlntv](https://github.com/dgtlntv)).
- Fixed slash command autocompletion not triggering when the input starts with whitespace ([#10218](https://github.com/earendil-works/pi/pull/10218) by [@haoqixu](https://github.com/haoqixu)).
- Fixed color bleeding past mouse selections and search highlights in fullscreen mode when a styled token ends at the highlight boundary ([#10169](https://github.com/earendil-works/pi/issues/10169)).
- Fixed memory retained per rendered message in the transcript; a long assistant message keeps about a fifth of the heap it kept before.

## [0.99.2] - 2026-09-30

### New Features

- MCP servers stay out of the way: servers with the default `codemode` exposure are no longer listed in the `codemode` description and no longer block the first prompt. They appear in a short system prompt section, and scripts find their tools with `searchTools()` and `describeNamespace()`. See [Control tool exposure](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/mcp.md#control-tool-exposure).
- More MCP authentication options: `oauth.clientName` for servers that only accept known OAuth clients, and `"auth": { "provider": "<provider>" }` to authenticate HTTP servers with a provider's `/login` token. See [Authenticate with OAuth](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/mcp.md#authenticate-with-oauth).
- Anthropic workload identity federation from the Anthropic SDK environment variables. See [Use an API key from the environment](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/providers.md#use-an-api-key-from-the-environment).
- `/reload` enables tools newly added to the `defaultTools` setting. See [Tools](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/settings.md#tools).

### Added

- Added a `description` field for MCP servers (`pi mcp add --description`), shown with the server in the system prompt and used to rank its tools in tool search, and a `describeNamespace(name)` codemode helper that returns a namespace's instructions and tool names. `describeNamespace()` and `searchTools()` accept a namespace as `mcp__dev-radius`, `mcp__dev_radius`, `dev-radius`, or `dev_radius`.
- Added an `oauth.clientName` setting for MCP servers (`pi mcp add --oauth-client-name`) to change the client name sent during OAuth client registration, for servers that only accept known clients ([#10226](https://github.com/earendil-works/pi/issues/10226)).
- Added `"auth": { "provider": "<provider>" }` for HTTP MCP servers to send a provider's current `/login` token as the bearer token instead of using MCP OAuth. The token is read on every request, so provider refreshes apply. Only allowed in the global `mcp.json` and from extensions, and requires https except on loopback hosts.
- Added Anthropic workload identity federation from the `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, and `ANTHROPIC_IDENTITY_TOKEN_FILE` environment variables (see [Providers](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/providers.md)) ([#10177](https://github.com/earendil-works/pi/issues/10177), [#10242](https://github.com/earendil-works/pi/pull/10242) by [@philfreo](https://github.com/philfreo)).
- `/reload` now enables tools newly added to the `defaultTools` setting. Tools removed from it stay enabled, tools turned off during the session stay off unless newly added, and `--tools`, `--no-tools`, and `--no-builtin-tools` still override the setting ([#10245](https://github.com/earendil-works/pi/issues/10245)).

### Changed

- MCP servers with the default `codemode` exposure no longer appear in the `codemode` description; scripts find them with `searchTools()`. `codemode-deferred` is now an alias for `codemode`. Use `direct` exposure for tools the model should see without searching ([#10212](https://github.com/earendil-works/pi/issues/10212)).
- The `codemode` description no longer includes deferred tools, tool counts, or MCP server instructions, so it no longer changes when MCP servers connect or change their tools. The `tool_search` description no longer lists the servers whose tools it can load, for the same reason. Servers are listed instead in an `mcp_servers` system prompt section with a one-line summary, updated at the start of each prompt; a changed section is appended to the conversation. Scripts read server instructions with `describeNamespace()` ([#10212](https://github.com/earendil-works/pi/issues/10212)).
- The first prompt no longer waits for MCP servers without `direct` tools. They connect in the background and are waited for when a codemode script names them, a script searches tools, or `tool_search` runs ([#10212](https://github.com/earendil-works/pi/issues/10212)).

### Fixed

- Fixed new sessions intermittently ignoring the saved default model, or warning that no models are available, when it belongs to an extension-registered native provider with a stored credential ([#9962](https://github.com/earendil-works/pi/issues/9962), [#10190](https://github.com/earendil-works/pi/pull/10190) by [@davidbrai](https://github.com/davidbrai)).
- Fixed the `/mcp` sign-in URL not being clickable when it wraps across lines, by emitting it as a terminal hyperlink with a `Cmd/Ctrl+click to open` line like `/login` ([#10186](https://github.com/earendil-works/pi/issues/10186)).
- Fixed codemode `image()` accepting malformed base64 data or unsupported image types, which persisted an invalid image block that made every later provider request fail with HTTP 400 ([#10215](https://github.com/earendil-works/pi/issues/10215)).
- Fixed codemode failing to start its script worker from the standalone Windows executable ([#10204](https://github.com/earendil-works/pi/issues/10204)).
- Fixed prompt submission slowing down with session length, because resolving the session's model selection looked up the model catalog once per assistant message ([#10198](https://github.com/earendil-works/pi/issues/10198)).
- Fixed model lookups slowing down for providers with a refreshed pi.dev catalog, because merging remote catalog models took quadratic time.
- Fixed the `built-in-tool-renderer.ts` and `minimal-mode.ts` extension examples removing the built-in tools' summaries and guidelines from the system prompt ([#10072](https://github.com/earendil-works/pi/issues/10072), [#10193](https://github.com/earendil-works/pi/pull/10193) by [@christianklotz](https://github.com/christianklotz)).
- Fixed context overflow detection for Z.AI CN endpoint `Prompt exceeds max length` errors ([#10208](https://github.com/earendil-works/pi/issues/10208)).
- Fixed Anthropic requests failing when a tool schema uses keywords Anthropic strict tool use rejects, such as `minimum`/`maximum`; such tools are now sent non-strict ([#9953](https://github.com/earendil-works/pi/issues/9953)).
- Fixed provider retries firing immediately when a `Retry-After` header contains an unparseable date; they now use exponential backoff ([#9571](https://github.com/earendil-works/pi/issues/9571)).
- Fixed extension commands registered without a string name or handler crashing pi when typing `/`; the extension now fails to load with an error instead ([#10054](https://github.com/earendil-works/pi/issues/10054)).
- Fixed collapsed `codemode` and MCP tool results filling the screen when the output is one long line, such as minified JSON. Like bash output, the preview is now limited to wrapped lines instead of logical lines.
- Fixed `codemode.mode: "only"` listing `read`, `bash`, `edit`, and `write` in the system prompt's tool list although requests only declare `codemode` ([#10192](https://github.com/earendil-works/pi/issues/10192)).
- Fixed codemode scripts calling the wrong MCP tool when two tool names differ only in `-` and `_`, such as `read-file` and `read_file`. Like in Codex, MCP tool and namespace names now replace `-` with `_` (`mcp__my-server__x` is now `mcp__my_server__x`), colliding tools of a server all get a hash suffix, and server names that differ only in `-` and `_` are rejected ([#10239](https://github.com/earendil-works/pi/issues/10239)).

## [0.99.1] - 2026-09-29

### New Features

- **GPT-6.1 Sol** — Available on OpenAI, Azure OpenAI, and OpenAI Codex, and now the default OpenAI Codex model. See [Select a model](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/models.md#select-a-model).

### Added

- Added GPT-6.1 Sol (`gpt-6.1-sol`) to the OpenAI, Azure OpenAI Responses, and OpenAI Codex providers.

### Changed

- Changed the default OpenAI Codex model to GPT-6.1 Sol (`gpt-6.1-sol`).

### Fixed

- Fixed `/login` with OpenAI failing in the bundled release with a missing `openai-chatgpt.js` module error.
