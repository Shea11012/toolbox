#!/usr/bin/env python3
"""Build versioned references from an installed Pi package, without network access.

Usage: python3 scripts/build-references.py [package_root_or_docs_dir] [output_dir]
Without a source argument, locate the package through the pi executable on PATH.
All required inputs are validated before writing any references.
"""

import argparse
from datetime import date
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urljoin

PACKAGE = "@earendil-works/pi-coding-agent"
SKILL_ROOT = Path(__file__).resolve().parent.parent
# Each official Markdown page belongs to exactly one bundle.
BUNDLES = {
    "cli-and-usage.md": ("CLI, Usage, Sessions & Keybindings", [
        "index.md", "quickstart.md", "usage.md", "cli.md", "slash-commands.md",
        "sessions.md", "keybindings.md", "environment-variables.md",
    ]),
    "providers-and-models.md": ("Providers & Models", [
        "providers.md", "models.md", "models-configuration.md", "custom-provider.md",
    ]),
    "settings-and-compaction.md": ("Configuration, Settings & Compaction", [
        "configuration.md", "settings.md", "compaction.md",
    ]),
    "extending-pi.md": ("Extensions, Skills, Prompt Templates, Themes & Packages", [
        "extensions.md", "skills.md", "prompt-templates.md", "themes.md", "packages.md",
    ]),
    "tui-components.md": ("TUI Components", ["tui.md"]),
    "security-and-containerization.md": ("Security & Containerization", [
        "security.md", "containerization.md",
    ]),
    "session-format.md": ("Session Format & Message Types", [
        "session-format.md", "message-types.md",
    ]),
    "programmatic.md": ("CLI Integration, SDK, RPC & JSON", [
        "cli-integration.md", "sdk.md", "rpc.md", "rpc-commands.md",
        "rpc-extension-ui.md", "json.md",
    ]),
    "platform-setup.md": ("Platform Setup", [
        "windows.md", "termux.md", "tmux.md", "terminal-setup.md", "shell-aliases.md",
    ]),
    "mcp.md": ("MCP Servers", ["mcp.md"]),
    "codemode.md": ("Codemode", ["codemode.md"]),
    "virtual-models.md": ("Virtual Models", ["virtual-models.md"]),
    "local-models.md": ("Local Models & llama.cpp", [
        "llama-cpp.md", "nvidia-rtx-llama-cpp.md",
    ]),
    "how-pi-works.md": ("How Pi Works", ["how-pi-works.md"]),
}


def locate_package(source):
    if source:
        root = Path(source).expanduser().resolve()
        if root.name == "docs":
            root = root.parent
        return root
    executable = shutil.which("pi")
    if executable:
        for root in Path(executable).resolve().parents:
            manifest = root / "package.json"
            if manifest.is_file():
                try:
                    if json.loads(manifest.read_text(encoding="utf-8")).get("name") == PACKAGE:
                        return root
                except (OSError, ValueError):
                    continue
    raise ValueError("Cannot locate Pi; pass its installed package root explicitly.")


def rewrite_links(content, base):
    """Resolve relative inline/reference links against their versioned source page.

    Leave code fences and inline code untouched so example strings stay literal.
    """
    inline = re.compile(r"(!?\[[^\]\n]*\]\()([^\s)]+)([^)\n]*\))")
    reference = re.compile(r"^(\s{0,3}\[[^\]\n]+\]:\s*)(\S+)(.*)$", re.MULTILINE)

    def target(value):
        if value.startswith(("#", "http:", "https:", "mailto:", "data:", "/")):
            return value
        if value.startswith("<") and value.endswith(">"):
            return "<" + urljoin(base, value[1:-1]) + ">"
        return urljoin(base, value)

    lines = []
    fence = None
    for line in content.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            lines.append(line)
            if (marker and marker[1][0] == fence[0]
                    and len(marker[1]) >= len(fence) and not marker[2].strip()):
                fence = None
            continue
        if marker:
            fence = marker[1]
            lines.append(line)
            continue
        spans = re.split(r"(`+[^`\n]*`+)", line)
        for j in range(0, len(spans), 2):
            spans[j] = inline.sub(lambda m: m[1] + target(m[2]) + m[3], spans[j])
            spans[j] = reference.sub(lambda m: m[1] + target(m[2]) + m[3], spans[j])
        lines.append("".join(spans))
    return "".join(lines)


def build(root):
    manifest = json.loads((root / "package.json").read_text(encoding="utf-8"))
    if manifest.get("name") != PACKAGE:
        raise ValueError(f"Expected {PACKAGE}, got {manifest.get('name')!r}")
    version = manifest["version"]
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.+-]+)?", version):
        raise ValueError(f"Invalid package version: {version!r}")
    refreshed = date.today().isoformat()
    base = f"https://github.com/earendil-works/pi/blob/v{version}/packages/coding-agent/"
    pages = {name for _, names in BUNDLES.values() for name in names}
    required = [root / "docs" / name for name in sorted(pages)]
    required += [root / "README.md", root / "CHANGELOG.md"]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise ValueError("Missing required source files:\n" + "\n".join(missing))
    inputs = {path: path.read_text(encoding="utf-8") for path in required}

    def header(title):
        return (f"# Pi — {title}\n\n"
                f"> Official {PACKAGE} {version} documentation.\n"
                f"> Refreshed from the installed package on {refreshed}; not a live `latest` mirror.\n\n")

    def page(path, relative):
        url = base + relative
        return f"Source: <{url}>\n\n" + rewrite_links(inputs[path], url).strip() + "\n"

    outputs = {}
    for name, (title, sources) in BUNDLES.items():
        outputs[name] = header(title) + "\n---\n\n".join(
            page(root / "docs" / src, "docs/" + src) for src in sources
        )
    outputs["development.md"] = header("Overview & Development") + page(root / "README.md", "README.md")
    # Keep a bounded release history from the same installed version.
    changelog = inputs[root / "CHANGELOG.md"]
    releases = list(re.finditer(r"^## \[", changelog, re.MULTILINE))
    if not releases or not changelog[releases[0].start():].startswith(f"## [{version}]"):
        raise ValueError("Installed changelog does not start with the package version")
    end = releases[12].start() if len(releases) > 12 else len(changelog)
    outputs["changelog.md"] = (header("Changelog")
        + f"Source: <{base}CHANGELOG.md>\n\n"
        + "Recent releases from the installed package; newer releases have not been checked.\n\n"
        + rewrite_links(changelog[releases[0].start():end].strip(), base + "CHANGELOG.md") + "\n")
    # Normalize whitespace-only lines while preserving Markdown hard line breaks.
    outputs = {name: re.sub(r"(?m)^[ \t]+$", "", content) for name, content in outputs.items()}
    # Gallery files have their own refresh date and are left untouched.
    return outputs, version, pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?")
    parser.add_argument("output", nargs="?", type=Path, default=SKILL_ROOT / "references")
    args = parser.parse_args()
    try:
        root = locate_package(args.source)
        outputs, version, pages = build(root)
        args.output.mkdir(parents=True, exist_ok=True)
        for name, content in outputs.items():
            (args.output / name).write_text(content, encoding="utf-8")
        print(f"Built {len(outputs)} references from Pi {version} ({len(pages)} official doc pages).")
        extra = sorted(path.name for path in (root / "docs").glob("*.md") if path.name not in pages)
        if extra:
            print("Additional source pages to review: " + ", ".join(extra))
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Refresh failed: {error}\n")


if __name__ == "__main__":
    main()
