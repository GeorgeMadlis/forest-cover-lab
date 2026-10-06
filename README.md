# Forest Cover Lab

Forest Cover Lab is the governance, research, and evidence registry for forest-cover work
across a family of narrower repositories. It defines scientific contracts, explains the
reasoning behind them, and collects reusable data-source assessments for downstream
implementation repos.

## Purpose

This repository is designed to support:

- governance of downstream forest-cover repositories
- explanation of scientific assumptions, evidence, and non-claims
- a reusable registry of data sources and context products
- a transparent **big-picture forest coverage baseline**
- a structured research process for **monthly forest-cover estimation**
- parallel evaluation of:
  - **scientific methods and publications**
  - **data sources and adjacent context products**
  - **external source code and reverse-engineered reasoning**
  - **software packages and platforms**
- reproducible reporting with explicit provenance, assumptions, and limitations

Downstream repos such as `sentinel-monthly-forest-cover` and `gedi-validation-lab` should
consume contracts from this repo instead of redefining their own forest definitions,
data-source semantics, validation rules, or reporting disclaimers.

## ⚠️ Critical Warning

> **Hansen annual loss ≠ monthly ground truth.**
> Monthly forest cover must not be claimed as verified when it is derived from annual weak labels.

This constraint applies to all phases of this repository.

## Scope

The repository is intentionally organized in phases.

### v1 — Evidence-first baseline

Build a large-scale forest coverage baseline using established forest-cover / forest-change products and explicit forest-definition rules.

This phase prioritizes:

- transparency
- reproducibility
- easy review
- documented thresholds
- area accounting in hectares

### v2 — Monthly confirmation from time series

Add Sentinel-1 and Sentinel-2 monthly compositing and confirmation logic to improve temporal relevance.

This phase prioritizes:

- cloud-robust monthly inputs
- optical + SAR consistency
- temporal persistence rules
- operational monthly summaries

### v3 — Weakly supervised monthly estimation

Research a latent monthly forest-state or monthly disturbance model trained under annual or coarse supervision.

This phase prioritizes:

- methodological rigor
- explicit supervision semantics
- uncertainty communication
- external triangulation

## Principles

The six canonical principles governing this repository are defined in
[`governance/principles.md`](governance/principles.md).

Run [`governance/drift_checklist.md`](governance/drift_checklist.md) after every structural
change and record the result in [`governance/audit_log.md`](governance/audit_log.md).

The principles cover: research protocol and evidence capture, data and context product
suitability, external source code discovery, scientific reverse engineering, independent
workstreams, and architecture drift control.

The current architecture assessment is documented in
[`docs/architecture.md`](docs/architecture.md).

Guidance for downstream implementation repos is documented in
[`docs/downstream_repos.md`](docs/downstream_repos.md).

---

## Scientific constraints

### Forest definition must be explicit

No forest area number is meaningful without a documented forest definition.

Each run must specify:

- source dataset
- forest threshold(s)
- exclusion rules
- minimum mapping area
- nodata handling
- temporal interpretation

### Exchange CRS vs area CRS

- **EPSG:4326** is the required exchange format for AOI input and output interchange.
- **Equal-area CRS or explicit geodesic methods** must be used for area computation.
- All reported areas must be in **hectares**.

### Provenance is mandatory

Every run must produce a `run_manifest.json` containing:

- AOI identifier
- geometry hash
- data sources
- data access timestamps
- dataset versions
- algorithm version
- thresholds and parameters
- CRS and area method
- output artifact paths
- limitations notes

### Monthly outputs are not assumed to be ground truth

If annual forest-loss products are used as supervisory signals, they must be treated as
**weak supervision**, not literal monthly truth.

This repository must not claim that annual forest-loss labels are equivalent to monthly
forest-state labels.

## Repository structure

```text
governance/          Canonical principles, drift checklist, audit log
docs/                Architecture assessment and ADRs
docs/adr/            Architecture Decision Records — per-decision governance
docs/downstream_repos.md
                     Contract for narrower implementation repos
research/
  methodology/       Search scopes, research protocol, practitioner sources (P1)
  publications/      Literature and practitioner source inventory (P1)
  data_sources/      Satellite, in situ, fusion, and context product suitability (P2)
  code_sources/      External codebase discovery and reverse engineering (P3, P4)
  packages/          Reusable tooling assessments and backend policy
knowledge/           Contextual concepts and candidate/validated relationships
graph/               Ontology, schemas, local generator and derived JSON
specs/               Formal algorithm specifications (v1, v2, v3)
fetch/               Reference data acquisition code for contract validation
process/             Reference processing/modeling code for contract validation
validate/            Validation specs and tests
report/              Reporting contracts and evidence artifacts
configs/             Example configuration files
tests/               Shared contract and reference behavior tests
notebooks/           Exploratory notebooks for evidence and contract design
```

## Expected workflow

1. Define the AOI in GeoJSON or WKT.
2. Select the target phase: v1, v2, or v3.
3. Record forest-definition parameters.
4. Record the area-computation policy.
5. Acquire data through approved sources.
6. Process rasters and produce intermediate outputs.
7. Validate against required checks.
8. Export reports and a `run_manifest.json`.

