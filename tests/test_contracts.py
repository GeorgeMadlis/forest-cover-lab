import copy
import json
import subprocess
import sys

import jsonschema
import pytest
from test_knowledge import ROOT, build


def example(filename):
    return json.loads((ROOT / "configs" / filename).read_text())


def test_existing_manifest_and_schemas():
    for path in [
        ROOT / "validate/run_manifest.schema.json",
        *list((ROOT / "graph/schemas").glob("*.json")),
    ]:
        jsonschema.Draft202012Validator.check_schema(json.loads(path.read_text()))
    build.validate_provenance(
        example("run_manifest.example.json"), build.generate(ROOT)
    )


def test_extended_manifest():
    build.validate_provenance(
        example("run_manifest.semantic.example.json"), build.generate(ROOT)
    )


@pytest.mark.parametrize("field", ["dataset_ids", "concept_ids"])
def test_provenance_unresolved_ids(field):
    manifest = example("run_manifest.semantic.example.json")
    manifest["semantic_provenance"][field] = ["DS-9999"]
    with pytest.raises(build.KnowledgeError, match="Unresolved"):
        build.validate_provenance(manifest, build.generate(ROOT))


def test_ai_plan_required():
    manifest = example("run_manifest.semantic.example.json")
    manifest["semantic_provenance"].pop("planning_record_id")
    with pytest.raises(build.KnowledgeError, match="planning_record_id"):
        build.validate_provenance(manifest, build.generate(ROOT))
    manifest["semantic_provenance"]["ai_planner_involved"] = False
    build.validate_provenance(manifest, build.generate(ROOT))


@pytest.mark.parametrize(
    "field", ["dataset_version", "inventory_id", "access_time_utc"]
)
def test_extended_dataset_metadata_required(field):
    manifest = example("run_manifest.semantic.example.json")
    manifest["data_provenance"][0].pop(field)
    with pytest.raises(build.KnowledgeError, match=field):
        build.validate_provenance(manifest, build.generate(ROOT))


def test_access_timestamp_format():
    manifest = example("run_manifest.semantic.example.json")
    manifest["data_provenance"][0]["access_time_utc"] = "yesterday"
    with pytest.raises(build.KnowledgeError, match="date-time"):
        build.validate_provenance(manifest, build.generate(ROOT))


def test_provenance_method_version():
    manifest = example("run_manifest.semantic.example.json")
    manifest["semantic_provenance"]["methods"][0]["version"] = "99"
    with pytest.raises(build.KnowledgeError, match="version mismatch"):
        build.validate_provenance(manifest, build.generate(ROOT))


def test_dataset_selection_consistency():
    manifest = example("run_manifest.semantic.example.json")
    manifest["semantic_provenance"]["dataset_ids"] = ["DS-0002"]
    with pytest.raises(build.KnowledgeError, match="disagree"):
        build.validate_provenance(manifest, build.generate(ROOT))


def test_descriptor_valid():
    descriptor = example("downstream.sentinel-monthly.example.json")
    assert descriptor["status"] == "proposed"
    build.validate_descriptor(descriptor, build.generate(ROOT))


@pytest.mark.parametrize(
    "field",
    [
        "implemented_method_ids",
        "observation_ids",
        "dataset_ids",
        "tool_ids",
        "capability_ids",
        "validation_ids",
    ],
)
def test_descriptor_required_fields(field):
    descriptor = example("downstream.sentinel-monthly.example.json")
    descriptor.pop(field)
    with pytest.raises(build.KnowledgeError, match=field):
        build.validate_descriptor(descriptor, build.generate(ROOT))


@pytest.mark.parametrize("target", ["method:missing", "observation:forest-baseline"])
def test_descriptor_reference_type(target):
    descriptor = example("downstream.sentinel-monthly.example.json")
    descriptor["implemented_method_ids"] = [target]
    with pytest.raises(build.KnowledgeError):
        build.validate_descriptor(descriptor, build.generate(ROOT))


def test_snapshot_mismatch():
    graph = copy.deepcopy(build.generate(ROOT))
    graph["revision"] = "a" * 64
    with pytest.raises(build.KnowledgeError, match="stale graph"):
        build.validate_descriptor(
            example("downstream.sentinel-monthly.example.json"), graph
        )
    with pytest.raises(build.KnowledgeError, match="different graph"):
        build.validate_provenance(example("run_manifest.semantic.example.json"), graph)


def test_cli_check_no_diff():
    path = ROOT / "graph/generated/knowledge.json"
    before = path.read_bytes()
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "graph/build.py"),
            "--check",
            "--descriptor",
            str(ROOT / "configs/downstream.sentinel-monthly.example.json"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert path.read_bytes() == before


def test_existing_nonclaims_preserved():
    assert (
        "Hansen annual loss ≠ monthly ground truth." in (ROOT / "README.md").read_text()
    )
    assert "Annual agreement" in (ROOT / "validate/validation_plan.md").read_text()
    assert (
        "They have not been validated as month-resolved truth."
        in (ROOT / "report/reporting_contract.md").read_text()
    )
