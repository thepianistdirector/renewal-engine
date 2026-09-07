import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from renewal_engine.execution import run_process, runtime_identity, validate_capture


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        base=Path(__file__).resolve().parents[1]/'.local/tests';base.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base);self.cwd=Path(self.temp.name)

    def tearDown(self):self.temp.cleanup()

    def test_environment_credentials_scrubbed(self):
        with patch.dict(os.environ,{'RENEWAL_TEST_SECRET':'must-not-reach-child','PYTHONPATH':'/invalid'}):
            result=run_process([sys.executable,'-I','-S','-c','import os;print(sorted(os.environ))'],self.cwd)
        self.assertEqual(result['returncode'],0)
        self.assertNotIn('RENEWAL_TEST_SECRET',result['stdout'])
        self.assertNotIn('PYTHONPATH',result['stdout'])

    def test_timeout_and_output_limits(self):
        result=run_process([sys.executable,'-I','-S','-c','while True: pass'],self.cwd,timeout=.1)
        self.assertEqual(result['failure'],'timeout')
        result=run_process([sys.executable,'-I','-S','-c','print("x"*200000)'],self.cwd,output_limit=1024)
        self.assertEqual(result['failure'],'output limit')
        self.assertLessEqual(len(result['stdout'])+len(result['stderr']),1024)

    def test_wrong_runtime_refused(self):
        with self.assertRaisesRegex(ValueError,'unsupported runtime'):
            runtime_identity(Path(sys.executable),'0.0.0',self.cwd)

    def test_raw_bytes_are_not_silently_normalized(self):
        result=run_process([sys.executable,'-I','-S','-c','import sys;sys.stdout.buffer.write(bytes([255]))'],self.cwd)
        self.assertEqual(result['stdout_hex'],'ff')
        self.assertEqual(result['failure'],'invalid UTF-8 output')
        with self.assertRaisesRegex(ValueError,'did not complete'):validate_capture(result)
        literal=run_process([sys.executable,'-I','-S','-c',r'print(r"\xff",end="")'],self.cwd)
        self.assertEqual(literal['stdout'],result['stdout'])
        self.assertNotEqual(literal['stdout_hex'],result['stdout_hex'])
        self.assertIsNone(literal['failure']);validate_capture(literal)
        literal['stdout']='tampered'
        with self.assertRaisesRegex(ValueError,'invalid retained'):validate_capture(literal)

    def test_descendant_killed_after_leader_exits(self):
        code=('import os,time; child=os.fork(); '
              '\nif child == 0: time.sleep(30)'
              '\nelse: os.write(1,str(child).encode()); os._exit(0)')
        result=run_process([sys.executable,'-I','-S','-c',code],self.cwd,timeout=.2)
        self.assertEqual(result['failure'],'timeout')
        child=int(result['stdout'])
        status=Path('/proc')/str(child)/'status'
        deadline=time.monotonic()+1
        while status.exists() and time.monotonic()<deadline:
            if '\nState:\tZ' in status.read_text():break
            time.sleep(.01)
        self.assertTrue(not status.exists() or '\nState:\tZ' in status.read_text(), 'live descendant survived process-group cleanup')


if __name__=='__main__':unittest.main()
