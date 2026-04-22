# Configuration

This directory holds versioned configuration files. **Never hardcode thresholds or dataset versions in scripts** — read them from this directory.

## Files

| File | Purpose |
|---|---|
| `v1_defaults.yaml` | Default parameters for v1 baseline runs |
| `forest_definition.example.yaml` | Example forest definition; copy and adapt per AOI |
| `run_manifest.example.json` | Example of the run manifest emitted by every run |

## Rules

- Every parameter that affects scientific interpretation lives here.
- Configs are versioned with the repo; changes require a PR.
- The active config used in a run must be hashed and recorded in the run manifest.
