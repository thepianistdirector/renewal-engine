# Renewal Engine: proposed work packages

These are planning briefs. No task is complete or approved for automatic execution. Before implementation, maintainers must publish a scoped task revision with the actual repository, paths, tools and validation commands.

## W1-T1 — Select and document the reference migration

**Wave:** W1 · **Status:** Planned · **Prerequisites:** None; begin with maintainer scope review

Pick a maintained open-source fixture and a bounded dependency or framework change.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- Record licensing, source revisions, supported runtime and the specific migration objective.
- List behavior that must remain stable and areas that are intentionally out of scope.

## W1-T2 — Capture characterization fixtures

**Wave:** W1 · **Status:** Planned · **Prerequisites:** W1-T1

Record representative inputs, outputs, side effects and important error behavior.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- Fixtures run against the original application and fail for a deliberate behavioral regression.
- Sensitive or nondeterministic values are handled explicitly rather than silently ignored.

## W2-T1 — Map affected code and migration dependencies

**Wave:** W2 · **Status:** Planned · **Prerequisites:** W1-T1, W1-T2

Identify call sites, configuration and interfaces involved in the chosen change.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- The map links each proposed edit to a concrete migration requirement.
- Uncertain or unsupported patterns are surfaced for human review.

## W2-T2 — Implement the first migration recipe

**Wave:** W2 · **Status:** Planned · **Prerequisites:** W1-T1, W1-T2

Use deterministic transforms where possible and bounded AI proposals where needed.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- The recipe produces a reviewable patch without unrelated rewrites.
- Repeated application is stable or explicitly refuses an already migrated source.

## W3-T1 — Build differential execution

**Wave:** W3 · **Status:** Planned · **Prerequisites:** W2-T1, W2-T2

Run old and new versions against the characterization fixtures in isolated environments.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- Reports distinguish expected changes, regressions and unmeasured behavior.
- The deliberately wrong transformation is detected.

## W3-T2 — Build review and rollback guidance

**Wave:** W3 · **Status:** Planned · **Prerequisites:** W2-T1, W2-T2

Present affected contracts, evidence and the exact proposed changes.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- A maintainer can reject individual changes and reproduce the comparison.
- Document how to return to the prior source and data state within the bounded migration.

## W4-T1 — Publish a migration recipe kit

**Wave:** W4 · **Status:** Planned · **Prerequisites:** W3-T1, W3-T2

Define prerequisites, transformations, fixtures and supported version ranges.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- A second maintainer can author and run a recipe using only the documented interfaces.
- Unsupported versions stop with an explicit reason.

## W4-T2 — Add local and private-code operation

**Wave:** W4 · **Status:** Planned · **Prerequisites:** W3-T1, W3-T2

Package execution so repositories and credentials remain under owner control.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- A run can complete without uploading source to a hosted service.
- Any optional model request shows its data boundary and requires explicit configuration.

## W5-T1 — Model migration ordering and compatibility windows

**Wave:** W5 · **Status:** Planned · **Prerequisites:** W4-T1, W4-T2

Represent dependencies between separately deployed components.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- A staged fixture demonstrates old/new compatibility during the transition.
- An unsafe ordering is rejected or clearly marked as requiring coordinated downtime.

## W5-T2 — Rehearse data migration and recovery

**Wave:** W5 · **Status:** Planned · **Prerequisites:** W4-T1, W4-T2

Add a bounded schema-change fixture with backup and restoration.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- The chosen migration demonstrates recovery from an interrupted data step.
- The report distinguishes reversible source changes from irreversible data loss risks.

## W6-T1 — Pilot migrations with volunteer maintainers

**Wave:** W6 · **Status:** Planned · **Prerequisites:** W5-T1, W5-T2

Run selected recipes on approved repositories through normal maintainer review.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- Report accepted, rejected and revised patches without treating patch generation as adoption.
- Capture missed behavior and incorporate it into fixtures.

## W6-T2 — Publish recipe maintenance and regression checks

**Wave:** W6 · **Status:** Planned · **Prerequisites:** W5-T1, W5-T2

Define ownership, deprecation and compatibility testing for the catalog.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Acceptance criteria:

- A changed dependency that invalidates a recipe is caught by a reproducible check.
- Maintainers can see the last verified versions and remaining gaps.
