"""Bounded, offline project impact hints; never imports inspected modules."""
from __future__ import annotations

import ast
import re
import tomllib
from collections import defaultdict, deque
from pathlib import PurePosixPath

MAX_FILES = 4096
MAX_FILE_BYTES = 1_048_576
MAX_TOTAL_BYTES = 16_777_216
MAX_AST_NODES = 100_000


def _module(path):
    parts = list(PurePosixPath(path).with_suffix('').parts)
    if parts and parts[0] == 'src':
        parts.pop(0)
    if parts and parts[-1] == '__init__':
        parts.pop()
    return '.'.join(parts)


def _metadata(files, changed_modules):
    result = dict(python_requires=[], requirements=[], pin_conflicts=[],
                  lockfiles=[], review_hints=[], errors=[])
    pins = defaultdict(list)

    def requirement(raw, path, scope):
        item = dict(raw=raw, path=path, scope=scope)
        match = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]+\])?\s*==\s*([^\s;,*]+)\s*', raw)
        if match:
            name = re.sub(r'[-_.]+', '-', match[1]).lower()
            item.update(name=name, pin=match[2])
            pins[name].append(item)
        else:
            item['status'] = 'unresolved declaration; no dependency resolution performed'
        result['requirements'].append(item)

    total = 0
    for index, (path, data) in enumerate(sorted(files.items())):
        if index >= MAX_FILES:
            result['errors'].append(dict(path=path, reason='metadata file count limit exceeded'))
            break
        name = PurePosixPath(path).name
        if name in {'poetry.lock', 'uv.lock', 'Pipfile.lock'}:
            result['lockfiles'].append(dict(path=path, status='present; not resolved or validated'))
        total += len(data)
        if len(data) > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
            result['errors'].append(dict(path=path, reason='metadata byte limit exceeded'))
            continue
        try:
            text = data.decode('utf-8')
        except UnicodeError:
            result['errors'].append(dict(path=path, reason='metadata is not UTF-8'))
            continue
        for module in sorted(changed_modules):
            if module and re.search(r'(?<![\w.])' + re.escape(module) + r'(?![\w.])', text):
                result['review_hints'].append(dict(path=path, module=module,
                    reason='text reference to changed module; configuration behavior is unverified'))
        if name.startswith('requirements') and name.endswith('.txt'):
            for line in text.splitlines():
                line = re.split(r'\s+#', line, maxsplit=1)[0].strip()
                if line and not line.startswith('#'):
                    requirement(line, path, 'requirements file')
        if name != 'pyproject.toml':
            continue
        try:
            config = tomllib.loads(text)
            project = config.get('project', {})
            if not isinstance(project, dict):
                raise ValueError('project must be a table')
            python = project.get('requires-python')
            if python is not None:
                if not isinstance(python, str):
                    raise ValueError('requires-python must be a string')
                result['python_requires'].append(dict(path=path, range=python, source='project.requires-python'))
            dependencies = project.get('dependencies', [])
            optional = project.get('optional-dependencies', {})
            if not isinstance(optional, dict):
                raise ValueError('optional-dependencies must be a table')
            groups = [('project.dependencies', dependencies)] + [
                ('optional:' + group, values) for group, values in optional.items()]
            for scope, values in groups:
                if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                    raise ValueError(scope + ' must be a string array')
                for value in values:
                    requirement(value, path, scope)
            tool = config.get('tool', {})
            poetry = tool.get('poetry', {}) if isinstance(tool, dict) else {}
            deps = poetry.get('dependencies', {}) if isinstance(poetry, dict) else {}
            if isinstance(deps, dict):
                if isinstance(deps.get('python'), str):
                    result['python_requires'].append(dict(path=path, range=deps['python'], source='tool.poetry.dependencies.python'))
                for name, constraint in deps.items():
                    if name != 'python':
                        requirement(name + ' ' + str(constraint), path, 'poetry declaration (unresolved)')
        except (tomllib.TOMLDecodeError, ValueError, TypeError, RecursionError) as exc:
            result['errors'].append(dict(path=path, reason='invalid pyproject: ' + str(exc)))
    for name, items in sorted(pins.items()):
        if len({item['pin'] for item in items}) > 1:
            result['pin_conflicts'].append(dict(name=name, pins=sorted({i['pin'] for i in items}),
                declarations=items, status='potential conflict; scopes may not be installed together'))
    return result


