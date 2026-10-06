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
