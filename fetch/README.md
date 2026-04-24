# Fetch

Reference data acquisition code and configuration.

Forest Cover Lab may contain small reference fetchers used to validate contracts. Production
or product-specific acquisition pipelines should live in downstream repos such as
`sentinel-monthly-forest-cover`.

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
| `fetch_sentinel2_monthly.py` | Reference S2 fetcher for validating v2 contracts |
| `fetch_sentinel1_monthly.py` | Reference S1 fetcher for validating v2 contracts |
