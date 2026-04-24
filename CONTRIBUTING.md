# Contributing to Forest Cover Lab

Before contributing, read `governance/principles.md`. Every contribution is evaluated
against the six principles. Run `governance/drift_checklist.md` if your change affects
the repository structure.

---

## What belongs in this repo

Contributions are welcome for:

- downstream repo contracts and compatibility notes
- literature review and evidence synthesis (papers, reports, and blogs)
- data source and adjacent context product suitability analysis
- external codebase discovery and reverse engineering
- package and platform comparison
- method specifications
- architecture decision records
- validation plans
- reporting contracts
- reproducible geospatial processing code

---

## Research track contributions

### Methodology track (`research/methodology/`)

- Use when: proposing changes to the research protocol, adding practitioner sources,
  or refining the search guide.
- Required: record reusable search scopes in `research/methodology/search_scopes.csv`.
- Rule: changes to `research_guide.md` that affect how other tracks operate must be
  discussed in an issue before merging.

### Publications track (`research/publications/`)

- Use when: adding or reviewing a paper, technical report, or blog post.
- Required: declare a search scope (objective, keywords, date range, databases) before
  adding a batch of entries. Record it in `research/methodology/search_scopes.csv` and
  reference it with `search_scope_id`.
- Required: score all five dimensions immediately after reading.
- Required: set `venue_type` correctly — `journal`, `conference`, `technical_report`,
  `blog`, or `preprint`. Never classify a blog post as a journal article.
- ADR link: if a source influences an ADR, reference the source in the ADR.

### Data and context sources track (`research/data_sources/`)

- Use when: adding or reviewing a satellite dataset, in situ dataset, fusion product, or
  adjacent EO context product.
- Required: fill all columns in `inventory.csv` including license and access method.
- Required: fill `evidence_role`, `domain`, `forest_relevance`, and `search_scope_id`.
- Required: assess suitability for all three phases (v1, v2, v3) using `suitability_rubric.md`.
- Rule: data sources are separate from implementation tools. Do not add GDAL or GEE here;
  those belong in `research/packages/`.
- Rule: biodiversity, oceans, energy, integrity, floods, fire, climate, and land-pressure
  products are valid only when their relevance to forest-cover estimation is explicit.

### Code sources track (`research/code_sources/`)

- Use when: cataloguing an external codebase (P3) or producing a reverse engineering
  artifact (P4).
- P3 entry: fill all columns in `inventory.csv`, including `search_scope_id`. A codebase
  without a linked paper is valid.
- P4 artifact: copy `reverse_engineering_template.md` to
  `analysis/<repo_name>/reverse_engineering.md`. Fill all sections. Record the commit hash
  analyzed. Set `reverse_engineered = yes` in the inventory.
- Rule: a P4 artifact explains **why** the code does what it does, not what it does
  operationally. If the artifact is primarily a list of function descriptions, it is not
  a reverse engineering artifact.

---

## What must be explicit in any contribution

Any contribution affecting outputs or interpretation must document:

- the target phase: v1, v2, or v3
- data source(s)
- downstream repo(s) affected, if any
- forest-definition assumptions
- evidence role and forest relevance for any non-forest context products
- CRS and area method
- limitations and uncertainty
- whether the change affects scientific interpretation

---

## Pull request guidance

A PR should generally do one of these:

- add or revise one ADR
- add or review one paper, report, or blog (or a batch with a shared search scope)
- add or review one data source (or a batch from the same provider)
- add or review one code source entry
- produce one reverse engineering artifact
- update downstream repo contract guidance
- refine one spec
- add one coherent unit of implementation
- improve validation or reporting contracts

Keep changes scoped. Do not mix research contributions with implementation changes in one PR.

---

## Review checklist

Before submitting:

- `governance/drift_checklist.md` has been run if the PR changes directory structure
- docs are updated if behavior or meaning changes
- names and schemas are consistent with existing files
- thresholds are not hard-coded without explanation
- annual labels are not presented as monthly ground truth
- area is not reported without documenting the method
- `venue_type` is set correctly in every new publications row

---

## Commit style

```
docs: add ADR for forest definition
research: add Hansen GFC to data sources inventory
research: reverse engineer MapBiomas detection pipeline
specs: refine v2 monthly confirmation requirements
governance: add initial drift checklist run to audit log
```

---

## Issues

Use issue templates for:

- method research
- package evaluation
- ADR proposals

---

## Code quality

When processing code is added:

- keep functions small and testable
- document configuration inputs
- avoid notebook-only logic for core processing
- preserve reproducibility of outputs
