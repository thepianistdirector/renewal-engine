# Bounded execution packets

Root task 01a07e1c-3ed5-7f90-9b4d-f5c4977ad123 owns integration. All work is
scoped to this repository. Historical frozen Tanduna revisions remain intact.
Status is held in project-plan.json; this file describes execution, not a second
status ledger. Proposed command names become documented user commands only
after the corresponding packet implements and runs them.

1. Planning agent: project-plan.json, task-contracts.json, ROADMAP.md, TASKS.md,
   tools/plan.py, docs/planning and docs/publication. Validate all task fields,
   lineage mappings, dependency cycles, release scopes and generated views.
   Falsifier: a cycle or dangling predecessor must fail validation.
2. Root: renewal_engine/discovery.py, transformation.py and tests/test_recipe.py.
   Source-span changes and selected-tree inspection only. Falsifiers: shadowed
   import, receiver reassignment, star argument, comment/string near readfp,
   multibyte offsets and second application. No reference fixture execution.
3. Root after fixture/runtime decision: trusted fixture, characterization,
   execution, comparison and related tests. Falsifiers: wrong source name,
   dropped error attribute, unexpected warning, runtime mismatch, timeout,
   mutated fixture hash. Preserve failed attempts. Actual old runtime required.
4. Root: CLI, artifact stages, accessible HTML and packaging. Falsifiers: existing
   destination, interrupted generation/comparison, original-byte mutation,
   changed source/recipe hash, evidence reopening and escaped HTML input.
5. Independent Astra critic: stable code and evidence, read-only. Fixed rubric:
   rewrite safety, comparator independence, truthful claims, recovery/integrity,
   package usability and report accessibility. Findings require reproduction;
   critic opinion cannot replace functional or human validation.
6. Root: integrate evidence and prepare concrete GitHub/Tanduna publication
   materials. Public writes wait for exact applicable authorization. External
   and human checks stay pending until actually supplied.
