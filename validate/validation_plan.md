# Validation Plan

## Minimum validation requirements

### 1. Geometry and area unit tests

Required before reporting any area statistics. See `tests/`.

| Test ID | Description |
|---|---|
| `test_area_units` | Assert area output is in hectares; assert method is stated in manifest |
| `test_crs_round_trip` | EPSG:4326 → equal-area → EPSG:4326 area drift < 0.01 % on a known polygon |
| `test_threshold_sensitivity` | Output area changes monotonically as `canopy_threshold_pct` increases |
| `test_datamask_applied` | Pixels with `datamask != 1` are excluded from the forest mask |
| `test_manifest_present` | Every run output directory contains `run_manifest.json` |
| `test_manifest_schema` | The manifest validates against `validate/run_manifest.schema.json` |

### 2. Small-AOI integration test

Required before any v1 baseline run is reported externally.

| Property | Requirement |
|---|---|
| AOI size | ≤ 10 000 hectares |
| Forest composition | Known reference value available |
| Tolerance | Output forest area within ± 5 % of reference |
| Runtime | < 10 minutes on a standard laptop using cached tiles |
| Output | Valid `run_manifest.json` and `area_summary.csv` |

### 3. External comparison hooks

Where authoritative or widely used reference layers exist, validation must support comparison hooks.

Examples:

- national authoritative forest inventory layers
- Global Forest Watch annual loss overlay (reference / visual QA only)
- manually reviewed orthophoto samples (≥ 30 random points per stratum)

### 4. Temporal plausibility review (v2 / v3)

Monthly outputs require a documented review design:

- N ≥ 30 random pixel-months per stratum reviewed manually or by external triangulation
- Reviewer notes archived in `outputs/<run_id>/validation/`
- Implausible flicker (rapid month-to-month state oscillation without evidence) flagged and counted

## Important caution

> Annual agreement with annual forest-loss products **does not** prove monthly correctness.

This caveat must appear in every monthly report and in every v3 run manifest's `limitations` field.
