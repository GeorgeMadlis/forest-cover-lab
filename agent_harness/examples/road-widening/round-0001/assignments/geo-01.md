# Subagent assignment: geo-01

**Example only — planned, never executed.**

- **Role contract:** `agent_harness/roles/national-geospatial-evidence.md` from pinned Forest Cover Lab commit at execution
- **Planned host:** `claude-code`; actual host, model, available tools and loaded files must be recorded after execution
- **Falsifiable task:** Assess whether the apparent road or corridor pre-existed and whether its visible width changed.
- **Inputs / permitted source scope:** Historic geoportal orthophotos with acquisition dates; documented topographic roads and national geo-services; verify source lineage.
- **Required outputs:** Before/after georeferenced comparators and acquisition-linked width uncertainty.
- **Required reading:** Forest Cover Lab `AGENTS.md`, `docs/agents.md`, role contract, this assignment; downstream `AGENTS.md` and applicable review/Sentinel skills only if explicitly used
- **Access limits:** read-only source discovery by default; no unauthorized downloads or edits outside assigned review; operator approval for scope expansion
- **Evidence contract:** URLs/provider receipt, original/acquisition dates, UTC access time, license, lineage group, checksums when downloaded; no manufactured source IDs
- **Checks:** independent original-source verification, geometry/units checks where relevant, explicit alternative hypotheses and missing evidence; cite executed commands/tests precisely
- **Failure/escalation:** unavailable or undated decisive source, insufficient spatial resolution, ambiguous attribution, irreproducible calculations or conflicting denominators -> record `indeterminate` and ask for next evidence
- **Handoff:** record claim IDs, uncertainty, supports/contradicts/inconclusive and exact artifact references; no automatic promotion
