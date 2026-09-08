"""Narrow Linux/x86-64 CPython execution boundary; no unsandboxed fallback.

The caller must trust the runtime and supply a private, immutable project snapshot.
Only /work/output is writable. This deliberately excludes general build tools.
"""
from __future__ import annotations
from .jsonio import loads as strict_loads

from dataclasses import dataclass, asdict
import hashlib
import errno
import json
import os
from pathlib import Path
import platform
import resource
import selectors
import signal
import stat
import struct
import subprocess
import sys
import tempfile
import time


class IsolationRefused(ValueError):
    """The requested boundary cannot be established."""


@dataclass(frozen=True)
class IsolationLimits:
    timeout: float = 3.0
    output_bytes: int = 65536
    memory_bytes: int = 256 * 1024 * 1024
    cpu_seconds: int = 2
    file_bytes: int = 65536

    def validate(self):
        bounds = ((self.timeout, .05, 30), (self.output_bytes, 1, 1048576),
                  (self.memory_bytes, 32 * 1024 * 1024, 512 * 1024 * 1024),
                  (self.cpu_seconds, 1, 10), (self.file_bytes, 1, 1048576))
        if any(type(v) not in (int, float) or not lo <= v <= hi for v, lo, hi in bounds):
            raise IsolationRefused('limits outside supported bounds')
        if any(type(v) is not int for v in (self.output_bytes, self.memory_bytes,
                                           self.cpu_seconds, self.file_bytes)):
            raise IsolationRefused('resource limits must be integers')


@dataclass(frozen=True)
class RuntimeIdentity:
    executable: str
    prefix: str
    executable_sha256: str
    bwrap_sha256: str
    runtime_tree_sha256: str


def _sha(path):
    with open(path, 'rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def freeze_runtime(executable=None, prefix=None):
    """Freeze caller-trusted runtime inputs; never execute discovery from a project."""
    exe = Path(executable or sys.executable).resolve(strict=True)
    base = Path(prefix or sys.base_prefix).resolve(strict=True)
    if base in (Path('/'), Path('/home'), Path('/usr'), Path('/usr/local')):
        raise IsolationRefused('a dedicated CPython runtime prefix is required')
    if not exe.is_relative_to(base):
        raise IsolationRefused('runtime executable must be inside its dedicated prefix')
    return RuntimeIdentity(str(exe), str(base), _sha(exe), _sha('/usr/bin/bwrap'), _runtime_tree(base))


# Linux x86-64 syscall numbers. Default EPERM; unknown ABIs are killed.
# No clone/fork/vfork/exec, sockets, namespace/mount, ptrace, io_uring, IPC,
# device ioctl, file linking, directory creation, or resource-limit mutation.
_ALLOWED = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            17, 19, 20, 21, 23, 24, 25, 28, 35, 39, 60, 63, 72, 74,
            75, 77, 78, 79, 80, 81, 89, 95, 96, 97, 98, 99, 102,
            104, 107, 108, 110, 111, 131, 158, 186, 202, 204, 217, 218,
            228, 229, 230, 231, 234, 257, 262, 267, 270, 271, 273,
            302, 318, 332, 334)
# prlimit64 (302) is intentionally omitted below: it can raise soft limits.
_ALLOWED = tuple(n for n in _ALLOWED if n != 302)


def _filter(bootstrap=False):
    instructions = [(0x20, 0, 0, 4), (0x15, 1, 0, 0xC000003E),
                    (0x06, 0, 0, 0x80000000), (0x20, 0, 0, 0)]
    for number in _ALLOWED + ((59, 61, 157, 247, 302) if bootstrap else ()):
        instructions += [(0x15, 0, 1, number), (0x06, 0, 0, 0x7FFF0000)]
    instructions += [(0x06, 0, 0, 0x00050001)]
    return b''.join(struct.pack('HBBI', *row) for row in instructions)


_READY = b'RENEWAL_ISOLATION_READY\n'

