# Architecture Assessment

This document records the current architecture view for Forest Cover Lab. It is not a
decision record; durable choices still belong in `docs/adr/`.

**GeoFM assessment updated: 2026-10-19.** The GeoFM design below is a research proposal,
not an accepted model choice or an implemented capability. Primary evidence and review
limits are recorded in the [GeoFM evidence review](../research/publications/geofm_architecture_review_2026.md).

## Architecture intent

Forest Cover Lab is a governance, research, and evidence registry for forest-cover work
from satellite data. The architecture must support three parallel jobs:

1. Govern downstream implementation repositories through shared scientific contracts.
2. Explain why datasets, methods, codebases, and
   scientific claims were accepted, rejected, or deferred.
3. Collect reusable data-source assessments that downstream repos can consume by stable ID.

Adjacent Earth-observation domains are intentionally in scope as context. Biodiversity,
ocean/coastal, renewable energy, environmental integrity, flood, fire, climate, and land-use
products can inform interpretation, validation, or risk assessment. They must not become a
second mission that distracts from forest cover estimation.

## Current strengths

- The repo already separates research evidence, specifications, validation, reporting, and
  ADRs (Architecture Decision Records). That is the right high-level separation for a scientific geospatial project.
- The v1/v2/v3 roadmap is useful because it distinguishes a baseline estimate, monthly
  confirmation, and weakly supervised monthly estimation.
- The governance scaffold makes drift visible through principles, a checklist, and an audit
  log instead of leaving architecture rules implicit.
- The code-discovery and reverse-engineering tracks correctly treat external source code as
  scientific evidence, not only as reusable software.
- The data-source inventory can act as a shared registry for narrow repos such as
  `sentinel-monthly-forest-cover` and `gedi-validation-lab`.

## Main gaps found

- The data-source architecture was too forest-product focused. It did not clearly model
  adjacent context products such as biodiversity, floods, integrity indices, oceans, or
  renewable energy surfaces.
- P1 required a search scope, but there was no concrete artifact where search scopes could
  be recorded once and referenced by inventories.
- The boundary between "core forest estimation input" and "background context" was not
  explicit enough, creating a risk that broad Earth-observation research could dilute the
  forest-cover mission.
- Track independence was stated, but downstream influence was not always explicit: a reader
  could not immediately see whether a track feeds ADRs, specs, reports, validation, or only
  notes.
- There was no single architecture assessment document tying the six principles to the
  repository layout.
- Downstream repository expectations were implicit rather than documented as a contract.

## Target architecture

| Section | Governing principle | Main location | Purpose |
|---|---|---|---|
| Research protocol | P1 | `research/methodology/` | Search scopes, reading protocol, practitioner sources |
| Publications and practitioner knowledge | P1 | `research/publications/` | Papers, reports, blogs, method synthesis |
| Data and context products | P2 | `research/data_sources/` | Satellite, in situ, fusion, and adjacent EO context suitability |
| External source code discovery | P3 | `research/code_sources/inventory.csv` | Catalogue external implementations as evidence |
| Scientific reverse engineering | P4 | `research/code_sources/analysis/` | Explain scientific reasoning embedded in selected code |
| Specifications | P5 | `specs/` | Phase-specific algorithm contracts |
| Decisions | P5, P6 | `docs/adr/` | Durable accepted or proposed decisions |
| Validation and reporting | P5, P6 | `validate/`, `report/` | Make claims testable, bounded, and reproducible |
| Downstream contracts | P5, P6 | `docs/downstream_repos.md` | Define how narrower repos consume this repo |
| Drift control | P6 | `governance/` | Keep the repo aligned with the mission and principles |

## Architectural rules

- Forest cover estimation remains the primary objective.
- Adjacent Earth-observation products enter through `research/data_sources/` as context
  products with an explicit `evidence_role`, `domain`, and `forest_relevance`.
- Every inventory row should reference a search scope where practical.
- Every material claim should be traceable from report/spec/ADR back to evidence in
  `research/`.
- Downstream repos should reference this repo by commit or release and cite the data-source
  IDs, ADRs, schemas, and reporting contracts they consume.
