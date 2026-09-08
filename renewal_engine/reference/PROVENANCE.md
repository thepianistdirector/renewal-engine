# Reference fixture provenance

Original fixture authored for Renewal Engine under the repository's AGPL-3.0
license. No third-party application or maintainer adoption is claimed.

Owner decision: approved September 8, 2026. The owner accepted this original
reference fixture for the narrow 0.1 and authorized proceeding with the real
Python 3.11.16 / 3.12.14 comparison. This does not satisfy the historical
maintained-upstream-fixture or maintainer-adoption requirements. Actual runtime
claims must still be backed by retained observations.

The three loader functions cover local import aliases and positional/keyword
stream/source-name argument binding. Cases cover successful input, Unicode,
duplicate sections/options, malformed and missing headers, interpolation,
missing option/section, multiline CRLF and an empty explicit source name.

The driver writes only input.ini and optional normalized.ini in its supplied
working directory. It measures stream position, closure, file content, output,
exception type/message/args/instance-dictionary attributes, and warning category/message/source
line. JSON encodes exception tuples as arrays on both sides. Exception chaining
(__cause__, __context__, __suppress_context__) is unmeasured. Warning filenames
are program.py on both sides; run manifests retain full source hashes.
Traceback frames and arbitrary external effects are
unmeasured. The driver loads only the hash-pinned local fixture using runpy;
unreviewed source loading, credentials, network, shell and package installation
are excluded from this workflow.

Expected policy: only the exact ConfigParser.readfp DeprecationWarning is absent
from the target. Any other observed difference is a regression. The independent
negative control changes the explicit diagnostic source name to WRONG.ini.
