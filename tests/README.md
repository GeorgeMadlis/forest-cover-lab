# Tests

Unit and integration tests for Forest Cover Lab contracts.

Tests here verify shared schemas, examples, governance expectations, and reference behavior.
Pipeline-specific tests belong in downstream repos, while still referencing this repo's
contracts.

## Planned minimum tests (Phase 2)

| Test file | Scope |
|---|---|
| `test_geometry_area.py` | Geometry validity, CRS round-trip, hectare conversion |
| `test_manifest_schema.py` | `run_manifest.json` validates against schema |
| `test_config_loading.py` | Configs load and contain required keys |
| `test_v1_threshold.py` | Threshold sensitivity and datamask exclusion |
| `test_v1_integration_small_aoi.py` | End-to-end small-AOI integration test |

## Conventions

- `pytest` is the test runner.
- Tests must not require network access by default; integration tests may use cached fixtures under `tests/fixtures/`.
- Tests must run in < 5 minutes total locally (excluding the small-AOI integration test, which has a 10-minute budget).
