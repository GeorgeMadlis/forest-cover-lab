---
id: role:evidence-synthesis
type: role
title: Evidence synthesis
version: '1.0'
status: candidate
updated: '2026-10-25'
review_after: '2027-01-25'
sources:
- agent_harness/roles/evidence-synthesis.md
- docs/agents.md
- docs/adr/0006-round-agent-harness.md
relations:
- type: BOUNDED_BY
  target: claim:agent-output-is-candidate
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  scope: Responsibility grants no knowledge-promotion authority.
- type: BOUNDED_BY
  target: claim:agent-agreement-is-not-independent-evidence
  status: candidate
  sources:
  - agent_harness/roles/evidence-synthesis.md
  - docs/agents.md
  scope: Summarising agreeing outputs does not make them independent corroboration.
parameters:
  contract_status: proposed; human review pending
  role_contract: agent_harness/roles/evidence-synthesis.md
  execution_evidence: round records only
---

# Evidence synthesis

Scan, analyse and summarise the recorded outputs of other round instances, retask them with bounded addenda when evidence is missing, and write one source-cited report for human review.

This portable responsibility may be performed sequentially, in a separate session or by a native subagent. It is not an agent instance, permission boundary or evidence of execution. It reads all branch outputs and is therefore not an independent challenge. The cited role file defines inputs, outputs and stop conditions.
