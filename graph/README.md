# Derived knowledge graph

The authority is `knowledge/**/*.md` together with existing specs, inventories and contracts.
`ontology.yaml` restricts entity types and identifier prefixes; `relation_types.yaml` defines
allowed typed endpoints. JSON schemas enforce concept and downstream descriptor fields.
No individual scenes, runs or results are accepted entity types.

Install the lightweight validator independently of any reference execution stack:

```sh
python -m pip install -e '.[dev]'
python graph/build.py
python graph/build.py --check
python graph/build.py --check --descriptor configs/downstream.sentinel-monthly.example.json
python -m pytest
```

The generator parses strict YAML front matter, rejects duplicate YAML keys and stable IDs,
checks inventory registration/title drift, sources, review metadata, relationship types,
typed endpoints and unresolved/duplicate references. Validated relations must have active
endpoints and review attribution. Candidate edges stay in a separate collection. Invalid
input stops generation before writing. `--check` never writes the graph.

Output JSON has sorted nodes and edges, full context and paths, separate validated/candidate
relationships, input hashes and a revision SHA-256. The revision hashes concept files,
local sources and graph rules/schemas/generator. It excludes output, environment, current Git
commit and timestamps; a Forest Cover Lab commit/tag is recorded separately. Reordering
relations does not alter edge order, although any source-file byte change alters its snapshot
hash. SHA-256 identifies a snapshot; it is not evidence of scientific validation.

Downstream descriptor validation checks schema, typed reference resolution, local validation
and reporting contracts and snapshot freshness. It validates a declaration, not installed
software, executed tests or method equivalence. Proposed examples remain proposed. Consumers
must explicitly gate candidate nodes/edges; the build does not promote them.

To edit: update corpus/contracts, regenerate, update example snapshot hashes with
`python graph/update_examples.py`, and run tests plus `--check`. Never edit generated JSON
as an independent scientific record. A workflow run cannot write canonical knowledge.