_BOOTSTRAP = r'''
import ctypes, os, runpy, struct, sys
class Filter(ctypes.Structure):
    _fields_ = [('code', ctypes.c_ushort), ('jt', ctypes.c_ubyte), ('jf', ctypes.c_ubyte), ('k', ctypes.c_uint)]
class Program(ctypes.Structure):
    _fields_ = [('len', ctypes.c_ushort), ('filter', ctypes.POINTER(Filter))]
raw = bytes.fromhex(sys.argv[1])
filters = (Filter * (len(raw)//8)).from_buffer_copy(raw)
program = Program(len(filters), filters)
libc = ctypes.CDLL(None, use_errno=True)
if libc.prctl(38, 1, 0, 0, 0) != 0 or libc.prctl(22, 2, ctypes.byref(program), 0, 0) != 0:
    raise SystemExit('isolation seccomp activation failed')
os.write(1, b'RENEWAL_ISOLATION_READY\n')
# The irreversible kernel filter is active before any project import.
sys.path.insert(0, '/project')
sys.argv = [sys.argv[2]]
runpy.run_path(sys.argv[0], run_name='__main__')
'''


def _check_runtime(runtime):
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise IsolationRefused('only Linux x86_64 is supported')
    if platform.python_implementation() != 'CPython':
        raise IsolationRefused('CPython is required')
    tool = Path('/usr/bin/bwrap')
    if not tool.is_file() or tool.stat().st_mode & (stat.S_ISUID | stat.S_ISGID):
        raise IsolationRefused('non-setuid /usr/bin/bwrap is required')
    try:
        capabilities = os.getxattr(tool, 'security.capability')
    except OSError as exc:
        if exc.errno not in (errno.ENODATA, errno.ENOTSUP):
            raise IsolationRefused('cannot verify bubblewrap file capabilities') from exc
        capabilities = b''
    if capabilities:
        raise IsolationRefused('bubblewrap file capabilities are not supported')
    if runtime != freeze_runtime(runtime.executable, runtime.prefix):
        raise IsolationRefused('runtime or bubblewrap identity changed')


def _resource_limits(limits):
    def apply():
        for kind, value in ((resource.RLIMIT_CPU, limits.cpu_seconds),
                            (resource.RLIMIT_AS, limits.memory_bytes),
                            (resource.RLIMIT_FSIZE, limits.file_bytes),
                            (resource.RLIMIT_NOFILE, 32), (resource.RLIMIT_CORE, 0)):
            resource.setrlimit(kind, (value, value))
    return apply


