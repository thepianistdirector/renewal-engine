# Decision 006: provision the reviewed backend in a disposable external runner

The first approved public 0.5 verification job, 34247933729, failed its initial
`test -x /usr/bin/bwrap` prerequisite. No product test executed there. Its failed
record is retained in `docs/evidence/0.5/external-attempt-1.json`.

The owner then approved the concrete recovery and all needed dependencies. The
second workflow, commit `249b33bc31dd747a46e194c62ca5757ff9426987`, copies one
checksum-pinned ordinary executable into the disposable GitHub-hosted Ubuntu
24.04 runner. It does not modify the shared VPS or any published product asset.

## Exact dependency and graph

Ubuntu Noble amd64 `bubblewrap` **0.9.0-1ubuntu0.1**, from the official security
archive, is 50,178 bytes. Its package SHA-256 is
`1b506492bd9c7fd0cdb4f02ac822f1d3e336b0aead5113c1239baf8db5db562a`.
The extracted executable SHA-256 is
`52231e1caf55bcbc667b269f49c63599a6f7db4767ae6a039580d0ff853db712`.

The exact package control and read-only ELF inspection agree on its dependencies:
`libc6 >= 2.38`, `libcap2 >= 1:2.10`, and `libselinux1 >= 3.1~`. The workflow checks
that these libraries are already compatible. It installs or upgrades none of them;
missing prerequisites remain failures requiring an evidenced dependency resolution.
`procps` is recommended by the package, not required or installed by this workflow.
The executable's exact copyright file declares LGPL-2.0-or-later.

The package was downloaded and inspected without executing its contents on the
VPS. Its post-install hook would apply a sysctl file. This workflow instead uses
`dpkg-deb --extract` in the job workspace and copies **only** `/usr/bin/bwrap`, with
mode 0755, after refusing an existing file or symlink. It does not run maintainer
hooks, install sysctl files, alter AppArmor, use setuid or grant file capabilities.
Copyright and other package files remain in the disposable job workspace.

Ubuntu's security changelog records the mount-descriptor backport assisting the
CVE-2024-42472 fix. This records the reviewed version and provenance; it does not
assert the tool or environment is free from vulnerabilities.

## Boundaries and replacement

The job retains the published source/CLI hashes, dedicated official-source Python
builds, the original product checks, negative controls and real interruption tests.
Every isolated execution must still pass live denial probes. No missing dependency,
namespace restriction or probe failure authorizes an unsandboxed fallback.

The runner has empty repository-token permissions. Public Ubuntu downloads send
no source or credentials. Standard public-repository runner scope and the existing
30-minute job limit apply; no paid service, account or quota expansion is requested.
The operation is discarded with the disposable runner. Replacement is a separately
reviewed compatible backend or environment, not a host-security bypass. The first
failure and all immutable public 0.5 assets remain available for audit.

The prepared shell blocks passed syntax checks. Job
https://github.com/thepianistdirector/renewal-engine/actions/runs/34249603564
successfully completed this provisioning and verified the public downloads; its
final product result is recorded separately after completion.

## Primary references

- [Ubuntu package and dependencies](https://packages.ubuntu.com/ca/noble/bubblewrap)
- [Exact Ubuntu download digest](https://packages.ubuntu.com/nl/noble/amd64/bubblewrap/download)
- [Package file inventory](https://packages.ubuntu.com/noble/amd64/bubblewrap/filelist)
- [Ubuntu security changelog](https://launchpad.net/ubuntu/+source/bubblewrap/+changelog)
- [Upstream 0.9.0 license](https://github.com/containers/bubblewrap/blob/v0.9.0/COPYING)

## Compatible-runner follow-up

The Ubuntu 24.04 attempt completed both official interpreter builds and the
migration/negative-control checks, but isolation failed. A diagnostic wrapper
retained the unchanged launcher's real output:
`bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
It failed before the isolation bootstrap marker or any selected project execution.
The independent trusted-reference SIGINT/restart checks passed. This does not
establish the precise kernel-policy owner; no AppArmor or sysctl change is inferred
as authorized or performed.

Within the owner's expanded dependency authorization, the next attempt selects
an ordinary GitHub-hosted **Ubuntu 22.04** environment with its compatible official
Jammy backend. The product's Linux x86_64 profile and every denial check remain
unchanged; only the disposable runner image and matching dependency bytes change.
The Ubuntu 24.04 failure remains an explicit unsupported observation.

The reviewed Jammy amd64 package is `bubblewrap_0.6.1-1ubuntu0.1_amd64.deb`, 46,300
bytes, package SHA-256
`f75c835d6871d1b36370e12ee82940334b2a9f94efc7b959b5b236447e89743d`.
Its executable SHA-256 is
`d78807229d616606e339c5988392b9e0ab4a6a6998fa51e4590837f426a12fca`.
The digest was read from the official `jammy-security/main/binary-amd64/Packages.xz`
index and checked against the exact downloaded package. Its control, LGPL-2+ main
license, maintainer scripts and ELF dependencies were inspected without execution.
Dependencies are libc6 >= 2.34, libcap2 >= 1:2.10 and libselinux1 >= 3.1~. The
old-Flatpak package conflict is not relevant to this single-purpose job, which
neither installs nor executes Flatpak. No package hooks, sysctl files, setuid or
security-policy edits are used. A pre-existing backend is retained only if its
bytes match the reviewed executable; it is never silently overwritten.

Sources: [Ubuntu Jammy package](https://packages.ubuntu.com/ca/jammy/bubblewrap)
and [official security package index](https://security.ubuntu.com/ubuntu/dists/jammy-security/main/binary-amd64/Packages.xz).

## Observed final result

The Ubuntu 22.04 workflow initially exposed a Python prerequisite-order error:
the system interpreter was 3.10 and the installer correctly required >=3.11.
The workflow was corrected to build the exact declared runtimes first and install
using its dedicated Python 3.12.14. No product guard was bypassed.

Final commit `f83b31c6abc669a258307f0469a921003f58dcb6`, run 34251350280, passed the
27 public CLI checks, all nine live isolation checks and real interruption/recovery.
The public CLI independently verified sixteen retained results/refusals. Exact
hashes, platform, captures and prior failures are in docs/evidence/0.5. No further
dependency installation or repeated job is needed for this declared profile.
