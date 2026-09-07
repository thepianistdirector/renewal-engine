# Renewal Engine

Inspect a focused Python API migration, keep the original source, and review a
candidate patch with its evidence.

**Development candidate: source inspection is implemented and tested. Public
0.1 is not released.** The original reference fixture decision and its actual
old/new differential execution remain pending. The bundled demo implementation
is not yet runtime-verified; synthetic tests do not establish equivalence.

## Try the working inspection

Prerequisite: Python 3.11 or newer. The current CLI checks ran on Linux x86_64
with CPython 3.12.14. No third-party Python packages, network account, hosted
model or source upload are required.

From a source checkout:

```sh
python3 -m renewal_engine --help
mkdir -p .runs
python3 -m renewal_engine inspect renewal_engine/reference/program.py --out .runs/my-inspection
python3 -m renewal_engine verify .runs/my-inspection
```

Open `.runs/my-inspection/report.html` in a browser. The report is fully offline.
It links the focused patch, JSON results, immutable manifest and recovery state.
The candidate and read-only original Python snapshots are saved beside it.
An inspection report explicitly says **INSPECTION ONLY**: no code was executed.

Select another `.py` file or bounded directory with the same `inspect` command.
Choose a new output directory outside the selected source tree. Only Python
source is copied; non-Python resources are not included. Symlinks, special
files, oversized trees and unsupported encodings are refused. Standard cache,
environment and Git directories are excluded and named in the manifest.

## Exact first recipe boundary

The supported form is an ordinary undecorated top-level function beginning with
an explicit local ConfigParser import, direct no-argument construction, and an
immediately following direct `readfp` call. Explicit local import aliases,
positional `fp` / `filename`, and `fp=` / `filename=` are recognized. Arguments
must be parameters or constants. The recipe maps `filename` to `source` and
`fp` to `f`. Comments, strings, Unicode and line endings are preserved.

```python
def load(stream, source):
    import configparser
    parser = configparser.ConfigParser()
    parser.readfp(stream, filename=source)
    return parser
```

Ambiguous receivers, module-global import bindings, decorators, nested/control
flow calls, constructor options, star arguments and dynamic mutations remain
unchanged with a review-needed finding. A second application produces no further
edits. See [the precise boundary](docs/decisions/003-recipe-boundary.md).

## Local package

```sh
python3 tools/build.py
python3 dist/renewal-engine.pyz --version
```

The build creates a deterministic self-contained CLI and source archive in
`dist/`, plus SHA-256 checksums. These are local development candidates, not
public release artifacts. The source archive includes `install.py`; after
extracting it into a new directory, run:

```sh
python3 install.py --prefix ./local-install
./local-install/bin/renewal-engine --help
```

The installer refuses to overwrite an existing command and does not change
PATH or shell configuration. Keep the source archive and license with the CLI.
No interpreter binaries or development browser dependencies are distributed.

## Comparison and recovery

`demo --help` describes the implemented trusted-reference workflow. It requires
explicit Linux CPython 3.11.16 and 3.12.14 executable paths and runs only the
bundled hash-pinned fixture. `--negative-control` deliberately corrupts a
source-name diagnostic; a real comparison must return exit code 1. These demo
paths are **not yet runtime-verified** and are not a public-use promise.

The reference candidate is original AGPL-3.0 material, not upstream adoption.
Its [provenance and case coverage](renewal_engine/reference/PROVENANCE.md) are
prepared for the fixture decision. Only removal of the exact readfp deprecation
warning is an allowed behavioral difference. Exception fields and declared
stream/file effects are retained. No traceback equivalence is claimed.

A completed run can be reopened with `verify RUN_DIRECTORY`, which executes no
source. If interrupted, retain the whole incomplete run and restart with a new
output directory. Original source stays unchanged. This is source recovery;
no restoration of arbitrary external data or effects is promised.

Exit codes: 0 for completed inspection, verified saved evidence, or a passing
comparison; 1 for a measured regression; 2 for refusal/error; 130 for interruption.
A zero inspection exit code is not a behavioral pass. Process limits and a
scrubbed environment are not an OS sandbox. Arbitrary repository execution,
automatic merge, production migration and private-code upload are excluded.

## Evidence and long-term plan

Run the meaningful automated checks:

```sh
python3 -m unittest discover -s tests -v
python3 tools/plan.py validate
python3 tools/plan.py self-test
python3 tools/plan.py check
```

[project-plan.json](project-plan.json) is the canonical plan: 218 outcomes across
26 waves, including 50 for 0.1. [ROADMAP.md](ROADMAP.md), [TASKS.md](TASKS.md),
contracts and publication export are generated from it. The twelve frozen
Tanduna identities and acceptance history remain in
[the lineage records](docs/lineage/2026-09-07).

The [public Tanduna roadmap](https://tanduna.com/projects/renewal-engine/roadmap)
currently contains the historical plan; the new export is not yet published or
accepted. Public release, external reproduction and human maintainer validation
are separate unfinished gates. See [HANDOFF.md](HANDOFF.md) for exact next work.

Licensed under [GNU AGPL-3.0](LICENSE). [Contributions](CONTRIBUTING.md) require
scoped evidence and normal maintainer review; generated patches are not adoption.
