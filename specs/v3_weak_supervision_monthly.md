# v3 Weak Supervision Monthly Specification

## Goal

Research a latent monthly forest-state and/or monthly disturbance probability model trained under coarse (annual) supervision, using Sentinel-1/2 monthly feature stacks as inputs.

## Critical constraint

> Hansen annual loss is a **weak supervisory signal**, not monthly ground truth.
> Monthly latent outputs from this spec must never be reported as verified monthly truth.

This applies to all v3 artifacts, manifests, and reports (see ADR 0004).

## Inputs

| Input | Format | Source |
|---|---|---|
| AOI geometry | GeoJSON or WKT in EPSG:4326 | User-supplied |
| v1 baseline forest mask | GeoTIFF / COG | Output of v1 run |
| Monthly Sentinel feature sequences | Stacked GeoTIFFs or zarr | Output of v2 run |
| Annual Hansen `lossyear` | EE asset | `UMD/hansen/global_forest_change_2024_v1_12` |
| Model config | YAML | `configs/v3_model.yaml` (TBD) |

## Targets

This spec recognises two distinct latent targets (per ADR 0004):

1. **Monthly forest-state** — probability that pixel is forest in calendar month *m*.
2. **Monthly disturbance probability** — probability that a stand-replacement event occurred in calendar month *m*.

Both are **latent** when trained under annual supervision. They must be reported with explicit uncertainty.

## Outputs

| Output | Format | Path |
|---|---|---|
| Monthly latent prediction rasters | GeoTIFF / COG (`float32`, [0,1]) | `outputs/<run_id>/predictions/<target>_<YYYY-MM>.tif` |
| Annual consistency summary | CSV + PNG | `outputs/<run_id>/annual_consistency.csv` |
| Uncertainty rasters | GeoTIFF / COG (`float32`) | `outputs/<run_id>/uncertainty/<target>_<YYYY-MM>.tif` |
| Run manifest | JSON | `outputs/<run_id>/run_manifest.json` |
| Validation artifacts | mixed | `outputs/<run_id>/validation/` |

## Algorithm (high level)

1. Build monthly Sentinel feature stack from v2 outputs.
2. Construct weak supervision: annual Hansen `lossyear` is mapped to a *bag* of months for each calendar year.
3. Train a latent model (e.g. multi-instance learning, temporal CNN with annual pooling, or HMM-style temporal disaggregator) such that:
   - Monthly predictions aggregate to the annual label under the chosen pooling rule.
   - Monthly predictions are constrained by Sentinel evidence at the focal month.
4. Emit monthly predictions and per-pixel, per-month uncertainty.
5. Compute annual consistency: aggregate monthly predictions to annual and compare with Hansen `lossyear`.
6. Generate validation artifacts (see below).

## Required rules

- **Distinguish supervision from target** in every artifact and manifest.
- **Document aggregation logic**: the function that maps monthly predictions → annual label.
- **External triangulation plan required**: at minimum, manual review of N random pixel-months per stratum (default N ≥ 30).
- **Avoid overclaiming**: annual agreement does not prove monthly correctness.
- **Annual-loss labels** used for supervision must be tagged as `weak_supervision` in the manifest's `data_provenance`.

## Error modes

| Error mode | Mitigation |
|---|---|
| Model collapses to constant monthly probability | Add temporal smoothness regulariser; monitor entropy |
| Annual-only signal allows arbitrary monthly assignment | Constrain by Sentinel evidence; require minimum data density per pixel-month |
| Teacher-label noise propagated as truth | External triangulation; report uncertainty |
| Distribution shift across biomes | Stratified evaluation; do not extrapolate beyond training biome |

## Validation requirements

- Annual consistency check (predicted annual vs Hansen annual) within ± 10 %.
- Manual review of ≥ 30 random pixel-months per stratum, with reviewer notes archived.
- Temporal plausibility review (monotonicity where expected; no implausible flicker).
- Manifest validates against schema with `weak_supervision = true` in algorithm metadata.

## Non-claims

This v3 spec must not produce or imply:

- That monthly latent outputs are validated monthly forest-state ground truth.
- That high annual agreement implies high monthly accuracy.
- Operational alerts suitable for enforcement or commercial decisions without v2-equivalent confirmation.

## References

- ADR 0001 — Default Platform
- ADR 0002 — Forest Definition
- ADR 0003 — Area Computation Policy
- ADR 0004 — Monthly Target Definition
- `specs/v1_forest_baseline.md`
- `specs/v2_monthly_confirmation.md`
