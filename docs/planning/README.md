# Canonical planning protocol

`project-plan.json` is the sole editable outcome/status ledger. `ROADMAP.md`, `TASKS.md`, `task-contracts.json`, `docs/planning/source-mapping.md`, and `docs/publication/tanduna-plan-export.json` are deterministic generated views. Do not change a generated status independently.

The plan contains 218 distinct outcomes in 26 waves: 50 for the narrow 0.1, 72 for later 0.x, 80 long-term and 16 exploratory. The count expresses scope coverage, not a commitment to implement the full backlog for 0.1. Language expansion and optional model assistance are exploratory admission decisions. The other later scopes remain proposals derived from retained requirements and the owner's outcome families.

From the repository root, using the already available Python interpreter:

```sh
python3 tools/plan.py validate
python3 tools/plan.py self-test
python3 tools/plan.py generate
python3 tools/plan.py check
```

The tool uses the standard library and does not install dependencies, execute product code, call a platform API, or mutate the frozen lineage. `validate` checks graph integrity, explicit prerequisite outcome coverage, scope/order consistency, one-wave ownership, source/decision references, 12 source mappings, criterion coverage, original IDs/revisions/content hashes, exact original acceptance/dependency records, lineage file digests and truthful evidence-bearing statuses. `self-test` rejects 20 meaningful malformed-plan mutations without modifying the canonical input. `check` additionally rejects stale generated files. These checks validate the plan; none proves product behavior or human acceptance.

Semantic overlap still needs reviewer judgment. For example, the 0.1 trusted fixture runner is narrower than future enforced arbitrary-code isolation; the first static report is narrower than later varied-user accessibility research; original preservation is narrower than data restoration. These are deliberate scope distinctions, not duplicated completion claims. Mechanical uniqueness checks cannot prove that every proposed outcome is useful.

The new 0.1 critical path is recorded under `criticalPath`, independently of `sourceMappings`' preserved historical graph. It progresses through exact cut/rights/runtime decisions, original observations, conservative transformation, independent differential evidence and public user/release/publication evidence. Each wave exit consumes all its peer outcomes. No later general recipe kit, data migration or pilot programme is implicitly complete because the narrow CLI can run.

When an execution packet begins, assign its exact project-owned paths, runnable commands, falsifiers and evidence location in the owner's execution records, then update only the relevant canonical task. New rows begin `PLANNED`. Use `IN PROGRESS`, `IMPLEMENTED`, `AUTOMATED PASS`, `RUNTIME VERIFIED`, `USER VALIDATED`, `RELEASE VERIFIED`, `BLOCKED`, `FAILED` and `NOT TESTED` with retained evidence. An evidence-bearing task needs an evidence record; include the observed scope, command or protocol, actual result, path/digest and relevant environment. A status does not imply the other evidence levels. Keep required human observations pending until a real participant or qualified reviewer supplies them.

Frozen source mappings retain the original full briefs and repository contracts, all 12 identities, each revision 3, publication snapshot hash, original planning base, briefing HEAD, structured native and repository prerequisites, textual prerequisites and textual-only differences. Null predecessor revision means none was stated; it does not invent earlier history. Source requirements remain intact even where the original-fixture 0.1 proposal narrows the chosen implementation. Current Astra-only execution does not alter historical model fields in immutable records.
