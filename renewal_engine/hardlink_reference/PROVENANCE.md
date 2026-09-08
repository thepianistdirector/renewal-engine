# Hard-link reference provenance

The program, driver, cases and policy were authored for Renewal Engine on
September 8, 2026 and are distributed under this repository's AGPL-3.0 license.
They do not copy an upstream application or test suite. `trust.json` pins every
executable/input/policy byte and independently expected normal/wrong candidates.
The fixture contains original short Unicode text and no third-party data.

CPython's documentation and maintainer issue establish the API motivation, not
ownership or adoption of this fixture:
https://github.com/python/cpython/issues/84131
https://docs.python.org/3.12/library/pathlib.html#pathlib.Path.hardlink_to

The exact existing 3.11.16 and 3.12.14 interpreters are separately trusted inputs,
not redistributed by this package. The only expected change is disappearance of
the complete old deprecation warning at its exact reference source line. No
filesystem difference, filename reversal, errno change or variance is allowed.
The negative control deliberately changes the method name without reversing the
receiver/argument and must fail. An external maintainer's usefulness review is
still pending; automated evidence must not be represented as that review.
