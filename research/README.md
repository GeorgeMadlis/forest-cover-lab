# Research

This directory contains the research tracks that feed Forest Cover Lab decisions.

All tracks are governed by `governance/principles.md`. Each track is designed to be entered
independently — completing one track is not a prerequisite for entering another.

The primary mission is forest cover estimation. Adjacent Earth-observation domains are
handled as context evidence when they support forest interpretation, validation, uncertainty,
or risk assessment.

---

## Tracks

| Subdirectory | Principle | Purpose |
|---|---|---|
| `methodology/` | P1 | How to conduct research: search scopes, protocol, blogs, stopping criteria |
| `publications/` | P1 | Literature review: papers, technical reports, practitioner blogs |
| `data_sources/` | P2 | Data and context suitability: satellite, in situ, fusion, adjacent EO products |
| `code_sources/` | P3 + P4 | Code discovery and reverse engineering: external implementations |
| `packages/` | — | Implementation tooling for this repo's own processing pipeline |

---

## Track summaries

### `methodology/` — Research Conduct Protocol

Defines how all knowledge acquisition is done in this repo. Contains the search-scope
registry, search protocol, and a curated list of practitioner sources to monitor. Does not
produce publication, data-source, or code-source entries directly — it governs how the other
tracks operate.

### `publications/` — Literature and Practitioner Sources

Inventory of reviewed papers, technical reports, and practitioner blogs. Scored on five
dimensions (scientific relevance, label match, codeability, reproducibility, operational
usefulness). Feeds ADRs and the shortlist.

### `data_sources/` — Data and Context Product Suitability

Inventory of satellite datasets, in situ measurements, fusion products, and adjacent
Earth-observation context products evaluated for phase-by-phase suitability (v1/v2/v3).
Context products include biodiversity, ocean/coastal, renewable energy, environmental
integrity, flood, fire, climate, and pressure layers when they help interpret forest-cover
outputs. Kept separate from `packages/` — a data source is what you pull from; a package is
what you run it through.

### `code_sources/` — Code Discovery and Reverse Engineering

Inventory of external codebases (P3) and written reverse engineering artifacts that surface
the scientific reasoning embedded in selected implementations (P4). A codebase may be
catalogued with or without a linked publication.

### `packages/` — Implementation Tooling

Comparison of software packages and platforms used in this repo's own processing pipeline
(GEE, GDAL, Rasterio, eo-learn, etc.). Scope is limited to tools for running the pipeline,
not datasets or external research implementations.

---

## Shared rules

- Both `publications/` and `code_sources/` accept entries without requiring the other.
- Inventories should reference `research/methodology/search_scopes.csv` through a
  `search_scope_id` where practical.
- ADRs in `docs/adr/` are not final until they reference supporting evidence from at least
  one of the research tracks.
- Decisions arising from research tracks must be recorded in an ADR — not in README files.
- Context products must have a clear forest-cover relevance statement before they influence
  specs, reports, or validation.
