import json
from pathlib import Path
import tempfile
import unittest
from renewal_engine.session import compare_files,export_summary
from renewal_engine.workflow import verify_saved

class SessionTests(unittest.TestCase):
    def test_strict_saved_result_and_private_export(self):
        parent=Path(__file__).resolve().parents[1]/'.local/tests';parent.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as tmp:
            root=Path(tmp)
            original=[{'v':True,'secret':'PRIVATE-CANARY /home/private/token'}]*2
            for name,value in [('old',original),('new',original),('policy',{'schema_version':1,'owner':'PRIVATE-OWNER','reason':'secret policy','rules':[]})]:
                (root/(name+'.json')).write_text(json.dumps(value))
            result=compare_files(root/'old.json',root/'new.json',root/'policy.json',root/'run')
            self.assertEqual(result['status'],'PASS')
            self.assertEqual(verify_saved(root/'run')['result'],'PASS')
            export_summary(root/'run',root/'share.json')
            self.assertNotIn('PRIVATE', (root/'share.json').read_text())
            self.assertNotIn('/home', (root/'share.json').read_text())
            self.assertNotIn('secret', (root/'share.json').read_text())
            result['raw']['original'][0]['v']=1
            (root/'run/results.json').write_text(json.dumps(result))
            with self.assertRaisesRegex(ValueError,'differs'):verify_saved(root/'run')
            with self.assertRaises(ValueError):export_summary(root/'run',root/'bad.json')
            self.assertFalse((root/'bad.json').exists())

    def test_large_valid_result_reopens_and_duplicate_json_rejected(self):
        parent=Path(__file__).resolve().parents[1]/'.local/tests'
        with tempfile.TemporaryDirectory(dir=parent) as tmp:
            root=Path(tmp)
            (root/'old.json').write_text(json.dumps([{'v':'x'*300000}]*2))
            (root/'new.json').write_bytes((root/'old.json').read_bytes())
            (root/'policy.json').write_text(json.dumps({'schema_version':1,'owner':'test','reason':'exact','rules':[]}))
            compare_files(root/'old.json',root/'new.json',root/'policy.json',root/'large')
            self.assertGreater((root/'large/results.json').stat().st_size,1048576)
            self.assertEqual(verify_saved(root/'large')['result'],'PASS')
            (root/'old.json').write_text('[{"v":1,"v":2},{"v":1,"v":2}]')
            with self.assertRaisesRegex(ValueError,'duplicate'):compare_files(root/'old.json',root/'new.json',root/'policy.json',root/'ambiguous')
            self.assertFalse((root/'ambiguous').exists())
