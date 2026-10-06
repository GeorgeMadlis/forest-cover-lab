# Contextual knowledge corpus

Forest Cover Lab remains focused on forest-cover estimation. This corpus follows practical
[Open Knowledge Format principles](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/README.md):
portable Markdown with YAML front matter, provenance, freshness and contextual prose.
This is a repository-specific OKF-oriented profile, not a claim of full OKF v0.2 conformance.
The enforced fields are defined by `graph/schemas/concept.schema.json`.

| Concept | Meaning | Directory |
|---|---|---|
| Application | Intended monitoring or screening use | applications |
| Scientific question | Question the evidence must answer | questions |
| Method | Scientific procedure independent of backend | methods |
| Observation requirement | Evidence needed; substitutable dataset families may satisfy it | observations |
| Measurement | Variable/index/class and its temporal interpretation | measurements |
| Dataset | Registered product family, never individual scenes | datasets |
| Access | Mechanism for resolving actual observations | access |
| Capability | Reusable software operation, not scientific validity | capabilities |
| Tool | Software exposing capabilities | tools |
| Executable workflow | Versioned downstream implementation, possibly partial | workflows |
| Validation | Required evidence checks | validation |
| Claim | Bounded interpretation/non-claim | claims |

IDs use typed prefixes (e.g. `method:ndvi-anomaly`) except existing dataset IDs (`DS-0002`).
Never recycle an identifier for a different scientific meaning. Concepts have a version,
lifecycle status, update date, review-after date, sources, relations and explanatory body.
Sources are repo-relative files or primary documentation URLs. External sources are reviewed
manually; the offline generator checks their syntax but does not fetch them. Existing dataset
assessments remain in the inventory; titles must match and inventory IDs must resolve.

Relations have type, target, candidate/validated status, evidence and (when validated) an
explicit review basis. The initial validated relations are transcriptions of repository
contracts or documented APIs, reviewed as transcriptions by this change. They do not claim
empirical validation, scientific performance or human scientific sign-off. New seasonal
methods, NDVI anomaly decisions, annual loss comparison extensions and downstream implementation
mappings stay candidates until review. See `governance/knowledge_promotion.md`.

`review_after` is a review deadline, not automatic rejection or proof of freshness. Consumers
must check deadlines against their planning date and pin a snapshot; an offline build does
not change authoritative records on the basis of wall-clock time. New versions and deprecated
concepts require explicit updates and relationship review.

Navigation starts with applications, then questions/methods and observations, then measurements,
datasets/access and capabilities. `graph/generated/knowledge.json` indexes all concepts with
context and source paths. Use only `relationships` for authoritative discovery; display
`candidate_relationships` separately. Neither stream includes a complete EO archive.
