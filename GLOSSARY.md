# Glossary

Abbreviations and short names used in this repository, its README and the
[overview diagram](docs/img/problems-and-approaches.svg). Entries explain what a term means
here; the linked ADRs, specs and inventories remain the authoritative definitions.

Two abbreviations have more than one meaning in this repo — read them from context:

- **MAE** — *masked autoencoder* (a pretraining method, as in SatMAE or Scale-MAE) or
  *mean absolute error* (a regression metric).
- **F1** — *F1 score* (a classification metric) or *experiment arm F1* (one frozen GeoFM
  plus a small local head; see B0/B1/F1–F4).

## Repository conventions and identifiers

| Term | Meaning |
|---|---|
| ADR | Architecture Decision Record — a durable, numbered decision in `docs/adr/` (e.g. ADR 0004 on monthly targets). Accepted ADRs change only by a superseding ADR. |
| P1–P6 | The six canonical principles in `governance/principles.md`: P1 Research Protocol and Evidence Capture, P2 Data and Context Product Suitability, P3 External Source Code Discovery and Analysis, P4 Scientific Reverse Engineering of Source Code, P5 Independent and Composable Workstreams, P6 Architecture Drift Control. |
| v1 / v2 / v3 | Roadmap phases: v1 evidence-first forest baseline, v2 monthly confirmation from Sentinel time series, v3 weakly supervised monthly estimation. Specs live in `specs/`. |
| B0, B1, F1–F4 | Proposed experiment arms in `docs/architecture.md`: B0 current NDVI/SAR rules, B1 local model on raw features, F1 frozen GeoFM + local head, F2 controlled adaptation, F3 two-branch fusion or ensemble, F4 stacked meta-model. |
| DS-NNNN | Stable ID of a data source in `research/data_sources/inventory.csv` (e.g. DS-0002 Sentinel-2). |
| PUB-NNNN | Stable ID of a publication or practitioner source in `research/publications/publications_inventory.csv`. |
| CS-NNNN | Stable ID of an external codebase in `research/code_sources/inventory.csv`. |
| SS-NNNN | Stable ID of a declared search scope in `research/methodology/search_scopes.csv`. |
| PKG-NNNN | Stable ID of a software package in `research/packages/packages_matrix.csv`. |
| KG | Knowledge graph — the typed relationships generated from `knowledge/` into `graph/generated/knowledge.json`. |
| OKF | Open Knowledge Format — Markdown with YAML front matter and provenance; `knowledge/` follows an OKF-oriented profile, not full OKF conformance. |
| AOI | Area of interest — the geometry a run or study covers. |
| MMU | Minimum mapping unit — the smallest patch counted as forest or change under a forest definition. |
| QA | Quality assurance — e.g. per-month QA thumbnails or quality masks. |
| TBD | To be decided — a placeholder for a file or value not yet defined. |
| PR | Pull request. |
| CI | Continuous integration — the GitHub Actions checks in `.github/workflows/ci.yml`. |

## Geospatial reference systems and formats

| Term | Meaning |
|---|---|
| CRS | Coordinate reference system. |
| EPSG | Registry of CRS codes (originally the European Petroleum Survey Group). **EPSG:4326** is WGS 84 longitude/latitude, used here for exchange; **EPSG:6933** is the global EASE-Grid 2.0 equal-area CRS, used for area computation (ADR 0003). |
| WGS 84 | World Geodetic System 1984 — the datum behind EPSG:4326 and GPS coordinates. |
| EASE-Grid | Equal-Area Scalable Earth Grid, maintained by NSIDC. |
| GeoJSON | JSON-based format for vector geometries; an accepted AOI input. |
| WKT | Well-Known Text — a text encoding of geometries; an accepted AOI input. |
| GeoTIFF / COG | Georeferenced TIFF raster / Cloud Optimized GeoTIFF, a GeoTIFF laid out for efficient HTTP range reads. |
| GeoParquet | Apache Parquet with a standard geometry encoding; used for queryable vector and catalogue data. |
| STAC | SpatioTemporal Asset Catalog — a specification for searchable catalogues of EO scenes and assets. |
| GDAL | Geospatial Data Abstraction Library — the core raster/vector I/O and warping library. |
| JSON / YAML / CSV | Data and configuration file formats used for manifests, configs and inventories. |
| SHA-256 | Cryptographic hash used for geometry hashes, checksums and graph revisions. |
| UTC | Coordinated Universal Time — the timestamp basis for provenance records. |

## Earth observation, sensors and indices

| Term | Meaning |
|---|---|
| EO | Earth observation. |
| SAR | Synthetic aperture radar — active microwave imaging that sees through cloud (Sentinel-1). |
| VV / VH | SAR polarisations: vertical transmit/vertical receive and vertical transmit/horizontal receive. |
| GRD | Ground Range Detected — the Sentinel-1 product level used in v2. |
| RTC | Radiometric terrain correction — SAR backscatter normalised for terrain effects. |
| MSI | MultiSpectral Instrument — the optical sensor on Sentinel-2. |
| L1C / L2A | Sentinel-2 processing levels: top-of-atmosphere (L1C) and surface reflectance (L2A). |
| SCL | Scene Classification Layer — the Sentinel-2 L2A per-pixel class layer used for cloud/shadow masking. |
| NDVI | Normalized Difference Vegetation Index. |
| NDMI | Normalized Difference Moisture Index. |
| EVI | Enhanced Vegetation Index. |
| GSD | Ground sampling distance — the ground size of a pixel. |
| RGB | Red, green and blue image bands. |
| HLS | Harmonized Landsat Sentinel-2 — NASA's harmonised 30 m surface-reflectance product (L30 from Landsat, S30 from Sentinel-2). |
| MODIS | Moderate Resolution Imaging Spectroradiometer; **MOD13Q1** is its 250 m, 16-day vegetation-index product. |
| GEDI | Global Ecosystem Dynamics Investigation — spaceborne lidar measuring canopy height and structure in sparse footprints. |
| ICESat-2 | Ice, Cloud and land Elevation Satellite-2 — spaceborne lidar. |
| ISS | International Space Station — the GEDI platform, which limits GEDI's latitude coverage. |
| NFI | National Forest Inventory — field-plot-based national forest statistics. |

