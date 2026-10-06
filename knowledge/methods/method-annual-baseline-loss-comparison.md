---
id: method:annual-baseline-loss-comparison
type: method
title: Annual baseline/loss comparison
version: '1.0'
status: candidate
updated: '2026-10-06'
review_after: '2027-04-06'
sources: &id001
- specs/v1_forest_baseline.md
relations:
- type: REQUIRES_OBSERVATION
  target: observation:forest-baseline
  status: candidate
  sources: *id001
- type: REQUIRES_OBSERVATION
  target: observation:forest-cover-change
  status: candidate
  sources: *id001
- type: REQUIRES_VALIDATION
  target: validation:forest-evidence
  status: candidate
  sources: *id001
- type: BOUNDED_BY
  target: claim:monthly-non-truth
  status: candidate
  sources: *id001
parameters:
  decision_rule: configured; validate for target context
---

# Annual baseline/loss comparison

Apply declared canopy threshold, datamask and MMU to year-2000 baseline; annual lossyear can screen baseline loss, not regrowth or monthly timing. The loss comparison is a candidate extension of the baseline spec.
