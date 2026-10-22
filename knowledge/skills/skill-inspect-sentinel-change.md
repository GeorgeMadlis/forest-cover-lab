---
id: skill:inspect-sentinel-change
type: skill
title: Inspect sentinel change
version: '1.0'
status: candidate
updated: '2026-10-22'
review_after: '2027-01-22'
sources:
- https://github.com/GeorgeMadlis/sentinel-monthly-forest-cover/blob/bacbea70cf3badb1c137285f827b3570f84c0c22/.codex/skills/inspect-sentinel-change/SKILL.md
- docs/agents.md
relations:
- type: BOUNDED_BY
  target: claim:agent-output-is-candidate
  status: candidate
  sources:
  - docs/agents.md
  - docs/adr/0006-round-agent-harness.md
  - research/publications/agent_harness_review_2026.md
  scope: Skill execution cannot approve scientific knowledge.
parameters:
  source_repository: sentinel-monthly-forest-cover
  source_commit: bacbea70cf3badb1c137285f827b3570f84c0c22
  contract_status: candidate mapping; human review pending
---

# Inspect sentinel change

Task-specific Sentinel instructions and supporting resources. The commit-pinned source defines the scope; other hosts require the content to be supplied explicitly. Availability is not an observed load or proof of completed analysis. Instructions/configuration are not scientific observations.
