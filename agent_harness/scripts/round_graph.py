"""Agent-graph checks for round manifests (ADR 0007). Record structure only, no execution.

The optional ``graph`` block names which agents exist, what each passes to the next, where
a human must approve and how often an agent may retry. These checks make that plan
explicit and compare recorded attempts with the approvals the record declares. They
cannot prove that a human actually approved or that a host honoured the graph.
"""
from __future__ import annotations

from datetime import datetime
import re

DIGEST = re.compile(r"^[0-9a-f]{64}$")
CHAT_HOSTS = {"chatgpt", "claude"}  # no programmatic invocation: manual hand-off


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def topo_order(node_ids: list[str], edges: list[dict]) -> list[str] | None:
    """Kahn's algorithm, ties broken by declaration order. None if the graph has a cycle."""
    indegree = {n: 0 for n in node_ids}
    successors: dict[str, list[str]] = {n: [] for n in node_ids}
    for edge in edges:
        successors[edge["from"]].append(edge["to"])
        indegree[edge["to"]] += 1
    rank = {n: i for i, n in enumerate(node_ids)}
    ready = [n for n in node_ids if indegree[n] == 0]
    order: list[str] = []
    while ready:
        ready.sort(key=rank.__getitem__)
        node = ready.pop(0)
        order.append(node)
        for target in successors[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    return order if len(order) == len(node_ids) else None


def reachable(start: str, adjacency: dict[str, list[str]]) -> set[str]:
    seen: set[str] = set()
    stack = list(adjacency.get(start, []))
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            stack.extend(adjacency.get(node, []))
    return seen


def available_outputs(graph: dict, order: list[str]) -> dict[str, set[str]]:
    """Declared outputs per node; a gate passes on only what it received."""
    nodes = {n["id"]: n for n in graph["nodes"]}
    available: dict[str, set[str]] = {}
    for node_id in order:
        node = nodes[node_id]
        if node["kind"] == "gate":
            available[node_id] = {item for e in graph["edges"] if e["to"] == node_id for item in e["carries"]}
        else:
            available[node_id] = set(node.get("outputs", []))
    return available


def _approval_errors(label: str, approval: dict) -> list[str]:
    if approval["status"] == "pending":
        if any(approval[k] for k in ("approver", "decided_utc", "basis")):
            return [f"{label}: pending approval must not name an approver, time or basis"]
        return []
    if not all(approval[k] and str(approval[k]).strip() for k in ("approver", "decided_utc", "basis")):
        return [f"{label}: {approval['status']} approval requires named human, time and basis"]
    return []


def node_status(data: dict, node: dict) -> str:
    """Status shown in the graph image, derived only from the record."""
    if node["kind"] == "gate":
        return node["approval"]["status"]
    if node["kind"] == "input":
        return "declared"
    if node["kind"] == "script":
        return "planned (no record)"
    instance = next(i for i in data["instances"] if i["id"] == node["instance"])
    attempts = len(instance["actual_executions"])
    status = instance["selection_status"]
    return f"{status} · {attempts} attempt{'s' if attempts != 1 else ''}" if attempts else status


def graph_errors(data: dict) -> list[str]:
    graph = data["graph"]
    nodes = graph["nodes"]
    edges = graph["edges"]
    errors: list[str] = []
    ids = [n["id"] for n in nodes]
    if len(set(ids)) != len(ids):
        return ["graph: duplicate node IDs"]
    by_id = {n["id"]: n for n in nodes}
    instances = {i["id"]: i for i in data["instances"]}

    used: dict[str, str] = {}
    for node in nodes:
        if node["kind"] != "agent":
            continue
        name = node["instance"]
        if name not in instances:
            errors.append(f"graph/{node['id']}: unknown instance {name}")
        elif name in used:
            errors.append(f"graph/{node['id']}: instance {name} already used by {used[name]}")
        else:
            used[name] = node["id"]
    for name, instance in instances.items():
        if instance["selection_status"] == "not_used" and name in used:
            errors.append(f"graph/{used[name]}: instance {name} is not_used but placed in the graph")
        if instance["selection_status"] != "not_used" and name not in used:
            errors.append(f"graph: instance {name} is missing from the graph (hidden agent)")

    seen_pairs: set[tuple[str, str]] = set()
    for edge in edges:
        pair = (edge["from"], edge["to"])
        for end in pair:
            if end not in by_id:
                errors.append(f"graph: edge {pair[0]}->{pair[1]} references unknown node {end}")
        if pair[0] == pair[1]:
            errors.append(f"graph: self-loop on {pair[0]}; declare node loop instead")
        if pair in seen_pairs:
            errors.append(f"graph: duplicate edge {pair[0]}->{pair[1]}")
        seen_pairs.add(pair)
    if errors:
        return errors

    order = topo_order(ids, edges)
    if order is None:
        return ["graph: cycle detected; iteration belongs in a node loop, not an edge cycle"]

    successors: dict[str, list[str]] = {n: [] for n in ids}
    predecessors: dict[str, list[str]] = {n: [] for n in ids}
    for edge in edges:
        successors[edge["from"]].append(edge["to"])
        predecessors[edge["to"]].append(edge["from"])

    available = available_outputs(graph, order)
    for edge in edges:
        label = f"graph: edge {edge['from']}->{edge['to']}"
        missing = sorted(set(edge["carries"]) - available[edge["from"]])
        if missing:
            errors.append(f"{label} carries undeclared outputs: {', '.join(missing)}")
        if by_id[edge["from"]]["kind"] != "gate" and not edge["carries"]:
            errors.append(f"{label} must name what it carries")
        if by_id[edge["to"]]["kind"] == "input":
            errors.append(f"{label}: input nodes cannot receive edges")

    parent = {n: n for n in ids}

    def root(n: str) -> str:
        while parent[n] != n:
            parent[n] = parent[parent[n]]
            n = parent[n]
        return n

    for edge in edges:
        parent[root(edge["from"])] = root(edge["to"])
    if len({root(n) for n in ids}) > 1:
        errors.append("graph: nodes form more than one disconnected graph")
    for node_id in ids:
        if not successors[node_id] and by_id[node_id]["kind"] != "gate":
            errors.append(f"graph/{node_id}: every sink must be a human gate")

    for index, group in enumerate(graph.get("independence_groups", []), 1):
        for member in group:
            if member not in by_id:
                errors.append(f"graph: independence group {index} names unknown node {member}")
        members = [m for m in group if m in by_id]
        for a in members:
            downstream = reachable(a, successors)
            for b in members:
                if a != b and b in downstream:
                    errors.append(f"graph: independence group {index}: {a} reaches {b}")

    for node in nodes:
        if "approval" in node:
            errors.extend(_approval_errors(f"graph/{node['id']}", node["approval"]))
        if "step_plan" in node:
            errors.extend(_approval_errors(f"graph/{node['id']}/step_plan", node["step_plan"]["approval"]))
    errors.extend(_approval_errors("graph/approval", graph["approval"]))

    attempts_by_node = {
        n["id"]: instances[n["instance"]]["actual_executions"] for n in nodes if n["kind"] == "agent"
    }
    any_attempt = any(attempts_by_node.values())
    graph_approval = graph["approval"]
    if any_attempt and graph_approval["status"] != "approved":
        errors.append("graph: attempts recorded but the graph itself is not approved")

    for node in nodes:
        if node["kind"] == "gate" and node["approval"]["status"] == "approved":
            for upstream in reachable(node["id"], predecessors):
                if by_id[upstream]["kind"] == "agent":
                    if instances[by_id[upstream]["instance"]]["selection_status"] != "completed":
                        errors.append(f"graph/{node['id']}: approved before upstream {upstream} completed")
        if node["kind"] != "agent":
            continue
        attempts = attempts_by_node[node["id"]]
        bound = node.get("loop", {}).get("max_iterations", 1)
        if len(attempts) > bound:
            errors.append(f"graph/{node['id']}: {len(attempts)} attempts exceed loop bound {bound}")
        if not attempts:
            continue
        first = min(_time(a["started_utc"]) for a in attempts)
        if graph_approval["status"] == "approved" and graph_approval["decided_utc"] and _time(graph_approval["decided_utc"]) > first:
            errors.append(f"graph/{node['id']}: attempt started before the graph was approved")
        for upstream in reachable(node["id"], predecessors):
            gate = by_id[upstream]
            if gate["kind"] != "gate":
                continue
            approval = gate["approval"]
            if approval["status"] != "approved":
                errors.append(f"graph/{node['id']}: upstream gate {upstream} is {approval['status']}")
            elif approval["decided_utc"] and _time(approval["decided_utc"]) > first:
                errors.append(f"graph/{node['id']}: attempt started before gate {upstream} was approved")
        if graph["mode"] == "stepwise":
            plan = node.get("step_plan")
            if not plan:
                errors.append(f"graph/{node['id']}: stepwise mode requires an approved step plan")
                continue
            if not DIGEST.fullmatch(plan["plan_sha256"] or ""):
                errors.append(f"graph/{node['id']}: step plan without SHA-256")
            approval = plan["approval"]
            if approval["status"] != "approved":
                errors.append(f"graph/{node['id']}: step plan is {approval['status']}")
            elif approval["decided_utc"] and _time(approval["decided_utc"]) > first:
                errors.append(f"graph/{node['id']}: attempt started before its step plan was approved")
    return errors
