---
id: role:discrepancy-analysis
type: role
title: Discrepancy analysis
version: '1.0'
status: candidate
updated: '2026-10-22'
review_after: '2027-01-22'
sources:
- agent_harness/roles/discrepancy-analysis.md
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
  role_contract: agent_harness/roles/discrepancy-analysis.md
  execution_evidence: round records only
---

# Discrepancy analysis

Explain differences between calculated forest-removal area and published figures through a transparent decomposition instead of selecting one preferred number.

This portable responsibility may be performed sequentially, in a separate session or by a native subagent. It is not an agent instance, permission boundary or evidence of execution. The cited role file defines inputs, outputs and stop conditions.
