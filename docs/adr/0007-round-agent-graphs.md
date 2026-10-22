# ADR 0007: Explicit agent graphs for rounds

- **Status:** Proposed — operator review pending
- **Date:** 2026-10-22
- **Deciders:** Pending maintainer review
- **Technical area:** architecture / provenance
- **Supersedes:** None
- **Superseded by:** None

## Context

ADR 0006 (Proposed) defines portable role contracts and a per-round record
(`round.yaml`) of which instances were selected and what actually ran. It deliberately
implements no scheduler. The order in which instances run, what each one hands to the
next, where a human must approve, and how often an agent may retry are currently
described only in prose (`docs/agents.md` §5) and in identical free-text "Handoff" lines
in assignments. A reader therefore cannot see, before execution, which agents exist and
what flows between them, nor check afterwards that execution followed an approved plan.

The operator requires, for each question specified in enough detail (AOI, time window,
measurement), an explicit plan that names the agents, shows the graph as an image, states
whether the chain runs automatically or step by step, and requires approval before each
step runs in step-by-step mode. This follows the progression prompt → agent → loop →
graph: an assignment is the prompt, an instance is the agent, a bounded retry policy is
the loop, and the graph decides which agents exist and what each passes to the next.

Scope boundaries: this ADR is about the round record format and its checks. It does not
change scientific contracts, roles, the knowledge graph or promotion rules, and it does
not add execution machinery.

## Decision

Add an **optional** `graph` block to the round manifest (`agent_harness/schemas/round.schema.json`,
schema version unchanged; rounds without it remain valid):

- `mode`: `stepwise` (every agent node needs an approved step plan before it runs) or
  `auto` (agent nodes run without per-step approval; declared gates still stop the chain).
- `approval`: the graph itself is a plan. It is proposed (by a human or an AI planner) and
  must be approved by a named human, with time and basis, before any instance has an
  execution attempt. Its `planning_record_id` is the value a run manifest cites in
  `semantic_provenance.planning_record_id`.
- `nodes` of four kinds:
  - `input` — declared starting artifacts (frame, AOI, windows);
  - `agent` — exactly one round instance; optional `loop.max_iterations` bounds its
    attempts (default 1) and `loop.until` states the stop condition;
  - `script` — a deterministic command (recorded, not executed by Lab tooling);
  - `gate` — a human decision point with its own approval record.
  Every non-gate node declares its `outputs`.
- `edges` with `carries`: the named outputs passed from source to target. A gate passes on
  only what it received. Optional `lineage` tags shared sources.
- `independence_groups`: nodes that must not exchange information. No path may connect
  two members of the same group.

Validation (`agent_harness/scripts/validate_round.py`), applied when `graph` is present:
unique node IDs; agent nodes reference existing instances; every used instance appears in
the graph (no hidden agents); no cycles (iteration is a node loop, not a cycle); edges
reference existing nodes, are not duplicated and carry only outputs available at their
source; non-gate edges carry at least one item; independence groups are path-free; the
graph is connected and every sink is a gate; attempts never exceed the node's loop bound.
For recorded attempts: the graph approval, every upstream gate and, in `stepwise` mode,
the node's step plan (with SHA-256) must be approved.

Rendering (`agent_harness/scripts/render_round_graph.py`) writes a deterministic,
dependency-free SVG and a Mermaid file next to the manifest, shows node kind, host,
loop bound, status and carried artifacts, marks hosts that require manual hand-off
(`chatgpt`, `claude`), and refuses to draw a manifest that fails validation.
`--check` detects stale images.

Excluded: no runner, scheduler, host adapter, model call, credential or download. A
separate decision will cover execution and script-node execution records.

## Rationale

The graph is written down before anything runs, can be read as an image, and is checked
mechanically; execution records can then be compared with what was approved. Keeping the
block optional preserves existing rounds and ADR 0006. A dependency-free renderer keeps
output identical across machines and avoids requiring Graphviz or Node.js.

## Alternatives considered

### Adopt an orchestration framework now (e.g. LangGraph)
Provides checkpoints and human interrupts but places the graph inside framework code,
targets API-key model calls, and would make execution machinery a precondition for
drawing and checking plans. Not chosen; a later runner can still export to one.

### Encode order in assignment prose only
The current state. Not machine-checkable and invisible as a whole.

### Amend ADR 0006
ADR 0006 explicitly excludes scheduling and may be accepted on its own; a separate
record keeps each decision reviewable.

## Consequences

### Positive
- Each round can show, before execution, which agents exist and what each passes on.
- Approval, loop bounds and independence become checkable record properties.

### Negative
- Manifests become longer; graph and instances must be kept consistent (the validator
  enforces this).

### Neutral / follow-up
- An execution runner (stepwise/auto, host adapters, manual hand-off for chat hosts) needs
  its own ADR and PR.

## Acceptance criteria

- Rounds without `graph` validate unchanged; existing tests pass.
- The road-widening planning example carries a graph and a committed, up-to-date image;
  no execution or approval is claimed.
- Tests reject cycles, hidden instances, undeclared payloads, connected independence
  members, non-gate sinks, exceeded loop bounds and executions without approval.
- Drift checklist run and audit log entry appended.

## Risks and limitations

- The validator checks record structure and declared approvals. It cannot prove that a
  human actually approved, that a step plan was read, or that hosts honoured the graph.
- Independence is declared information flow inside the round; it does not prove that
  agents used independent data or models.
- Approvals in the record are not knowledge promotion; `governance/knowledge_promotion.md`
  still governs.

## References

- Internal: `docs/agents.md`, `agent_harness/README.md`, `validate/semantic_provenance.md`
- Related ADRs: `docs/adr/0006-round-agent-harness.md`, `docs/adr/0005-semantic-architecture-and-backends.md`
