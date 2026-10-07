// Interactive graph page: filters, layouts, focus and record details.
(function () {
  "use strict";

  const { bundle, LAYERS, OTHER, layerFor, shapeFor, shapeIcon, cssVar, esc } = KGV;
  const graph = bundle.graph;
  KGV.renderHeader("graph");

  const nodesById = new Map(graph.nodes.map((n) => [n.id, n]));
  const edges = KGV.allEdges();
  const edgesByKey = new Map(edges.map((e) => [e.key, e]));
  const dangling = edges.filter((e) => !nodesById.has(e.source) || !nodesById.has(e.target));
  const drawable = edges.filter((e) => nodesById.has(e.source) && nodesById.has(e.target));

  const degree = new Map();
  drawable.forEach((e) => {
    degree.set(e.source, (degree.get(e.source) || 0) + 1);
    degree.set(e.target, (degree.get(e.target) || 0) + 1);
  });
  const maxDegree = Math.max(1, ...degree.values());

  const types = [...new Set(graph.nodes.map((n) => n.type))].sort((a, b) => {
    const la = LAYERS.indexOf(layerFor(a));
    const lb = LAYERS.indexOf(layerFor(b));
    const ia = la < 0 ? LAYERS.length : la;
    const ib = lb < 0 ? LAYERS.length : lb;
    return ia - ib || layerFor(a).types.indexOf(a) - layerFor(b).types.indexOf(b) || a.localeCompare(b);
  });
  const relations = [...new Set(edges.map((e) => e.type))].sort();

  const elements = [
    ...graph.nodes.map((n) => ({
      group: "nodes",
      data: {
        id: n.id,
        label: KGV.shortLabel(n),
        type: n.type,
        layer: layerFor(n.type).key,
        size: 18 + 22 * Math.sqrt((degree.get(n.id) || 0) / maxDegree),
      },
    })),
    ...drawable.map((e) => ({
      group: "edges",
      data: { id: e.key, source: e.source, target: e.target, rel: e.type, set: e.set },
    })),
  ];

  function style() {
    const text2 = cssVar("--text-secondary");
    const text1 = cssVar("--text-primary");
    const surface = cssVar("--surface-1");
    const rules = [
      {
        selector: "node",
        style: {
          width: "data(size)",
          height: "data(size)",
          "border-width": 2,
          "border-color": surface,
          label: "data(label)",
          "font-size": 11,
          color: text2,
          "text-valign": "bottom",
          "text-margin-y": 4,
          "text-wrap": "ellipsis",
          "text-max-width": 130,
          "min-zoomed-font-size": 5,
        },
      },
      ...[...LAYERS, OTHER].map((layer) => ({
        selector: `node[layer = "${layer.key}"]`,
        style: { "background-color": cssVar(layer.slot) },
      })),
      ...types.map((type) => {
        const shape = shapeFor(type);
        const s = shape.ellipse
          ? { shape: "ellipse" }
          : shape.roundRect
            ? { shape: "round-rectangle" }
            : { shape: "polygon", "shape-polygon-points": shape.polygon.map((v) => +v.toFixed(3)).join(" ") };
        return { selector: `node[type = "${type}"]`, style: s };
      }),
      {
        selector: "edge",
        style: {
          width: 1.5,
          "line-color": cssVar("--edge"),
          "target-arrow-color": cssVar("--edge"),
          "target-arrow-shape": "triangle",
          "arrow-scale": 0.8,
          "curve-style": "bezier",
          "font-size": 9,
          "min-zoomed-font-size": 6,
          color: text2,
          "text-rotation": "autorotate",
          "text-background-color": surface,
          "text-background-opacity": 1,
          "text-background-padding": 2,
        },
      },
      {
        selector: 'edge[set = "candidate"]',
        style: {
          "line-style": "dashed",
          "line-dash-pattern": [6, 4],
          "line-color": cssVar("--edge-candidate"),
          "target-arrow-color": cssVar("--edge-candidate"),
        },
      },
      { selector: "edge.labelled", style: { label: "data(rel)" } },
      { selector: ".hidden", style: { display: "none" } },
      { selector: ".faded", style: { opacity: 0.12, "text-opacity": 0 } },
      { selector: "node.match", style: { "border-color": text1, "border-width": 3 } },
      {
        selector: "node.focus",
        style: { color: text1, "font-weight": 600, "z-index": 10 },
      },
      {
        selector: "node:selected",
        style: { "border-color": text1, "border-width": 3, color: text1, "font-weight": 700 },
      },
      {
        selector: "edge.focus",
        style: {
          width: 2.25,
          "line-color": text2,
          "target-arrow-color": text2,
          "z-index": 9,
        },
      },
      {
        selector: "edge:selected",
        style: { width: 3, "line-color": text1, "target-arrow-color": text1, label: "data(rel)" },
      },
    ];
    return rules;
  }

  const cy = cytoscape({
    container: document.getElementById("cy"),
    elements,
    style: style(),
    minZoom: 0.15,
    maxZoom: 3,
    selectionType: "single",
    boxSelectionEnabled: false,
  });
  KGV.onThemeChange(() => cy.style(style()));

  // ---- Layouts -------------------------------------------------------------
  // Columns are deterministic; the force layout starts from them, so a given
  // graph always opens in the same arrangement.
  function columnPositions(eles) {
    const byType = new Map();
    eles.nodes().forEach((n) => {
      const list = byType.get(n.data("type")) || [];
      list.push(n);
      byType.set(n.data("type"), list);
    });
    const positions = {};
    let column = 0;
    types.forEach((type) => {
      const list = byType.get(type);
      if (!list) return;
      list.sort((a, b) => a.id().localeCompare(b.id()));
      list.forEach((n, i) => {
        positions[n.id()] = { x: column * 190, y: (i - (list.length - 1) / 2) * 56 };
      });
      column += 1;
    });
    return positions;
  }

  function layoutOptions(name, eles) {
    if (name === "columns" || name === "seed") {
      const positions = columnPositions(eles);
      return { name: "preset", positions: (n) => positions[n.id()], fit: true, padding: 40 };
    }
    if (name === "concentric") {
      return {
        name: "concentric",
        concentric: (n) => degree.get(n.id()) || 0,
        levelWidth: () => 3,
        minNodeSpacing: 28,
        fit: true,
        padding: 40,
        animate: false,
      };
    }
    if (name === "hierarchy") {
      return {
        name: "breadthfirst",
        directed: true,
        spacingFactor: 1.1,
        roots: eles.nodes().filter((n) => n.indegree(false) === 0 && n.outdegree(false) > 0),
        fit: true,
        padding: 40,
        animate: false,
      };
    }
    return {
      name: "cose",
      randomize: false,
      animate: false,
      fit: true,
      padding: 40,
      nodeRepulsion: () => 22000,
      idealEdgeLength: () => 110,
      edgeElasticity: () => 80,
      gravity: 0.6,
      numIter: 1500,
      nodeDimensionsIncludeLabels: true,
    };
  }

  function runLayout() {
    const eles = cy.elements().not(".hidden");
    const name = document.getElementById("layout").value;
    if (name === "force") eles.layout(layoutOptions("seed", eles)).run();
    eles.layout(layoutOptions(name, eles)).run();
  }

  // ---- Filters -------------------------------------------------------------
  const typeState = new Map(types.map((t) => [t, true]));
  const relState = new Map(relations.map((r) => [r, true]));
  const setState = new Map([["validated", true], ["candidate", true]]);

  function checkbox(container, id, labelHtml, count, checked, onChange) {
    const label = document.createElement("label");
    label.className = "check";
    label.htmlFor = id;
    label.innerHTML = `<input type="checkbox" id="${esc(id)}" ${checked ? "checked" : ""}>${labelHtml}<span class="count">${count}</span>`;
    label.querySelector("input").addEventListener("change", (ev) => onChange(ev.target.checked));
    container.appendChild(label);
  }

  const typeBox = document.getElementById("type-filters");
  [...LAYERS, OTHER].forEach((layer) => {
    const layerTypes = types.filter((t) => layerFor(t) === layer);
    if (!layerTypes.length) return;
    const h = document.createElement("h3");
    h.textContent = layer.label;
    typeBox.appendChild(h);
    layerTypes.forEach((t) => {
      const count = graph.nodes.filter((n) => n.type === t).length;
      checkbox(typeBox, `type-${t}`, `${shapeIcon(t)} ${esc(t)}`, count, true, (on) => {
        typeState.set(t, on);
        applyFilters();
      });
    });
  });

  const statusBox = document.getElementById("status-filters");
  [["validated", "Validated"], ["candidate", "Candidate"]].forEach(([key, label]) => {
    const count = drawable.filter((e) => e.set === key).length;
    checkbox(statusBox, `set-${key}`, `<span class="swatch-line ${key}"></span> ${label}`, count, true, (on) => {
      setState.set(key, on);
      applyFilters();
    });
  });

  const relBox = document.getElementById("relation-filters");
  relations.forEach((r) => {
    const count = drawable.filter((e) => e.type === r).length;
    checkbox(relBox, `rel-${r}`, `<span class="mono">${esc(r)}</span>`, count, true, (on) => {
      relState.set(r, on);
      applyFilters();
    });
  });

  const hideOrphans = document.getElementById("hide-orphans");
  hideOrphans.addEventListener("change", applyFilters);

  function applyFilters() {
    cy.batch(() => {
      cy.nodes().forEach((n) => n.toggleClass("hidden", !typeState.get(n.data("type"))));
      cy.edges().forEach((e) => {
        const visible =
          relState.get(e.data("rel")) &&
          setState.get(e.data("set")) &&
          !e.source().hasClass("hidden") &&
          !e.target().hasClass("hidden");
        e.toggleClass("hidden", !visible);
      });
      if (hideOrphans.checked) {
        cy.nodes().forEach((n) => {
          if (!n.hasClass("hidden") && n.connectedEdges().not(".hidden").empty()) n.addClass("hidden");
        });
      }
    });
    const selected = cy.$("node:selected");
    if (selected.nonempty() && selected.hasClass("hidden")) clearFocus();
    else if (selected.nonempty()) focusNode(selected.id(), false);
  }

  // ---- Focus and details ---------------------------------------------------
  const details = document.getElementById("details");
  const initialDetails = details.innerHTML;
  const depthSelect = document.getElementById("depth");

  // Walk visible edges only, so hidden (e.g. candidate) edges never pull in neighbours.
  function neighbourhood(node, depth) {
    let nodes = node.collection();
    let traversed = cy.collection();
    for (let i = 0; i < depth; i++) {
      const step = nodes.connectedEdges().not(".hidden");
      traversed = traversed.union(step);
      nodes = nodes.union(step.connectedNodes());
    }
    return nodes.union(traversed);
  }

  function clearFocus() {
    cy.elements().removeClass("faded focus");
    cy.elements().unselect();
    details.innerHTML = initialDetails;
    KGV.writeHash({});
  }

  function focusNode(id, animate) {
    const node = cy.getElementById(id);
    if (node.empty()) return;
    if (node.hasClass("hidden")) {
      // Reveal the type so a link from the catalogue never lands on nothing.
      const box = document.getElementById(`type-${node.data("type")}`);
      if (box) box.checked = true;
      typeState.set(node.data("type"), true);
      applyFilters();
    }
    const hood = neighbourhood(node, Number(depthSelect.value));
    cy.batch(() => {
      cy.elements().unselect().removeClass("focus").addClass("faded");
      hood.removeClass("faded").addClass("focus");
      node.select();
    });
    if (animate !== false) {
      cy.animate({ fit: { eles: hood, padding: 70 }, duration: 250 });
    }
    renderNode(nodesById.get(id));
    KGV.writeHash({ node: id });
  }

  function focusEdge(key) {
    const edge = cy.getElementById(key);
    const e = edgesByKey.get(key);
    cy.batch(() => {
      cy.elements().unselect().removeClass("focus").addClass("faded");
      edge.union(edge.connectedNodes()).removeClass("faded").addClass("focus");
      edge.select();
    });
    renderEdge(e);
  }

  function nodeButton(id) {
    const node = nodesById.get(id);
    const icon = node ? shapeIcon(node.type, 12) : "";
    return `${icon} <button type="button" class="link-btn" data-node="${esc(id)}"
      title="${esc(node ? node.title : "Unresolved reference")}">${esc(id)}</button>`;
  }

  function setPill(set) {
    return `<span class="pill ${set === "candidate" ? "candidate" : ""}">${esc(set)}</span>`;
  }

  function sourcesList(sources) {
    if (!sources || !sources.length) return "—";
    return sources.map((s) => `<code>${esc(s)}</code>`).join("<br>");
  }

  function relList(list, direction) {
    if (!list.length) return '<p class="hint">None.</p>';
    const sorted = [...list].sort(
      (a, b) => a.type.localeCompare(b.type) || (a.set > b.set ? 1 : -1) || a.key.localeCompare(b.key)
    );
    return `<ul class="rels">${sorted
      .map((e) => {
        const other = direction === "out" ? e.target : e.source;
        return `<li><span class="rel mono"><button type="button" class="link-btn" data-edge="${esc(e.key)}">${esc(e.type)}</button></span>
          <span>${nodeButton(other)}</span>${setPill(e.set)}</li>`;
      })
      .join("")}</ul>`;
  }

  function renderNode(n) {
    const out = edges.filter((e) => e.source === n.id);
    const inc = edges.filter((e) => e.target === n.id);
    const layer = layerFor(n.type);
    const params = n.parameters && Object.keys(n.parameters).length
      ? `<h2>Parameters</h2><pre class="json">${esc(JSON.stringify(n.parameters, null, 2))}</pre>`
      : "";
    details.innerHTML = `
      <div class="tagline">${shapeIcon(n.type, 16)} <span>${esc(n.type)} · ${esc(layer.label)}</span>
        <span class="pill">${esc(n.status)}</span></div>
      <h2 class="title">${esc(n.title)}</h2>
      <code>${esc(n.id)}</code>
      <dl class="meta">
        <dt>Version</dt><dd>${esc(n.version)}</dd>
        <dt>Updated</dt><dd>${esc(n.updated)}</dd>
        <dt>Review after</dt><dd>${esc(n.review_after)}</dd>
        <dt>Record</dt><dd><code>${esc(n.path)}</code></dd>
        <dt>Sources</dt><dd>${sourcesList(n.sources)}</dd>
      </dl>
      <p><a href="catalogue.html#node=${encodeURIComponent(n.id)}">Open in catalogue</a></p>
      <h2>Context</h2>
      <div class="context">${KGV.renderContext(n.context)}</div>
      ${params}
      <h2>Outgoing (${out.length})</h2>${relList(out, "out")}
      <h2>Incoming (${inc.length})</h2>${relList(inc, "in")}`;
  }

  function renderEdge(e) {
    const review = e.review
      ? `<dt>Reviewed by</dt><dd>${esc(e.review.by)}</dd>
         <dt>Review date</dt><dd>${esc(e.review.date)}</dd>
         <dt>Basis</dt><dd>${esc(e.review.basis)}</dd>`
      : "<dt>Review</dt><dd>None recorded</dd>";
    const scope = e.scope ? `<dt>Scope</dt><dd>${esc(typeof e.scope === "string" ? e.scope : JSON.stringify(e.scope))}</dd>` : "";
    details.innerHTML = `
      <div class="tagline"><span class="mono">relationship</span> ${setPill(e.set)}</div>
      <h2 class="title mono">${esc(e.type)}</h2>
      <dl class="meta">
        <dt>Source</dt><dd>${nodeButton(e.source)}</dd>
        <dt>Target</dt><dd>${nodeButton(e.target)}</dd>
        <dt>Status</dt><dd>${esc(e.status)}</dd>
        ${review}
        ${scope}
        <dt>Sources</dt><dd>${sourcesList(e.sources)}</dd>
      </dl>
      ${e.set === "candidate" ? '<p class="hint">Candidate relationship: proposed, not validated knowledge. Consumers must gate it explicitly.</p>' : ""}`;
  }

  details.addEventListener("click", (ev) => {
    const nodeBtn = ev.target.closest("[data-node]");
    if (nodeBtn) return focusNode(nodeBtn.dataset.node);
    const edgeBtn = ev.target.closest("[data-edge]");
    if (edgeBtn && cy.getElementById(edgeBtn.dataset.edge).nonempty()) focusEdge(edgeBtn.dataset.edge);
  });

  cy.on("tap", "node", (ev) => focusNode(ev.target.id()));
  cy.on("tap", "edge", (ev) => focusEdge(ev.target.id()));
  cy.on("tap", (ev) => {
    if (ev.target === cy) clearFocus();
  });
  depthSelect.addEventListener("change", () => {
    const selected = cy.$("node:selected");
    if (selected.nonempty()) focusNode(selected.id());
  });

  // ---- Tooltip -------------------------------------------------------------
  const tooltip = document.getElementById("tooltip");
  cy.on("mouseover", "node, edge", (ev) => {
    const t = ev.target;
    if (t.isNode()) {
      const n = nodesById.get(t.id());
      tooltip.innerHTML = `<strong>${esc(n.title)}</strong><br><span class="muted">${esc(n.type)} · ${esc(n.id)} · ${degree.get(n.id) || 0} edges</span>`;
    } else {
      const e = edgesByKey.get(t.id());
      tooltip.innerHTML = `<span class="mono">${esc(e.source)}</span> <strong>${esc(e.type)}</strong> <span class="mono">${esc(e.target)}</span><br><span class="muted">${esc(e.set)}</span>`;
    }
    tooltip.hidden = false;
  });
  cy.on("mousemove", (ev) => {
    if (tooltip.hidden || !ev.originalEvent) return;
    const { clientX, clientY } = ev.originalEvent;
    const right = clientX + 14 + tooltip.offsetWidth > window.innerWidth;
    tooltip.style.left = `${right ? clientX - 14 - tooltip.offsetWidth : clientX + 14}px`;
    tooltip.style.top = `${clientY + 14}px`;
  });
  cy.on("mouseout", "node, edge", () => {
    tooltip.hidden = true;
  });

  // ---- Search and controls -------------------------------------------------
  const search = document.getElementById("search");
  const searchResult = document.getElementById("search-result");
  function matches() {
    const q = search.value.trim().toLowerCase();
    if (!q) return [];
    return graph.nodes
      .filter((n) => n.id.toLowerCase().includes(q) || n.title.toLowerCase().includes(q))
      .map((n) => n.id);
  }
  search.addEventListener("input", () => {
    const ids = new Set(matches());
    cy.nodes().forEach((n) => n.toggleClass("match", ids.has(n.id())));
    searchResult.textContent = search.value.trim() ? `${ids.size} match${ids.size === 1 ? "" : "es"}` : "";
  });
  search.addEventListener("keydown", (ev) => {
    if (ev.key !== "Enter") return;
    const first = matches()[0];
    if (first) focusNode(first);
  });

  document.getElementById("relayout").addEventListener("click", runLayout);
  document.getElementById("layout").addEventListener("change", runLayout);
  document.getElementById("fit").addEventListener("click", () => cy.fit(cy.elements().not(".hidden"), 40));
  document.getElementById("edge-labels").addEventListener("change", (ev) => {
    cy.edges().toggleClass("labelled", ev.target.checked);
  });

  if (dangling.length) {
    searchResult.textContent = `${dangling.length} relationship(s) reference unknown concepts and are not drawn.`;
  }

  runLayout();
  const start = KGV.readHash().node;
  if (start && nodesById.has(start)) focusNode(start, false);
})();
