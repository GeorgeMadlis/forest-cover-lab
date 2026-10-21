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
