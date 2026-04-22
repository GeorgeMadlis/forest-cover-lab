# Packages and Platforms Research Track

This directory contains the comparison of software packages, platforms, and reference-data systems relevant to Forest Cover Lab.

## Objective

Compare candidate tools for:

- v1 baseline forest-cover estimation
- v2 monthly time-series processing
- v3 weakly supervised research workflows

## Files

| File | Purpose |
|---|---|
| `packages_matrix.csv` | Master comparison table |
| `packages_notes.md` | Tool-by-tool qualitative notes |
| `platform_decision.md` | Default / fallback / research-only recommendation |

## Review rules

Each entry should be assessed for:

- execution model (cloud, local, hybrid)
- sensor support (Sentinel-1, Sentinel-2, Landsat)
- reproducibility
- scalability
- fit for each roadmap phase
- operational complexity

Use qualitative levels consistently:

- `low`
- `medium`
- `high`

## Workflow

1. Add a new row to `packages_matrix.csv` with `status = to_review`.
2. Fill all comparison columns.
3. Add a qualitative note section to `packages_notes.md`.
4. Set `status = reviewed` and `recommended_role` to `default`, `fallback`, `research-only`, `candidate`, or `reject`.
5. Update `platform_decision.md` if the recommendation set changes.
