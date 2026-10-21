# Agent registry

This registry lists the AI coding and research agents set up to work in Forest Cover Lab,
their attributes, and every repository file that defines their instructions, rules and
checks. It describes configuration, not performance: no agent's output is scientific
validation (`governance/knowledge_promotion.md`).

**Keep it current.** Update this file in the same change whenever an agent is added,
removed or changes status, an agent definition file is added, renamed or removed, or
`AGENTS.md` starts or stops referencing a file. `tests/test_agent_registry.py` fails when
an agent definition file or a file referenced by `AGENTS.md` is missing from this
registry, or when a path listed here no longer exists.

## Summary

| Agent | Status | Entry point | How instructions load | Model, tools, MCP servers, subagents, skills, hooks |
|---|---|---|---|---|
| Claude Code | Active — changes recorded in `governance/audit_log.md` | `CLAUDE.md` | Claude Code reads `CLAUDE.md`, whose `@AGENTS.md` line imports the shared instructions | Not configured in this repo (see [Not defined](#not-defined-in-this-repository)); set by each user's client |
| Codex | Active — architecture and evidence reviews recorded in `governance/audit_log.md` | `AGENTS.md` | Codex reads `AGENTS.md` natively | Not configured in this repo (see [Not defined](#not-defined-in-this-repository)); set by each user's client |
| Copilot | Named in `AGENTS.md`; no recorded use | `AGENTS.md` | Copilot's coding agent supports `AGENTS.md`; other Copilot surfaces would need a separate instructions file, which this repo does not have | Not configured in this repo |
| Bounded planner / evidence assistant | Proposed, not implemented (`docs/architecture.md`, delivery stage D) | — | — | — |

All three active or named agents share the same instructions, so they differ only by
harness and model, not by repository rules.

## Files that define the agents

Every file below applies to Claude Code, Codex and Copilot alike, except `CLAUDE.md`,
which only Claude Code reads.

### Entry points

| File | Role |
|---|---|
| `AGENTS.md` | Shared agent instructions: mission, non-negotiable rules, checks, structural-change and README-sync procedures, conventions |
| `CLAUDE.md` | Claude Code entry point; contains only `@AGENTS.md` |

### Required reading named in `AGENTS.md`

| File | Role |
|---|---|
| `governance/principles.md` | The six canonical principles (P1–P6) and the mission boundary |
| `docs/architecture.md` | Current architecture assessment, including the proposed bounded agent |
| `docs/adr/` | Durable decisions; ADR 0005 supersedes ADR 0001's platform policy |

### Rule sources referenced by `AGENTS.md`

| File | Rule it carries |
|---|---|
| `configs/v1_defaults.yaml` | Forest-definition defaults (ADR 0002); thresholds are never hardcoded |
| `validate/run_manifest.schema.json` | Run manifest contract |
| `validate/semantic_provenance.md` | Semantic provenance block for downstream runs |
| `governance/knowledge_promotion.md` | Agent output enters as `status: candidate`; promotion needs human review |
| `research/methodology/search_scopes.csv` | Search scopes to declare before adding inventory entries (P1) |
| `governance/drift_checklist.md` | Checklist to run after structural changes |
| `governance/audit_log.md` | Append-only record of each checklist run |
| `docs/downstream_repos.md` | How downstream repos consume this repo's contracts |
| `specs/` | Phase specifications the overview roadmap must match |
| `knowledge/` | Contextual corpus; edits require regenerating the graph |
| `README.md` | Must reflect current scope (README-sync rule) |
| `GLOSSARY.md` | Must explain new abbreviations |
| `docs/img/build_overview_diagram.py` | Generates the README overview diagram |
| `docs/img/problems-and-approaches.svg` | Generated overview diagram; never hand-edited |
| `docs/agents.md` | This registry |

### Checks agents must run or keep passing

| File | Role |
|---|---|
| `graph/build.py` | Builds and checks the knowledge graph (`--check`, `--descriptor`) |
| `graph/` | Ontology, schemas and relation types the graph build enforces |
| `graph/generated/knowledge.json` | Derived graph; regenerate and commit when inputs change |
| `pyproject.toml` | Dev dependencies installed with `pip install -e '.[dev]'` |
| `tests/` | Contract tests run with `python -m pytest` |
| `tests/test_overview_diagram.py` | Fails when the README diagram is out of sync |
| `tests/test_agent_registry.py` | Fails when this registry is out of sync |
| `.github/workflows/ci.yml` | CI that runs the graph check and tests on every push and pull request |
| `.pre-commit-config.yaml` | Formatting, lint and notebook-output hooks |

## Not defined in this repository

None of the following exist here, so no agent has repository-specific subagents, skills,
tool permissions, MCP servers, hooks or model pins: `.claude/agents/`, `.claude/skills/`,
`.claude/settings.json`, `.mcp.json`, `.codex/`, `.github/copilot-instructions.md`,
`.github/instructions/`, `.github/agents/`, `.github/prompts/` and `SKILL.md` files.
`tests/test_agent_registry.py` scans for these locations, so adding one fails the tests
until it is listed above.

User-level configuration outside the repository (for example `~/.claude/` or
`~/.codex/config.toml`) is not covered here, and downstream repositories such as
`sentinel-monthly-forest-cover` keep their own agent instructions.
