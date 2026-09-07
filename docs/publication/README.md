# Native plan publication handoff

`tanduna-plan-export.json` is generated from the canonical ledger for review and supported import/manual entry. It is **not an asserted Tanduna API schema**, an accepted proposal, a public task collection, or proof of publication. No platform write is performed by the planning tool.

The September 7 saved public pages expose project `prj_9ef51e9826817323b774d5d3b900520f`, repository connection `repo_ee03f828c0ad9fee23ad67dd857b2d12`, and approved founding proposal `prp_7b37b259ab06edc6c724198400d4fc62`. The task page lists all 12 source IDs as READY, revision 3; the proposals page shows one historical approved proposal and nothing open. The saved task/proposal pages expose no pagination links. The frozen snapshot hash is `d09143e713849a2c76cd094a97971d8d325efe091f87a180ee5be89a8d0c26e8`. These observations establish textual plan identity, not executed work or current write authority.

Before any authorized publication, freshly resolve the identity and complete current inventory from:

- [Project](https://tanduna.com/projects/renewal-engine)
- [Published roadmap](https://tanduna.com/projects/renewal-engine/roadmap)
- [Tasks](https://tanduna.com/p/renewal-engine/tasks), including all pages and task briefs
- [Proposals](https://tanduna.com/p/renewal-engine/proposals), including any new open or accepted revisions

Use supported platform tools and the actual revision/proposal/import workflow. Preserve frozen records. A new dated proposal, a zero-ballot option, a successful request or a local artifact does not establish acceptance. If the platform cannot represent the proposed waves or fields, document that exact capability gap and provide the export for a supported manual path. Do not invent endpoints or replace the required native plan with a link to GitHub.

The export contains task IDs, outcomes, feature areas, release horizons, prerequisites and their needed outcomes, falsifiable acceptance, source and decision references, risk/evidence needs, evidence status, wave entry/exit dependencies, the separate narrow critical path and original-to-successor mappings. New task `platformId` values are null until returned by the platform. The `publication.newPlatformMappings` object is the place to reconcile returned stable IDs in canonical state; generated files must then be refreshed. Do not create a second status ledger here.

Prepare the concrete publication decision only after the local candidate and exact export are reviewable: account, destination, revision scope, diff/artifact digest, data exposure, cost, reversibility and remaining risks. Existing credentials do not themselves authorize publication. Use prior exact owner authorization when present.

Release access instructions in the initial export are explicitly unavailable pending actual packaged verification and authorized release. Before publishing final 0.1 access instructions, fill canonical `release.publicVersion`, `release.publicUrl` and `release.accessInstructions` from the actual public artifact and tested command names. Do not infer usable commands from a proposed design or present development-checkout instructions as an externally obtained release.

After publication, read back public project identity, accepted plan revision/content hash, wave order, task counts and release horizons, prerequisite links, honest evidence states and exact 0.1 access instructions. Compare every returned task to its canonical stable ID; reconcile partial success before retrying. Retain the returned IDs and read-back evidence in canonical state. Only successful public verification can advance publication evidence; unaccepted or stale native content keeps the Goal unfinished.

## Observed connection gate

The public guide at https://tanduna.com/guide/connect-through-mcp documents
`https://tanduna.com/api/mcp`, including task-plan draft/get/submit and published
plan listing tools. It requires owner sign-in on the same computer as the
browser through the supported helper; direct Codex MCP OAuth is marked
unavailable. This task exposes no connected Tanduna tools. No login helper,
credential copying, hidden endpoint, direct database write or platform mutation
was attempted. A public guide capture is retained in docs/references. Use a
supported authenticated owner session and obtain the concrete publication
decision before submitting this export. A submitted plan still needs review
and approval of its exact poll option; authentication is not publication authority.
