"""Live denial tests use tiny resources and create no external network traffic."""
from dataclasses import replace
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from renewal_engine.isolation import (IsolationLimits, IsolationRefused, execute_python,
                                     freeze_runtime, probe_isolation, _filter)


class IsolationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.probe = probe_isolation()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='renewal-isolation-test-')
        self.root = Path(self.temp.name)
        self.project = self.root / 'project'
        self.project.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def run_source(self, source, **kwargs):
        if not self.probe['verified']:
            self.skipTest('verified isolation unavailable: ' + self.probe['failure'])
        (self.project / 'main.py').write_text(source)
        return execute_python(self.project, 'main.py', authorized=True, **kwargs)

    def test_authorization_required_before_discovery(self):
        with patch('renewal_engine.isolation.freeze_runtime', side_effect=AssertionError):
            with self.assertRaisesRegex(IsolationRefused, 'authorization'):
                execute_python(self.project, 'main.py')

    def test_probe_failure_refuses_without_execution(self):
        with patch('renewal_engine.isolation.probe_isolation', return_value={'verified': False, 'failure': 'test refusal'}):
            with self.assertRaisesRegex(IsolationRefused, 'test refusal'):
                execute_python(self.project, 'main.py', authorized=True)

    def test_denial_probe(self):
        if not self.probe['verified']:
            self.skipTest(self.probe['failure'])
        self.assertEqual(len(self.probe['checks']), 9)
        self.assertTrue(all(self.probe['checks'].values()))

    def test_host_canary_read_write_environment_and_project_readonly(self):
        canary = self.root / 'canary'
        canary.write_text('canary')
        source = '''import os
for path in [%r, '/project/main.py', '/work/new', '/new']:
    try:
        open(path, 'w').write('changed')
        print('UNEXPECTED')
    except OSError:
        print('denied')
try:
    open(%r).read()
    print('UNEXPECTED')
except OSError:
    print('denied')
assert 'RENEWAL_CANARY_SECRET' not in os.environ
assert not os.path.exists('/proc')
''' % (str(canary), str(canary))
        with patch.dict(os.environ, {'RENEWAL_CANARY_SECRET': 'test-value'}):
            result = self.run_source(source)
        self.assertEqual(result['stdout'], 'denied\n' * 5)
        self.assertEqual(canary.read_text(), 'canary')
        self.assertEqual((self.project / 'main.py').read_text(), source)
        self.assertEqual(result['snapshot_manifest'], [{'path':'main.py', 'type':'file', 'size':len(source.encode()), 'sha256':hashlib.sha256(source.encode()).hexdigest()}])
        self.assertEqual(result['returncode'], 0)

    def test_syscall_fork_clone_exec_socket_denied(self):
        # Raw syscalls exercise kernel denial independently of Python wrappers.
        result = self.run_source('''import ctypes,errno
libc=ctypes.CDLL(None,use_errno=True)
for syscall in [56,57,58,59,41,272,435,322,0x40000039]:
    ctypes.set_errno(0)
    assert libc.syscall(syscall,0,0,0,0,0,0)==-1
    assert ctypes.get_errno()==errno.EPERM
print('denied')
''')
        self.assertEqual(result['returncode'], 0, result['stderr'])
        self.assertEqual(result['stdout'], 'denied\n')

    def test_writable_file_bound_and_independent_capture(self):
        result = self.run_source("with open('/work/output','wb') as f: f.write(b'x'*4096); f.flush()",
                                 limits=IsolationLimits(file_bytes=1024))
        self.assertLessEqual(result['work_output_size'], 1024)
        raw = bytes.fromhex(result['work_output_hex'])
        self.assertEqual(result['work_output_sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(raw), 1024)
        self.assertNotEqual(result['returncode'], 0)
        self.assertIsNone(result['failure'])

    def test_timeout_and_output_bounds(self):
        result = self.run_source('while True: pass', limits=IsolationLimits(timeout=.2))
        self.assertEqual(result['failure'], 'timeout')
        result = self.run_source("while True: print('x'*4096)", limits=IsolationLimits(output_bytes=1024))
        self.assertEqual(result['failure'], 'output limit')
        self.assertLessEqual(len(bytes.fromhex(result['stdout_hex'])) + len(bytes.fromhex(result['stderr_hex'])), 1024)

    def test_memory_and_cpu_bounds(self):
        result = self.run_source("x=bytearray(256*1024*1024)",
                                 limits=IsolationLimits(memory_bytes=64*1024*1024))
        self.assertNotEqual(result['returncode'], 0)
        self.assertIn('MemoryError', result['stderr'])
        result = self.run_source('while True: pass', limits=IsolationLimits(timeout=3, cpu_seconds=1))
        self.assertNotEqual(result['returncode'], 0)
        self.assertIsNone(result['failure'])

    def test_nonzero_is_not_infrastructure_failure(self):
        result = self.run_source('raise SystemExit(7)')
        self.assertEqual(result['returncode'], 7)
        self.assertIsNone(result['failure'])
        self.assertTrue(result['boundary_activated'])

    def test_symlink_and_entrypoint_escape_refused(self):
        (self.project / 'escape').symlink_to('/etc/passwd')
        with self.assertRaises(IsolationRefused):
            self.run_source('print(42)')
        (self.project / 'escape').unlink()
        with self.assertRaises(IsolationRefused):
            execute_python(self.project, '../other.py', authorized=True)

    def test_runtime_identity_tamper_refused(self):
        runtime = freeze_runtime()
        changed = replace(runtime, executable_sha256='0'*64)
        result = probe_isolation(changed)
        self.assertFalse(result['verified'])
        self.assertIn('identity changed', result['failure'])

    def test_seccomp_architecture_guard_and_default_deny(self):
        import struct
        rows = list(struct.iter_unpack('HBBI', _filter()))
        self.assertEqual(rows[:3], [(0x20,0,0,4),(0x15,1,0,0xC000003E),(0x06,0,0,0x80000000)])
        self.assertEqual(rows[-1], (0x06,0,0,0x50001))
