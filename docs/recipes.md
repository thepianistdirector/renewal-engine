# Shipped recipe author contract

Read `renewal_engine/recipes.py` and `recipe_data/pathlib.json` for the complete
schema and minimal independently useful example. Run `python3 -m renewal_engine
conformance` to check declared positive/refusal fixtures, exact output hashes and
idempotence. It does not execute user source or prove runtime equivalence.

A contract uses schema 1, a stable unique ID, semantic version, engine schema,
nonempty old/target half-open version intervals, explicit preconditions, effect
coverage, comparison-policy owner, ordered recipe dependencies, limitations and
hash-pinned positive/refusal examples. Extra fields, incompatible schemas, missing
policy ownership, empty intervals and changed fixture bytes are refused. The
registry returns fresh copies so callers cannot mutate another run's policy.

Declare safe bindings narrowly. Preserve all bytes outside exact edits. Reject
unknown dynamic binding, import shadowing and source digest/span mismatches. Do
not let the transformation approve its own expected behavioral differences. Add a
separately authored wrong transform that the actual runtime observer rejects.
Retain both failures and passes, interpreter identities, policy hashes, provenance,
source/candidate hashes and a reproduction command with actual prerequisites.

The current registry deliberately admits only the two shipped reviewed handlers.
Updating their metadata/fixtures does not require core changes; adding an entirely
new executable discovery handler requires source review and registry dispatch
changes. There is no dynamic plugin loader or claim that an unreviewed third-party
recipe can run. A schema change must receive a new explicit reader; unknown saved
schemas are refused. Existing 0.1 evidence uses its original interpretation and
unchanged comparator, and is included in compatibility checks.

Before contributing: supply the exact patch, positive/refusal/conformance tests,
actual baseline/candidate observations, independent negative control, legal origin,
changed limitations, and known unsupported cases. A second human contributor's
authoring experience has not yet been observed; N13-07 and N13-08 remain pending.