def _execute_python(snapshot, entrypoint, *, authorized=False, runtime=None,
                   limits=IsolationLimits(), data=b''):
    """Execute a relative .py entrypoint, explicitly authorized by the caller.

    The snapshot/runtime must not be concurrently modified by a trusted host actor.
    A project cannot execute child processes, create sockets, or create work files.
    """
    if authorized is not True:
        raise IsolationRefused('explicit project-execution authorization is required')
    limits.validate()
    if not isinstance(data, bytes) or len(data) > 4096:
        raise IsolationRefused('stdin must be at most 4096 bytes')
    runtime = runtime or freeze_runtime()
    _check_runtime(runtime)
    project = Path(snapshot).resolve(strict=True)
    relative = Path(entrypoint)
    if relative.is_absolute() or '..' in relative.parts or relative.suffix != '.py':
        raise IsolationRefused('entrypoint must be a relative Python file')
    target = (project / relative).resolve(strict=True)
    if not project.is_dir() or not target.is_relative_to(project) or not target.is_file():
        raise IsolationRefused('entrypoint escapes the project snapshot')
    with tempfile.TemporaryDirectory(prefix='renewal-isolation-') as temp:
        root = Path(temp)
        copied = root / 'project'
        copied.mkdir()
        snapshot_manifest = _copy_snapshot(project, copied)
        project = copied
        work = root / 'work'
        work.mkdir()
        output = work / 'output'
        output.touch()
        with tempfile.TemporaryFile() as seccomp:
            seccomp.write(_filter(bootstrap=True)); seccomp.flush(); seccomp.seek(0)
            args = ['/usr/bin/bwrap', '--unshare-all', '--die-with-parent', '--new-session',
                    '--cap-drop', 'ALL', '--ro-bind', runtime.prefix, '/runtime']
            for directory in ('/lib', '/lib64', '/usr/lib'):
                if Path(directory).exists():
                    args += ['--ro-bind', directory, directory]
            args += ['--ro-bind', str(project), '/project', '--ro-bind', str(work), '/work',
                     '--bind', str(output), '/work/output', '--chdir', '/work',
                     '--remount-ro', '/', '--seccomp', str(seccomp.fileno()), '--',
                     '/runtime/' + str(Path(runtime.executable).relative_to(runtime.prefix)),
                     '-I', '-S', '-B', '-c', _BOOTSTRAP, _filter().hex(), '/project/' + str(relative)]
            result = _capture(args, seccomp.fileno(), limits, data)
        output_bytes = output.read_bytes()
        result['work_output_hex'] = output_bytes.hex()
        result['work_output_sha256'] = hashlib.sha256(output_bytes).hexdigest()
        result['work_output_size'] = len(output_bytes)
        result['isolation'] = 'bubblewrap-seccomp-python-v1'
        result['runtime'] = asdict(runtime)
        result['snapshot_manifest'] = snapshot_manifest
        result['snapshot_sha256'] = hashlib.sha256(json.dumps(snapshot_manifest, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        return result


def _capture(args, seccomp_fd, limits, data):
    environment = {'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', 'TZ': 'UTC', 'HOME': '/nonexistent', 'TMPDIR': '/work'}
    buffers = {'stdout': bytearray(), 'stderr': bytearray()}
    failure = None
    process = subprocess.Popen(args, env=environment, cwd='/', stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True, close_fds=True, pass_fds=(seccomp_fd,),
                               preexec_fn=_resource_limits(limits))
    deadline = time.monotonic() + limits.timeout
    try:
        try:
            process.stdin.write(data); process.stdin.close()
        except BrokenPipeError:
            pass
        with selectors.DefaultSelector() as selector:
            for name in buffers:
                selector.register(getattr(process, name), selectors.EVENT_READ, name)
            while selector.get_map() and not failure:
                if time.monotonic() >= deadline:
                    failure = 'timeout'; break
                for key, _ in selector.select(min(.05, max(0, deadline-time.monotonic()))):
                    chunk = os.read(key.fileobj.fileno(), 8192)
                    if not chunk:
                        selector.unregister(key.fileobj); continue
                    remaining = limits.output_bytes + len(_READY) - sum(map(len, buffers.values()))
                    buffers[key.data].extend(chunk[:remaining])
                    if len(chunk) > remaining:
                        failure = 'output limit'; break
        if not failure:
            try:
                process.wait(timeout=max(.01, deadline-time.monotonic()))
            except subprocess.TimeoutExpired:
                failure = 'timeout'
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        for stream in (process.stdin, process.stdout, process.stderr):
            stream.close()
    ready = buffers['stdout'].startswith(_READY)
    if ready:
        del buffers['stdout'][:len(_READY)]
    else:
        failure = 'isolation startup failed'
        remaining = limits.output_bytes
        for raw in buffers.values():
            del raw[remaining:]
            remaining -= len(raw)
    result = {'returncode': process.returncode, 'failure': failure, 'boundary_activated': ready}
    for name, raw in buffers.items():
        result[name + '_hex'] = raw.hex()
        try:
            result[name] = raw.decode('utf-8')
        except UnicodeDecodeError:
            result[name] = raw.decode('utf-8', 'backslashreplace')
            result['failure'] = result['failure'] or 'invalid UTF-8 output'
    return result


def probe_isolation(runtime=None):
    """Run trusted denial probes; a failed probe never enables a fallback."""
    try:
        runtime = runtime or freeze_runtime()
        with tempfile.TemporaryDirectory(prefix='renewal-probe-') as temp:
            project = Path(temp) / 'project'; project.mkdir()
            canary = Path(temp) / 'host-canary'; canary.write_text('not-a-secret')
            source = "import os,socket,json,sys\nchecks={}\n"
            source += "for name, action in [('host_read', lambda:open(%r).read()), ('host_write', lambda:open(%r,'w')), ('network',lambda:socket.socket()), ('fork',lambda:os.fork()), ('exec',lambda:os.execv(sys.executable,[sys.executable,'-V'])), ('work_create',lambda:open('/work/new','w')), ('root_create',lambda:os.mkdir('/new'))]:\n try:\n  action();checks[name]=False\n except OSError:\n  checks[name]=True\n" % (str(canary), str(canary))
            source += "checks['environment']=not any(k not in {'LANG','LC_ALL','TZ','HOME','TMPDIR','PWD'} for k in os.environ)\nchecks['no_proc']=not os.path.exists('/proc')\nprint(json.dumps(checks,sort_keys=True))\n"
            (project / 'probe.py').write_text(source)
            result = _execute_python(project, 'probe.py', authorized=True, runtime=runtime)
            checks = strict_loads(result['stdout']) if result['returncode'] == 0 and not result['failure'] else {}
            verified = len(checks) == 9 and all(checks.values()) and canary.read_text() == 'not-a-secret'
            return {'available': verified, 'verified': verified, 'checks': checks,
                    'runtime': asdict(runtime), 'failure': None if verified else 'isolation denial probe failed'}
    except (OSError, ValueError, TypeError) as exc:
        return {'available': False, 'verified': False, 'checks': {}, 'failure': str(exc)}


def _copy_snapshot(source, destination):
    """Copy through O_NOFOLLOW directory descriptors with strict aggregate bounds."""
    budget = [0, 0]
    manifest = []
    def copy_directory(fd, dest, depth):
        if depth > 32:
            raise IsolationRefused('snapshot nesting exceeds 32')
        with os.scandir(fd) as entries:
            for entry in entries:
                name = entry.name
                budget[0] += 1
                if budget[0] > 512:
                    raise IsolationRefused('snapshot exceeds 512 entries')
                info = os.stat(name, dir_fd=fd, follow_symlinks=False)
                if stat.S_ISDIR(info.st_mode):
                    child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                    try:
                        (dest / name).mkdir()
                        manifest.append({'path': (dest / name).relative_to(destination).as_posix(),
                                         'type': 'directory', 'size': 0, 'sha256': None})
                        copy_directory(child, dest / name, depth+1)
                    finally:
                        os.close(child)
                elif stat.S_ISREG(info.st_mode):
                    child = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
                    with os.fdopen(child, 'rb') as stream:
                        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                            raise IsolationRefused('snapshot entry changed type')
                        data = stream.read(16 * 1024 * 1024 - budget[1] + 1)
                    budget[1] += len(data)
                    if budget[1] > 16 * 1024 * 1024:
                        raise IsolationRefused('snapshot exceeds 16 MiB')
                    (dest / name).write_bytes(data)
                    manifest.append({'path': (dest / name).relative_to(destination).as_posix(),
                                     'type': 'file', 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
                else:
                    raise IsolationRefused('snapshot contains a special file or symlink')
    fd = os.open(source, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        copy_directory(fd, destination, 0)
    finally:
        os.close(fd)
    return sorted(manifest, key=lambda item: item['path'])


def execute_python(snapshot, entrypoint, *, authorized=False, runtime=None,
                   limits=IsolationLimits(), data=b''):
    """Verify the denial probes before each explicitly authorized execution."""
    if authorized is not True:
        raise IsolationRefused('explicit project-execution authorization is required')
    runtime = runtime or freeze_runtime()
    evidence = probe_isolation(runtime)
    if not evidence['verified']:
        raise IsolationRefused(evidence['failure'])
    result = _execute_python(snapshot, entrypoint, authorized=True, runtime=runtime,
                             limits=limits, data=data)
    result['probe'] = evidence
    return result


def _runtime_tree(base):
    digest = hashlib.sha256()
    for path in sorted(base.rglob('*')):
        relative = path.relative_to(base).as_posix()
        digest.update(relative.encode() + b'\0')
        if path.is_symlink():
            if not path.resolve(strict=True).is_relative_to(base):
                raise IsolationRefused('runtime symlink escapes its prefix')
            digest.update(b'L' + os.readlink(path).encode() + b'\0')
        elif path.is_file():
            digest.update(b'F' + bytes.fromhex(_sha(path)))
        elif path.is_dir():
            digest.update(b'D')
        else:
            raise IsolationRefused('runtime contains a special file')
    return digest.hexdigest()
