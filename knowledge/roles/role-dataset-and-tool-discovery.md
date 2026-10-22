---
id: role:dataset-and-tool-discovery
type: role
title: Dataset and tool discovery
version: '1.0'
status: candidate
updated: '2026-10-22'
review_after: '2027-01-22'
sources:
- agent_harness/roles/dataset-and-tool-discovery.md
- docs/agents.md
- docs/adr/0006-round-agent-harness.md
- research/publications/agent_harness_review_2026.md
relations:
- type: BOUNDED_BY
  target: claim:agent-output-is-candidate
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Responsibility grants no knowledge-promotion authority.
parameters:
  contract_status: proposed; human review pending
  role_contract: agent_harness/roles/dataset-and-tool-discovery.md
  execution_evidence: round records only
---

# Dataset and tool discovery

Discover, verify and explain datasets and their associated discovery, access and processing tools for forest-cover estimation, forest disturbance screening and land-surface classification (e.g. roads, agricultural fields, buildings, water, settlements). Provide cited, conditional advice to other agents and people planning processing pipelines. This is a **portable logical subagent role**, not a continuously running crawler, production pipeline or scientific authority.

This portable responsibility may be performed sequentially, in a separate session or by a native subagent. It is not an agent instance, permission boundary or evidence of execution. The cited role file defines inputs, outputs and stop conditions.
