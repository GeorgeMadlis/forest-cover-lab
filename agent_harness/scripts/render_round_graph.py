#!/usr/bin/env python3
"""Draw a round's agent graph (ADR 0007) as SVG and Mermaid. Record view only, no execution.

Writes ``graph.svg`` and ``graph.mmd`` next to the manifest (or into ``--out-dir``).
Only manifests that pass ``validate_round.py`` are drawn, so the image never shows a plan
that fails its own checks. Layout is deterministic and uses no third-party packages or
fonts; ``--check`` exits non-zero if committed images are stale.

    python agent_harness/scripts/render_round_graph.py path/to/round.yaml
    python agent_harness/scripts/render_round_graph.py --root .          # every graph round
    python agent_harness/scripts/render_round_graph.py --root . --check  # CI freshness
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from xml.sax.saxutils import escape

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from round_graph import CHAT_HOSTS, node_status, topo_order  # noqa: E402
from validate_round import LAB, UniqueLoader, check, discover  # noqa: E402

FONT = "DejaVu Sans, Arial, Helvetica, sans-serif"
# Approximate advance widths (px) for DejaVu Sans, wider than most UI fonts.
CHAR_W = {13: 8.0, 11: 6.8, 10: 6.2}
NODE_H = 82
MIN_W = 160
H_GAP = 36
MARGIN = 28
LINE = 13

STYLE = {  # kind: fill, stroke, title text, sub text
    "input": ("#E6F1FB", "#185FA5", "#0C447C", "#185FA5"),
    "agent": ("#E1F5EE", "#0F6E56", "#085041", "#0F6E56"),
    "script": ("#F1EFE8", "#5F5E5A", "#2C2C2A", "#5F5E5A"),
    "gate": ("#FAEEDA", "#854F0B", "#633806", "#854F0B"),
}
PROBLEM = {"failed", "blocked", "rejected"}


def text_w(text: str, size: int) -> float:
    return len(text) * CHAR_W[size]


def describe(data: dict, node: dict) -> tuple[str, list[str], str]:
    """Title, detail lines and status line for one node."""
    title = node.get("label", node["id"])
    kind = node["kind"]
    if kind == "agent":
        instance = next(i for i in data["instances"] if i["id"] == node["instance"])
        host = instance["host_planned"]
        details = [host + (" · manual hand-off" if host in CHAT_HOSTS else ""), Path(instance["role"]).stem]
    elif kind == "script":
        details = ["deterministic script"]
    elif kind == "gate":
        details = [f"{node['approver']} approval gate"]
    else:
        details = ["input artifacts"]
    status = node_status(data, node)
    if kind == "agent":
        bound = node.get("loop", {}).get("max_iterations", 1)
        status += f" · loop ≤{bound}" if bound > 1 else " · single attempt"
    return title, details, status


def is_problem(status: str) -> bool:
    return status.split(" ")[0] in PROBLEM


def is_done(status: str) -> bool:
    return status.split(" ")[0] in {"completed", "approved"}


def layout(data: dict) -> dict:
    graph = data["graph"]
    nodes = {n["id"]: n for n in graph["nodes"]}
    ids = [n["id"] for n in graph["nodes"]]
    order = topo_order(ids, graph["edges"])
    preds = {n: [e["from"] for e in graph["edges"] if e["to"] == n] for n in ids}
    layer = {}
    for node_id in order:
        layer[node_id] = max((layer[p] + 1 for p in preds[node_id]), default=0)
    rows: list[list[str]] = [[] for _ in range(max(layer.values()) + 1)]
    for node_id in ids:
        rows[layer[node_id]].append(node_id)
    text = {n: describe(data, nodes[n]) for n in ids}
    width = {
        n: max([MIN_W, text_w(text[n][0], 13) + 28, text_w(text[n][2], 11) + 24]
               + [text_w(d, 11) + 24 for d in text[n][1]])
        for n in ids
    }
    # Order each row by the mean position of its predecessors (one downward sweep).
    position: dict[str, float] = {}
    for row in rows:
        decl = {n: i for i, n in enumerate(row)}
        row.sort(key=lambda n: (sum(position[p] for p in preds[n]) / len(preds[n]) if preds[n] else decl[n], decl[n]))
        for index, n in enumerate(row):
            position[n] = index - (len(row) - 1) / 2
    row_width = [sum(width[n] for n in row) + H_GAP * (len(row) - 1) for row in rows]
    content_w = max(row_width)

    edges = graph["edges"]
    long_edges = [e for e in edges if layer[e["to"]] - layer[e["from"]] > 1]
    labels = {}
    out_deg = {n: [e for e in edges if e["from"] == n] for n in ids}
    in_deg = {n: [e for e in edges if e["to"] == n] for n in ids}
    for e in edges:
        if e in long_edges:
            labels[id(e)] = "lane"
        elif len(out_deg[e["from"]]) == 1 or len({tuple(x["carries"]) for x in out_deg[e["from"]] if x not in long_edges}) == 1:
            labels[id(e)] = "source"
        elif len(in_deg[e["to"]]) == 1:
            labels[id(e)] = "target"
        else:
            labels[id(e)] = "middle"
    gap_lines = [1] * len(rows)
    for e in edges:
        if labels[id(e)] != "lane":
            gap_lines[layer[e["from"]]] = max(gap_lines[layer[e["from"]]], len(e["carries"]) + (1 if e.get("lineage") else 0))
    header_h = 64
    y = MARGIN + header_h
    row_y = []
    for index in range(len(rows)):
        row_y.append(y)
        y += NODE_H + 34 + gap_lines[index] * LINE
    longest_lane_label = max((max((text_w(c, 10) for c in e["carries"]), default=0) for e in long_edges), default=0)
    lane_space = (len(long_edges) * 18 + longest_lane_label + 24) if long_edges else 0
    title_w = text_w(f"Agent graph · {data['round_id']}", 13)
    canvas_w = max(content_w + 2 * MARGIN + lane_space, title_w + 2 * MARGIN, 560)
    boxes = {}
    for index, row in enumerate(rows):
        x = MARGIN + (content_w - row_width[index]) / 2
        for n in row:
            boxes[n] = (x, row_y[index], width[n], NODE_H)
            x += width[n] + H_GAP
    return {
        "rows": rows, "layer": layer, "boxes": boxes, "text": text, "labels": labels,
        "long_edges": long_edges, "content_right": MARGIN + content_w,
        "height": y - 34 + 24, "width": canvas_w,
    }


def _ports(edges_out: list[dict], box: tuple) -> dict[int, float]:
    x, _, w, _ = box
    count = len(edges_out)
    return {id(e): x + w * (i + 1) / (count + 1) for i, e in enumerate(edges_out)}


def render_svg(data: dict) -> str:
    graph = data["graph"]
    nodes = {n["id"]: n for n in graph["nodes"]}
    L = layout(data)
    boxes, layer = L["boxes"], L["layer"]
    edges = graph["edges"]
    any_attempt = any(i["actual_executions"] for i in data["instances"])
    legend_h = 76
    height = L["height"] + legend_h
    width = L["width"]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" font-family="{FONT}" role="img">',
        f"<title>Agent graph for round {escape(data['round_id'])}</title>",
        '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M1 1L9 5L1 9z" fill="#5F5E5A"/></marker></defs>',
        f'<rect width="{width:.0f}" height="{height:.0f}" fill="#FFFFFF"/>',
    ]
    approval = graph["approval"]
    out.append(f'<text x="{MARGIN}" y="{MARGIN + 6}" font-size="13" font-weight="bold" fill="#2C2C2A">'
               f"Agent graph · {escape(data['round_id'])}</text>")
    meta = (f"mode: {graph['mode']} · graph approval: {approval['status']}"
            + (f" by {approval['approver']}" if approval["approver"] else "")
            + f" · round status: {data['status']}")
    out.append(f'<text x="{MARGIN}" y="{MARGIN + 26}" font-size="11" fill="#444441">{escape(meta)}</text>')
    out.append(f'<text x="{MARGIN}" y="{MARGIN + 42}" font-size="11" fill="#5F5E5A">'
               f"proposed by: {escape(approval['proposed_by'])}</text>")

    # Independence groups: dashed enclosure when members share a row.
    for index, group in enumerate(graph.get("independence_groups", []), 1):
        rows_of = {layer[m] for m in group}
        if len(rows_of) != 1:
            continue
        xs = [boxes[m][0] for m in group]
        xe = [boxes[m][0] + boxes[m][2] for m in group]
        y0 = boxes[group[0]][1]
        out.append(f'<rect x="{min(xs) - 10:.1f}" y="{y0 - 18:.1f}" width="{max(xe) - min(xs) + 20:.1f}" '
                   f'height="{NODE_H + 28:.1f}" rx="10" fill="none" stroke="#7F77DD" stroke-dasharray="5 4"/>')
        out.append(f'<text x="{min(xs) - 4:.1f}" y="{y0 - 6:.1f}" font-size="10" fill="#534AB7">'
                   f"group {index}</text>")

    out_edges = {n: [e for e in edges if e["from"] == n and e not in L["long_edges"]] for n in nodes}
    in_edges = {n: [e for e in edges if e["to"] == n and e not in L["long_edges"]] for n in nodes}
    for n in nodes:
        out_edges[n].sort(key=lambda e: boxes[e["to"]][0])
        in_edges[n].sort(key=lambda e: boxes[e["from"]][0])
    src_port = {k: v for n in nodes for k, v in _ports(out_edges[n], boxes[n]).items()}
    dst_port = {k: v for n in nodes for k, v in _ports(in_edges[n], boxes[n]).items()}
    drawn_source_labels: set[tuple[str, tuple]] = set()
    label_svg = []

    def label_lines(e: dict) -> list[str]:
        lines = list(e["carries"]) or ["(control only)"]
        if e.get("lineage"):
            lines.append("lineage: " + ", ".join(e["lineage"]))
        return lines

    def put_label(x: float, y: float, lines: list[str], anchor: str = "middle") -> None:
        w = max(text_w(s, 10) for s in lines) + 8
        h = len(lines) * LINE + 4
        x0 = x - w / 2 if anchor == "middle" else x - 4
        label_svg.append(f'<rect x="{x0:.1f}" y="{y - 10:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" '
                         'fill="#FFFFFF" fill-opacity="0.92"/>')
        for i, s in enumerate(lines):
            color = "#534AB7" if s.startswith("lineage:") else "#444441"
            label_svg.append(f'<text x="{x:.1f}" y="{y + i * LINE:.1f}" font-size="10" fill="{color}" '
                             f'text-anchor="{anchor}">{escape(s)}</text>')

    for e in edges:
        if e in L["long_edges"]:
            continue
        sx, sy = src_port[id(e)], boxes[e["from"]][1] + NODE_H
        tx, ty = dst_port[id(e)], boxes[e["to"]][1]
        mid = (sy + ty) / 2
        out.append(f'<path d="M{sx:.1f} {sy:.1f} C{sx:.1f} {mid:.1f} {tx:.1f} {mid:.1f} {tx:.1f} {ty - 2:.1f}" '
                   'fill="none" stroke="#5F5E5A" stroke-width="1.2" marker-end="url(#arr)"/>')
        where = L["labels"][id(e)]
        lines = label_lines(e)
        if where == "source":
            key = (e["from"], tuple(lines))
            if key in drawn_source_labels:
                continue
            drawn_source_labels.add(key)
            cx = boxes[e["from"]][0] + boxes[e["from"]][2] / 2
            put_label(cx, sy + 16, lines)
        elif where == "target":
            put_label(tx, ty - 8 - (len(lines) - 1) * LINE - 6, lines)
        else:
            put_label((sx + tx) / 2, mid - (len(lines) - 1) * LINE / 2, lines)

    for k, e in enumerate(L["long_edges"]):
        lane = L["content_right"] + 18 + k * 18
        fx, fy, fw, _ = boxes[e["from"]]
        tx, ty, tw, _ = boxes[e["to"]]
        sy, ey = fy + NODE_H / 2, ty + NODE_H / 2
        out.append(f'<path d="M{fx + fw:.1f} {sy:.1f} L{lane:.1f} {sy:.1f} L{lane:.1f} {ey:.1f} L{tx + tw + 2:.1f} {ey:.1f}" '
                   'fill="none" stroke="#5F5E5A" stroke-width="1.2" marker-end="url(#arr)"/>')
        put_label(lane + 8, (sy + ey) / 2 - (len(label_lines(e)) - 1) * LINE / 2, label_lines(e), anchor="start")

    for n, node in nodes.items():
        x, y, w, h = boxes[n]
        fill, stroke, title_c, sub_c = STYLE[node["kind"]]
        title, details, status = L["text"][n]
        if is_problem(status):
            stroke, dash, sw = "#A32D2D", "", 2
        elif is_done(status):
            dash, sw = "", 2
        else:
            dash, sw = ' stroke-dasharray="5 3"', 1.2
        rx = 22 if node["kind"] == "gate" else 6
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{rx}" fill="{fill}" '
                   f'stroke="{stroke}" stroke-width="{sw}"{dash}/>')
        cx = x + w / 2
        top = y + (h - (18 + 15 * (len(details) + 1))) / 2 + 14
        out.append(f'<text x="{cx:.1f}" y="{top:.1f}" font-size="13" font-weight="bold" fill="{title_c}" '
                   f'text-anchor="middle">{escape(title)}</text>')
        for i, detail in enumerate(details, 1):
            out.append(f'<text x="{cx:.1f}" y="{top + 3 + 15 * i:.1f}" font-size="11" fill="{sub_c}" '
                       f'text-anchor="middle">{escape(detail)}</text>')
        status_c = "#A32D2D" if is_problem(status) else sub_c
        out.append(f'<text x="{cx:.1f}" y="{top + 3 + 15 * (len(details) + 1):.1f}" font-size="11" '
                   f'font-style="italic" fill="{status_c}" text-anchor="middle">{escape(status)}</text>')
    out.extend(label_svg)

    ly = L["height"] + 4
    x = MARGIN
    for kind, name in (("input", "input"), ("agent", "agent"), ("script", "script"), ("gate", "human gate")):
        fill, stroke, _, sub_c = STYLE[kind]
        out.append(f'<rect x="{x}" y="{ly}" width="14" height="12" rx="2" fill="{fill}" stroke="{stroke}"/>')
        out.append(f'<text x="{x + 20}" y="{ly + 10}" font-size="11" fill="#444441">{name}</text>')
        x += 34 + text_w(name, 11)
    out.append(f'<rect x="{x}" y="{ly}" width="14" height="12" rx="2" fill="none" stroke="#7F77DD" '
               'stroke-dasharray="3 2"/>')
    out.append(f'<text x="{x + 20}" y="{ly + 10}" font-size="11" fill="#444441">independence group</text>')
    x += 34 + text_w("independence group", 11)
    out.append(f'<text x="{x + 6}" y="{ly + 10}" font-size="11" fill="#444441">'
               "dashed border = not yet done · solid = completed/approved · red = failed/blocked/rejected</text>")
    out.append(f'<text x="{MARGIN}" y="{ly + 30}" font-size="11" fill="#444441">'
               "Arrows are labelled with the artifacts they carry. No path may link members of an independence "
               "group. Manual hand-off hosts (chatgpt, claude) are not invoked programmatically.</text>")
    note = ("Planned graph: no execution recorded." if not any_attempt
            else "Status is read from the round record; it does not prove what a host actually did.")
    out.append(f'<text x="{MARGIN}" y="{ly + 48}" font-size="11" font-weight="bold" fill="#633806">'
               f"{escape(note)} Generated by agent_harness/scripts/render_round_graph.py; do not edit.</text>")
    out.append("</svg>")
    lines_needed = max(text_w(
        "dashed border = not yet done · solid = completed/approved · red = failed/blocked/rejected", 11)
        + x + 6, text_w(note + " Generated by agent_harness/scripts/render_round_graph.py; do not edit.", 11) + MARGIN,
        text_w("Arrows are labelled with the artifacts they carry. No path may link members of an independence "
               "group. Manual hand-off hosts (chatgpt, claude) are not invoked programmatically.", 11) + MARGIN)
    svg = "\n".join(out) + "\n"
    if lines_needed + MARGIN > width:  # widen canvas so legend text is never clipped
        new_w = lines_needed + MARGIN
        svg = svg.replace(f'width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}"',
                          f'width="{new_w:.0f}" height="{height:.0f}" viewBox="0 0 {new_w:.0f} {height:.0f}"', 1)
        svg = svg.replace(f'<rect width="{width:.0f}" height="{height:.0f}" fill="#FFFFFF"/>',
                          f'<rect width="{new_w:.0f}" height="{height:.0f}" fill="#FFFFFF"/>', 1)
    return svg


def _mm(text: str) -> str:
    return text.replace('"', "#quot;")


def render_mermaid(data: dict) -> str:
    graph = data["graph"]
    ids = {n["id"]: f"n{i}" for i, n in enumerate(graph["nodes"])}
    approval = graph["approval"]
    lines = [
        "%% Generated by agent_harness/scripts/render_round_graph.py; do not edit.",
        f"%% round {data['round_id']} · mode {graph['mode']} · graph approval {approval['status']}",
        "flowchart TD",
    ]
    grouped = {m for g in graph.get("independence_groups", []) for m in g}

    def declare(node: dict) -> str:
        title, details, status = describe(data, node)
        label = _mm("<br/>".join([title] + [f"<small>{d}</small>" for d in details] + [f"<small><i>{status}</i></small>"]))
        shape = {"input": ('(["', '"])'), "agent": ('["', '"]'), "script": ('[["', '"]]'), "gate": ('{{"', '"}}')}
        left, right = shape[node["kind"]]
        return f"  {ids[node['id']]}{left}{label}{right}:::{node['kind']}"

    for node in graph["nodes"]:
        if node["id"] not in grouped:
            lines.append(declare(node))
    for index, group in enumerate(graph.get("independence_groups", []), 1):
        lines.append(f'  subgraph g{index}["independence group {index}"]')
        for node in graph["nodes"]:
            if node["id"] in group:
                lines.append("  " + declare(node))
        lines.append("  end")
    for edge in graph["edges"]:
        carried = ", ".join(edge["carries"]) or "control only"
        if edge.get("lineage"):
            carried += " · lineage: " + ", ".join(edge["lineage"])
        lines.append(f'  {ids[edge["from"]]} -->|"{_mm(carried)}"| {ids[edge["to"]]}')
    for kind, (fill, stroke, title_c, _) in STYLE.items():
        lines.append(f"  classDef {kind} fill:{fill},stroke:{stroke},color:{title_c}")
    return "\n".join(lines) + "\n"


def outputs_for(manifest: Path, out_dir: Path | None) -> tuple[Path, Path]:
    folder = out_dir or manifest.parent
    return folder / "graph.svg", folder / "graph.mmd"


def render(manifest: Path, lab: Path = LAB, out_dir: Path | None = None, check_only: bool = False) -> list[str]:
    """Return problems; write or compare graph.svg and graph.mmd."""
    errors = check(manifest, lab)
    if errors:
        return [f"not drawn, manifest fails validation: {e}" for e in errors]
    data = yaml.load(manifest.read_text(encoding="utf-8"), Loader=UniqueLoader)
    if "graph" not in data:
        return []
    produced = {}
    svg_path, mmd_path = outputs_for(manifest, out_dir)
    produced[svg_path] = render_svg(data)
    produced[mmd_path] = render_mermaid(data)
    problems = []
    for path, content in produced.items():
        if check_only:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                problems.append(f"stale or missing {path.name}; run render_round_graph.py")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("manifest", type=Path, nargs="*")
    parser.add_argument("--root", type=Path, help="render every graph round found in this checkout")
    parser.add_argument("--lab", type=Path, default=LAB, help="Lab roles/schema checkout")
    parser.add_argument("--out-dir", type=Path, help="write images here instead of beside the manifest")
    parser.add_argument("--check", action="store_true", help="fail if images are stale; write nothing")
    args = parser.parse_args()
    if not args.manifest and args.root is None:
        parser.error("provide manifests or --root")
    if args.out_dir and (args.root or len(args.manifest) != 1):
        parser.error("--out-dir needs exactly one manifest")
    paths = sorted(set(args.manifest + (list(discover(args.root)) if args.root else [])))
    failed = False
    drawn = 0
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else None
        if args.root and not (isinstance(data, dict) and "graph" in data):
            continue
        problems = render(path.resolve(), args.lab.resolve(), args.out_dir, args.check)
        if isinstance(data, dict) and "graph" not in data and not problems:
            print(f"SKIP (no graph block): {path}")
            continue
        failed |= bool(problems)
        drawn += not problems
        for problem in problems:
            print(f"FAIL: {path}: {problem}")
        if not problems:
            svg, _ = outputs_for(path, args.out_dir)
            print(f"{'CURRENT' if args.check else 'WROTE'}: {svg} (+ graph.mmd)")
    print(f"{drawn} graph(s) {'checked' if args.check else 'drawn'}; {'FAIL' if failed else 'PASS'}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
