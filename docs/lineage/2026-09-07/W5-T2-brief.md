# Saved task work brief

> This brief contains saved work instructions. It does not reserve or claim the task, start an agent, verify a model, report token usage, prove completed checks, or establish a merged contribution.

## Project

### Project ID

```text
prj_9ef51e9826817323b774d5d3b900520f
```

### Project slug

```text
renewal-engine
```

### Project name

```text
Renewal Engine
```

## Task

### Task ID

```text
tsk_5d9c9f4b35e62de3e818ee428565ce91
```

### Title

```text
W5-T2 — Rehearse data migration and recovery
```

### Status

```text
READY
```

### Claimed by

Not claimed.

### Saved revision

```text
3
```

### Publication

Published after a textual task-plan review and approval of the linked poll option. This does not verify implementation or completed checks.

### Publication content hash

```text
d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8
```

### Roadmap position

10

### Wave

```text
5. W5 — Modernize connected systems carefully
```

### Prerequisites

### 1

```text
tsk_79615ef58d4b13fae68ef7d5e7314eeb
```

### 2

```text
tsk_57ea7445d8928fcd6b0c9890b459a98a
```

### 3

```text
tsk_e68f1340d670a17234cd0e91c5691fc1
```

### Required model

```text
- openai / gpt-6-astra · minimum effort high
- anthropic / claude-fable-5-1 · minimum effort high
```

```text
Prepared reciprocal primary/fallback instructions at the stated effort; declaration is not evidence of an executed model.
```

### Required effort

high

## Objective

```markdown
Add a bounded schema-change fixture with backup and restoration.
```

## Work instructions

```markdown
Add a bounded schema-change fixture with backup and restoration.

Start only after the listed prerequisites and scope are accepted by a maintainer. Work in the project's own repository. Document assumptions, unresolved questions and reproducible evidence. This is a proposed work package, not a claim that the implementation already exists.

Wave: W5
Prerequisites: W4-T1, W4-T2, W5-T1

Planning source: https://github.com/thepianistdirector/renewal-engine/blob/main/TASKS.md
This draft is not ready for automatic execution. Repository connection, concrete file scope and validation commands must be set in a reviewed revision before implementation.

## Prepared planning reference and execution boundary
Repository: https://github.com/thepianistdirector/renewal-engine
Branch: main
Planning base commit: 8af461149e2c4b6b3b17d54a10b3559168f8b32f
This reference identifies planning material and published skills; it does not establish integrated prerequisite implementation.
Prerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths.

## Validation boundaries
These existing Git commands verify checkout identity and patch hygiene only. They do not replace functional tests.
Exact functional commands, fixtures and paths must be ratified in the execution revision once the prerequisite-selected stack/harness exists. Do not claim these future checks ran.
Evidence artifact: docs/work/W5-T2/acceptance.md
Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion.
```

## Acceptance criteria

### Criterion 1

```markdown
The chosen migration demonstrates recovery from an interrupted data step.
```

### Criterion 2

```markdown
The report distinguishes reversible source changes from irreversible data loss risks.
```

## Repository reference

### Repository ID

```text
repo_ee03f828c0ad9fee23ad67dd857b2d12
```

### Repository location

See saved structured planning requirements and host source observations below. An absent observation is not a verified repository location.

### Base commit

