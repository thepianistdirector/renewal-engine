import json
import unittest
from unittest.mock import patch

from renewal_engine.impact import analyze


class ImpactTests(unittest.TestCase):
    def test_relative_reexport_and_transitive_dependents(self):
        result = analyze({
            'src/pkg/__init__.py': b'from .core import parse\n',
            'src/pkg/core.py': b'def parse(value: str, /, *, strict=True) -> int:\n return 1\n',
            'src/pkg/sub/__init__.py': b'',
            'src/pkg/sub/client.py': b'from .. import parse\n',
            'main.py': b'from pkg.sub.client import run\n',
        }, {}, ['src/pkg/core.py'])
        change = result['changed']['src/pkg/core.py']
        self.assertEqual(change['direct_dependents'], ['src/pkg/__init__.py'])
        self.assertEqual(change['transitive_dependents'], ['main.py', 'src/pkg/sub/client.py'])
        self.assertEqual(result['exports']['src/pkg/core.py'][0]['signature'],
                         '(value: str, /, *, strict=True) -> int')
        json.dumps(result)

    def test_cycles_terminate_and_exclude_changed_from_dependents(self):
        result = analyze({'a.py': b'import b', 'b.py': b'import a',
                          'c.py': b'import b'}, {}, ['a.py'])
        self.assertEqual(result['changed']['a.py'], {
            'direct_dependents': ['b.py'], 'transitive_dependents': ['c.py'],
            'impacted_paths': ['a.py', 'b.py', 'c.py']})

    def test_ambiguous_modules_include_all_candidates(self):
        result = analyze({'foo.py': b'', 'src/foo.py': b'',
                          'use.py': b'import foo\nimport external\n__import__(name)'}, {}, ['foo.py'])
        self.assertEqual(result['graph']['use.py'], ['foo.py', 'src/foo.py'])
        reasons = [i['reason'] for i in result['uncertainties']]
        self.assertTrue(any('ambiguous local' in r for r in reasons))
        self.assertTrue(any('unresolved import' in r for r in reasons))
        self.assertTrue(any('dynamic import' in r for r in reasons))

    def test_dynamic_import_alias_is_uncertain(self):
        result = analyze({'a.py': b'from importlib import import_module as load\nload(name)'}, {}, [])
        self.assertTrue(any('dynamic import' in i['reason'] for i in result['uncertainties']))

    def test_namespace_child_and_wildcard(self):
        result = analyze({'pkg/child.py': b'', 'use.py': b'from pkg import child\nfrom pkg.child import *'}, {}, ['pkg/child.py'])
        self.assertEqual(result['graph']['use.py'], ['pkg/child.py'])
        self.assertTrue(any('wildcard' in i['reason'] for i in result['uncertainties']))

    def test_metadata_pins_python_locks_and_hints(self):
        result = analyze({'pkg/core.py': b''}, {
            'pyproject.toml': b'[project]\nrequires-python=">=3.11"\ndependencies=["Foo_Bar==1.0"]\n[project.scripts]\nstart="pkg.core:main"\n',
            'requirements-dev.txt': b'foo-bar==2.0 # explicit pin\nconditional==1; python_version<"3.11"\n-r other.txt\n',
            'uv.lock': b'version = 1',
        }, ['pkg/core.py'])['metadata']
        self.assertEqual(result['python_requires'][0]['range'], '>=3.11')
        self.assertEqual(result['pin_conflicts'][0]['name'], 'foo-bar')
        self.assertEqual(result['pin_conflicts'][0]['pins'], ['1.0', '2.0'])
        self.assertEqual(result['lockfiles'][0]['path'], 'uv.lock')
        self.assertEqual(result['review_hints'][0]['module'], 'pkg.core')
        self.assertEqual(len([r for r in result['requirements'] if 'status' in r]), 2)

    def test_malformed_metadata_and_source_are_reported(self):
        for config in [b'[project', b'project=4', b'[project]\ndependencies=3', b'\xff']:
            result = analyze({'bad.py': b'def :'}, {'pyproject.toml': config}, ['missing.py'])
            self.assertTrue(result['metadata']['errors'])
            self.assertEqual(len(result['uncertainties']), 2)

    def test_analysis_never_executes_and_honors_literal_exports(self):
        result = analyze({'a.py': b'raise RuntimeError("must never run")\n__all__=["_api"]\ndef _api(x=1): pass\ndef hidden(): pass'}, {}, ['a.py'])
        self.assertEqual([f['name'] for f in result['exports']['a.py']], ['_api'])

    def test_limits_leave_explicit_uncertainty(self):
        with patch('renewal_engine.impact.MAX_FILE_BYTES', 5):
            result = analyze({'a.py': b'import b', 'b.py': b''}, {}, ['a.py'])
        self.assertTrue(any('byte limit' in i['reason'] for i in result['uncertainties']))
        with patch('renewal_engine.impact.MAX_FILES', 1):
            result = analyze({'a.py': b'', 'b.py': b''}, {}, ['b.py'])
        self.assertTrue(any('count limit' in i['reason'] for i in result['uncertainties']))

    def test_deterministic_order(self):
        sources = {'b.py': b'import a', 'a.py': b''}
        self.assertEqual(analyze(sources, {}, ['a.py']),
                         analyze(dict(reversed(list(sources.items()))), {}, ['a.py', 'a.py']))


if __name__ == '__main__':
    unittest.main()
