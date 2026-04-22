# Publications Research Track

This directory contains the structured literature review for Forest Cover Lab.

## Objective

Identify, compare, and prioritize publications relevant to:

- forest extent / forest cover baselines
- annual forest-loss products and label semantics
- Sentinel-1 / Sentinel-2 forest monitoring
- time-series forest disturbance detection
- weak supervision and noisy labels in EO
- reproducible codebases suitable for adaptation

## Files

| File | Purpose |
|---|---|
| `publications_inventory.csv` | Master inventory of all reviewed papers |
| `publications_scoring_rubric.md` | Scoring rules and interpretation guide |
| `methods_landscape.md` | Thematic synthesis of method families |
| `shortlist.md` | Selected papers and codebases for roadmap phases |

## Review rules

Every paper must be classified for:

- scientific relevance (0–3)
- label match to the repo goal (0–3)
- codeability (0–3)
- reproducibility (0–3)
- operational usefulness (0–3)

Use the schema documented in `publications_scoring_rubric.md` and update `total_score` after review.

## Workflow

1. Add a new row to `publications_inventory.csv` with `status = to_review`.
2. Score all five dimensions after reading.
3. Set `status = reviewed` and `roadmap_fit` to `v1`, `v2`, `v3`, or `reject`.
4. If `total_score >= 12`, add to `shortlist.md`.
5. Update `methods_landscape.md` to reflect any new method families.
