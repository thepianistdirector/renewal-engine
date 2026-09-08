"""Versioned, closed recipe contracts and deterministic composition. No plugins execute."""
from __future__ import annotations
from .jsonio import loads as strict_loads

import ast
from copy import deepcopy
from importlib.resources import files
import json
import re

from .discovery import Discovery, Edit, Finding, discover
from .transformation import digest, transform

DEFAULT = 'configparser-local-prefix-v1'
PATHLIB = 'pathlib-local-hardlink-v1'


def validate_contract(record):
    required = {'schema', 'id', 'version', 'engine_schema', 'baseline', 'target', 'preconditions',
                'effects', 'policy_owner', 'dependencies', 'fixtures', 'limitations'}
    if not isinstance(record, dict) or set(record) != required:
        raise ValueError('recipe contract fields do not match schema 1')
    if type(record['schema']) is not int or record['schema'] != 1 or type(record['engine_schema']) is not int or record['engine_schema'] != 1:
        raise ValueError('unsupported recipe schema')
    if not isinstance(record['id'], str) or not re.fullmatch(r'[a-z][a-z0-9-]{1,79}', record['id']):
        raise ValueError('invalid recipe id')
    if not isinstance(record['version'], str) or not re.fullmatch(r'[1-9][0-9]*\.[0-9]+\.[0-9]+', record['version']):
        raise ValueError('invalid recipe version')
    for key in ('baseline', 'target'):
        interval = record[key]
        if not isinstance(interval, dict) or set(interval) != {'min', 'max_exclusive'}:
            raise ValueError('invalid runtime interval')
        for value in interval.values():
            if not isinstance(value, list) or len(value) != 2 or any(type(n) is not int or n < 0 for n in value):
                raise ValueError('runtime bound requires [major, minor]')
        if tuple(interval['min']) >= tuple(interval['max_exclusive']):
            raise ValueError('empty runtime interval')
    for key in ('preconditions', 'effects', 'limitations', 'dependencies'):
        value = record[key]
        if not isinstance(value, list) or (key != 'dependencies' and not value) or any(not isinstance(s, str) or not s.strip() or len(s) > 1000 for s in value) or len(set(value)) != len(value):
            raise ValueError('invalid recipe ' + key)
    if not isinstance(record['policy_owner'], str) or not record['policy_owner'].strip():
        raise ValueError('comparison policy owner is required')
    if not isinstance(record['fixtures'], list) or not record['fixtures']:
        raise ValueError('recipe requires conformance fixtures')
    for fixture in record['fixtures']:
        if not isinstance(fixture, dict) or set(fixture) != {'name', 'source', 'expected', 'source_sha256', 'expected_sha256', 'kind'}:
            raise ValueError('invalid fixture fields')
        if fixture['kind'] not in ('positive', 'refusal'):
            raise ValueError('invalid fixture kind')
        for key in ('source', 'expected'):
            if not isinstance(fixture[key], str) or len(fixture[key].encode()) > 1048576 or digest(fixture[key].encode()) != fixture[key + '_sha256']:
                raise ValueError('fixture hash mismatch')
        if fixture['kind'] == 'refusal' and fixture['source'] != fixture['expected']:
            raise ValueError('refusal fixture must preserve source')
    if {f['kind'] for f in record['fixtures']} != {'positive', 'refusal'}:
        raise ValueError('positive and refusal fixtures are required')
    return deepcopy(record)


def registry():
    result = {}
    for name in ('configparser.json', 'pathlib.json'):
        record = validate_contract(strict_loads(files('renewal_engine').joinpath('recipe_data', name).read_text()))
        if record['id'] in result:
            raise ValueError('duplicate recipe identity')
        result[record['id']] = record
    return result


def select(ids=None):
    catalog = registry()
    ids = [DEFAULT] if ids is None else list(ids)
    if not ids or len(set(ids)) != len(ids) or any(i not in catalog for i in ids):
        raise ValueError('select distinct known recipe IDs')
    for identity in ids:
        if any(dep not in ids[:ids.index(identity)] for dep in catalog[identity]['dependencies']):
            raise ValueError('recipe dependencies must precede the dependent recipe')
    return [catalog[i] for i in ids]


