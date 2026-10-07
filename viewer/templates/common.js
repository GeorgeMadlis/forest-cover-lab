// Shared vocabulary for the viewer pages: layers, shapes, theme and header.
(function () {
  "use strict";

  const bundle = window.KG_BUNDLE;

  // Colour encodes the conceptual layer (four reference-palette slots in fixed
  // order); shape encodes the concept type. Types added to the ontology later
  // fall into "other" with a circle until they are given a place here.
  const LAYERS = [
    { key: "purpose", label: "Purpose & assurance", slot: "--layer-1",
      types: ["application", "question", "claim", "validation"] },
    { key: "science", label: "Science", slot: "--layer-2",
      types: ["method", "observation", "measurement"] },
    { key: "data", label: "Data", slot: "--layer-3", types: ["dataset", "access"] },
    { key: "implementation", label: "Implementation", slot: "--layer-4",
      types: ["workflow", "tool", "capability"] },
  ];
  const OTHER = { key: "other", label: "Other", slot: "--layer-other", types: [] };

  function regular(n, rotation) {
    const pts = [];
    for (let i = 0; i < n; i++) {
      const a = rotation + (2 * Math.PI * i) / n;
      pts.push(Math.cos(a), Math.sin(a));
    }
    return pts;
  }
  function star() {
    const pts = [];
    for (let i = 0; i < 10; i++) {
      const a = -Math.PI / 2 + (Math.PI * i) / 5;
      const r = i % 2 ? 0.45 : 1;
      pts.push(r * Math.cos(a), r * Math.sin(a));
    }
    return pts;
  }
  // Points are in [-1, 1] with y pointing down, shared by Cytoscape and the SVG icons.
  const SHAPES = {
    application: { polygon: star() },
    question: { polygon: [0, -1, 1, 0, 0, 1, -1, 0] },
    claim: { polygon: [-1, -0.8, 0.45, -0.8, 1, 0, 0.45, 0.8, -1, 0.8] },
    validation: { polygon: regular(8, Math.PI / 8) },
    method: { polygon: regular(6, 0) },
    observation: { ellipse: true },
    measurement: { polygon: [0, -1, 1, 0.85, -1, 0.85] },
    dataset: { polygon: [-0.9, -0.9, 0.9, -0.9, 0.9, 0.9, -0.9, 0.9] },
    access: { polygon: [-1, -0.9, 0, -0.2, 1, -0.9, 0, 1] },
    workflow: { polygon: regular(5, -Math.PI / 2) },
    tool: { roundRect: true },
    capability: { polygon: [-0.5, -0.8, 1, -0.8, 0.5, 0.8, -1, 0.8] },
  };
  const FALLBACK_SHAPE = { ellipse: true };

  const layerOfType = new Map();
  LAYERS.forEach((layer) => layer.types.forEach((t) => layerOfType.set(t, layer)));

  function layerFor(type) {
    return layerOfType.get(type) || OTHER;
  }
  function shapeFor(type) {
    return SHAPES[type] || FALLBACK_SHAPE;
  }
  function round(v) {
    return Math.round(v * 1000) / 1000;
  }

  function shapeIcon(type, size) {
    size = size || 14;
    const shape = shapeFor(type);
    const fill = `var(${layerFor(type).slot})`;
    const s = size / 2;
    let body;
    if (shape.ellipse) {
      body = `<circle cx="${s}" cy="${s}" r="${s - 1}" fill="${fill}"/>`;
    } else if (shape.roundRect) {
      body = `<rect x="1" y="2" width="${size - 2}" height="${size - 4}" rx="3" fill="${fill}"/>`;
    } else {
      const pts = [];
      for (let i = 0; i < shape.polygon.length; i += 2) {
        pts.push(`${round(s + shape.polygon[i] * (s - 1))},${round(s + shape.polygon[i + 1] * (s - 1))}`);
      }
      body = `<polygon points="${pts.join(" ")}" fill="${fill}"/>`;
    }
    return `<svg class="icon" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" aria-hidden="true">${body}</svg>`;
  }

  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  // Minimal rendering of corpus Markdown context: headings, paragraphs, inline code.
  function renderContext(text) {
    const inline = (s) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>");
    return String(text || "")
      .split(/\n\s*\n/)
      .map((block) => block.trim())
      .filter(Boolean)
      .map((block) => {
        const heading = block.match(/^#{1,6}\s+(.*)$/);
        if (heading && !block.includes("\n")) return `<h4>${inline(heading[1])}</h4>`;
        return `<p>${inline(block).replace(/\n/g, "<br>")}</p>`;
      })
      .join("");
  }

  function shortLabel(node) {
    const prefix = `${node.type}:`;
    return node.id.startsWith(prefix) ? node.id.slice(prefix.length) : node.id;
  }

  // Theme: explicit choice persists per viewer; otherwise follow the OS.
  const THEME_KEY = "kg-viewer-theme";
  const themeListeners = [];
  function storedTheme() {
    try {
      return localStorage.getItem(THEME_KEY);
    } catch (e) {
      return null;
    }
  }
  function effectiveTheme() {
    const explicit = document.documentElement.getAttribute("data-theme");
    if (explicit) return explicit;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try {
      localStorage.setItem(THEME_KEY, theme);
    } catch (e) {
      /* storage unavailable: theme lasts for this page view only */
    }
    themeListeners.forEach((fn) => fn());
  }
  function onThemeChange(fn) {
    themeListeners.push(fn);
  }
  const saved = storedTheme();
  if (saved === "light" || saved === "dark") {
    document.documentElement.setAttribute("data-theme", saved);
  }
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", () => themeListeners.forEach((fn) => fn()));

  function readHash() {
    const params = new URLSearchParams(location.hash.slice(1));
    return Object.fromEntries(params.entries());
  }
  function writeHash(values) {
    const params = new URLSearchParams();
    Object.entries(values).forEach(([k, v]) => v && params.set(k, v));
    const hash = params.toString();
    try {
      history.replaceState(null, "", hash ? `#${hash}` : location.pathname);
    } catch (e) {
      location.hash = hash;
    }
  }

  function renderHeader(active) {
    const meta = bundle.meta;
    const commit = meta.forest_cover_lab_revision
      ? `${meta.forest_cover_lab_revision.slice(0, 7)}${meta.forest_cover_lab_dirty ? " (dirty)" : ""}`
      : "unknown";
    const header = document.createElement("header");
    header.className = "topbar";
    header.innerHTML = `
      <h1>Forest Cover Lab knowledge graph</h1>
      <nav aria-label="Pages">
        <a href="index.html" ${active === "graph" ? 'aria-current="page"' : ""}>Graph</a>
        <a href="catalogue.html" ${active === "catalogue" ? 'aria-current="page"' : ""}>Catalogue</a>
      </nav>
      <span class="snapshot" title="Graph revision ${esc(meta.graph_revision)}">
        Revision <code>${esc(meta.graph_revision.slice(0, 12))}</code> ·
        Lab commit <code>${esc(commit)}</code> ·
        ${meta.node_count} concepts · ${meta.relationship_count} validated ·
        ${meta.candidate_relationship_count} candidate
      </span>
      <button type="button" id="theme-toggle" aria-label="Toggle colour theme"></button>`;
    document.body.prepend(header);
    if (!meta.fresh) {
      const banner = document.createElement("div");
      banner.className = "banner";
      banner.setAttribute("role", "status");
      banner.textContent =
        "Stale snapshot: this graph differed from the knowledge corpus when it was " +
        "exported. Regenerate with graph/build.py before relying on it.";
      header.after(banner);
    }
    const toggle = header.querySelector("#theme-toggle");
    const label = () => {
      toggle.textContent = effectiveTheme() === "dark" ? "Light theme" : "Dark theme";
    };
    toggle.addEventListener("click", () => {
      setTheme(effectiveTheme() === "dark" ? "light" : "dark");
    });
    onThemeChange(label);
    label();
  }

  function allEdges() {
    const graph = bundle.graph;
    return [
      ...graph.relationships.map((r, i) => ({ ...r, key: `v${i}`, set: "validated" })),
      ...graph.candidate_relationships.map((r, i) => ({ ...r, key: `c${i}`, set: "candidate" })),
    ];
  }

  window.KGV = {
    bundle, LAYERS, OTHER, layerFor, shapeFor, shapeIcon, cssVar, esc, renderContext,
    shortLabel, onThemeChange, readHash, writeHash, renderHeader, allEdges,
  };
})();
