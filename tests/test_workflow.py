"""Orchestration tests use synthetic observations, never original-runtime proof."""

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from renewal_engine.workflow import demo, trusted_assets, verify_saved


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        base=Path(__file__).resolve().parents[1]/'.local/tests';base.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base);self.root=Path(self.temp.name)
        self.policy=json.loads(trusted_assets()[0]['policy.json'])

    def tearDown(self):
        for directory,_,files in os.walk(self.root):
            Path(directory).chmod(0o700)
            for name in files:(Path(directory)/name).chmod(0o600)
        self.temp.cleanup()

    def observe(self,argv,cwd,data):
        case=json.loads(data);old=Path(argv[-1]).parent.name=='original'
        run=cwd.parents[2]
        self.assertTrue((run/'manifest.json').is_file())
        if old:self.assertFalse((run/'candidate').exists())
        (cwd/'input.ini').write_bytes(case['content'].encode())
        record={'stdout':'synthetic observation only','exception':None,
                'warnings':[{**self.policy['warning'],'lineno':self.policy['warning_lines'][case['mode']]}] if old else [],
                'effects':{'stream_closed_after_call':False}}
        stdout=json.dumps(record)
        return {'returncode':0,'failure':None,'stderr':'','stdout':stdout,
                'stdout_hex':stdout.encode().hex(),'stderr_hex':''}

    def synthetic_run(self,out):
        with patch('renewal_engine.workflow.runtime_identity',side_effect=self.identity), \
             patch('renewal_engine.workflow.run_process',side_effect=self.observe):
            return demo(out,Path('/unused/baseline'),Path('/unused/target'))

    def identity(self,executable,expected,cwd):
        return {'implementation':'CPython','version':expected,'platform':'Linux','machine':'x86_64',
                'build':'SYNTHETIC UNIT TEST DATA; not runtime evidence','readfp':expected.startswith('3.11.'),
                'configparser_sha256':'0'*64,'executable_sha256':'0'*64}

    def test_orchestration_and_reopen_synthetic_only(self):
        out=self.root/'run';result=self.synthetic_run(out)
        self.assertEqual(len(result['cases']),12)
        self.assertEqual(verify_saved(out)['result'],'PASS')

    def test_false_summary_and_changed_files_rejected(self):
        for mutation in ['status','input','process','harness','observation','runtime']:
            with self.subTest(mutation=mutation):
                out=self.root/mutation;self.synthetic_run(out)
                case=out/'observations/candidate/valid-default'
                if mutation=='status':
                    r=json.loads((out/'results.json').read_text());r['status']='REGRESSION';(out/'results.json').write_text(json.dumps(r))
                elif mutation=='input':(case/'input.ini').write_text('changed')
                elif mutation=='process':(case/'process.json').unlink()
                elif mutation=='observation':
                    r=json.loads((case/'observation.json').read_text());r['stdout']='changed';(case/'observation.json').write_text(json.dumps(r))
                elif mutation=='runtime':
                    f=out/'manifest.json';f.chmod(0o600);r=json.loads(f.read_text());r['runtimes']['original']['version']='3.12.14';f.write_text(json.dumps(r))
                else:
                    f=out/'reference/harness.py';f.chmod(0o600);f.write_text('changed')
                with self.assertRaises((ValueError,OSError)):verify_saved(out)

    def test_interruption_during_comparison_retains_evidence(self):
        out=self.root/'interrupted'
        with patch('renewal_engine.workflow.runtime_identity',side_effect=self.identity), \
             patch('renewal_engine.workflow.run_process',side_effect=self.observe), \
             patch('renewal_engine.workflow.compare_case',side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):demo(out,Path('/unused/a'),Path('/unused/b'))
        self.assertFalse(json.loads((out/'state.json').read_text())['complete'])
        self.assertTrue((out/'observations/original/valid-default/process.json').is_file())
        self.assertEqual((out/'original/program.py').read_bytes(),trusted_assets()[0]['program.py'])
        self.synthetic_run(self.root/'restart')
        self.assertFalse(json.loads((out/'state.json').read_text())['complete'])


if __name__=='__main__':unittest.main()