- Tooling comparisons stay in `research/packages/`; datasets and products stay in
  `research/data_sources/`; external implementations stay in `research/code_sources/`.
- Reverse-engineering artifacts must explain scientific reasoning, assumptions, limitations,
  and paper-to-code divergence, not just list files and functions.

## Semantic architecture (ADR 0005)

The semantic/scientific plane is the human-maintained `knowledge/` corpus plus existing
specs, governance and evidence assessments. `graph/` contains ontology, typed relationships,
schemas and a deterministic generator; `graph/generated/knowledge.json` is derived.
The executable software plane belongs to downstream repositories. Live observation
catalogues (STAC, GeoParquet, provider services) resolve scenes at runtime. The provenance
plane records planning, selected inputs, versions, parameters, limitations and results in
run manifests and evidence bundles. These four planes have separate authorities.

The conceptual flow is:

```text
Application → Scientific question → Method → Observation requirements
→ Measurements/variables → Candidate datasets → Access mechanisms
→ Processing/tool capabilities → Executable workflow → Validation → Evidence/result
```

This is a discovery sequence, not an assertion that every record forms a complete linear
path. Datasets satisfy observation requirements subject to scale, geography, quality and
semantic compatibility. Capabilities describe software operations; workflows implement
methods partially or fully and must declare divergence. Run-specific evidence/results are
outside the graph. `knowledge/README.md` defines each concept layer and its directory.

Candidate and validated edges are separate output collections. AI-generated proposals cannot
become canonical through deterministic checks alone or a single run. Contract transcriptions
have explicit attribution; seasonal method decisions remain candidates requiring review.
The revision hashes corpus, cited local contracts and graph rules; Git commits/tags are pinned
separately. Review-after deadlines are consumer checks, not nondeterministic build behavior.

Production methods must not require GEE. ADR 0005 supersedes ADR 0001's platform default;
GEE acquisition in existing phase specs is a reference route, preserving scientific rules.
The repo needs only lightweight local validation dependencies, with optional backend extras.
No graph service, execution engine or observation archive is introduced.

## GeoFMs in the current framework

**None of the eight named model families is currently integrated or locally benchmarked
in this repository's registered framework.** The v3 specification describes latent temporal
models without choosing a pretrained backbone. The registered Sentinel workflow describes
NDVI anomalies, SAR confirmation, compositing and seasonal comparisons; it registers no
GeoFM encoder, trained local head or model ensemble. Some persistence/confirmation
relationships are target-only, as their workflow edge scopes explicitly state. Local
contract tests establish reference integrity, not model accuracy or scientific equivalence.

The architecture can accommodate GeoFMs by separating pretrained representations, local
task learning and workflow execution. Most base checkpoints produce features or
reconstructions. A claim such as "40% canopy loss" additionally requires a trained task
head, a defined denominator and time interval, quality control and validation. A model
family name alone specifies none of these.

Here **GeoFM** denotes the model class. **GFM (Mendieta et al.)** denotes the particular
GeoPile/continual-pretraining model, the working interpretation of the ambiguous name in
the request. "Global" describes pretraining scope, not guaranteed local validity. The
comparison below uses identifiable reference releases, not an assertion that each is the
latest or preferred checkpoint.

