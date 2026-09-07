# Reference fixture provenance

Original fixture authored for Renewal Engine under the repository's AGPL-3.0
license. No third-party application or maintainer adoption is claimed.

Owner decision: pending. These files are a concrete review candidate; no
original/target differential execution is claimed until the fixture is approved
and actual pinned runtime results exist.

The three loader functions cover local import aliases and positional/keyword
stream/source-name argument binding. Cases cover successful input, Unicode,
duplicate sections/options, malformed and missing headers, interpolation,
missing option/section, multiline CRLF and an empty explicit source name.

The driver writes only input.ini and optional normalized.ini in its supplied
working directory. It measures stream position, closure, file content, output,
exception type/message/args/all attributes, and warning category/message/source
line. JSON encodes exception tuples as arrays on both sides; no exception fields
are discarded. Warning filenames are program.py on both sides; run manifests
retain full source hashes. Traceback frames and arbitrary external effects are
unmeasured. The driver loads only the hash-pinned local fixture using runpy;
unreviewed source loading, credentials, network, shell and package installation
are excluded from this workflow.

Expected policy: only the exact ConfigParser.readfp DeprecationWarning is absent
from the target. Any other observed difference is a regression. The independent
negative control changes the explicit diagnostic source name to WRONG.ini.
