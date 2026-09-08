# Current owner-directed development

The September 7 launch and September 8 owner extension authorize development
through 0.5 in this repository. See docs/recipes.md and docs/0.5-guide.md. GPT-6 Astra owns all work, including UI/UX; older reciprocal
model fallback prose below is preserved history and no longer applies to this
owner-directed scope. The historical task revisions remain frozen. New work is
mapped in project-plan.json rather than retroactively accepted against them.

Run `python3 -m unittest discover -s tests -v`, `python3 tools/plan.py validate`,
`python3 tools/plan.py self-test`, and `python3 tools/plan.py check`. Synthetic
orchestration tests are labeled and cannot replace real runtime or human
validation. Keep every test artifact under this project’s .local or .runs.
Inspection never executes selected source. Project execution requires its explicit
command, scope authorization and a verified isolation profile; do not auto-apply a candidate.
Use a new run directory after failure; retain prior evidence and original bytes.

The repository’s initial planning guide follows for context. Its complete
unchanged form is also retained in docs/lineage/2026-09-07/CONTRIBUTING.md.

---

# Contributing to Renewal Engine

Start with [the project on Tanduna](https://tanduna.com/projects/renewal-engine) and select one [saved task](TASKS.md). Discuss your intended result before starting overlapping work. GitHub holds source and reviewable patches; Tanduna holds the community's task revisions and decisions.

## Before your agent starts

Use the exact repository, base commit and task revision in the accepted brief. The current planning baseline is `main` at `8af461149e2c4b6b3b17d54a10b3559168f8b32f`. Later tasks must be rebound to the real integrated prerequisite code. Do not silently substitute current HEAD, invent a missing harness or treat a branch name as an immutable base.

Read both public, standalone skills:

1. [Tanduna contribution protocol](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md).
2. [Renewal Engine validation](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md).

The links are pinned to Git commits and require no account. Save each as `SKILL.md` in the matching named skill folder used by your agent, or ask your agent to read the linked Markdown directly. Reading does not require installing or executing a downloaded script. These skills are covered by the hosting repositories' AGPL-3.0 licenses.

The preferred model and explicit fallback are listed for every task. Lucas permits GPT-6 Astra and Claude Fable 5.1 as mutual fallbacks for these tasks, using the specified Medium or High effort. Do not substitute another model or lower effort without a new maintainer decision. Record model/effort information exposed by the actual runtime, and clearly mark any contributor-only declaration or unavailable proof.

## Execute and request acceptance

Work in an isolated branch or fork with the saved allowed/excluded paths. Follow that task's testing procedure; keep failed and unrun checks visible. Design and playtest tasks use a reproducible manual protocol. Implementation tasks need real functional checks in the chosen stack plus runtime evidence. The baseline Git commands check identity and patch hygiene, not product behavior.

Submit the scoped patch or artifact, task ID/revision, base and result references, skill versions, model evidence and a criterion-by-criterion result report. The maintainer reviews and reproduces the relevant evidence before recording acceptance. Missing skills, a non-permitted model, unresolved required evidence or failed criteria cannot be converted into a passing contribution by self-reporting success.

If a prerequisite, scope, baseline or validation procedure is missing, explain the concrete gap and request a revised task before execution. Do not erase old task or review history. Changing execution instructions requires renewed review of the affected revision.

## Contribution boundaries

Keep credentials and private data out of prompts, artifacts and commits. Label generated concepts, simulated results, actual observations and unrun checks accurately. A planning task does not authorize purchases, account changes, live messages, merge or deployment.

Contribute material you have the right to publish under [AGPL-3.0](LICENSE), with attribution and third-party license records. Initial stewardship remains with the repository owner while founding maintainers are recruited. Accepted contributions matter; tokens spent do not automatically confer control, equity or voting rights.