## Research tracks

The core research tracks run in parallel. Each can be entered independently — no track is a
prerequisite for another. The full description of each track's inputs, outputs, and
cross-track dependencies is in `research/README.md`.

### A. Research methodology (P1)

Defines how all knowledge acquisition is done. Contains the search protocol and practitioner
source list. All other tracks follow this protocol, but none require it as a prerequisite.

Key artifacts: `research/methodology/search_scopes.csv`,
`research/methodology/research_guide.md`,
`research/methodology/practitioner_sources.md`

### B. Publications and practitioner sources (P1)

Covers journal papers, conference proceedings, technical reports, and practitioner blogs
(e.g. GEE blog, Sentinel Hub blog). Scored on five dimensions; high-scoring entries feed
`shortlist.md` and ADRs.

Key artifacts: `research/publications/publications_inventory.csv`,
`research/publications/shortlist.md`, `research/publications/methods_landscape.md`

### C. Data source suitability (P2)

Evaluates satellite datasets, in situ measurements, fusion products, and adjacent
Earth-observation context products independently of any algorithm. This includes background
products for biodiversity, ocean/coastal context, renewable energy, environmental integrity,
floods, fire, climate, and other pressure layers when they help interpret forest estimates.
Separate from package/tool comparison.

Key artifacts: `research/data_sources/inventory.csv`,
`research/data_sources/suitability_rubric.md`,
`research/data_sources/context_products.md`

Data-source entries are reusable across downstream repos. For example, Sentinel-1
(`DS-0003`) and Sentinel-2 (`DS-0002`) can support `sentinel-monthly-forest-cover`, while
GEDI (`DS-0006`) can support `gedi-validation-lab` as a validation reference.

### D. Code discovery and reverse engineering (P3 + P4)

Catalogues external codebases independently of publications (P3). Selected codebases receive
deep written analysis that surfaces the scientific reasoning embedded in implementation
choices (P4).

Key artifacts: `research/code_sources/inventory.csv`,
`research/code_sources/reverse_engineering_template.md`,
`research/code_sources/analysis/`

### E. Implementation tooling (supporting)

Compares software packages and platforms for downstream and reference implementations.
Scope covers reusable processing/discovery capabilities and optional reference backends;
dataset suitability and external scientific code assessments remain separate tracks.

Key artifacts: `research/packages/packages_matrix.csv`,
`research/packages/platform_decision.md`

## Minimum acceptance criteria for this repo

The planning milestone is complete when:

* the repository scaffold exists
* `governance/principles.md` is written and referenced from this README
* `docs/architecture.md` records the current architecture assessment
* `docs/downstream_repos.md` defines how narrower repos consume this repo's contracts
* the ADRs for platform, forest definition, area computation, and monthly target are written
* the publications inventory exists with scoring fields and `venue_type` column
* the methodology track includes a search-scope registry
* the data sources inventory exists with evidence-role, domain, forest-relevance, and phase
  suitability columns
* the code sources inventory and reverse engineering template exist
* the packages matrix exists with decision fields
* the v1, v2, and v3 specs are present
* the run manifest schema exists
* the validation plan exists
* `governance/drift_checklist.md` has been run at least once and recorded in `audit_log.md`

## Non-goals for the planning milestone

This milestone does **not** require:

* model training
* production deployment
* empirical validation results
* nationwide estimates
* publication-quality figures

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before adding methods, packages, thresholds, or interpretation claims.

## License

Apache License 2.0. See [LICENSE](LICENSE).

## Semantic discovery and implementation boundary

Forest Cover Lab = scientific/governance/semantic authority.
The [OKF-oriented corpus](knowledge/README.md) = contextual human- and agent-readable knowledge.
The [generated KG](graph/README.md) = machine-queryable typed relationships.
Downstream repos = executable implementations. STAC/GeoParquet/provider catalogues = live
observation discovery. Run manifests and evidence = execution provenance.

Discovery follows application → scientific question → method → observation requirements →
measurements → candidate datasets → access mechanisms → processing capabilities → executable
workflow → validation requirements → evidence/result. The observation layer allows dataset
substitution without redefining the application; compatibility still requires validation.
The KG describes capabilities and relationships, not the complete EO observation archive.
Individual Sentinel scenes and run results stay outside the corpus.

[ADR 0005](docs/adr/0005-semantic-architecture-and-backends.md) separates methods from backends:
regional/country-scale production prefers open/local/cloud-neutral tooling and must not require
GEE. GEE is optional for examples, research or suitable large/global analyses. Existing GEE
acquisition routes in phase specs are reference implementations. All scientific non-claims remain.
Seasonal comparisons and intended downstream mappings are candidates pending review, not
validated algorithms. See [promotion governance](governance/knowledge_promotion.md).

Local checks (no EO downloads or backend required):

```sh
python -m pip install -e '.[dev]'
python graph/build.py --check
python -m pytest
```

Core dependencies are PyYAML and jsonschema. Optional `reference` and `gee` extras are for
reference implementation work. Semantic provenance is a backward-compatible optional block;
see [its contract](validate/semantic_provenance.md).
