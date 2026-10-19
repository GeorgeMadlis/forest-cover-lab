# Methods Landscape

This document synthesizes the publication inventory into method families relevant to Forest Cover Lab.

## Main buckets

### 1. Forest baseline / forest extent
Methods focused on large-scale forest vs non-forest mapping or baseline forest area.

Examples of expected methods:
- canopy-cover threshold + minimum mapping unit (Hansen GFC family)
- supervised classification of optical imagery
- canopy height–derived forest masks

### 2. Forest disturbance / change detection
Methods focused on change, alerts, or disturbance timing.

Examples of expected methods:
- annual change products (Hansen `lossyear`, GLAD alerts)
- BFAST and time-series breakpoint methods
- CCDC / continuous change detection
- Sentinel-1 SAR change detection

### 3. Time-series EO modeling
Methods using temporal sequences from Sentinel, Landsat, SAR, or fused stacks.

Examples of expected methods:
- harmonic / seasonal decomposition
- recurrent and transformer architectures over EO time series
- temporal CNNs and TempCNN family
- self-supervised representation learning over EO sequences

### 4. Weak supervision / noisy labels
Methods using annual, partial, or imperfect labels to train finer-grained targets.

Examples of expected methods:
- multi-instance learning with annual bag labels
- temporal disaggregation via latent state models
- co-training with cross-sensor agreement
- noisy-label-robust loss functions

### 5. Reproducible operational systems
Methods or codebases that can realistically seed repository implementation.

Examples of expected systems:
- Global Forest Watch processing chain
- SEPAL recipes
- `eo-learn` reference pipelines
- Sentinel Hub batch workflows

## GeoFM representations with local task models (SS-0002, 2026-10-19)

PUB-0003–PUB-0010 assess eight pretrained representation families as candidates for
v2/v3 experiments; none is integrated or locally validated. A foundation encoder plus
a locally trained spatial/temporal head is a distinct method from annual weak supervision
or deterministic anomaly confirmation. Feature fusion and prediction stacking are optional
experiments requiring independent blocked evaluation, not default architectural layers.
PUB-0011 supplies a transfer-evaluation reference. PUB-0012 is a pending full-text review
of land-change sampling/area guidance. See the
[evidence review](geofm_architecture_review_2026.md) and
[architecture assessment](../../docs/architecture.md).

## Notes

Populate each bucket with reviewed papers from `publications_inventory.csv`.
Cross-reference each entry by `id` (e.g., PUB-0001) and indicate roadmap fit.
