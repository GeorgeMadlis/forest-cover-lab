# GeoFM evidence for the architecture assessment

Review date: **2026-10-19**. Search scope: **SS-0002** in
[`search_scopes.csv`](../methodology/search_scopes.csv). Consumer:
[`docs/architecture.md`](../../docs/architecture.md). This is a targeted architecture
review, not a systematic review, checkpoint audit or local performance benchmark.

## Question and protocol

Determine how Clay, Prithvi, DOFA, SatMAE, Scale-MAE, SpectralGPT, GFM and TESSERA could
support local forest state/disturbance models within the existing four-plane architecture,
and which evidence is needed before claiming monthly or operational accuracy.

Search original papers, author repositories/documentation and official data documentation;
exclude marketing, generic model lists, unrelated namesakes and secondary summaries as
evidence of model performance. Date range: 2013 through 2026-10-19. Stop after locating
primary references for all eight families, a transfer-evaluation reference and land-change
validation guidance, and documenting input/timing/evaluation gaps. This bounds the search;
it does not establish exhaustive coverage of newer GeoFMs.

Web searches used family names plus `paper`, `arxiv` or author domains. Representative
queries, including unsuccessful/ambiguous ones:

| Query / refinement | Outcome |
|---|---|
| `Clay geospatial foundation model paper arxiv`; `Clay site:clay-foundation.github.io/model/` | Author model specification; unrelated 3D CLAY excluded |
| `Prithvi EO 2.0 foundation model paper`; `Prithvi-EO-2.0 site:arxiv.org` | Primary multitemporal model paper; weather/climate Prithvi excluded |
| `DOFA Dynamic One For All remote sensing foundation model paper`; `Neural Plasticity-Inspired arxiv.org/abs` | Original DOFA paper and revision; DOFA-CLIP excluded from this comparison |
| `SatMAE arxiv`; `Scale-MAE arxiv`; `SpectralGPT arxiv` | Original papers and full HTML versions |
| `GFM Remote Sensing Foundation Model Wang 2023`; `Towards Geospatial Foundation Models Mendieta` | Generic acronym initially ambiguous; resolved provisionally to Mendieta's GFM/GeoPile |
| `Tessera global geospatial embeddings paper`; `TESSERA Temporal Embeddings arxiv` | Original paper, CVPR 2026 record and author repository |
| `GEO-Bench arxiv.org/abs`; `GEO-Bench Toward Foundation Models for Earth Monitoring` | Earth-monitoring paper; generative-engine-optimization namesake excluded |
| `Good practices estimating area Olofsson 2014`; author/publisher searches | DOI and author-repository abstract located; full validation-method audit deferred |
| `Harmonized Landsat Sentinel 2 HLS S30 L30 30m site:earthdata.nasa.gov` | NASA product documentation and data identifiers |

Access limits: several direct CVF PDF/DOI/legacy NASA URLs failed. arXiv HTML was accessible
for the model methods; Clay is assessed from author technical documentation, not presented
as a peer-reviewed model paper. Olofsson's good-practice recommendations were available in
the indexed author-repository abstract; direct retrieval failed. Its inventory entry
remains `to_review` pending full-text methods review. No source code or weights were
downloaded, no license audit performed and no model run attempted. Live repository pages
can contain newer releases: pin a dated commit and checkpoint in an implementation study.

## Primary evidence and extraction limits

The architecture's model table contains the capability-to-use interpretation. The following
records identify the supporting source and the reading boundary. All proposed forest
applications and experiment priorities are our architectural inferences, not author claims
of accuracy on the unspecified user AOI.

