# Architecture Decision Records

This directory stores Architecture Decision Records (ADRs) for Forest Cover Lab.

## Purpose

ADRs capture durable technical and methodological decisions that affect:

- algorithm selection
- data source policy
- forest definitions
- area computation
- monthly target semantics
- validation requirements
- platform choices

## Rules

- One ADR per material decision.
- ADRs must be immutable once accepted, except by superseding ADR.
- Each ADR must state:
  - status
  - context
  - decision
  - consequences
  - alternatives considered
- If a decision changes, create a new ADR and reference the old one.

## Naming convention

`NNNN-short-title.md`

Examples:

- `0001-default-platform.md`
- `0002-forest-definition.md`
- `0003-area-computation-policy.md`
- `0004-monthly-target-definition.md`

## Status values

- Proposed
- Accepted
- Superseded
- Deprecated
- Rejected
