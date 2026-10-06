# Architecture Assessment

This document records the current architecture view for Forest Cover Lab. It is not a
decision record; durable choices still belong in `docs/adr/`.

## Architecture intent

Forest Cover Lab is a governance, research, and evidence registry for forest-cover work
from satellite data. The architecture must support three parallel jobs:

1. Govern downstream implementation repositories through shared scientific contracts.
2. Explain why datasets, methods, codebases, and
   scientific claims were accepted, rejected, or deferred.
3. Collect reusable data-source assessments that downstream repos can consume by stable ID.

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
- The data-source inventory can act as a shared registry for narrow repos such as
  `sentinel-monthly-forest-cover` and `gedi-validation-lab`.

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
- Downstream repository expectations were implicit rather than documented as a contract.

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
| Downstream contracts | P5, P6 | `docs/downstream_repos.md` | Define how narrower repos consume this repo |
| Drift control | P6 | `governance/` | Keep the repo aligned with the mission and principles |

## Architectural rules

- Forest cover estimation remains the primary objective.
- Adjacent Earth-observation products enter through `research/data_sources/` as context
  products with an explicit `evidence_role`, `domain`, and `forest_relevance`.
- Every inventory row should reference a search scope where practical.
- Every material claim should be traceable from report/spec/ADR back to evidence in
  `research/`.
- Downstream repos should reference this repo by commit or release and cite the data-source
  IDs, ADRs, schemas, and reporting contracts they consume.
- Tooling comparisons stay in `research/packages/`; datasets and products stay in
  `research/data_sources/`; external implementations stay in `research/code_sources/`.
- Reverse-engineering artifacts must explain scientific reasoning, assumptions, limitations,
  and paper-to-code divergence, not just list files and functions.

## Semantic architecture (ADR 0005)

The semantic/scientific plane is the human-maintained `knowledge/` corpus plus existing
specs, governance and evidence assessments. `graph/` contains ontology, typed relationships,
schemas and a deterministic generator; `graph/generated/knowledge.json` is derived.
The executable software plane belongs to downstream repositories. Live observation
catalogues (STAC, GeoParquet, provider services) resolve scenes at runtime. The provenance
plane records planning, selected inputs, versions, parameters, limitations and results in
run manifests and evidence bundles. These four planes have separate authorities.

The conceptual flow is:

```text
Application → Scientific question → Method → Observation requirements
→ Measurements/variables → Candidate datasets → Access mechanisms
→ Processing/tool capabilities → Executable workflow → Validation → Evidence/result
```

This is a discovery sequence, not an assertion that every record forms a complete linear
path. Datasets satisfy observation requirements subject to scale, geography, quality and
semantic compatibility. Capabilities describe software operations; workflows implement
methods partially or fully and must declare divergence. Run-specific evidence/results are
outside the graph. `knowledge/README.md` defines each concept layer and its directory.

Candidate and validated edges are separate output collections. AI-generated proposals cannot
become canonical through deterministic checks alone or a single run. Contract transcriptions
have explicit attribution; seasonal method decisions remain candidates requiring review.
The revision hashes corpus, cited local contracts and graph rules; Git commits/tags are pinned
separately. Review-after deadlines are consumer checks, not nondeterministic build behavior.

Production methods must not require GEE. ADR 0005 supersedes ADR 0001's platform default;
GEE acquisition in existing phase specs is a reference route, preserving scientific rules.
The repo needs only lightweight local validation dependencies, with optional backend extras.
No graph service, execution engine or observation archive is introduced.
