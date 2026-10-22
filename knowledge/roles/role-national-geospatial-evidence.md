---
id: role:national-geospatial-evidence
type: role
title: National geospatial evidence
version: '1.0'
status: candidate
updated: '2026-10-22'
review_after: '2027-01-22'
sources:
- agent_harness/roles/national-geospatial-evidence.md
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
  role_contract: agent_harness/roles/national-geospatial-evidence.md
  execution_evidence: round records only
---

# National geospatial evidence

Find and evaluate national geospatial databases for site-specific corroboration, with first-class attention to historical state and provenance.

This portable responsibility may be performed sequentially, in a separate session or by a native subagent. It is not an agent instance, permission boundary or evidence of execution. The cited role file defines inputs, outputs and stop conditions.
