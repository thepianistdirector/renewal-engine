# Renewal Engine execution handoff

**Current owner target: 0.5.0 local release candidate (see GOAL.md). Public 0.1.0 remains verified and immutable.**
Human maintainer review and native Tanduna publication remain unfinished.

Public release:
https://github.com/thepianistdirector/renewal-engine/releases/tag/v0.1.0

External verification:
https://github.com/thepianistdirector/renewal-engine/actions/runs/34226941566


## 0.5 candidate checkpoint

Local implementation now includes versioned shipped recipes/composition, the Path
hard-link migration, static impact, strict repeated observations and narrow
policies, exact hunk/approval/stale checks, private summary export and verified
narrow Python isolation. **72 tests and 27 packaged CLI checks pass**, as do real
SIGINT/restart checks. Evidence is in docs/evidence/0.5; usage is docs/0.5-guide.md.
The candidate is in dist/0.5.0; 0.1 dist assets and tag are not replaced.

0.5 publication, a fresh public-download external run, second-recipe human review
and native plan publication are unfinished. The prepared external workflow is
`docs/publication/0.5-external-workflow.yml`; it requires approved exact asset
hashes and uses the existing Linux profile without weakening runner security.
Do not call a 0.5 number or local test a completed public goal.

RE-MAC-005 supersedes the old PENDING/disabled checkpoint: all 218 current task
reviews are FAILED; deployed failure cause, attempt and recovery action are not
exposed. Missing planningRequirements are not established as that cause. The
existing IDs/revision/submitted hash stay frozen, RE-MAC-003 stays HOLD, and no
retry/vote/resubmission occurred. Mac native heartbeat firing is now verified.

## Ownership and approvals

Continue the same native Goal in Codex task
`01a07e1c-3ed5-7f90-9b4d-f5c4977ad123`. Work resumed on the Mac helper's
handoff. The native tool still reports blocked and offers no resume action;
do not duplicate the Goal or treat that status as cancellation. The remaining
conditions have changed: Mac setup and login succeeded; the native draft now
exists, but its current review is FAILED with no exposed cause; full human evidence remains missing.
The owner expanded the product target to 0.5 on September 8; public-plan and human evidence obligations remain. Execution
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
initial cycle and scoped transport passed. Native scheduled firing is now
verified in its updated registration snapshot. Local Tanduna login succeeded;
credentials stay in the official Mac login child and must never be transferred.

The complete native 218-task/26-wave/424-edge draft was saved and submitted.
Read `docs/publication/native-plan-status.md` for the exact proposal, snapshot,
review and option IDs. All returned task/wave mappings have been reconciled into
the canonical plan. Preserve the twelve historical IDs and the existing new IDs.
Do not recreate tasks, infer a passing review, cast votes or publish without the
specific reviewed-option approval.

Current native review is FAILED with cause, attempt and recovery unavailable.
The 218 structured planningRequirements remain null. RE-MAC-005 completed
read-only schema/policy discovery; absence of requirements is not established as
the failure cause. No Tanduna app/configuration change is authorized. RE-MAC-003
stays HOLD. Obtain supported failure/recovery details before any new request.

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
The 0.5 scoped product is implemented locally. Remaining release work is concrete
publication authorization, public artifact readback, fresh external reproduction,
human second-recipe evidence and supported native-plan recovery/publication.

## Mac request/results bridge

Source requests: `coordination/mac/requests.json` on
`codex/renewal-engine-0.1`. Mac registration/results:
`coordination/mac/registration.json` and `coordination/mac/results/` on
`codex/mac-helper-results`. Preserve that result branch; this root writes only
requests and its canonical/evidence files. Latest reconciled Mac result commit:
`87d1f8144f6c3165137d80f4c382567d36527e6d`.

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
