# Practitioner Sources

Practitioner sources supplement peer-reviewed literature with implementation knowledge,
dataset announcements, and operational insights. They are valid research inputs but must
be classified as `venue_type = blog` or `venue_type = technical_report` in inventories —
never as journal papers.

Monitor these sources when conducting literature research or data source surveys.

---

## Google Earth Engine

**Google Earth Engine Developer Blog**
- URL: https://medium.com/google-earth
- Covers: new datasets hosted on GEE, API changes, example workflows, quota policy updates
- Priority: **high** — GEE is the v1 default platform
- Note: monitor for quota policy changes affecting ADR 0001

---

## Sentinel / Copernicus

**Sentinel Hub Blog**
- URL: https://www.sentinel-hub.com/blog/
- Covers: Sentinel-1 and Sentinel-2 processing, custom scripts, cloud masking, use cases

**ESA Copernicus / EO Science**
- URL: https://www.esa.int/ESA_Multimedia/Missions/Copernicus
- Covers: Copernicus programme updates, new products, policy

---

## Forest monitoring agencies

**Global Forest Watch Blog** (World Resources Institute)
- URL: https://www.globalforestwatch.org/blog/
- Covers: forest monitoring updates, new products, deforestation alerts, policy context

**GLAD Lab / Hansen group** (University of Maryland)
- URL: https://glad.umd.edu/
- Covers: GFC dataset updates (annual versions), GLAD alerts methodology, landsat-based products

**INPE PRODES / TerraBrasilis**
- URL: https://terrabrasilis.dpi.inpe.br/
- Covers: Brazil deforestation monitoring methodology, PRODES annual releases

---

## Remote sensing research groups

**JRC Forest Resources** (European Commission)
- URL: https://forest.jrc.ec.europa.eu/
- Covers: Tropical Moist Forest (TMF) product updates, Global Forest Cover methodology

**ESA EO Science for Society**
- URL: https://eo4society.esa.int/
- Covers: research outcomes, dataset releases, method benchmarks

---

## Conference and workshop proceedings (practitioner track)

- **IGARSS tutorials and demo sessions** — often contain implementation details not in papers
- **ESA Living Planet workshops** — methodology notes for Copernicus-based products
- **EGU conference abstracts** — early-stage method proposals in forest EO

---

## Rules for using these sources

- Record any blog post consulted in `research/publications/publications_inventory.csv`
  with `venue_type = blog`.
- Extract any data source mentioned and verify it against `research/data_sources/inventory.csv`.
- Extract any code link and verify it against `research/code_sources/inventory.csv`.
- Do not cite a blog post as the primary justification for an ADR; back it with a
  peer-reviewed reference or technical report where possible.
