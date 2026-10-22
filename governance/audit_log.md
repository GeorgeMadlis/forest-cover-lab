# Audit Log

Each entry records one run of `drift_checklist.md`. Log entries are append-only.

---

## 2026-04-24 — Initial architecture revision

**Trigger:** Structural change — added governance/, research/methodology/,
research/data_sources/, research/code_sources/.

**Checklist result:** Pass (establishing baseline; all items satisfied by this revision).

**Open findings:** None.

**Reviewer:** Forest Cover Lab maintainers

---

## 2026-04-24 — Context-aware architecture revision

**Trigger:** Structural change — clarified the six principles, added an architecture
assessment, added search-scope tracking, and expanded the data-source track to handle
adjacent Earth-observation context products.

**Checklist result:** Pass after revision.

**Open findings:** None.

**Reviewer:** Codex architecture pass

---

## 2026-04-24 — Downstream repository role clarification

**Trigger:** Structural change — made Forest Cover Lab's role explicit as a governance,
explanation, and reusable data-source evidence repo for narrower downstream repositories.

**Checklist result:** Pass after revision.

**Open findings:** None.

**Reviewer:** Codex architecture pass

---

## 2026-10-06 — Semantic architecture and backend separation

**Trigger:** Added OKF-oriented corpus, local derived graph, typed contracts and provenance.

**Checklist result:** Pass. Mission and adjacent-context boundary preserved; research tracks,
search scopes, suitability fields, code discovery and reverse-engineering template retained.
Independent tracks remain enterable; governance references and downstream contracts updated.
Stable DS IDs, inventory semantics, scientific rules and all monthly non-claims preserved.
Candidate method/implementation relationships remain separate from contract transcriptions.
Execution software, live scene catalogues and run evidence remain separate authorities.
ADR 0005 records task-supplied backend policy; no new scientific performance claim added.

**Open findings:** Seasonal decision rules and downstream mapping require future scientific/
code review; retained explicitly as candidates rather than authoritative claims.

**Reviewer:** Codex contract/architecture review (not empirical scientific validation).

---

## 2026-10-06 — Cross-repository integration audit (sentinel-monthly-forest-cover)

**Trigger:** Independent integration and architecture-drift audit against downstream
`sentinel-monthly-forest-cover` (pre-audit commits: this repo `c0f21c7`, downstream `4df8370`).

**Checklist result:** Pass after revision. Findings fixed:

- The workflow record's candidate edges disagreed with the pinned downstream descriptor
  (persistence listed as implemented; moving-window/matched-season, pyproj/shapely and
  capabilities missing). Edges now separate declared 2.0.0 relationships from target-only ones.
- Descriptor validation did not check workflow relationships or tool/capability coverage;
  provenance validation accepted methods/tools the workflow does not implement. Both now fail.
- `graph/build.py --descriptor` accepted JSON only although the downstream descriptor is YAML.
- `configs/run_manifest.semantic.example.json` attributed a Hansen baseline method to the
  Sentinel workflow; the example now uses methods that workflow registers.
- Generation now rejects cyclic USES_METHOD composition and duplicate dataset entities.
- Stale "GEE is the v1 default platform" wording and unannotated ADR 0001 references updated.

**Open findings:** Workflow IMPLEMENTS edges remain candidates pending scientific/code review.
Seasonal decision thresholds remain unvalidated. No canonical forest definition, method meaning,
observation semantics, non-claim or validation policy was changed.

**Reviewer:** Claude cross-repository contract audit (not empirical scientific validation).

---

## 2026-10-19 — GeoFM and workflow-harness architecture assessment

**Trigger:** Extended the architecture assessment with current GeoFM integration status,
eight-family suitability comparison, six-step scientific/evaluation plan, and workflow versus
agentic harnessing. Added SS-0002, a primary-source evidence review, publication/code
discovery records and candidate HLS/annual TESSERA feature entries.

