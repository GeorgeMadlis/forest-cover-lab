# Principles

These six principles are the canonical reference for all decisions in Forest Cover Lab and
for downstream repositories that choose to depend on it. Any structural change to this
repository must be reviewed against these principles using `drift_checklist.md`.
Divergence is a defect, not natural evolution.

## Mission boundary

The primary mission is forest cover estimation from satellite data. Adjacent Earth-observation
products are in scope only when they improve interpretation, validation, transferability, or
risk assessment for forest cover estimation. Examples include biodiversity products, ocean
and coastal products, solar and wind resource layers, environmental integrity indices, flood
products, fire products, land-use layers, and climate reanalysis data.

Adjacent products must be recorded as context evidence, not allowed to dilute the primary
forest-cover objective.

This repository governs, explains, and collects reusable data-source evidence. Narrower
implementation repos should consume these contracts by reference, not fork the scientific
definitions silently.

---

## P1 - Research Protocol and Evidence Capture

All knowledge acquisition follows a declared protocol. Before entering any research track,
the researcher specifies a search scope: objective (one sentence), source types, keywords,
date range, and search engines or databases. The declared scope is recorded before entries
are added to an inventory. Reading a paper, blog post, or technical report is a deliberate
act that produces a structured record.

The process of how knowledge was sought is as important as what was found, because it
enables others to repeat the search, audit the coverage, and identify gaps.

**Covered source types:** journal papers, conference proceedings, technical reports,
practitioner blogs (e.g. Google Earth Engine blog, Sentinel Hub blog), working documents
from FAO, JRC, INPE, and national forest monitoring agencies.

**Governing files:** `research/methodology/`

---

## P2 - Data and Context Product Suitability

Satellite datasets, in situ measurements, fusion products, and adjacent context products are
evaluated as first-class research objects, independently of any algorithm or implementation.
For each candidate source, the repository records: evidence role, domain, spatial coverage,
temporal coverage, spatial resolution, access method, license, latency, forest relevance,
and phase-by-phase suitability against the v1/v2/v3 roadmap.

This track can be entered and conducted without completing the literature review.

**Covered source types:** Landsat, Sentinel-1, Sentinel-2, MODIS, GEDI, JRC TMF, Hansen
GFC, PRODES, Global Forest Watch, national forest inventories, in situ plot data, and
multi-source fusion products. Context products may include biodiversity, ocean/coastal,
renewable energy, environmental integrity, flood, fire, climate, and land-use products.

**Evidence roles:** core estimation input, auxiliary feature, validation reference,
context/risk layer, exclusion mask, or interpretation-only background.

Downstream repos should reference stable source IDs from `research/data_sources/inventory.csv`
when using shared sources. A source such as Sentinel-2 may be a core estimation input in one
repo and an auxiliary or validation input in another, but the provenance and suitability
assessment live here.

**Governing files:** `research/data_sources/`

---

## P3 - External Source Code Discovery and Analysis

External codebases that solve forest-cover-related tasks are catalogued and assessed as
research artifacts, independently of the publications that may accompany them. Code is found
through dedicated searches — GitHub, conference paper appendices, open review platforms, lab
repositories — and evaluated for: task addressed, language, license, maturity, and phase fit.

A codebase may be catalogued with or without a linked publication. The two tracks (P1 and
P3) are independent.

**Covered codebase types:** change detection implementations, time-series forest monitoring,
weakly supervised segmentation, SAR-optical fusion, forest baseline generation.

**Governing files:** `research/code_sources/`

---

## P4 - Scientific Reverse Engineering of Source Code

Selected external codebases are subjected to deeper analysis that surfaces the scientific
reasoning embedded in implementation choices. The output is a written artifact — not code
documentation — that explains:

- what assumptions about the forest definition are encoded in the code
- what algorithmic decisions represent scientific judgments rather than engineering preferences
- what limitations are hidden in implementation details and would not be visible from the paper
- where the implementation diverges from the paper that describes it

Reverse engineering artifacts are stored in `research/code_sources/analysis/<repo_name>/`.
The template governing their structure is `research/code_sources/reverse_engineering_template.md`.

**This principle is distinct from P3.** P3 discovers and catalogues; P4 explains.

---

## P5 - Independent and Composable Workstreams

Each major section is designed to be entered and conducted independently. A researcher can
contribute a search scope, a publication review, a data-source assessment, a code-source
entry, a reverse-engineering artifact, a spec, or an ADR without having completed another
section.

Dependencies between tracks are explicit and declared. Each track's README states:

- what it assumes as input
- what it produces as output
- which other tracks it optionally consumes
- what downstream artifacts it can influence
- which downstream repositories or contracts can consume the result

Cross-references between tracks are allowed and encouraged, but never required for entry.

---

## P6 - Architecture Drift Control

These six principles are the canonical reference. The repository maintains governance
artifacts in `governance/` that make adherence visible:

- `principles.md` — this file; the canonical statement
- `drift_checklist.md` — a structured checklist run after every structural change
- `audit_log.md` — a time-stamped record of checklist runs and findings

Any structural change to the repository must be reviewed against `drift_checklist.md`.
Findings are recorded in `audit_log.md`. Drift is treated as a defect and must be resolved
in the same change that introduced it, or tracked as an open finding.

The README must reference `governance/` as the canonical principle source.
