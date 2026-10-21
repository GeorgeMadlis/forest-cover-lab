# ADR 0006: Standing roles and per-round execution records

- **Status:** Proposed — operator review pending
- **Date:** 2026-10-21
- **Deciders:** Pending maintainer review
- **Technical area:** architecture / provenance
- **Supersedes:** None

## Context

Research assistants need bounded responsibilities and evidence of what actually ran.
The existing architecture recommends deterministic workflows with an optional bounded
planner. A client name, generated role or passing schema is no scientific authority.
These local checkouts had no standing agent entrypoints or registry tests; the supplied
overlay assumed they existed. This proposal adds them without changing accepted ADRs.

## Decision proposed

Keep repository rules in AGENTS.md (imported by CLAUDE.md), stable host/role policy in
docs/agents.md, reusable logical roles and format contracts in agent_harness/, and
task-specific assignments/execution attempts in each round. ChatGPT, Claude, Claude Code
and Codex identify hosts; role responsibilities are portable across hosts. Tool skills,
runtime configuration, scientific source data and execution traces are separate layers.

Lab owns role/schema definitions and research inquiry records. Sentinel owns operational
review rounds, rasters and ledgers. Use the Lab validator explicitly against a chosen
repository root; never assume a Lab test can traverse another checkout. A round manifest
supplements run manifests, investigation and semantic ledgers, preserving their authority.
Generated round-only roles must declare their scope and cannot bypass repository rules.
Actual executions require both commit pins, graph revision, mandatory loaded contracts,
file digests, output checksums, checks and limitations. Private external instructions may
be explicitly uncaptured. Planning examples claim no execution or findings.

## Rationale and alternatives

A single expanding standing registry would require policy edits for every task. Entirely
vendor-specific agents would mix responsibilities with tool permissions. Copying Lab
contracts downstream would fork authority. Portable role contracts plus explicit per-round
records avoid these costs while leaving real orchestration optional.

## Consequences and limits

The validator checks structure, bounded local paths and provenance declarations. It cannot
prove model independence, actual loads, digest authenticity, scientific validity or human
identity, nor enforce append-only history alone. Review pinned files, ledgers and Git diffs.
No new scheduler, delegation facility, credentials, data downloads or model inference is
implemented. Existing reviews retain their history without invented round records.

## Acceptance criteria

- Standing client and role contracts are indexed; round records inventory runtime files.
- Planned examples remain unexecuted; isolated synthetic test records cover completion
  and reject missing hashes/pins, omitted mandatory loads and unsafe paths.
- Lab checks its own examples/inquiries. Sentinel checks its review rounds with an explicit
  pinned Lab checkout in CI. Both existing test suites and descriptor checks pass.
- Scientific sources, graph meanings, forest/area policy and promotion gates are preserved.
- Structural audits record actual results and pending human review; no merge or promotion.

## References

- [Standing policy](../agents.md)
- [Existing architecture](../architecture.md)
- [Backend and semantic authority](0005-semantic-architecture-and-backends.md)
- [Promotion governance](../../governance/knowledge_promotion.md)
