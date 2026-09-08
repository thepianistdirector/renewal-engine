# Mac request-file protocol, version 1

This is an execution handoff, not another project roadmap. The remote project
owner remains responsible for its canonical plan and completion claims. Mac
results supply evidence; they do not silently change task acceptance or status.

## Files and ownership

The initial feed is `coordination/mac/requests.json` on branch
`codex/renewal-engine-0.1` in `thepianistdirector/renewal-engine`.
The Mac writes `coordination/mac/registration.json` and
`coordination/mac/results/<request-id>/r<revision>.json` on branch
`codex/mac-helper-results`. The remote owner reads that branch and reconciles
results into `project-plan.json`. Neither side edits the other side's files.

A helper may keep several explicitly approved feeds in its private local
registry. Each feed gets its own repository/project binding and allowed result
paths. A new feed or arbitrary file text cannot grant itself authority. Only
public-safe material belongs in this public repository; use a separately
approved private transport for private requests and evidence.

Request IDs use letters, digits and hyphens only. Revisions are positive integers.
Dependencies identify request IDs in this feed. Cross-feed work requires an
explicit reference and approved project binding. A changed task increments its
revision; it does not erase a prior result. Requests can be READY, HOLD or
CANCELLED. Completion belongs in the result, not in a Mac edit to requests.json.

Fetch the current branch before considering a request. Record the fetched commit
when available and the request document's SHA-256. Validate reference hashes for
immutable review inputs; if the canonical plan has changed, return STALE_INPUT
with the observed digest and ask the owner for the next revision rather than
silently publishing a different plan.

Use local atomic writes and a single-worker lock tied to an actual live process
or tool handle. An interrupted action must first be reconciled against its
external state. Use existing native IDs and file versions to avoid duplicate
proposals, result commits, votes or uploads. Do not force-push or reset user work.

## Result schema

Create a JSON object with these fields. This is the bridge's schema, not a claim
about Tanduna or Codex native tool schemas:

```json
{
  "schemaVersion": 1,
  "project": "renewal-engine",
  "requestId": "RE-MAC-001",
  "requestRevision": 1,
  "requestDocumentSha256": "actual fetched digest",
  "sourceCommit": "actual fetched commit if known",
  "status": "NEEDS_LUCAS",
  "evidenceLevel": "NOT TESTED",
  "startedAt": "actual ISO timestamp",
  "updatedAt": "actual ISO timestamp",
  "helper": {"hostKind": "macOS", "model": "actual verified model"},
  "summary": "What was actually done or observed",
  "checks": [],
  "publicEvidence": [],
  "nativeIds": {},
  "userAction": "One specific missing action, or null",
  "limitations": [],
  "humanObservation": null
}
```

Statuses: RUNNING, SUCCEEDED, PARTIAL, NEEDS_LUCAS, WAITING_REVIEW,
STALE_INPUT, FAILED or CANCELLED. Use evidence levels matching what occurred:
IMPLEMENTED, AUTOMATED PASS, RUNTIME VERIFIED, USER VALIDATED, RELEASE VERIFIED
or NOT TESTED. A successful setup may still leave a different request blocked.
Never use USER VALIDATED solely for an agent's execution or opinion.

Checks record actions, actual outcomes and evidence references. Public evidence
must contain no credentials, private paths or unconsented identifying participant
data. Native IDs must be returned by actual tools. A humanObservation is null
until a consenting person has performed the relevant steps; then record the
consented, public-safe summary, qualification, scope, assistance and limitations.

If the result branch cannot be written, retain the local result and surface that
specific synchronization failure once. Do not lose completed work or claim that
the remote owner has received evidence merely because a local file exists.

## First-run registration

Registration records actual setup status, helper task identity if available,
model verification basis, scheduling tool/ID, interval, enabled state, next run,
local-host binding and supported kinds. Do not store tokens or absolute home
paths. Mark scheduling NOT TESTED/BLOCKED if creation/readback is unavailable.
A Markdown file describing a timer is not proof that a native scheduled task
exists.

No-change cycles remain quiet. Continue processing other independent requests
while a request waits for Lucas. Retry a blocked request when its input, authority,
capability or user response changes, not simply because another 15 minutes passed.
