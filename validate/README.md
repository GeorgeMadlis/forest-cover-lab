# Validate

This directory defines validation rules, schemas, and the validation contract for Forest Cover Lab.

## Responsibilities

- manifest schema validation (`run_manifest.schema.json`)
- geometry and area unit tests
- integration test requirements
- external comparison hooks
- temporal plausibility review requirements (v2/v3)

## Files

| File | Purpose |
|---|---|
| `run_manifest.schema.json` | JSON Schema for `run_manifest.json` |
| `validation_plan.md` | Validation requirements and test design |

## Rule

A run without a valid `run_manifest.json` is **not considered complete**.
