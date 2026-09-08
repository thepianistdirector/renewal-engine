from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

from renewal_engine.observations import compare_repeated, observer, shareable_summary


def policy(*rules):
    return dict(schema_version=1, owner='test-owner', reason='reviewed contract', rules=list(rules))


def rule(path, kind, **options):
    return dict(path=path, kind=kind, reason='specific approved normalization', **options)


def repeated(value):
    return [deepcopy(value), deepcopy(value)]


class ObservationComparisonTests(unittest.TestCase):
    def test_exact_and_input_immutability(self):
        old = repeated({'stdout': 'ok', 'value': 3})
        new = deepcopy(old)
        frozen = policy()
        result = compare_repeated(old, new, frozen)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(old, new)
        self.assertEqual(frozen, policy())
        old[0]['stdout'] = 'later mutation'
        frozen['owner'] = 'later mutation'
        self.assertEqual(result['raw']['original'][0]['stdout'], 'ok')
        self.assertEqual(result['policy']['owner'], 'test-owner')
        self.assertEqual(len(result['policy_sha256']), 64)

    def test_strict_json_types_including_nested_and_unordered(self):
        for old, new in [(True, 1), (1, 1.0), ([False], [0]), ({'x': True}, {'x': 1})]:
            with self.subTest(old=old, new=new):
                self.assertEqual(compare_repeated(repeated({'v': old}), repeated({'v': new}), policy())['status'], 'REGRESSION')
        result = compare_repeated(repeated({'v': [True, 2]}), repeated({'v': [2, 1]}), policy(rule('/v', 'unordered')))
        self.assertEqual(result['status'], 'REGRESSION')

    def test_matching_variance_is_unstable(self):
        runs = [{'value': 1}, {'value': 2}]
        result = compare_repeated(runs, deepcopy(runs), policy())
        self.assertEqual(result['status'], 'UNSTABLE')
        self.assertEqual(result['counts']['unauthorized_variance'], 2)
        self.assertTrue(result['regressions'])

    def test_narrow_numeric_variance_and_all_pairs(self):
        frozen = policy(rule('/value', 'numeric', absolute_tolerance=0.125))
        result = compare_repeated([{'value': 1.0}, {'value': 1.125}], [{'value': 1.0}, {'value': 1.125}], frozen)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['counts']['variance'], 2)
        self.assertTrue(all(v['authorized'] for v in result['variance']))
        # Neighbor pairs are within tolerance, but the endpoints are not.
        runs = [{'value': 1.0}, {'value': 1.125}, {'value': 1.25}]
        self.assertEqual(compare_repeated(runs, deepcopy(runs), frozen)['status'], 'UNSTABLE')
        self.assertEqual(compare_repeated(repeated({'value': 1}), repeated({'value': 1.0}), frozen)['status'], 'REGRESSION')

    def test_timestamp_normalizes_same_instant_only(self):
        frozen = policy(rule('/time', 'timestamp'))
        old = repeated({'time': '2026-09-08T12:00:00Z'})
        new = repeated({'time': '2026-09-08T14:00:00+02:00'})
        self.assertEqual(compare_repeated(old, new, frozen)['status'], 'PASS')
        new = repeated({'time': '2026-09-08T14:00:01+02:00'})
        self.assertEqual(compare_repeated(old, new, frozen)['status'], 'REGRESSION')
        for timestamp in ['2026-09-08T12:00:00', '2026-09-08', '2026-09-08T12:00:00+01:99']:
            with self.assertRaises(ValueError):
                compare_repeated(old, repeated({'time': timestamp}), frozen)

    def test_unordered_is_exact_multiset(self):
        frozen = policy(rule('/items', 'unordered'))
        old = repeated({'items': [1, 1, {'a': [2, 3]}]})
        new = repeated({'items': [{'a': [2, 3]}, 1, 1]})
        self.assertEqual(compare_repeated(old, new, frozen)['status'], 'PASS')
        for items in [[1, {'a': [2, 3]}], [1, 2, {'a': [2, 3]}], [1, 1, {'a': [3, 2]}]]:
            self.assertEqual(compare_repeated(old, repeated({'items': items}), frozen)['status'], 'REGRESSION')

    def test_seeded_regressions_are_never_normalized(self):
        old = {'stdout': 'ok', 'exception': {'type': None, 'args': []}, 'return': 12,
               'env': {'flag': 'enabled'}, 'files': {'created.txt': {'bytes_hex': '6162'}}}
        mutations = [lambda x: x.update(stdout='wrong'), lambda x: x.pop('return'),
                     lambda x: x['exception'].update(type='ValueError'),
                     lambda x: x['env'].update(flag='disabled'),
                     lambda x: x['files'].clear(),
                     lambda x: x['files']['created.txt'].update(bytes_hex='6163')]
        random.Random(20260908).shuffle(mutations)
        for mutate in mutations:
            new = deepcopy(old)
            mutate(new)
            self.assertEqual(compare_repeated(repeated(old), repeated(new), policy())['status'], 'REGRESSION')

    def test_pointer_escaping_and_known_path_requirement(self):
        runs = repeated({'a/b': {'~key': 1}, 'items': [2]})
        self.assertEqual(compare_repeated(runs, runs, policy(rule('/a~1b/~0key', 'numeric', absolute_tolerance=0)))['status'], 'PASS')
        for pointer in ['', '*', 'a', '/missing', '/items/01', '/items/-1', '/items/*', '/a~2b']:
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                compare_repeated(runs, runs, policy(rule(pointer, 'numeric', absolute_tolerance=0)))
        with self.assertRaises(ValueError):
            compare_repeated(runs, runs, policy(rule('/items', 'unordered'), rule('/items/0', 'numeric', absolute_tolerance=0)))
        with self.assertRaises(ValueError):
            compare_repeated(runs, runs, policy(rule('/items', 'unordered'), rule('/items', 'unordered')))

    def test_invalid_policies_fail_closed(self):
        runs = repeated({'v': 1})
        malformed = [{}, {**policy(), 'schema_version': True}, {**policy(), 'owner': ''},
                     {**policy(), 'extra': True}, {**policy(), 'rules': {}},
                     policy(rule('/v', 'drop')),
                     policy({**rule('/v', 'numeric', absolute_tolerance=0), 'unknown': 2})]
        malformed += [policy(rule('/v', 'numeric', absolute_tolerance=t)) for t in
                      [-1, float('inf'), float('nan'), True, 1000001, 10 ** 1000]]
        for frozen in malformed:
            with self.subTest(frozen=str(frozen)[:100]), self.assertRaises(ValueError):
                compare_repeated(runs, runs, frozen)
        with self.assertRaises(ValueError):
            compare_repeated(repeated({'v': True}), repeated({'v': True}), policy(rule('/v', 'numeric', absolute_tolerance=0)))

    def test_input_bounds_and_invalid_json(self):
        for first, second in [([], []), ([{}], [{}]), ([{}] * 2, [{}] * 3), ([{}] * 11, [{}] * 11)]:
            with self.assertRaises(ValueError):
                compare_repeated(first, second, policy())
        for value in [float('nan'), float('inf'), (1, 2), {1: 'wrong'}, b'bytes']:
            with self.assertRaises(ValueError):
                compare_repeated(repeated({'v': value}), repeated({'v': value}), policy())
        cycle = {}
        cycle['self'] = cycle
        with self.assertRaises(ValueError):
            compare_repeated([cycle, cycle], [cycle, cycle], policy())
        with self.assertRaises(ValueError):
            compare_repeated(repeated({'v': list(range(1001))}), repeated({'v': []}), policy(rule('/v', 'unordered')))

    def test_difference_truncation_retains_full_counts(self):
        with patch('renewal_engine.observations.MAX_RECORDED_DIFFERENCES', 1):
            result = compare_repeated(repeated({'a': 1, 'b': 2}), repeated({'a': 3, 'b': 4}), policy())
        self.assertTrue(result['truncated'])
        self.assertEqual(len(result['regressions']), 1)
        self.assertEqual(result['counts']['regressions'], 8)

    def test_shareable_summary_excludes_canaries_and_untrusted_fields(self):
        canary = 'PRIVATE-CANARY-SOURCE-STDOUT-ENV-PATH'
        runs = repeated({canary: {'stdout': canary, 'env': {'TOKEN': canary}}})
        frozen = policy()
        frozen['reason'] = canary
        result = compare_repeated(runs, runs, frozen)
        result['secret'] = canary
        summary = shareable_summary(result)
        self.assertNotIn(canary, json.dumps(summary))
        self.assertEqual(set(summary), {'schema_version', 'status', 'counts', 'policy_sha256', 'observation_sha256'})
        malicious = {'status': canary, 'policy_sha256': canary, 'counts': {'regressions': canary},
                     'observation_sha256': {'original': [canary, canary]}}
        self.assertNotIn(canary, json.dumps(shareable_summary(malicious)))


