# Docs

Project-level documentation for Forest Cover Lab.

## Subdirectories

| Path | Purpose |
|---|---|
| `architecture.md` | Current architecture, GeoFM candidates, six-step evaluation and harness/agent assessment |
| `downstream_repos.md` | Contract for narrower implementation and validation repositories |
| `agents.md` | Standing host/role policy and stable contract index; rounds self-inventory, including the dataset/tool discovery role |
| `../research/data_sources/discovery_and_link_verification.md` | Dataset/tool discovery, FAIR appraisal, scoped link checks and pipeline-Q&A protocol |
| `img/` | README figures and the script that generates the overview diagram |
| `adr/` | Architecture Decision Records — durable technical and methodological decisions |

## Rules

- Substantive decisions belong in `adr/` as numbered ADRs, not in free-form notes.
- `architecture.md` may describe gaps and target structure, but it does not replace ADRs.
- This top-level `docs/` directory may host high-level guides and indexes once the project
  grows beyond the planning milestone.
