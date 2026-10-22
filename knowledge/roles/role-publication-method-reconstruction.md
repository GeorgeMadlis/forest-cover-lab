---
id: role:publication-method-reconstruction
type: role
title: Publication method reconstruction
version: '1.0'
status: candidate
updated: '2026-10-22'
review_after: '2027-01-22'
sources:
- agent_harness/roles/publication-method-reconstruction.md
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
  role_contract: agent_harness/roles/publication-method-reconstruction.md
  execution_evidence: round records only
---

# Publication method reconstruction

Reconstruct exactly what a published area/statistical result measured, including its denominator and accounting rules, before judging it against a new calculation.

This portable responsibility may be performed sequentially, in a separate session or by a native subagent. It is not an agent instance, permission boundary or evidence of execution. The cited role file defines inputs, outputs and stop conditions.