**Checklist result:** Mission and all P1–P6 boundaries retained. Primary evidence and access
limits are explicit; technical documentation/preprints are not relabelled as peer-reviewed
studies. Inputs, auxiliary features and independent references remain distinct. Code discovery
does not claim P4 reverse engineering. Existing independent tracks remain enterable.
Execution/GPU dependencies and runs stay downstream; model adoption and typed contract
extensions remain proposals requiring their own reviewed changes/ADRs. No method or graph
relationship is promoted and no empirical accuracy or legal conclusion is asserted.

**Open findings / follow-up:** AOI/time/target and operational objectives are unspecified;
local reference labels, checkpoint/code/license audits, model metadata contracts and empirical
benchmarks are still needed for adoption. PUB-0012 remains pending full-text review. New
DS-0014/0015 and CS-0002–0010 remain candidates/discovery records. Earlier seasonal-method
and workflow-equivalence findings remain open. These are research gaps, not implemented
capabilities. Local consistency-check results are recorded below after verification.

**Verification:** 55 local tests passed. `graph/build.py --check --descriptor
configs/downstream.sentinel-monthly.example.json` passed after regenerating the inventory
snapshot and refreshing example hashes. Graph concept and relationship counts are unchanged.
CSV row structure, unique IDs, new review-score totals and 19 local Markdown links checked;
`git diff --check` passed. No model training/inference or scientific accuracy test was run.

**Reviewer:** Codex architecture/evidence review (not empirical scientific validation).

---

## 2026-10-21 — Agent instruction files and downstream pin check

**Trigger:** Added agent-facing instructions (`AGENTS.md`, imported by `CLAUDE.md`) and a
README pointer to them. A companion change in `sentinel-monthly-forest-cover` re-pins its
descriptor to this repo's `71f5481` / graph `3e6dc320…914380a`.

**Checklist result:** Pass. Mission boundary and P1–P6 unchanged; the new file restates
existing rules (ADRs 0002–0005, knowledge promotion, drift control, stable IDs) and points to
their canonical sources instead of redefining them. No concept, relationship, threshold,
non-claim, schema or validation policy changed; the generated graph is not affected.

**Open findings:** Before this change the downstream descriptor pinned `f3895e4` / graph
`ef90b703…` and `graph/build.py --check --descriptor` failed with a stale graph revision.
The intervening commits only added DS-0014/DS-0015 inventory rows plus viewer and GeoFM
documents, so no semantics consumed by the workflow changed; resolved by the companion
re-pin. Earlier open findings (candidate IMPLEMENTS edges, unvalidated seasonal thresholds,
GeoFM follow-ups) remain open.

**Verification:** `python graph/build.py --check` (68 concepts; 72 validated and 67
candidate relationships; revision unchanged) and `python -m pytest` (55 passed).

**Reviewer:** Claude repository-sync change (not empirical scientific validation).

---

## 2026-10-21 — README overview diagram and glossary

**Trigger:** Added a new directory `docs/img/` with an overview diagram
(`problems-and-approaches.svg`) embedded in `README.md` after the Critical Warning, and a
root-level `GLOSSARY.md` explaining abbreviations; README repository-structure block and a
glossary pointer updated.

**Checklist result:** Pass. Mission boundary and P1–P6 unchanged. The diagram and glossary
summarise existing ADRs 0002–0005, the v2/v3 specs, `docs/architecture.md` and governance
rules and point back to them; they introduce no new concept, relationship, threshold,
non-claim, schema or validation policy. The Critical Warning text is unchanged and is also
restated in the diagram. GeoFM uplift and local accuracy remain stated as not measured.

**Open findings:** None new. Earlier open findings (candidate IMPLEMENTS edges, unvalidated
seasonal thresholds, GeoFM follow-ups) remain open.

**Verification:** `python graph/build.py --check` (68 concepts; 72 validated and 67
candidate relationships; revision unchanged), `python -m pytest` (55 passed) and
`git diff --check` passed.

**Reviewer:** Claude documentation change (not empirical scientific validation).

---

## 2026-10-21 — Overview diagram sync rule and generator