| Family / reference | Relevant published capability | Proposed place in this framework | Compatibility limit / first experiment |
|---|---|---|---|
| **Clay v1.5** ([author specification](https://clay-foundation.github.io/model/release-notes/specification.html)) | Multisensor MAE with wavelength, ground sampling distance (GSD), location and time metadata; produces embeddings | Frozen optical/SAR features feeding a local classifier or change head | Match checkpoint preprocessing and sensor metadata; timestamp encoding does not itself produce monthly disturbance estimates. Compare one encoder + small head with raw-feature learning. |
| **Prithvi-EO-2.0** ([paper, methods III](https://arxiv.org/html/2412.02732v3)) | Multitemporal optical model pretrained on global 30 m HLS sequences | Temporal/spatial backbone with local segmentation or disturbance head | Its HLS spectral/normalization contract is distinct from arbitrary 10 m S2 stacks. Test HLS first; treat S2 adaptation as a separate arm. SAR requires a separate branch/fusion design. |
| **DOFA — Dynamic One-For-All** ([paper, methods 3](https://arxiv.org/html/2403.15356v3)) | Wavelength-conditioned patch embedding for heterogeneous sensors | Shared encoder candidate for optical/SAR features | Multisensor support does not establish calibrated sensor fusion or event timing. Pin original DOFA separately from DOFA+ and test sensor-ablation arms. |
| **SatMAE** ([paper, sections 4–5](https://arxiv.org/html/2207.08051v2)) | Temporal and multispectral MAE variants | Optical representation baseline; temporal variant where inputs match | Temporal and multispectral results concern distinct configurations; do not assume a released checkpoint combines both. Select the variant before constructing tensors. |
| **Scale-MAE / ScaleMAE** ([paper, sections 3–4](https://arxiv.org/html/2212.14532v4)) | GSD-aware representations and multiscale reconstruction, demonstrated with RGB imagery | Scale-aware optical comparator; possible orthophoto branch | No default SAR or monthly change semantics. Test scale transfer on compatible RGB inputs, retaining a separate multispectral baseline. |
| **SpectralGPT** ([paper, methods and experiments](https://arxiv.org/html/2311.07113v3)) | Spatial–spectral 3D tokens and reconstruction; downstream classification, segmentation and change tasks | Multispectral feature backbone with local change decoder | The token's third dimension is spectral; it does not establish a monthly temporal model. Audit band grouping and change-head implementation. |
| **GFM (Mendieta et al.)** ([ICCV 2023 paper](https://openaccess.thecvf.com/content/ICCV2023/html/Mendieta_Towards_Geospatial_Foundation_Models_via_Continual_Pretraining_ICCV_2023_paper.html)) | GeoPile and ImageNet-guided continual pretraining, evaluated on several spatial tasks including change detection | Historical spatial-pretraining comparator | Verify the selected released model's RGB/channel contract; do not interpret its name as a universal global optical/SAR temporal model. |
| **TESSERA / Tessera, original reference** ([paper, sections 3–5](https://arxiv.org/html/2506.20380v6)) | Pixel-level S1/S2 time-series embeddings; annual 10 m products and lightweight task heads | Efficient frozen-feature arm for retrospective forest-state mapping; prior-year contextual features for monthly work | Annual embeddings do not identify disturbance month. A full target-year embedding leaks future observations into an earlier alert. Short-window inference is a separate experiment, not equivalent to the annual product. |

These are suitability hypotheses. Published land-cover, crop, biomass, building or canopy
height results do not establish local forest-loss performance. Precomputed embeddings are
derived data products; model weights are model artifacts. Neither is a reference label.

## Six steps from question to estimated performance

### 1. Clarify the scientific and operational question

Use a written question contract before selecting a model. A concrete starting question is:

> Within a specified AOI and baseline forest mask, which locations experienced a
> stand-replacement disturbance during month m, what area was affected, and what evidence
> was available by the declared observation cutoff?

The AOI, dates, baseline/reference years, biome, forest definition, minimum mapping unit,
minimum detectable event size, reporting grid and latency budget remain unspecified by this
assessment. Set them in a downstream study plan rather than inferring a country or inventing
accuracy estimates. Specify whether the study is retrospective or simulates timely alerts;
publication/availability timestamps matter in the latter.

Keep the following targets distinct:

- **Forest state / area:** forest probability or class at time m under ADR 0002; canopy
  fraction regression is a different target and needs fractional reference measurements.
- **Disturbance:** evidence of a defined structural change, with an event interval and
  affected area; seasonal browning alone is insufficient.
- **Deforestation / cause / legality:** land-use conversion, attribution and legal status
  require additional evidence and jurisdiction-specific definitions. A disturbance map
  does not establish them.
- **Recovery:** a longitudinal target with its own baseline, observation schedule and
  independent assessment; renewed greenness alone does not prove forest recovery.

Output a georeferenced probability map, uncertainty/quality and no-observation masks, event
polygons where justified, area estimates and evidence links. Preserve ADR 0004: annual
Hansen supervision cannot establish monthly truth. Specify the meaning of any "40%"
claim: percentage of baseline forest area disturbed differs from a 40 percentage-point
change in canopy fraction.

### 2. Find and assess the publications

Search scope **SS-0002** covers the eight requested families plus evaluation methods.
The [evidence review](../research/publications/geofm_architecture_review_2026.md) records
primary references, sections read, search terms, inclusion limits and open questions.
Publications, code and dataset assessments remain separate tracks under P1–P4.

For each model extract its pretraining geography/years, sensor/product level, bands and
units, spatial support, temporal context, output representation, task head, labels, splits,
metrics, compute and artifact availability. Distinguish author results from our proposed
use. Inspect a pinned implementation before recommending adaptation: paper-to-code
divergence, padding, masks, normalization and checkpoint compatibility are scientific
issues as well as engineering issues. A relevant paper or passing import is insufficient
for promotion to a validated method.

Use [GEO-Bench](https://arxiv.org/html/2306.03831v2) as a reproducible transfer-evaluation
reference, with task-specific scores and training budgets. Add an independently labelled
local monthly benchmark; an average across unrelated tasks cannot answer this question.

### 3. Define the data sources and their roles

| Source | Role and relationship to existing registry | Required checks |
|---|---|---|
| **DS-0002 Sentinel-2 L2A** | Core optical observations; bands/indices and compatible encoder inputs | Band-native 10/20/60 m support, scale/offset, cloud/shadow/snow, valid coverage, registration and timestamps. Resampling to 10 m creates no new detail. |
| **DS-0003 Sentinel-1** | Core SAR observations and independent sensor branch | GRD versus RTC product, calibration/terrain correction, orbit/polarization/incidence angle, linear power versus dB, speckle treatment and missing coverage. A 10 m grid is not necessarily 10 m resolving power. |
| **DS-0014 HLS L30/S30 v2, candidate** | Checkpoint-aligned optical arm for Prithvi; related to DS-0002/0004 but a distinct harmonized product | [NASA HLS documentation](https://hls.gsfc.nasa.gov/); 30 m support, spectral mapping, quality flags, harmonization, selected collection/version and access. Do not substitute raw S2 band names without testing. |
| **DS-0015 TESSERA annual embeddings, candidate** | Derived auxiliary features consumed with a trained local head | Exact encoder/product revision, AOI/year coverage, complete source observation interval, release availability, grid and quantization/scales. For alerts use a prior-year product or validate causal re-inference. |
| **DS-0001 Hansen loss / baseline** | v1 baseline and v3 annual weak supervision / annual consistency | Pin release and forest definition; never use its training labels as independent test truth. Annual consistency and monthly accuracy are separate. |
| **DS-0006 GEDI; DS-0007 TMF; DS-0008 PRODES** | Potential structure or regional/annual comparison references | Footprint/date/geography and target match; GEDI does not cover all latitudes or all pixels. Independence must consider shared imagery, algorithms and labels. |
| **Dated orthophotos, airborne lidar, plots, national inventory and independently interpreted image sequences** | Candidate local validation references; select/register actual products once the AOI is known | Sampling design, date interval, class definitions, licensing, interpreter agreement and positional error. References used for training must be excluded from independent testing. |
| **Terrain, weather, fire/flood, land use, permits and protected boundaries** | Optional confounder/context evidence with an explicit role | Register the actual version/jurisdiction and date. Laws/permits are documentary evidence, not raster training truth or automatic legal conclusions. |

Provider routes in existing inventory rows are historical assessments, not current access
guarantees. Resolve scenes through live catalogues and pin asset IDs, checksums, licenses
and availability in run provenance. Prefer the open/cloud-neutral execution policy of ADR
0005. Keep reference labels and interpretation notes separate from features; retain
uncertain event-date intervals instead of assigning a fabricated exact month.

### 4. Define global backbones, local models and optional stacking

Start by reusing pretrained weights, rather than training a new global foundation model.
Separate four choices: backbone/checkpoint, sensor adapter/preprocessing, local task head,
and temporal decision rule. Train the head on local labels; optionally adapt the backbone
with a parameter-efficient method or full fine-tuning if held-out evidence warrants it.
Local means adapted to the target region/task, not inherently small or independent.

The proposed computation is:

```text
Question + observation cutoff + pinned contracts
  -> catalogue selection -> quality-controlled, aligned observations
  -> model-specific input adapters
       -> compatible pretrained encoder(s) -> features
       -> raw spectral/SAR/seasonal features --------+
  -> local spatial/temporal head <- quality/missingness
  -> calibrated probabilities -> fixed persistence/event rules
  -> map + no-observation mask + area/uncertainty + evidence bundle
```

A monthly local head can use current/reference embeddings, their differences, raw NDVI/
NDMI and SAR changes, observation ages/counts and season metadata. For an alert at t, every
feature and persistence decision must use data available by t. Backdated confirmation and
retrospective smoothing must be labelled accordingly. Missing data are not evidence of
stable forest. Patch/global pooled embeddings need a suitable spatial decoder before
pixel-level mapping; retain their effective support.

Compare these experimental arms on identical independent evaluation units:

| Arm | Construction | Purpose |
|---|---|---|
| B0 | Pinned current NDVI/SAR workflow with its actual implemented rules | Operational/scientific baseline; expose unimplemented target rules |
| B1 | Local logistic/RF/boosted-tree or small temporal model on raw features | Test whether pretrained representations add value beyond local learning |
| F1 | One frozen GeoFM + small local head | Lowest-complexity foundation-model experiment |
| F2 | Same backbone/head with controlled adaptation | Isolate adaptation benefit and label/compute cost |
| F3 | Two compatible feature branches + local fusion head, or calibrated prediction ensemble | Test complementary optical/SAR or scale evidence |
| F4 | Stack local predictions with a trained meta-model | Test extra ensemble benefit only after F1/F3 justify it |

Screen Clay, DOFA and Prithvi as alternative first encoders based on the selected inputs;
screen annual TESSERA features separately for retrospective/prior-year use. Keep SatMAE,
Scale-MAE, SpectralGPT and GFM as targeted comparators when their contracts match the
question. This is an input-fit and experiment-cost ordering, not an accuracy ranking.

Do not feed an encoder's arbitrary embedding vector into another encoder expecting
reflectance images. Feature concatenation needs spatial/temporal alignment, train-only
normalization and an explicit fusion layer. Prediction stacking needs **spatially and
temporally out-of-fold** base predictions to train the meta-model, with an untouched outer
test set; in-sample predictions leak labels. Do not average unrelated latent spaces.
No reason currently supports stacking all eight models. Global retraining/continual
pretraining is a later research project requiring data/compute justification and an ADR.

For v3, a possible annual bag model pools local monthly **event** probabilities to an
annual probability. A noisy-OR, `1 - product_m(1 - p_m)`, is one explicit assumption-dependent
choice; correlated months and repeated disturbances require checking it. Forest-state
probabilities need their own transition/observation model. Agreement with the annual
training product measures consistency, not independent accuracy.

### 5. Define performance metrics before training

Predeclare the primary metric and operating point from the question: for example event
recall at a fixed independently assessed precision and alert-review budget. Fix thresholds
on validation data, never the final test set. Overall accuracy alone obscures rare loss.

| Target | Report | Interpretation |
|---|---|---|
| Forest / disturbance map | Per-class precision (user's accuracy), recall (producer's accuracy), F1, IoU; PR-AUC for probabilities | Include class prevalence and sample/area weighting; report forest state and disturbance separately |
| Event detection | Event precision/recall, false alerts per area/time, recall by event size, boundary error | Predefine object matching, overlap and split/merge rules |
| Timing / alerts | Detection delay from independently bounded event interval, missed events, latency from acquisition to output | Monthly correctness requires dated references; report interval censoring and confirmation lag |
| Area | Mapped hectares plus reference-sample-adjusted area, bias and 95% confidence interval under ADR 0003 | [Probability sampling and design-consistent area/error estimation](https://nottingham-repository.worktribe.com/output/728216/good-practices-for-estimating-area-and-assessing-accuracy-of-land-change) are preferable to treating pixel counts as true area |
| Fractional canopy, if selected | MAE/RMSE and bias against independent fractional references | Binary mask metrics do not validate percentage canopy loss |
| Probability / abstention | Brier score, reliability plot, calibration error, risk versus retained coverage | Expose missingness, uncertain/no-observation area and performance after abstention |
| Transfer / robustness | Scores by biome, season, cloud/data-density stratum and sensor availability; new-region/new-year degradation | Aggregate scores must not hide poor performance in important strata |
| Cost / operations | Labels and review hours, preprocessing/encoder/head GPU or CPU hours, peak memory, storage, runtime and cost per area/month, failed jobs | Compare cached and uncached operation; a faster head may hide expensive embedding generation |

Keep the existing v3 annual-consistency tolerance and minimum manual review as contract
checks, not substitutes for statistical evaluation. Recovery and legal-document workflows
need separate task-specific references and metrics; detection F1 does not validate them.

### 6. Estimate performance with a local, reproducible pilot

**Local performance and GeoFM uplift are currently unknown.** This assessment ran no
training or inference and has no independent local test labels. There is no defensible
"expected 90–95% accuracy" or model ranking for the user's AOI from the cited papers.

1. **Freeze the study design.** Select an AOI and label period, label taxonomy, error/cost
   objectives, spatial support, alert cutoff and reference protocol. Set acceptable
   precision, recall, area error, delay and cost before evaluating the final holdout.
2. **Create independent reference samples.** Use a probability design stratified by mapped
   change/stable/uncertain classes and relevant conditions; retain inclusion probabilities.
   Review dated evidence with adjudication of disagreements, blinded to model identity.
   Include rare/small events and uncertain onset intervals. Training/validation/test units
   must remain separate.
3. **Split by place and time.** Hold out spatial blocks larger than image overlap/context
   and relevant spatial dependence, whole events, a later year and (where possible) an
   external region. Use nested blocked validation for tuning. Fit all heads, normalization,
   feature selection and calibration within training/validation boundaries. Audit known
   pretraining/benchmark overlap and report residual unknown overlap.
4. **Run the ablations.** Begin B0/B1/F1 on a small representative subset; screen compatible
   encoders under the same local label budget and comparable tuning budgets. Then evaluate
   F2/F3/F4 only if justified. Record sensor-only/fused, raw/features, temporal context,
   missingness, trainable parameters and repeated seeds. Distinguish best-available-input
   comparisons from controlled comparisons using the same observations.
5. **Quantify uncertainty.** Report per-stratum counts and design-weighted estimates with
   confidence intervals; use paired spatial/event-block resampling for model differences
   where consistent with the sampling design. Seed variation is a separate uncertainty
   source and millions of adjacent pixels are not independent samples.
6. **Estimate scale and choose.** Measure pilot acquisition, preprocessing, embedding and
   inference throughput; project runtime from target area, observation density and measured
   rates, including fixed overhead, I/O, retries and cache reuse. Publish measured values
   separately from projections. Prefer the simplest arm meeting the predefined accuracy,
   delay, coverage and cost objectives. A marginal score gain alone does not justify fusion.

For sample-size planning only, an independent-binomial approximation is
`n ≈ 1.96² p(1-p) / e²`: precision near 0.90 with ±0.05 half-width suggests about **139
independent predicted-positive units**, or **385** at the worst-case p=0.5. This is not a
complete validation design: recall needs reference-positive units; spatial clustering,
stratum weights, rare events and uncertain labels alter allocation and effective sample
size. The existing ≥30 pixel-months per stratum is a review floor, not a promised interval.

The first results table must contain arm/checkpoint, dataset/label/split revisions, per-class
and event metrics with intervals, timing, area error, coverage, label count and cost. Until
the pilot exists, record all eight models' local metrics as **not measured**, not as zeros
or literature-derived forecasts.

## Harnessed workflow first; bounded agents where useful

**Recommendation:** adopt a reproducible GeoFM workflow as the next experiment. Add an
agent as a constrained planner/evidence assistant only after the deterministic workflow is
testable. Full autonomous detection, legal judgment, ranger notification and year-long
monitoring is not supported by the current implementation or validation evidence.

The user's three levels describe orchestration, not increasingly capable model weights:

| Level | What it actually supplies | Role in the proposed framework |
|---|---|---|
| Standard GeoFM / analyzer | Representation or task prediction from a defined input; quantified canopy loss needs a fitted/validated head | Versioned model component in the executable plane |
| Harnessed GeoFM / specialized workflow | Data selection, preprocessing, model/head, temporal rules, calibration, QA, map/area outputs and provenance | Recommended first implementation in a downstream repo |
| Agentic harness / autonomous operator | Plans and selects permitted tools, inspects evidence, handles exceptions and maintains scheduled task state | Optional outer control plane; it calls versioned workflows and records its decisions |

A suitable harness has typed inputs/outputs, model-specific adapters, data-quality gates,
checkpoint and environment locks, cached feature provenance, retry/resource limits,
resumable jobs, explicit failure/abstention states and replayable evaluation fixtures.
Persist the AOI, observation cutoff, feature window, labels/splits, model/head versions,
thresholds and evidence references with each output. Canonical models/methods stay candidate
until reviewed; successful execution does not promote them.

Useful first agent tasks are proposing the question contract, retrieving publications with
citations, finding candidate datasets, selecting among reviewed compatible workflows,
summarizing failures/disagreement, and drafting evidence reports. The planner must expose
candidate relationships rather than silently choosing them as validated science. It may
request more observations or queue a bounded rerun; it must not tune thresholds against the
final test set or silently change the forest definition.

For the broader autonomous-operator example, separate the capabilities:

- **Legal context:** retrieve jurisdiction- and date-specific official rules/permit records,
  preserve excerpts and applicability evidence, and route unresolved interpretation to a
  qualified reviewer. Keep change evidence, rule retrieval and legal conclusions distinct.
- **Notifications:** draft a reviewed alert containing geometry, date uncertainty, confidence
  and source evidence. External delivery requires an explicitly authorized recipient/action
  policy and deduplication; this assessment configures or sends no notifications.
- **Recovery monitoring:** create a durable schedule with a defined end date, observation
  windows, recovery target, budget, cancellation and exception handling. Scheduled workflows
  alone can provide routine monitoring; an LLM agent is optional.

Evaluate an agent against the same workflow without an agent on fixed scenarios, including
missing imagery, provider failure, conflicting evidence and misleading retrieved text.
Measure task completion, correct tool/workflow choice, citation/applicability accuracy,
unsupported claims, policy violations, review burden, cost and reproducibility. Require
permission-boundary tests and provenance for each action. Better orchestration must not
be claimed as better map accuracy unless the controlled map evaluation demonstrates it.

## Delivery sequence and repository responsibilities

| Stage | Forest Cover Lab artifact | Downstream work and exit evidence |
|---|---|---|
| A. Question and evidence | SS-0002, primary-source review, candidate data/model suitability and explicit unknowns | AOI/time/target and reference-label plan agreed; input compatibility demonstrated |
| B. Baseline and one encoder | Proposed evaluation contract referencing v2/v3 and ADRs | B0/B1/F1 pilot with independent held-out estimates, quality masks and cost measurements |
| C. Adaptation/fusion, if useful | Pinned code reverse engineering, proposed method/workflow concepts and an ADR for adoption | Controlled F2/F3/F4 improvement meeting predefined objectives; reproducible bundle |
| D. Bounded agent, if useful | Reviewed planner/action policy, evaluation scenarios and proposed contract extensions | Replay/shadow comparison with workflow-only execution and explicit action authorization |
| E. Operational use | Accepted decisions and reviewed scientific claims for the validated scope | Monitored drift, scheduled revalidation, rollback and separately justified recovery/notification capabilities |

Keep training/inference/GPU dependencies, model caches, observation catalogues and run
outputs downstream. Keep publication/data/code inventories and future reviewed model
contracts here. The existing graph has no dedicated model/checkpoint entity, and the
provenance schema has no complete model-training contract: propose typed model metadata
and a compatible manifest extension before implementation, with checkpoint checksum,
preprocessing revision, head/adaptation weights, feature lineage, split/label IDs,
calibration, cutoff, environment and resource use. Do not invent unregistered graph nodes
or claim current validators enforce these proposed fields. Such contract changes need
their own reviewed change and, for durable choices, an ADR.
