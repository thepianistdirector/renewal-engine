# Renewal Engine roadmap

This is a public planning repository. There is no product implementation or playable build yet. The image is an AI-generated vision reference, not a screenshot. All waves and tasks are proposed; no completed work, community approval or funding is implied.

The order reflects dependencies, not calendar commitments. Each wave advances only when its stated outcome is demonstrated and a maintainer accepts the next scope. Capacity targets are hypotheses to test.

## W1 — Know what must survive

Choose one migration and define its behavior boundary.

- **W1-T1: Select and document the reference migration.** Pick a maintained open-source fixture and a bounded dependency or framework change.
- **W1-T2: Capture characterization fixtures.** Record representative inputs, outputs, side effects and important error behavior.

## W2 — Understand and propose a narrow change

Build a useful transformation pipeline.

- **W2-T1: Map affected code and migration dependencies.** Identify call sites, configuration and interfaces involved in the chosen change.
- **W2-T2: Implement the first migration recipe.** Use deterministic transforms where possible and bounded AI proposals where needed.

## W3 — Compare behavior, including failures

Make evidence stronger than a successful build.

- **W3-T1: Build differential execution.** Run old and new versions against the characterization fixtures in isolated environments.
- **W3-T2: Build review and rollback guidance.** Present affected contracts, evidence and the exact proposed changes.

## W4 — Recipes other maintainers can trust

Turn the single migration into a contribution format.

- **W4-T1: Publish a migration recipe kit.** Define prerequisites, transformations, fixtures and supported version ranges.
- **W4-T2: Add local and private-code operation.** Package execution so repositories and credentials remain under owner control.

## W5 — Modernize connected systems carefully

Extend to staged, multi-repository changes.

- **W5-T1: Model migration ordering and compatibility windows.** Represent dependencies between separately deployed components.
- **W5-T2: Rehearse data migration and recovery.** Add a bounded schema-change fixture with backup and restoration.

## W6 — An ecosystem that stays maintainable

Validate sustained use and recipe quality.

- **W6-T1: Pilot migrations with volunteer maintainers.** Run selected recipes on approved repositories through normal maintainer review.
- **W6-T2: Publish recipe maintenance and regression checks.** Define ownership, deprecation and compatibility testing for the catalog.

See [TASKS.md](TASKS.md) for observable acceptance criteria.