class FilesystemObserverTests(unittest.TestCase):
    def test_binary_bytes_digest_and_create_delete(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'nested').mkdir()
            (root / 'nested' / 'a.bin').write_bytes(b'\x00\xffab')
            before = observer(root)
            self.assertEqual(before['files']['nested/a.bin'], dict(size=4, bytes_hex='00ff6162', sha256=hashlib.sha256(b'\x00\xffab').hexdigest()))
            (root / 'nested' / 'a.bin').unlink()
            (root / 'new.txt').write_bytes(b'new')
            after = observer(root)
            result = compare_repeated(repeated(before), repeated(after), policy())
            self.assertEqual(result['status'], 'REGRESSION')
            self.assertTrue(any('nested~1a.bin' in item['path'] for item in result['regressions']))

    def test_reject_symlinks_and_symlink_ancestors(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'actual').mkdir()
            (root / 'actual' / 'child').mkdir()
            (root / 'alias').symlink_to(root / 'actual', target_is_directory=True)
            for path in [root, root / 'alias', root / 'alias' / 'child']:
                with self.subTest(path=path), self.assertRaises(ValueError):
                    observer(path)

    def test_reject_special_and_oversized_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            os.mkfifo(root / 'pipe')
            with self.assertRaises(ValueError):
                observer(root)
            (root / 'pipe').unlink()
            (root / 'large').write_bytes(b'a' * 65537)
            with self.assertRaises(ValueError):
                observer(root)

    def test_count_total_and_depth_limits(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'a').write_bytes(b'abc')
            (root / 'b').write_bytes(b'def')
            for name, value in [('MAX_FILES', 1), ('MAX_ENTRIES', 1), ('MAX_TOTAL_FILE_BYTES', 5)]:
                with patch('renewal_engine.observations.' + name, value), self.assertRaises(ValueError):
                    observer(root)
            (root / 'child').mkdir()
            with patch('renewal_engine.observations.MAX_DIRECTORY_DEPTH', 0), self.assertRaises(ValueError):
                observer(root)


if __name__ == '__main__':
    unittest.main()
