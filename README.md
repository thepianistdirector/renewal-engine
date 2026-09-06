# Renewal Engine

**Help entire software ecosystems modernize without losing the behavior people rely on.**

The hardest software to replace is the software that already does thousands of invisible things correctly.

![Renewal Engine: aspirational concept, not an implemented product](assets/vision-concept.png)

> This is a public planning repository. There is no product implementation or playable build yet. The image is an AI-generated vision reference, not a screenshot. All waves and tasks are proposed; no completed work, community approval or funding is implied.

## The mission

Build an open modernization system that helps teams understand existing behavior, propose narrow changes and compare the results. Combine deterministic transformations, AI-assisted patches and reproducible evidence so useful old software can keep evolving.

Choose a migration, map the affected behavior, capture representative fixtures, propose a transformation, run old and new versions against the same cases, inspect the differences and adopt changes through normal review.

## Who this is for

Maintainers and engineering teams with aging libraries, frameworks and business-critical applications.

## The first thing we want to prove

One well-scoped library or framework upgrade in an approved open-source fixture, with a deliberately wrong transformation that the behavior comparison must catch.

A green test suite may miss the behavior that matters. Document coverage gaps and observed contracts; use deliberate wrong changes to test the checks. Never claim general semantic equivalence for arbitrary programs.

## What this could become

A shared library of migration recipes, behavior fixtures and compatibility knowledge across languages and ecosystems, usable locally on private code as well as public projects.

Automated refactoring already has mature foundations. The proposed contribution joins source understanding, differential behavior checks, migration planning and reviewable AI patches into a maintainable end-to-end workflow.

## Why build it together

Maintainers can contribute one migration recipe, one tricky fixture or one language adapter. Thousands of small, well-tested contributions can reduce repeated migration work across an ecosystem.

We are looking for founding maintainers and contributors who can make one small, reviewable part real. Bring a concrete use case, a difficult test case, an interface sketch or a focused patch. If you use a coding agent, give it one agreed task and review its result. Accepted work matters more than generated volume.

## Build the first useful piece with us

Start with [Renewal Engine on Tanduna](https://tanduna.com/projects/renewal-engine) and the [first task: Select and document the reference migration](https://tanduna.com/p/renewal-engine/tasks/tsk_17cb9d58845743cb4d031739f78f3ab1). Bring a concrete use case, a difficult fixture or time to review a small contribution. An agent can help do the work; a maintainer still checks that the result meets the agreed task.

1. Pick one task from the [six-wave roadmap](ROADMAP.md) and [twelve task contracts](TASKS.md), then agree its scope and prerequisites.
2. Read its exact repository/base, preferred model and fallback, required skills, testing procedure and acceptance flow.
3. Work on the accepted revision and return a focused patch or artifact with evidence another contributor can reproduce.

The first milestone is **Know what must survive**: Choose one migration and define its behavior boundary.

The complete [contribution guide](CONTRIBUTING.md) includes two public downloads: the [shared contribution skill](https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md) and [Renewal Engine validation skill](https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md). Both are pinned to exact Git commits. Every task selects GPT-6 Astra or Claude Fable 5.1 as preferred model and the other as fallback, with Medium or High effort stated explicitly.

This repository currently contains the proposal, concept art, roadmap, task contracts and contribution skills. It does not yet contain a working product. Future implementation tasks remain dependent on earlier results and a maintainer-approved execution baseline. The written contract describes what contributors must satisfy; it does not claim every corresponding Tanduna enforcement feature is already live.

## What we are not promising

No automatic merging or production migration, private-code upload by default, universal language support or a guarantee that an upgrade has no regressions.

There is no delivery date, token target, paid offer or crowdfunding campaign here. Community interest does not guarantee a finished product. The next milestone depends on contributors, maintainer capacity and evidence from the previous one.

## Existing work we should learn from

- [OpenRewrite](https://docs.openrewrite.org/)

These are related foundations and references, not partners or endorsements. We should reuse compatible components or contribute upstream when that is the better route. This proposal does not claim that its individual ingredients are unprecedented. Dependencies and their licenses will be evaluated before adoption.

## License and contribution

This repository is published under [GNU AGPL-3.0](LICENSE). See [CONTRIBUTING.md](CONTRIBUTING.md) for the proposed contribution workflow and [the image note](assets/README.md) for concept provenance.
