"""Build the README overview diagram: docs/img/problems-and-approaches.svg.

The diagram summarises the repository's current problems, the approaches that address
them and the phased roadmap. It must stay in sync with README.md and the canonical
sources it cites (ADRs, specs, governance). When the scope, phases, ADRs, key
constraints or other significant details change:

1. edit the content section below (HEADER, WARNING, ROWS, PHASES, FOOTNOTE);
2. run ``python docs/img/build_overview_diagram.py`` from the repository root;
3. update README.md if its wording or the overview section is affected;
4. commit the script and the regenerated SVG together.

``python docs/img/build_overview_diagram.py --check`` exits non-zero if the committed SVG
differs from what this script generates. ``tests/test_overview_diagram.py`` runs that
check and verifies that every cited source exists, every non-superseded ADR is cited and
every phase spec appears in the roadmap.

Text wrapping uses fixed character-width tables (DejaVu Sans metrics, which are wider
than common UI fonts), so output is deterministic and needs no font files or third-party
packages.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = REPO_ROOT / "docs" / "img" / "problems-and-approaches.svg"

# ---------------------------------------------------------------------------
# Content — edit here when the repository's scope or significant details change.
# Each tag is (label shown in the diagram, repository path glob that must exist).
# ---------------------------------------------------------------------------

HEADER = (
    "Forest Cover Lab — problems and how the repo addresses them",
    (
        "Governance, research and evidence registry for forest-cover estimation from "
        "satellite data. Executable workflows live in downstream repos."
    ),
)

WARNING = (
    "⚠ Binding constraint:",
    (
        " Hansen annual loss ≠ monthly ground truth. Monthly forest cover is never "
        "reported as verified when derived from annual weak labels."
    ),
)

ROWS = [
    {
        "problem": "Annual labels are not monthly truth",
        "problem_text": "Hansen lossyear says a pixel was lost in a year, not in which "
        "month. Training and scoring monthly models on it leaks labels and overclaims "
        "accuracy.",
        "approach": "Separate targets + weak supervision",
        "approach_text": "Monthly coverage, monthly disturbance probability and annual "
        "supervision are distinct concepts. v3 treats monthly state as latent, pools "
        "monthly events to the annual bag (e.g. noisy-OR) and reports agreement as "
        "consistency, not accuracy.",
        "tags": [
            ("ADR 0004", "docs/adr/0004-*.md"),
            ("specs/v3", "specs/v3_*.md"),
            ("claim:monthly-non-truth", "knowledge/claims/claim-monthly-non-truth.md"),
        ],
    },
    {
        "problem": "“Forest” is ambiguous",
        "problem_text": "Area numbers are meaningless when the threshold, minimum mapping "
        "area, exclusions and nodata handling are left implicit or hardcoded.",
        "approach": "Explicit, versioned forest definition",
        "approach_text": "Every run declares dataset, threshold variable and value, "
        "minimum mapping area, exclusions, nodata policy and temporal interpretation; "
        "defaults live in config, never in code.",
        "tags": [
            ("ADR 0002", "docs/adr/0002-*.md"),
            ("configs/v1_defaults.yaml", "configs/v1_defaults.yaml"),
        ],
    },
    {
        "problem": "Area depends on projection",
        "problem_text": "Pixel counts in EPSG:4326 or a conformal CRS distort hectares, "
        "especially away from the equator.",
        "approach": "Exchange vs. area CRS policy",
        "approach_text": "Exchange geometries in EPSG:4326; compute area in an equal-area "
        "CRS (EPSG:6933 globally) or geodesically; always report hectares and the "
        "method used.",
        "tags": [("ADR 0003", "docs/adr/0003-*.md")],
    },
    {
        "problem": "Monthly signal is noisy",
        "problem_text": "Clouds, seasonal browning and single-month anomalies trigger "
        "false alerts; optical and SAR evidence can disagree.",
        "approach": "Composite, confirm, persist",
        "approach_text": "Cloud-masked monthly S2 and S1 composites; NDVI/NDMI anomalies "
        "confirmed by SAR backscatter; an N-consecutive-month persistence rule; "
        "per-pixel optical/SAR disagreement flags.",
        "tags": [
            ("specs/v2", "specs/v2_*.md"),
            (
                "workflow: sentinel-monthly",
                "knowledge/workflows/workflow-sentinel-monthly-*.md",
            ),
        ],
    },
    {
        "problem": "Model value is unknown locally",
        "problem_text": "Eight GeoFM families look promising, but none is integrated or "
        "benchmarked; published scores do not transfer to a local forest-loss task.",
        "approach": "Harnessed experiments before agents",
        "approach_text": "Compare B0 (current rules), B1 (raw-feature model) and F1–F4 "
        "(frozen encoder, adaptation, fusion, stacking) on independent, spatially and "
        "temporally blocked reference samples with predeclared metrics.",
        "tags": [
            ("docs/architecture.md", "docs/architecture.md"),
            ("SS-0002", "research/methodology/search_scopes.csv"),
        ],
    },
    {
        "problem": "Platform lock-in",
        "problem_text": "Production methods tied to Google Earth Engine cannot be "
        "reproduced or run independently at regional or country scale.",
        "approach": "Methods separated from backends",
        "approach_text": "Open, local, cloud-neutral tooling for production (STAC, "
        "GDAL/rasterio, xarray, DuckDB); GEE remains an optional reference or research "
        "route.",
        "tags": [("ADR 0005", "docs/adr/0005-*.md")],
    },
    {
        "problem": "Agent plans are not observed execution",
        "problem_text": "A selected role or host name does not prove which instructions "
        "were loaded, which tools ran or whether evidence is independent.",
        "approach": "Discoverable roles and round provenance",
        "approach_text": "Candidate role/harness/skill graph contracts and bounded assignments; "
        "record actual hosts, pinned repositories, loaded-file hashes, evidence and "
        "checks. Human review governs scientific promotion.",
        "tags": [
            ("ADR 0006", "docs/adr/0006-*.md"),
            ("ADR 0008", "docs/adr/0007-*.md"),
            ("docs/agents.md", "docs/agents.md"),
            ("round schema", "agent_harness/schemas/round.schema.json"),
        ],
    },
    {
        "problem": "Knowledge and repos drift",
        "problem_text": "Evidence gets scattered, downstream repos redefine contracts, and "
        "agents can turn a proposal or a successful run into “validated” "
        "science.",
        "approach": "Governed corpus, graph and provenance",
        "approach_text": "Knowledge corpus + deterministic graph; agent output enters as "
        "candidate and needs human review to promote; run manifests with semantic "
        "provenance; drift checklist and audit log; downstream repos pin contracts.",
        "tags": [
            ("P1–P6", "governance/principles.md"),
            ("knowledge/ + graph/", "graph/build.py"),
            ("run_manifest", "validate/run_manifest.schema.json"),
        ],
    },
]

# One entry per phase spec in specs/ (the test enforces this).
PHASES = [
    (
        "v1",
        "Evidence-first baseline",
        "Established forest products + explicit forest definition; area in hectares.",
        "#2F6B4F",
    ),
    (
        "v2",
        "Monthly confirmation",
        "S1/S2 monthly composites, SAR confirmation, temporal persistence.",
        "#3E7F9C",
    ),
    (
        "v3",
        "Weakly supervised monthly",
        "Latent monthly state / disturbance under annual supervision, with uncertainty.",
        "#7A5AA6",
    ),
]

FOOTNOTE = (
    "GeoFM uplift, local accuracy and model rankings are currently not measured; "
    "candidate methods stay candidates until human review promotes them."
)

# ---------------------------------------------------------------------------
# Layout and rendering — no edits needed for content changes.
# ---------------------------------------------------------------------------

FONT = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Menlo, Consolas, 'DejaVu Sans Mono', monospace"

C = {
    "bg": "#FFFFFF",
    "ink": "#1F2A24",
    "muted": "#5B665F",
    "line": "#D5DDD8",
    "p_fill": "#FBF1EC",
    "p_edge": "#E3B9A4",
    "p_acc": "#B4532A",
    "a_fill": "#EDF5F0",
    "a_edge": "#A9CDB8",
    "a_acc": "#2F6B4F",
    "head": "#1E4D3A",
    "warn_fill": "#FFF6DD",
    "warn_edge": "#E2C26B",
    "warn_ink": "#6B4E00",
}

# Advance widths per 1000 units of font size for ASCII 32..126 (DejaVu Sans).
_REGULAR = [
    318,
    401,
    460,
    838,
    636,
    950,
    780,
    275,
    390,
    390,
    500,
    838,
    318,
    361,
    318,
    337,
    636,
    636,
    636,
    636,
    636,
    636,
    636,
    636,
    636,
    636,
    337,
    337,
    838,
    838,
    838,
    531,
    1000,
    684,
    686,
    698,
    770,
    632,
    575,
    775,
    752,
    295,
    295,
    656,
    557,
    863,
    748,
    787,
    603,
    787,
    695,
    635,
    611,
    732,
    684,
    989,
    685,
    611,
    685,
    390,
    337,
    390,
    838,
    500,
    500,
    613,
    635,
    550,
    635,
    615,
    352,
    635,
    634,
    278,
    278,
    579,
    278,
    974,
    634,
    612,
    635,
    635,
    411,
    521,
    392,
    634,
    592,
    818,
    592,
    592,
    525,
    636,
    337,
    636,
    838,
]
_BOLD = [
    348,
    456,
    521,
    838,
    696,
    1002,
    872,
    306,
    457,
    457,
    523,
    838,
    380,
    415,
    380,
    365,
    696,
    696,
    696,
    696,
    696,
    696,
    696,
    696,
    696,
    696,
    400,
    400,
    838,
    838,
    838,
    580,
    1000,
    774,
    762,
    734,
    830,
    683,
    683,
    821,
    837,
    372,
    372,
    775,
    637,
    995,
    837,
    850,
    733,
    850,
    770,
    720,
    682,
    812,
    774,
    1103,
    771,
    724,
    725,
    457,
    365,
    457,
    838,
    500,
    500,
    675,
    716,
    593,
    716,
    678,
    435,
    716,
    712,
    343,
    343,
    665,
    343,
    1042,
    712,
    687,
    716,
    716,
    493,
    595,
    478,
    712,
    652,
    924,
    645,
    652,
    582,
    712,
    365,
    712,
    838,
]
_EXTRA = {
    False: {"—": 1000, "–": 500, "·": 318, "“": 518, "”": 518},
    True: {"—": 1000, "–": 500, "·": 380, "“": 657, "”": 657},
}


def text_width(text: str, size: float, bold: bool = False) -> float:
    table = _BOLD if bold else _REGULAR
    total = 0
    for ch in text:
        code = ord(ch)
        if 32 <= code <= 126:
            total += table[code - 32]
        else:
            total += _EXTRA[bold].get(ch, 1000)
    return total * size / 1000


def wrap(text: str, size: float, width: float, bold: bool = False) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if text_width(candidate, size, bold) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _text(x, y, content, size, color, bold=False, font=FONT, extra=""):
    weight = ' font-weight="700"' if bold else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}"'
        f'{weight} fill="{color}"{extra}>{escape(content)}</text>'
    )


def _arrow(x1, x2, y):
    return [
        (
            f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
            f'stroke="{C["muted"]}" stroke-width="2"/>'
        ),
        (
            f'<path d="M{x2 - 2:.1f},{y - 6:.1f} L{x2 + 8:.1f},{y:.1f} '
            f'L{x2 - 2:.1f},{y + 6:.1f} Z" fill="{C["muted"]}"/>'
        ),
    ]


def render() -> str:
    width, margin, gap = 1280, 48, 64
    pad = 18
    problem_w = 430
    approach_w = width - 2 * margin - problem_w - gap
    title_size, body_size, tag_size = 17, 14, 12
    title_lh, body_lh = 22, 19.5
    px, ax = margin, margin + problem_w + gap

    out: list[str] = []
    y = margin
    out.append(_text(margin, y + 30, HEADER[0], 30, C["head"], bold=True))
    out.append(_text(margin, y + 58, HEADER[1], 15.5, C["muted"]))
    y += 82

    banner_h = 44
    out.append(
        f'<rect x="{margin}" y="{y}" width="{width - 2 * margin}" height="{banner_h}" '
        f'rx="8" fill="{C["warn_fill"]}" stroke="{C["warn_edge"]}"/>'
    )
    out.append(
        f'<text x="{margin + 18}" y="{y + 28}" font-family="{FONT}" font-size="15.5" '
        f'fill="{C["warn_ink"]}"><tspan font-weight="700">{escape(WARNING[0])}</tspan>'
        f"{escape(WARNING[1])}</text>"
    )
    y += banner_h + 30

    heading = ' letter-spacing="1.5"'
    out.append(_text(px, y, "PROBLEM", 13, C["p_acc"], True, extra=heading))
    out.append(
        _text(ax, y, "APPROACH IN THIS REPO", 13, C["a_acc"], True, extra=heading)
    )
    y += 14

    for index, row in enumerate(ROWS, start=1):
        p_title = wrap(row["problem"], title_size, problem_w - 2 * pad - 34, True)
        p_body = wrap(row["problem_text"], body_size, problem_w - 2 * pad)
        a_title = wrap(row["approach"], title_size, approach_w - 2 * pad, True)
        a_body = wrap(row["approach_text"], body_size, approach_w - 2 * pad)
        p_h = pad + len(p_title) * title_lh + 6 + len(p_body) * body_lh + pad - 4
        a_h = pad + len(a_title) * title_lh + 6 + len(a_body) * body_lh + 34 + pad - 4
        h = max(p_h, a_h)

        for x, w, fill, edge, accent in (
            (px, problem_w, C["p_fill"], C["p_edge"], C["p_acc"]),
            (ax, approach_w, C["a_fill"], C["a_edge"], C["a_acc"]),
        ):
            out.append(
                f'<rect x="{x}" y="{y:.1f}" width="{w}" height="{h:.1f}" rx="10" '
                f'fill="{fill}" stroke="{edge}"/>'
            )
            out.append(
                f'<rect x="{x}" y="{y:.1f}" width="5" height="{h:.1f}" rx="2" '
                f'fill="{accent}"/>'
            )

        cx, cy = px + pad + 11, y + pad + 9
        out.append(f'<circle cx="{cx}" cy="{cy:.1f}" r="12" fill="{C["p_acc"]}"/>')
        out.append(
            _text(
                cx,
                cy + 5,
                str(index),
                13,
                "#FFFFFF",
                True,
                extra=' text-anchor="middle"',
            )
        )
        ty = y + pad + 15
        for i, line in enumerate(p_title):
            out.append(
                _text(
                    px + pad + 34, ty + i * title_lh, line, title_size, C["ink"], True
                )
            )
        ty += len(p_title) * title_lh + 6
        for i, line in enumerate(p_body):
            out.append(_text(px + pad, ty + i * body_lh, line, body_size, C["muted"]))

        out.extend(_arrow(px + problem_w + 10, ax - 16, y + h / 2))

        ty = y + pad + 15
        for i, line in enumerate(a_title):
            out.append(
                _text(ax + pad, ty + i * title_lh, line, title_size, C["a_acc"], True)
            )
        ty += len(a_title) * title_lh + 6
        for i, line in enumerate(a_body):
            out.append(_text(ax + pad, ty + i * body_lh, line, body_size, C["ink"]))

        tag_y = y + h - pad - 20
        tx = ax + pad
        for label, _path in row["tags"]:
            tag_w = text_width(label, tag_size) * 1.02 + 18
            out.append(
                f'<rect x="{tx:.1f}" y="{tag_y:.1f}" width="{tag_w:.1f}" height="22" '
                f'rx="11" fill="#FFFFFF" stroke="{C["a_edge"]}"/>'
            )
            out.append(
                _text(tx + 9, tag_y + 15.5, label, tag_size, C["a_acc"], font=MONO)
            )
            tx += tag_w + 8
        y += h + 16

    y += 18
    out.append(
        f'<line x1="{margin}" y1="{y:.1f}" x2="{width - margin}" y2="{y:.1f}" '
        f'stroke="{C["line"]}"/>'
    )
    y += 30
    out.append(_text(margin, y, "PHASED ROADMAP", 13, C["head"], True, extra=heading))
    y += 16

    phase_gap = 40
    count = len(PHASES)
    phase_w = (width - 2 * margin - (count - 1) * phase_gap) / count
    wrapped = [wrap(desc, body_size, phase_w - 2 * pad) for _, _, desc, _ in PHASES]
    phase_h = max(
        pad + title_lh + 4 + len(lines) * body_lh + pad - 4 for lines in wrapped
    )
    for k, ((phase, name, _desc, color), lines) in enumerate(zip(PHASES, wrapped)):
        x = margin + k * (phase_w + phase_gap)
        out.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{phase_w:.1f}" height="{phase_h:.1f}" '
            f'rx="10" fill="#FFFFFF" stroke="{color}" stroke-width="1.5"/>'
        )
        out.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{phase_w:.1f}" height="5" rx="2" '
            f'fill="{color}"/>'
        )
        out.append(_text(x + pad, y + pad + 16, f"{phase} · {name}", 15.5, color, True))
        for i, line in enumerate(lines):
            out.append(
                _text(
                    x + pad,
                    y + pad + 16 + title_lh + 4 + i * body_lh,
                    line,
                    body_size,
                    C["ink"],
                )
            )
        if k < count - 1:
            out.extend(
                _arrow(x + phase_w + 8, x + phase_w + phase_gap - 14, y + phase_h / 2)
            )
    y += phase_h + 34
    out.append(_text(margin, y, FOOTNOTE, 13, C["muted"]))
    height = int(y + margin - 14)

    description = (
        f"{len(ROWS)} problems in forest-cover estimation ("
        + "; ".join(row["problem"] for row in ROWS)
        + ") mapped to the repository approaches that address them, plus the "
        + ", ".join(p[0] for p in PHASES)
        + " roadmap."
    )
    head = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">'
        ),
        '<title id="t">Forest Cover Lab: problems and approaches</title>',
        f'<desc id="d">{escape(description)}</desc>',
        f'<rect width="{width}" height="{height}" fill="{C["bg"]}"/>',
    ]
    return "\n".join(head + out + ["</svg>"]) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check", action="store_true", help="fail if the committed SVG is out of date"
    )
    args = parser.parse_args(argv)
    svg = render()
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != svg:
            print(
                f"{OUTPUT.relative_to(REPO_ROOT)} is out of date; run "
                "python docs/img/build_overview_diagram.py",
                file=sys.stderr,
            )
            return 1
        print(f"{OUTPUT.relative_to(REPO_ROOT)} is up to date")
        return 0
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
