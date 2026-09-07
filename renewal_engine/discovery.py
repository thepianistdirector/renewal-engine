"""Conservative syntax discovery; never import inspected source."""

from __future__ import annotations

import ast
import hashlib
import io
import tokenize
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Edit:
    start: int
    end: int
    before: str
    after: str
    reason: str


@dataclass(frozen=True)
class Finding:
    line: int
    column: int
    status: str
    reason: str


@dataclass(frozen=True)
class Discovery:
    edits: tuple[Edit, ...]
    findings: tuple[Finding, ...]
    source_sha256: str

    def json(self):
        return asdict(self)


def discover(data: bytes, *, shadowed: bool = False) -> Discovery:
    """Accept only the documented local import/construct/call prefix.

    Attribution assumes an unmodified standard-library import environment.
    It is not whole-program semantic equivalence or import-hook analysis.
    """
    source_hash = hashlib.sha256(data).hexdigest()
    if len(data) > 1_048_576:
        return Discovery((), (Finding(1, 1, "REVIEW NEEDED", "Python file exceeds 1 MiB"),), source_hash)
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(data).readline)
        if encoding not in ("utf-8", "utf-8-sig") or data.startswith(b"\xef\xbb\xbf"):
            raise ValueError("0.1 requires UTF-8 source without a byte-order mark")
        source = data.decode("utf-8")
        tree = ast.parse(source)
    except (SyntaxError, UnicodeError, ValueError, RecursionError) as exc:
        return Discovery((), (Finding(1, 1, "REVIEW NEEDED", str(exc)),), source_hash)

    lines = data.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    def offset(node, end=False):
        return offsets[(node.end_lineno if end else node.lineno) - 1] + (
            node.end_col_offset if end else node.col_offset
        )

    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Attribute) and n.func.attr == "readfp"]
    reasons = {id(c): "receiver or control flow is outside the proved local binding pattern" for c in calls}
    edits = []
    supported = set()
    # Dynamic name resolution and explicit attribute mutation invalidate this
    # deliberately small proof. Do not try to infer the effect of such code.
    dynamic = any(
        isinstance(n, (ast.Global, ast.Nonlocal))
        or isinstance(n, ast.Attribute) and isinstance(n.ctx, (ast.Store, ast.Del))
        or isinstance(n, ast.Attribute) and n.attr == "__dict__"
        or isinstance(n, ast.Subscript) and isinstance(n.ctx, (ast.Store, ast.Del))
        or isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        and n.func.id in {"exec", "eval", "setattr", "delattr", "globals", "locals", "vars", "__import__"}
        for n in ast.walk(tree)
    )
    if shadowed or dynamic:
        reason = "local configparser module/package shadows the standard library" if shadowed else "dynamic binding or attribute mutation requires review"
        return Discovery((), tuple(Finding(c.lineno, c.col_offset + 1, "REVIEW NEEDED", reason) for c in calls), source_hash)

    for func in tree.body:
        if not isinstance(func, ast.FunctionDef) or func.decorator_list:
            continue
        body = func.body
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            body = body[1:]
        if len(body) < 3:
            continue
        imp, assign, statement = body[:3]
        module_alias = class_alias = None
        if isinstance(imp, ast.Import) and len(imp.names) == 1 and imp.names[0].name == "configparser":
            module_alias = imp.names[0].asname or "configparser"
        elif isinstance(imp, ast.ImportFrom) and imp.module == "configparser" and not imp.level and len(imp.names) == 1 and imp.names[0].name == "ConfigParser":
            class_alias = imp.names[0].asname or "ConfigParser"
        else:
            continue
        params = {p.arg for p in func.args.posonlyargs + func.args.args + func.args.kwonlyargs}
        params.update(p.arg for p in (func.args.vararg, func.args.kwarg) if p)
        imported = module_alias or class_alias
        if imported in params:
            continue
        if not (isinstance(assign, ast.Assign) and len(assign.targets) == 1
                and isinstance(assign.targets[0], ast.Name) and isinstance(assign.value, ast.Call)):
            continue
        receiver = assign.targets[0].id
        if receiver in params or receiver == imported:
            continue
        ctor = assign.value
        if ctor.args or ctor.keywords:
            continue
        if module_alias:
            correct = (isinstance(ctor.func, ast.Attribute) and ctor.func.attr == "ConfigParser"
                       and isinstance(ctor.func.value, ast.Name) and ctor.func.value.id == module_alias)
        else:
            correct = isinstance(ctor.func, ast.Name) and ctor.func.id == class_alias
        if not correct or not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Call):
            continue
        call = statement.value
        if id(call) not in reasons or not isinstance(call.func.value, ast.Name) or call.func.value.id != receiver:
            continue
        args = call.args
        kw = call.keywords
        names = [k.arg for k in kw]
        simple = lambda n: isinstance(n, ast.Constant) or isinstance(n, ast.Name) and n.id in params
        if (len(args) > 2 or any(not simple(a) for a in args)
                or any(k.arg not in {"fp", "filename"} or not simple(k.value) for k in kw)
                or len(set(names)) != len(names)
                or (len(args) >= 1 and "fp" in names)
                or (len(args) == 2 and "filename" in names)
                or not args and "fp" not in names):
            reasons[id(call)] = "argument form is ambiguous or outside the supported fp/filename mapping"
            continue
        end = offset(call.func, True)
        call_edits = [Edit(end - 6, end, "readfp", "read_file", "Python 3.12 removed ConfigParser.readfp; preserve its read_file delegation")]
        for keyword in kw:
            before, after = ("filename", "source") if keyword.arg == "filename" else ("fp", "f")
            start = offset(keyword)
            call_edits.append(Edit(start, start + len(before), before, after, "Preserve the exact readfp argument binding in read_file"))
        if any(data[e.start:e.end] != e.before.encode() for e in call_edits):
            reasons[id(call)] = "identifier token is not an exact supported source spelling"
            continue
        edits.extend(call_edits)
        supported.add(id(call))
        reasons[id(call)] = "supported local ConfigParser binding; source and stream semantics require differential review"

    findings = tuple(Finding(c.lineno, c.col_offset + 1,
                            "SUPPORTED" if id(c) in supported else "REVIEW NEEDED", reasons[id(c)])
                     for c in sorted(calls, key=lambda c: (c.lineno, c.col_offset)))
    return Discovery(tuple(sorted(edits, key=lambda e: e.start)), findings, source_hash)
