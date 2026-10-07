# Knowledge graph viewer

Exports `graph/generated/knowledge.json` as a self-contained HTML bundle that opens
directly from disk (`file://`) in any modern browser: no server, network or install.

```sh
python graph/build.py          # if the corpus changed
python viewer/export.py        # -> outputs/kg-viewer-<revision12>/ and .zip
open outputs/kg-viewer-*/index.html
```

The bundle contains two linked pages:

- `index.html` — interactive graph. Colour = layer (purpose & assurance, science, data,
  implementation); shape = concept type; dashed edges = candidate relationships. Filter by
  concept type, relation type and validated/candidate status; switch layouts; search; click
  a concept or edge for its full record, context, sources and review metadata.
  `#node=<id>` deep-links to a focused concept.
- `catalogue.html` — sortable, filterable tables of concepts and relationships, with
  expandable context. Concept IDs link back to the graph.

`data.js` embeds the graph plus snapshot metadata (graph revision, Lab commit and dirty
state, freshness); `manifest.json` lists SHA-256 hashes of every bundle file. Exports
are deterministic: an identical graph and commit produce a byte-identical zip.

The exporter refuses a graph that is stale against the corpus unless `--allow-stale` is
given, in which case every page shows a stale banner. It never writes the graph.

This directory sits outside `graph/` on purpose: `graph/build.py` hashes every file under
`graph/` into the snapshot revision, so presentation code there would change the revision
pinned by downstream descriptors. The viewer is a browsing aid; it adds no scientific
authority, and candidate relationships remain candidates.

Cytoscape.js 3.30.2 is vendored under `vendor/` (MIT, see `vendor/cytoscape.LICENSE`).
