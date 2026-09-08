# Renewal Engine

Inspect a focused Python API migration, keep the original source, and review a
candidate patch with its evidence.

**Earlier release: [0.1.0](https://github.com/thepianistdirector/renewal-engine/releases/tag/v0.1.0).** The approved reference
passes all 12 cases on real CPython 3.11.16 and 3.12.14. A deliberately wrong
transformation produces two regressions. Packaged runtime and interruption
checks pass on Linux x86_64, including a [fresh external Ubuntu 24.04 run](https://github.com/thepianistdirector/renewal-engine/actions/runs/34226941566)
using the publicly downloaded release. Human validation remains pending.

## Current release: 0.5.0

The owner expanded this task through 0.5 on September 8. The current checkout adds
versioned recipes and composition, a Path hard-link migration, static project
impact, repeated-observation policies, hunk selection and exact approval,
private summary export, and explicitly authorized execution in a verified narrow
Linux isolation profile. See [the 0.5 guide](docs/0.5-guide.md) and [current objective](GOAL.md).
**[Download 0.5.0](https://github.com/thepianistdirector/renewal-engine/releases/tag/v0.5.0).** All public asset hashes and fresh-prefix installation were verified.
The [external attempt](https://github.com/thepianistdirector/renewal-engine/actions/runs/34247933729) stopped because its runner lacked an executable `/usr/bin/bwrap`; no product test ran there. Local 72-test and 27-packaged-check results passed. Human review and native-plan publication remain pending.

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

## Download or build

Download the source archive and SHA256SUMS from the versioned release above.
The published source archive SHA-256 is
`2bf2d535ab2c27b87305f960f793151f630d8e70186a52e34ec704cf1eb0c48e`.
The tagged release assets are immutable checkpoints; later checkout builds
contain subsequent evidence and may have different source archive hashes.

To build the current checkout locally:

```sh
python3 tools/build.py
python3 dist/renewal-engine.pyz --version
```

The build creates a deterministic self-contained CLI and source archive in
`dist/`, plus SHA-256 checksums. A local build is separate from the verified published assets. The source archive includes `install.py`; after
extracting it into a new directory, run:

```sh
python3 install.py --prefix ./local-install
./local-install/bin/renewal-engine --help
```

The installer refuses to overwrite an existing command and does not change
PATH or shell configuration. Keep the source archive and license with the CLI.
No interpreter binaries or development browser dependencies are distributed.

## Comparison and recovery

The trusted-reference workflow requires existing **Linux x86_64 CPython
3.11.16 and 3.12.14** interpreters. Different patch versions are refused. These
are the only measured versions; no compatibility shim is used. Users supply
both runtimes: interpreter binaries are not bundled. See the
[runtime acquisition record](docs/decisions/002-runtime-acquisition.md) for the
checksum-verified baseline source and limitations of the tested build.

Set `BASELINE_PYTHON` and `TARGET_PYTHON` to your two trusted executable paths.
From the extracted archive, after installation:

```sh
mkdir -p runs
./local-install/bin/renewal-engine demo --baseline "$BASELINE_PYTHON" --target "$TARGET_PYTHON" --out runs/normal
./local-install/bin/renewal-engine verify runs/normal
./local-install/bin/renewal-engine demo --baseline "$BASELINE_PYTHON" --target "$TARGET_PYTHON" --out runs/negative --negative-control
# The negative-control command must return exit code 1 and report REGRESSION.
./local-install/bin/renewal-engine verify runs/negative
```

Open `runs/normal/report.html` and `runs/negative/report.html`. Normal has
12 passing cases and 12 expected warning removals. Negative has two regressions
that expose `WRONG.ini` in the diagnostic source. Verification exit 0 means
the saved evidence is consistent, including when its result is REGRESSION.
The complete retained [normal example](examples/normal/report.html) and
[negative example](examples/negative/report.html) can also be reopened offline.

The reference is original AGPL-3.0 material, approved September 8, 2026, not
upstream adoption. Its [provenance](renewal_engine/reference/PROVENANCE.md)
describes coverage. Only removal of the exact readfp deprecation warning is
allowed. Exception type, message, arguments and instance-dictionary attributes,
plus declared stream/file effects, are retained. Tracebacks and exception
chaining are unmeasured. Passing these cases is not general equivalence.

A completed run can be reopened with `verify RUN_DIRECTORY`, which executes no
source and checks retained sources, patch, observations, policy and summary.
This detects inconsistent artifacts; it is not a cryptographic signature against
an attacker replacing the complete evidence bundle. If interrupted, retain the whole incomplete run and restart with a new
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

To reproduce the packaged checks, including a real SIGINT during partial
candidate creation and comparison, run from the extracted source archive:

```sh
python3 tools/verify_runtime.py --cli ./local-install/bin/renewal-engine --baseline "$BASELINE_PYTHON" --target "$TARGET_PYTHON" --out runs/verification
```

This uses deterministic stage fault injection with real runtime executions;
it retains incomplete attempts and proves a fresh restart. See the
[runtime evidence](docs/evidence/runtime-verification.md) for exact scope.

[project-plan.json](project-plan.json) is the canonical plan: 218 outcomes across
26 waves, including 50 for 0.1. [ROADMAP.md](ROADMAP.md), [TASKS.md](TASKS.md),
contracts and publication export are generated from it. The twelve frozen
Tanduna identities and acceptance history remain in
[the lineage records](docs/lineage/2026-09-07).

The [public Tanduna roadmap](https://tanduna.com/projects/renewal-engine/roadmap)
currently contains the historical plan; the new export is not yet published or
accepted. External runtime reproduction has passed. Required human maintainer
validation and native plan publication remain unfinished; see the
[maintainer walkthrough](docs/publication/maintainer-walkthrough.md). See [HANDOFF.md](HANDOFF.md) for exact next work.

Licensed under [GNU AGPL-3.0](LICENSE). [Contributions](CONTRIBUTING.md) require
scoped evidence and normal maintainer review; generated patches are not adoption.
