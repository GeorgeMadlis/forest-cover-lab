# Contributing to Forest Cover Lab

Thank you for contributing.

## What belongs in this repo

Contributions are welcome for:

- literature review and evidence synthesis
- package and platform comparison
- method specifications
- architecture decision records
- validation plans
- reporting contracts
- reproducible geospatial processing code

## What must be explicit

Any contribution affecting outputs or interpretation must document:

- the target phase: v1, v2, or v3
- data source(s)
- forest-definition assumptions
- CRS and area method
- limitations and uncertainty
- whether the change affects scientific interpretation

## Pull request guidance

Please keep changes scoped.

A PR should generally do one of these:

- add or revise one ADR
- add or review one paper or paper batch
- add or review one package or package batch
- refine one spec
- add one coherent unit of implementation
- improve validation or reporting contracts

## Review checklist

Before submitting:

- update docs if behavior or meaning changes
- keep names and schemas consistent
- do not hard-code unexplained thresholds
- do not present annual labels as monthly ground truth
- do not report area without documenting the method

## Commit style

Prefer clear commit messages, for example:

- `docs: add ADR for forest definition`
- `research: add first package comparison matrix`
- `specs: refine v2 monthly confirmation requirements`

## Issues

Use the issue templates for:

- method research
- package evaluation
- ADR proposals

## Code quality

When code is added later:

- keep functions small and testable
- document configuration inputs
- avoid notebook-only logic for core processing
- preserve reproducibility of outputs
