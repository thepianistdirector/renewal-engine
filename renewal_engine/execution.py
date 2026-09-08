"""Bounded invocation of approved runtimes. Process limits are not a sandbox."""

from __future__ import annotations
from .jsonio import loads as strict_loads

import json
import os
from pathlib import Path
import resource
import re
import selectors
import signal
import subprocess
import time

from .transformation import digest


def _limits():
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def run_process(argv: list[str], cwd: Path, data: bytes = b"", timeout=10, output_limit=131072):
    if os.name != "posix":
        raise ValueError("0.1 execution is verified only on the declared Linux environment")
    if len(data) > 4096:
        raise ValueError("trusted case input exceeds the atomic 4 KiB pipe envelope")
    environment = {"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC", "TMPDIR": str(cwd)}
    process = subprocess.Popen(argv, cwd=cwd, env=environment, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True, preexec_fn=_limits, close_fds=True)
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    failure = None
    try:
        try:
            process.stdin.write(data)
            process.stdin.close()
        except BrokenPipeError:
            pass
        deadline = time.monotonic() + timeout
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ, "stdout")
            selector.register(process.stderr, selectors.EVENT_READ, "stderr")
            while selector.get_map():
                if time.monotonic() >= deadline:
                    failure = "timeout"
                    break
                for key, _ in selector.select(min(.1, max(0, deadline - time.monotonic()))):
                    chunk = os.read(key.fileobj.fileno(), 8192)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    remaining = output_limit - sum(map(len, buffers.values()))
                    buffers[key.data].extend(chunk[:max(0, remaining)])
                    if len(chunk) > remaining:
                        failure = "output limit"
                        break
                if failure:
                    break
        if not failure:
            try:
                process.wait(timeout=max(.01, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                failure = "timeout"
    finally:
        # Clean up descendants even when the direct child already exited.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        for stream in (process.stdin, process.stdout, process.stderr):
            stream.close()
    result = {"returncode": process.returncode, "failure": failure}
    for name, raw in buffers.items():
        result[name + "_hex"] = raw.hex()
        try:
            result[name] = raw.decode("utf-8")
        except UnicodeDecodeError:
            # Keep exact bytes and an explicit failed observation; an invalid
            # byte must never become equivalent to a literal backslash escape.
            result[name] = raw.decode("utf-8", errors="backslashreplace")
            result["failure"] = result["failure"] or "invalid UTF-8 output"
    return result


def validate_capture(record):
    """Check retained raw bytes agree with a successful decoded capture."""
    if record.get("failure") or record.get("returncode") != 0 or record.get("stderr"):
        raise ValueError("saved process did not complete successfully")
    for name in ("stdout", "stderr"):
        try:
            raw = bytes.fromhex(record[name + "_hex"])
            if raw.decode("utf-8") != record[name]:
                raise ValueError("decoded capture differs from retained raw bytes")
        except (KeyError, TypeError, UnicodeDecodeError, ValueError) as exc:
            raise ValueError("invalid retained " + name + " capture") from exc


def runtime_identity(executable: Path, expected: str, cwd: Path):
    executable = executable.resolve(strict=True)
    code = ("import sys,platform,json,configparser,hashlib,pathlib; "
            "print(json.dumps({'implementation':platform.python_implementation(),"
            "'version':platform.python_version(),'build':sys.version,"
            "'platform':platform.system(),'machine':platform.machine(),"
            "'configparser_sha256':hashlib.sha256(pathlib.Path(configparser.__file__).read_bytes()).hexdigest(),"
            "'pathlib_sha256':hashlib.sha256(pathlib.Path(pathlib.__file__).read_bytes()).hexdigest(),"
            "'readfp':hasattr(configparser.ConfigParser,'readfp')}))")
    observed = run_process([str(executable), "-I", "-S", "-B", "-X", "utf8", "-c", code], cwd)
    if observed["failure"] or observed["returncode"] != 0 or observed["stderr"]:
        raise ValueError("runtime identity probe failed: " + json.dumps(observed))
    identity = strict_loads(observed["stdout"])
    if (identity["implementation"] != "CPython" or identity["version"] != expected
            or identity["platform"] != "Linux" or identity["machine"] != "x86_64"):
        raise ValueError("unsupported runtime: expected Linux CPython " + expected + "; observed " + json.dumps(identity))
    if identity["readfp"] != expected.startswith("3.11."):
        raise ValueError("runtime does not expose the expected original API boundary")
    identity["executable_sha256"] = digest(executable.read_bytes())
    return identity


def validate_runtime_record(identity, expected):
    """Validate a retained identity's declared matrix, not its authenticity."""
    if (identity.get("implementation") != "CPython" or identity.get("version") != expected
            or identity.get("platform") != "Linux" or identity.get("machine") != "x86_64"
            or identity.get("readfp") is not expected.startswith("3.11.")
            or not isinstance(identity.get("build"), str) or not identity["build"]):
        raise ValueError("saved runtime identity does not match the declared supported matrix")
    for name in ("configparser_sha256", "executable_sha256"):
        if not isinstance(identity.get(name), str) or not re.fullmatch(r"[0-9a-f]{64}", identity[name]):
            raise ValueError("saved runtime identity lacks a valid " + name)
