# Agent instructions — Forest Cover Lab

These instructions apply to any coding or research agent (Claude Code, Codex, Copilot)
working in this repository. `CLAUDE.md` imports this file.

## What this repository is

Forest Cover Lab is the **scientific, governance and semantic authority** for a family of
forest-cover repositories. It defines contracts and collects evidence; it does not run
pipelines or store run outputs. Executable workflows live in downstream repos, currently
[`sentinel-monthly-forest-cover`](https://github.com/GeorgeMadlis/sentinel-monthly-forest-cover)
(see `docs/downstream_repos.md`).

Read before changing anything:

1. `governance/principles.md` — the six canonical principles (P1–P6) and the mission boundary
2. `docs/architecture.md` — current architecture assessment
3. `docs/adr/` — durable decisions; ADR 0005 supersedes ADR 0001's platform policy

## Non-negotiable rules

- **Hansen annual loss ≠ monthly ground truth.** Never claim monthly forest cover as verified
  when it is derived from annual weak labels. Keep this warning wherever it already appears.
- **Forest definition** (ADR 0002): every workflow declares dataset, threshold variable and
  value, minimum mapping area, exclusions, nodata policy and temporal interpretation.
  Defaults live in `configs/v1_defaults.yaml`; never hardcode thresholds.
- **Area** (ADR 0003): exchange in EPSG:4326; compute in an equal-area CRS (EPSG:6933 for
  global AOIs) or with an explicit geodesic method; report hectares and state the method.
- **Monthly targets** (ADR 0004): monthly coverage estimate, monthly disturbance probability
  and annual weak supervision are distinct concepts.
- **Backends** (ADR 0005): production methods must not depend on Google Earth Engine. Prefer
  open, local, cloud-neutral tooling. GEE is optional reference/research code only.
- **Provenance**: run manifests follow `validate/run_manifest.schema.json`; downstream runs add
  the semantic provenance block described in `validate/semantic_provenance.md`.
- **Knowledge promotion** (`governance/knowledge_promotion.md`): anything an agent extracts or
  proposes enters as `status: candidate`. Never change a candidate to validated, alter a
  canonical concept, threshold or claim, or treat a successful run as scientific validation.
  Promotion requires human review (`review.by`, `review.date`, `review.basis`).
- **Stable IDs**: reuse existing `DS-`, `PUB-`, `CS-` and `SS-` identifiers; never renumber.
  Declare a search scope in `research/methodology/search_scopes.csv` before adding inventory
  entries (P1).
- Do not present evidence-role context products (biodiversity, flood, energy, etc.) as a
  competing mission; they are context, validation, auxiliary or exclusion evidence.

## Checks to run

No Earth-observation downloads or backends are needed:

```sh
python -m pip install -e '.[dev]'
python graph/build.py --check
python -m pytest
```

If you edit anything under `knowledge/`, `graph/` or an input listed in
`graph/generated/knowledge.json` (`input_hashes`), regenerate with `python graph/build.py`
and commit the updated `graph/generated/knowledge.json`. A changed graph revision means
downstream descriptors must re-pin; say so in the PR description.

To check a downstream repo cloned alongside this one:

```sh
python graph/build.py --check --descriptor ../sentinel-monthly-forest-cover/workflow.yaml
```

## Structural changes

After any structural change (new directory, track, contract, schema, ADR or agent-facing
instruction), run `governance/drift_checklist.md` and append an entry to
`governance/audit_log.md` (append-only; trigger, checklist result, open findings, reviewer,
verification). Drift is a defect: fix it in the same change or record it as an open finding.

## README and overview diagram

`README.md` and its overview diagram (`docs/img/problems-and-approaches.svg`) must reflect
the repository's current scope. Whenever a change affects the scope, phases, ADRs, binding
constraints, problems addressed or other significant details, update both in the same
change:

1. Edit the content section of `docs/img/build_overview_diagram.py` (never hand-edit the
   SVG) and run `python docs/img/build_overview_diagram.py`.
2. Update the README text, and `GLOSSARY.md` for any new abbreviation.
3. Commit the script, the regenerated SVG and the README together.

`tests/test_overview_diagram.py` fails if the SVG is stale, a cited source is missing, a
non-superseded ADR is not cited or the roadmap differs from the phase specs in `specs/`.

## Conventions

- Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `research:`.
- Branches: `feature/…`, `fix/<issue>`, `research/<topic>`, `docs/…`.
- One coherent change per PR (one ADR, one paper batch, one spec refinement…).
- ADR files: `docs/adr/NNNN-short-title.md`; accepted ADRs change only by superseding ADR.
- Notebooks are exploratory only and committed without outputs (`nbstripout`).
- Area numbers always state hectares, CRS and method; forest claims always state threshold,
  dataset version and date.
