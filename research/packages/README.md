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

The [dataset/tool discovery specialist](../../agent_harness/roles/dataset-and-tool-discovery.md) can propose APIs, STAC/OGC discovery services, data readers, model toolchains and cloud-array services. See the [shared protocol](../data_sources/discovery_and_link_verification.md) for source evidence and access constraints. Register **tools/software** here, not as duplicate scientific datasets. Discovery alone does not approve production use.

## Workflow

1. Add a new row to `packages_matrix.csv` with `status = to_review`.
2. Fill all comparison columns.
3. Add a qualitative note section to `packages_notes.md`.
4. After human review, set `status = reviewed` and `recommended_role` to `default`, `fallback`, `research-only`, `candidate`, or `reject`. Tool review does not promote scientific concepts or authorize pipeline execution.
5. Update `platform_decision.md` if the recommendation set changes.

Current execution policy is ADR 0005. Reusable, documented tool operations are indexed in
`knowledge/tools/` and `knowledge/capabilities/`; these do not add runtime dependencies.
The matrix retains assessments but GEE/geemap roles are optional research/reference.
