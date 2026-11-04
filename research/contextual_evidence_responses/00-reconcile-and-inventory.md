# Prompt 00 — baseline reconciliation

> Status: candidate. This is the historical assistant reply to the 2026-11-04 inspection request, not an approved decision or scientific validation. Local absolute links describe the original workspace and may not resolve elsewhere.

**The baseline is ready for an operator decision on architecture and scope, but not yet for a new investigation or a fully specified implementation.** The October round contains substantial reusable retrievals and visual evidence. Its controls are not independent ground truth, its source responses have not been replay-tested in this inspection, and the November power-line hypothesis has not been georeferenced or tested.

This was a read-only inspection. No files, branches, issues or commits were created. Official documentation was consulted, but I did **not** make live GetCapabilities or feature requests; October service observations below come from the round’s records, not from a new live test.

### Baseline

| Repository or workspace | Actual state | Evidence and gaps |
|---|---|---|
| [forest-cover-lab](/Users/server/projects/forest-cover-lab) | `main`, `c322e89fb96def2434c62776ac595f6cd995ef92`; dirty | Governing contracts, discovery protocol, schemas and graph present. Existing edits include `pyproject.toml` and untracked research/workspace files; preserved. |
| [sentinel-monthly-forest-cover](/Users/server/projects/sentinel-monthly-forest-cover) | `main`, `bb1b51437a4df274c5bca2c4a66b742c2ef21a93`; clean | October round and ignored raw evidence are present. A remote-tracking branch named `feat/round-0003-synthesis-report` exists; current PR status was not verified. |
| [private-bundles](/Users/server/projects/private-bundles) | `main`, `c510682b1c9269fdfc9112cceea72db3804943ca`; clean | `origin` is the user-named `https://github.com/GeorgeMadlis/private-bundles.git`. Local checkout and remote-tracking refs exist. Current remote authorization was not tested; no inference about existence or permission follows. Its policy requires privacy and reviewed PRs. |
| [geospatial-context](/Users/server/projects/geospatial-context) | Existing empty directory; no Git repository or SHA | Suitable proposed location, subject to operator decision. No repository or remote was created. |

Lab’s new-round schema is **1.1**, with 1.0 still supported; the inspected round itself declares 1.1. Its pinned graph revision is `f70789df04b79ca8ec65e0094c571e0b3f6844afa2b88af2f8c9bcf1776a20f7`. ADR 0005 is accepted; 0006–0008 are proposed. The next available numbers by the inspected ADR directory, source inventory and search-scope register are **0009**, **DS-0016** and **SS-0004**, respectively; recheck before allocation. `DS-0099` and `DS-9999` occur in tests, not as inventory allocations.

The documented checks are `python agent_harness/scripts/validate_round.py --root .` and `python agent_harness/scripts/render_round_graph.py --root . --check`. They were not run: this inspection was read-only, and `python` was unavailable in the shell. `python3` was available for read-only inventory. The four Sentinel `.codex/skills` exist; none was invoked.

### Corrections and independent challenge