def analyze(sources: dict[str, bytes], metadata: dict[str, bytes], changed_paths: list[str]) -> dict:
    """Return JSONable static review hints from caller-provided project bytes.

    Paths are project-relative POSIX names. ``src/`` is treated as a conventional
    source root as well as root-level modules. No files are opened here.
    """
    uncertain = []
    graph = {}
    trees = {}
    modules = defaultdict(set)
    exports = {}

    def issue(path, reason, **extra):
        uncertain.append(dict(path=path, reason=reason, **extra))

    total = 0
    for index, (path, data) in enumerate(sorted(sources.items())):
        if index >= MAX_FILES:
            issue(path, 'source file count limit exceeded; remaining sources omitted')
            break
        if not path.endswith('.py'):
            continue
        graph[path] = set()
        module = _module(path)
        if module:
            modules[module].add(path)
        total += len(data)
        if len(data) > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
            issue(path, 'source byte limit exceeded; imports unknown')
            continue
        try:
            tree = ast.parse(data, filename=path)
            if sum(1 for _ in ast.walk(tree)) > MAX_AST_NODES:
                issue(path, 'AST node limit exceeded; imports unknown')
                continue
            trees[path] = tree
        except (SyntaxError, UnicodeError, ValueError, RecursionError) as exc:
            issue(path, 'source parse failed: ' + str(exc))

    def resolve(path, module, line, required=True):
        targets = modules.get(module, set())
        graph[path].update(targets)
        if len(targets) > 1:
            issue(path, 'ambiguous local module; all candidates included', module=module, line=line)
        if not targets and required:
            issue(path, 'unresolved import: external, missing, or unsupported source root', module=module, line=line)
        # Importing a child executes package initializers too.
        parts = module.split('.')
        for count in range(1, len(parts)):
            graph[path].update(p for p in modules.get('.'.join(parts[:count]), ())
                               if PurePosixPath(p).name == '__init__.py')
        return bool(targets)

    for path, tree in trees.items():
        module = _module(path)
        package = module if PurePosixPath(path).name == '__init__.py' else module.rpartition('.')[0]
        public = None
        dynamic_calls = {'__import__', 'eval', 'exec', 'import_module'}
        for imported in ast.walk(tree):
            if isinstance(imported, ast.ImportFrom) and imported.module in {'importlib', 'builtins'}:
                dynamic_calls.update(alias.asname or alias.name for alias in imported.names
                                     if alias.name in {'import_module', '__import__', 'eval', 'exec'})
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if any(isinstance(t, ast.Name) and t.id == '__all__' for t in targets):
                    try:
                        value = ast.literal_eval(node.value)
                        if isinstance(value, (list, tuple)) and all(isinstance(v, str) for v in value):
                            public = set(value)
                        else:
                            raise ValueError('nonliteral export names')
                    except (ValueError, TypeError, RecursionError):
                        issue(path, 'dynamic __all__; public functions are inferred by name')
        exports[path] = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                    node.name in public if public is not None else not node.name.startswith('_')):
                try:
                    signature = '(' + ast.unparse(node.args) + ')'
                    if node.returns:
                        signature += ' -> ' + ast.unparse(node.returns)
                    exports[path].append(dict(name=node.name, signature=signature,
                        async_function=isinstance(node, ast.AsyncFunctionDef), line=node.lineno,
                        decorated=bool(node.decorator_list)))
                except RecursionError:
                    issue(path, 'signature depth limit exceeded', line=node.lineno)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    resolve(path, alias.name, node.lineno)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    pieces = package.split('.') if package else []
                    if node.level > len(pieces):
                        issue(path, 'relative import escapes known package', line=node.lineno)
                        continue
                    base = '.'.join(pieces[:len(pieces) - node.level + 1])
                    base += ('.' if base and node.module else '') + (node.module or '')
                else:
                    base = node.module or ''
                found = resolve(path, base, node.lineno, required=False)
                children = False
                for alias in node.names:
                    if alias.name == '*':
                        issue(path, 'wildcard reexport names unresolved', module=base, line=node.lineno)
                    else:
                        child = base + '.' + alias.name if base else alias.name
                        children = resolve(path, child, node.lineno, required=False) or children
                if not found and not children:
                    issue(path, 'unresolved from-import: external, missing, or ambiguous symbol', module=base, line=node.lineno)
            elif isinstance(node, ast.Call) and (
                isinstance(node.func, ast.Name) and node.func.id in dynamic_calls
                or isinstance(node.func, ast.Attribute) and node.func.attr in {'import_module', '__import__'}):
                issue(path, 'dynamic import or execution; targets unknown', line=node.lineno)
        graph[path].discard(path)

    reverse = defaultdict(set)
    for importer, imports in graph.items():
        for imported in imports:
            reverse[imported].add(importer)
    changed = {}
    all_impacted = set()
    for path in sorted(set(changed_paths)):
        reached = {path}
        queue = deque([path])
        while queue:
            for dependent in sorted(reverse[queue.popleft()]):
                if dependent not in reached:
                    reached.add(dependent)
                    queue.append(dependent)
        direct = reverse[path] - {path}
        impacted = reached & graph.keys()
        all_impacted.update(impacted)
        changed[path] = dict(direct_dependents=sorted(direct),
            transitive_dependents=sorted(reached - direct - {path}), impacted_paths=sorted(impacted))
        if path.endswith('.py') and path not in graph:
            issue(path, 'changed source absent from supplied graph; dependents unknown')
    return dict(schema_version=1, graph={p: sorted(v) for p, v in sorted(graph.items())},
        changed=changed, impacted_paths=sorted(all_impacted), exports=exports,
        uncertainties=uncertain, metadata=_metadata(metadata, {_module(p) for p in changed_paths if p.endswith('.py')}),
        limits=dict(max_files=MAX_FILES, max_file_bytes=MAX_FILE_BYTES,
                    max_total_bytes=MAX_TOTAL_BYTES, max_ast_nodes=MAX_AST_NODES),
        status='static review hints; not complete runtime or dependency resolution')
