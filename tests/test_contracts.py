import copy
import unittest
from renewal_engine.recipes import DEFAULT, PATHLIB, registry, validate_contract, compose, conformance, select

class ContractTests(unittest.TestCase):
    def test_contract_mutations_refused(self):
        original = registry()[DEFAULT]
        for key, value in [('schema',True),('extra',1),('version','latest'),('baseline',{'min':[3,12],'max_exclusive':[3,11]}),('policy_owner',''),('effects',[]),('fixtures',[])]:
            candidate=copy.deepcopy(original);candidate[key]=value
            with self.subTest(key=key), self.assertRaises(ValueError):validate_contract(candidate)
        damaged=copy.deepcopy(original);damaged['fixtures'][0]['expected']+='pass\n'
        with self.assertRaises(ValueError):validate_contract(damaged)
        for selection in [[],['unknown'],[DEFAULT,DEFAULT]]:
            with self.assertRaises(ValueError):select(selection)
    def test_conformance_and_both_composition_orders(self):
        self.assertEqual(conformance()['status'],'PASS')
        catalog=registry()
        original='\n'.join(catalog[i]['fixtures'][0]['source'] for i in (DEFAULT,PATHLIB)).encode()
        forward,steps=compose(original,[DEFAULT,PATHLIB]);backward,_=compose(original,[PATHLIB,DEFAULT])
        self.assertEqual(forward,backward)
        self.assertIn(b't.hardlink_to(s)',forward);self.assertIn(b'read_file',forward)
        self.assertEqual(steps[1]['input_sha256'],steps[0]['output_sha256'])
        self.assertEqual(compose(forward,[DEFAULT,PATHLIB])[0],forward)
    def test_pathlib_refusals(self):
        source=registry()[PATHLIB]['fixtures'][0]['source']
        variants=[source.replace('s.link_to(t)','s.link_to(Path(target))'),
                  source.replace('t = Path(target)','t = Other(target)'),
                  source.replace('t = Path(target)','s = Path(target)'),
                  source.replace('s.link_to(t)','s.link_to(t, other=True)'),
                  source.replace('from pathlib import Path','from custom import Path'),
                  '@decorated\n'+source,
                  'Path.link_to = other\n'+source,
                  source.replace('    s.link_to','    s = other\n    s.link_to')]
        for value in variants:
            with self.subTest(value=value):self.assertEqual(compose(value.encode(),[PATHLIB])[0],value.encode())
        self.assertEqual(compose(source.encode(),[PATHLIB],shadowed_modules=['pathlib'])[0],source.encode())
        kw=source.replace('s.link_to(t)','s.link_to(target=t)')
        self.assertIn(b't.hardlink_to(target=s)',compose(kw.encode(),[PATHLIB])[0])
        commented=source.replace('s.link_to(t)', 's.link_to(\n        # preserve this comment\n        t\n    )')
        self.assertIn(b'# preserve this comment',compose(commented.encode(),[PATHLIB])[0])