## Forest datasets and products

| Term | Meaning |
|---|---|
| GFC | Global Forest Change — the Hansen/UMD product with tree cover and annual `lossyear`; v1 baseline and v3 weak supervision only (never monthly truth). |
| GLAD | Global Land Analysis and Discovery lab at UMD, and its forest-disturbance alerts. |
| TMF | Tropical Moist Forests — the JRC product on tropical forest change. |
| PRODES | Brazil's satellite deforestation monitoring programme for the Legal Amazon, run by INPE. |
| CCI | ESA Climate Change Initiative (e.g. CCI Land Cover). |
| FRA | Global Forest Resources Assessment, published by FAO. |
| GFW | Global Forest Watch — an online forest-monitoring platform and processing chain. |

## Organisations, platforms and tools

| Term | Meaning |
|---|---|
| GEE / EE | Google Earth Engine (`ee` is its API namespace). Optional reference/research backend only (ADR 0005). |
| ESA | European Space Agency. |
| NASA | US National Aeronautics and Space Administration. |
| USGS | United States Geological Survey. |
| UMD | University of Maryland (Hansen/GLAD products). |
| JRC | Joint Research Centre of the European Commission. |
| INPE | Brazil's National Institute for Space Research. |
| FAO | Food and Agriculture Organization of the United Nations. |
| NSIDC | US National Snow and Ice Data Center. |
| LP DAAC | Land Processes Distributed Active Archive Center — NASA's archive for HLS and other land products. |
| CMR | NASA's Common Metadata Repository — the search API behind Earthdata. |
| SEPAL | FAO's System for Earth Observation Data Access, Processing and Analysis for Land Monitoring. |
| SNAP | ESA's Sentinel Application Platform. |
| OTB | Orfeo ToolBox — open-source remote-sensing processing library. |
| MCP | Model Context Protocol — the standard by which coding agents connect to external tools and data (see `docs/agents.md`). |
| API | Application programming interface. |
| HTML / URL | Web page markup / web address. |
| CC BY / MIT | Open licences: Creative Commons Attribution and the MIT software licence. |

## Machine learning and foundation models

| Term | Meaning |
|---|---|
| AI / ML | Artificial intelligence / machine learning. |
| LLM | Large language model. |
| GeoFM | Geospatial foundation model — a large model pretrained on EO data whose features feed local task heads. Used as the model-class name. |
| GFM | The specific model of Mendieta et al. (ICCV 2023), pretrained on GeoPile; not a synonym for GeoFM. |
| MAE | Masked autoencoder — self-supervised pretraining by reconstructing hidden image patches (see also *mean absolute error* under metrics). |
| DOFA | Dynamic One-For-All — a GeoFM with wavelength-conditioned patch embedding for heterogeneous sensors. |
| SatMAE / Scale-MAE | MAE-based GeoFMs for temporal/multispectral imagery and scale-aware (GSD-aware) imagery respectively. |
| SpectralGPT | A spatial–spectral GeoFM for multispectral imagery. |
| Prithvi-EO-2.0 | NASA/IBM multitemporal GeoFM pretrained on HLS. |
| Clay | Clay Foundation's multisensor GeoFM. |
| TESSERA | GeoFM producing pixel-level Sentinel-1/2 time-series embeddings, released as annual 10 m products. |
| GEO-Bench | A benchmark for evaluating transfer of EO foundation models. |
| BFAST | Breaks For Additive Season and Trend — time-series breakpoint detection. |
| CCDC | Continuous Change Detection and Classification. |
| CNN / TempCNN | Convolutional neural network / temporal CNN for EO time series. |
| HMM | Hidden Markov model. |
| RF | Random forest classifier. |
| GPU / CPU | Graphics / central processing unit. |

## Evaluation metrics

| Term | Meaning |
|---|---|
| F1 | F1 score — harmonic mean of precision and recall (see also experiment arm F1). |
| IoU | Intersection over union — overlap between predicted and reference areas. |
| PR-AUC | Area under the precision–recall curve. |
| RMSE | Root mean square error. |
| MAE | Mean absolute error (see also *masked autoencoder*). |

## Publication venues and identifiers

| Term | Meaning |
|---|---|
| DOI | Digital Object Identifier for publications. |
| CVPR / ICCV / ECCV | Computer vision conferences (Computer Vision and Pattern Recognition; International / European Conference on Computer Vision). |
| CVF | Computer Vision Foundation — hosts CVPR/ICCV open-access papers. |
| NeurIPS | Conference on Neural Information Processing Systems. |
| IEEE | Institute of Electrical and Electronics Engineers. |
| TPAMI | IEEE Transactions on Pattern Analysis and Machine Intelligence. |
| TGRS | IEEE Transactions on Geoscience and Remote Sensing. |
| IGARSS | IEEE International Geoscience and Remote Sensing Symposium. |
| ISPRS | International Society for Photogrammetry and Remote Sensing. |
| RSE | *Remote Sensing of Environment* (journal). |
| EGU | European Geosciences Union. |
| ESSOAr | Earth and Space Science Open Archive (preprint server). |
