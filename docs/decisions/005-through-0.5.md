# Decision 005: bounded Python 0.2–0.5 implementation

Owner instruction, September 8, 2026: continue this task through 0.5. The former
0.1 publication dependency does not block independent local technical progress.
GOAL.md records the revised objective; native goal controls cannot edit it.
Existing task IDs, wave IDs and historical acceptance stay intact.

0.2 introduces closed, versioned recipe contracts with digest-pinned conformance
fixtures, runtime intervals, effect coverage, review policy ownership, dependency
ordering and deterministic selection. Arbitrary executable plugins remain out
of scope. A registry admits only shipped, reviewed discovery handlers. ConfigParser
0.1 discovery and its comparator stay byte-compatible for retained evidence.

0.3 adds the Path.link_to migration and static impact. CPython's own issue 39950
records the confusing direction and motivates hardlink_to. The replacement must
reverse source/destination; simply renaming the method is a negative control.
Sources: https://github.com/python/cpython/issues/84131 and
https://docs.python.org/3.12/library/pathlib.html#pathlib.Path.hardlink_to .
The original AGPL conformance/reference fixture is authored in this repository;
no upstream project code or adoption is implied. Trusted characterization uses
actual existing 3.11.16 and 3.12.14 runtimes with file content/link relationships,
exceptions and exact warning transition. Static support is restricted to two
locally constructed Path values followed immediately by the direct call.
Impact analysis reads syntax and metadata, never resolver hooks or setup code.

0.4 adds repeated observations, explicit narrow variance rules, hunk selection
and exact approval of a retained candidate, plus allowlisted shareable summaries.
Changing source or selection invalidates approval and requires fresh inspection
and characterization; no automatic three-way merge or apply-to-original claim.
Raw evidence stays private by default and is never implied safe for publication.

0.5 adds a verified narrow Linux Python isolation profile and integrated CLI,
package, contributor instructions and actual release-candidate evidence. The
profile's constraints are part of its public API, not a general container claim.
The existing bubblewrap backend must pass independent denial checks before user
project execution; default inspect remains offline and nonexecuting.

These scopes map to existing N06–N14 outcomes. They do not declare all 72 tasks
complete: human second-recipe review, independent contributor feedback, and
broader future execution/observation contracts retain their individual gates.
No new runtime Python dependencies are introduced. Packaged outputs use separate
version directories to preserve published 0.1 assets. A failed candidate can be
retained, rejected and rebuilt into a new directory without altering originals.
Final 0.5 publication needs a concrete reviewed packet under the original owner
publication instruction; the old 0.1 artifact approval is not silently widened.