| Claim or issue | Assessment and evidence | Implementation consequence |
|---|---|---|
| October conclusions dispose of the new power-line idea | **Corrected.** The November 4 hypothesis arose later and may concern another feature. October ETAK results include power-line crossings, but do not establish the new feature’s identity. See [geo findings](/Users/server/projects/sentinel-monthly-forest-cover/reviews/road-like-ndvi-2025-2026-monthly/rounds/round-0003/artifacts/geo-01/README.md) and [works claims](/Users/server/projects/sentinel-monthly-forest-cover/reviews/road-like-ndvi-2025-2026-monthly/rounds/round-0003/artifacts/works-01/works_claims.csv). | Obtain the operator’s actual geometry first; test power line, road, rail and other alternatives. Do not reuse `prior_rois.geojson` as the new AOI without evidence. |
| ROI-01 and ROI-02 have established single explanations | **Qualified.** October records support planning/land/notice associations for the northeast of ROI-01 and road-4/Are bypass evidence for the south of ROI-02; southwest ROI-01 and northern ROI-02 retain uncertainty. The synthesis makes stronger candidate interpretations with stated caveats. | Preserve claim scope and disagreements. Plans and parcels are not as-built alignments; notice approval is not a felling date. |
| Teeregister WFS is absent | **Unverified.** The round empirically used ArcGIS REST. [RIHA lists a public WFS documentation file](https://www.riha.ee/Infos%C3%BCsteemid/Vaata/teeregister); a working WFS URL and feature types remain unverified. | Implement against the recorded REST baseline first; investigate WFS separately. |
| Electricity restriction layers are interchangeable | **Unverified.** [MaRu documents](https://geoportaal.maaamet.ee/est/Teenused/WMSWFS-teenused-p65.html) `kma_avalik_elekter` in the `kmakitsendused` WMS. The round used `kitsendus_suunatud` WFS for other restriction layers. | Compare identifiers, geometry, authority and lineage before treating either as equivalent or independent. |
| WMS metainfo establishes flight dates | **Corrected for this historical case.** Round `GS-04/05` records stale `LENNUAEG` of 2023-06-09 versus 2025-04-03 in the sheet listings. The WMS-to-flight association was inferred, and GeoTIFF embedded metadata was not checked. | Keep this mismatch as a regression fixture. Compare listing, WMS and both grid scales; [the official grid documentation](https://geoportaal.maaamet.ee/est/ruumiandmed/kaardilehtede-susteemid/kaardiruudustikud-allalaadimiseks-p488.html) describes different 1:2000 and 1:10000 `LENNUAEG` scopes. Grid freshness is unknown. |
| Fotoladu API is an orthophoto API | **Corrected.** Its documented coordinate API concerns oblique aerial photographs; the wider archive contains other materials. [Official Fotoladu documentation](https://geoportaal.maaamet.ee/est/Kaardirakendused/Fotoladu/Fotoladu-aerofotode-digitaalarhiiv-p545.html). | Model it separately from orthophoto WMS and verify relevant coverage. |
| GFW independently validates Hansen loss | **Corrected for GFW’s UMD/Hansen tree-cover-loss product:** it shares the underlying lineage. Other GFW datasets require their own source and method checks. | Record lineage per dataset; annual Hansen loss is weak supervision, not monthly ground truth. |
| Controls establish absence | **Corrected.** `works-01` claim C15 explicitly says its control polygons fell outside those download bounding boxes; geo-01 checked controls with ETAK only. | They can be retrieval fixtures, not established independent control truth. |

### Candidate source and adapter matrix

Status below refers to evidence available **here**, not implementation in geospatial-context. `R` means an October retrieval is recorded and its response is locally retained; **no adapter replay was performed**. `D` means documentation or the supplied brief identifies the source; current service response is unverified. Unless specified, licence and redistribution terms need source- and asset-level confirmation. A/B/C refer to discovery, tool-operation provenance and evidence assembly.

| Source / authority | Documented or recorded endpoint and layer | Last recorded retrieval UTC; status | Lineage; A/B/C potential; priority and licence gap |
|---|---|---|---|
| ETAK / MaRu | [ETAK WFS](https://gsavalik.envir.ee/geoserver/etak/wfs): `etak:e_501_tee_j`, `e_502_roobastee_j`, `e_503_siht_j`, `e_601_elektriliin_j` | 2026-10-24 16:46–16:47; R | ETAK, partly orthophoto-derived. A/B/C, P0; attribution/open-data terms recorded, fixture redistribution to verify. |
| Metsaregister / Keskkonnaagentuur | Round records `metsaregister:teatis` and archive under the GeoServer Metsaregister WFS | 2026-10-24, exact times in [ledger](/Users/server/projects/sentinel-monthly-forest-cover/reviews/road-like-ndvi-2025-2026-monthly/rounds/round-0003/artifacts/works-01/works_ledger.csv); R | Administrative notices, not event confirmation. A/B/C, P0; terms and archive coverage verify. |
| Planning / MaRu | [Planning WFS](https://gsavalik.envir.ee/geoserver/planeeringud/wfs), `planeeringud:rb_planeeringutrass` | 2026-10-24 16:39:14; R | County plan; shares underlying plan with restriction record E05. A/B/C, P0; terms verify. |
| Cadastre / MaRu | [Cadastre WFS](https://gsavalik.envir.ee/geoserver/kataster/wfs), `kataster:ky_kehtiv` | 2026-10-24 16:42:10; R | Cadastre; parcels are not construction geometry. A/B/C, P0; terms and sensitive attributes verify. |
| KPOIS directed restrictions / MaRu | [Directed WFS](https://gsavalik.envir.ee/geoserver/kitsendus_suunatud/wfs), recorded `kpo_avalik_planeering` and transport layers | 2026-10-24 16:40:41 for planning; R | KPOIS; shared plan lineage. A/B/C, P1; electrical WFS type and equivalence unverified. |
| KMA electricity / MaRu | [KMA WMS](https://gsavalik.envir.ee/geoserver/kmakitsendused/wms), `kma_avalik_elekter` | No retrieval here; D | Electricity restriction zones, relation to WFS unknown. A/B/C, P1; terms and GetCapabilities verify. |
| EHAK / MaRu | Round’s EHAK WFS village download | 2026-10-24; exact UTC requires ledger verification; R | Administrative boundaries. A/B/C, P1; licence and specific type verify. |
| Teeregister / Transpordiamet | [ArcGIS MapServer](https://gis.transpordiamet.ee/arcgis/rest/services/Teeregister/MapServer), recorded layers 1, 9, 12 | 2026-10-24; precise UTC requires ledger verification; R | Road register. A/B/C, P0; layer semantics and terms verify. RIHA WFS documentation is D; endpoint/types unverified. |
| Orthophoto / MaRu | [Historical WMS](https://kaart.maaamet.ee/wms/ajalooline), [current](https://kaart.maaamet.ee/wms/fotokaart), [base](https://kaart.maaamet.ee/wms/alus) | 2026-10-24 16:37–16:48; R | Imagery and ETAK may share lineage. A/B/C, P0; attribution recorded, retention and redistribution per asset verify. |
| Sheet listings / MaRu | [Page 610](https://geoportaal.maaamet.ee/index.php?lang_id=1&page_id=610); historical per-sheet requests in `raw/sheets*` | 2026-10-24 16:41 and 16:47; R | Official filename dates, not embedded metadata. A/B/C, P1; HTML access policy and retention approval needed. |
| 1:2000 and 1:10000 grids / MaRu | [Download documentation](https://geoportaal.maaamet.ee/est/ruumiandmed/kaardilehtede-susteemid/kaardiruudustikud-allalaadimiseks-p488.html) | No grid download examined; D | MaRu metadata; freshness unknown. A/B/C, P1; licence and actual grid values verify. |
| Fotoladu / MaRu | [Documented API](https://fotoladu.maaamet.ee/api.php?B=59.420826774381965&L=24.697852488050824) | No API response examined; D | Oblique photographs; possible shared flight lineage. A/B/C, P2; per-image terms and coverage verify. |
| GFW tree-cover loss / UMD and GFW | [GFW data API documentation](https://data-api.globalforestwatch.org/docs) | No dataset request examined; D | Hansen/UMD lineage. A/B/C, P3; exact edition, coverage and terms verify. Other GFW datasets are separate unverified candidates. |
| Official works, procurement, literature | Round’s official and secondary-source records | October timestamps in ledger; R for retained items | Mixed publishers and potentially shared underlying releases. Primarily C, outside v0 map-service adapters; P1 research track. Copyright and retention differ by source. |

The prompt requests precise live retrieval UTC for each source: where it is absent above, it remains unknown in this assessment. Documentation consulted during this inspection is not a live feature-service test.

### October replay inventory

The [round directory](/Users/server/projects/sentinel-monthly-forest-cover/reviews/road-like-ndvi-2025-2026-monthly/rounds/round-0003) contains `inputs/`, the manifest, execution records, scripts and ledgers. The current ignored directories contain:

- `artifacts/geo-01/raw/`: **99 files, 12,037,695 bytes**, including capabilities XML, `etak/` (23 files), `wms/` (28), sheet listings (29 across two directories), probes, metadata and request logs.
- `artifacts/works-01/downloads/`: **51 files, 16,820,117 bytes**, including ETAK, notices, cadastre, planning, restrictions, EHAK, six Teeregister GeoJSON files and 12 web/PDF files.
- Filenames and individual byte sizes can be enumerated from those directories; `geo_primary_evidence.json`, `works_primary_evidence.json`, and the geo fetch logs provide recorded hashes for listed artifacts. I did **not** recompute every checksum or verify that every ignored file is covered. Some logs retain original `round-0002` absolute paths even though the inspected artifacts are under round-0003; replay must resolve files by verified content, not trust those paths.

A concrete fixture is the recorded WFS 2.0 request for `etak:e_501_tee_j`, `EPSG:3301`, bbox `534721,6476287,547541,6489584`, `count=5000`: the geo log records **2,090 bbox features** and SHA-256 `3440b0924205324d2863925e72b944ba40dd76a75219c1f0a889c5eda2bebd04`. Its exact encoded request is in [etak_fetch_log.json](/Users/server/projects/sentinel-monthly-forest-cover/reviews/road-like-ndvi-2025-2026-monthly/rounds/round-0003/artifacts/geo-01/raw/etak/etak_fetch_log.json). For the same geo retrieval, ROI-01 road/rail/cutline/power-line bbox counts are **2090/1/36/95**; ROI-02 counts are **214/0/5/14**. These are bbox response counts, not intersection counts.

Useful independent fixture assertions include:

- The recorded ROI-01 rail intersection has ETAK ID **4076351** and 143 m inside the ROI; the planning corridor covers a reported **46.0%** of ROI-01 in the historical calculation. Reproduce with the same geometry, CRS and method rather than treating those figures as new measurements.
- WMS request logs contain exact GetMap parameters, including WMS 1.3 axis ordering. An empty `of2023aero` probe and a populated `of2023mets` example can exercise empty-coverage handling.
- The page-610 listing versus stale WMS `LENNUAEG` supplies a date-conflict fixture. The original records report 2025-04-03 for the ROI sheets, with the WMS-layer association inferred.
- Teeregister layers 1, 9 and 12 and the notices/cadastre responses can exercise parsing and linkage; exact query parameters and expected feature IDs must be checked against each source’s own logs and ledger before freezing fixtures. Geo IDs and works IDs are separate namespaces.

Present visuals include [geo composites](/Users/server/projects/sentinel-monthly-forest-cover/reviews/road-like-ndvi-2025-2026-monthly/rounds/round-0003/artifacts/geo-01/images), [works maps](/Users/server/projects/sentinel-monthly-forest-cover/reviews/road-like-ndvi-2025-2026-monthly/rounds/round-0003/artifacts/works-01/images), and the [synthesis report](/Users/server/projects/sentinel-monthly-forest-cover/reviews/road-like-ndvi-2025-2026-monthly/rounds/round-0003/artifacts/synthesis-01/synthesis_report/index.html). Geo’s 2023 and 2025 samples, limited 2024 coverage and 2024/2026 map editions are present; its record found no post-April-2025 orthophoto for those ROI sheets at the time. This is a historical, scoped observation, not a current archive-wide claim. Feature-scale inspection covered only portions of the ROIs.

### Proposed inspectability contract

- **A — Sources:** maintain a versioned source catalogue distinct from the adapter catalogue. Per case, record each candidate as considered, attempted, used, not relevant, blocked, failed or no matching records, with coverage and reason. A successful empty response is different from an inaccessible source.
- **B — Tools:** maintain declared tools and fixture test evidence separately from availability to a host and actual invocations. Append observed executions with tool/version, role, UTC, parameters or privacy-safe hash, source, cache mode, result hash/path, error and elapsed time or `not_measured`.
- **C — Evidence:** link claim → evidence → retrieval/computation → raw and derived assets. Record source edition, acquisition, publication, event and retrieval dates separately; AOI/CRS, query, hashes, licence, lineage, limitations, contradiction and missingness. Visual sidecars retain georeferencing, source, rendering and attribution. Evidence remains candidate material; retrieval and geometry tools issue no causal or scientific verdict.

The offline index should expose all three structures, including missing and blocked sources, with no runtime CDN or external tiles. It must make shared lineage visible and must not imply independence from multiple presentations of the same data.

### Decisions and approval gates

I recommend a **library → CLI → local stdio MCP** sequence in geospatial-context. A library first permits deterministic offline tests and reuse by multiple consumers; a CLI makes recorded replay practical before an MCP interface adds host/tool lifecycle concerns. MCP-first could accelerate host experiments, but would couple initial testing to an interface before source, failure and provenance contracts are stable. Local stdio access for Codex and Claude Code does not provide remote access to browser chat hosts.

Start with an allowlist of the recorded national GeoServer, MaRu map services and Teeregister MapServer, with explicit permitted paths, methods and layers. Deny arbitrary URLs, private-address resolution and unexpected redirects; set configured AOI, response, pagination, timeout and rate limits. Public HTML parsing should remain disabled until the operator approves a named official host/path, purpose, request rate, retention and terms; it should never become general browsing.

Existing projects are candidates for assessment, not dependencies: [mcp-ogc](https://github.com/nickoulos/mcp-ogc) advertises WFS/WMS and AGPL; [geoserver-mcp](https://github.com/mahdin75/geoserver-mcp) advertises MIT and broader GeoServer administration; [esri-mcp](https://github.com/daraobeirnecode/esri-mcp) advertises ArcGIS service queries, but its licence and suitability were not established here. Their arbitrary-service access, write surfaces, dependencies and licence obligations need review before any reuse.

Keep reusable semantics and candidate source records in Lab, retrieval code in geospatial-context, case execution records in Sentinel, and authorized case assets in private storage. Private-bundles’ existing policy requires reviewed PRs and preservation of source bytes; its suitability for large binaries or MinIO is not established.

**Operator decisions still needed:** repository creation and remote ownership; source/layer allowlist and HTML policy; fixture redistribution and private raw-asset storage; performance limits; new-case geometry; and any live testing. Before proposing execution agents for a sufficiently specified new question, the existing round rules require a rendered graph and human approval, followed by the applicable stepwise approvals. Knowledge promotion remains a separate human review.

### Suggested stages and first PR boundaries

| Stage | Proposed work | Acceptance boundary |
|---|---|---|
| 01 | Approve architecture, source scope, access and storage decisions; frame the new feature. | Named geometry and alternatives; no inferred AOI; approved graph before agent execution. |
| 02 | Lab candidate discovery and contracts under a declared search scope. | Stable IDs, citations, lineage, candidate status; governance, graph and drift checks as applicable. |
| 03 | Geospatial-context library and offline WFS/REST fixture replay. | Hash-verified inputs, deterministic queries and counts, CRS/axis, empty/error/pagination tests; no network-dependent CI. |
| 04 | Date and imagery metadata, visual sidecars and offline evidence index. | Stale-date conflict preserved, provenance and attribution complete, blocked/missing inputs visible. |
| 05 | CLI, execution logging and security limits. | Actual calls distinguishable from declared tools; allowlist and failure tests pass. |
| 06 | Local stdio MCP and operator-approved live checks, then a separately approved investigation. | Interface parity with library, no automatic verdicts, replay versus live drift explained. |

The first PRs should remain separately reviewable: a Lab governance/source-candidate PR, then a geospatial-context offline retrieval and fixture PR, followed by visual/CLI and MCP work. These boundaries are proposals; prompts 01–06 were not supplied, so their exact contents and acceptance criteria remain to be reconciled.

**Stopped for operator review**, as requested.
