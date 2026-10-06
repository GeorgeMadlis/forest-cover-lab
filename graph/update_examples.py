"""Refresh proposed example snapshot hashes after a reviewed corpus change."""

import json
import subprocess

from build import ROOT, canonical_bytes, generate


def main():
    graph = generate()
    source_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    snapshot = {
        "forest_cover_lab_revision": source_commit,
        "graph_revision": graph["revision"],
    }
    for filename in [
        "downstream.sentinel-monthly.example.json",
        "run_manifest.semantic.example.json",
    ]:
        path = ROOT / "configs" / filename
        example = json.loads(path.read_text())
        if "semantic_provenance" in example:
            example["semantic_provenance"]["knowledge_snapshot"] = snapshot
        else:
            example["knowledge_snapshot"] = snapshot
        path.write_bytes(canonical_bytes(example))


if __name__ == "__main__":
    main()
