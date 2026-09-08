"""Exclusive, restart-safe run artifacts and bounded source snapshots."""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

from .discovery import discover
from .transformation import digest, patch, transform

EXCLUDED = {".git", ".venv", "venv", "__pycache__", ".local", ".runs", ".build", "dist"}


def atomic_json(path: Path, value):
    temporary = path.with_name(path.name + ".pending")
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def read_regular(path: Path, limit=1_048_576) -> bytes:
    path = Path(path).absolute()
    parent_fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for name in path.parts[1:-1]:
            if name == '..':
                raise ValueError('parent traversal is not supported')
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
            os.close(parent_fd)
            parent_fd = child
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
    finally:
        os.close(parent_fd)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError("inspection requires a regular file of at most 1 MiB")
        data = stream.read(limit + 1)
        if len(data) > limit:
            raise ValueError("file grew beyond the inspection limit")
        return data


def snapshot(source: Path) -> dict[str, bytes]:
    if source.is_symlink():
        raise ValueError("source symlinks are not supported")
    if source.is_file():
        if source.suffix != ".py":
            raise ValueError("select a .py file or a directory")
        return {source.name: read_regular(source)}
    if not source.is_dir():
        raise ValueError("source does not exist or is not a directory")
    files = {}
    count = total = 0
    for directory, dirs, names in os.walk(source, followlinks=False):
        base = Path(directory)
        if len(base.relative_to(source).parts) > 32:
            raise ValueError("source tree exceeds the 32-level inspection limit")
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED)
        count += len(dirs) + len(names)
        if count > 10_000:
            raise ValueError("source tree exceeds the 10,000-entry inspection limit")
        for name in dirs + names:
            path = base / name
            if path.is_symlink():
                raise ValueError("source tree contains a symlink; select a bounded regular source tree")
            mode = path.lstat().st_mode
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                raise ValueError("source tree contains a special file")
        for name in sorted(names):
            if not name.endswith(".py"):
                continue
            path = base / name
            data = read_regular(path)
            total += len(data)
            if len(files) >= 1000 or total > 16 * 1_048_576:
                raise ValueError("source exceeds 1,000 Python files or 16 MiB")
            files[path.relative_to(source).as_posix()] = data
    if not files:
        raise ValueError("no Python source files found")
    return files


def new_run(destination: Path):
    if destination.is_symlink():
        raise ValueError("run destination may not be a symlink")
    destination.mkdir(mode=0o700, parents=False, exist_ok=False)
    atomic_json(destination / "state.json", {"stage": "STARTED", "complete": False,
                                            "recovery": "Retain this directory; restart into a new destination."})


def save_sources(destination: Path, sources: dict[str, bytes], *, shadowed=False, recipe_ids=None, shadowed_modules=()):
    original = destination / "original"
    candidate = destination / "candidate"
    original.mkdir()
    candidate.mkdir()
    shadowed = shadowed or any(Path(n).name == "configparser.py" or "configparser" in Path(n).parts[:-1] for n in sources)
    rows, diffs = [], []
    for name, data in sorted(sources.items()):
        # Names come from a snapshot; never accept archive/member paths here.
        if Path(name).is_absolute() or ".." in Path(name).parts:
            raise ValueError("invalid source member path")
        steps = None
        if recipe_ids is None:
            discovered = discover(data, shadowed=shadowed)
            transformed = transform(data, discovered)
            details = discovered.json()
        else:
            from .recipes import compose
            modules = set(shadowed_modules)
            if shadowed:
                modules.add('configparser')
            if any(Path(n).name == 'pathlib.py' or 'pathlib' in Path(n).parts[:-1] for n in sources):
                modules.add('pathlib')
            transformed, steps = compose(data, recipe_ids, shadowed_modules=modules)
            details = {'source_sha256': digest(data), 'steps':steps,
                       'edits':[edit for step in steps for edit in step['edits']],
                       'findings':[finding for step in steps for finding in step['findings']]}
        for base, content in [(original, data), (candidate, transformed)]:
            target = base / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(content)
            if base == original:
                target.chmod(0o444)
        diffs.append(patch(data, transformed, name))
        rows.append({"path": name, "source_sha256": digest(data), "candidate_sha256": digest(transformed),
                     "changed": transformed != data, **details})
    for directory, _, _ in os.walk(original, topdown=False):
        Path(directory).chmod(0o555)
    (destination / "changes.patch").write_text("".join(diffs), encoding="utf-8", newline="")
    return rows


