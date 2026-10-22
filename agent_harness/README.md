# Role-based, round-bound harnesses

This directory is the **proposed standing harness** for Forest Cover Lab. `roles/` stores reusable task contracts, `templates/` seeds new rounds, `schemas/` validates their manifests, and `examples/` illustrates *planned* (not executed) investigations. It is deliberately host-agnostic.

For discovery, URL maintenance and pipeline-design questions select `roles/dataset-and-tool-discovery.md` with `../research/data_sources/discovery_and_link_verification.md`. Treat `eudr-dmi-gil` auto-catalogue rows as external unverified seeds, not Lab source IDs or authorized writes. Keep data-source and software-tool assessments in their distinct research tracks. Actual provider checks and answers are captured in the round, not inferred from role selection.

Select only the needed roles. Give each one a task-specific assignment and source boundary. Record actual host, loaded files, permissions and resulting evidence in the round; do not infer execution from a planned assignment. When used with a downstream Sentinel review, the actual round should be created under that review and refer to Lab role definitions by pinned Lab revision.

**Quick path:** copy `templates/round.yaml` and `templates/assignment.md`; replace placeholders; validate round YAML with `python agent_harness/scripts/validate_round.py <path-to-round.yaml>`; as work proceeds append `actual_executions` with observed configuration, source hashes and artifact checksums. Promote nothing automatically.

Existing Sentinel `.codex/skills/` files are relevant components of a Codex harness and can be referenced by revision/digest in `harness_sources` and `actual_executions[].loaded_harness`. A plain role contract is not a machine-executable tool declaration; adapters are optional and must be recorded if used.

**Agent graph (optional, ADR 0007):** add a `graph` block to `round.yaml` to state which agents exist, what each edge carries, where human gates sit, each agent's loop bound, independence groups, and whether the chain runs `stepwise` (each step plan approved first) or `auto` (up to the next gate). The graph itself carries an approval and a `planning_record_id`. Draw and check it with `python agent_harness/scripts/render_round_graph.py <round.yaml>` (writes `graph.svg` and `graph.mmd` beside the manifest; refuses invalid manifests; `--check` for staleness). See the [road-widening example](examples/road-widening/round-0001/graph.svg). Drawing a graph runs nothing; there is no runner yet.

See [record validation and path rules](../docs/agents.md) and ADR 0006. `role` resolves
against Lab unless `role_scope: round_only` selects a round-local file. Assignments
always resolve against the manifest directory. Paths must remain within those roots.
A completed attempt records nonempty outputs and checks, and `output_hashes` maps every
output reference to its SHA-256. Source/evidence references point to the existing hashed
ledgers; record exact commands, input versions and disagreements there. Both repositories
need full commit pins for any executed round; `lab_graph_revision` is its SHA-256 revision.
Loaded repository files require commit pins and digests; private external instructions may
be `not_captured` with an explicit reproducibility limitation. A captured external copy
needs a digest too. `selected` is planning-only.

Validate all local examples and inquiry records (no sibling checkout needed):

```sh
python agent_harness/scripts/validate_round.py --root .
```

For downstream reviews use the same script with `--root /path/to/sentinel` or pass
individual manifest paths. Lab role paths resolve against the Lab containing the script;
`--lab` can select another explicitly checked-out revision. No automatic download occurs.
The CLI checks record structure and local role/assignment existence; it does not verify
repository object availability, recompute every evidence digest, prove actual model loads,
or enforce append-only history. Review the pinned content and evidence independently.
Existing reviews without round manifests are not retroactively assigned executions.
