import copy
import importlib.util
import json
import shutil
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "knowledge_build", ROOT / "graph/build.py"
)
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


@pytest.fixture
def repo(tmp_path):
    for directory in [
        "knowledge",
        "graph",
        "research",
        "docs",
        "specs",
        "validate",
        "report",
        "governance",
    ]:
        shutil.copytree(
            ROOT / directory,
            tmp_path / directory,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
    return tmp_path


def edit_record(repo, mutate, identifier="method:monthly-compositing"):
    path = next(
        p
        for p in (repo / "knowledge").rglob("*.md")
        if f"id: {identifier}\n" in p.read_text()
    )
    header, body = path.read_text().split("---\n", 2)[1:]
    record = yaml.safe_load(header)
    mutate(record)
    path.write_text("---\n" + yaml.safe_dump(record) + "---\n" + body)
    return path


def test_parse_document():
    schema = json.loads((ROOT / "graph/schemas/concept.schema.json").read_text())
    path = ROOT / "knowledge/datasets/DS-0002.md"
    doc, body = build.parse_document(path, schema)
    assert doc["id"] == "DS-0002"
    assert doc["updated"] == "2026-10-06"
    assert "Cloud masking" in body


@pytest.mark.parametrize("text", ["# no header", "---\nid: x", "---\n[]\n---\nbody"])
def test_invalid_document(tmp_path, text):
    path = tmp_path / "bad.md"
    path.write_text(text)
    schema = json.loads((ROOT / "graph/schemas/concept.schema.json").read_text())
    with pytest.raises(build.KnowledgeError):
        build.parse_document(path, schema)


def test_duplicate_yaml_keys():
    with pytest.raises(build.KnowledgeError, match="Duplicate YAML key"):
        build.load_yaml("id: a\nid: b")


def test_unique_ids(repo):
    path = repo / "knowledge/datasets/DS-0002.md"
    shutil.copy(path, path.with_name("duplicate.md"))
    with pytest.raises(build.KnowledgeError, match="Duplicate identifier"):
        build.generate(repo)


@pytest.mark.parametrize("bad_id", ["scene:sentinel-2-item", "DS-2", "method:BAD"])
def test_stable_id_rules(repo, bad_id):
    edit_record(repo, lambda d: d.update(id=bad_id))
    with pytest.raises(build.KnowledgeError):
        build.generate(repo)


@pytest.mark.parametrize("kind", ["UNKNOWN", "CONSUMES"])
def test_relation_types_and_endpoints(repo, kind):
    edit_record(repo, lambda d: d["relations"][0].update(type=kind))
    with pytest.raises(build.KnowledgeError, match="relationship"):
        build.generate(repo)


def test_unresolved_reference(repo):
    edit_record(repo, lambda d: d["relations"][0].update(target="observation:missing"))
    with pytest.raises(build.KnowledgeError, match="Unresolved reference"):
        build.generate(repo)


def test_duplicate_relationship(repo):
    edit_record(repo, lambda d: d["relations"].append(copy.deepcopy(d["relations"][0])))
    with pytest.raises(build.KnowledgeError, match="Duplicate relationship"):
        build.generate(repo)


def test_review_required(repo):
    edit_record(repo, lambda d: d["relations"][0].pop("review"))
    with pytest.raises(build.KnowledgeError, match="review"):
        build.generate(repo)


def test_candidate_cannot_be_authoritative(repo):
    edit_record(repo, lambda d: d.update(status="candidate"))
    with pytest.raises(build.KnowledgeError, match="non-active"):
        build.generate(repo)


def test_source_must_resolve(repo):
    edit_record(repo, lambda d: d.update(sources=["../outside.md"]))
    with pytest.raises(build.KnowledgeError, match="Unresolved source"):
        build.generate(repo)


def test_inventory_drift(repo):
    edit_record(repo, lambda d: d.update(title="different source"), "DS-0002")
    with pytest.raises(build.KnowledgeError, match="Dataset title drift"):
        build.generate(repo)


def test_deterministic_generation_and_checked_in_output():
    first = build.canonical_bytes(build.generate(ROOT))
    second = build.canonical_bytes(build.generate(ROOT))
    assert first == second
    assert first == (ROOT / "graph/generated/knowledge.json").read_bytes()


def test_source_change_updates_revision(repo):
    before = build.generate(repo)["revision"]
    path = repo / "specs/v2_monthly_confirmation.md"
    path.write_text(path.read_text() + "\nContext correction.\n")
    assert build.generate(repo)["revision"] != before


def test_graph_boundaries_and_candidate_partition():
    graph = build.generate(ROOT)
    ids = {n["id"] for n in graph["nodes"]}
    assert len(ids) == len(graph["nodes"])
    assert {n["type"] for n in graph["nodes"]}.isdisjoint({"scene", "run", "result"})
    assert all(e["status"] == "validated" for e in graph["relationships"])
    assert all(e["status"] == "candidate" for e in graph["candidate_relationships"])
    assert any(
        e["source"] == "application:seasonal-forest-change-monitoring"
        for e in graph["candidate_relationships"]
    )
    assert all(
        e["source"] in ids and e["target"] in ids
        for e in graph["relationships"] + graph["candidate_relationships"]
    )


def test_method_composition_must_be_acyclic(repo):
    edit_record(
        repo,
        lambda d: d["relations"].append(
            {
                "type": "USES_METHOD",
                "target": "method:matched-season-interannual-comparison",
                "status": "candidate",
                "sources": ["docs/adr/0005-semantic-architecture-and-backends.md"],
            }
        ),
        "method:moving-window-comparison",
    )
    with pytest.raises(build.KnowledgeError, match="Cyclic USES_METHOD"):
        build.generate(repo)


def test_duplicate_dataset_entity(repo):
    inventory = repo / "research/data_sources/inventory.csv"
    rows = inventory.read_text().splitlines()
    original = next(row for row in rows if row.startswith("DS-0002,"))
    inventory.write_text("\n".join(rows + [original.replace("DS-0002", "DS-0099", 1)]) + "\n")
    path = repo / "knowledge/datasets/DS-0002.md"
    path.with_name("DS-0099.md").write_text(
        path.read_text().replace("id: DS-0002", "id: DS-0099")
    )
    with pytest.raises(build.KnowledgeError, match="Duplicate dataset entity"):
        build.generate(repo)
