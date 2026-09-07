import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from renewal_engine.artifacts import inspect, snapshot
from renewal_engine.report import render
from renewal_engine.workflow import verify_saved


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        base = Path(__file__).resolve().parents[1] / '.local' / 'tests'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.root = Path(self.temp.name)
        self.source = self.root / 'input'
        self.source.mkdir()
        self.data = b'def load(stream):\n    import configparser\n    p = configparser.ConfigParser()\n    p.readfp(stream)\n    return p\n'
        (self.source/'load.py').write_bytes(self.data)

    def tearDown(self):
        # Test cleanup only, restoring permissions on read-only test snapshots.
        for directory, _, files in os.walk(self.root):
            Path(directory).chmod(0o700)
            for name in files:
                p=Path(directory)/name
                if not p.is_symlink():p.chmod(0o600)
        self.temp.cleanup()

    def test_saved_evidence_and_source_preservation(self):
        out=self.root/'run'
        result=inspect(self.source,out)
        self.assertFalse(result['behavior_measured'])
        self.assertEqual((self.source/'load.py').read_bytes(),self.data)
        self.assertEqual((out/'original/load.py').read_bytes(),self.data)
        self.assertIn(b'read_file',(out/'candidate/load.py').read_bytes())
        self.assertTrue(json.loads((out/'state.json').read_text())['complete'])
        self.assertIn('INSPECTION ONLY',(out/'report.html').read_text())
        before=(out/'manifest.json').read_bytes()
        with self.assertRaises(FileExistsError):inspect(self.source,out)
        self.assertEqual((out/'manifest.json').read_bytes(),before)

    def test_restart_after_interrupted_candidate(self):
        out=self.root/'partial'
        with patch('renewal_engine.artifacts.save_sources',side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):inspect(self.source,out)
        self.assertFalse(json.loads((out/'state.json').read_text())['complete'])
        self.assertEqual((self.source/'load.py').read_bytes(),self.data)
        inspect(self.source,self.root/'restart')
        self.assertFalse(json.loads((out/'state.json').read_text())['complete'])

    def test_symlink_and_overlap_rejected(self):
        (self.source/'link.py').symlink_to(self.source/'load.py')
        with self.assertRaisesRegex(ValueError,'symlink'):snapshot(self.source)
        with self.assertRaisesRegex(ValueError,'outside'):inspect(self.source,self.source/'out')

    def test_source_not_executed_and_shadow_reported(self):
        marker=self.root/'must-not-exist'
        (self.source/'configparser.py').write_text(f'raise RuntimeError({str(marker)!r})\n')
        result=inspect(self.source,self.root/'shadow')
        self.assertFalse(marker.exists())
        row=next(r for r in result['files'] if r['path']=='load.py')
        self.assertFalse(row['changed'])
        self.assertIn('shadows',row['findings'][0]['reason'])

    def test_html_escapes_untrusted_fields(self):
        html=render({'status':'<script>alert(1)</script>','limitations':['<img src=x onerror=alert(1)>']},{'tool_version':'test'})
        self.assertNotIn('<script>',html)
        self.assertNotIn('<img ',html)
        self.assertIn('&lt;script&gt;',html)
        self.assertIn('lang="en"',html)
        self.assertIn('Skip to review',html)

    def test_single_file_shadow_context(self):
        (self.source/'configparser.py').write_text('class ConfigParser:\n    def readfp(self, stream): pass\n')
        result=inspect(self.source/'load.py',self.root/'single')
        self.assertFalse(result['files'][0]['changed'])
        self.assertEqual(result['files'][0]['findings'][0]['status'],'REVIEW NEEDED')

    def test_saved_verification_rejects_false_success(self):
        out=self.root/'saved'
        inspect(self.source,out)
        self.assertFalse(verify_saved(out)['behavior_measured'])
        result=json.loads((out/'results.json').read_text())
        result.update(status='PASS',behavior_measured=True)
        (out/'results.json').write_text(json.dumps(result))
        with self.assertRaisesRegex(ValueError,'cannot claim'):verify_saved(out)


if __name__ == '__main__':unittest.main()
