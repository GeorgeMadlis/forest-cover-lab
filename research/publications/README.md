# Publications and Practitioner Sources Track

This directory contains the structured literature review for Forest Cover Lab.

**Principle:** P1 - Research Protocol and Evidence Capture (`governance/principles.md`)

## Inputs

None required. This track can be entered independently.

Optionally consumes:
- `research/methodology/research_guide.md` — search protocol for how to find and read sources
- `research/methodology/practitioner_sources.md` — curated list of practitioner blogs to monitor

## Outputs

- `publications_inventory.csv` — master record of all reviewed sources
- `shortlist.md` — high-scoring sources selected for implementation reference
- `methods_landscape.md` — thematic synthesis that feeds ADRs in `docs/adr/`

---

## Objective

Identify, compare, and prioritize knowledge sources relevant to:

- forest extent / forest cover baselines
- annual forest-loss products and label semantics
- Sentinel-1 / Sentinel-2 forest monitoring
- time-series forest disturbance detection
- weak supervision and noisy labels in EO
- reproducible codebases suitable for adaptation

## Source types covered

This track covers **all knowledge sources**, not only journal papers:

| `venue_type` value | Examples |
|---|---|
| `journal` | Remote Sensing of Environment, TGRS, ISPRS |
| `conference` | IGARSS, ESA Living Planet, CVPR |
| `technical_report` | FAO FRA, JRC product documentation, INPE methodology reports |
| `blog` | Google Earth Engine blog, Sentinel Hub blog, GFW blog |
| `preprint` | arXiv, ESSOAr |

Use the correct `venue_type` in every row. Never classify a blog post as a journal article.

---

## Files

| File | Purpose |
|---|---|
| `publications_inventory.csv` | Master inventory of all reviewed sources |
| `publications_scoring_rubric.md` | Scoring rules and interpretation guide |
| `methods_landscape.md` | Thematic synthesis of method families |
| `shortlist.md` | Selected sources for roadmap phases |

## Review rules

Every source must be scored on:

- scientific relevance (0–3)
- label match to the repo goal (0–3)
- codeability (0–3)
- reproducibility (0–3)
- operational usefulness (0–3)

Use `publications_scoring_rubric.md` and record `total_score` immediately after review.

## Workflow

1. Declare a search scope following `research/methodology/research_guide.md`.
2. Record the scope in `research/methodology/search_scopes.csv`.
3. Add a new row to `publications_inventory.csv` with `status = to_review` and the
   relevant `search_scope_id`.
4. Score all five dimensions after reading.
5. Set `status = reviewed` and `roadmap_fit` to `v1`, `v2`, `v3`, or `reject`.
6. If `total_score >= 12`, add to `shortlist.md`.
7. Update `methods_landscape.md` to reflect any new method families.
8. If the source references a codebase not yet in `research/code_sources/inventory.csv`,
   add it there (this is a cross-track contribution; it does not block step 4).
9. If the source references a data source not yet in `research/data_sources/inventory.csv`,
   add it there.
