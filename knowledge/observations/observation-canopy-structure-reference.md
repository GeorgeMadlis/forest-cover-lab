---
id: observation:canopy-structure-reference
type: observation
title: Canopy structure reference
version: '1.0'
status: active
updated: '2026-10-06'
review_after: '2027-04-06'
sources: &id001
- research/data_sources/inventory.csv
relations:
- type: CAN_BE_OBSERVED_BY
  target: DS-0006
  status: validated
  sources: *id001
  review:
    by: repository-contract-transcription
    date: '2026-10-06'
    basis: Traceable transcription of the cited contract; no empirical validation
      implied.
- type: MEASURED_AS
  target: measurement:canopy-height
  status: validated
  sources: *id001
  review:
    by: repository-contract-transcription
    date: '2026-10-06'
    basis: Traceable transcription of the cited contract; no empirical validation
      implied.
---

# Canopy structure reference

Sparse validation reference; check footprint alignment and ISS latitude coverage. It cannot estimate continuous forest area alone.
