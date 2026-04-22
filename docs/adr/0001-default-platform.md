# ADR 0001: Default Platform

- **Status:** Proposed
- **Date:** 2026-04-22
- **Deciders:** Forest Cover Lab maintainers
- **Technical area:** platform
- **Supersedes:** None
- **Superseded by:** None

## Context

Forest Cover Lab needs a default platform for:

- v1 baseline forest-cover estimation
- reproducible AOI-scale processing
- straightforward export of rasters, vectors, and summary tables
- future extension toward monthly estimation

The default platform must balance:

- speed of implementation
- archive access
- reproducibility
- maintainability
- ease of inspection
- suitability for later time-series work

### Earth Engine quota notice

Google Earth Engine is introducing non-commercial quota tiers effective **27 April 2026**.
The repo must not assume unlimited free compute. This ADR must be updated as quota policy changes.

## Decision

Adopt a Python-first workflow centered on:

- a cloud-capable remote sensing platform (Google Earth Engine + `geemap`) for v1 baseline prototyping
- local reproducible post-processing using `GDAL`, `Rasterio`, and `rioxarray` for clipping, reprojection, export, and reporting
- portable artifacts stored outside the execution environment

The exact package stack is documented in:

- `research/packages/platform_decision.md`

Until superseded, the implementation must remain portable and must not depend on interactive notebook state for correctness.

## Rationale

- Rapid baseline generation with Earth Engine archive access
- Explicit artifact export enforced locally
- Support for later monthly extension via Sentinel-1/2
- Low friction for standard geospatial engineering tasks

A mixed cloud + local workflow is the most practical starting point for the planning milestone.

## Alternatives considered

### Fully local-first stack
Good for reproducibility, but slower to stand up at large scale and requires local tile storage.

### Desktop GIS-first workflow
Useful for manual exploration, but weaker as the default engineering path and harder to automate.

### Research-only ML stack as default
Premature for the planning milestone; too complex before v1 is validated.

## Consequences

### Positive
- Fast path to a baseline
- Easier separation of research and production artifacts
- Better portability of outputs

### Negative
- Platform access and quota risk (especially post-27 April 2026)
- Split execution model may increase orchestration complexity

### Neutral / follow-up
- Final package selection depends on `research/packages/` research track
- Fallback to a fully local GDAL pipeline must be designed before quota limits bind

## Acceptance criteria

- `research/packages/platform_decision.md` names a default stack
- the default stack supports v1 outputs
- the stack does not block v2 and v3 evolution
- EE quota status is reviewed before any production run

## Risks and limitations

- EE non-commercial quota limits effective 27 April 2026 may restrict large-AOI jobs
- Platform-specific assumptions may leak into the repo
- Cloud convenience can obscure reproducibility if exports are not enforced

## References

- `research/packages/packages_matrix.csv`
- `research/packages/platform_decision.md`
- `specs/v1_forest_baseline.md`
