# Governance

This directory holds the canonical governance artifacts for Forest Cover Lab.

## Files

| File | Purpose |
|---|---|
| `principles.md` | The six canonical principles - the reference for all repo decisions |
| `drift_checklist.md` | Checklist run after every structural change and quarterly |
| `audit_log.md` | Append-only log of checklist runs and findings |

## Rules

- `principles.md` is the source of truth. If it contradicts a README, the README is wrong.
- The primary mission is forest cover estimation; adjacent Earth-observation products are
  admitted only as context, auxiliary, validation, exclusion, or interpretation evidence.
- This repo governs, explains, and collects reusable evidence for downstream repos; it does
  not need to contain every narrow implementation pipeline.
- `drift_checklist.md` must be run and recorded in `audit_log.md` for every structural
  change to the repository.
- Findings of divergence are defects. Resolve them before or immediately after the change
  that introduced them.
- Do not add decision-specific content here. Per-decision records belong in `docs/adr/`.
