---
id: workflow:sentinel-monthly-forest-cover
type: workflow
title: sentinel-monthly-forest-cover
version: '1.0'
status: candidate
updated: '2026-10-06'
review_after: '2027-04-06'
sources: &id001
- docs/downstream_repos.md
relations:
- type: IMPLEMENTS
  target: method:ndvi-anomaly
  status: candidate
  sources: *id001
  scope: Intended partial implementation; confirm against pinned downstream code.
- type: IMPLEMENTS
  target: method:s1-backscatter-confirmation
  status: candidate
  sources: *id001
  scope: Intended partial implementation; confirm against pinned downstream code.
- type: IMPLEMENTS
  target: method:monthly-compositing
  status: candidate
  sources: *id001
  scope: Intended partial implementation; confirm against pinned downstream code.
- type: IMPLEMENTS
  target: method:temporal-persistence
  status: candidate
  sources: *id001
  scope: Intended partial implementation; confirm against pinned downstream code.
- type: CONSUMES
  target: DS-0002
  status: candidate
  sources: *id001
- type: CONSUMES
  target: DS-0003
  status: candidate
  sources: *id001
- type: REQUIRES_OBSERVATION
  target: observation:forest-baseline
  status: candidate
  sources: *id001
- type: REQUIRES_OBSERVATION
  target: observation:optical-vegetation-state
  status: candidate
  sources: *id001
- type: REQUIRES_OBSERVATION
  target: observation:sar-backscatter-state
  status: candidate
  sources: *id001
- type: REQUIRES_OBSERVATION
  target: observation:temporal-persistence
  status: candidate
  sources: *id001
- type: REQUIRES_OBSERVATION
  target: observation:forest-cover-change
  status: candidate
  sources: *id001
- type: REQUIRES_OBSERVATION
  target: observation:disturbance-confirmation
  status: candidate
  sources: *id001
- type: USES_TOOL
  target: tool:stac-client
  status: candidate
  sources: *id001
- type: USES_TOOL
  target: tool:rasterio
  status: candidate
  sources: *id001
- type: USES_TOOL
  target: tool:xarray
  status: candidate
  sources: *id001
- type: REQUIRES_VALIDATION
  target: validation:forest-evidence
  status: candidate
  sources: *id001
---

# sentinel-monthly-forest-cover

Proposed downstream contract example. IMPLEMENTS edges describe intended partial implementation, not an audited scientific equivalence claim. The implementation must pin its own version, declare divergences and demonstrate validation.
