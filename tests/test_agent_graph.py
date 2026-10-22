"""Agent-graph record checks and rendering (ADR 0007). Synthetic fixtures assert no real runs."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml

from agent_harness.scripts.render_round_graph import render, render_mermaid, render_svg
from agent_harness.scripts.validate_round import LAB, check, discover

GRAPH_EXAMPLE = LAB / "agent_harness/examples/road-widening/round-0001/round.yaml"
RENDERER = LAB / "agent_harness/scripts/render_round_graph.py"


def write(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    return path


@pytest.fixture
def planned(tmp_path):
    shutil.copytree(GRAPH_EXAMPLE.parent / "assignments", tmp_path / "assignments")
    return tmp_path / "round.yaml", yaml.safe_load(GRAPH_EXAMPLE.read_text())


def findings(record):
    path, data = record
    return check(write(path, data))


def node(data, node_id):
    return next(n for n in data["graph"]["nodes"] if n["id"] == node_id)


def approve(target, when="2026-10-22T09:00:00Z"):
    # Synthetic approval for structural tests only; not a real human decision.
    target.update(status="approved", approver="synthetic test reviewer", decided_utc=when, basis="fixture only")


def attempt(path, data, instance, attempt_id="synthetic-1", start="2026-10-22T10:00:00Z"):
    loaded = []
    for source, name in [("forest-cover-lab", "AGENTS.md"), ("forest-cover-lab", "docs/agents.md"),
                         ("forest-cover-lab", instance["role"]), ("round", instance["assignment"])]:
        content = (path.parent if source == "round" else LAB) / name
        loaded.append({"source": source, "path_or_identifier": name,
                       "revision": data["repos"]["forest_cover_lab"] if source == "forest-cover-lab" else None,
                       "sha256": hashlib.sha256(content.read_bytes()).hexdigest(), "capture_status": "captured"})
    return {
        "attempt_id": attempt_id, "host": instance["host_planned"], "started_utc": start,
        "ended_utc": start.replace("T10", "T11"), "status": "completed", "model_if_known": None,
        "loaded_harness": loaded, "prompt_ref": "synthetic fixture", "tool_access": [], "source_refs": [],
        "output_refs": ["synthetic.txt"], "output_hashes": {"synthetic.txt": hashlib.sha256(b"test-only").hexdigest()},
        "checks": ["fixture structure only"], "limitations": ["Synthetic test record; not an observed execution"],
    }


@pytest.fixture
def executed(planned):
    """eo-01 completed once, with graph and step plan approved before the attempt."""
    path, data = planned
    data["status"] = "active"
    data["repos"] = {"forest_cover_lab": "a" * 40, "sentinel_monthly_forest_cover": "b" * 40, "lab_graph_revision": "c" * 64}
    instance = next(i for i in data["instances"] if i["id"] == "eo-01")
    instance["selection_status"] = "completed"
    instance["actual_executions"] = [attempt(path, data, instance)]
    approve(data["graph"]["approval"])
    plan = {"plan_ref": "steps/eo-01/plan.md", "plan_sha256": "d" * 64,
            "approval": {"status": "pending", "approver": None, "decided_utc": None, "basis": None}}
    approve(plan["approval"], "2026-10-22T09:30:00Z")
    node(data, "eo-01")["step_plan"] = plan
    return path, data


def test_graph_example_is_valid_planned_and_unexecuted():
    data = yaml.safe_load(GRAPH_EXAMPLE.read_text())
    assert not check(GRAPH_EXAMPLE)
    assert data["status"] == "planned" and data["graph"]["approval"]["status"] == "pending"
    assert all(not i["actual_executions"] for i in data["instances"])
    assert all(n["approval"]["status"] == "pending" for n in data["graph"]["nodes"] if n["kind"] == "gate")


def test_rounds_without_graph_remain_valid():
    plain = [p for p in discover(LAB) if "graph" not in yaml.safe_load(p.read_text())]
    assert plain
    for path in plain:
        assert not check(path)


def test_committed_graph_images_are_current():
    for path in discover(LAB):
        if "graph" in yaml.safe_load(path.read_text()):
            assert not render(path, check_only=True), f"stale images for {path}; run render_round_graph.py"
            assert (path.parent / "graph.svg").is_file() and (path.parent / "graph.mmd").is_file()


@pytest.mark.parametrize("change, expected", [
    ("cycle", "cycle"),
    ("self_loop", "self-loop"),
    ("duplicate_edge", "duplicate edge"),
    ("unknown_edge_node", "unknown node"),
    ("duplicate_node", "duplicate node"),
    ("hidden_agent", "hidden agent"),
    ("unknown_instance", "unknown instance"),
    ("instance_twice", "already used"),
    ("not_used_in_graph", "not_used"),
    ("undeclared_payload", "undeclared outputs"),
    ("gate_forwards_unreceived", "undeclared outputs"),
    ("empty_payload", "must name what it carries"),
    ("edge_into_input", "input nodes"),
    ("independence_path", "independence group"),
    ("non_gate_sink", "sink"),
    ("disconnected", "disconnected"),
    ("approved_without_basis", "requires named human"),
    ("pending_with_approver", "must not name"),
])
def test_structural_violations(planned, change, expected):
    data = planned[1]
    graph = data["graph"]
    if change == "cycle":
        graph["edges"].append({"from": "critic-01", "to": "reconcile", "carries": ["challenge_report.md"]})
    elif change == "self_loop":
        graph["edges"].append({"from": "eo-01", "to": "eo-01", "carries": ["eo_claims.csv"]})
    elif change == "duplicate_edge":
        graph["edges"].append(copy.deepcopy(graph["edges"][0]))
    elif change == "unknown_edge_node":
        graph["edges"].append({"from": "eo-01", "to": "ghost", "carries": ["eo_claims.csv"]})
    elif change == "duplicate_node":
        graph["nodes"].append(copy.deepcopy(node(data, "reconcile")))
    elif change == "hidden_agent":
        graph["nodes"] = [n for n in graph["nodes"] if n["id"] != "sources-01"]
        graph["edges"] = [e for e in graph["edges"] if "sources-01" not in (e["from"], e["to"])]
        graph["independence_groups"] = [["eo-01", "geo-01", "works-01"]]
        node(data, "reconcile")  # still present; payload mismatch is reported separately
    elif change == "unknown_instance":
        node(data, "geo-01")["instance"] = "nobody"
    elif change == "instance_twice":
        node(data, "geo-01")["instance"] = "eo-01"
    elif change == "not_used_in_graph":
        next(i for i in data["instances"] if i["id"] == "works-01")["selection_status"] = "not_used"
    elif change == "undeclared_payload":
        graph["edges"][0]["carries"].append("secret_extra.tif")
    elif change == "gate_forwards_unreceived":
        next(e for e in graph["edges"] if e["from"] == "accept-outputs")["carries"].append("aoi.geojson")
    elif change == "empty_payload":
        graph["edges"][0]["carries"] = []
    elif change == "edge_into_input":
        graph["nodes"].append({"id": "extra", "kind": "input", "outputs": ["extra.csv"]})
        graph["edges"].append({"from": "extra", "to": "frame", "carries": ["extra.csv"]})
    elif change == "independence_path":
        graph["edges"].append({"from": "eo-01", "to": "geo-01", "carries": ["eo_claims.csv"]})
    elif change == "non_gate_sink":
        graph["edges"] = [e for e in graph["edges"] if e["to"] != "human-review"]
        graph["nodes"] = [n for n in graph["nodes"] if n["id"] != "human-review"]
    elif change == "disconnected":
        graph["nodes"].append({"id": "orphan-gate", "kind": "gate", "approver": "human",
                               "approval": {"status": "pending", "approver": None, "decided_utc": None, "basis": None}})
    elif change == "approved_without_basis":
        approve(node(data, "human-review")["approval"])
        node(data, "human-review")["approval"]["basis"] = None
    elif change == "pending_with_approver":
        graph["approval"]["approver"] = "someone"
    errors = findings(planned)
    assert any(expected in e for e in errors), errors


@pytest.mark.parametrize("node_id, field, value", [
    ("reconcile", "instance", "eo-01"),        # scripts are not agents
    ("accept-outputs", "outputs", ["x"]),     # gates only forward what they receive
    ("eo-01", "command", "python x.py"),      # agents are not scripts
    ("frame", "loop", {"max_iterations": 2, "until": "never"}),
])
def test_schema_rejects_mixed_node_kinds(planned, node_id, field, value):
    node(planned[1], node_id)[field] = value
    assert any(e.startswith("schema") for e in findings(planned))


def test_executed_record_with_approvals_passes(executed):
    assert not findings(executed)


@pytest.mark.parametrize("change, expected", [
    ("graph_pending", "graph itself is not approved"),
    ("graph_approved_late", "before the graph was approved"),
    ("no_step_plan", "requires an approved step plan"),
    ("step_plan_pending", "step plan is pending"),
    ("step_plan_late", "before its step plan was approved"),
    ("step_plan_no_digest", "without SHA-256"),
    ("loop_exceeded", "exceed loop bound"),
    ("downstream_gate_pending", "upstream gate accept-outputs is pending"),
    ("gate_before_upstream_done", "approved before upstream"),
])
def test_execution_gating(executed, change, expected):
    path, data = executed
    graph = data["graph"]
    eo = node(data, "eo-01")
    instance = next(i for i in data["instances"] if i["id"] == "eo-01")
    if change == "graph_pending":
        graph["approval"].update(status="pending", approver=None, decided_utc=None, basis=None)
    elif change == "graph_approved_late":
        graph["approval"]["decided_utc"] = "2026-10-22T12:00:00Z"
    elif change == "no_step_plan":
        eo.pop("step_plan")
    elif change == "step_plan_pending":
        eo["step_plan"]["approval"].update(status="pending", approver=None, decided_utc=None, basis=None)
    elif change == "step_plan_late":
        eo["step_plan"]["approval"]["decided_utc"] = "2026-10-22T12:00:00Z"
    elif change == "step_plan_no_digest":
        eo["step_plan"]["plan_sha256"] = None
    elif change == "loop_exceeded":
        instance["actual_executions"] = [attempt(path, data, instance, f"synthetic-{k}") for k in range(4)]
    elif change == "downstream_gate_pending":
        critic = next(i for i in data["instances"] if i["id"] == "critic-01")
        critic["selection_status"] = "completed"
        critic["actual_executions"] = [attempt(path, data, critic)]
        node(data, "critic-01")["step_plan"] = copy.deepcopy(eo["step_plan"])
    elif change == "gate_before_upstream_done":
        approve(node(data, "accept-outputs")["approval"])
    errors = findings(executed)
    assert any(expected in e for e in errors), errors


def test_loop_bound_allows_declared_retries(executed):
    path, data = executed
    instance = next(i for i in data["instances"] if i["id"] == "eo-01")
    instance["actual_executions"] = [attempt(path, data, instance, f"synthetic-{k}") for k in range(3)]
    assert not findings(executed)


def test_auto_mode_needs_no_step_plan_but_still_needs_graph_approval(executed):
    data = executed[1]
    data["graph"]["mode"] = "auto"
    node(data, "eo-01").pop("step_plan")
    assert not findings(executed)
    data["graph"]["approval"].update(status="pending", approver=None, decided_utc=None, basis=None)
    assert findings(executed)


def test_renderings_show_every_node_and_payload_deterministically():
    data = yaml.safe_load(GRAPH_EXAMPLE.read_text())
    svg, mermaid = render_svg(data), render_mermaid(data)
    assert svg == render_svg(copy.deepcopy(data)) and mermaid == render_mermaid(copy.deepcopy(data))
    for item in data["graph"]["nodes"]:
        assert item.get("label", item["id"]) in svg and item.get("label", item["id"]) in mermaid
    for edge in data["graph"]["edges"]:
        for carried in edge["carries"]:
            assert carried in svg and carried in mermaid
    assert "manual hand-off" in svg and "Planned graph: no execution recorded." in svg
    assert "loop ≤3" in svg


def test_renderer_refuses_invalid_and_detects_stale(planned, tmp_path):
    path, data = planned
    write(path, data)
    run = lambda *args: subprocess.run([sys.executable, str(RENDERER), *args], capture_output=True, text=True)
    assert run(str(path), "--check").returncode == 1  # nothing rendered yet
    assert run(str(path)).returncode == 0
    assert (tmp_path / "graph.svg").is_file() and (tmp_path / "graph.mmd").is_file()
    assert run(str(path), "--check").returncode == 0
    data["graph"]["edges"][0]["carries"] = ["observation_windows.yaml"]
    write(path, data)
    assert run(str(path), "--check").returncode == 1
    data["graph"]["edges"].append({"from": "critic-01", "to": "reconcile", "carries": ["challenge_report.md"]})
    write(path, data)
    result = run(str(path))
    assert result.returncode == 1 and "not drawn" in result.stdout
