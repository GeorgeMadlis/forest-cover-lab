# Research Guide

This guide defines the protocol for all knowledge acquisition in Forest Cover Lab.
Following it makes the research process reproducible and auditable.

---

## Step 0 — Declare a search scope before starting

Record the following before reading or searching anything:

| Field | Description |
|---|---|
| `objective` | One sentence: what question are you trying to answer? |
| `source_types` | Which types will you search? (papers / blogs / code / data) |
| `keywords` | The exact terms you will use |
| `date_range` | Temporal window (e.g. 2010–2026) |
| `databases_or_platforms` | Where you will search (see lists below) |
| `stopping_criterion` | When will you consider the search complete? |

Record this scope in `research/methodology/search_scopes.csv` before the first result is
entered. Inventories should reference the relevant `search_scope_id` when practical.

---

## Finding academic papers

**Primary databases:**
- Google Scholar — broad coverage, citation graph
- Semantic Scholar — semantic search, citation context
- IEEE Xplore — TGRS, IGARSS proceedings
- arXiv — preprints in cs.CV and eess.SP

**Key journals for this domain:**
- *Remote Sensing of Environment*
- *IEEE Transactions on Geoscience and Remote Sensing*
- *ISPRS Journal of Photogrammetry and Remote Sensing*
- *International Journal of Remote Sensing*
- *Forest Ecology and Management*
- *Global Change Biology*

**Key conferences:**
- IGARSS — IEEE International Geoscience and Remote Sensing Symposium
- ESA Living Planet Symposium
- ECCV / CVPR / NeurIPS — for deep learning methods in remote sensing

---

## Finding technical reports and dataset documentation

| Source | What to search for |
|---|---|
| FAO Global Forest Resources Assessment | Forest area definitions, country-level data |
| JRC European Commission | Global Forest Cover, TMF dataset, GFC methodology |
| INPE PRODES | Brazil deforestation methodology |
| GEE Dataset Catalog | Data provenance, product specifications (not algorithm discovery) |
| Hansen / GLAD lab (UMD) | GFC updates, GLAD alerts methodology |

## Finding adjacent Earth-observation context products

Adjacent products are searched when they help interpret, validate, or bound forest-cover
estimates. They are not searched as a separate mission. Record them in
`research/data_sources/inventory.csv` with `evidence_role = context/risk layer`,
`auxiliary feature`, `validation reference`, `exclusion mask`, or
`interpretation-only background`.

| Domain | Examples of useful searches |
|---|---|
| Biodiversity | habitat intactness, species richness, ecosystem integrity, protected areas |
| Ocean/coastal | mangrove context, coastal change, ocean color, shoreline or estuary products |
| Renewable energy | solar resource layers, wind resource layers, transmission or infrastructure context |
| Integrity indices | environmental integrity index, ecosystem integrity, human footprint |
| Floods and water | flood extent, surface water seasonality, wetland inundation |
| Fire and climate | burned area, drought, precipitation, temperature, reanalysis data |
| Land use and pressure | agriculture, roads, settlements, mining, concessions |

For each context product, record the forest relevance explicitly. A product can be useful
background without being suitable as a forest-cover input.

---

## Finding practitioner blogs and developer posts

See `practitioner_sources.md` for a curated list of sources to monitor.

When reading a blog post:

1. Note the publication date and author affiliation.
2. Record whether it references a peer-reviewed paper or represents standalone practitioner
   knowledge.
3. Record any data sources, platforms, or methods mentioned.
4. Note any code links.
5. Classify it in the publications inventory as `venue_type = blog` or
   `venue_type = technical_report` — never as a journal article.

---

## Reading a paper

When reading a paper for this repository, evaluate in this order:

1. **Forest definition**: what threshold, what sensor, what temporal interpretation?
2. **Label semantics**: are labels annual, seasonal, or monthly? Human annotation or
   derived from another product? If from annual products, is weak supervision acknowledged?
3. **Code availability**: is there a repository? Is it usable? Record the URL.
4. **Reproducibility signals**: is data publicly available? Are hyperparameters reported?
5. **Operational relevance**: can this method run at AOI scale within reasonable compute?

Score all five dimensions in `publications_inventory.csv` immediately after reading.
Do not defer scoring.

---

## Stopping criteria

Stop a search when any of the following applies:

- Three consecutive searches with varied keywords return no new candidate entries.
- You have covered all source types declared in the search scope.
- You have reached the declared date-range boundary.
- You have reached the entry limit declared in the scope (if any).

Record the stopping criterion that applied in the scope record alongside the final entry.

---

## Cross-track triggers

While conducting literature research, you may discover:

- A data source not yet in `research/data_sources/inventory.csv` → add it there.
- A codebase not yet in `research/code_sources/inventory.csv` → add it there.
- A codebase worth deep analysis → create a reverse engineering artifact in
  `research/code_sources/analysis/<repo_name>/`.

These are independent contributions. You do not need to complete the publication review
first.
