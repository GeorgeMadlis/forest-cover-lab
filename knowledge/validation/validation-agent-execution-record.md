---
id: validation:agent-execution-record
type: validation
title: Agent execution record validation
version: '1.0'
status: candidate
updated: '2026-10-22'
review_after: '2027-01-22'
sources:
- validate/agent_harness_evaluation.md
- agent_harness/schemas/round.schema.json
- research/publications/agent_harness_review_2026.md
- agent_harness/scripts/validate_round.py
relations: []
---

# Agent execution record validation

Require versioned round structure, repository pins, observed instruction loads, file/output hashes and explicit limitations. Version 1.1 additionally records delegation contracts, runtime context, handoffs, independence disclosures and coordination events. Unknown details remain unknown. The validator cannot prove actual execution, digest authenticity, human identity or scientific validity.
