# Downstream Repository Contract

Forest Cover Lab governs, explains, and collects reusable data-source evidence for narrower
implementation repositories. Downstream repos execute a specific pipeline or validation
study; this repo remains the source of truth for shared scientific contracts.

## Responsibilities

| This repo governs | Downstream repos implement |
|---|---|
| Forest definition policy | Concrete masks, composites, models, and products |
| Data-source suitability and stable source IDs | Source-specific ingestion and processing code |
| ADRs and scientific non-claims | Repo-specific engineering choices |
| Run manifest schema | Run output generation |
| Validation and reporting contracts | Project-specific tests, reports, and QA dashboards |
| Research evidence and reverse engineering | Narrow implementation experiments |

## Required references

A downstream repo should declare which Forest Cover Lab contracts it consumes:

- source repo commit or release tag
- data-source IDs from `research/data_sources/inventory.csv`
- ADRs from `docs/adr/`
- phase spec from `specs/`
- manifest schema from `validate/run_manifest.schema.json`
- reporting contract from `report/reporting_contract.md`
- validation requirements from `validate/validation_plan.md`

Do not silently redefine forest definitions, area methods, label semantics, data-source
roles, or monthly non-claims in a downstream repo. If a downstream implementation needs a
different rule, propose or document that divergence here first.

## Example downstream repos

| Repo | Likely consumed sources | Main consumed contracts |
|---|---|---|
| `sentinel-monthly-forest-cover` | `DS-0002` Sentinel-2 MSI L2A, `DS-0003` Sentinel-1 GRD, optional `DS-0005` MODIS vegetation context | v2/v3 specs, monthly target ADR, manifest schema, reporting contract |
| `gedi-validation-lab` | `DS-0006` GEDI, optional `DS-0002` Sentinel-2, `DS-0003` Sentinel-1, forest baseline products | validation plan, data-source roles, forest definition ADR, report non-claims |
| `hansen-baseline-forest-cover` | `DS-0001` Hansen GFC, optional `DS-0007` JRC TMF and `DS-0008` PRODES for comparison | v1 spec, forest definition ADR, area computation ADR, manifest schema |

## Data-source reuse

Data-source entries are reusable evidence objects. A source can be used by multiple
downstream repos with different roles:

- Sentinel-2 can be a core optical input in `sentinel-monthly-forest-cover`.
- Sentinel-2 can be an auxiliary comparison layer in `gedi-validation-lab`.
- GEDI can be a validation reference in a monthly forest-cover repo.
- Flood or surface-water products can be context/risk layers in multiple repos.

The shared assessment lives in `research/data_sources/inventory.csv`. Downstream repos may
add implementation-specific notes, but license, provenance, suitability, and forest relevance
should trace back here.

## Compatibility checklist

Before a downstream repo claims compatibility with Forest Cover Lab:

- [ ] It pins a Forest Cover Lab commit or release.
- [ ] It lists consumed data-source IDs.
- [ ] It uses the run manifest schema or documents a compatible superset.
- [ ] It states forest-definition assumptions.
- [ ] It states CRS and area-computation policy.
- [ ] It preserves monthly weak-supervision non-claims.
- [ ] It links any divergence back to an ADR, issue, or documented finding in this repo.

