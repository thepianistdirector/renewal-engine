# 0.5 local acceptance evidence

The final local suite ran **72 discovered tests**, all passed. Twelve tests exercise
actual Linux isolation and syscall/resource denials; they were not skipped here.
`unit-tests.txt` retains the complete discovered-test names and outcome.

`packaged-checks.json` identifies the exact CLI hash and **27 actual CLI checks**
run outside the checkout: conformance, inspection and reverse import impact,
selected hunks, exact approval, stale refusal and new inspection, both migration
demos and independent negative controls, repeated comparison and seeded variance,
private summary export, explicit-execution refusal, actual isolation execution,
source/output identity verification and typed tamper refusal.

`hardlink-normal.json` and `hardlink-negative.json` retain all five cases, with two
actual observations on each runtime. Normal: 5/5 PASS. Wrong direction: 5/5
REGRESSION. They include exact binary/ConfigParser/pathlib hashes and the independently
observed filesystem contract. These exported records summarize the local retained
run; the original hard-link topology remains in its private raw run directory.

`isolation.json` exports nine actual denial/environment checks, frozen hashes,
the copied source manifest and one successful isolated program's output-file
bytes/hash. Absolute runtime paths are explicitly omitted. Further live negative
coverage is named in the twelve isolation tests and docs/isolation.md.

`recovery.json` retains the exact packaged normal/negative/idempotence/tamper
verification plus real SIGINT during partial candidate generation and comparison,
refusal to reopen incomplete attempts, and a safe new run. Developer workspace
prefixes are replaced with the fixed `LOCAL_WORKSPACE` label and the target path with `TRUSTED_TARGET_RUNTIME` in this shareable copy.

Independent Astra reviewers reproduced and prompted fixes for strict bool/int
verification, duplicate JSON keys, oversized retained results, source membership
and schema checks, unsafe verifier reads, and source-package document inclusion.
Focused regression tests are included. Review is automated agent evidence.

These are **local automated/runtime results**. They are not a public 0.5 release,
fresh external reproduction, human second-recipe assessment, or completed Tanduna
publication. The old public 0.1 assets remain unchanged. The exact 0.5 publication
packet and fresh external workflow require their concrete release authorization.

## Public readback and external attempt

The owner approved the exact packet. `public-release.json` records actual public
v0.5.0, all three anonymous asset/hash checks and installation from the public
archive. The source tag and assets retain the approved immutable identities.
`external-attempt-1.json` records a FAILED PREREQUISITE on fresh Ubuntu 24.04: the
runner lacked an executable `/usr/bin/bwrap`, so interpreter builds and product
checks were skipped. The returned evidence archive had zero members. No external
execution, successful isolation or human validation is inferred from that run.
