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
