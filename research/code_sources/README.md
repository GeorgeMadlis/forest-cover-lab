# Code Sources Track

This track catalogues and analyses external codebases that solve forest-cover-related tasks.
Code repositories are treated as research artifacts independently of any linked publication.

**Principle:** P3 — Source Code Discovery and Analysis (`governance/principles.md`)
**Principle:** P4 — Source Code Reverse Engineering (`governance/principles.md`)

## Inputs

None required. This track can be entered without completing the literature review or the
data sources track.

Optionally consumes:
- `research/publications/publications_inventory.csv` — papers may have `code_url` entries
  not yet catalogued here; add them when discovered.
- `research/data_sources/inventory.csv` — code may depend on data sources already assessed.
- `research/methodology/research_guide.md` — search protocol applies to code discovery.

## Outputs

### P3 — Discovery
- `inventory.csv` — master catalogue of all evaluated external codebases

### P4 — Reverse engineering
- `analysis/<repo_name>/reverse_engineering.md` — written artifact explaining the scientific
  reasoning embedded in a selected codebase
- Template: `reverse_engineering_template.md`

---

## Files

| File | Purpose |
|---|---|
| `inventory.csv` | Master catalogue of all evaluated codebases |
| `reverse_engineering_template.md` | Template for producing P4 analysis artifacts |
| `analysis/` | Directory of per-repository reverse engineering artifacts |

## Where to find codebases

- GitHub search: `topic:forest-cover`, `topic:deforestation`, `topic:change-detection`
- Conference paper appendices and supplementary material
- Open review platforms (OpenReview, Papers with Code)
- Research lab repositories (GLAD, MapBiomas, JRC, GFW tech teams)
- GEE script repositories and community scripts

## P3 — Discovery workflow

1. Declare or reuse a search scope in `research/methodology/search_scopes.csv`.
2. Add a row to `inventory.csv` with `status = to_review` and the relevant
   `search_scope_id`.
3. Fill all columns.
4. Set `status = reviewed` and fill the suitability columns.
5. If the repo warrants deep analysis (see P4 criteria below), create an entry in
   `analysis/`.

## P4 — When to produce a reverse engineering artifact

Produce a reverse engineering artifact when the codebase:
- Is a strong candidate for adaptation into Forest Cover Lab, **or**
- Embeds scientific assumptions about forest cover that are non-obvious from its README, **or**
- Has been cited in a key publication on the shortlist

One inventory entry in `inventory.csv` does not require a P4 artifact. P4 is selective.

## P4 — Reverse engineering workflow

1. Select a codebase from `inventory.csv` (status = reviewed).
2. Create `analysis/<repo_name>/reverse_engineering.md` using `reverse_engineering_template.md`.
3. Record the commit hash analyzed in the artifact header.
4. Set `reverse_engineered = yes` in `inventory.csv`.

## Rules

- A codebase may be catalogued with or without a linked publication. Code without a paper
  is a valid entry.
- A code entry is not the same as a publications entry — do not duplicate review effort
  between the two inventories.
- Reverse engineering artifacts explain **why** the code does what it does, not **what** it
  does operationally. Comments describing function signatures are not reverse engineering.
- Code that depends on adjacent context products should link those products through
  `research/data_sources/inventory.csv` rather than describing them only in prose.
