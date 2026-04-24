# Drift Checklist

Run this checklist after any structural change to the repository and at least once per
quarter. Record each run and its findings in `audit_log.md`.

A finding of **No** on any item is a defect. Resolve it before or immediately after
the change that introduced the divergence.

---

## Mission boundary

- [ ] Does the repository still state forest cover estimation as the primary mission?
- [ ] Does the repository still state that it governs, explains, and collects reusable
      data-source evidence for downstream repos rather than implementing every narrow
      pipeline itself?
- [ ] Are adjacent EO products recorded as context, validation, auxiliary, exclusion, or
      interpretation evidence rather than as a competing mission?

---

## P1 — Research Protocol and Evidence Capture

- [ ] Does `research/methodology/research_guide.md` exist and define how to declare a search
      scope before entering any research track?
- [ ] Does `research/methodology/search_scopes.csv` exist and provide reusable scope IDs
      for inventories?
- [ ] Does the guide cover how to search for papers, blogs, and technical reports?
- [ ] Does `research/methodology/practitioner_sources.md` exist with a curated list of
      practitioner sources (including the GEE blog and Sentinel Hub blog)?
- [ ] Does the publications track require a `search_scope_id` record before new entries are
      accepted?
- [ ] Are blogs and technical reports classified separately from peer-reviewed papers
      in the publications inventory?

---

## P2 — Data and Context Product Suitability

- [ ] Does `research/data_sources/` exist as a dedicated top-level research track?
- [ ] Does `research/data_sources/inventory.csv` include entries spanning satellite,
      in situ, and fusion product categories?
- [ ] Does the inventory include `evidence_role`, `domain`, `forest_relevance`,
      `source_priority`, and `search_scope_id` columns?
- [ ] Does `research/data_sources/context_products.md` define how biodiversity, ocean/coastal,
      energy, integrity, flood, fire, climate, and other context products are admitted?
- [ ] Does `research/data_sources/suitability_rubric.md` define phase-by-phase suitability
      criteria for v1, v2, and v3?
- [ ] Is data source evaluation kept separate from package/tool evaluation in
      `research/packages/`?
- [ ] Does the data sources track README state what it assumes, what it produces, and which
      other tracks it optionally consumes?

---

## P3 — Source Code Discovery and Analysis

- [ ] Does `research/code_sources/` exist as a dedicated top-level research track?
- [ ] Does `research/code_sources/inventory.csv` catalogue codebases independently of
      papers (a codebase may have no linked publication)?
- [ ] Does the code inventory include `search_scope_id` so discovery can be traced to a
      declared search?
- [ ] Does the code discovery workflow include non-paper sources (GitHub search,
      lab repositories, conference appendices)?
- [ ] Does the code sources track README state what it assumes, what it produces, and which
      other tracks it optionally consumes?

---

## P4 — Source Code Reverse Engineering

- [ ] Does `research/code_sources/reverse_engineering_template.md` exist?
- [ ] Does the template require analysis of: (a) forest definition assumptions,
      (b) algorithmic scientific judgments, (c) hidden implementation limitations,
      (d) paper-to-code divergences?
- [ ] Is the reverse engineering artifact stored separately from the code inventory row
      (i.e. in `research/code_sources/analysis/<repo_name>/`)?
- [ ] Is there a `.gitkeep` or example entry in `research/code_sources/analysis/` so the
      directory exists in git history?

---

## P5 — Section Independence and Composability

- [ ] Does each of the four track READMEs (methodology, data_sources, code_sources,
      publications) declare its inputs, outputs, and optional cross-track dependencies?
- [ ] Can `research/data_sources/` be entered without a complete literature review?
- [ ] Can `research/code_sources/` be entered without completing either the literature
      review or the data source track?
- [ ] Can `research/code_sources/analysis/` (P4) be entered by selecting any entry from
      the `code_sources/inventory.csv` without completing other tracks?

---

## P6 — Architecture Drift Control

- [ ] Does `governance/principles.md` exist and contain all six principles?
- [ ] Does `README.md` reference `governance/` as the canonical principle source?
- [ ] Does `docs/architecture.md` exist and reflect the current architecture assessment?
- [ ] Does `docs/downstream_repos.md` exist and define how narrower repos consume this
      repo's contracts?
- [ ] Has this checklist been run and recorded in `audit_log.md` within the last quarter?
- [ ] Does `audit_log.md` contain an entry for the most recent structural change?
- [ ] Are all open findings from the most recent audit either resolved or tracked?