def discover_pathlib(data, *, shadowed=False):
    hashed = digest(data)
    try:
        if len(data) > 1048576 or data.startswith(b'\xef\xbb\xbf'):
            raise ValueError('requires bounded UTF-8 source without BOM')
        tree = ast.parse(data.decode('utf-8'))
    except (ValueError, SyntaxError, UnicodeError, RecursionError) as exc:
        return Discovery((), (Finding(1, 1, 'REVIEW NEEDED', str(exc)),), hashed)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'link_to']
    dynamic = any(isinstance(n, (ast.Global, ast.Nonlocal))
                  or isinstance(n, (ast.Attribute, ast.Subscript)) and isinstance(n.ctx, (ast.Store, ast.Del))
                  or isinstance(n, ast.Attribute) and n.attr == '__dict__'
                  or isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in {'exec','eval','setattr','delattr','globals','locals','vars','__import__'}
                  for n in ast.walk(tree))
    supported, edits = set(), []
    lines = data.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    def span(n):
        return offsets[n.lineno-1] + n.col_offset, offsets[n.end_lineno-1] + n.end_col_offset
    if not shadowed and not dynamic:
        for func in tree.body:
            if not isinstance(func, ast.FunctionDef) or func.decorator_list:
                continue
            body = func.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
                body = body[1:]
            if len(body) < 4:
                continue
            imp, first, second, stmt = body[:4]
            if not isinstance(imp, ast.ImportFrom) or imp.module != 'pathlib' or imp.level or len(imp.names) != 1 or imp.names[0].name != 'Path':
                continue
            imported = imp.names[0].asname or 'Path'
            params = {p.arg for p in func.args.posonlyargs + func.args.args + func.args.kwonlyargs}
            params.update(p.arg for p in (func.args.vararg, func.args.kwarg) if p)
            if imported in params:
                continue
            receivers = []
            for assign in (first, second):
                if not (isinstance(assign, ast.Assign) and len(assign.targets) == 1 and isinstance(assign.targets[0], ast.Name)
                        and isinstance(assign.value, ast.Call) and isinstance(assign.value.func, ast.Name)
                        and assign.value.func.id == imported and len(assign.value.args) == 1 and not assign.value.keywords
                        and isinstance(assign.value.args[0], (ast.Name, ast.Constant))):
                    break
                arg = assign.value.args[0]
                if isinstance(arg, ast.Name) and arg.id not in params:
                    break
                name = assign.targets[0].id
                if name in params or name == imported or name in receivers:
                    break
                receivers.append(name)
            if len(receivers) != 2 or not isinstance(stmt, ast.Expr) or not isinstance(stmt.value, ast.Call):
                continue
            call = stmt.value
            if call not in calls or not isinstance(call.func.value, ast.Name) or call.func.value.id != receivers[0]:
                continue
            if len(call.args) == 1 and not call.keywords:
                target = call.args[0]
            elif not call.args and len(call.keywords) == 1 and call.keywords[0].arg == 'target':
                target = call.keywords[0].value
            else:
                continue
            if not isinstance(target, ast.Name) or target.id != receivers[1]:
                continue
            receiver_start, receiver_end = span(call.func.value)
            target_start, target_end = span(target)
            _, attribute_end = span(call.func)
            replacements = [(receiver_start, receiver_end, receivers[0], receivers[1]),
                            (attribute_end-7, attribute_end, 'link_to', 'hardlink_to'),
                            (target_start, target_end, receivers[1], receivers[0])]
            if any(data[start:end] != before.encode() for start,end,before,after in replacements):
                continue
            edits.extend(Edit(start,end,before,after,
                              'Preserve hard-link direction: destination.hardlink_to(source)')
                         for start,end,before,after in replacements)
            supported.add(id(call))
    reason = ('local pathlib shadow requires review' if shadowed else
              'dynamic mutation requires review' if dynamic else 'requires local Path import, two direct constructions, then source.link_to(destination)')
    return Discovery(tuple(sorted(edits, key=lambda e:e.start)), tuple(Finding(c.lineno,c.col_offset+1,
                     'SUPPORTED' if id(c) in supported else 'REVIEW NEEDED',
                     'local Path bindings; filesystem behavior requires differential review' if id(c) in supported else reason)
                     for c in sorted(calls,key=lambda c:(c.lineno,c.col_offset))), hashed)


def compose(data, ids=None, *, shadowed_modules=()):
    steps, current = [], data
    for contract in select(ids):
        identity = contract['id']
        fn, module = (discover, 'configparser') if identity == DEFAULT else (discover_pathlib, 'pathlib')
        found = fn(current, shadowed=module in shadowed_modules)
        candidate = transform(current, found)
        steps.append({'recipe': identity, 'version': contract['version'], 'contract_sha256': digest(json.dumps(contract,sort_keys=True,separators=(',',':')).encode()),
                      'input_sha256': digest(current), 'output_sha256': digest(candidate), **found.json()})
        current = candidate
    return current, strict_loads(json.dumps(steps))


def conformance():
    checks = []
    for contract in select([DEFAULT, PATHLIB]):
        for fixture in contract['fixtures']:
            original = fixture['source'].encode()
            candidate, _ = compose(original, [contract['id']])
            repeated, _ = compose(candidate, [contract['id']])
            ok = candidate == fixture['expected'].encode() and repeated == candidate
            checks.append({'recipe':contract['id'], 'fixture':fixture['name'], 'kind':fixture['kind'], 'passed':ok})
    return {'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL', 'checks':checks,
            'behavior_measured':False}
