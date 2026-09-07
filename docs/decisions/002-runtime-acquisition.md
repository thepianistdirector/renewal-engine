# Decision 002: proposed original runtime acquisition

State: owner authorized September 7, 2026. The official source checksum was
verified and the project-local build completed. An actual probe reports
CPython 3.11.16 and readfp present; see docs/evidence/baseline-runtime.json.
Reference fixture execution remains pending the distinct fixture decision.

Owner response: "Install all the needed dependencies that you need, you can use
all the resources you need from this VPS too." This reuses the requested
project-local scope and does not expand publication or shared-host changes.

Recommend building CPython 3.11.16 from the official Python.org XZ source:
https://www.python.org/ftp/python/3.11.16/Python-3.11.16.tar.xz

Official release page:
https://www.python.org/downloads/release/python-31116/

Expected SHA-256: 91bcdebfdde239a003ae93738a7fce0f9230fee5c4bc2b86f6e6e8c6f98aabe8

Scope: project-local download, source/build directory and interpreter prefix
under .local; no PATH, shell profile, host package or global configuration changes.
Use existing gcc/make, at most two compile jobs, without PGO or ensurepip.
Bound initial envelope: 2 CPUs, 2 GiB memory, 2 GiB disk, 15 minutes.
No third-party Python packages are installed. Optional extension modules may
link existing system libraries; inspect the actual configure/build results and
dynamic links before accepting the runtime. Missing optional modules must be
reported, never remedied by an unapproved machine package install.

License: PSF License Version 2 plus retained historical and bundled notices;
the pinned upstream LICENSE is retained in docs/references/python311-LICENSE.
This is the official security release of the supported 3.11 branch. A complete
vulnerability audit is not claimed. Only reviewed small fixtures will execute.
Acquisition contacts Python.org and exposes normal download metadata; runtime
execution has no application network requirement and no source upload.

No interpreter binary redistribution is proposed. Users supply matching
runtimes; a later binary bundle requires a separate dependency/notice review.
Replacement path: an owner-approved existing CPython 3.11.16 installation.
Rollback: stop only this project's build, retain its logs, and retire its prefix.
No paid resources, credentials, account changes or shared toolchains are needed.

Observed build limitations: _bz2, _curses, _curses_panel, _dbm, _gdbm, _lzma,
_tkinter, _uuid, nis and readline were unavailable; _sqlite3 was disabled by
configure and _ctypes failed to build. None is used by the reviewed candidate
ConfigParser fixture. Core interpreter, configparser, hashlib, pathlib and JSON
identity probes passed. This is a local evidence runtime, not a complete Python
binary distribution. Full configure/make logs are retained under
.local/runtime-build and are excluded from public artifacts because they contain
build-machine paths.
