# Renewal Engine roadmap

Generated from `project-plan.json` by `python3 tools/plan.py generate`. Do not edit this view. Canonical SHA-256: `a54c8244c34f33ccf42129ff8437c65fffe010ea5b9f99d792ea64ab14390eb1`.

Public 0.1.0 and fresh external runtime reproduction verified; human review and native Tanduna publication pending

218 outcome tasks in 26 waves. 0.1: 50; later 0.x: 72; long-term: 80; exploratory: 16.

The 12 historical contracts remain immutable in [lineage](docs/lineage/2026-09-07). Their original graph is separate from the new narrow 0.1 path. Later outcomes require accepted scope and evidence; exploratory options are not promised delivery.

## Narrow 0.1 path

This is a new narrow 0.1 dependency path. Historical W1–W6 edges remain frozen in sourceMappings and lineage; later recipe kits, data migrations and pilot programmes are not silently treated as complete.

RE-W01 → RE-W02 → RE-W03 → RE-W04 → RE-W05

## Release access and unresolved decisions

Download renewal-engine-0.1.0.tar.gz and SHA256SUMS from the versioned GitHub release, verify the digest, extract and follow README. Linux x86_64 CPython 3.11.16 and 3.12.14 are supplied separately. Public asset hashes and installed example verification passed anonymously. Fresh external reproduction passed on a GitHub-hosted Ubuntu 24.04 x86_64 runner using the anonymously downloaded artifact and both official-source pinned runtimes; human validation and native Tanduna publication remain unfinished.

- **D01 · APPROVED:** Owner approved the prepared original AGPL-3.0 ConfigParser fixture September 8, 2026, as narrow 0.1 scope. Original W1-T1 maintained-upstream acceptance remains unchanged and incomplete.
- **D02 · APPROVED:** Owner approved actual CPython 3.11.16 / 3.12.14 comparison September 8. Both identities and actual packaged normal/negative and restart observations are retained.
- **D03 · APPROVED:** Owner explicitly approved publication September 8. Exact commit 737dc0867d5b4e6c8f3ba29f04fade8573ff683d tagged v0.1.0 and published with the approved CLI/source/checksum assets.
- **D04 · UNRESOLVED:** Authorize concrete native Tanduna revision/proposal publication after supported workflow discovery and export review.

## Outcome waves

### RE-W01 — A migration has a precise behavioral promise

**Horizon:** 0.1. **Basis:** proposal.

**Outcome:** A migration has a precise behavioral promise.

**Entry dependencies:** None; exact cut still requires owner decisions.

**Assigned outcomes:**

