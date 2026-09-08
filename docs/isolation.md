# Narrow Python isolation

`renewal_engine.isolation.execute_python` runs one explicitly authorized Python
entrypoint from a private snapshot. It refuses by default, requires a successful
live denial probe before every execution, and has no unsandboxed fallback.
This is a constrained Linux x86-64 CPython backend, not a general build runner.

```python
from renewal_engine.isolation import execute_python, freeze_runtime

runtime = freeze_runtime()  # the caller trusts this dedicated CPython installation
result = execute_python(snapshot, "main.py", authorized=True, runtime=runtime)
```

The frozen dataclass records the executable path, dedicated runtime prefix,
executable SHA-256, runtime-tree SHA-256, and bubblewrap SHA-256. They are checked
again before running. A trusted host administrator must keep runtime files and
system libraries stable during a run; this does not defend against concurrent
host administrators or a compromised kernel. A runtime prefix is a trusted input,
never discovered by executing project code. Broad `/usr`, `/usr/local`, `/home`,
and `/` runtime prefixes are refused. Dedicated project-local or uv CPython
installations are supported when their symlinks remain inside the prefix.

The project is copied through directory descriptors with `O_NOFOLLOW`; symlinks,
sockets, devices, and FIFOs are refused. The copy is limited to 16 MiB, 512
entries, and 32 directory levels. The result includes a sorted manifest of copied paths, entry types, byte lengths, and SHA-256
values (directories are included with zero size and a null hash) plus a digest of the canonical JSON manifest, identifying actual copied
bytes independently of subsequent source-path changes. The private copy is mounted read-only at
`/project`. The runtime is mounted read-only at `/runtime`; only the system library
roots `/lib`, `/lib64`, and `/usr/lib` are additionally mounted read-only. No host
home directory, credential directory, `/etc`, host process filesystem, or device
tree is mounted. The caller must exclude credentials from its project snapshot
and trusted runtime. This boundary cannot hide files deliberately supplied as
project inputs.

`/work` is a **read-only directory containing one writable file, `/work/output`**.
No other files or directories can be created. The parent reads that file after
process cleanup and records exact bytes as hexadecimal, length, and SHA-256.
General filesystem-effect workflows, package installation, subprocess-based
builds, threads, and network clients are unsupported. The existing bubblewrap
0.4.0 lacks a bounded tmpfs-size option, so an ordinary writable tmpfs would not
supply the required aggregate disk bound. A single bounded file does.

The launcher uses `--unshare-all`, `--die-with-parent`, `--new-session`, drops all
capabilities, remounts the root read-only, and passes only clean locale, time,
home, and work environment values. Bubblewrap adds `PWD=/work`. Stdin is at most
4 KiB. Default bounds are 3 wall-clock seconds, 2 CPU seconds, 256 MiB address
space, 64 KiB combined stdout/stderr, 64 KiB output-file length, 32 file
descriptors, and zero core-file size. Bounds have hard upper limits. Address-space
limits are not total kernel-memory accounting; this is not a cgroup-backed
multi-process workload service.

A standard-library-generated classic BPF syscall allowlist is supplied to
bubblewrap through its seccomp descriptor. It already denies process creation,
sockets, mounts, and namespace creation during trusted Python startup. A trusted
`-I -S -B` Python bootstrap installs a second irreversible filter before importing
or executing any project code. The second filter also denies `execve`,
`execveat`, `prctl`, and resource-limit mutation. Unknown syscalls return EPERM;
non-x86-64 audit architectures are killed and x32 syscall numbers are absent
from the allowlist. This is a small application-specific syscall policy, not a
claim that Python object restrictions provide security. Project code may use
`ctypes`; kernel filtering still applies. No compiler, generated native helper,
new package, or host configuration change is needed.

An activation marker emitted by the trusted bootstrap is removed from captured
stdout. Absence of that marker is an infrastructure failure. A project nonzero
exit is recorded separately from startup failure, timeout, output truncation,
and invalid UTF-8. Exact stdout and stderr bytes are always retained up to the
combined bound. The launcher kills its process group on every path; bubblewrap's
parent-death and PID namespace behavior handle its sandbox child. Project code
cannot fork, clone, spawn threads, create another session, or execute another
program after bootstrap.

## Verified scope and dependency review

The installed tool reviewed here is `/usr/bin/bwrap`, reporting **bubblewrap
0.4.0**, SHA-256
`eb767688b8224d8d3dbe1f8cb30ac3dff9ae8b02ff0452eaec9f94874d4e0011`.
RPM identifies the exact package as **bubblewrap-0.4.0-2.el8_10.x86_64**,
vendor **AlmaLinux**, license `LGPLv2+`. The installed RPM changelog records an
August 30, 2024 backport assisting the Flatpak CVE-2024-42472 fix. This is also
consistent with the [upstream mount-descriptor change](https://github.com/containers/bubblewrap/commit/68e75c3091c87583c28a439b45c45627a94d622c).
It is an existing, non-setuid system executable; this change neither downloads
nor redistributes it. Its source declares **LGPL-2.0-or-later**. Version 0.4.0 is
historical: passing local behavioral checks does not establish that it contains
all later security fixes. Local `rpm -V bubblewrap` reported no mismatches, and `getcap` reported no file
capabilities. The backend refuses setuid/setgid builds and file capabilities and requires
working namespaces and seccomp. Updating or auditing the host tool remains a
host-operator responsibility; this component does not alter it.

Primary references reviewed:

- [Version 0.4.0 usage and namespace model](https://github.com/containers/bubblewrap/blob/v0.4.0/README.md)
- [Version 0.4.0 source, options, parent-death handling, and license header](https://github.com/containers/bubblewrap/blob/v0.4.0/bubblewrap.c)
- [Version 0.4.0 license text](https://github.com/containers/bubblewrap/blob/v0.4.0/COPYING)
- [Kernel seccomp BPF documentation and architecture caveats](https://docs.kernel.org/userspace-api/seccomp_filter.html)
- [Upstream security policy and published advisories](https://github.com/containers/bubblewrap/security)

`tests/test_isolation.py` exercises actual denial of host canary reads and writes,
project writes, work-file creation, root-directory creation, socket creation,
raw fork/clone/clone3/execve/execveat/unshare syscalls, and x32 syscall numbers.
It also checks environment scrubbing, absence of `/proc`, memory/CPU/time/output
bounds, output-file bounds and independent hashing, frozen identity mismatch,
symlink refusal, authorization refusal, and probe failure. Socket creation is
blocked before connection, so these tests send no external network packet.
A bounded raw fork/clone denial test proves process creation is refused without
launching a dangerous fork bomb. Tests skip live execution when the backend is
unavailable; such a skip is not verification. The public API still refuses then.

The [upstream CVE-2020-5291 advisory](https://github.com/containers/bubblewrap/security/advisories/GHSA-j2qp-rvxj-43vj)
identifies the historical 0.4.0 issue as a setuid-mode/userns2 privilege escalation.
This backend rejects setuid/setgid tools and does not expose userns2 options.
The [maintainer security policy](https://github.com/containers/bubblewrap/security)
places responsibility for application confinement on the caller's mount,
namespace, and syscall policy. Here terminal injection is also excluded by
pipes, a new session, and denial of ioctl. These are bounded profile findings,
not a blanket assertion that a historical tool or this host is vulnerability-free.
