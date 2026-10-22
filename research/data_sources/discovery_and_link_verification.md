# Dataset and tool discovery, FAIR assessment, and link verification

This is the standing protocol for [dataset-and-tool-discovery](../../agent_harness/roles/dataset-and-tool-discovery.md). Its tasks are selected per round by a human/general agent, not automatically scheduled. A declared role is not evidence that searches or checks ran; preserve actual tools, timestamps, loaded harness files and evidence in the round.

## Inventory authority and seed sources

The Lab's `research/data_sources/inventory.csv` and stable `DS-` identifiers are the governed dataset assessment index. `suitability_rubric.md` and `sources_notes.md` provide suitability and detail. A new Lab candidate requires a search scope from `research/methodology/search_scopes.csv` and starts as `status = to_review`. Assess software and service platforms separately in `research/packages/`.

The [eudr-dmi-gil auto catalogue](https://github.com/GeorgeMadlis/eudr-dmi-gil/blob/main/data_db/dataset_catalogue_auto.csv) is an **external, partly auto-generated discovery seed**; preserve the source commit, `dataset_id`, link field and original value. Do not import it wholesale into the Lab or modify the other repository without explicit authority. Reconcile duplicate products, collection pages, aliases and obsolete editions.

Three complementary surfaces are [Fields of The World](https://fieldsofthe.world/) (labeled field datasets versus predictions, segmentation models, inference tools), [Source Cooperative](https://docs.source.coop/) / [source.coop](https://source.coop/) (public dataset hosting and distribution), and [Earthmover](https://www.earthmover.io/) / [docs](https://docs.earthmover.io/) (catalogue, marketplace, Icechunk/Arraylake and delivery interfaces). For Source or Earthmover, follow the listing back to the originating producer, collection and asset. Check product-specific authentication, licensing and price; do not infer that a platform or advertised 'open' catalogue makes each product free to reuse. Search original national/international agencies, official schemas, papers and model/tool releases beyond these leads.

## Distinct entities to capture

| Entity | Minimum record | Not evidence of |
|---|---|---|
| Dataset/product | Canonical producer, collection and item/edition, PID, temporal/spatial coverage, CRS, resolution, variables/classes | Endpoint uptime or label correctness |
| Data distribution | URL, query/protocol, version/ETag, format, auth/license, tested time | A distinct scientific dataset |
| Portal/index service | STAC, OGC, S3/HTTP, market listing or metadata search | Data usability/quality for a concrete AOI |
| Software/model | Version, code license, checkpoint/input schema, runtime resources, method | Independently acquired reference labels |
| Validation/reference | Acquisition/annotation time, independence group, method and spatial uncertainty | Automatically independent ground truth |

Live scene searches should record the collection, query and actual item/asset revision or ETag without assuming a permanent duplicate catalogue is required. Neither the knowledge graph nor GeoParquet/STAC metadata is itself a full scene archive.

## FAIR-inspired and task-specific assessment

Annotate each dimension `supported`, `partial`, `unknown`, or `not_supported`, with original provider evidence and checked UTC:

- **Findable:** persistent dataset/product ID, indexed descriptive metadata and version/release notes.
- **Accessible:** demonstrably retrievable metadata/data via lawful protocol; credential, quota, subscription, cost and retention caveats.
- **Interoperable:** machine-readable STAC/OGC/CF/GeoParquet or other documented schema; CRS, temporal meaning, data format and class legend.
- **Reusable:** explicit license *for data and models separately*, redistribution/commercial rights, citation, traceable lineage, quality, uncertainty and validation information.

Do not call this formal FAIR certification. Independently assess geographic fit, true effective mapping unit, reference years versus release dates, expected update frequency and latency, cloud/missing-data artifacts, prediction/reference distinction, class-confusion risk, source independence and local/cloud-neutral implementation cost. For phase-specific scores use [suitability rubric](suitability_rubric.md). A field boundary product supports agricultural pressure/land-use context; it does not by itself date forest clearing.

## Auditing existing URLs

1. Freeze source catalogue revision and select exact row IDs and fields, e.g. `primary_url`, `api_url`, `download_url`, `documentation_url`, `metadata_url`.
2. Record original URL, HTTP method, response/status code, redirect chain, final URL, content type, UTC time and query parameters. Test safely (HEAD, then bounded GET/metadata or OGC GetCapabilities if needed), honoring quota and credentials; no mass downloads.
3. Classify `verified`, `redirect`, `restricted`, `broken`, `timeout`, or `unverified`. A HTTP 200 HTML login page is not a verified asset. A 403/429 or timeout is not proof of a permanently broken URL; a 404/410 should be checked against provider migration documentation.
4. When proposing replacement, cite provider-owned evidence, confirm scientific product and edition consistency, and retain original link plus date. Propose a patch for review; do not rewrite unconfirmed references.
5. Report untouched fields and negative results rather than invent success. Recheck near publication if link changes are time-sensitive.

Suggested per-link CSV fields: `catalogue_repo,catalogue_commit,row_id,field,original_url,tested_utc,method,http_status,redirect_chain,final_url,content_type,resource_identity,outcome,provider_evidence_url,proposed_url,reason,review_status`. An absence of a link report means no audit was performed.

## Answer contract for a human or another agent

Return a concise evidence-backed **dataset-to-pipeline memo**: the problem definition (AOI, reference and observation dates, forest/class measurement, desired resolution, exclusions, unknowns); candidate Lab ID if truly matched (else original external ID + `candidate`); provider and version; source/link validation date, availability and license; comparison of suitability, independence and alternatives; a proposed STAC/OGC/API retrieval route, preprocessing/classification tools and likely resource use; expected checks for CRS/time/quality/class accuracy and lineage; and explicit limits/stop conditions.

The pipeline is **a proposal, not an executed result**. Acquire actual rasters, process tiles, run models and store operational provenance in the downstream repo. Distinguish forest disturbance from legal deforestation; surface presence from construction date; predicted features from field-checked reference. Generated science/graph relations remain candidates subject to human promotion governance.

## Example assignment for a future round (not executed)

Compare sources for agricultural field boundaries versus new-road construction as forest
pressure/context evidence as of a declared date. State missing AOI, observation interval,
resolution and license/compute constraints. Require separate producer citations and editions
for field reference labels, predicted polygons, dated imagery and road/construction records.
Report data and model licenses, lineage/independence, event-date uncertainty, feasible
cloud-neutral tools and a proposed acquisition-to-validation pipeline. Return conditional
options or `insufficient_evidence`; label unchecked URLs `unverified`. This example verifies
no source, performs no HTTP requests and records no role execution. A real assignment must
first establish its bounded source scope and preserve evidence in the round.
