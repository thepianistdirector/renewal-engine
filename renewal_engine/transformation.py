"""Apply preconditioned source-span edits without touching original files."""

import difflib
import hashlib

from .discovery import Discovery


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform(data: bytes, discovery: Discovery) -> bytes:
    if digest(data) != discovery.source_sha256:
        raise ValueError("source digest precondition failed; inspect the current source again")
    previous_end = 0
    for edit in discovery.edits:
        if edit.start < previous_end or data[edit.start:edit.end] != edit.before.encode("utf-8"):
            raise ValueError("source edit precondition failed; inspect the current source again")
        previous_end = edit.end
    candidate = data
    for edit in reversed(discovery.edits):
        candidate = candidate[:edit.start] + edit.after.encode("utf-8") + candidate[edit.end:]
    return candidate


def patch(original: bytes, candidate: bytes, name: str) -> str:
    if original == candidate:
        return ""
    diff = difflib.unified_diff(original.decode("utf-8").splitlines(keepends=True),
                                candidate.decode("utf-8").splitlines(keepends=True),
                                fromfile="original/" + name, tofile="candidate/" + name)
    # Preserve the standard marker so patches of files without a final newline
    # can be applied with ordinary maintainer tools.
    return "".join(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n" for line in diff)
