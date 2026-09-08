"""Strict repeated observations, narrow policies, and bounded filesystem evidence."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat

MAX_JSON_BYTES = 4_194_304
MAX_JSON_NODES = 50_000
MAX_DEPTH = 64
MAX_RECORDED_DIFFERENCES = 1000
MAX_UNORDERED_ITEMS = 1000
MAX_TOLERANCE = 1_000_000
MAX_FILES = 256
MAX_ENTRIES = 1024
MAX_FILE_BYTES = 65_536
MAX_TOTAL_FILE_BYTES = 1_048_576
MAX_DIRECTORY_DEPTH = 16


def _json_bytes(value):
    nodes = 0
    active = set()

    def visit(item, depth):
        nonlocal nodes
        nodes += 1
        if nodes > MAX_JSON_NODES or depth > MAX_DEPTH:
            raise ValueError('JSON observation exceeds structural bounds')
        kind = type(item)
        if kind in (dict, list):
            if id(item) in active:
                raise ValueError('cyclic observations are not JSON')
            active.add(id(item))
            if kind is dict:
                if any(type(key) is not str for key in item):
                    raise ValueError('JSON object keys must be strings')
                children = item.values()
            else:
                children = item
            for child in children:
                visit(child, depth + 1)
            active.remove(id(item))
        elif kind not in (str, int, float, bool, type(None)):
            raise ValueError('observations must contain strict JSON types')
        elif kind is float and not math.isfinite(item):
            raise ValueError('nonfinite JSON number')
    visit(value, 0)
    try:
        encoded = json.dumps(value, sort_keys=True, ensure_ascii=False,
                             allow_nan=False, separators=(',', ':')).encode('utf-8')
    except (ValueError, UnicodeError, OverflowError) as exc:
        raise ValueError('observation cannot be encoded as bounded UTF-8 JSON') from exc
    if len(encoded) > MAX_JSON_BYTES:
        raise ValueError('JSON observation exceeds byte bounds')
    return encoded


def _hash(value):
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _tokens(pointer):
    if type(pointer) is not str or not pointer.startswith('/') or '*' in pointer:
        raise ValueError('policy requires a nonroot exact JSON pointer without wildcards')
    tokens = pointer[1:].split('/')
    if len(tokens) > MAX_DEPTH or any(re.search(r'~(?![01])', token) for token in tokens):
        raise ValueError('invalid or excessively deep JSON pointer')
    return tuple(token.replace('~1', '/').replace('~0', '~') for token in tokens)


def _lookup(record, tokens):
    value = record
    for token in tokens:
        if type(value) is dict and token in value:
            value = value[token]
        elif type(value) is list and re.fullmatch(r'0|[1-9][0-9]*', token) and len(token) <= 8 and int(token) < len(value):
            value = value[int(token)]
        else:
            raise ValueError('policy path is absent or invalid in an observation')
    return value


def _timestamp(value):
    if type(value) is not str or not re.fullmatch(
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})', value):
        raise ValueError('timestamp rule requires ISO timestamps with explicit timezone')
    try:
        # datetime permits unusual timezone minute values; reject these explicitly.
        if not value.endswith('Z') and (int(value[-5:-3]) > 23 or int(value[-2:]) > 59):
            raise ValueError('invalid timezone offset')
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, OverflowError) as exc:
        raise ValueError('timestamp rule contains an invalid timestamp') from exc


def _validate_policy(policy, records):
    if type(policy) is not dict or set(policy) != {'schema_version', 'owner', 'reason', 'rules'}:
        raise ValueError('policy requires exactly schema_version, owner, reason, rules')
    _json_bytes(policy)
    if type(policy['schema_version']) is not int or policy['schema_version'] != 1:
        raise ValueError('unsupported policy schema_version')
    for key in ('owner', 'reason'):
        if type(policy[key]) is not str or not policy[key].strip() or len(policy[key]) > 1000:
            raise ValueError('policy owner and reason must be nonempty bounded strings')
    if type(policy['rules']) is not list or len(policy['rules']) > 256:
        raise ValueError('policy rules must be a list of at most 256 rules')
    rules = {}
    for rule in policy['rules']:
        if type(rule) is not dict:
            raise ValueError('policy rule must be an object')
        kind = rule.get('kind')
        if type(kind) is not str or kind not in {'numeric', 'timestamp', 'unordered'}:
            raise ValueError('unknown policy rule kind')
        keys = {'path', 'kind', 'reason'} | ({'absolute_tolerance'} if kind == 'numeric' else set())
        if set(rule) != keys or type(rule.get('reason')) is not str or not rule['reason'].strip() or len(rule['reason']) > 1000:
            raise ValueError('policy rule has unknown/missing fields or invalid reason')
        tokens = _tokens(rule['path'])
        if any(tokens[:len(existing)] == existing or existing[:len(tokens)] == tokens for existing in rules):
            raise ValueError('duplicate or overlapping policy paths')
        if kind == 'numeric':
            tolerance = rule['absolute_tolerance']
            if type(tolerance) not in (int, float) or not 0 <= tolerance <= MAX_TOLERANCE or (type(tolerance) is float and not math.isfinite(tolerance)):
                raise ValueError('numeric tolerance must be finite and between 0 and 1000000')
        for record in records:
            value = _lookup(record, tokens)
            if kind == 'numeric' and type(value) not in (int, float):
                raise ValueError('numeric rule must target a number, excluding bool')
            if kind == 'timestamp':
                _timestamp(value)
            if kind == 'unordered' and (type(value) is not list or len(value) > MAX_UNORDERED_ITEMS):
                raise ValueError('unordered rule requires a list of at most 1000 items')
        rules[tokens] = rule
    return rules


def _pointer(tokens):
    return ''.join('/' + str(token).replace('~', '~0').replace('/', '~1') for token in tokens)


def _differences(left, right, rules, emit, tokens=()):
    # Canonical JSON retains the bool/int and int/float distinctions recursively.
    if type(left) is type(right) and _json_bytes(left) == _json_bytes(right):
        return
    rule = rules.get(tokens)
    authorized = False
    if rule and type(left) is type(right):
        if rule['kind'] == 'numeric':
            authorized = abs(Fraction(left) - Fraction(right)) <= Fraction(rule['absolute_tolerance'])
        elif rule['kind'] == 'timestamp':
            authorized = _timestamp(left) == _timestamp(right)
        else:
            authorized = sorted(_json_bytes(v) for v in left) == sorted(_json_bytes(v) for v in right)
    if authorized:
        emit(dict(path=_pointer(tokens), authorized=True, kind=rule['kind'], reason=rule['reason']))
    elif type(left) is not type(right):
        emit(dict(path=_pointer(tokens), authorized=False, reason='JSON type changed'))
    elif type(left) is dict:
        for key in sorted(set(left) | set(right)):
            if key not in left or key not in right:
                emit(dict(path=_pointer(tokens + (key,)), authorized=False, reason='field presence changed'))
            else:
                _differences(left[key], right[key], rules, emit, tokens + (key,))
    elif type(left) is list:
        if len(left) != len(right):
            emit(dict(path=_pointer(tokens), authorized=False, reason='list length changed'))
        else:
            for index, (old, new) in enumerate(zip(left, right)):
                _differences(old, new, rules, emit, tokens + (str(index),))
    else:
        emit(dict(path=_pointer(tokens), authorized=False, reason='value changed'))


def compare_repeated(original: list[dict], candidate: list[dict], policy: dict) -> dict:
    """Compare all within-side and cross-side pairs without modifying raw inputs.

    Invalid JSON, counts or policy raise ValueError. UNSTABLE takes precedence
    over REGRESSION, and both categories of evidence remain in the result.
    """
    if type(original) is not list or type(candidate) is not list or not 2 <= len(original) == len(candidate) <= 10:
        raise ValueError('equal repetition counts between 2 and 10 are required')
    for record in original + candidate:
        if type(record) is not dict:
            raise ValueError('each observation must be a JSON object')
        _json_bytes(record)
    rules = _validate_policy(policy, original + candidate)
    counts = dict(runs_per_side=len(original), expected_changes=0, variance=0,
                  unauthorized_variance=0, regressions=0)
    result = dict(schema_version=1, status='PASS', raw=dict(original=deepcopy(original), candidate=deepcopy(candidate)),
        policy=deepcopy(policy), policy_sha256=_hash(policy),
        observation_sha256=dict(original=[_hash(r) for r in original], candidate=[_hash(r) for r in candidate]),
        expected_changes=[], variance=[], regressions=[], counts=counts, truncated=False)

    def record_difference(item, scope, first, second):
        item.update(scope=scope, first_run=first, second_run=second)
        if scope == 'cross':
            category = 'expected_changes' if item['authorized'] else 'regressions'
        else:
            category = 'variance'
            if not item['authorized']:
                counts['unauthorized_variance'] += 1
        counts[category] += 1
        if len(result[category]) < MAX_RECORDED_DIFFERENCES:
            result[category].append(item)
        else:
            result['truncated'] = True

    for scope, runs in (('original', original), ('candidate', candidate)):
        for first in range(len(runs)):
            for second in range(first + 1, len(runs)):
                _differences(runs[first], runs[second], rules,
                    lambda item: record_difference(item, scope, first, second))
    for first, old in enumerate(original):
        for second, new in enumerate(candidate):
            _differences(old, new, rules, lambda item: record_difference(item, 'cross', first, second))
    if counts['unauthorized_variance']:
        result['status'] = 'UNSTABLE'
    elif counts['regressions']:
        result['status'] = 'REGRESSION'
    return result


def _open_root(root):
    root = Path(root)
    if '..' in root.parts:
        raise ValueError('filesystem root must not contain parent traversal')
    absolute = root.absolute()
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open('/', flags)
    try:
        for component in absolute.parts[1:]:
            next_fd = os.open(component, flags, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def observer(root: Path) -> dict:
    """Capture bounded regular-file bytes; reject symlinks and special entries.

    Opens every ancestor and descendant relative to directory descriptors with
    O_NOFOLLOW. Unsupported platforms or changing/unreadable trees fail closed.
    """
    files = {}
    total_bytes = 0
    entries_seen = 0

    def walk(directory, prefix, depth):
        nonlocal total_bytes, entries_seen
        if depth > MAX_DIRECTORY_DEPTH:
            raise ValueError('filesystem directory depth limit exceeded')
        names = []
        with os.scandir(directory) as entries:
            for entry in entries:
                entries_seen += 1
                if entries_seen > MAX_ENTRIES:
                    raise ValueError('filesystem entry count limit exceeded')
                names.append(entry.name)
        for name in sorted(names):
            path = prefix + name
            info = os.stat(name, dir_fd=directory, follow_symlinks=False)
            if stat.S_ISDIR(info.st_mode):
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                try:
                    opened = os.fstat(child)
                    if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                        raise ValueError('filesystem changed during observation')
                    walk(child, path + '/', depth + 1)
                finally:
                    os.close(child)
            elif stat.S_ISREG(info.st_mode):
                if len(files) >= MAX_FILES or info.st_size > MAX_FILE_BYTES or total_bytes + info.st_size > MAX_TOTAL_FILE_BYTES:
                    raise ValueError('filesystem file count or byte limit exceeded')
                fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
                try:
                    before = os.fstat(fd)
                    if not stat.S_ISREG(before.st_mode) or (before.st_dev, before.st_ino) != (info.st_dev, info.st_ino):
                        raise ValueError('filesystem entry changed during observation')
                    if before.st_size > MAX_FILE_BYTES:
                        raise ValueError('filesystem file byte limit exceeded')
                    chunks = []
                    size = 0
                    while size <= MAX_FILE_BYTES:
                        chunk = os.read(fd, min(8192, MAX_FILE_BYTES + 1 - size))
                        if not chunk:
                            break
                        chunks.append(chunk)
                        size += len(chunk)
                    after = os.fstat(fd)
                finally:
                    os.close(fd)
                if size > MAX_FILE_BYTES or total_bytes + size > MAX_TOTAL_FILE_BYTES:
                    raise ValueError('filesystem byte limit exceeded')
                if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns) or size != after.st_size:
                    raise ValueError('filesystem file changed during observation')
                data = b''.join(chunks)
                files[path] = dict(size=size, sha256=hashlib.sha256(data).hexdigest(), bytes_hex=data.hex())
                total_bytes += size
            else:
                raise ValueError('filesystem symlink or special entry rejected')
    try:
        fd = _open_root(root)
        try:
            walk(fd, '', 0)
        finally:
            os.close(fd)
    except (OSError, AttributeError, TypeError) as exc:
        raise ValueError('filesystem observation unavailable or unsafe') from exc
    return dict(schema_version=1, files=files, counts=dict(files=len(files), bytes=total_bytes))


def shareable_summary(result: dict) -> dict:
    """Allowlist only validated statuses, counters and SHA256 identities."""
    summary = dict(schema_version=1, status='INVALID', counts={}, observation_sha256={})
    if type(result) is not dict:
        return summary
    status = result.get('status')
    if type(status) is str and status in {'PASS', 'REGRESSION', 'UNSTABLE'}:
        summary['status'] = status
    counts = result.get('counts')
    if type(counts) is dict:
        for key in ('runs_per_side', 'expected_changes', 'variance', 'unauthorized_variance', 'regressions'):
            value = counts.get(key)
            if type(value) is int and 0 <= value <= 1_000_000_000:
                summary['counts'][key] = value

    def digest(value):
        return type(value) is str and re.fullmatch(r'[0-9a-f]{64}', value) is not None
    if digest(result.get('policy_sha256')):
        summary['policy_sha256'] = result['policy_sha256']
    identities = result.get('observation_sha256')
    if type(identities) is dict:
        for side in ('original', 'candidate'):
            values = identities.get(side)
            if type(values) is list and 2 <= len(values) <= 10 and all(digest(v) for v in values):
                summary['observation_sha256'][side] = values[:]
    return summary