- `renewal-engine:N01-01` — Ratify the ConfigParser cut (IMPLEMENTED)
- `renewal-engine:N01-02` — Resolve lawful fixture provenance (IMPLEMENTED)
- `renewal-engine:N01-03` — Pin the actual baseline interpreter (RUNTIME VERIFIED)
- `renewal-engine:N01-04` — Approve the modern runtime (RUNTIME VERIFIED)
- `renewal-engine:N01-05` — Declare unchanged behavior (IMPLEMENTED)
- `renewal-engine:N01-06` — Freeze intentional changes (RUNTIME VERIFIED)
- `renewal-engine:N01-07` — Define inspection authority (AUTOMATED PASS)
- `renewal-engine:N01-08` — Choose the supported Linux environment (RUNTIME VERIFIED)
- `renewal-engine:N01-09` — Approve the narrow architecture (IMPLEMENTED)
- `renewal-engine:N01-10` — Accept the 0.1 execution contract (IMPLEMENTED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N01-01 through renewal-engine:N01-10. An unapproved cut or unavailable interpreter invalidates runtime claims. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W02 — Original behavior is observable

**Horizon:** 0.1. **Basis:** proposal.

**Outcome:** Original behavior is observable.

**Entry dependencies:** renewal-engine:N01-10

**Assigned outcomes:**

- `renewal-engine:N02-01` — Define trusted case envelopes (RUNTIME VERIFIED)
- `renewal-engine:N02-02` — Capture valid and Unicode INI behavior (RUNTIME VERIFIED)
- `renewal-engine:N02-03` — Capture duplicate-section failures (RUNTIME VERIFIED)
- `renewal-engine:N02-04` — Capture malformed-input failures (RUNTIME VERIFIED)
- `renewal-engine:N02-05` — Capture source-name semantics (RUNTIME VERIFIED)
- `renewal-engine:N02-06` — Capture interpolation behavior (RUNTIME VERIFIED)
- `renewal-engine:N02-07` — Capture stream and file effects (RUNTIME VERIFIED)
- `renewal-engine:N02-08` — Record baseline observations (RUNTIME VERIFIED)
- `renewal-engine:N02-09` — Expose measurement limits (IMPLEMENTED)
- `renewal-engine:N02-10` — Seal characterization evidence (RUNTIME VERIFIED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N02-01 through renewal-engine:N02-10. Incomplete characterization can make a broken migration appear correct. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W03 — Supported code is transformed conservatively

**Horizon:** 0.1. **Basis:** proposal.

**Outcome:** Supported code is transformed conservatively.

**Entry dependencies:** renewal-engine:N02-10

**Assigned outcomes:**

- `renewal-engine:N03-01` — Inventory syntax and bindings (IMPLEMENTED)
- `renewal-engine:N03-02` — Recognize direct ConfigParser construction (AUTOMATED PASS)
- `renewal-engine:N03-03` — Refuse shadowed or rebound receivers (AUTOMATED PASS)
- `renewal-engine:N03-04` — Refuse unsupported call signatures (AUTOMATED PASS)
- `renewal-engine:N03-05` — Preserve source-name arguments (RUNTIME VERIFIED)
- `renewal-engine:N03-06` — Apply bounded source-span edits (AUTOMATED PASS)
- `renewal-engine:N03-07` — Create a separate candidate copy (RUNTIME VERIFIED)
- `renewal-engine:N03-08` — Emit a deterministic focused patch (RUNTIME VERIFIED)
- `renewal-engine:N03-09` — Explain repeat application (RUNTIME VERIFIED)
- `renewal-engine:N03-10` — Verify the conservative recipe boundary (IMPLEMENTED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N03-01 through renewal-engine:N03-10. Binding mistakes or imprecise spans can rewrite unrelated behavior. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W04 — Wrong transformations fail independently

**Horizon:** 0.1. **Basis:** proposal.

**Outcome:** Wrong transformations fail independently.

**Entry dependencies:** renewal-engine:N03-10

**Assigned outcomes:**

- `renewal-engine:N04-01` — Bind runs to immutable identities (IMPLEMENTED)
- `renewal-engine:N04-02` — Execute only the trusted reference (IMPLEMENTED)
- `renewal-engine:N04-03` — Scrub the execution environment (AUTOMATED PASS)
- `renewal-engine:N04-04` — Bound process lifetime and output (IMPLEMENTED)
- `renewal-engine:N04-05` — Retain raw structured observations (RUNTIME VERIFIED)
- `renewal-engine:N04-06` — Compare unchanged behavior strictly (RUNTIME VERIFIED)
- `renewal-engine:N04-07` — Apply the frozen expected-change policy (RUNTIME VERIFIED)
- `renewal-engine:N04-08` — Reject a deliberately wrong candidate (RUNTIME VERIFIED)
- `renewal-engine:N04-09` — Report incomplete evidence honestly (IMPLEMENTED)
- `renewal-engine:N04-10` — Verify real old/new differential execution (RUNTIME VERIFIED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N04-01 through renewal-engine:N04-10. A self-fulfilling comparator or unsafe execution can invalidate all evidence. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W05 — A maintainer can obtain and review the result

**Horizon:** 0.1. **Basis:** proposal.

**Outcome:** A maintainer can obtain and review the result.

**Entry dependencies:** renewal-engine:N04-10

**Assigned outcomes:**

- `renewal-engine:N05-01` — Generate one evidence-backed review report (RUNTIME VERIFIED)
- `renewal-engine:N05-02` — Make the report accessible offline (IMPLEMENTED)
- `renewal-engine:N05-03` — Persist attempts atomically (RUNTIME VERIFIED)
- `renewal-engine:N05-04` — Provide a safe restart workflow (RUNTIME VERIFIED)
- `renewal-engine:N05-05` — Build an installable local distribution (RUNTIME VERIFIED)
- `renewal-engine:N05-06` — Verify first-run and limitation instructions (IMPLEMENTED)
- `renewal-engine:N05-07` — Prepare a lawful release candidate (IMPLEMENTED)
- `renewal-engine:N05-08` — Publish and read back versioned 0.1 (RELEASE VERIFIED)
- `renewal-engine:N05-09` — Obtain external maintainer evidence (IN PROGRESS)
- `renewal-engine:N05-10` — Publish and verify the native Tanduna plan (BLOCKED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N05-01 through renewal-engine:N05-10. Local implementation does not prove external use, accessibility or public release. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W06 — Recipe inputs are explicit

**Horizon:** later 0.x. **Basis:** proposal.

**Outcome:** Recipe inputs are explicit.

**Entry dependencies:** renewal-engine:N05-10

**Assigned outcomes:**

- `renewal-engine:N06-01` — Version recipe contracts (PLANNED)
- `renewal-engine:N06-02` — Express runtime ranges (PLANNED)
- `renewal-engine:N06-03` — Declare syntax preconditions (PLANNED)
- `renewal-engine:N06-04` — Declare effect coverage (PLANNED)
- `renewal-engine:N06-05` — Declare expected-change policy ownership (PLANNED)
- `renewal-engine:N06-06` — Distribute negative fixtures with recipes (PLANNED)
- `renewal-engine:N06-07` — Define contract upgrade compatibility (PLANNED)
- `renewal-engine:N06-08` — Validate a complete recipe envelope (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N06-01 through renewal-engine:N06-08. Recipe contracts can drift from their actual supported domain. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W07 — More Python API migrations are defensible

**Horizon:** later 0.x. **Basis:** proposal.

**Outcome:** More Python API migrations are defensible.

**Entry dependencies:** renewal-engine:N06-08

**Assigned outcomes:**

- `renewal-engine:N07-01` — Prioritize Python migration demand (PLANNED)
- `renewal-engine:N07-02` — Clear the second fixture rights (PLANNED)
- `renewal-engine:N07-03` — Characterize a second API contract (PLANNED)
- `renewal-engine:N07-04` — Prove the second recipe transformation (PLANNED)
- `renewal-engine:N07-05` — Measure combined recipe interactions (PLANNED)
- `renewal-engine:N07-06` — Control recipe selection (PLANNED)
- `renewal-engine:N07-07` — Bound Python support claims (PLANNED)
- `renewal-engine:N07-08` — Review second-recipe external usefulness (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N07-01 through renewal-engine:N07-08. Recipe expansion can imply unsafe general Python modernization. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W08 — Dependency changes have inspectable impact

**Horizon:** later 0.x. **Basis:** proposal.

**Outcome:** Dependency changes have inspectable impact.

**Entry dependencies:** renewal-engine:N06-08

**Assigned outcomes:**

- `renewal-engine:N08-01` — Map declared dependencies (PLANNED)
- `renewal-engine:N08-02` — Trace imported symbols (PLANNED)
- `renewal-engine:N08-03` — Map configuration entry points (PLANNED)
- `renewal-engine:N08-04` — Identify public interface exposure (PLANNED)
- `renewal-engine:N08-05` — Represent uncertainty in impact maps (PLANNED)
- `renewal-engine:N08-06` — Connect edits to migration requirements (PLANNED)
- `renewal-engine:N08-07` — Expose transitive dependency effects (PLANNED)
- `renewal-engine:N08-08` — Validate the impact inventory against a fixture (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N08-01 through renewal-engine:N08-08. Static impact maps can omit configuration and dynamically selected interfaces. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W09 — Characterization covers richer effects

**Horizon:** later 0.x. **Basis:** proposal.

**Outcome:** Characterization covers richer effects.

**Entry dependencies:** renewal-engine:N06-08

**Assigned outcomes:**

- `renewal-engine:N09-01` — Define bounded filesystem observations (PLANNED)
- `renewal-engine:N09-02` — Capture file creation and deletion (PLANNED)
- `renewal-engine:N09-03` — Capture serialized data contracts (PLANNED)
- `renewal-engine:N09-04` — Capture protocol transcripts locally (PLANNED)
- `renewal-engine:N09-05` — Capture process exit behavior (PLANNED)
- `renewal-engine:N09-06` — Observe resource lifecycle effects (PLANNED)
- `renewal-engine:N09-07` — Control sensitive evidence retention (PLANNED)
- `renewal-engine:N09-08` — Validate observer independence (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N09-01 through renewal-engine:N09-08. Rich observations risk leaking private data or missing destructive effects. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W10 — Nondeterminism is not hidden

**Horizon:** later 0.x. **Basis:** proposal.

**Outcome:** Nondeterminism is not hidden.

**Entry dependencies:** renewal-engine:N09-08

**Assigned outcomes:**

- `renewal-engine:N10-01` — Detect repeated-run variance (PLANNED)
- `renewal-engine:N10-02` — Declare timestamp normalization (PLANNED)
- `renewal-engine:N10-03` — Declare random-input reproducibility (PLANNED)
- `renewal-engine:N10-04` — Preserve meaningful ordering (PLANNED)
- `renewal-engine:N10-05` — Separate locale and encoding variance (PLANNED)
- `renewal-engine:N10-06` — Bound tolerance policies (PLANNED)
- `renewal-engine:N10-07` — Audit normalization changes (PLANNED)
- `renewal-engine:N10-08` — Expose unresolved variance to users (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N10-01 through renewal-engine:N10-08. Overbroad normalization can erase genuine regressions. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W11 — Review survives concurrent source changes

**Horizon:** later 0.x. **Basis:** proposal.

**Outcome:** Review survives concurrent source changes.

**Entry dependencies:** renewal-engine:N08-08

**Assigned outcomes:**

- `renewal-engine:N11-01` — Identify the patch application base (PLANNED)
- `renewal-engine:N11-02` — Detect concurrent candidate modification (PLANNED)
- `renewal-engine:N11-03` — Explain conflicting hunks (PLANNED)
- `renewal-engine:N11-04` — Preserve unrelated local edits (PLANNED)
- `renewal-engine:N11-05` — Support selective change rejection (PLANNED)
- `renewal-engine:N11-06` — Recharacterize an updated source base (PLANNED)
- `renewal-engine:N11-07` — Bind approvals to exact artifacts (PLANNED)
- `renewal-engine:N11-08` — Rehearse conflict recovery (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N11-01 through renewal-engine:N11-08. A valid patch can become unsafe when its source base changes. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W12 — Private operation is verifiable

**Horizon:** later 0.x. **Basis:** proposal.

**Outcome:** Private operation is verifiable.

**Entry dependencies:** renewal-engine:N05-10

**Assigned outcomes:**

- `renewal-engine:N12-01` — Inventory local data flows (PLANNED)
- `renewal-engine:N12-02` — Prove offline default behavior (PLANNED)
- `renewal-engine:N12-03` — Constrain diagnostic logging (PLANNED)
- `renewal-engine:N12-04` — Separate raw and shareable evidence (PLANNED)
- `renewal-engine:N12-05` — Require explicit provider scope (PLANNED)
- `renewal-engine:N12-06` — Enforce workspace boundaries (PLANNED)
- `renewal-engine:N12-07` — Support private artifact cleanup (PLANNED)
- `renewal-engine:N12-08` — Audit the privacy boundary end to end (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N12-01 through renewal-engine:N12-08. Local processing alone does not establish every data boundary. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W13 — Maintainers author independent recipes

**Horizon:** later 0.x. **Basis:** proposal.

**Outcome:** Maintainers author independent recipes.

**Entry dependencies:** renewal-engine:N06-08, renewal-engine:N07-08

**Assigned outcomes:**

- `renewal-engine:N13-01` — Publish an authoring contract (PLANNED)
- `renewal-engine:N13-02` — Provide a minimal recipe example (PLANNED)
- `renewal-engine:N13-03` — Expose a conformance runner (PLANNED)
- `renewal-engine:N13-04` — Document reviewable edit rules (PLANNED)
- `renewal-engine:N13-05` — Package contributor evidence (PLANNED)
- `renewal-engine:N13-06` — Support independent recipe maintenance (PLANNED)
- `renewal-engine:N13-07` — Observe a second maintainer authoring (PLANNED)
- `renewal-engine:N13-08` — Close authoring gaps from observation (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N13-01 through renewal-engine:N13-08. A kit that only its author can use is not an independent contribution interface. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W14 — Runtime isolation is enforceable

**Horizon:** later 0.x. **Basis:** proposal.

**Outcome:** Runtime isolation is enforceable.

**Entry dependencies:** renewal-engine:N12-08

**Assigned outcomes:**

- `renewal-engine:N14-01` — Define execution threat boundaries (PLANNED)
- `renewal-engine:N14-02` — Select an approved isolation backend (PLANNED)
- `renewal-engine:N14-03` — Deny host filesystem escape (PLANNED)
- `renewal-engine:N14-04` — Deny unauthorized network access (PLANNED)
- `renewal-engine:N14-05` — Constrain descendants and resource use (PLANNED)
- `renewal-engine:N14-06` — Exclude inherited credentials (PLANNED)
- `renewal-engine:N14-07` — Expose isolation profile limitations (PLANNED)
- `renewal-engine:N14-08` — Admit approved arbitrary-repository execution (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N14-01 through renewal-engine:N14-08. A subprocess is not a sandbox; untrusted execution requires denial evidence. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W15 — Additional languages retain semantics

**Horizon:** exploratory. **Basis:** exploratory.

**Outcome:** Additional languages retain semantics.

**Entry dependencies:** renewal-engine:N13-08, renewal-engine:N14-08

**Assigned outcomes:**

- `renewal-engine:N15-01` — Choose a language from demonstrated demand (PLANNED)
- `renewal-engine:N15-02` — Assess parser fidelity (PLANNED)
- `renewal-engine:N15-03` — Define symbol attribution rules (PLANNED)
- `renewal-engine:N15-04` — Define language-specific behavior observations (PLANNED)
- `renewal-engine:N15-05` — Review adapter dependencies and rights (PLANNED)
- `renewal-engine:N15-06` — Prove a bounded first foreign-language recipe (PLANNED)
- `renewal-engine:N15-07` — Integrate heterogeneous reports (PLANNED)
- `renewal-engine:N15-08` — Decide whether to support the new language (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N15-01 through renewal-engine:N15-08. Language breadth is exploratory and cannot inherit Python safety claims. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W16 — Framework migrations expose intentional changes

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** Framework migrations expose intentional changes.

**Entry dependencies:** renewal-engine:N08-08, renewal-engine:N09-08, renewal-engine:N13-08

**Assigned outcomes:**

- `renewal-engine:N16-01` — Select a bounded framework transition (PLANNED)
- `renewal-engine:N16-02` — Map framework configuration changes (PLANNED)
- `renewal-engine:N16-03` — Characterize lifecycle ordering (PLANNED)
- `renewal-engine:N16-04` — Characterize framework error handling (PLANNED)
- `renewal-engine:N16-05` — Declare intentional framework changes (PLANNED)
- `renewal-engine:N16-06` — Generate a staged framework patch (PLANNED)
- `renewal-engine:N16-07` — Measure old/new framework behavior (PLANNED)
- `renewal-engine:N16-08` — Review framework migration limits (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N16-01 through renewal-engine:N16-08. Framework upgrades can change lifecycle and configuration beyond API spelling. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W17 — Connected systems migrate in a safe order

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** Connected systems migrate in a safe order.

**Entry dependencies:** renewal-engine:N13-08, renewal-engine:N14-08, renewal-engine:N16-08

**Assigned outcomes:**

- `renewal-engine:N17-01` — Represent independently deployed components (PLANNED)
- `renewal-engine:N17-02` — Model compatibility edges (PLANNED)
- `renewal-engine:N17-03` — Derive safe partial orders (PLANNED)
- `renewal-engine:N17-04` — Define compatibility windows (PLANNED)
- `renewal-engine:N17-05` — Detect unsafe rollout order (PLANNED)
- `renewal-engine:N17-06` — Rehearse partial deployment failure (PLANNED)
- `renewal-engine:N17-07` — Require evidence before advancing stages (PLANNED)
- `renewal-engine:N17-08` — Validate staged modernization with a maintainer (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N17-01 through renewal-engine:N17-08. Individually valid migrations may fail during mixed-version deployment. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W18 — Data changes have their own recovery contract

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** Data changes have their own recovery contract.

**Entry dependencies:** renewal-engine:N17-08

**Assigned outcomes:**

- `renewal-engine:N18-01` — Choose a disposable data migration (PLANNED)
- `renewal-engine:N18-02` — Define data invariants (PLANNED)
- `renewal-engine:N18-03` — Verify a restorable backup (PLANNED)
- `renewal-engine:N18-04` — Model schema and application compatibility (PLANNED)
- `renewal-engine:N18-05` — Persist data-step checkpoints (PLANNED)
- `renewal-engine:N18-06` — Rehearse interrupted data recovery (PLANNED)
- `renewal-engine:N18-07` — Expose irreversible operations (PLANNED)
- `renewal-engine:N18-08` — Validate the bounded data recovery claim (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N18-01 through renewal-engine:N18-08. Source rollback cannot restore irreversible data effects. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W19 — Rollback instructions match actual state

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** Rollback instructions match actual state.

**Entry dependencies:** renewal-engine:N18-08

**Assigned outcomes:**

- `renewal-engine:N19-01` — Identify rollback state domains (PLANNED)
- `renewal-engine:N19-02` — Bind recovery to observed versions (PLANNED)
- `renewal-engine:N19-03` — Restore approved source revisions (PLANNED)
- `renewal-engine:N19-04` — Restore compatible data and schema (PLANNED)
- `renewal-engine:N19-05` — Represent external-effect compensation (PLANNED)
- `renewal-engine:N19-06` — Handle failed recovery steps (PLANNED)
- `renewal-engine:N19-07` — Rehearse rollback decision points (PLANNED)
- `renewal-engine:N19-08` — Validate recovery instructions independently (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N19-01 through renewal-engine:N19-08. A rollback instruction can itself cause damage when its assumptions are stale. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W20 — Regression evidence persists across releases

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** Regression evidence persists across releases.

**Entry dependencies:** renewal-engine:N10-08, renewal-engine:N11-08

**Assigned outcomes:**

- `renewal-engine:N20-01` — Version retained observation schemas (PLANNED)
- `renewal-engine:N20-02` — Identify evidence by content (PLANNED)
- `renewal-engine:N20-03` — Link candidate generations (PLANNED)
- `renewal-engine:N20-04` — Retain unsuccessful attempts (PLANNED)
- `renewal-engine:N20-05` — Record last-verified versions (PLANNED)
- `renewal-engine:N20-06` — Migrate report storage safely (PLANNED)
- `renewal-engine:N20-07` — Define retention and pruning rules (PLANNED)
- `renewal-engine:N20-08` — Reproduce a historical regression (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N20-01 through renewal-engine:N20-08. Historical evidence can silently drift or become unreadable. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W21 — CI consumers use the same comparison

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** CI consumers use the same comparison.

**Entry dependencies:** renewal-engine:N14-08, renewal-engine:N20-08

**Assigned outcomes:**

- `renewal-engine:N21-01` — Define CI invocation inputs (PLANNED)
- `renewal-engine:N21-02` — Separate inspection from execution jobs (PLANNED)
- `renewal-engine:N21-03` — Key caches to complete identities (PLANNED)
- `renewal-engine:N21-04` — Emit machine-readable gate results (PLANNED)
- `renewal-engine:N21-05` — Publish review artifacts without secrets (PLANNED)
- `renewal-engine:N21-06` — Keep adoption under maintainer control (PLANNED)
- `renewal-engine:N21-07` — Handle interrupted CI attempts (PLANNED)
- `renewal-engine:N21-08` — Verify one supported CI environment (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N21-01 through renewal-engine:N21-08. CI convenience can introduce unauthorized execution or different comparison semantics. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W22 — Optional assistance remains a proposal

**Horizon:** exploratory. **Basis:** exploratory.

**Outcome:** Optional assistance remains a proposal.

**Entry dependencies:** renewal-engine:N12-08, renewal-engine:N13-08

**Assigned outcomes:**

- `renewal-engine:N22-01` — Define the assistance use case (PLANNED)
- `renewal-engine:N22-02` — Specify provider input boundaries (PLANNED)
- `renewal-engine:N22-03` — Require per-scope provider authorization (PLANNED)
- `renewal-engine:N22-04` — Isolate suggestions from accepted recipes (PLANNED)
- `renewal-engine:N22-05` — Validate model output as untrusted data (PLANNED)
- `renewal-engine:N22-06` — Compare assisted proposals independently (PLANNED)
- `renewal-engine:N22-07` — Measure assistance value and cost (PLANNED)
- `renewal-engine:N22-08` — Decide assistance support from evidence (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N22-01 through renewal-engine:N22-08. Model suggestions can leak private code or be mistaken for verified migrations. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W23 — A maintained catalog stays trustworthy

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** A maintained catalog stays trustworthy.

**Entry dependencies:** renewal-engine:N13-08, renewal-engine:N20-08

**Assigned outcomes:**

- `renewal-engine:N23-01` — Assign recipe stewardship (PLANNED)
- `renewal-engine:N23-02` — Publish compatibility evidence (PLANNED)
- `renewal-engine:N23-03` — Detect dependency invalidation (PLANNED)
- `renewal-engine:N23-04` — Define recipe deprecation (PLANNED)
- `renewal-engine:N23-05` — Respond to recipe safety advisories (PLANNED)
- `renewal-engine:N23-06` — Review catalog contributions (PLANNED)
- `renewal-engine:N23-07` — Track unresolved coverage gaps (PLANNED)
- `renewal-engine:N23-08` — Rehearse stewardship continuity (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N23-01 through renewal-engine:N23-08. Unowned recipes and stale compatibility claims erode catalog trust. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W24 — Volunteer maintainers test real usefulness

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** Volunteer maintainers test real usefulness.

**Entry dependencies:** renewal-engine:N19-08, renewal-engine:N23-08

**Assigned outcomes:**

- `renewal-engine:N24-01` — Recruit consented pilot participants (PLANNED)
- `renewal-engine:N24-02` — Select representative pilot migrations (PLANNED)
- `renewal-engine:N24-03` — Capture pre-migration maintainer expectations (PLANNED)
- `renewal-engine:N24-04` — Submit patches through ordinary review (PLANNED)
- `renewal-engine:N24-05` — Record accepted rejected and revised outcomes (PLANNED)
- `renewal-engine:N24-06` — Reproduce behavior missed by the tool (PLANNED)
- `renewal-engine:N24-07` — Measure review burden (PLANNED)
- `renewal-engine:N24-08` — Decide pilot-driven priorities (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N24-01 through renewal-engine:N24-08. Generated patches and simulated reviews do not establish adoption. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W25 — Review interfaces support varied users

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** Review interfaces support varied users.

**Entry dependencies:** renewal-engine:N20-08, renewal-engine:N24-08

**Assigned outcomes:**

- `renewal-engine:N25-01` — Design evidence navigation around maintainer decisions (PLANNED)
- `renewal-engine:N25-02` — Provide accessible diff semantics (PLANNED)
- `renewal-engine:N25-03` — Support keyboard-only review controls (PLANNED)
- `renewal-engine:N25-04` — Handle narrow screens and high zoom (PLANNED)
- `renewal-engine:N25-05` — Make diagnostic language actionable (PLANNED)
- `renewal-engine:N25-06` — Prepare localization without changing evidence (PLANNED)
- `renewal-engine:N25-07` — Respect motion and contrast preferences (PLANNED)
- `renewal-engine:N25-08` — Validate review accessibility with varied users (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N25-01 through renewal-engine:N25-08. Automated checks alone miss human comprehension and accessibility barriers. Retain failing and unrun evidence; require the named human or runtime observation where specified.

### RE-W26 — The tool can be operated sustainably

**Horizon:** long-term. **Basis:** proposal.

**Outcome:** The tool can be operated sustainably.

**Entry dependencies:** renewal-engine:N21-08, renewal-engine:N23-08, renewal-engine:N25-08

**Assigned outcomes:**

- `renewal-engine:N26-01` — Define supported release policy (PLANNED)
- `renewal-engine:N26-02` — Make release builds reproducible (PLANNED)
- `renewal-engine:N26-03` — Preserve upgrade compatibility (PLANNED)
- `renewal-engine:N26-04` — Provide a vulnerability reporting path (PLANNED)
- `renewal-engine:N26-05` — Budget runtime and storage costs (PLANNED)
- `renewal-engine:N26-06` — Plan failure and recovery operations (PLANNED)
- `renewal-engine:N26-07` — Audit long-term dependency health (PLANNED)
- `renewal-engine:N26-08` — Review sustainable project stewardship (PLANNED)

**Exit evidence:** Criterion-level acceptance records for renewal-engine:N26-01 through renewal-engine:N26-08. Release operations can overpromise compatibility and outgrow maintainer capacity. Retain failing and unrun evidence; require the named human or runtime observation where specified.

## Publication boundary

A local export is not an accepted or published native plan. Refresh all public pages before an authorized platform write and reconcile returned IDs before retries.

The generated [publication export](docs/publication/tanduna-plan-export.json) is a local review artifact, not a supported API payload or proof of native publication. See the [source mapping](docs/planning/source-mapping.md).
