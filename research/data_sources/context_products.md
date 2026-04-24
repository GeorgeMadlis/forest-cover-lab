# Adjacent Context Products

Forest Cover Lab focuses on forest cover estimation. Adjacent Earth-observation products are
included only when they can improve interpretation, validation, transferability, uncertainty
assessment, or AOI-specific risk analysis.

## Why this exists

Forest estimates can be misread when surrounding context is ignored. Flooding can change SAR
backscatter, biodiversity layers can highlight ecological stakes, integrity indices can
explain landscape pressure, and energy or infrastructure products can explain land-use
conversion risk. These products are useful, but they are not forest-cover ground truth.

## Context domains

| Domain | How it can help | Main risk |
|---|---|---|
| Biodiversity | Identify ecological stakes, protected areas, habitat or intactness context | Being mistaken for canopy or forest condition |
| Ocean/coastal | Support mangrove, estuary, shoreline, and coastal forest interpretation | Irrelevant for inland AOIs unless explicitly justified |
| Renewable energy | Explain solar, wind, transmission, or infrastructure pressure near forest areas | Turning land-pressure context into forest evidence |
| Environmental integrity | Provide landscape pressure or ecosystem condition context | Index components may already include land cover, causing circular reasoning |
| Floods and water | Explain inundation, wetland signals, optical anomalies, and SAR anomalies | Temporary water can be confused with disturbance or non-forest |
| Fire and climate | Explain disturbance, drought stress, recovery context, and seasonal risk | Coarse products may overstate local causality |
| Land use and access | Explain agriculture, roads, settlements, mining, or concessions near forest | Pressure layers are explanatory, not validation labels |

## Admission rules

- Record each product in `inventory.csv` with `evidence_role`, `domain`, `forest_relevance`,
  and `source_priority`.
- Use `interpretation-only background` when a product supports report narrative but should
  not influence raster classification.
- Use `context/risk layer` when a product can explain uncertainty, anomalies, or likely
  future pressure.
- Use `auxiliary feature` only when the product can be plausibly used by an algorithm and
  its semantics do not leak target labels.
- Use `validation reference` only when temporal, spatial, and semantic alignment with the
  forest-cover target is documented.

## Rejection rules

Reject or defer a context product if:

- Its license or access route is unclear.
- It cannot be tied to a forest-cover interpretation or validation question.
- Its spatial or temporal resolution is too coarse for the intended claim.
- It duplicates a component already used in another index, creating circular evidence.
- It would encourage a report to make claims beyond forest cover estimation.

