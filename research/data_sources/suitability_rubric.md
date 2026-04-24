# Data Source Suitability Rubric

Each data source is assessed for phase-by-phase suitability against the v1, v2, and v3
roadmap goals. Use the levels below in `inventory.csv`.

Suitability is not the same as relevance. A context product can be highly relevant to
interpretation while still being `not_applicable` as a direct v1/v2 forest-cover input.

---

## Suitability levels

| Level | Meaning |
|---|---|
| `high` | Directly supports the phase goal without significant preprocessing or access friction |
| `medium` | Usable with non-trivial effort (mosaicking, fusion, access setup) or with known limitations |
| `low` | Possible but requires significant workarounds; prefer alternatives if available |
| `not_applicable` | Not relevant to this phase |

Suitability is a judgment about the combination of spatial resolution, temporal resolution,
geographic coverage, access method, and license — not any single attribute.

---

## Evidence role rules

Use these values in `inventory.csv`.

| Value | Use when |
|---|---|
| `core estimation input` | The source directly supports a forest-cover or disturbance estimate |
| `auxiliary feature` | The source may improve a model but cannot define forest cover by itself |
| `validation reference` | The source is independent enough to compare against outputs |
| `context/risk layer` | The source explains pressures, anomalies, uncertainty, or interpretation |
| `exclusion mask` | The source masks areas such as permanent water, urban areas, or clouds |
| `interpretation-only background` | The source belongs in reports or notes, not algorithmic processing |

## Domain rules

Use short, stable `domain` values such as:

- `forest cover`
- `forest disturbance`
- `forest structure`
- `vegetation condition`
- `biodiversity`
- `ocean/coastal`
- `energy`
- `environmental integrity`
- `floods and water`
- `fire`
- `climate`
- `land use pressure`

---

## Phase-specific criteria

### v1 — Evidence-first forest baseline

A source is **high** for v1 if it:
- Provides a direct forest cover, tree cover, or forest-change product
- Spatial resolution ≤ 30 m
- Covers the target geography globally or at continental scale
- Available via GEE, direct download, or stable API with open license
- Annual or coarser temporal resolution is sufficient (monthly not required)

A source is **low** for v1 if it:
- Requires cloud-based compositing before a forest classification can be made
- Is coarser than 250 m
- Has restricted or commercial license without clear access route

Context products are usually `not_applicable` for v1 unless they are used as exclusion
masks or independent plausibility checks.

### v2 — Monthly confirmation from time series

A source is **high** for v2 if it:
- Provides data at monthly or finer native temporal resolution, or enables monthly compositing
- Covers Sentinel-1 or Sentinel-2 spectral bands or equivalent SAR/optical time series
- Enables cloud-robust monthly compositing strategies (e.g. SAR always-on, optical SCL)
- Accessible via GEE, Sentinel Hub, or a stable tile server with open license
- ≤ 30 m resolution preferred; 10 m strongly preferred

A source is **low** for v2 if it:
- Is annual only with no sub-annual structure
- Has cloud contamination with no available cloud mask
- Has revisit cycle longer than 30 days

Flood, surface-water, fire, and weather products may be `medium` for v2 as context if they
explain monthly anomalies, even when they are not forest-cover inputs.

### v3 — Weakly supervised monthly estimation

A source is **high** for v3 if it:
- Can serve as a supervisory signal or pseudo-label for monthly or seasonal forest state
- Has documented label semantics: what time period, what annotation method, what geographic
  scope, how noisy
- Compatible with a weakly supervised or semi-supervised training setup
- Enables external triangulation against independent sources for uncertainty assessment

A source is **medium** for v3 if it:
- Provides useful auxiliary features but cannot serve as a supervisory signal alone
- Has documented label semantics but with known biases that must be flagged

A source is **low** for v3 if it:
- Is annual without any temporal disaggregation potential
- Has undocumented label semantics
- Has geographic restrictions that prevent generalizable training

Adjacent context products can be `medium` for v3 if they support uncertainty modeling,
stratified validation, transferability analysis, or external triangulation. They should not
be treated as labels unless their target semantics match the forest variable.

---

## Forest relevance classification

The `forest_relevance` field should answer one question: why does this source matter for
forest cover estimation?

Good examples:

- "Direct forest cover and annual loss baseline; weak supervision only for monthly tasks."
- "Flood or inundation context can explain optical/SAR anomalies and uncertainty."
- "Integrity index supports landscape context; verify components to avoid circular evidence."

Bad examples:

- "Interesting dataset."
- "May be useful later."
- "General environmental information."

## Source priority

Use `source_priority` to distinguish actionability from curiosity.

| Value | Meaning |
|---|---|
| `high` | Candidate for near-term specs, validation, or processing |
| `medium` | Worth reviewing and may influence ADRs or reports |
| `candidate` | Needs review before any recommendation |
| `watch` | Track only for relevant AOIs or later phases |
| `reject` | Keep only as a record of why it should not be used |

---

## Access method classification

Use consistent values in the `access_method` column:

| Value | Meaning |
|---|---|
| `GEE asset` | Available directly in Google Earth Engine |
| `GEE + download` | Available in GEE and as direct download |
| `direct download` | Tile or file download from agency or cloud storage |
| `API` | Requires authenticated API (e.g. Sentinel Hub, NASA CMR) |
| `restricted` | Requires registration, data agreement, or institutional access |
| `commercial` | Requires commercial license or paid subscription |

---

## License classification

Use consistent values in the `license` column:

| Value | Meaning |
|---|---|
| `open (public domain)` | No restrictions (e.g. US Government data) |
| `open (Creative Commons)` | CC BY or CC BY 4.0 |
| `open (Copernicus open access)` | Copernicus programme free and open access policy |
| `open (other)` | Open but document the specific license |
| `restricted (registration)` | Free after registration or data agreement |
| `commercial` | Paid license required |
| `unclear` | License not documented — flag before use |
