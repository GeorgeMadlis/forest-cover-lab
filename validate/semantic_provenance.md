# Semantic provenance extension (1.0)

`run_manifest.schema.json` retains its existing required fields. Legacy manifests without
`semantic_provenance` remain valid. The optional 1.0 block requires:

- method IDs and versions (`methods`)
- Forest Cover Lab commit/tag and graph SHA-256 (`knowledge_snapshot`)
- relevant concept IDs and selected dataset IDs
- tool/backend IDs and versions (`tools`)
- workflow implementation ID and version (`workflow`)
- whether an AI planner was involved; `planning_record_id` is mandatory if true

When the block is present every `data_provenance` entry also requires its inventory ID,
dataset version and UTC access timestamp. Existing top-level `parameters` and `limitations`
carry configured choices and caveats. Reports must include this block when supplied and
retain all monthly and weak-supervision disclaimers. Never infer legality or validated
monthly truth from a semantic reference or successful schema validation.

See `configs/run_manifest.semantic.example.json`. Its example revision points to the
pre-change source commit and generated snapshot; a real run must pin the actual consumed
Forest Cover Lab commit/tag and implementation version. Catalogue queries, selected scene
IDs, execution outputs, access timestamps and AI plan records belong in downstream evidence.
They are not canonical knowledge concepts.

JSON Schema checks structure and date/time format. It cannot independently resolve a graph
snapshot. `graph/build.py` provides `validate_provenance` for checking method/concept/dataset/
tool/workflow IDs and versions against the pinned graph and consistency with data_provenance.
For historical runs load their pinned graph rather than today's graph. Limitations and
parameters remain scientifically reviewed; empty or incomplete prose is not cured by a
structurally valid manifest.
