"""Keep the README overview diagram in sync with the repository.

These checks fail when the committed SVG is stale, when a source the diagram cites is
renamed or removed, when a new non-superseded ADR or phase spec is not reflected in the
diagram, or when README.md stops embedding it. Fix by editing
docs/img/build_overview_diagram.py and regenerating (see its docstring).
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs" / "img" / "build_overview_diagram.py"


def _load():
    spec = importlib.util.spec_from_file_location("build_overview_diagram", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


diagram = _load()


def _tags():
    return [tag for row in diagram.ROWS for tag in row["tags"]]


def test_committed_svg_matches_generator():
    assert diagram.OUTPUT.read_text(encoding="utf-8") == diagram.render(), (
        "docs/img/problems-and-approaches.svg is stale; run "
        "python docs/img/build_overview_diagram.py"
    )


def test_readme_embeds_diagram_and_glossary():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "](docs/img/problems-and-approaches.svg)" in readme
    assert "](GLOSSARY.md)" in readme


def test_cited_sources_exist():
    missing = [(label, path) for label, path in _tags() if not list(ROOT.glob(path))]
    assert not missing, f"diagram cites sources that do not exist: {missing}"


def test_cited_search_scopes_are_registered():
    scopes = (ROOT / "research/methodology/search_scopes.csv").read_text(
        encoding="utf-8"
    )
    for label, _path in _tags():
        for scope_id in re.findall(r"SS-\d{4}", label):
            assert scope_id in scopes, f"{scope_id} is not in search_scopes.csv"


def test_every_active_adr_is_cited():
    cited = {label for label, _path in _tags()}
    for adr in sorted((ROOT / "docs/adr").glob("[0-9][0-9][0-9][0-9]-*.md")):
        number = adr.name[:4]
        if number == "0000":
            continue  # template
        status = re.search(r"\*\*Status:\*\*\s*(.+)", adr.read_text(encoding="utf-8"))
        if status and status.group(1).strip().lower().startswith("superseded"):
            continue
        assert f"ADR {number}" in cited, (
            f"{adr.name} is not superseded but the overview diagram does not cite it; "
            "update docs/img/build_overview_diagram.py and README.md"
        )


def test_roadmap_matches_phase_specs():
    spec_phases = {
        p.name.split("_", 1)[0] for p in (ROOT / "specs").glob("v[0-9]*_*.md")
    }
    diagram_phases = {phase for phase, *_rest in diagram.PHASES}
    assert spec_phases == diagram_phases, (
        f"phase specs {sorted(spec_phases)} differ from diagram roadmap "
        f"{sorted(diagram_phases)}; update the diagram and README.md"
    )
