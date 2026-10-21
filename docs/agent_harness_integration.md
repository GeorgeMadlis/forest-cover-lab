# Agent harness integration review — 2026-10-21

This implements the attached forest-agent-harness proposal on a local feature branch.
The architecture and ADR 0006 remain proposed for operator review. No scientific
findings, downloads, real agent rounds or human approvals were invented.

## Changed-file inventory

- AGENTS.md and CLAUDE.md: new repository-wide rules and Claude Code import.
- README.md, docs/README.md, docs/architecture.md, tests/README.md: integration pointers
  and responsibility boundaries.
- docs/agents.md: reconciled standing policy and discoverable contract/role index.
- docs/adr/0006-round-agent-harness.md: proposed durable architecture decision.
- agent_harness/README.md: local/downstream usage, path rules and validator limits.
- agent_harness/roles/: seven unchanged proposed logical role contracts.
- agent_harness/templates/: assignment.md and round.yaml planning seeds.
- agent_harness/schemas/round.schema.json: new 1.0 record format, explicit role_scope
  and output_hashes extension.
- agent_harness/scripts/validate_round.py: shared read-only validator and local discovery.
- agent_harness/examples/forest-area-discrepancy/round-0001/: README.md, round.yaml,
  assignments/{pub-01,eo-01,official-01,bridge-01,critic-01}.md (planning only).
- agent_harness/examples/road-widening/round-0001/: README.md, round.yaml,
  assignments/{eo-01,geo-01,works-01,sources-01,critic-01}.md (planning only).
- tests/test_agent_registry.py and tests/test_agent_harness.py: standing discovery,
  schema, local round discovery and isolated synthetic provenance/path tests.
- .github/workflows/ci.yml: explicit local round CLI check.
- governance/audit_log.md and this report: actual review results and deviations.

## Reconciliation with the package

The assumed existing agent files/registry and glossary/overview generator did not exist.
Added the entrypoints and tests; indexed only actual contracts. No existing instructions
were overwritten and no named unused client needed removal. Defensive detection of other
client files remains tested, while per-round runtime files stay out of the stable registry.
Both illustrative examples, assignments and all seven role contracts retain their supplied
planning content. The package README and IMPLEMENTATION_PROMPT.md are integration inputs,
not replacement repository instructions; neither was copied over the project README.

The CLI adds local-root discovery, strict YAML and safer path semantics. Round-only roles
are explicit. Observed executions require both repository pins, graph SHA-256, mandatory
rule/role/assignment loads, terminal timestamps and meaningful completion checks. Completed
outputs also require output_hashes. Private external instructions may remain uncaptured,
with a limitation. A change to pinned repository instructions starts a new round rather
than mutating the baseline. Lab tests never traverse another checkout. Sentinel's explicit
adapter and pinned CI checkout validate its own reviews using these shared contracts.

## Validation and limits

See the appended governance audit for exact commands/results: 104 Lab tests pass, graph
and descriptor checks pass unchanged, both planning examples validate. Tests use isolated,
explicitly synthetic completed records; those are not real rounds or findings. Sentinel
records its own tests and the pre-existing graph-pin repair in its architecture audit.
Optional Black/Ruff formatters are unavailable in the existing environment.

The CLI checks declarations, not repository object existence, evidence digest authenticity,
actual host loads, scientific independence, human identity or append-only history. Hosted
reasoning/search replay remains limited. Human review is pending; no scheduler, model
inference, automatic orchestration, new scientific capability or knowledge promotion occurs.
There is no existing governed SVG overview to regenerate; docs/agents.md contains a small
Mermaid architecture diagram. Earlier research/scientific gaps remain unresolved.

Pre-existing pyproject.toml and untracked research/workspace edits are excluded from the
commit. No push, merge or modification of canonical scientific sources is authorized here.