**Trigger:** Changed agent-facing instructions (`AGENTS.md`: new "README and overview
diagram" section) and the drift checklist (new P6 item); added the diagram generator
`docs/img/build_overview_diagram.py` and `tests/test_overview_diagram.py`.

**Checklist result:** Pass. Mission boundary and P1–P6 unchanged. The SVG is now generated
from a committed script with deterministic text metrics; its rendered content is unchanged.
The new test fails when the SVG is stale, a cited source is missing, a non-superseded ADR is
not cited or the roadmap differs from `specs/v*_*.md`. No concept, relationship, threshold,
non-claim, schema or validation policy changed; the generated graph is not affected.

**Open findings:** Changes in scope that do not touch ADRs, specs or cited files (e.g. a
revised problem statement) still rely on the AGENTS.md rule and this checklist item rather
than an automated check. Earlier open findings remain open.

**Verification:** `python graph/build.py --check` (revision unchanged), `python -m pytest`
(61 passed), `python docs/img/build_overview_diagram.py --check`, ruff and black clean on
the new files.

**Reviewer:** Claude documentation/tooling change (not empirical scientific validation).

---

## 2026-10-21 — Agent registry

**Trigger:** Added `docs/agents.md`, a registry of the agents working in this repository
(Claude Code, Codex, Copilot; a proposed bounded planner), their attributes and every file
that defines them; added `tests/test_agent_registry.py`; changed agent-facing instructions
(`AGENTS.md`: new "Agent registry" section). README, `docs/README.md` and `GLOSSARY.md`
(CI, MCP) updated with pointers and abbreviations.

**Checklist result:** Pass. Mission boundary and P1–P6 unchanged. The registry describes
existing configuration only: all three agents share `AGENTS.md`, and no subagents, skills,
tool permissions, MCP servers, hooks or model pins are defined in the repository. The
proposed planner agent stays proposed. No concept, relationship, threshold, non-claim,
schema or validation policy changed; the generated graph is not affected.

**Open findings:** Agent status changes that leave files untouched (e.g. Copilot first used)
rely on the AGENTS.md rule rather than an automated check. Earlier open findings remain open.

**Verification:** `python graph/build.py --check` (revision unchanged), `python -m pytest`
(65 passed); the registry test was confirmed to fail on an unlisted `.claude/agents/` file.

**Reviewer:** Claude documentation/tooling change (not empirical scientific validation).

---

## 2026-10-21 — Round-bound agent harness integration

**Trigger:** Added standing client instructions, portable roles, schema/templates,
planning-only examples, local round validation and registry/provenance tests. ADR 0006
is Proposed; operator human review remains pending. Baseline Lab commit:
`71f54816d148a8b011a3917e731361768447205f`.

**Checklist review:** Mission and P1–P6 retained. Forest-cover estimation and downstream
scientific authority remain explicit. P1 search protocol, scopes and source-type distinction
are unchanged; no search/inventory entries added. P2 data roles, phase suitability and
separate tool assessment remain unchanged. P3 discovery scopes and independent code
catalogue remain intact. P4 template and analysis placeholder remain intact; no reverse
engineering is claimed. P5 all four track READMEs retain input/output declarations and
independent entry. P6 architecture/docs/downstream boundary are updated or retained; this
entry records the structural change and carries earlier open research findings forward.
No scientific contract, source inventory, concept, relation, generated graph or threshold
was changed. Operational data and results stay downstream. No candidate was promoted.

**Actual checks:** `.venv/bin/python -m pytest`: baseline 55 passed; final 104 passed
in 4.20 s. `.venv/bin/python graph/build.py --check --descriptor
configs/downstream.sentinel-monthly.example.json`: PASS, 68 concepts, 72 validated and
67 candidate relationships, unchanged graph revision
`3e6dc320bd9f59a483d605d100614005eaa1beb35139edcd1d7d37f04914380a`.
`.venv/bin/python agent_harness/scripts/validate_round.py --root .`: PASS, two planning
examples, no real inquiry rounds. `.venv/bin/python -m compileall -q agent_harness
tests/test_agent_harness.py tests/test_agent_registry.py` and `git diff --check`: PASS.
A local Python drift probe checked required governance/protocol/template files, all four
track README input/output declarations, required inventory fields and CSV row structure
(15 data, 10 code, 12 publication rows): PASS. Manual checklist review covered mission,
source/tool separation and independent entry semantics. These checks establish record
and architectural consistency, not empirical scientific validity.

**Reconciliation / deviations:** AGENTS.md, CLAUDE.md, docs/agents.md and the registry test
were absent in the actual checkout, so they were added rather than replacing prior files.
No named unused client was found in standing documentation; defensive discovery for
additional instruction formats is retained and regression-tested. Nonexistent overlay
references (GLOSSARY.md, overview SVG/generator and its test) were removed from the index;
there is no governed README overview generator to run. A small Mermaid diagram documents
the harness instead. Strengthened the proposed validator with both-repo pins, graph digest,
mandatory loaded contracts, output_hashes, explicit round-only roles, bounded paths,
status consistency and strict YAML. Schema remains the new, unreleased 1.0 contract.
Black/Ruff are not installed in the existing environment; their optional formatter hooks
were not run. CI's existing pytest/graph checks plus explicit round CLI remain enabled.

**Open findings:** Human review of ADR 0006/policy remains pending. Declaration validation
cannot prove actual model loads, independence, digest authenticity or scientific accuracy;
review pinned content/evidence and append-only history separately. No orchestration or
scientific evaluation was introduced. Earlier seasonal/workflow/GeoFM research gaps remain
open. Sentinel baseline had four stale-graph errors, to be repaired and recorded downstream.
Unrelated local pyproject.toml license metadata and untracked research/workspace files are
preserved and excluded from this change.

**Reviewer:** Codex structural/contract review; no human approval or scientific validation
is asserted. Detailed scope/deviations: docs/agent_harness_integration.md.

---

## 2026-10-21 — Publication reconciliation with current main

**Trigger:** Operator authorized commit, push and merge after the initial implementation.
Fetching revealed upstream main `713154028ef7689162c6694e78ff906e081023ac` had added standing instructions,
registry tests, glossary, governed overview generator and its sync rule. Merged that history
into the feature branch and reconciled conflicts without losing either set of audit entries.
Initial-checkout observations above remain historical; the previously absent files now exist.

**Checklist result:** Mission and P1–P6 preserved. All upstream scientific, stable-ID,
backend, graph-regeneration, diagram-sync and convention rules remain in AGENTS.md.
Current host documentation names ChatGPT, Claude, Claude Code and Codex; historical
append-only audit entries retain original names/descriptions. Registry checks retain all
upstream client formats (including .mcp.json, local instructions, skills, prompts and
chatmodes) and reject stale indexed standing paths, while round runtime files self-inventory.
ADR 0006 triggers the governed overview rule: updated generator content with the eighth
problem, regenerated SVG and updated README together. No glossary abbreviation was added.
No scientific corpus, graph input, inventory, phase semantics or promotion status changed.

**Actual verification:** `.venv/bin/python -m pytest`: 111 passed in 4.36 s.
`.venv/bin/python docs/img/build_overview_diagram.py` regenerated the SVG;
`.venv/bin/python docs/img/build_overview_diagram.py --check`: PASS.
`.venv/bin/python graph/build.py --check --descriptor
configs/downstream.sentinel-monthly.example.json`: PASS, 68 concepts, 72 validated and
67 candidate relationships, graph revision unchanged (`3e6dc320…914380a`).
`.venv/bin/python agent_harness/scripts/validate_round.py --root .`: PASS, two planned
examples. `git diff --check`: PASS. Hosted checks are pending publication at this point.
The manual drift review preserves independent research tracks and source/tool separation.

**Open findings / review:** Publication/merge is operator-authorized; this does not authorize
scientific promotion or assert human empirical validation. ADR 0006 remains proposed.
Earlier scientific, workflow-equivalence and evidence-authenticity limits remain open.
Unrelated local edits remain excluded. This record supersedes the initial integration's
missing-overview limitation; the upstream diagram contract is now enforced.

**Reviewer:** Codex integration/architecture checks; no scientific approval asserted.

---

## 2026-10-22 — Dataset and tool discovery subagent addition

**Trigger:** User-requested standing role for FAIR-inspired dataset/tool discovery, link health and evidence-backed pipeline-Q&A. Added a portable role, a source/link protocol and pointers across agent, data-source, tooling, research, downstream and architecture documentation. Stable role-index tests and drift-checklist requirements were extended.

**Checklist review:** Codex reviewed all 39 items in `governance/drift_checklist.md`:
38 satisfied structurally; the existing P2 inventory breadth item remains open because
there is no in situ dataset row (GEDI is spaceborne lidar). Mission, P1 search scopes,
independent P2/P3/P4 research tracks, P5 composability and P6 audit/promotion boundaries
are preserved. The external `eudr-dmi-gil` catalogue remains a read-only, unverified seed;
its IDs are not Lab `DS-` IDs. Dataset, distribution, portal, reference, model and tool
records stay distinct. Reconciled the data-track search-scope order and human-review
gate, the rubric's optional GEE access examples with ADR 0005, and `research/README.md`'s
outdated in-Lab pipeline description. No inventory or scientific concept was changed.
The existing overview already covers portable roles and round provenance; scope,
phases, ADRs, constraints and diagram content remain unchanged, so regeneration was
unnecessary and the generator's freshness check passed. FAIR/OGC glossary entries added.

**Reconciliation:** Applied the checksum-verified archive outside the repository after
review and a successful `python3 /tmp/forest-cover-discovery-integration/dataset-tool-discovery-subagent/apply_to_forest_cover_lab.py --repo /Users/server/projects/forest-cover-lab --dry-run`,
then ran it without `--dry-run`. Work started from
`804ec26300118e30ef563e06bd59296d5823e70a` on `feature/dataset-tool-discovery`.
The first test run reported 16 failed / 96 passed: one missing standard role contract
marker and 15 failures caused by a stale graph snapshot; the graph check also failed.
Added the required input/output markers. Contrary to the package's expectation,
`docs/downstream_repos.md` is a graph input, so `.venv/bin/python graph/build.py`
regenerated `graph/generated/knowledge.json` and the two illustrative config graph pins
were updated. Exact comparison against the base confirms identical nodes, validated
relationships and candidate relationships; only an input hash and revision changed.
New graph revision: `950e1405aacb2d6459745d7f2e0674890249752ebc952b58ad34bbc7e8e5e146`.
Consumers adopting the merged Lab revision must re-pin their full Lab commit and graph
revision and run their own checks. No downstream file or historical evidence was edited.

**Verification:** Commands below ran from `/Users/server/projects/forest-cover-lab`
using its existing environment unless specified. Final observed results:

- `.venv/bin/python -m pytest --tb=short`: **112 passed**, 0 failed in 4.47 s.
- `.venv/bin/python agent_harness/scripts/validate_round.py --root .`: **2 planned
  manifests passed**, 0 failed; structure only, not proof of execution.
- `.venv/bin/python graph/build.py --check --descriptor configs/downstream.sentinel-monthly.example.json`:
  **PASS**, 68 concepts, 72 validated and 67 candidate relationships; includes graph freshness.
- `.venv/bin/python docs/img/build_overview_diagram.py --check`: **PASS**, SVG current.
- `.venv/bin/python /tmp/forest-cover-discovery-integration/check_markdown_links.py`:
  **PASS**, 153 tracked/new Markdown files, 53 relative file targets, 0 missing targets.
  This temporary static checker excludes fenced code, external URLs and fragment validation;
  it does not make HTTP requests.
- `git diff --check`: **PASS** after removing the overlay's extra EOF blank line.
- From the Sentinel checkout, `.venv/bin/python scripts/validate_agent_rounds.py --lab /Users/server/projects/forest-cover-lab`:
  **PASS**, 0 manifests recorded; no assertion about historical investigations.
- SHA-256 comparison: all six unrelated local files preserved; historical audit content
  preserved byte-for-byte. Only this appended audit entry was revised.

**Open findings:** No live URL audit or discovery-role execution was performed; no external
catalogue was modified, downloaded or imported. Product-specific FAIR/licensing claims
remain unverified leads requiring scoped provider evidence. The field-boundary versus
new-road smoke scenario is a future assignment example in the protocol, not a completed
answer or scientific test. The existing P2 in situ inventory gap needs a separately scoped
source assessment; do not invent an entry to satisfy a structural checklist. The research
guide addition needs issue discussion before merge under `CONTRIBUTING.md`. ADR 0006,
this role addition and scientific promotion retain their human-review gates. Earlier
scientific gaps remain; no scheduler, crawler, model execution or promotion was added.

**Reviewer:** Codex integration and structural review only; human/operator review pending.
Passing checks do not validate scientific candidates. Commit and review-PR publication
are user-authorized; merge is not authorized.


## 2026-10-22 — Candidate agent-governance graph and offline viewer

**Trigger and scope:** User authorized implementation of the preceding recommendations
and an updated KG viewer under outputs. Codex performed integration and structural review;
no subagents, scientific specialist executions, behavioral model trials, commits, PRs or
promotion were performed. Work began from Lab `d67e08354d748f1bd9423af1953de31244671f53` and Sentinel
`bacbea70cf3badb1c137285f827b3570f84c0c22`. The initial Lab tree contained pyproject.toml and five unrelated
untracked files; all six retain their captured pre-change SHA-256 values. Source consultation
preceded SS-0003 registration in the preceding chat; the scope was registered before this
inventory batch. The review explicitly states that chronology without backfilling it.

**Change:** Added SS-0003 / PUB-0013–PUB-0018, a candidate primary-source assessment and
proposed ADR 0007. Added 20 candidate concepts (eight roles, four pinned Sentinel skills,
one harness, two hosts, one capability, two validations and two non-claims) and 37 candidate
relationships. All 72 existing validated and 67 existing candidate relationships are
unchanged; existing non-workflow concept records are identical. The workflow record's
version/date and one candidate governance link changed; scientific method declarations did
not. The graph now has 88 concepts, 72 validated and 104 candidate relationships.
Round schema 1.1 adds explicit delegation/runtime/handoff/independence/event capture and
retains 1.0 compatibility. Historical rounds, runs and review bundles were not rewritten.
Updated standing policy, README, glossary, architecture and generated overview together.
The viewer has a Research governance layer, distinct shapes and Agent contracts entry.

**Drift checklist review:** Reviewed governance/drift_checklist.md against the changed
files and existing track contracts. Mission boundary remains forest-cover estimation and
Lab governance; no competing mission, production processing or observation archive was
added. P1 scope/inventory classification and source-transfer limits are recorded; earlier
unscoped consultation remains an explicit process limitation. P2 dataset/tool separation,
context roles, discovery indexing and external-catalogue boundaries are preserved; the
existing absence of an in-situ category row remains an open inventory gap. P3/P4 code
inventories and reverse-engineering boundaries are preserved; no code-source assessment
or new source-code discovery is claimed. P5 track independence is preserved: governance
contracts are optional and do not require delegation. P6 README/overview/glossary, source
index, proposed ADR and both append-only audits are updated. Human/operator and scientific
review remain pending; structural passes do not promote candidates.

**Observed checks and exact commands:** From the Lab checkout with its existing environment:

- `.venv/bin/python graph/build.py` and `.venv/bin/python graph/update_examples.py`:
  regenerated the graph and illustrative config pins. Final revision `359109d4c2801c71b6cb37026cd0a9b7a1c42a6db5a085f880ecd6919a133062`.
- `.venv/bin/python -m pytest --tb=short`: **132 passed**, 0 failed (7.16 s).
- `.venv/bin/python agent_harness/scripts/validate_round.py --root .`: **2 planned
  example manifests passed**; no execution or scientific validation implied.
- `.venv/bin/python graph/build.py --check --descriptor configs/downstream.sentinel-monthly.example.json`:
  **PASS**, including graph freshness and the illustrative descriptor.
- `.venv/bin/python docs/img/build_overview_diagram.py` then
  `.venv/bin/python docs/img/build_overview_diagram.py --check`: **PASS**.
- `git diff --check`: **PASS** after normalizing the newly appended CSV rows to LF.
- `node --check viewer/templates/common.js`, `node --check viewer/templates/graph.js`
  and `node --check viewer/templates/catalogue.js`: **PASS**.
- `.venv/bin/python viewer/export.py`: exported `outputs/kg-viewer-359109d4c280` and ZIP;
  the bundle declares actual HEAD and dirty state, with fresh graph and file checksums.
- `node /tmp/lab_kg_browser_smoke.cjs`: **PASS** against the final bundle using the
  already cached puppeteer-core and local Chromium. Checked offline deep-link, governance
  layer, role navigation and catalogue role/skill/harness filters; zero page errors;
  external page requests blocked. Sandbox startup initially failed at a macOS Mach-port
  permission boundary; the same local test passed with reviewed escalation. Screenshot
  `/tmp/lab-kg-governance-viewer.png` was visually inspected on the earlier equivalent
  presentation export; the final bundle passed the same interactions.
- Temporary Python comparison: existing relationships/non-workflow concepts and six
  unrelated files preserved; relative Markdown file links resolve (HTTP/fragment
  availability not re-audited). Tests cover exported-file hashes and deterministic ZIPs.
- Optional `.venv/bin/python -m ruff check ...` could not run: ruff is not installed
  in the existing Lab environment. No lint success is claimed.

From the Sentinel checkout:

- `.venv/bin/python scripts/validate_agent_rounds.py --lab /Users/server/projects/forest-cover-lab`:
  **PASS**, zero operational manifests recorded; not validation of historical reviews.
- `.venv/bin/python -m unittest discover -v`: **42 tests run; 38 pass, 4 errors**.
  Each error is a graph/provenance snapshot mismatch with the stale production pin.
  The standalone descriptor check also fails with that explicit reason.
- `.venv/bin/python ../forest-cover-lab/graph/build.py --check --descriptor workflow.yaml`:
  **FAIL**, downstream descriptor has a stale graph revision. A temporary Python
  baseline check loaded `git -C ../forest-cover-lab show HEAD:graph/generated/knowledge.json`
  and confirmed the same mismatch before these edits: Lab baseline
  `950e1405aacb2d6459745d7f2e0674890249752ebc952b58ad34bbc7e8e5e146`,
  downstream pin `3e6dc320bd9f59a483d605d100614005eaa1beb35139edcd1d7d37f04914380a`.
- `.venv/bin/python scripts/create_synthetic_fixture.py --directory /tmp/lab-agent-kg-demo.xT1WlV`
  followed by `.venv/bin/python scripts/run_pipeline.py --manifest /tmp/lab-agent-kg-demo.xT1WlV/workflow.yaml --forest-def /tmp/lab-agent-kg-demo.xT1WlV/forest.yaml --aoi-geojson /tmp/lab-agent-kg-demo.xT1WlV/aoi.geojson`:
  **PASS**, synthetic local pipeline, no EO downloads or model inference.

**Output SHA-256 values:**

- `graph/generated/knowledge.json`: `811a2ac5cd4d00f649c62a2cffccc9d3e1f058a4b0eef7875f0e2faa669ef991`.
- `outputs/kg-viewer-359109d4c280/manifest.json`: `a688a9f06c793469727bd56dfca5e4795b904f3b56ed6e903bb0cbb1d92d8941`.
- `outputs/kg-viewer-359109d4c280.zip`: `40a7923c1b958681ab195eaf10db1ec2548ac51833b4f4a3b514da8270c10b41`.

**Open findings and next adoption step:** ADR 0006 and ADR 0007, host compatibility,
behavioral evaluation and all new graph knowledge remain pending human review. No host
adapter or orchestrator was implemented, and no model/agent independence is inferred.
After committing/reviewing the Lab change, consumers must pin the resulting full commit
and graph revision, review the upstream diff and re-run their tests/demo. Production pins
and old evidence were deliberately not rewritten to describe an uncommitted graph as a
committed snapshot. The Sentinel audit records the same compatibility limitation.

**Reviewer:** Codex structural integration review only; human/operator approval pending.
