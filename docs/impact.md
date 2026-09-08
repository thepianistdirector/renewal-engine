# Offline project impact (0.5)

`renewal_engine.impact.analyze(sources, metadata, changed_paths)` accepts mappings
of project-relative POSIX paths to bytes and a list of changed paths. The caller
owns safe file discovery and reading. The analyzer opens no files, executes no
project code or configuration, accesses no network, and needs only Python's
standard library (including `tomllib`). Its result is JSON serializable.

The result includes:

- `graph`: importer source path to sorted imported source paths.
- `changed`: each changed path's `direct_dependents`, `transitive_dependents`
  (excluding direct dependents and the changed file), and `impacted_paths`
  (including the changed file when supplied).
- `impacted_paths`: union of affected supplied source files.
- `exports`: top-level public function names, AST signature strings, line numbers,
  async flags and decorator flags. Literal `__all__` overrides naming convention.
- `uncertainties`: parse failures, ambiguous modules, unresolved imports, dynamic
  execution/import hints, wildcard exports, missing changed sources and limits.
- `metadata`: `python_requires`, raw `requirements`, `pin_conflicts`, `lockfiles`,
  `review_hints`, and `errors`.
- `limits`, `schema_version` (1), and an explicit static-review `status`.

Root and conventional `src/` modules are indexed; duplicate module names produce
an ambiguity and all candidates are included. Relative imports, package
initializers, namespace child imports and reexport import edges are followed.
Reverse traversal terminates on cycles. Imports inside functions, conditionals
and type-checking blocks are conservatively included regardless of execution.

This is a file-level graph, not an import resolver or proof of compatibility.
Arbitrary source roots, runtime paths, import hooks, alias-driven dynamic imports,
monkey patches, conditional exports and generated modules can escape the graph.
External imports, including the standard library, are unresolved here. An import
from a known module can denote an attribute or a child module; possible local
child modules are included conservatively. Function summaries describe declared
syntax, not decorated runtime signatures. Reexported functions are represented
by import edges, not synthesized signatures. Private class methods and nested
functions are outside signature summaries. An empty uncertainty list does not
establish complete runtime coverage.

`pyproject.toml` uses the standard TOML parser, with structural validation of the
supported project fields. Python ranges are declared strings, not evaluated
constraints. PEP 621 dependencies and optional groups are preserved. Poetry
Python constraints and dependency declarations are preserved without interpreting
Poetry's version language. `requirements*.txt` lines are preserved; only plain
unconditional exact `name==version` declarations are recognized as pins. Different
pins for a normalized package name produce a **potential** conflict because groups
and separate files may target different environments. Markers, URLs, ranges,
includes, hashes and wildcard pins remain unresolved. Lockfiles are recorded as
present, without claiming freshness, integrity or dependency resolution. Text
references to changed module names in metadata are configuration review hints.
Malformed metadata is reported; any partial declarations are only hints.

Each source or metadata collection is bounded to 4,096 files, 1 MiB per file and
16 MiB total; each parsed source is limited to 100,000 AST nodes. Limit failures
are explicit uncertainties/errors and make coverage incomplete. AST parsing
occurs before node counting, so these bounds are a resource guard rather than an
isolated hostile-input sandbox. Outputs sort paths for reproducibility.

Run the component checks from the project directory:

```sh
python -m unittest discover -s tests -p test_impact.py
```
