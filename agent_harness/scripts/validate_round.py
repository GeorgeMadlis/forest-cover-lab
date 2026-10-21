#!/usr/bin/env python3
"""Validate round records, not science. Resolve Lab roles separately from round files."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re

import jsonschema
import yaml

LAB = Path(__file__).resolve().parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
REPOSITORIES = {"forest-cover-lab", "sentinel-monthly-forest-cover"}


class UniqueLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _local_file(root: Path, name: str) -> bool:
    target = (root / name).resolve()
    return not Path(name).is_absolute() and target.is_relative_to(root.resolve()) and target.is_file()


def discover(root: Path):
    """Only the chosen repository: examples, research inquiries, or review rounds."""
    for pattern in (
        "agent_harness/examples/*/round-*/round.yaml",
        "research/inquiries/*/rounds/*/round.yaml",
        "reviews/*/rounds/*/round.yaml",
    ):
        yield from sorted(root.glob(pattern))


def check(path: Path, lab_root: Path = LAB) -> list[str]:
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
        schema = json.loads((lab_root / "agent_harness/schemas/round.schema.json").read_text())
    except (OSError, ValueError, yaml.YAMLError) as error:
        return [f"read: {error}"]
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = [f"schema: {'.'.join(map(str, e.path))}: {e.message}" for e in validator.iter_errors(data)]
    if errors:
        return errors
    ids = [i["id"] for i in data["instances"]]
    if len(set(ids)) != len(ids):
        errors.append("duplicate instance IDs")
    has_actual = any(i["actual_executions"] for i in data["instances"])
    if data["status"] == "planned" and has_actual:
        errors.append("planned round contains actual executions")
    for instance in data["instances"]:
        name = instance["id"]
        if not _local_file(path.parent, instance["assignment"]):
            errors.append(f"{name}: missing or unsafe assignment: {instance['assignment']}")
        role_root = path.parent if instance.get("role_scope") == "round_only" else lab_root
        if not _local_file(role_root, instance["role"]):
            errors.append(f"{name}: missing or unsafe role: {instance['role']}")
        attempts = instance["actual_executions"]
        selection = instance["selection_status"]
        if selection in {"started", "completed", "blocked"} and not attempts:
            errors.append(f"{name}: status requires an observed attempt")
        if selection == "completed" and not any(a["status"] == "completed" for a in attempts):
            errors.append(f"{name}: missing completed attempt")
        if selection in {"planned", "not_used"} and attempts:
            errors.append(f"{name}: {selection} conflicts with attempts")
        attempt_ids = [a["attempt_id"] for a in attempts]
        if len(set(attempt_ids)) != len(attempt_ids):
            errors.append(f"{name}: duplicate attempt IDs")
        for attempt in attempts:
            label = f"{name}/{attempt['attempt_id']}"
            if attempt["status"] != "running" and not attempt["ended_utc"]:
                errors.append(f"{label}: terminal attempt missing end time")
            if attempt["ended_utc"] and datetime.fromisoformat(attempt["ended_utc"].replace('Z', '+00:00')) < datetime.fromisoformat(attempt["started_utc"].replace('Z', '+00:00')):
                errors.append(f"{label}: end time precedes start")
            if attempt["status"] == "completed":
                if not attempt["output_refs"] or not attempt["checks"]:
                    errors.append(f"{label}: completed attempt requires outputs and documented checks")
                for output in attempt["output_refs"]:
                    if not DIGEST.fullmatch(attempt.get("output_hashes", {}).get(output, "")):
                        errors.append(f"{label}: output without digest: {output}")
            loaded = attempt["loaded_harness"]
            for ref in loaded:
                if ref["capture_status"] == "selected":
                    errors.append(f"{label}: selected is not an observed load")
                if ref["capture_status"] == "captured" and not ref["sha256"]:
                    errors.append(f"{label}: captured file without digest: {ref['path_or_identifier']}")
                if ref["source"] in REPOSITORIES | {"round"} and ref["capture_status"] != "captured":
                    errors.append(f"{label}: repository/round harness must be captured")
                if ref["source"] in REPOSITORIES:
                    if not FULL_SHA.fullmatch(ref["revision"] or ""):
                        errors.append(f"{label}: repository harness requires full commit")
                    key = ref["source"].replace('-', '_')
                    if ref["revision"] != data["repos"][key]:
                        errors.append(f"{label}: repository harness differs from pinned round revision")
                if ref["capture_status"] == "not_captured" and not attempt["limitations"]:
                    errors.append(f"{label}: uncaptured instructions require a limitation")
            required = {("forest-cover-lab", "AGENTS.md"), ("forest-cover-lab", "docs/agents.md"), ("round", instance["assignment"])}
            required.add(("round" if instance.get("role_scope") == "round_only" else "forest-cover-lab", instance["role"]))
            if data["kind"] == "execution" or "reviews" in path.parts:
                required.add(("sentinel-monthly-forest-cover", "AGENTS.md"))
            observed = {(ref["source"], ref["path_or_identifier"]) for ref in loaded}
            for source, item in sorted(required - observed):
                errors.append(f"{label}: mandatory harness not recorded: {source}:{item}")
    if has_actual or data["status"] in {"active", "reviewed", "superseded"}:
        for key in ("forest_cover_lab", "sentinel_monthly_forest_cover"):
            if not FULL_SHA.fullmatch(data["repos"][key] or ""):
                errors.append(f"executed/active round missing pinned {key} commit SHA")
        if not DIGEST.fullmatch(data["repos"]["lab_graph_revision"] or ""):
            errors.append("executed/active round missing Lab graph revision SHA-256")
    review = data["human_review"]
    if data["status"] == "reviewed" or review["status"] != "pending":
        if review["status"] == "pending" or not all(review[k] and review[k].strip() for k in ("reviewer", "decision", "basis")):
            errors.append("reviewed round requires named human, decision and review basis")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, nargs="*")
    parser.add_argument("--root", type=Path, help="discover records only inside this checkout")
    parser.add_argument("--lab", type=Path, default=LAB, help="Lab roles/schema checkout")
    args = parser.parse_args()
    if not args.manifest and args.root is None:
        parser.error("provide manifests or --root")
    if args.root is not None and not args.root.is_dir():
        parser.error("--root must be an existing directory")
    if not (args.lab / "agent_harness/schemas/round.schema.json").is_file():
        parser.error("--lab must contain the round schema")
    paths = sorted(set(args.manifest + (list(discover(args.root)) if args.root else [])))
    failed = False
    for path in paths:
        errors = check(path.resolve(), args.lab.resolve())
        failed |= bool(errors)
        for error in errors:
            print(f"FAIL: {path}: {error}")
        if not errors:
            print(f"PASS (record structure only): {path}")
    print(f"Checked {len(paths)} round manifest(s); {'FAIL' if failed else 'PASS'} (zero means none recorded)")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
