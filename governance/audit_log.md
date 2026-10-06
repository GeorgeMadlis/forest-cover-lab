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
