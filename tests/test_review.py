import json
from pathlib import Path
import tempfile
import unittest
from renewal_engine.artifacts import inspect
from renewal_engine.recipes import registry, DEFAULT, PATHLIB
from renewal_engine.review import hunks, approve, verify_approval

class ReviewTests(unittest.TestCase):
    def test_selection_staleness_and_candidate_tamper(self):
        parent=Path(__file__).resolve().parents[1]/'.local/tests';parent.mkdir(exist_ok=True,parents=True)
        with tempfile.TemporaryDirectory(dir=parent) as name:
            root=Path(name);source=root/'input';source.mkdir()
            catalog=registry()
            raw=(catalog[DEFAULT]['fixtures'][0]['source']+'\n'*12+catalog[PATHLIB]['fixtures'][0]['source']).encode()
            (source/'both.py').write_bytes(raw)
            run=root/'run';inspect(source,run,[DEFAULT,PATHLIB])
            choices=hunks(run);self.assertEqual(len(choices),2)
            result=approve(run,source,[choices[0]['id']],root/'selected')
            selected=(root/'selected/candidate/both.py').read_bytes()
            self.assertIn(b'read_file',selected);self.assertIn(b's.link_to(t)',selected)
            self.assertEqual((source/'both.py').read_bytes(),raw)
            self.assertEqual(verify_approval(root/'selected',source,result['approval_sha256'])['status'],'VERIFIED APPROVAL')
            (source/'both.py').write_bytes(raw+b'# unrelated edit\n')
            with self.assertRaisesRegex(ValueError,'stale'):approve(run,source,[choices[1]['id']],root/'stale')
            self.assertFalse((root/'stale').exists())
            with self.assertRaisesRegex(ValueError,'stale'):verify_approval(root/'selected',source,result['approval_sha256'])
            (source/'both.py').write_bytes(raw)
            (source/'pyproject.toml').write_text('[project]\nname="changed"\n')
            with self.assertRaisesRegex(ValueError,'stale metadata'):verify_approval(root/'selected',source,result['approval_sha256'])
            (source/'pyproject.toml').unlink()
            (root/'selected/candidate/both.py').write_bytes(selected+b'# changed\n')
            with self.assertRaisesRegex(ValueError,'candidate changed'):verify_approval(root/'selected',source,result['approval_sha256'])
            for ids in [[],['invented'],[choices[0]['id']]*2]:
                with self.assertRaises(ValueError):approve(run,source,ids,root/'bad')
