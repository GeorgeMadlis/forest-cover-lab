# Process

Raster processing and modeling code.

## Responsibilities

- masking
- compositing
- change detection
- model inference
- area summarisation support

## Rules

- Core processing must be reproducible.
- Notebook-only logic is not sufficient for any v1/v2/v3 deliverable.
- All threshold logic must be explicit and read from `configs/`.
- Every script must log its config hash and write a `run_manifest.json` to its output directory.

## Planned scripts (Phase 2)

| Script | Purpose |
|---|---|
| `v1_forest_mask.py` | Apply threshold + MMU + datamask to Hansen GFC; export COG |
| `v2_monthly_indicator.py` | Compute monthly forest indicators from S1/S2 composites |
| `v3_latent_monthly.py` | Train and infer the v3 weak-supervision monthly model |
