from copy import deepcopy
import json
from pathlib import Path
import unittest

from renewal_engine.comparison import compare_case


class ComparatorTests(unittest.TestCase):
    def setUp(self):
        self.policy=json.loads((Path(__file__).resolve().parents[1]/'renewal_engine/reference/policy.json').read_text())
        self.case={'id':'synthetic-error','mode':'keyword'}
        self.warning={**self.policy['warning'],'lineno':20}
        self.old={'stdout':'','exception':{'type':'ParsingError','message':'bad source.ini','args':['source.ini'],
                  'attributes':{'source':'source.ini','lineno':3}},'warnings':[self.warning],
                  'effects':{'stream_position':4,'stream_closed_after_call':False}}
        self.new=deepcopy(self.old);self.new['warnings']=[]

    def test_only_declared_warning_change_passes(self):
        result=compare_case(self.case,self.old,self.new,self.policy)
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(len(result['expected_changes']),1)
        self.assertEqual(self.old['warnings'],[self.warning])

    def test_wrong_diagnostics_and_dropped_fields_fail(self):
        for field in ['message','args','attributes']:
            new=deepcopy(self.new);del new['exception'][field]
            with self.subTest(field=field):self.assertEqual(compare_case(self.case,self.old,new,self.policy)['status'],'REGRESSION')
        new=deepcopy(self.new);new['exception']['attributes']['source']='WRONG.ini'
        result=compare_case(self.case,self.old,new,self.policy)
        self.assertEqual(result['status'],'REGRESSION')
        self.assertTrue(any(d['path']=='$.exception.attributes.source' for d in result['differences']))

    def test_warning_not_normalized_broadly(self):
        for side in ['original','candidate']:
            old,new=deepcopy(self.old),deepcopy(self.new)
            (old if side=='original' else new)['warnings'].append({'category':'UserWarning','message':'unexpected'})
            self.assertEqual(compare_case(self.case,old,new,self.policy)['status'],'REGRESSION')
        old=deepcopy(self.old);old['warnings']=[]
        self.assertEqual(compare_case(self.case,old,self.new,self.policy)['status'],'REGRESSION')

    def test_effect_or_output_change_fails(self):
        for field,value in [('stdout','changed'),('effects',{})]:
            new=deepcopy(self.new);new[field]=value
            self.assertEqual(compare_case(self.case,self.old,new,self.policy)['status'],'REGRESSION')


if __name__=='__main__':unittest.main()
