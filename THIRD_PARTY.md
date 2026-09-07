# Third-party source and development notices

Renewal Engine's authored implementation and original proposed fixture are
offered under the repository's GNU AGPL-3.0 license. Fixture selection approval
and human/upstream adoption evidence remain separate pending decisions.

## Retained source references

- `docs/references/python311-configparser.py` is an unchanged source reference
  from CPython v3.11.16, retained to review the exact readfp delegation. Source:
  https://github.com/python/cpython/blob/v3.11.16/Lib/configparser.py.
  The accompanying upstream license and historical notices are retained in
  `docs/references/python311-LICENSE`. This file is not imported by the product.
- `docs/lineage/2026-09-07/tanduna-contribution-SKILL.md` is the pinned shared
  contribution guide from context-harbor commit
  a288bac1ff8bf87fe382ee6bf15ace4c0a090cbd, provided under that repository's
  AGPL-3.0 license. Other lineage files are frozen Renewal Engine planning
  records and public Tanduna read-back evidence, not proof of implemented work.

## Runtime prerequisites and local development tools

The product installs no third-party Python packages and includes no interpreter
binary. Users supply the declared Python runtimes. The locally built CPython
3.11.16 runtime and all build outputs stay under .local and are not distributed.

Browser verification used agent-browser 0.36.0 (Apache-2.0), an existing Chromium
binary, and thirteen locally extracted AlmaLinux x86_64 library packages.
Exact package versions, hashes and reported licenses are recorded in
docs/evidence/browser-dependencies.json. These binaries/libraries are development
prerequisites only and are excluded from the CLI and source distribution.
No shared host package or security setting was changed for verification.