def metadata_snapshot(source: Path):
    context = source.parent if source.is_file() else source
    metadata = {}
    for path in sorted(context.iterdir()):
        if path.name in {'pyproject.toml','poetry.lock','uv.lock','Pipfile.lock','setup.cfg','tox.ini'} or path.name.startswith('requirements') and path.suffix == '.txt':
            metadata[path.name] = read_regular(path)
    if sum(map(len, metadata.values())) > 4 * 1048576:
        raise ValueError('metadata exceeds 4 MiB')
    return metadata


def inspect(source: Path, destination: Path, recipe_ids=None):
    from . import __version__
    from .report import render

    source = source.absolute()
    destination = destination.absolute()
    if destination.resolve() == source.resolve() or source.is_dir() and source.resolve() in destination.resolve().parents:
        raise ValueError("run destination must be outside the selected source directory")
    from .recipes import select
    selected = select(recipe_ids)
    recipe_ids = [r['id'] for r in selected]
    sources = snapshot(source)
    context = source.parent if source.is_file() else source
    metadata = metadata_snapshot(source)
    new_run(destination)
    try:
        context = source.parent if source.is_file() else source
        shadowed = any((context / name).exists() or (context / name).is_symlink()
                       for name in ("configparser.py", "configparser"))
        modules = [m for m in ('configparser','pathlib') if any((context / n).exists() or (context / n).is_symlink() for n in (m, m+'.py'))]
        modules = sorted(set(modules) | {m for m in ('configparser','pathlib') if any(Path(n).name == m+'.py' or m in Path(n).parts[:-1] for n in sources)})
        rows = save_sources(destination, sources, shadowed=shadowed, recipe_ids=recipe_ids, shadowed_modules=modules)
        from .impact import analyze
        impact = analyze(sources, metadata, [r['path'] for r in rows if r['changed']])
        atomic_json(destination / 'impact.json', impact)
        (destination / 'metadata').mkdir()
        for name, data in metadata.items():
            (destination / 'metadata' / name).write_bytes(data)
        manifest = {"schema": 2, "tool_version": __version__, "mode": "inspection",
                    "recipes": selected, "shadowed_modules": modules,
                    "metadata_sha256": {n:digest(d) for n,d in metadata.items()},
                    "impact_sha256": digest((destination / "impact.json").read_bytes()),
                    "recipe": "configparser-local-prefix-v1", "runtimes": None,
                    "scope": "Python source snapshot only; non-Python resources and excluded directories are not copied",
                    "excluded_directories": sorted(EXCLUDED), "files": rows}
        atomic_json(destination / "manifest.json", manifest)
        (destination / "manifest.json").chmod(0o444)
        result = {"status": "INSPECTION ONLY", "behavior_measured": False, "files": rows,
                  "limitations": ["No original or candidate code was executed.",
                                  "Standard-library identity assumes no external import hooks or monkey-patching.",
                                  "Candidate contains only the inspected Python source; review-needed sites are unchanged.",
                                  "No general behavioral equivalence or maintainer adoption is established."]}
        atomic_json(destination / "results.json", result)
        (destination / "report.html").write_text(render(result, manifest), encoding="utf-8")
        atomic_json(destination / "state.json", {"stage": "INSPECTED", "complete": True,
                                                "behavior_measured": False})
        return result
    except BaseException:
        atomic_json(destination / "state.json", {"stage": "INCOMPLETE", "complete": False,
                                                "recovery": "Retain evidence; restart into a new destination."})
        raise
