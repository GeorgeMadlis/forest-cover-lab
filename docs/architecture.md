# Architecture Assessment

This document records the current architecture view for Forest Cover Lab. It is not a
decision record; durable choices still belong in `docs/adr/`.

## Architecture intent

Forest Cover Lab is a research-and-implementation repository for forest cover estimation
from satellite data. The architecture must support two parallel jobs:

1. Produce reproducible forest-cover estimates with explicit assumptions.
2. Build an auditable research base that explains why datasets, methods, codebases, and
   scientific claims were accepted, rejected, or deferred.

Adjacent Earth-observation domains are intentionally in scope as context. Biodiversity,
ocean/coastal, renewable energy, environmental integrity, flood, fire, climate, and land-use
products can inform interpretation, validation, or risk assessment. They must not become a
second mission that distracts from forest cover estimation.

## Current strengths

- The repo already separates research evidence, specifications, validation, reporting, and
  ADRs. That is the right high-level separation for a scientific geospatial project.
- The v1/v2/v3 roadmap is useful because it distinguishes a baseline estimate, monthly
  confirmation, and weakly supervised monthly estimation.
- The governance scaffold makes drift visible through principles, a checklist, and an audit
  log instead of leaving architecture rules implicit.
- The code-discovery and reverse-engineering tracks correctly treat external source code as
  scientific evidence, not only as reusable software.

## Main gaps found

- The data-source architecture was too forest-product focused. It did not clearly model
  adjacent context products such as biodiversity, floods, integrity indices, oceans, or
  renewable energy surfaces.
- P1 required a search scope, but there was no concrete artifact where search scopes could
  be recorded once and referenced by inventories.
- The boundary between "core forest estimation input" and "background context" was not
  explicit enough, creating a risk that broad Earth-observation research could dilute the
  forest-cover mission.
- Track independence was stated, but downstream influence was not always explicit: a reader
  could not immediately see whether a track feeds ADRs, specs, reports, validation, or only
  notes.
- There was no single architecture assessment document tying the six principles to the
  repository layout.

## Target architecture

| Section | Governing principle | Main location | Purpose |
|---|---|---|---|
| Research protocol | P1 | `research/methodology/` | Search scopes, reading protocol, practitioner sources |
| Publications and practitioner knowledge | P1 | `research/publications/` | Papers, reports, blogs, method synthesis |
| Data and context products | P2 | `research/data_sources/` | Satellite, in situ, fusion, and adjacent EO context suitability |
| External source code discovery | P3 | `research/code_sources/inventory.csv` | Catalogue external implementations as evidence |
| Scientific reverse engineering | P4 | `research/code_sources/analysis/` | Explain scientific reasoning embedded in selected code |
| Specifications | P5 | `specs/` | Phase-specific algorithm contracts |
| Decisions | P5, P6 | `docs/adr/` | Durable accepted or proposed decisions |
| Validation and reporting | P5, P6 | `validate/`, `report/` | Make claims testable, bounded, and reproducible |
| Drift control | P6 | `governance/` | Keep the repo aligned with the mission and principles |

## Architectural rules

- Forest cover estimation remains the primary objective.
- Adjacent Earth-observation products enter through `research/data_sources/` as context
  products with an explicit `evidence_role`, `domain`, and `forest_relevance`.
- Every inventory row should reference a search scope where practical.
- Every material claim should be traceable from report/spec/ADR back to evidence in
  `research/`.
- Tooling comparisons stay in `research/packages/`; datasets and products stay in
  `research/data_sources/`; external implementations stay in `research/code_sources/`.
- Reverse-engineering artifacts must explain scientific reasoning, assumptions, limitations,
  and paper-to-code divergence, not just list files and functions.

