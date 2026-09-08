# Repeated observations and narrow policies (0.5)

`renewal_engine.observations` is a standalone standard-library utility. It does
not modify the existing recipe comparator in `comparison.py` and does not run a
program. The caller collects raw observations and decides which runs to compare.

## Repeated comparison

```python
from renewal_engine.observations import compare_repeated

policy = {
    "schema_version": 1,
    "owner": "release-reviewer",
    "reason": "Compare the approved observation contract",
    "rules": [],
}
result = compare_repeated(original_runs, candidate_runs, policy)
```

Both sides must contain an equal number of JSON objects, from two through ten.
Strict JSON types are required: booleans, integers and floating-point numbers
remain distinct, including inside lists and objects. NaN, infinity, tuples,
bytes, nonstring object keys and cycles are rejected. Object key order is
irrelevant; other differences are exact by default, including signed floating
zero's canonical JSON representation. Inputs are never modified; retained raw
records and policy are deep copies. These are ordinary mutable result objects,
not read-only containers. Observation and policy SHA256 identities use sorted-key,
compact, UTF-8 JSON with finite numbers.

Every pair within each side and every original/candidate pair is checked. This
prevents paired runs from hiding identical variance and prevents a tolerance
chain from accepting distant endpoints. Status precedence is:

1. `UNSTABLE`: at least one unauthorized within-side difference.
2. `REGRESSION`: stable sides with at least one unauthorized cross-side difference.
3. `PASS`: all differences are explicitly authorized, or there are none.

The result includes `schema_version`, `status`, `raw.original`, `raw.candidate`,
`policy`, `policy_sha256`, `observation_sha256.original/candidate`,
`expected_changes`, `variance`, `regressions`, `counts`, and `truncated`.
Difference records contain exact JSON pointers, zero-based `first_run` and
`second_run`, `scope` (`original`, `candidate`, or `cross`), `authorized`, and a
reason. Authorized records also name the rule kind. `variance` includes both
authorized and unauthorized within-side differences. `expected_changes` records
authorized cross-side differences, not arbitrary expected value transitions.
`counts` contains `runs_per_side`, `expected_changes`, `variance`,
`unauthorized_variance`, and `regressions`. Counts represent pairwise difference
events, not unique paths. Each evidence list retains at most 1,000 records;
counters continue counting, and `truncated` is set if evidence was omitted.

## Policy schema

The policy must contain exactly `schema_version` (integer `1`), nonempty `owner`
and `reason` strings of at most 1,000 characters, and `rules` (at most 256).
An empty rule list is the exact default. Each rule has an exact `path`, a `kind`,
and a nonempty bounded `reason`. Numeric rules also require
`absolute_tolerance`; no other fields are accepted.

```json
{
  "schema_version": 1,
  "owner": "release-reviewer",
  "reason": "Approved observation representation differences",
  "rules": [
    {"path": "/metrics/elapsed", "kind": "numeric", "absolute_tolerance": 0.125,
     "reason": "Measured timing variation within the reviewed limit"},
    {"path": "/recorded_at", "kind": "timestamp",
     "reason": "Timezone spelling may differ for the same instant"},
    {"path": "/items", "kind": "unordered",
     "reason": "Order is outside the contract; all values and counts matter"}
  ]
}
```

Numeric tolerance must be a finite number from zero through 1,000,000; booleans
are invalid. Both target values must retain the same JSON numeric type. The
absolute difference is checked using exact fractions of the supplied Python
numbers, so floating-point values retain their actual binary meaning.

Timestamp rules require ISO strings with a date, `T`, seconds, optional one to
six fractional digits, and an explicit `Z` or `±HH:MM` offset. Only representations
of the same instant are authorized. Naive dates, time-only values, invalid
calendar values and timezone offsets are rejected.

Unordered rules accept lists of at most 1,000 items and compare exact multisets.
Duplicates, element types, every nested field, and nested list ordering remain
significant. No values are dropped or coerced.

Paths use JSON pointer escaping (`~0` for `~`, `~1` for `/`). The root pointer,
wildcards, invalid escapes, noncanonical list indices, duplicate rules and
ancestor/descendant rule overlaps are rejected. Every path must exist and target
the appropriate type in every run. A missing policy path is invalid input, not
permission to suppress missing fields. Invalid observations or policies raise
`ValueError`; callers should report invalid evidence separately from behavioral
regressions.

Each observation or policy is limited to 4 MiB of encoded JSON, 50,000 values,
and depth 64. Encoding and validation are resource guards, not a process sandbox.

## Filesystem observation

`observer(root: Path)` returns:

```json
{
  "schema_version": 1,
  "files": {"relative/name.bin": {"size": 2, "sha256": "...", "bytes_hex": "00ff"}},
  "counts": {"files": 1, "bytes": 2}
}
```

This retains exact regular-file bytes, including nontext files. Comparing
observations detects creation, deletion and content changes through the file
mapping. Empty directories, permissions, owners, timestamps, extended attributes
and hardlink relationships are not observed behavior.

Every ancestor and descendant directory is opened using directory descriptors
and `O_NOFOLLOW`; symlinks, special files, parent traversal in the root, unreadable
entries and detected changes during reading fail closed with `ValueError`.
Support requires POSIX descriptor-relative filesystem operations. Files are
opened nonblocking to avoid hanging on a concurrent replacement with a pipe.
Inode and file change checks reduce races; a concurrently modified tree is not an
atomic snapshot. Supply a quiescent, isolated fixture tree. Hardlinks to regular
files are not rejected; the caller remains responsible for fixture provenance.

Bounds are 256 regular files, 1,024 total directory entries, 64 KiB per file,
1 MiB total file bytes and directory depth 16. No file contents are truncated.
Violations fail the observation rather than emitting incomplete evidence.

## Shareable summaries

`shareable_summary(result)` creates a fresh allowlisted object containing only
schema version, validated status, known numeric counters, policy SHA256, and
original/candidate observation SHA256 lists. It excludes raw observations,
source, paths, stdout, environment values, policy owner/reasons and all unexpected
fields. Even purported hashes and statuses are shape-validated before inclusion.
Hashes are identities, not encryption: low-entropy observations can potentially
be guessed by recomputing their hashes. Full results and filesystem observations
contain raw evidence and must not be treated as shareable summaries.

Run focused validation from the project directory:

```sh
python -m unittest discover -s tests -p test_observations.py
```
