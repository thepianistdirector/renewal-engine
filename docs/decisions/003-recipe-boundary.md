# Decision 003: first recipe binding proof

State: proposed conservative implementation boundary within the owner’s 0.1 cut.
No claim of general call-site safety or supported behavior beyond tested fixtures.

Support an ordinary, undecorated function whose first executable statements are:

```python
def load(stream, source):
    import configparser
    parser = configparser.ConfigParser()
    parser.readfp(stream, filename=source)
    return parser
```

A docstring and comments may precede these statements. An explicit local
`from configparser import ConfigParser` or import alias is also attributable.
The constructor has no arguments in this cut. The readfp call must be a direct
expression immediately following construction; positional `fp` and optional
`filename`, or the exact `fp=` / `filename=` keywords, are supported. Arguments
are parameter names or constants, with no calls, unpacking, property reads or
other expressions. Source-name forms await actual pinned-runtime verification.

Bindings must not collide with function parameters, each other, or global/nonlocal
declarations. No async functions, decorators, class methods, nested closures,
control-flow-contained calls, reassignment between constructor and call, indirect
receivers, imported subclasses, monkey-patching syntax, or star arguments are
rewritten. All remaining syntactic readfp calls receive an explicit review-needed
finding. A second application reports no supported legacy calls.

This narrower pattern avoids a dependency on an unproved whole-program binding
analysis. A later recipe revision may admit module-level imports and richer
control flow only after negative binding fixtures prove that extension.

Inspection of a selected tree rejects symlinks/special files, bounds file sizes
and counts, and reports a local configparser module/package as a shadowing risk.
No source is imported or executed. Standard-library identity assumes an ordinary
Python import environment with no external import hooks or sys.modules injection;
such whole-process behavior is unmeasured and the saved report must say so.

Edits use AST UTF-8 source offsets for the attribute/keyword identifiers only.
Non-UTF-8 Python source is refused explicitly in 0.1. CRLF, Unicode, comments,
docstrings and unrelated bytes remain byte-identical. The patch records every
edit and reason; there is no automatic application to the selected source.
