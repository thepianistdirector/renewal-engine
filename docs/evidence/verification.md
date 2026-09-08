# Verification record — September 7, 2026

Historical scope: September 7 local increment, before fixture approval.
September 8 update: see runtime-verification.md for actual packaged evidence
and resolved follow-up critic findings. Earlier unrun statements below describe
the September 7 checkpoint only. Current task evidence levels live in project-plan.json.

## Automated evidence

`python3 -m unittest discover -s tests -v`: 27 tests passed. These check exact
source bytes and argument mapping; Unicode/CRLF/bare-CR offsets; imports,
receiver rebinding and dynamic mutation; same-line support labels; full-source
stale hash rejection; shadowing for directory and single-file inspection;
source preservation; exclusive outputs; candidate/comparison interruption;
reopening and rejection of falsified summaries, changed observations/files or
missing process logs; narrow warning changes; exception-field and effect
mutants; environment credential canaries; timeout and output overflow; exact
raw-byte retention and descendant termination after its leader exits. Saved
runtime records are checked against the declared version/platform/hash schema;
these unsigned local artifacts do not constitute authorship attestation.

Workflow orchestration and saved-comparison tests use synthetic observations.
They do not invoke or emulate the original runtime and are not evidence of
ConfigParser behavior under either runtime. Actual subprocess tests use small
authored infrastructure probes, not the pending reference program.

`python3 tools/plan.py validate`, `self-test` and `check`: passed for 218 tasks,
26 waves and 12 exact source mappings. Twenty deliberately malformed plans
(including graph, lineage, scope and schema mutations) were rejected.

`python3 tools/build.py`: produced a self-contained CLI and source archive.
The package smoke test extracted the local archive, installed into an explicit
project-local prefix, printed the version, inspected the reference source
without executing it, and reopened the evidence successfully. Exact command
outputs are in package-smoke.json. No public download or external machine was
involved. Stable final artifact hashes are recorded after the final build.

## Independent Astra criticism and fixes

The critic verified its runtime model and remained read-only. Six concrete
findings were reproduced and fixed with regression checks:

1. Subscript writes through ConfigParser.__dict__ could bypass dynamic-binding
   rejection. Reject those dynamic access/mutation forms.
2. Equal-length import changes could reuse stale edit spans. Bind discovery to
   the complete source SHA-256 and check it before every transformation.
3. Support status was shared by line. Associate it with the exact AST call node.
4. Single-file inspection missed sibling import shadows. Inspect that context
   before admitting the local ConfigParser binding.
5. Saved verification trusted a modified PASS/measurement label. Validate the
   mode/stage and recompute the summary from retained comparison evidence.
6. Saved verification ignored process records, measured files and harness
   identity. Verify the records, independent file hashes and pinned sources.

The fixed review rubric covered rewrite safety, comparator independence,
truthful claims, recovery/integrity and package usability. Code criticism did
not establish human maintainer validation or real-runtime equivalence.

## Runtime and interface boundaries

Actual probes report CPython 3.11.16 with readfp present and CPython 3.12.14
with readfp absent. Binary and standard-library hashes are retained in the
separate runtime JSON files. The original reference program has not run.
Normal/negative demonstration, packaged old/new comparison, actual interrupted
reference execution, external reproduction and human review remain NOT TESTED.

The browser initially lacked native libraries; thirteen x86_64 AlmaLinux
packages were extracted under .local without host installation. A later trace
and shorter project-local TMPDIR resolved the remaining startup failure.
Actual narrow/desktop layouts, keyboard focus/disclosure activation, CSS zoom,
expanded content and no-resource loading were observed. The visual critic's
misleading review-count label was fixed. See report-browser-review.md and its
screenshots. Native zoom and human/assistive-technology observations remain
unrun; no universal accessibility claim is made.

No release or native Tanduna plan was published. The current public pages were
read unauthenticated and still show the twelve frozen historical tasks.
