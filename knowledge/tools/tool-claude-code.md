---
id: tool:claude-code
type: tool
title: Claude Code
version: '1.0'
status: candidate
updated: '2026-10-22'
review_after: '2027-01-22'
sources:
- https://code.claude.com/docs/en/sub-agents
- research/publications/agent_harness_review_2026.md
relations:
- type: CAN
  target: capability:subagent-delegation
  status: candidate
  sources:
  - https://code.claude.com/docs/en/sub-agents
  scope: Documented delegation facility; availability and semantics vary by client/version
    and effective permissions.
---

# Claude Code

Host/client software for bounded tool use and delegated assistance. Candidate capability transcription from official documentation, not evidence of installation, access, execution or an implemented Lab adapter. Record actual client version, context, permissions and model configuration in the round.
