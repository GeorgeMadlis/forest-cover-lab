"""Keep docs/agents.md in sync with the agent configuration in this repository.

The registry must list every agent named in AGENTS.md, every agent definition file found
in the repository and every repository path that AGENTS.md references, and every path it
lists must exist. Fix failures by updating docs/agents.md in the same change.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "agents.md"
AGENTS = ROOT / "AGENTS.md"

# Locations where coding agents (Claude Code, Codex, Copilot, Cursor, Gemini, Windsurf…)
# pick up instructions, subagents, skills, tool permissions, MCP servers or hooks.
AGENT_FILE_PATTERNS = [
    "**/AGENTS.md",
    "**/CLAUDE.md",
    "**/CLAUDE.local.md",
    "**/GEMINI.md",
    "**/SKILL.md",
    ".claude/**/*",
    ".codex/**/*",
    ".mcp.json",
    ".github/copilot-instructions.md",
    ".github/instructions/**/*",
    ".github/agents/**/*",
    ".github/prompts/**/*",
    ".github/chatmodes/**/*",
    ".cursorrules",
    ".cursor/**/*",
    ".windsurfrules",
]
IGNORED_PARTS = {".git", ".pytest_cache", "node_modules", "outputs", "__pycache__"}
PATH_SUFFIXES = (".md", ".py", ".json", ".yaml", ".yml", ".csv", ".toml", ".svg")


def _defined_section() -> str:
    """Registry text describing what exists (excludes the 'Not defined' section)."""
    text = REGISTRY.read_text(encoding="utf-8")
    return text.split("## Not defined in this repository", 1)[0]


def _code_spans(text: str) -> set[str]:
    return set(re.findall(r"`([^`\n]+)`", text))


def _ignored(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return any(
        part in IGNORED_PARTS or part.endswith(".egg-info") for part in rel.parts
    )


def test_registry_lists_every_agent_named_in_agents_md():
    match = re.search(
        r"any coding or research agent\s+\(([^)]+)\)",
        AGENTS.read_text(encoding="utf-8"),
    )
    assert match, "AGENTS.md no longer names its agents"
    summary = _defined_section().split("## Files that define the agents", 1)[0]
    for name in (n.strip() for n in match.group(1).split(",")):
        assert f"| {name} |" in summary, f"agent {name!r} missing from summary table"


def test_registry_lists_every_agent_definition_file():
    listed = _code_spans(_defined_section())
    found = sorted(
        {
            path.relative_to(ROOT).as_posix()
            for pattern in AGENT_FILE_PATTERNS
            for path in ROOT.glob(pattern)
            if path.is_file() and not _ignored(path)
        }
    )
    missing = [path for path in found if path not in listed]
    assert not missing, f"agent definition files missing from docs/agents.md: {missing}"


def test_registry_lists_every_path_referenced_by_agents_md():
    listed = _code_spans(_defined_section())
    referenced = set()
    for span in _code_spans(AGENTS.read_text(encoding="utf-8")):
        for token in span.split():
            if "<" in token or "…" in token or token.startswith("-"):
                continue
            if (ROOT / token).exists() and token not in {".", "./"}:
                referenced.add(token)
    missing = sorted(referenced - listed)
    assert (
        not missing
    ), f"paths referenced by AGENTS.md missing from registry: {missing}"


def test_every_path_in_registry_exists():
    stale = []
    for span in _code_spans(_defined_section()):
        if " " in span or "*" in span or span.startswith(("~", "@", "-")):
            continue
        looks_like_path = "/" in span or span.endswith(PATH_SUFFIXES)
        if looks_like_path and not (ROOT / span).exists():
            stale.append(span)
    assert not stale, f"docs/agents.md lists paths that do not exist: {sorted(stale)}"