| Inventory ID | Verified reference and source type | Material consulted / bounded conclusion |
|---|---|---|
| **PUB-0003** | Clay Foundation, **Pretrained Model release v1.5**, weights released 2024-11-19. [Author technical specification](https://clay-foundation.github.io/model/release-notes/specification.html) | Summary, components, inputs, normalization and limitations. An embedding component is documented; its MAE reconstruction loss is not a forest-loss accuracy metric. |
| **PUB-0004** | Szwarcman et al., **Prithvi-EO-2.0: A Versatile Multi-Temporal Foundation Model for Earth Observation Applications**, original preprint 2024, [v3, 2026-03-06](https://arxiv.org/html/2412.02732v3) | III-A–C and IV-A: HLS sampling, band contract, task heads and evaluation design. Published transfer results justify a local experiment, not a local accuracy forecast. |
| **PUB-0005** | Xiong et al., **Neural Plasticity-Inspired Multimodal Foundation Model for Earth Observation**, original preprint 2024, [v3, 2025-10-15](https://arxiv.org/html/2403.15356v3) | Sections 3–4: wavelength-conditioned architecture, continual pretraining, DOFA versus DOFA+ and benchmark tasks. Treat a chosen variant as a separate experiment. |
| **PUB-0006** | Cong et al., **SatMAE: Pre-training Transformers for Temporal and Multi-Spectral Satellite Imagery**, NeurIPS 2022. [Paper v2](https://arxiv.org/html/2207.08051v2) | Sections 4–5: separate temporal and spectral constructions and task evaluation. Combined temporal/multispectral capability must be checked against a specific checkpoint. |
| **PUB-0007** | Reed et al., **Scale-MAE: A Scale-Aware Masked Autoencoder for Multiscale Geospatial Representation Learning**, ICCV 2023. [Paper v4](https://arxiv.org/html/2212.14532v4) | Methods and experiments: scale encoding, reconstruction and transfer tasks. Scale robustness is evidence for a comparator, not evidence of monthly event timing. |
| **PUB-0008** | Hong et al., **SpectralGPT: Spectral Remote Sensing Foundation Model**, IEEE TPAMI 2024, [DOI 10.1109/TPAMI.2024.3362475](https://doi.org/10.1109/TPAMI.2024.3362475). [Paper v3](https://arxiv.org/html/2311.07113v3) | Architecture and downstream task sections: spatial–spectral tokens and task-specific evaluation. Spectral tokenization is not equivalent to temporal localization. |
| **PUB-0009** | Mendieta, Han, Shi, Zhu and Chen, **Towards Geospatial Foundation Models via Continual Pretraining**, ICCV 2023, pp. 16806–16816. [Proceedings record](https://openaccess.thecvf.com/content/ICCV2023/html/Mendieta_Towards_Geospatial_Foundation_Models_via_Continual_Pretraining_ICCV_2023_paper.html), [full HTML v3](https://arxiv.org/html/2302.04476v3) | Sections 3–4: GeoPile, teacher/student objective and spatial downstream tasks. Proper-name GFM is distinguished from the generic acronym. |
| **PUB-0010** | Feng et al., **TESSERA: Temporal Embeddings of Surface Spectra for Earth Representation and Analysis**, original preprint 2025, [v6, 2025-11-19](https://arxiv.org/html/2506.20380v6); [CVPR 2026 proceedings version](https://openaccess.thecvf.com/content/CVPR2026/papers/Feng_TESSERA_Temporal_Embeddings_of_Surface_Spectra_for_Earth_Representation_and_CVPR_2026_paper.pdf) | Sections 3–5 and inference-window discussion. The paper discusses shorter seasonal inference windows; this is not validation of monthly causal disturbance inference or equivalence with annual downloaded products. |
| **PUB-0011** | Lacoste et al., **GEO-Bench: Toward Foundation Models for Earth Monitoring**, 2023. [Paper v2](https://arxiv.org/html/2306.03831v2) | Benchmark and evaluation methodology: useful controlled transfer protocol, with task-specific interpretation required. Generic benchmark rank cannot validate monthly forest disturbance. |
| **PUB-0012** | Olofsson, Foody, Herold, Stehman, Woodcock and Wulder, **Good practices for estimating area and assessing accuracy of land change**, RSE 148 (2014), 42–57, DOI **10.1016/j.rse.2014.02.015**. [Author-repository record](https://nottingham-repository.worktribe.com/output/728216/good-practices-for-estimating-area-and-assessing-accuracy-of-land-change) | Abstract-level guidance only: probability sampling, response design, design-consistent area/error estimates and intervals. Full estimator selection and audit remain pending. |

Architecture-review scores are deliberately separate from experimental evidence. For the
eight model references, label match is only 1/3: none supplies independently validated
monthly disturbance labels for the user's unspecified AOI. Reproducibility is 2/3 because
public artifacts are identified but not executed/audited. Codeability scores reflect
method description, not verified software quality. No candidate reaches the shortlist's
12-point threshold. These scores must be revisited after a checkpoint/code review; they
are not an accuracy ranking.

## Data and code follow-up

**DS-0014** records HLS separately from raw Sentinel-2 and Landsat sources. Official
[NASA data access guidance](https://git.earthdata.nasa.gov/projects/LPDUR/repos/hls-tutorial/commits/e0bed93b067fa22d06c38aa2d119149bd05a5693)
identifies L30/S30 v2; exact collections, quality processing and checkpoint compatibility
remain pilot choices. **DS-0015** records original TESSERA annual embeddings as an auxiliary
feature family; the [author repository](https://github.com/ucam-eo/tessera) is an access and
version-discovery route, not an immutable artifact. Neither candidate is a validated
monthly label. Both require AOI/year, version, access, latency and terms review before use.

Code entries **CS-0002–CS-0009** are discovery records only (`to_review`), linked to their
model references; **CS-0010** records the GEO-Bench evaluation implementation. P4 reverse
engineering is still required for any selected implementation:
input product/units, band order, scaling/masks, temporal context, token support, head,
checkpoint provenance, evaluation splits and paper-to-code divergences. Do not infer
commercial suitability from a paper, an "open" label or a third-party mirror.

## Synthesis and unresolved evidence

The existing framework has the right separation of question, observations, methods,
execution and provenance. Its gap is a reviewed contract connecting a concrete pretrained
model to a locally trained task head and an independent evaluation. The proposed path is
raw-feature baseline → one frozen encoder/head → controlled adaptation or fusion → optional
agent evaluation. Each arrow is conditional on evidence, not a requirement to build all
levels.

Still required before implementation/adoption:

- AOI, dates, forest/disturbance target and practical error/latency/cost objectives.
- A dated, independently sampled local reference set and an event-time annotation protocol.
- Pinned checkpoint/code/weights and input compatibility, license and compute checks.
- A pilot reporting local metrics and uncertainty, including failure/missingness strata.
- A separate justification for an agent over scheduled deterministic workflows; none of
  these model papers validates an autonomous legal/notification/recovery operator.

No local result, performance uplift, legal finding or operational readiness claim is made
by this review. No knowledge-graph relationship is promoted by this assessment.
