# Forest Cover Lab

Forest Cover Lab is a reproducible repository for estimating forest coverage from raster satellite data, with a phased roadmap toward monthly forest-cover estimation and disturbance monitoring.

## Purpose

This repository is designed to support:

- a transparent **big-picture forest coverage baseline**
- a structured research process for **monthly forest-cover estimation**
- parallel evaluation of:
  - **scientific methods and publications**
  - **software packages and platforms**
- reproducible reporting with explicit provenance, assumptions, and limitations

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

## Core principles

### 1. Forest definition must be explicit

No forest area number is meaningful without a documented forest definition.

Each run must specify:

- source dataset
- forest threshold(s)
- exclusion rules
- minimum mapping area
- nodata handling
- temporal interpretation

### 2. Exchange CRS vs area CRS

- **EPSG:4326** is the required exchange format for AOI input and output interchange.
- **Equal-area CRS or explicit geodesic methods** must be used for area computation.
- All reported areas must be in **hectares**.

### 3. Provenance is mandatory

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

### 4. Monthly outputs are not assumed to be ground truth

If annual forest-loss products are used as supervisory signals, they must be treated as **weak supervision**, not literal monthly truth.

This repository must not claim that annual forest-loss labels are equivalent to monthly forest-state labels.

## Repository structure

```text
docs/                Architecture decisions and governance
research/            Publications and package/platform comparison
specs/               Formal algorithm specifications
fetch/               Data acquisition code
process/             Raster processing and modeling code
validate/            Validation specs and tests
report/              Reporting contracts and evidence artifacts
configs/             Example configuration files
tests/               Unit and integration tests
notebooks/           Exploratory notebooks only
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

## Initial research tracks

Two research tracks run in parallel:

### A. Publications / methods

This track answers:

* Which methods are scientifically relevant?
* Which methods are reproducible?
* Which methods are suitable for v1, v2, or v3?

Artifacts live in:

* `research/publications/publications_inventory.csv`
* `research/publications/publications_scoring_rubric.md`
* `research/publications/methods_landscape.md`
* `research/publications/shortlist.md`

### B. Packages / platforms

This track answers:

* Which stack should be the default implementation stack?
* Which tools are suitable for baseline work vs monthly time series vs ML research?
* Which dependencies introduce access, licensing, or operational risk?

Artifacts live in:

* `research/packages/packages_matrix.csv`
* `research/packages/packages_notes.md`
* `research/packages/platform_decision.md`

## Minimum acceptance criteria for this repo

The planning milestone is complete when:

* the repository scaffold exists
* the ADRs for platform, forest definition, area computation, and monthly target are written
* the publications inventory exists with scoring fields
* the packages matrix exists with decision fields
* the v1, v2, and v3 specs are present
* the run manifest schema exists
* the validation plan exists

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

TBD.
