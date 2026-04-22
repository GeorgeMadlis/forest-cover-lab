# Fetch

Data acquisition code and configuration.

## Responsibilities

- Authenticate or connect to approved data sources (Earth Engine, Sentinel Hub, etc.)
- Fetch or request source data
- Record provenance inputs for run manifests

## Rules

- Do not hardcode secrets — read from environment variables or `.env` files (gitignored).
- Do not mix fetching with core processing logic.
- Always preserve dataset name, dataset version, and access timestamp for the run manifest.

## Planned scripts (Phase 2)

| Script | Purpose |
|---|---|
| `fetch_hansen_v1.py` | Download/export Hansen GFC tiles for an AOI |
| `fetch_sentinel2_monthly.py` | Build monthly S2 composites for an AOI (v2) |
| `fetch_sentinel1_monthly.py` | Build monthly S1 composites for an AOI (v2) |
