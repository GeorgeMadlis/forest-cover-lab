# Evidence Artifacts

Expected artifact types across phases.

## Phase v1

| Artifact | Format | Required |
|---|---|---|
| Baseline forest mask | GeoTIFF / COG (`uint8`, nodata 255) | Yes |
| AOI summary table | CSV | Yes |
| Run manifest | JSON | Yes |
| Summary report | HTML | Yes |
| QA thumbnails | PNG | Recommended |

## Phase v2

| Artifact | Format | Required |
|---|---|---|
| Monthly S2 composites | GeoTIFF / COG per month | Yes |
| Monthly S1 composites | GeoTIFF / COG per month | Yes |
| Monthly forest indicators | GeoTIFF / COG per month | Yes |
| Monthly area summary table | CSV | Yes |
| Optical/SAR disagreement masks | GeoTIFF / COG per month | Yes |
| Run manifest | JSON | Yes |
| Monthly QA thumbnails | PNG per month | Yes |
| Summary report | HTML | Yes |

## Phase v3

| Artifact | Format | Required |
|---|---|---|
| Monthly latent prediction rasters | GeoTIFF / COG (`float32`, [0,1]) | Yes |
| Per-pixel uncertainty rasters | GeoTIFF / COG (`float32`) | Yes |
| Annual consistency summary | CSV + PNG | Yes |
| External triangulation review notes | Markdown or CSV | Yes |
| Run manifest with `weak_supervision = true` | JSON | Yes |
| Validation artifacts | mixed | Yes |
| Research report | HTML or Markdown | Yes |

## Common rules

- All raster artifacts are Cloud-Optimised GeoTIFFs (COG) unless otherwise stated.
- All tables include header row and explicit units.
- All artifact paths are recorded in the run manifest's `outputs` array.
