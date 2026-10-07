// Catalogue page: sortable, filterable tables of concepts and relationships.
(function () {
  "use strict";

  const { bundle, LAYERS, layerFor, shapeIcon, esc } = KGV;
  const graph = bundle.graph;
  KGV.renderHeader("catalogue");

  const edges = KGV.allEdges();
  const counts = new Map();
  function bump(id, key) {
    const c = counts.get(id) || { out: 0, in: 0, candidate: 0 };
    c[key] += 1;
    counts.set(id, c);
  }
  edges.forEach((e) => {
    if (e.set === "candidate") {
      bump(e.source, "candidate");
      bump(e.target, "candidate");
    } else {
      bump(e.source, "out");
      bump(e.target, "in");
    }
  });
  const countsFor = (id) => counts.get(id) || { out: 0, in: 0, candidate: 0 };

  const layerOrder = (type) => {
    const i = LAYERS.indexOf(layerFor(type));
    return i < 0 ? LAYERS.length : i;
  };

  document.getElementById("tiles").innerHTML = [
    [graph.nodes.length, "Concepts"],
    [new Set(graph.nodes.map((n) => n.type)).size, "Concept types"],
    [graph.relationships.length, "Validated relationships"],
    [graph.candidate_relationships.length, "Candidate relationships"],
  ]
    .map(([v, l]) => `<div class="tile"><div class="value">${v}</div><div class="label">${esc(l)}</div></div>`)
    .join("");

  const nodeLink = (id) =>
    `<a href="index.html#node=${encodeURIComponent(id)}" title="Show in graph"><code>${esc(id)}</code></a>`;

  const VIEWS = {
    concepts: {
      rows: graph.nodes,
      types: [...new Set(graph.nodes.map((n) => n.type))].sort(
        (a, b) => layerOrder(a) - layerOrder(b) || a.localeCompare(b)
      ),
      statuses: [...new Set(graph.nodes.map((n) => n.status))].sort(),
      typeOf: (n) => n.type,
      statusOf: (n) => n.status,
      text: (n) => `${n.id} ${n.title} ${n.context} ${(n.sources || []).join(" ")}`,
      columns: [
        { label: "Type", key: (n) => `${layerOrder(n.type)}-${n.type}`,
          cell: (n) => `<span class="type-cell">${shapeIcon(n.type)} ${esc(n.type)}</span>` },
        { label: "ID", key: (n) => n.id, cell: (n) => nodeLink(n.id) },
        { label: "Title", key: (n) => n.title, cell: (n) => esc(n.title) },
        { label: "Status", key: (n) => n.status, cell: (n) => `<span class="pill">${esc(n.status)}</span>` },
        { label: "Version", key: (n) => n.version, cell: (n) => esc(n.version) },
        { label: "Updated", key: (n) => n.updated, cell: (n) => esc(n.updated) },
        { label: "Review after", key: (n) => n.review_after, cell: (n) => esc(n.review_after) },
        { label: "Out", num: true, key: (n) => countsFor(n.id).out, cell: (n) => countsFor(n.id).out },
        { label: "In", num: true, key: (n) => countsFor(n.id).in, cell: (n) => countsFor(n.id).in },
        { label: "Candidate", num: true, key: (n) => countsFor(n.id).candidate, cell: (n) => countsFor(n.id).candidate },
      ],
      detail: (n) => `
        <div class="context">${KGV.renderContext(n.context)}</div>
        <dl class="meta">
          <dt>Record</dt><dd><code>${esc(n.path)}</code></dd>
          <dt>Sources</dt><dd>${(n.sources || []).map((s) => `<code>${esc(s)}</code>`).join("<br>") || "—"}</dd>
        </dl>
        ${n.parameters && Object.keys(n.parameters).length ? `<pre class="json">${esc(JSON.stringify(n.parameters, null, 2))}</pre>` : ""}`,
      idOf: (n) => n.id,
    },
    relationships: {
      rows: edges,
      types: [...new Set(edges.map((e) => e.type))].sort(),
      statuses: ["validated", "candidate"],
      typeOf: (e) => e.type,
      statusOf: (e) => e.set,
      text: (e) => `${e.source} ${e.type} ${e.target} ${(e.sources || []).join(" ")} ${e.review ? `${e.review.by} ${e.review.basis}` : ""}`,
      columns: [
        { label: "Source", key: (e) => e.source, cell: (e) => nodeLink(e.source) },
        { label: "Relation", key: (e) => e.type, cell: (e) => `<span class="mono">${esc(e.type)}</span>` },
        { label: "Target", key: (e) => e.target, cell: (e) => nodeLink(e.target) },
        { label: "Status", key: (e) => e.set,
          cell: (e) => `<span class="pill ${e.set === "candidate" ? "candidate" : ""}">${esc(e.set)}</span>` },
        { label: "Reviewed by", key: (e) => (e.review ? e.review.by : ""), cell: (e) => esc(e.review ? e.review.by : "—") },
        { label: "Review date", key: (e) => (e.review ? e.review.date : ""), cell: (e) => esc(e.review ? e.review.date : "—") },
        { label: "Sources", key: (e) => (e.sources || []).join(" "),
          cell: (e) => (e.sources || []).map((s) => `<code>${esc(s)}</code>`).join("<br>") || "—" },
      ],
      detail: null,
      idOf: (e) => e.key,
    },
  };

  const state = { view: "concepts", sort: { concepts: [0, 1], relationships: [0, 1] }, expanded: new Set() };
  const text = document.getElementById("filter-text");
  const typeSel = document.getElementById("filter-type");
  const statusSel = document.getElementById("filter-status");
  const table = document.getElementById("table");
  const resultCount = document.getElementById("result-count");

  function fillSelect(select, label, values) {
    select.innerHTML = `<option value="">All ${label}</option>` +
      values.map((v) => `<option value="${esc(v)}">${esc(v)}</option>`).join("");
  }

  function setView(view) {
    state.view = view;
    document.getElementById("tab-concepts").setAttribute("aria-selected", view === "concepts");
    document.getElementById("tab-relationships").setAttribute("aria-selected", view === "relationships");
    fillSelect(typeSel, view === "concepts" ? "concept types" : "relation types", VIEWS[view].types);
    fillSelect(statusSel, "statuses", VIEWS[view].statuses);
    render();
  }

  function render() {
    const view = VIEWS[state.view];
    const q = text.value.trim().toLowerCase();
    const [sortCol, dir] = state.sort[state.view];
    const col = view.columns[sortCol];
    const rows = view.rows
      .filter((r) => !typeSel.value || view.typeOf(r) === typeSel.value)
      .filter((r) => !statusSel.value || view.statusOf(r) === statusSel.value)
      .filter((r) => !q || view.text(r).toLowerCase().includes(q))
      .sort((a, b) => {
        const ka = col.key(a);
        const kb = col.key(b);
        const c = typeof ka === "number" ? ka - kb : String(ka).localeCompare(String(kb));
        return c * dir || view.idOf(a).localeCompare(view.idOf(b));
      });

    const head = view.columns
      .map((c, i) => `<th scope="col" data-col="${i}" class="${c.num ? "num" : ""}"
        aria-sort="${i === sortCol ? (dir > 0 ? "ascending" : "descending") : "none"}">${esc(c.label)}</th>`)
      .join("");
    const body = rows
      .map((r) => {
        const id = view.idOf(r);
        const cells = view.columns.map((c) => `<td class="${c.num ? "num" : ""}">${c.cell(r)}</td>`).join("");
        if (!view.detail) return `<tr>${cells}</tr>`;
        const open = state.expanded.has(id);
        const main = `<tr class="concept ${open ? "expanded" : ""}" data-id="${esc(id)}" aria-expanded="${open}">${cells}</tr>`;
        return open
          ? `${main}<tr class="expanded"><td colspan="${view.columns.length}">${view.detail(r)}</td></tr>`
          : main;
      })
      .join("");
    table.innerHTML = `<thead><tr>${head}</tr></thead><tbody>${body}</tbody>`;
    resultCount.textContent = `${rows.length} of ${view.rows.length} ${state.view}` +
      (state.view === "concepts" ? " · click a row for its context; click an ID to show it in the graph" : "");
    KGV.writeHash({ tab: state.view === "concepts" ? "" : state.view, q: text.value.trim() });
  }

  table.addEventListener("click", (ev) => {
    const th = ev.target.closest("th[data-col]");
    if (th) {
      const col = Number(th.dataset.col);
      const [cur, dir] = state.sort[state.view];
      state.sort[state.view] = [col, cur === col ? -dir : 1];
      return render();
    }
    if (ev.target.closest("a")) return;
    const row = ev.target.closest("tr.concept");
    if (!row) return;
    const id = row.dataset.id;
    if (state.expanded.has(id)) state.expanded.delete(id);
    else state.expanded.add(id);
    render();
  });
  [text, typeSel, statusSel].forEach((el) => el.addEventListener("input", render));
  document.getElementById("tab-concepts").addEventListener("click", () => setView("concepts"));
  document.getElementById("tab-relationships").addEventListener("click", () => setView("relationships"));

  // Deep links: #node=<id> opens that concept; #tab=relationships&q=<text> restores a filter.
  const hash = KGV.readHash();
  if (hash.node) {
    text.value = hash.node;
    state.expanded.add(hash.node);
  } else if (hash.q) {
    text.value = hash.q;
  }
  setView(hash.tab === "relationships" ? "relationships" : "concepts");
})();
