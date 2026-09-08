# Decision 001: bounded local ConfigParser migration

State: narrow fixture and runtime matrix approved by the owner September 8.
Real execution and packaged recovery checks now have retained evidence.

## Observed facts

The checkout began clean on main at f434e00913f5df6c78721300ca68625401d87a41.
The twelve live Tanduna briefs are READY revision 3, not implemented outcomes.
Their planning base is 8af461149e2c4b6b3b17d54a10b3559168f8b32f.
The public project identity freshly returned by the briefs is
prj_9ef51e9826817323b774d5d3b900520f. Public task listing shows all 12 tasks;
proposals shows one approved founding plan and nothing open.

Native Goal belongs to task 01a07e1c-3ed5-7f90-9b4d-f5c4977ad123. It still
reports blocked after the owner resumed; the available tool has no resume action.
The destination's turn metadata reports OpenAI gpt-6-astra, high effort.
Owner inventory found this as the only Renewal Engine primary task.
Installed target interpreter reports CPython 3.12.14 on Linux x86_64.
The initial audit found no Python 3.11 executable. An approved project-local
build now supplies actual CPython 3.11.16; no shim is used.

## Requirements and architecture

Keep the source untouched. Discovery only reads selected Python files, without
importing them. Use Python's standard-library AST and token/source offsets,
with a deliberately restrictive straight-line binding proof. Refuse uncertainty.
Source-span edits preserve unrelated bytes; no AST unparse or text replacement.
Split discovery, transformation, execution, comparison, report, and CLI modules.
No production Python packages are required. No LLM, network client, or upload
is part of the product. The standard library is the replacement path for these
small module boundaries; a general parser library may be reviewed later.

Only a pinned, original, reviewed reference fixture may execute. Selected user
source trees are inspection/transformation inputs, never executable inputs.
Interpreter subprocesses use explicit argv, isolated import mode, a scrubbed
environment, bounded execution/output, and process-group cleanup. This is not
an OS sandbox. Cross-repository execution requires a future enforced isolation
contract and separate authorization.

The immutable manifest identifies source, fixture, recipe, comparator policy,
and actual runtimes. Attempt directories are exclusive and never reused.
Atomic stage records retain interruption evidence. Restart creates a new run,
which avoids trusting stale results or overwriting accepted evidence. The
original snapshot is read-only; candidate edits are opt-in review artifacts.

The comparator owns frozen expectations independently of the transformer.
Compare complete measured outputs, exception class/message/args/attributes,
warnings, and declared stream/filesystem effects. Permit only the exact
documented readfp DeprecationWarning removal. No broad error normalization.
An independently constructed wrong patch must fail on a concrete discrepancy.

## Proposals and unresolved decisions

Use a new original AGPL-3.0 reference as the narrow 0.1 cut. This cannot satisfy
the older maintained-upstream fixture or volunteer-adoption requirements.
Owner approved the original fixture and proceeding on September 8, 2026.
Recommend old CPython 3.11.16 and installed target CPython 3.12.14.
Exact patch versions are the initial validation matrix, not all Python versions.
Git author identity was resolved from the repository history without global
configuration changes. Public release, fresh external reproduction, human review,
and native Tanduna publication remain separate unresolved gates.

## Alternatives, costs, and rollback

A general codemod library adds dependency and binding complexity before one
recipe is proved. A hosted demo adds an unnecessary private-code execution
surface. Both are deferred. Original-fixture results are narrower than upstream
adoption evidence and must be labeled accordingly. One comparison at a time,
small fixtures, and a few megabytes of run artifacts are the intended envelope.
Rollback means retain the original and reject the candidate; no external data
restoration or automatic patch application is promised.

## References

- [Python 3.12 removals](https://docs.python.org/3.12/whatsnew/3.12.html)
- [Python 3.11 ConfigParser](https://docs.python.org/3.11/library/configparser.html)
- [Pinned implementation](https://github.com/python/cpython/blob/v3.11.16/Lib/configparser.py)
- [Subprocess semantics](https://docs.python.org/3/library/subprocess.html)
- [OpenRewrite maintainer recipe workflow](https://docs.openrewrite.org/running-recipes)

The Python source confirms readfp(fp, filename=None) delegates to
read_file(fp, source=filename). This establishes argument mapping, not arbitrary
call-site safety. All twelve original briefs and repository records are retained
under docs/lineage/2026-09-07 without editing their acceptance history.
