# ADR 0002: Forest Definition

- **Status:** Proposed
- **Date:** 2026-04-22
- **Deciders:** Forest Cover Lab maintainers
- **Technical area:** data
- **Supersedes:** None
- **Superseded by:** None

## Context

Forest area estimates depend strongly on the operational definition of "forest".

Without a written forest definition, output metrics are not comparable across:

- datasets
- geographies
- time periods
- implementations

## Decision

Every workflow in this repository must declare an explicit forest definition including, at minimum:

| Field | Description |
|---|---|
| `baseline_dataset` | Source dataset name and version |
| `forest_threshold_variable` | The variable used for the threshold test (e.g. `treecover2000`) |
| `forest_threshold_value` | Numeric threshold (default: 30 % for v1 Hansen GFC) |
| `minimum_mapping_area_ha` | Minimum contiguous area to be classified as forest (default: 0.5 ha) |
| `exclusion_masks` | Any layers explicitly excluded (water, urban, permanent agriculture) |
| `nodata_policy` | How nodata pixels are handled |
| `temporal_interpretation` | What time period the definition applies to |
| `datamask_value` | For Hansen GFC: only `datamask == 1` (mapped land) pixels qualify |

### v1 operational baseline (binding)

A pixel or patch is classified as **forest** if **all** of the following hold:

1. `datamask == 1` (mapped land, Hansen GFC).
2. `treecover2000 >= canopy_threshold_pct` (default: 30 %).
3. The contiguous mapped area satisfies the minimum mapping unit (default: 0.5 ha).
4. Any exclusions are documented separately in the run manifest.

The forest definition must be stored in `configs/` and recorded in the run manifest.

## Rationale

This decision ensures:

- comparability across runs
- transparency in reporting
- traceability of results
- reviewability by external parties

It also prevents accidental mixing of incompatible forest concepts.

## Alternatives considered

### Implicit dataset-native definition
Rejected because it is too ambiguous and varies between dataset releases.

### Hard-coded threshold for all contexts
Rejected because ecological and operational contexts differ; threshold must be declared per run.

### No minimum mapping area
Rejected because it makes outputs unstable and sensitive to noise pixels.

## Consequences

### Positive
- Better reproducibility
- Easier scientific interpretation
- Clearer validation requirements

### Negative
- More configuration burden per run
- More review overhead for contributors

### Neutral / follow-up
- Threshold values can vary by study but must be declared and versioned

## Acceptance criteria

- `configs/forest_definition.example.yaml` exists
- `configs/v1_defaults.yaml` references the Hansen GFC dataset and default thresholds
- v1 spec references the declared forest definition
- run manifest schema contains all required forest-definition fields

## Risks and limitations

- A declared definition can still be ecologically wrong for a given biome
- Different authoritative sources use different forest concepts; comparisons remain conditional on harmonization
- 30 m Landsat resolution imposes a practical minimum mapping constraint below the stated 0.5 ha MMU

## References

- `configs/forest_definition.example.yaml`
- `configs/v1_defaults.yaml`
- `validate/run_manifest.schema.json`
- `specs/v1_forest_baseline.md`
