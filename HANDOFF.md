# Renewal Engine execution handoff

**Public 0.1.0 and fresh external runtime reproduction are verified.**
Human maintainer review and native Tanduna publication remain unfinished.

Public release:
https://github.com/thepianistdirector/renewal-engine/releases/tag/v0.1.0

External verification:
https://github.com/thepianistdirector/renewal-engine/actions/runs/34226941566

## Ownership and approvals

Continue the same native Goal in Codex task
`01a07e1c-3ed5-7f90-9b4d-f5c4977ad123`. The latest native readback is blocked
pending Mac-side Tanduna access and actual human observations. The same gates
remained through publication, helper preparation and the subsequent availability
check. The complete public-product/native-plan objective is unchanged. The
canonical plan retains its earlier activation snapshot; always read the live
native Goal before resuming. Its already reviewed export remains pinned for
the Mac helper because the product plan itself has not changed. Execution
metadata verified OpenAI gpt-6-astra, high effort, including leaf critics.

The owner approved the original fixture and actual runtime comparison, necessary
dependencies/VPS resources, and then the concrete GitHub publication packet on
September 8, 2026. Do not request those permissions again. GitHub publication
used the existing `thepianistdirector` account. The source work remains in this
repository; no parent/sibling/shared configuration was changed.

## Published identity and evidence

Tag `v0.1.0` points to `737dc0867d5b4e6c8f3ba29f04fade8573ff683d`.
The release and tag were publicly read back; all three assets downloaded
anonymously and match their approved hashes:

- CLI: `ee6b2b9e6ba3ffc3e34102dc70ac596b1e3f8479bacd8a6e99072a7c78c80047`.
- Source archive: `2bf2d535ab2c27b87305f960f793151f630d8e70186a52e34ec704cf1eb0c48e`.
- SHA256SUMS: `a731488978edcc8e26224a461b4655f101abebe9b87bc08d443844bb3aacbb6e`.

The released tag/assets remain unchanged. Subsequent evidence and current plan
updates live on `codex/renewal-engine-0.1`. Do not rebuild and replace published
assets from that later checkout. Main has not been automatically merged.

The 27-test suite passes. Both real runtimes, CPython 3.11.16 and 3.12.14, run
12 passing normal cases and reject two diagnostic-source regressions in the
negative control. The installed public package also verifies saved normal and
negative examples without a development checkout.

The fresh GitHub-hosted Ubuntu 24.04 x86_64 runner downloaded the exact public
archive anonymously, checked its digest, installed the CLI, and built both
runtimes from checksum-pinned official sources. Normal, negative, idempotence,
real SIGINT during partial candidate creation and comparison, safe restart and
tamper refusal all passed. The 424 retained external files were retrieved from
the completed job log; the public CLI independently reopened normal, negative,
repeat and restart results and refused both incomplete attempts.

Evidence: `docs/evidence/public-release.json`, `external-runtime.json`,
`external-observations.json`, and `runtime-verification.md`. The external
observation JSON contains base64-encoded exact files and a sanitized test
transcript; raw provider logs remain project-local. No shim, arbitrary repository
execution, human observation or adoption is claimed.

The external workflow is on dedicated branch
`codex/renewal-engine-public-verification`, commit
`400f269d780fd7dd720eb0947939454dba0845d5`. Its local isolated worktree is
`.local/worktrees/public-verification`, verified to belong to this repository.
The job is completed successfully; do not restart it or wait for it as live.
No third-party action, repository write token, paid runner, artifact storage,
sudo or shared machine installation was used. Decision 004 records its scope.

## Remaining gates

1. A consenting Python maintainer or qualified human reviewer must complete
   `docs/publication/maintainer-walkthrough.md` using the public artifact outside
   the development VPS. Record actual installation, patch review, independent
   negative-control diagnosis, saved reopening/recovery and manual interface
   observations. No participant observations have been received. Native zoom
   and assistive-technology observations remain unrun; agent browser/CI evidence
   does not replace the required human review.
2. Connect authorized Tanduna MCP. No Tanduna tools are available in this task;
   the user has been asked to connect it. The public guide requires its helper
   on the user's own computer, with local/browser sign-in, not on this VPS.
   Never copy credentials, use another task's login, change shared config or
   edit Tanduna's application.
3. Once connected, make a read-only identity/project check, refresh live tasks,
   draft plans and proposals. Prepare the native draft using actual tool schemas,
   preserve original IDs/history, submit for textual review, and obtain approval
   of its exact poll option before publication. GitHub publication approval does
   not authorize a native Tanduna vote.
4. Read back native 26 waves, 218 tasks, release horizons, mappings, dependency
   links, accurate statuses and real public-release access instructions at:
   https://tanduna.com/projects/renewal-engine/roadmap and
   https://tanduna.com/p/renewal-engine/tasks.

September 8 public readback still exposes the original twelve task IDs. The
updated export is local/GitHub material, not an accepted native plan. Counts:
50 outcomes for 0.1, 72 later 0.x, 80 long-term, 16 exploratory. All twelve
historical identities and acceptance/dependency records remain immutable and
mapped. Task-level BLOCKED for native publication does not mark the full Goal
complete or satisfy the native Goal's three-turn blocked audit.

## Continue locally

Inspect Git status and native Goal first. Update only `project-plan.json` for
canonical task evidence, then generate/check views. Keep frozen lineage intact.

```sh
python3 tools/plan.py generate
python3 tools/plan.py validate
python3 tools/plan.py check
```

Run implementation tests again when code changes justify it. Do not repeat
successful runtime jobs to substitute for missing human/native evidence.
The next later-0.x outcome is an explicit versioned recipe contract; it is
outside this bounded 0.1 gate.

## Mac helper handoff requested by Lucas

Lucas requested a prompt for a local Mac Codex task that creates a native
15-minute schedule and reads a shared request file. The complete English prompt
is `coordination/mac/MAC-HELPER-PROMPT.md`; protocol and initial four requests
are beside it. Request branch: `codex/renewal-engine-0.1`. Mac result branch:
`codex/mac-helper-results`. The Mac owns registration/results on that branch;
this remote owner owns the request file and canonical plan.

Read `coordination/mac/registration.json` and the per-request result files from
the result branch once the Mac task is actually set up. No native Mac schedule
or live helper has yet been observed. Queued requests are not a live process or
verified wait. The prompt must be pasted into a task running locally on the Mac.
It instructs the helper to discover native scheduling tools, verify creation,
keep unchanged checks quiet, facilitate actual Lucas observations, and obtain
specific native poll approval before publication. It cannot substitute agent
judgment for the human gate or transfer login credentials to this VPS.

The queued canonical export is pinned to the published d947cea evidence commit
and SHA-256. If later plan changes alter that export, increment the relevant
request revision and pin the new reviewed input before asking the Mac to use it.
