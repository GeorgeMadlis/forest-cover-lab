---
id: role:official-infrastructure-records
type: role
title: Official infrastructure records
version: '1.0'
status: candidate
updated: '2026-10-22'
review_after: '2027-01-22'
sources:
- agent_harness/roles/official-infrastructure-records.md
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
- type: CAN_USE_SKILL
  target: skill:corroborate-sentinel-change
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Proposed supporting skill; selection and actual loading are recorded per
    execution, with source scope checked.
parameters:
  contract_status: proposed; human review pending
  role_contract: agent_harness/roles/official-infrastructure-records.md
  execution_evidence: round records only
---

# Official infrastructure records

Test whether a spatial change is explained by planned, permitted, constructed or modified infrastructure, without equating these stages.

This portable responsibility may be performed sequentially, in a separate session or by a native subagent. It is not an agent instance, permission boundary or evidence of execution. The cited role file defines inputs, outputs and stop conditions.
