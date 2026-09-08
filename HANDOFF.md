# Renewal Engine execution handoff

**Public 0.1.0 and fresh external runtime reproduction are verified.**
Human maintainer review and native Tanduna publication remain unfinished.

Public release:
https://github.com/thepianistdirector/renewal-engine/releases/tag/v0.1.0

External verification:
https://github.com/thepianistdirector/renewal-engine/actions/runs/34226941566

## Ownership and approvals

Continue the same native Goal in Codex task
`01a07e1c-3ed5-7f90-9b4d-f5c4977ad123`. Work resumed on the Mac helper's
handoff. The native tool still reports blocked and offers no resume action;
do not duplicate the Goal or treat that status as cancellation. The remaining
conditions have changed: Mac setup and login succeeded; the native draft now
exists, but its reviewer is disabled and full human evidence remains missing.
The complete public-product/native-plan objective is unchanged. Execution
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

The Mac helper is established on task `01a0811a-9fe7-7b23-9107-8222da04124f`,
host `local`, native heartbeat `lucas-mac-helper`, every 15 minutes. Its setup,
initial cycle and scoped transport passed. Native scheduled firing remains
unobserved in its registration snapshot. Local Tanduna login succeeded;
credentials stay in the official Mac login child and must never be transferred.

The complete native 218-task/26-wave/424-edge draft was saved and submitted.
Read `docs/publication/native-plan-status.md` for the exact proposal, snapshot,
review and option IDs. All returned task/wave mappings have been reconciled into
the canonical plan. Preserve the twelve historical IDs and the existing new IDs.
Do not recreate tasks, infer a passing review, cast votes or publish without the
specific reviewed-option approval.

Textual review is PENDING with reason `disabled` and no attempt. The 218
structured planningRequirements fields are null. RE-MAC-005 is a new read-only
request for actual tool schemas, applicable long-term-planning policy and
supported recovery controls. No Tanduna app/configuration change is authorized.
RE-MAC-003 revision 1 is held to preserve the frozen submission. Prepare a new
versioned request only after the missing facts establish the appropriate change.

Partial Mac public-package inspection/reopening passed on arm64 CPython 3.14.6.
The participant reported report-review approval; detailed negative-control
diagnosis, qualification and performed/skipped steps remain unconfirmed. The
Mac task already asked for those missing observations. Do not repeat an approval
question or relabel an agent run as human validation.

Root public readback still shows twelve historical task IDs. The new proposal
returns 404 anonymously. After passing native review and specific poll approval,
verify publication/readback of 26 waves, 218 tasks, mappings, 424 edges, release
horizons, honest evidence levels and real access instructions at:
https://tanduna.com/projects/renewal-engine/roadmap and
https://tanduna.com/p/renewal-engine/tasks.

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

## Mac request/results bridge

Source requests: `coordination/mac/requests.json` on
`codex/renewal-engine-0.1`. Mac registration/results:
`coordination/mac/registration.json` and `coordination/mac/results/` on
`codex/mac-helper-results`. Preserve that result branch; this root writes only
requests and its canonical/evidence files. Latest reconciled Mac result commit:
`b9304597937b4d7307f2ea195537e4b48418ebe2`.

The Mac task can notify this existing remote owner through the supported task
message path. Root can read/wait on the known Mac task using host `local`;
root's currently exposed tool set has no send-message-to-task or Tanduna tools,
so use the versioned file requests for further work. Never obtain credentials
or invoke undocumented task APIs to bypass that capability boundary.

RE-MAC-001 and 002 succeeded, 003 is held at its existing submitted snapshot,
004 needs the participant's missing observations, and 005 requests read-only
review/schema facts. A submitted review with no attempt is not a live job.
After a genuine user/Mac resume, start a fresh blocked audit if needed and keep
the full Goal uncompleted until both human and native-publication gates pass.
