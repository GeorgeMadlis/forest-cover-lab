# Reverse Engineering Template

Copy this file to `analysis/<repo_name>/reverse_engineering.md` and fill each section.

The goal is to surface the scientific reasoning embedded in implementation choices — not to
document what the code does operationally. A reader who has already read the paper should
learn something new from this artifact.

---

## Metadata

| Field | Value |
|---|---|
| Repository | |
| URL | |
| Commit analyzed | |
| Inventory entry | (CS-XXXX in `inventory.csv`) |
| Linked publication | (DOI or "none") |
| Analyst | |
| Date | |
| Time spent | |

---

## 1. Forest definition assumptions

What operational definition of "forest", "forest cover", or "forest disturbance" does this
code encode? Look for:

- Threshold values (canopy cover %, NDVI, backscatter cutoffs)
- Spatial constraints (minimum mapping unit, contiguity requirements)
- Temporal constraints (persistence windows, lookback periods for change detection)
- Hardcoded exclusions (water bodies, urban areas, permanent agriculture)
- Nodata handling that silently affects the forest area estimate

*Write what you found. Quote specific variable names and line numbers where threshold values
appear, so the reader can verify.*

---

## 2. Algorithmic scientific judgments

What choices in the algorithm encode scientific judgments rather than engineering preferences?
Look for:

- Band combinations and their spectral justification (why those bands?)
- Auxiliary or context products used by the algorithm (biodiversity, water, fire, climate,
  integrity indices, land pressure) and why they are scientifically justified
- Compositing strategies (median vs. percentile vs. harmonic fitting) and their temporal
  assumptions (what does a median over a wet season represent?)
- Change detection thresholds and their sensitivity rationale
- Loss function choices and their implied label distribution assumptions
- Post-processing steps that encode ecological assumptions (minimum patch size, boundary
  smoothing)

*Write what you found. Distinguish judgments that are documented in the paper from those
embedded silently in the code.*

---

## 3. Label semantics embedded in training

*(Complete this section only if the codebase includes a machine learning training component.)*

- What labels are used for training? Are they annual, seasonal, monthly, or event-based?
- Does the code treat annual labels as if they were monthly ground truth? If yes, document
  this as a critical assumption and flag it.
- How does the code handle label noise? (Soft labels, label smoothing, loss masking?)
- Is the temporal alignment between the label and the input features verified in code, or
  assumed?

*Write what you found.*

---

## 4. Limitations hidden in implementation details

What limitations does the code impose that would not be apparent from reading the paper or
README? Look for:

- Hardcoded geographic or sensor constraints (latitude bounds, specific GEE asset IDs,
  fixed projection assumptions)
- Hidden context-product assumptions (e.g. flood masks, water masks, fire layers, integrity
  indices, or protected-area layers treated as universally valid)
- Silent failure modes (how are nodata pixels handled? what happens at tile edges?)
- Assumptions that hold in the paper's study region but may not generalize (phenology,
  cloud regimes, canopy structure)
- Dependencies on specific dataset versions that may not be updated (hardcoded GEE asset
  paths, fixed download URLs)
- Platform-specific behavior that is not portable (GEE scale, projection, resampling
  defaults)

*Write what you found.*

---

## 5. Paper-to-code divergences

Where does the implementation differ from the paper that describes it? Look for:

- Thresholds that differ from values reported in the paper
- Steps described in the paper that are absent from the code (or vice versa)
- Evaluation metrics computed differently from how the paper defines them
- Edge cases handled differently from the paper's stated methodology

*Write what you found. Indicate whether each divergence is minor (implementation detail)
or substantive (affects results or reproducibility).*

---

## 6. Adaptation assessment

What would be required to adapt this codebase for Forest Cover Lab?

**Compatibility checklist:**

- [ ] Forest definition is compatible with or can be parameterized to match our `configs/`
- [ ] Sensor inputs overlap with our planned data sources (see `research/data_sources/`)
- [ ] Execution platform (GEE, PyTorch, GDAL, etc.) fits our stack (see ADR 0001)
- [ ] License permits adaptation and redistribution

**Estimated adaptation effort:** low / medium / high

*Justify the effort estimate with specific blockers or gaps identified above.*

**Recommended action:** adapt / reference / reject

*State the recommended action and one sentence justifying it.*
