---
id: application:annual-forest-loss-screening
type: application
title: Annual forest-loss screening
version: '1.0'
status: candidate
updated: '2026-10-06'
review_after: '2027-04-06'
sources: &id001
- specs/v1_forest_baseline.md
relations:
- type: ASKS
  target: question:annual-forest-loss-screening
  status: candidate
  sources: *id001
- type: REQUIRES_OBSERVATION
  target: observation:forest-baseline
  status: candidate
  sources: *id001
- type: REQUIRES_OBSERVATION
  target: observation:forest-cover-change
  status: candidate
  sources: *id001
- type: BOUNDED_BY
  target: claim:monthly-non-truth
  status: candidate
  sources: *id001
---

# Annual forest-loss screening

Discovery intent: Where does annual baseline canopy loss warrant review? Outputs remain screening or monitoring evidence under explicit validation, uncertainty and forest definitions.
