"""Validate the authoritative corpus and deterministically derive its graph.

Run from any directory: python /path/to/repo/graph/build.py [--check].
No catalogue queries, execution backends, or graph service are used.
"""

import argparse
import csv
import datetime
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


class KnowledgeError(ValueError):
    """Invalid scientific knowledge or downstream reference."""


class UniqueLoader(yaml.SafeLoader):
    """Reject ambiguous YAML keys rather than silently taking the last value."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise KnowledgeError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def load_yaml(text):
    # Keep ISO dates as strings so JSON serialization and schema checks are stable.
    class StringDateLoader(UniqueLoader):
        pass

    StringDateLoader.yaml_implicit_resolvers = {
        key: [
            (tag, regex) for tag, regex in value if tag != "tag:yaml.org,2002:timestamp"
        ]
        for key, value in UniqueLoader.yaml_implicit_resolvers.items()
    }
    try:
        return yaml.load(text, Loader=StringDateLoader)
    except yaml.YAMLError as exc:
        raise KnowledgeError(f"Invalid YAML: {exc}") from exc


def validate_schema(instance, schema, label):
    checker = jsonschema.FormatChecker()

    @checker.checks("date-time")
    def timestamp(value):
        if not isinstance(value, str):
            return True
        if not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}[Tt][0-9]{2}:[0-9]{2}:[0-9]{2}"
            r"(?:\.[0-9]+)?(?:[Zz]|[+-][0-9]{2}:[0-9]{2})",
            value,
        ):
            return False
        try:
            datetime.datetime.fromisoformat(value.upper().replace("Z", "+00:00"))
        except ValueError:
            return False
        return True

    try:
        jsonschema.Draft202012Validator(schema, format_checker=checker).validate(
            instance
        )
    except jsonschema.ValidationError as exc:
        raise KnowledgeError(f"{label}: {exc.message}") from exc


def parse_document(path, schema):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise KnowledgeError(f"{path}: missing YAML front matter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise KnowledgeError(f"{path}: unclosed YAML front matter") from exc
    document = load_yaml("\n".join(lines[1:end]))
    validate_schema(document, schema, str(path))
    body = "\n".join(lines[end + 1 :]).strip()
    if not body:
        raise KnowledgeError(f"{path}: explanatory context is required")
    if document["review_after"] < document["updated"]:
        raise KnowledgeError(f"{path}: review_after precedes updated")
    return document, body


def validate_sources(sources, root):
    for source in sources:
        url = urlparse(source)
        if url.scheme in {"https", "http"} and url.netloc:
            continue  # Documentation retrieval is a review activity, not a build step.
        path = (root / source).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise KnowledgeError(f"Unresolved source: {source}")


def canonical_bytes(value):
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode()


def check_acyclic(edges, relation):
    """Method composition must not be circular (validated or candidate)."""
    graph = {}
    for edge in edges:
        if edge["type"] == relation:
            graph.setdefault(edge["source"], []).append(edge["target"])
    state = {}

    def visit(node, path):
        if state.get(node) == "done":
            return
        if state.get(node) == "active":
            raise KnowledgeError(f"Cyclic {relation}: {' -> '.join(path + [node])}")
        state[node] = "active"
        for target in graph.get(node, []):
            visit(target, path + [node])
        state[node] = "done"

    for node in sorted(graph):
        visit(node, [])


def workflow_targets(graph, workflow_id):
    """All targets declared on a workflow record, by relation type and any status."""
    targets = {}
    for edge in graph["relationships"] + graph["candidate_relationships"]:
        if edge["source"] == workflow_id:
            targets.setdefault(edge["type"], set()).add(edge["target"])
    return targets


def generate(root=ROOT):
    root = Path(root)
    schema = json.loads((root / "graph/schemas/concept.schema.json").read_text())
    ontology = load_yaml((root / "graph/ontology.yaml").read_text())
    relations = load_yaml((root / "graph/relation_types.yaml").read_text())
    inventory = {
        row["id"]: row
        for row in csv.DictReader(
            (root / "research/data_sources/inventory.csv").open(encoding="utf-8")
        )
    }
    nodes = {}
    inputs = []
    for path in sorted((root / "knowledge").rglob("*.md")):
        if path.name in {"README.md", "index.md"}:
            continue
        doc, body = parse_document(path, schema)
        identifier = doc["id"]
        kind = doc["type"]
        if identifier in nodes:
            raise KnowledgeError(f"Duplicate identifier: {identifier}")
        prefix = ontology["types"].get(kind)
        separator = "-" if kind == "dataset" else ":"
        if not prefix or not identifier.startswith(prefix + separator):
            raise KnowledgeError(f"Identifier/type mismatch: {identifier} ({kind})")
        if kind == "dataset" and identifier not in inventory:
            raise KnowledgeError(f"Unregistered dataset: {identifier}")
        if kind == "dataset" and doc["title"] != inventory[identifier]["name"]:
            raise KnowledgeError(f"Dataset title drift: {identifier}")
        validate_sources(doc["sources"], root)
        relative = path.relative_to(root).as_posix()
        nodes[identifier] = {**doc, "path": relative, "context": body}
        inputs.append(relative)
    if not nodes:
        raise KnowledgeError("Empty knowledge corpus")
    edges = []
    seen = set()
    for identifier, node in sorted(nodes.items()):
        for edge in node.pop("relations"):
            target = nodes.get(edge["target"])
            if target is None:
                raise KnowledgeError(f"Unresolved reference: {edge['target']}")
            rule = relations.get(edge["type"])
            if rule is None:
                raise KnowledgeError(f"Unknown relationship: {edge['type']}")
            if (
                node["type"] not in rule["source_types"]
                or target["type"] not in rule["target_types"]
            ):
                raise KnowledgeError(
                    f"Invalid relationship endpoints: {identifier} {edge}"
                )
            key = (identifier, edge["type"], edge["target"])
            if key in seen:
                raise KnowledgeError(f"Duplicate relationship: {key}")
            seen.add(key)
            if edge["status"] == "validated" and (
                node["status"] != "active" or target["status"] != "active"
            ):
                raise KnowledgeError(
                    f"Validated relation uses non-active concept: {key}"
                )
            validate_sources(edge["sources"], root)
            edges.append({"source": identifier, **edge})
    edges.sort(key=lambda e: (e["source"], e["type"], e["target"]))
    titles = {}
    for identifier, node in nodes.items():
        if node["type"] == "dataset":
            if node["title"] in titles:
                raise KnowledgeError(
                    f"Duplicate dataset entity: {identifier} and {titles[node['title']]}"
                )
            titles[node["title"]] = identifier
    check_acyclic(edges, "USES_METHOD")
    # Include cited local contracts and graph rules/schemas in the snapshot digest.
    # Exclude run outputs, timestamps, and the current Git commit (avoids self-reference).
    sources = {source for node in nodes.values() for source in node["sources"]}
    sources.update(source for edge in edges for source in edge["sources"])
    inputs.extend(source for source in sources if not urlparse(source).scheme)
    inputs.extend(
        path.relative_to(root).as_posix()
        for path in (root / "graph").rglob("*")
        if path.is_file()
        and "generated" not in path.parts
        and "__pycache__" not in path.parts
    )
    inputs = sorted(set(inputs))
    hashes = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in inputs
    }
    revision = hashlib.sha256(canonical_bytes(hashes)).hexdigest()
    return {
        "schema_version": "1.0",
        "revision": revision,
        "input_hashes": hashes,
        "nodes": [nodes[key] for key in sorted(nodes)],
        "relationships": [e for e in edges if e["status"] == "validated"],
        "candidate_relationships": [e for e in edges if e["status"] == "candidate"],
    }


def validate_descriptor(descriptor, graph, root=ROOT):
    schema = json.loads(
        (Path(root) / "graph/schemas/downstream.schema.json").read_text()
    )
    validate_schema(descriptor, schema, "downstream descriptor")
    nodes = {n["id"]: n for n in graph["nodes"]}
    fields = {
        "workflow_id": "workflow",
        "implemented_method_ids": "method",
        "observation_ids": "observation",
        "dataset_ids": "dataset",
        "tool_ids": "tool",
        "capability_ids": "capability",
        "validation_ids": "validation",
    }
    for field, kind in fields.items():
        ids = [descriptor[field]] if field == "workflow_id" else descriptor[field]
        for identifier in ids:
            if identifier not in nodes or nodes[identifier]["type"] != kind:
                raise KnowledgeError(f"Unresolved or mistyped {field}: {identifier}")
    # A downstream declaration may not exceed what the canonical workflow record
    # registers; new implementation relationships are proposed here first.
    declared = workflow_targets(graph, descriptor["workflow_id"])
    backing = {
        "implemented_method_ids": "IMPLEMENTS",
        "observation_ids": "REQUIRES_OBSERVATION",
        "dataset_ids": "CONSUMES",
        "tool_ids": "USES_TOOL",
        "capability_ids": "REQUIRES_CAPABILITY",
        "validation_ids": "REQUIRES_VALIDATION",
    }
    for field, relation in backing.items():
        missing = sorted(set(descriptor[field]) - declared.get(relation, set()))
        if missing:
            raise KnowledgeError(
                f"{field} not registered as {relation} on "
                f"{descriptor['workflow_id']}: {', '.join(missing)}"
            )
    provided = {
        edge["target"]
        for edge in graph["relationships"] + graph["candidate_relationships"]
        if edge["type"] == "CAN" and edge["source"] in descriptor["tool_ids"]
    }
    unprovided = sorted(set(descriptor["capability_ids"]) - provided)
    if unprovided:
        raise KnowledgeError(
            f"capability_ids not provided by declared tool_ids: {', '.join(unprovided)}"
        )
    validate_sources(descriptor["validation_contracts"], Path(root))
    validate_sources(descriptor["reporting_contracts"], Path(root))
    snapshot = descriptor["knowledge_snapshot"]
    if snapshot["graph_revision"] != graph["revision"]:
        raise KnowledgeError("Downstream descriptor has a stale graph revision")
    return descriptor


def validate_provenance(manifest, graph, root=ROOT):
    """Check an extended manifest against its pinned semantic snapshot."""
    schema = json.loads((Path(root) / "validate/run_manifest.schema.json").read_text())
    validate_schema(manifest, schema, "run manifest")
    provenance = manifest.get("semantic_provenance")
    if provenance is None:
        return manifest
    if provenance["knowledge_snapshot"]["graph_revision"] != graph["revision"]:
        raise KnowledgeError("Run manifest has a different graph revision")
    nodes = {n["id"]: n for n in graph["nodes"]}
    for field, kind in [("methods", "method"), ("tools", "tool")]:
        for item in provenance[field]:
            node = nodes.get(item["id"])
            if node is None or node["type"] != kind:
                raise KnowledgeError(f"Unresolved {field}: {item['id']}")
            # Tool versions are installed software versions, not concept versions.
            if kind == "method" and item["version"] != node["version"]:
                raise KnowledgeError(f"Method version mismatch: {item['id']}")
    workflow = nodes.get(provenance["workflow"]["id"])
    if workflow is None or workflow["type"] != "workflow":
        raise KnowledgeError("Unresolved workflow implementation")
    declared = workflow_targets(graph, workflow["id"])
    for field, relation in [("methods", "IMPLEMENTS"), ("tools", "USES_TOOL")]:
        for item in provenance[field]:
            if item["id"] not in declared.get(relation, set()):
                raise KnowledgeError(
                    f"{item['id']} is not registered as {relation} on {workflow['id']}"
                )
    for identifier in provenance["concept_ids"]:
        if identifier not in nodes:
            raise KnowledgeError(f"Unresolved concept: {identifier}")
    for identifier in provenance["dataset_ids"]:
        if identifier not in nodes or nodes[identifier]["type"] != "dataset":
            raise KnowledgeError(f"Unresolved dataset: {identifier}")
    data_ids = {item["inventory_id"] for item in manifest["data_provenance"]}
    if data_ids != set(provenance["dataset_ids"]):
        raise KnowledgeError("Selected dataset IDs disagree with data_provenance")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Fail if generated JSON differs"
    )
    parser.add_argument(
        "--descriptor", type=Path, help="Validate a downstream JSON/YAML descriptor"
    )
    args = parser.parse_args()
    try:
        graph = generate()
        output = canonical_bytes(graph)
        path = ROOT / "graph/generated/knowledge.json"
        if args.check:
            if not path.exists() or path.read_bytes() != output:
                raise KnowledgeError("Generated graph is stale; run graph/build.py")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(output)
        if args.descriptor:
            # Descriptors may be JSON or YAML; YAML parsing is strict and JSON-compatible.
            validate_descriptor(load_yaml(args.descriptor.read_text()), graph)
    except (KnowledgeError, OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print(
        f"{len(graph['nodes'])} concepts; "
        f"{len(graph['relationships'])} validated and "
        f"{len(graph['candidate_relationships'])} candidate relationships; "
        f"revision {graph['revision']}"
    )


if __name__ == "__main__":
    main()
