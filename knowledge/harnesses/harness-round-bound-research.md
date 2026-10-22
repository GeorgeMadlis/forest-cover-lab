---
id: harness:round-bound-research
type: harness
title: Round-bound forest-cover research harness
version: '1.0'
status: candidate
updated: '2026-10-22'
review_after: '2027-01-22'
sources:
- docs/agents.md
- docs/adr/0006-round-agent-harness.md
- research/publications/agent_harness_review_2026.md
- agent_harness/schemas/round.schema.json
- validate/agent_harness_evaluation.md
- docs/adr/0008-agent-governance-graph.md
- agent_harness/README.md
- agent_harness/templates/round.yaml
- agent_harness/templates/assignment.md
relations:
- type: SUPPORTS_ROLE
  target: role:dataset-and-tool-discovery
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Optional standing responsibility; does not mandate invocation or assert execution.
- type: SUPPORTS_ROLE
  target: role:discrepancy-analysis
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Optional standing responsibility; does not mandate invocation or assert execution.
- type: SUPPORTS_ROLE
  target: role:independent-challenge
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Optional standing responsibility; does not mandate invocation or assert execution.
- type: SUPPORTS_ROLE
  target: role:literature-and-media
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Optional standing responsibility; does not mandate invocation or assert execution.
- type: SUPPORTS_ROLE
  target: role:national-geospatial-evidence
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Optional standing responsibility; does not mandate invocation or assert execution.
- type: SUPPORTS_ROLE
  target: role:official-infrastructure-records
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Optional standing responsibility; does not mandate invocation or assert execution.
- type: SUPPORTS_ROLE
  target: role:publication-method-reconstruction
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Optional standing responsibility; does not mandate invocation or assert execution.
- type: SUPPORTS_ROLE
  target: role:remote-sensing-quantification
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Optional standing responsibility; does not mandate invocation or assert execution.
- type: CAN_USE_SKILL
  target: skill:inspect-sentinel-change
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Candidate instructional resource; actual use must be evidenced by a round.
- type: CAN_USE_SKILL
  target: skill:research-sentinel-change
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Candidate instructional resource; actual use must be evidenced by a round.
- type: CAN_USE_SKILL
  target: skill:corroborate-sentinel-change
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Candidate instructional resource; actual use must be evidenced by a round.
- type: CAN_USE_SKILL
  target: skill:report-sentinel-change
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Candidate instructional resource; actual use must be evidenced by a round.
- type: CAN_RUN_ON
  target: tool:codex
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Proposed host compatibility; no automatic orchestration or adapter execution
    demonstrated.
- type: CAN_RUN_ON
  target: tool:claude-code
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Proposed host compatibility; no automatic orchestration or adapter execution
    demonstrated.
- type: REQUIRES_VALIDATION
  target: validation:agent-execution-record
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Proposed governance/evaluation requirement; neither completed checks nor
    scientific validity asserted.
- type: REQUIRES_VALIDATION
  target: validation:agent-harness-behavior
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Proposed governance/evaluation requirement; neither completed checks nor
    scientific validity asserted.
- type: BOUNDED_BY
  target: claim:agent-output-is-candidate
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Explicit non-claim; human review remains required.
- type: BOUNDED_BY
  target: claim:agent-agreement-is-not-independent-evidence
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Explicit non-claim; human review remains required.
parameters:
  contract_status: proposed ADR 0006; human review pending
  round_schema: agent_harness/schemas/round.schema.json
  schema_versions:
  - '1.0'
  - '1.1'
  execution_records: downstream reviews; Lab research inquiries
  default_orchestration: optional; no automatic delegation
---

# Round-bound forest-cover research harness

Reusable research-governance contract under proposed ADR 0006. Select bounded roles and skills, freeze instructions, record actual execution, reconcile disagreements and request human review. This is distinct from a GeoFM processing harness. It installs no scheduler, delegation engine, model service or scientific validation. Operational rounds and results remain downstream.