```text
8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

## Current project repository context

This saved project connection is current context outside any approved immutable task revision and its publication content hash. It may change independently and does not prove a checked-out repository, branch, or commit.

The saved task repository ID matches this connection record. The current location was not frozen or approved with the task revision.

### Current connection ID

```text
repo_ee03f828c0ad9fee23ad67dd857b2d12
```

### Current repository name

```text
thepianistdirector/renewal-engine
```

### Current repository location

```text
https://github.com/thepianistdirector/renewal-engine
```

## Allowed work paths

### 1

```text
docs/work/W5-T2/acceptance.md
```

### 2

```text
docs/work/W5-T2/scope-and-integration.md
```

### 3

```text
examples/data-restore/**
```

### 4

```text
fixtures/interrupted-data-migration/**
```

### 5

```text
src/recovery/data-migration/**
```

### 6

```text
tests/recovery/data-migration/**
```

### 7

```text
tests/task-scenarios/W5-T2/**
```

## Excluded work paths

### 1

```text
.env
```

### 2

```text
.env.*
```

### 3

```text
.git
```

### 4

```text
.github/workflows
```

## Required validation commands

### 1

```sh
git rev-parse HEAD
```

### 2

```sh
git status --short
```

### 3

```sh
git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f
```

## Expected artifact

```text
pull_request
```

## Saved structured planning requirements

The JSON below preserves the current saved repository connection, branch and full base commit; preferred (recommended), fallback and permitted models with effort; deliverable; automated and manual testing instructions; ordered maintainer acceptance workflow; and pinned skill download links. JSON escapes preserve embedded line endings and exact saved text when decoded.

These fields are included in new V3 textual review snapshots. This brief exports the saved task and does not create or approve a review, attest an executed model, report completed checks, or establish execution readiness.

```json
{
  "models": {
    "allowed": [
      {
        "model": "gpt-6-astra",
        "effort": "high",
        "provider": "openai"
      },
      {
        "model": "claude-fable-5-1",
        "effort": "high",
        "provider": "anthropic"
      }
    ],
    "fallback": {
      "model": "claude-fable-5-1",
      "effort": "high",
      "provider": "anthropic"
    },
    "recommended": {
      "model": "gpt-6-astra",
      "effort": "high",
      "provider": "openai"
    }
  },
  "repository": {
    "baseSha": "8af461149e2c4b6b3b17d54a10b3559168f8b32f",
    "baseBranch": "main",
    "connectionId": "repo_ee03f828c0ad9fee23ad67dd857b2d12"
  },
  "deliverable": {
    "kind": "pull_request",
    "description": "Add a bounded schema-change fixture with backup and restoration.\n\nEvidence artifact: docs/work/W5-T2/acceptance.md plus the actual patch, fixtures and logs within the approved task scope.\n\nPrerequisite results must be accepted and integrated. Maintainer publishes a new task revision against that integrated base before execution; runtime work also needs the real harness and exact allowed paths."
  },
  "verification": {
    "manual": {
      "steps": [
        "Back up disposable data, interrupt the schema/data migration at a documented boundary and restore. Compare recovered data and source versions; report any state that cannot be reversed safely."
      ],
      "evidence": [
        "docs/work/W5-T2/acceptance.md",
        "Record setup/fixtures, actions, expected and observed results, relevant logs or artifacts, and PASS / FAIL / NOT RUN for each criterion."
      ],
      "notApplicableReason": null
    },
    "automated": {
      "commands": [
        "git rev-parse HEAD",
        "git status --short",
        "git diff --check 8af461149e2c4b6b3b17d54a10b3559168f8b32f"
      ],
      "notApplicableReason": null
    }
  },
  "schemaVersion": 1,
  "requiredSkills": [
    {
      "name": "tanduna-contribution",
      "path": ".agents/skills/tanduna-contribution/SKILL.md",
      "commitSha": "a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd",
      "downloadUrl": "https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md",
      "repositoryUrl": "https://github.com/thepianistdirector/context-harbor"
    },
    {
      "name": "renewal-engine-validation",
      "path": ".agents/skills/renewal-engine-validation/SKILL.md",
      "commitSha": "8af461149e2c4b6b3b17d54a10b3559168f8b32f",
      "downloadUrl": "https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md",
      "repositoryUrl": "https://github.com/thepianistdirector/renewal-engine"
    }
  ],
  "acceptanceWorkflow": [
    "Contributor identifies the saved Tanduna task revision, repository/base, accepted prerequisites, selected primary or fallback model and effort, and exact required skill versions.",
    "Contributor performs the task-specific testing procedure and maps each original acceptance criterion to setup, expected result, observed result and reproducible evidence. Failed and unrun checks remain visible.",
    "Maintainer reproduces the material checks, reviews the scoped patch or design artifact and verifies the stated model/skill evidence. Unsupported model claims or missing evidence remain unresolved rather than accepted automatically.",
    "Maintainer records acceptance or requested changes against the reviewed revision. A passing format check, generated patch or completed model invocation does not by itself satisfy the task."
  ]
}
```

### Saved host source observations

Observation timestamps are the saved host-supplied values, not a fresh source check or proof of completed testing. Missing observations remain missing.

```json
{
  "skills": [
    {
      "path": ".agents/skills/tanduna-contribution/SKILL.md",
      "commitSha": "a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd",
      "observedAt": 1788712974112,
      "downloadUrl": "https://raw.githubusercontent.com/thepianistdirector/context-harbor/a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd/.agents/skills/tanduna-contribution/SKILL.md",
      "repositoryUrl": "https://github.com/thepianistdirector/context-harbor"
    },
    {
      "path": ".agents/skills/renewal-engine-validation/SKILL.md",
      "commitSha": "8af461149e2c4b6b3b17d54a10b3559168f8b32f",
      "observedAt": 1788712974257,
      "downloadUrl": "https://raw.githubusercontent.com/thepianistdirector/renewal-engine/8af461149e2c4b6b3b17d54a10b3559168f8b32f/.agents/skills/renewal-engine-validation/SKILL.md",
      "repositoryUrl": "https://github.com/thepianistdirector/renewal-engine"
    }
  ],
  "repository": {
    "baseSha": "8af461149e2c4b6b3b17d54a10b3559168f8b32f",
    "projectId": "prj_9ef51e9826817323b774d5d3b900520f",
    "baseBranch": "main",
    "observedAt": 1788712974867,
    "visibility": "PUBLIC",
    "connectionId": "repo_ee03f828c0ad9fee23ad67dd857b2d12",
    "repositoryUrl": "https://github.com/thepianistdirector/renewal-engine"
  }
}
```
