# Packages Notes

Use this file for qualitative notes that do not fit cleanly into the comparison matrix.

## Suggested structure per package

```
### Package name
- strengths
- weaknesses
- dependencies
- likely role in repo
- risks
- migration or replacement concerns
```

---

### Google Earth Engine (PKG-0001)

- **Strengths:** global Landsat + Sentinel + Hansen GFC archives, JS and Python APIs, scalable server-side compute.
- **Weaknesses:** non-commercial quota tiers from 27 April 2026; vendor lock-in; export latency for large AOIs.
- **Dependencies:** Google account + EE registration.
- **Likely role:** v1 baseline prototyping, AOI inspection, Hansen tile export.
- **Risks:** quota limits binding production runs; need a documented fallback to local GDAL pipeline.
- **Migration concerns:** algorithms expressed in EE JS/Python idioms do not port cleanly to local stacks.

### geemap (PKG-0002)

- **Strengths:** Pythonic EE wrapper, interactive map widgets, integrates with notebooks.
- **Weaknesses:** notebook-coupled state if used carelessly; depends on EE.
- **Likely role:** v1 baseline scripts and exploratory notebooks.
- **Risks:** inherits EE quota risk.

### GDAL / Rasterio / rioxarray (PKG-0003, PKG-0004, PKG-0005)

- **Strengths:** local, reproducible, well-maintained, Python-friendly.
- **Weaknesses:** less suited for global-scale processing without orchestration.
- **Likely role:** local clipping, reprojection, area computation, COG export, QA, validation tests.
- **Risks:** none material for v1; xarray integration is essential for v2 monthly stacks.

### SEPAL (PKG-0006)

- **Strengths:** FAO-hosted, institutional, designed for forest workflows.
- **Weaknesses:** less Python-native than EE+geemap; harder to script outside the platform.
- **Likely role:** fallback if EE quota binds; institutional collaboration.

### Orfeo ToolBox (PKG-0007) and SNAP (PKG-0008)

- **Strengths:** mature, scientifically validated, strong Sentinel processing (especially SAR for SNAP).
- **Weaknesses:** heavier installation footprint; slower to iterate than Python-only stacks.
- **Likely role:** v2 SAR preprocessing (SNAP); v2/production classification (OTB).

### eo-learn (PKG-0009)

- **Strengths:** ML-friendly, time-series-aware EO pipeline framework.
- **Likely role:** v3 research stack.
- **Risks:** moving target; community-maintained.

### sentinelhub-py (PKG-0010)

- **Strengths:** programmatic Sentinel access independent of EE.
- **Weaknesses:** commercial component; pricing affects fallback economics.
- **Likely role:** EE alternative for Sentinel data access in v2.

### Global Forest Watch (PKG-0011)

- **Strengths:** authoritative reference layers; well-documented.
- **Likely role:** reference-only cross-check; not primary processing logic.
- **Risks:** must not be used as the single source of truth.
