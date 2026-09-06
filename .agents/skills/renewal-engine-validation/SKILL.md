---
name: renewal-engine-validation
description: Validate a scoped Renewal Engine contribution using its domain invariants and reproducible evidence; apply the checks relevant to the saved task.
---

# Validate behavior-preserving modernization

Read the exact task revision and select the checks that address its acceptance criteria. This skill does not expand a task to the entire roadmap or authorize future implementation. These are validation instructions, not claims of an existing product.

1. Pin the reference repository, license, source revision and old/new runtime versions. Define the bounded migration and behavior intentionally changed before generating a patch.

2. Run characterization inputs against the original and candidate in isolated environments. Compare outputs, errors and side effects; make nondeterministic normalization narrow and explicit.

3. Include a deliberately wrong transformation that the differential check rejects. A build that succeeds without that sensitivity does not establish behavioral preservation.

4. Apply the recipe twice and show idempotence or a clear already-migrated refusal. Keep unsupported patterns for human review and prevent unrelated source rewrites.

5. For ordering or data steps, test an interrupted transition and the documented recovery using disposable data. Distinguish reverting source from restoring data; a generated patch is not maintainer adoption.

For every selected check, record fixture/setup, actions, expected outcome, observed outcome and reproducible evidence. State which checks were not applicable and why; do not count unrun checks as passing.
