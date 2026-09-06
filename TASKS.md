# Renewal Engine: task contracts

Twelve proposed work packages, with named waves and dependency order. None is completed by publishing this document. The linked Tanduna revision is the contribution authority; this repository records the maintainer's intended contract while Tanduna's structured requirement support is being updated.

Every task below names its repository, branch, verified planning commit, preferred model, allowed fallback, immutable public skills, task-specific testing procedure and maintainer acceptance flow. A later implementation task still needs its prerequisite code, a rebased execution revision, narrow file scope and real functional commands. Do not treat the current planning commit as if that future code exists.

The allowed model pair is GPT-6 Astra and Claude Fable 5.1, with the effort stated per task. A model declaration is not independent runtime evidence; unresolved proof remains visible to the maintainer. See [CONTRIBUTING.md](CONTRIBUTING.md) and [the machine-readable authored contracts](task-contracts.json).

## W1-T1 — Select and document the reference migration

**Wave:** W1 · **Prerequisites:** None; maintainer scope review first

Pick a maintained open-source fixture and a bounded dependency or framework change.

**Saved Tanduna task:** [W1-T1](https://tanduna.com/p/renewal-engine/tasks/tsk_17cb9d58845743cb4d031739f78f3ab1)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Maintainer accepts the scoped design protocol; this is not product implementation.

**Preferred:** `gpt-6-astra` / medium. **Accepted fallback:** `claude-fable-5-1` / medium. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- Record licensing, source revisions, supported runtime and the specific migration objective.
- List behavior that must remain stable and areas that are intentionally out of scope.

### Testing procedure

Inspect the chosen open-source fixture at a pinned revision and record its license, old/new runtime and bounded migration. Run or document the actual baseline behavior and identify intentionally unchanged contracts.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

This task uses the saved reproducible manual protocol. Distinguish paper/synthetic exercises from actual participant or physical observations.

**Evidence artifact:** `docs/work/W1-T1/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W1-T2 — Capture characterization fixtures

**Wave:** W1 · **Prerequisites:** W1-T1

Record representative inputs, outputs, side effects and important error behavior.

**Saved Tanduna task:** [W1-T2](https://tanduna.com/p/renewal-engine/tasks/tsk_a35bd15aa7b3e4318c5552b4cc3e82b3)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- Fixtures run against the original application and fail for a deliberate behavioral regression.
- Sensitive or nondeterministic values are handled explicitly rather than silently ignored.

### Testing procedure

Run representative inputs against the original fixture and retain outputs, errors and side effects. Introduce a deliberate behavioral regression and confirm the characterization check fails; document narrow nondeterminism handling.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W1-T2/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W2-T1 — Map affected code and migration dependencies

**Wave:** W2 · **Prerequisites:** W1-T1, W1-T2

Identify call sites, configuration and interfaces involved in the chosen change.

**Saved Tanduna task:** [W2-T1](https://tanduna.com/p/renewal-engine/tasks/tsk_17179248999bbb2086133ef8ed4cb216)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- The map links each proposed edit to a concrete migration requirement.
- Uncertain or unsupported patterns are surfaced for human review.

### Testing procedure

Trace each proposed migration requirement to actual call sites, config and interfaces. Review an unsupported pattern and verify it remains flagged rather than silently transformed.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

This task uses the saved reproducible manual protocol. Distinguish paper/synthetic exercises from actual participant or physical observations.

**Evidence artifact:** `docs/work/W2-T1/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W2-T2 — Implement the first migration recipe

**Wave:** W2 · **Prerequisites:** W1-T1, W1-T2, W2-T1

Use deterministic transforms where possible and bounded AI proposals where needed.

**Saved Tanduna task:** [W2-T2](https://tanduna.com/p/renewal-engine/tasks/tsk_a9e192b7ec0fa463c48c7b7b3aea4386)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- The recipe produces a reviewable patch without unrelated rewrites.
- Repeated application is stable or explicitly refuses an already migrated source.

### Testing procedure

Apply the recipe to the pinned fixture, review the patch, and apply it a second time. Verify stability or an explicit already-migrated refusal and run characterization cases to detect unrelated behavior changes.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W2-T2/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W3-T1 — Build differential execution

**Wave:** W3 · **Prerequisites:** W2-T1, W2-T2

Run old and new versions against the characterization fixtures in isolated environments.

**Saved Tanduna task:** [W3-T1](https://tanduna.com/p/renewal-engine/tasks/tsk_89e135a4cdda5620e7737ed426e59e3c)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- Reports distinguish expected changes, regressions and unmeasured behavior.
- The deliberately wrong transformation is detected.

### Testing procedure

Execute old and candidate versions on the same characterization fixtures in isolated environments. Run a deliberately wrong transformation and verify the differential report distinguishes regression from expected change.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W3-T1/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W3-T2 — Build review and rollback guidance

**Wave:** W3 · **Prerequisites:** W2-T1, W2-T2, W3-T1

Present affected contracts, evidence and the exact proposed changes.

**Saved Tanduna task:** [W3-T2](https://tanduna.com/p/renewal-engine/tasks/tsk_7e9f19f4a3e6ff05eb357075dac35818)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `claude-fable-5-1` / high. **Accepted fallback:** `gpt-6-astra` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- A maintainer can reject individual changes and reproduce the comparison.
- Document how to return to the prior source and data state within the bounded migration.

### Testing procedure

Have a maintainer inspect the proposed patch and reject one change. Reproduce the comparison and exercise the documented return to prior source/disposable data; expose irreversible data limitations.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W3-T2/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W4-T1 — Publish a migration recipe kit

**Wave:** W4 · **Prerequisites:** W3-T1, W3-T2

Define prerequisites, transformations, fixtures and supported version ranges.

**Saved Tanduna task:** [W4-T1](https://tanduna.com/p/renewal-engine/tasks/tsk_79615ef58d4b13fae68ef7d5e7314eeb)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- A second maintainer can author and run a recipe using only the documented interfaces.
- Unsupported versions stop with an explicit reason.

### Testing procedure

Have a second maintainer author a recipe from the public kit. Test supported and unsupported version ranges, then run the fixture and review its exact proposed changes.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W4-T1/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W4-T2 — Add local and private-code operation

**Wave:** W4 · **Prerequisites:** W3-T1, W3-T2

Package execution so repositories and credentials remain under owner control.

**Saved Tanduna task:** [W4-T2](https://tanduna.com/p/renewal-engine/tasks/tsk_57ea7445d8928fcd6b0c9890b459a98a)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- A run can complete without uploading source to a hosted service.
- Any optional model request shows its data boundary and requires explicit configuration.

### Testing procedure

Complete a local fixture migration without uploading source. Enable an optional model route only with explicit test configuration and inspect its declared data boundary; reject absent permission or credentials clearly.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W4-T2/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W5-T1 — Model migration ordering and compatibility windows

**Wave:** W5 · **Prerequisites:** W4-T1, W4-T2

Represent dependencies between separately deployed components.

**Saved Tanduna task:** [W5-T1](https://tanduna.com/p/renewal-engine/tasks/tsk_e68f1340d670a17234cd0e91c5691fc1)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- A staged fixture demonstrates old/new compatibility during the transition.
- An unsafe ordering is rejected or clearly marked as requiring coordinated downtime.

### Testing procedure

Run a staged old/new component fixture through the documented ordering. Try an unsafe order and verify refusal or an explicit coordinated-downtime requirement; inspect compatibility during each intermediate step.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W5-T1/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W5-T2 — Rehearse data migration and recovery

**Wave:** W5 · **Prerequisites:** W4-T1, W4-T2, W5-T1

Add a bounded schema-change fixture with backup and restoration.

**Saved Tanduna task:** [W5-T2](https://tanduna.com/p/renewal-engine/tasks/tsk_5d9c9f4b35e62de3e818ee428565ce91)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- The chosen migration demonstrates recovery from an interrupted data step.
- The report distinguishes reversible source changes from irreversible data loss risks.

### Testing procedure

Back up disposable data, interrupt the schema/data migration at a documented boundary and restore. Compare recovered data and source versions; report any state that cannot be reversed safely.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W5-T2/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W6-T1 — Pilot migrations with volunteer maintainers

**Wave:** W6 · **Prerequisites:** W5-T1, W5-T2

Run selected recipes on approved repositories through normal maintainer review.

**Saved Tanduna task:** [W6-T1](https://tanduna.com/p/renewal-engine/tasks/tsk_c5c45d54c7d504d440dc18fdd697b84a)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- Report accepted, rejected and revised patches without treating patch generation as adoption.
- Capture missed behavior and incorporate it into fixtures.

### Testing procedure

Submit bounded patches through the volunteer maintainer's normal review with permission. Count accepted, revised and rejected outcomes separately; turn missed behavior into a reproduced characterization fixture.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W6-T1/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.

## W6-T2 — Publish recipe maintenance and regression checks

**Wave:** W6 · **Prerequisites:** W5-T1, W5-T2, W6-T1

Define ownership, deprecation and compatibility testing for the catalog.

**Saved Tanduna task:** [W6-T2](https://tanduna.com/p/renewal-engine/tasks/tsk_4094a1ff51d72e4a7b4a14420a3f3c48)

**Repository:** [https://github.com/thepianistdirector/renewal-engine](https://github.com/thepianistdirector/renewal-engine) · **Branch:** `main`

**Planning base commit:** [`8af461149e2c4b6b3b17d54a10b3559168f8b32f`](https://github.com/thepianistdirector/renewal-engine/commit/8af461149e2c4b6b3b17d54a10b3559168f8b32f)

**Execution gate:** Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

**Preferred:** `gpt-6-astra` / high. **Accepted fallback:** `claude-fable-5-1` / high. Other models require a maintainer revision before work.

**Required skills:** [contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md), at the linked immutable versions.

### Acceptance criteria

- A changed dependency that invalidates a recipe is caught by a reproducible check.
- Maintainers can see the last verified versions and remaining gaps.

### Testing procedure

Change a dependency so a supported recipe becomes invalid and run its compatibility checks. Verify the failure is surfaced with last verified versions, maintainer ownership and a reproducible regression case.

Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.

Existing baseline checks (repository root; identity and patch hygiene only):

```sh
git rev-parse HEAD
git status --short
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.

**Evidence artifact:** `docs/work/W6-T2/acceptance.md` plus the actual patch, fixtures and logs within the approved task scope.

### Acceptance workflow

1. Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.
2. Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.
3. Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.
4. Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task.
