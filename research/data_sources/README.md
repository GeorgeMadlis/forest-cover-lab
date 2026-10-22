# Data Sources Track

This track evaluates satellite datasets, in situ measurements, fusion products, and adjacent
Earth-observation context products as first-class research objects, independently of any
algorithm or implementation.

**Principle:** P2 - Data and Context Product Suitability (`governance/principles.md`)

## Inputs

None required. This track can be entered without completing the literature review or
the code sources track.

Optionally consumes:

- [eudr-dmi-gil auto catalogue](https://github.com/GeorgeMadlis/eudr-dmi-gil/blob/main/data_db/dataset_catalogue_auto.csv) as a cross-repo **unverified** lead inventory, retaining its row IDs and source version.
- [Fields of The World](https://fieldsofthe.world/), [Source Cooperative](https://docs.source.coop/) and [Earthmover](https://www.earthmover.io/) for labeled/predicted agriculture features, hosted data discovery and data-access tooling respectively.
- `research/publications/publications_inventory.csv` — papers may reference data sources
  not yet catalogued here; add them when discovered.
- `research/methodology/research_guide.md` — search protocol applies when surveying
  new data source categories.

## Outputs

- `inventory.csv` — master catalogue of all evaluated data sources
- `suitability_rubric.md` — criteria for phase-by-phase suitability assessment
- `context_products.md` — guidance for biodiversity, oceans, energy, integrity, floods,
  and other adjacent products
- `sources_notes.md` — qualitative notes per data source
- `discovery_and_link_verification.md` — FAIR-inspired provider discovery, URL audit and question-answer protocol
- Findings feed ADRs in `docs/adr/`, phase specifications in `specs/`, and downstream
  repository contracts in `docs/downstream_repos.md`

---

## Files

| File | Purpose |
|---|---|
| `inventory.csv` | Master catalogue of all evaluated data sources |
| `suitability_rubric.md` | Scoring criteria for v1, v2, v3 suitability |
| `context_products.md` | Scope and usage rules for adjacent EO context products |
| `sources_notes.md` | Qualitative per-source notes (format as one section per source) |
| `discovery_and_link_verification.md` | Discovery, link checks and source-backed dataset/tool handoffs |

## Evidence roles

Use the `evidence_role` column to keep broad Earth-observation context from diluting the
forest-cover mission.

| Role | Meaning |
|---|---|
| `core estimation input` | Direct input to a forest-cover or disturbance estimate |
| `auxiliary feature` | Feature that may improve modeling but cannot define forest alone |
| `validation reference` | Independent reference used for comparison or plausibility checks |
| `context/risk layer` | Explains pressures, anomalies, or uncertainty around forest estimates |
| `exclusion mask` | Used to exclude non-target areas such as permanent water or urban pixels |
| `interpretation-only background` | Useful context for reports, not an algorithmic input |

## Domains tracked

| Category | Examples |
|---|---|
| Forest cover and disturbance | Hansen GFC, JRC TMF, MapBiomas, PRODES, GLAD alerts |
| Optical and SAR observations | Landsat, Sentinel-1, Sentinel-2, MODIS, Planet |
| Forest structure | GEDI, ICESat-2, lidar-derived canopy-height products |
| In situ / field data | National Forest Inventories (NFIs), field plots |
| Fusion products | ESA CCI Land Cover, Copernicus Global Land Cover |
| Biodiversity | protected areas, habitat integrity, species richness, ecosystem intactness |
| Ocean/coastal | mangroves, ocean color, shoreline change, estuary context |
| Energy | solar resource, wind resource, transmission, infrastructure pressure |
| Environmental integrity | environmental integrity index, human footprint, ecosystem integrity |
| Floods and water | flood extent, surface water seasonality, wetlands, inundation |
| Other pressure/context | fire, climate, agriculture, settlements, roads, mining, concessions |

## Discovery and maintenance role

The [dataset/tool discovery specialist](../../agent_harness/roles/dataset-and-tool-discovery.md) supports scoped web/provider searches, link verification and evidence-backed pipeline questions. Use the [discovery protocol](discovery_and_link_verification.md) to separate products, access services and tools, assess FAIR dimensions and produce reviewable link deltas. New sources remain `to_review` until human review; software/platform comparisons belong in `research/packages/`. No existing link has been verified solely by adding this role.

## Workflow

1. Declare a search scope in `research/methodology/search_scopes.csv` before adding
   an inventory entry.
2. Add a row to `inventory.csv` with `status = to_review` and its `search_scope_id`.
3. Fill all columns, including `evidence_role`, `domain`, and `forest_relevance`.
4. Fill the three suitability columns; set `status = reviewed` only after human review.
   Inventory review does not validate scientific graph claims; those require the separate
   [knowledge-promotion gate](../../governance/knowledge_promotion.md).
5. Add a qualitative section to `sources_notes.md` if needed.
6. If suitability changes an ADR recommendation, open an ADR update.

## Rules

- Data source evaluation is independent of package/tool evaluation in `research/packages/`.
  A data source is what you pull from; a package is what you run it through.
- Data-source IDs are stable references for downstream repos. Reuse an existing ID such as
  `DS-0002` or `DS-0003` instead of re-describing Sentinel sources in each implementation
  repo.
- Every entry must declare license and access method — a source with unclear licensing
  must be flagged, not silently included.
- In situ data must be classified as validation resources, not training labels, unless
  their temporal and spatial alignment with the target variable has been verified.
- Context products must state why they matter for forest cover. If `forest_relevance` is
  unclear, the entry should remain `to_review` or be rejected.
