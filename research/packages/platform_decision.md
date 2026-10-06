# Platform Decision

This document recommends:

- one **default** stack
- one **fallback** stack
- one **research-only** stack

## Decision status

Superseded by ADR 0005 on 2026-10-06. The stacks below are historical reference choices.
Current production policy is open/local/cloud-neutral and does not require GEE.

---

## Historical default stack

**Earth Engine + geemap (cloud) + GDAL + Rasterio + rioxarray (local)**

### Why

- Fast path to v1 baseline using Hansen GFC already hosted on Earth Engine.
- `geemap` provides Python-first scripting and notebook integration.
- Local GDAL/Rasterio/rioxarray enforces portable, reproducible artifact export outside EE.
- Supports v2 evolution (Sentinel-1/2 monthly composites are also available on EE).

### Constraints

- All EE outputs must be exported to local disk as GeoTIFF/COG before reporting.
- Run manifest must record EE asset IDs and access timestamp.
- EE quota status must be reviewed before any production run (see ADR 0001).

---

## Historical fallback stack

**SEPAL (cloud) or sentinelhub-py + GDAL/Rasterio (local)**

### Why

- Required because Earth Engine's non-commercial quota tiers take effect 27 April 2026.
- SEPAL provides a hosted forestry-focused alternative with comparable archive access.
- `sentinelhub-py` enables programmatic Sentinel access independent of Google.

### Constraints

- Fallback stack must produce identical run manifest fields and output formats.
- Must be exercised at least once per quarter to confirm operational readiness.

---

## Research-only stack

**eo-learn + PyTorch (or equivalent ML framework) + xarray**

### Why

- v3 weak supervision and latent monthly state models require ML tooling beyond v1/v2 needs.
- `eo-learn` provides time-series-aware EO pipelines suitable for research.
- Outputs from this stack are research artifacts, not production deliverables, and must be labelled as such.

### Constraints

- Research-only outputs must not be reported as operational forest-cover estimates without v2-equivalent validation.
- Annual Hansen labels used for supervision must be flagged as weak supervision in every manifest (see ADR 0004).

---

## Constraints to respect (all stacks)

- Support v1 baseline implementation
- Do not block v2 monthly evolution
- Keep exports portable (GeoTIFF/COG, GeoJSON, CSV)
- Preserve reproducibility outside notebooks
- Record dataset versions and access timestamps in every run manifest
