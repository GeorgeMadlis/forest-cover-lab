"""Index standing definitions, including unused client formats; rounds self-inventory."""
from __future__ import annotations

import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOC = (ROOT / 'docs/agents.md').read_text()
STANDING = [
    'AGENTS.md', 'CLAUDE.md', 'docs/agents.md', 'agent_harness/README.md',
    'agent_harness/schemas/round.schema.json', 'agent_harness/templates/assignment.md',
    'agent_harness/templates/round.yaml', 'agent_harness/scripts/validate_round.py',
]


def standing_files(root):
    for directory, subdirs, files in os.walk(root):
        rel = Path(directory).relative_to(root)
        subdirs[:] = [d for d in subdirs if d not in {'.git', '.venv', '__pycache__', '.pytest_cache', 'node_modules', 'outputs', 'runs', 'reviews'}]
        if rel.as_posix() in {'research/inquiries', 'agent_harness/examples'}:
            subdirs[:] = []
            continue
        for filename in files:
            path = rel / filename
            if (filename in {'AGENTS.md', 'CLAUDE.md', 'GEMINI.md', '.cursorrules', '.windsurfrules'}
                or filename.endswith(('.instructions.md', '.agent.md'))
                or path.as_posix() == '.github/copilot-instructions.md'
                or any(part in {'.codex', '.claude', '.cursor'} for part in path.parts)
                or path.parts[:2] == ('.github', 'agents')):
                yield path.as_posix()


def test_standing_contracts_exist_and_are_discoverable():
    for name in STANDING:
        assert (ROOT / name).is_file(), name
        assert f'`{name}`' in DOC, name


def test_all_role_contracts_are_listed():
    roles = list((ROOT / 'agent_harness/roles').glob('*.md'))
    assert roles
    for role in roles:
        assert f'`{role.relative_to(ROOT).as_posix()}`' in DOC


def test_host_inventory_and_no_copilot():
    for host in ('ChatGPT', 'Claude', 'Claude Code', 'Codex'):
        assert re.search(rf'^\| {re.escape(host)} \|', DOC, re.M)
    for path in ('docs/agents.md', 'AGENTS.md', 'CLAUDE.md', 'README.md'):
        assert not re.search(r'\bCopilot\b', (ROOT / path).read_text(), re.I)


def test_existing_agent_instruction_files_are_indexed():
    for name in standing_files(ROOT):
        assert f'`{name}`' in DOC, f'unregistered standing definition: {name}'


def test_existing_rule_dependencies_still_registered():
    for span in set(re.findall(r'`([^`\n]+)`', (ROOT / 'AGENTS.md').read_text())):
        for token in span.split():
            if (ROOT / token).exists() and token not in {'.', './'}:
                assert f'`{token}`' in DOC, token


def test_defensive_discovery_keeps_unused_clients_and_excludes_rounds(tmp_path):
    standing = ['.github/copilot-instructions.md', '.github/instructions/python.instructions.md', '.codex/skills/tool/agents/openai.yaml', '.claude/agents/new.md', '.cursor/rules/project.mdc', 'nested/AGENTS.md']
    runtime = ['research/inquiries/q/rounds/r/AGENTS.md', 'reviews/i/rounds/r/.claude/agents/task.md', 'agent_harness/examples/task/round-1/CLAUDE.md']
    for name in standing + runtime:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    assert set(standing_files(tmp_path)) == set(standing)
