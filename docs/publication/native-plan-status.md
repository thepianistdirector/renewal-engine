# Native plan reconciliation — September 8, 2026

The authenticated Mac helper saved and submitted the complete native draft.
This is not an accepted or publicly published replacement plan.

| Record | Actual returned identity |
| --- | --- |
| Project | prj_9ef51e9826817323b774d5d3b900520f |
| Repository | repo_ee03f828c0ad9fee23ad67dd857b2d12 |
| Proposal | prp_dc23eeda9235cb75b05469c22c83342f |
| Publication snapshot | tpub_7edf546ba722af40bbcaad11daf2958e |
| Review request | tpr_cf62e2dc60f551288671c335fdc90d73 |
| Draft revision | 1 |
| Submitted content hash | cb2e36efa4678c13c74db9c35b2a2b690eca80dccba56f9f4653887e076fa4f4 |
| Approval option | approve_complete_plan |
| Option ID | opt_a9f6fb26c21a74ff896397674aaf9c41 |

Original submission evidence is the Mac result branch at
`b9304597937b4d7307f2ea195537e4b48418ebe2`; current read-only correction and schema
evidence are at `87d1f8144f6c3165137d80f4c382567d36527e6d`. Exact result records are retained under
`docs/evidence/mac-helper/`. Root reconciliation verifies that all 218 canonical
tasks map to unique new native task IDs, all 26 waves map uniquely, and none of
those new task IDs replaces the twelve frozen historical identities. The
canonical graph contains 424 edges. The authenticated helper reports exact
native field/edge/wave readback and unchanged historical tasks.

The root now records the returned IDs in `project-plan.json`. The earlier
submitted body remains bound to its original reviewed-input snapshot; later
canonical reconciliation does not mutate or approve that frozen submission.
RE-MAC-003 revision 1 is held. Reuse these native IDs before any authorized
revision; never create another batch of 218 tasks to retry the work.

## Actual gaps

Current RE-MAC-005 readback at 2026-09-08T13:55Z reports FAILED for all
218 mapped task reviews. The tasks remain SUBMITTED and the proposal remains
DISCUSSION with zero votes. Failure cause, current attempt and supported recovery
action are not exposed. The earlier PENDING/disabled result is a historical
checkpoint, not current reviewer configuration. No passing review or publication
is established.

All 218 snapshots have null structured `planningRequirements`. The new sample is
INCOMPLETE/MISSING and the historical sample is COMPLETE. The exact exposed
schemas, optional/required fields, restrictions and unknown deployed limits are
retained in `docs/evidence/mac-helper/results/RE-MAC-005/r1.json`. Missing fields
are not established as the reason for FAILED. Candidate-source review rules are
explicitly separated from deployed policy, which remains unknown from live reads.

Obtain the actual failure detail and supported maintainer recovery action before
any retry. Do not invent a retry endpoint, unfreeze/resubmit the draft, create
replacement tasks, infer a vote, or edit Tanduna's separate application/config.
RE-MAC-003 stays HOLD. RE-MAC-005 performed read-only inspection and grants no
additional mutation authority. The Mac's native scheduled firing is now verified.

Current unauthenticated readback still shows twelve historical task IDs on the
roadmap/tasks pages. The new proposal URL returns HTTP 404 anonymously. The
helper's authenticated draft evidence must not be presented as public access.

## Human evidence remains separate

Mac arm64 CPython 3.14.6 successfully installed the public package, inspected the
fixture, preserved original bytes and reopened saved evidence; the reports were
opened in Chrome. These are partial Mac agent runtime observations. Linux demo
and recovery were not run in that Mac session; their external Linux evidence
remains separately retained.

A limited report-review approval was reported by the participant. No independent
human negative-control diagnosis or complete performed-step record has been
provided. Do not call that full USER VALIDATED, infer a native poll vote from it,
or ask the participant to repeat an approval already received. The outstanding
Mac question requests the missing actual observations.
