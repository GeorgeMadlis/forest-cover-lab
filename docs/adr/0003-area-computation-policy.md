# ADR 0003: Area Computation Policy

- **Status:** Proposed
- **Date:** 2026-04-22
- **Deciders:** Forest Cover Lab maintainers
- **Technical area:** validation
- **Supersedes:** None
- **Superseded by:** None

## Context

Forest Cover Lab reports forest area and change area in hectares.

Area numbers can be materially wrong if computed directly in an unsuitable CRS or without documenting the method.

EPSG:4326 is a geographic coordinate system, not an area-safe projection. Computing area in degrees produces incorrect results without explicit geodesic correction.

## Decision

Use the following policy for all area computations:

| Rule | Value |
|---|---|
| Exchange format | EPSG:4326 GeoJSON or WKT |
| Area computation | Equal-area CRS **or** explicit geodesic area method |
| Preferred equal-area CRS | EPSG:6933 (WGS 84 / NSIDC EASE-Grid 2.0) for global AOIs |
| Area unit | Hectares — always state the method |
| Geometry hash | SHA-256 of canonical GeoJSON, stored in every run manifest |

No result may be published without stating the area-computation method and CRS.

The area method and CRS must be recorded in the run manifest under `area_method.type`, `area_method.crs`, and `area_method.unit`.

## Rationale

This protects the repo against:

- silent CRS errors producing wrong hectare figures
- inconsistent area numbers across runs
- irreproducible reporting that cannot be audited

## Alternatives considered

### Compute area in EPSG:4326
Rejected — EPSG:4326 is not an area-safe method. Results are meaningless without geodesic correction.

### Leave area method unspecified
Rejected — undermines traceability and makes results incomparable.

### Use only one equal-area CRS for all AOIs globally
Accepted as default (EPSG:6933) but the policy allows geodesic alternatives to be stated explicitly.

## Consequences

### Positive
- Safer area accounting
- Easier unit testing of area outputs
- Better interoperability with external reference figures

### Negative
- More implementation detail required per script
- Extra CRS selection logic may be needed for non-global AOIs

### Neutral / follow-up
- Geodesic and equal-area methods may differ slightly; both are acceptable if stated

## Acceptance criteria

- run manifest schema includes `exchange_crs`, `area_method.type`, `area_method.crs`, `area_method.unit`
- validation plan includes area unit tests
- all specs require hectare reporting with method stated

## Risks and limitations

- Users may misuse projected rasters unless area-method checks are enforced at runtime
- Geodesic and equal-area methods will differ slightly for large AOIs; difference should be < 0.1 %

## References

- `validate/run_manifest.schema.json`
- `validate/validation_plan.md`
- `specs/v1_forest_baseline.md`
- `configs/v1_defaults.yaml`
