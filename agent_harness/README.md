# Role-based, round-bound harnesses

This directory is the **proposed standing harness** for Forest Cover Lab. `roles/` stores reusable task contracts, `templates/` seeds new rounds, `schemas/` validates their manifests, and `examples/` illustrates *planned* (not executed) investigations. It is deliberately host-agnostic.

Select only the needed roles. Give each one a task-specific assignment and source boundary. Record actual host, loaded files, permissions and resulting evidence in the round; do not infer execution from a planned assignment. When used with a downstream Sentinel review, the actual round should be created under that review and refer to Lab role definitions by pinned Lab revision.

**Quick path:** copy `templates/round.yaml` and `templates/assignment.md`; replace placeholders; validate round YAML with `python agent_harness/scripts/validate_round.py <path-to-round.yaml>`; as work proceeds append `actual_executions` with observed configuration, source hashes and artifact checksums. Promote nothing automatically.

Existing Sentinel `.codex/skills/` files are relevant components of a Codex harness and can be referenced by revision/digest in `harness_sources` and `actual_executions[].loaded_harness`. A plain role contract is not a machine-executable tool declaration; adapters are optional and must be recorded if used.

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
