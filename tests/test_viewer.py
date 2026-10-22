import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("viewer_export", ROOT / "viewer/export.py")
viewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(viewer)


def embedded(bundle):
    text = (bundle / "data.js").read_text(encoding="utf-8")
    return json.loads(text.split("window.KG_BUNDLE = ", 1)[1].rstrip().rstrip(";"))


def test_bundle_embeds_current_graph(tmp_path):
    bundle = viewer.export(out_dir=tmp_path)
    graph = json.loads((ROOT / "graph/generated/knowledge.json").read_text())
    data = embedded(bundle)
    assert data["graph"] == graph
    assert data["meta"]["fresh"] is True
    assert data["meta"]["graph_revision"] == graph["revision"]
    assert bundle.name == f"kg-viewer-{graph['revision'][:12]}"


def test_pages_are_offline_and_self_contained(tmp_path):
    bundle = viewer.export(out_dir=tmp_path, make_zip=False)
    for page in ["index.html", "catalogue.html"]:
        html = (bundle / page).read_text(encoding="utf-8")
        refs = re.findall(r'(?:src|href)="([^"#]+)', html)
        assert refs
        for ref in refs:
            assert "://" not in ref, f"{page} loads remote {ref}"
            assert (bundle / ref).is_file(), f"{page} references missing {ref}"


def test_manifest_hashes_bundle_files(tmp_path):
    bundle = viewer.export(out_dir=tmp_path, make_zip=False)
    manifest = json.loads((bundle / "manifest.json").read_text())
    files = {
        p.relative_to(bundle).as_posix()
        for p in bundle.rglob("*")
        if p.is_file() and p.name != "manifest.json"
    }
    assert set(manifest["files"]) == files
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((bundle / name).read_bytes()).hexdigest() == digest


def test_zip_is_deterministic(tmp_path):
    first = viewer.export(out_dir=tmp_path / "a")
    second = viewer.export(out_dir=tmp_path / "b")
    assert (
        first.with_suffix(".zip").read_bytes()
        == second.with_suffix(".zip").read_bytes()
    )


def test_stale_graph_requires_explicit_opt_in(tmp_path):
    graph = json.loads((ROOT / "graph/generated/knowledge.json").read_text())
    graph["nodes"] = graph["nodes"][1:]
    stale = tmp_path / "knowledge.json"
    stale.write_text(json.dumps(graph))
    with pytest.raises(viewer.ViewerError, match="stale"):
        viewer.export(graph_path=stale, out_dir=tmp_path / "out")
    bundle = viewer.export(graph_path=stale, out_dir=tmp_path / "out", allow_stale=True)
    assert embedded(bundle)["meta"]["fresh"] is False


def test_script_embedding_cannot_close_script_element():
    assert "</script>" not in viewer.script_json({"context": "</script><b>"})


def test_governance_vocabulary_and_deep_link(tmp_path):
    node = shutil.which('node')
    if not node:
        pytest.skip('Node is required to exercise the browser vocabulary')
    bundle = viewer.export(out_dir=tmp_path, make_zip=False)
    script = r'''
const assert = require('node:assert/strict');
global.window = {KG_BUNDLE: {}, matchMedia: () => ({addEventListener() {}})};
global.document = {documentElement: {getAttribute() {return null;}}};
require(process.argv[1]);
const kg = window.KGV;
const shapes = new Set();
for (const type of ['harness', 'role', 'skill']) {
  assert.equal(kg.layerFor(type).key, 'governance');
  shapes.add(JSON.stringify(kg.shapeFor(type)));
  assert.match(kg.shapeIcon(type), /polygon/);
}
assert.equal(shapes.size, 3);
'''
    result = subprocess.run([node, '-e', script, str(bundle / 'common.js')], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    data = embedded(bundle)
    assert any(n['id'] == 'harness:round-bound-research' for n in data['graph']['nodes'])
    assert 'index.html#node=harness%3Around-bound-research' in (bundle / 'common.js').read_text()
