# ADR 0008: Discoverable research-governance contracts

- **Status:** Proposed — human/operator review pending
- **Date:** 2026-10-22
- **Deciders:** Pending maintainer review
- **Technical area:** semantic discovery / research governance
- **Supersedes:** None

## Context

ADR 0006 proposes portable responsibilities and per-round execution records. Those
contracts were outside the graph's vocabulary. Discovery should expose them while
preserving the distinction between scientific methods, instructional resources and
actual agent activity. Primary-source assessment: SS-0003 / PUB-0013–PUB-0018 in
[the harness review](../../research/publications/agent_harness_review_2026.md).

## Decision proposed

Add `role`, `harness` and `skill` as reusable contract types. Existing `tool` and
`capability` types describe scoped host software and delegation facilities; existing
`validation` and `claim` types describe governance checks and interpretation limits.
These supporting records do not become EO methods, observations or measurements.

Typed relationships: workflow `HAS_HARNESS_CONTRACT` harness; harness `SUPPORTS_ROLE`
role; harness/role `CAN_USE_SKILL` skill; harness `CAN_RUN_ON` tool. Extend
`REQUIRES_VALIDATION` to harness and `BOUNDED_BY` to harness/role/skill. The first
records and all new relationships are candidates pending reviewed promotion. Existing
scientific relationships retain their status and content.

Relations express declared compatibility or requirements, never executed delegation,
loaded instructions, proven isolation or independent scientific confirmation. Per-run
agent instances, contexts, events and results remain excluded entities. Static graph
edges must not be created from observed messages or agent agreement.

Round schema 1.1 adds delegation contracts and runtime/handoff/independence/event
capture while continuing to accept 1.0 records. Old rounds are neither rewritten nor
retrospectively assigned runtime details. New templates use 1.1. Unknown observations
remain explicitly unknown, with limitations. Configuration is not enforcement.

## Consequences

The viewer gains a Research governance layer, distinct shapes, contract metadata and
a direct Agent contracts entry. Its candidate partition remains intact. Canonical
graph revisions change; downstream consumers need the resulting full Lab commit and
graph revision before adopting the new snapshot. A local dirty export declares its
actual HEAD and dirty state and does not masquerade as a committed snapshot.

No scheduler, host adapter, delegated execution, behavioral experiment or scientific
promotion is introduced. Deterministic checks cannot prove execution, authentic
digests, human identity or scientific truth. Proposed behavioral evaluation remains
separate from structural validation and forest-map accuracy assessment.

## Alternatives

Keeping contracts only in documentation preserves the discovery gap. Encoding roles
as scientific methods confuses authority. Recording agent instances in this graph
violates the existing run/result boundary. A separate graph would duplicate source
and candidate-review machinery without a demonstrated need.

## Validation and review

Require typed endpoint and candidate-partition tests, schema backward compatibility,
parent-reference/cycle checks, explicit unknown-runtime limitations, artifact digests,
fresh graph/example snapshots and offline viewer integrity. Run both repositories'
round validators, the Lab suite, overview freshness and drift checklist. Human review
and future behavioral trials remain pending regardless of structural test success.
