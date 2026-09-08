# Real packaged runtime verification — September 8, 2026

RUNTIME VERIFIED on the same Linux x86_64 VPS. Owner approved the original
AGPL-3.0 fixture and CPython 3.11.16 / 3.12.14 matrix on September 8.
This is not an external download, human study or maintainer adoption.

The extracted source archive installed into a new project-local prefix. Its
self-contained CLI SHA-256 is
`ee6b2b9e6ba3ffc3e34102dc70ac596b1e3f8479bacd8a6e99072a7c78c80047`.
The verification script was run from the extracted package, outside the source
checkout import path. Both real interpreter and ConfigParser hashes are retained
in each example manifest. No baseline shim or synthetic observation was used.

## Actual outcomes

- Normal: 12/12 cases PASS, zero regressions and 12 exact expected readfp
  deprecation-warning removals. Baseline observations exist before candidate
  generation. Full sources, cases, effects, raw subprocess bytes and reports
  are in `examples/normal/`.
- Negative: exit 1, REGRESSION in `duplicate-option-keyword` and
  `malformed-source-keyword`. The independently injected `WRONG.ini` source
  changes exception arguments, message and source attribute. Full evidence is
  in `examples/negative/`.
- A fresh verification process accepts both consistent evidence bundles while
  preserving the normal PASS / negative REGRESSION distinction. Reusing an
  output directory is refused with exit 2. Reinspection of the candidate
  creates an empty patch and verifies as INSPECTION ONLY.
- Real SIGINT during candidate creation: a test-only worker writes half the
  candidate and stops itself with SIGSTOP. The supervisor sends SIGINT and
  SIGCONT. Exit 130, INCOMPLETE, 12 baseline records, no target observations,
  no report/results, and unchanged original bytes were asserted.
- Real SIGINT during comparison: the test-only wrapper stops at comparison
  after all 24 actual observations. The same signals produce exit 130 and
  INCOMPLETE with all observations retained and no report/results. Reopening
  either incomplete attempt refuses with exit 2.
- A fresh run after both interruptions passes all 12 cases and creates the
  identical candidate. The interrupted attempts remain incomplete.
- Changing saved case inputs, policy or candidate bytes causes refusal;
  restoring the original bytes allows verification again. Unit falsifiers
  separately reject corrupted patch bytes and inconsistent negative labels.

Reproduce with `tools/verify_runtime.py` using the README command. It contains
explicit deterministic stage fault injection; this is not a claim that a random
interruption happened to land inside the small write window. Local attempts
are retained under `.runs/package-0.1.0-01/checks/`. Public transcript
`packaged-runtime.json` replaces only machine paths with placeholders; raw
example observations are unchanged.

## Critic findings resolved

A fresh-context Astra leaf independently checked runtime hashes, normal and
negative results, idempotence, attribution and comparator scope. It reproduced
two saved-evidence defects: damaged patch bytes were not checked, and the
negative label could contradict the retained source identity. Verification now
reconstructs the patch and checks the Boolean label plus trusted candidate hash.
Regression tests cover both. Exception-fidelity wording now accurately names
instance-dictionary attributes and excludes chaining, traceback frames and
arbitrary effects. This independent agent review is not human validation.

The 27-test suite passes with these fixes. Native browser zoom, assistive
technology and required human review remain unfinished. Subsequent evidence
in public-release.json and external-runtime.json establishes actual GitHub
release and fresh external public-download reproduction. Native Tanduna
publication remains unfinished.
