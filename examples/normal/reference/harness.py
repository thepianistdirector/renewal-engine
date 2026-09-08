"""Original, bounded ConfigParser reference program. AGPL-3.0.

Prepared for the owner-reviewed 0.1 fixture decision. Not an upstream adoption.
Only this file and the declared tiny cases may be used by the demo runner.
"""

import contextlib
import io
import json
from pathlib import Path
import sys
import warnings


import hashlib
import runpy


def exception_record(exc):
    return {"module": type(exc).__module__, "type": type(exc).__name__,
            "message": str(exc), "args": exc.args, "attributes": vars(exc)}


def main():
    source = Path(sys.argv[1])
    trust = json.loads(Path(__file__).with_name("trust.json").read_text())
    if hashlib.sha256(source.read_bytes()).hexdigest() not in trust["program_hashes"].values():
        raise ValueError("unreviewed reference source refused")
    loaders = runpy.run_path(str(source))
    case = json.loads(sys.stdin.read())
    content = case["content"]
    path = Path("input.ini")
    path.write_bytes(content.encode("utf-8"))
    stream = path.open("r", encoding="utf-8", newline="")
    output = io.StringIO()
    error = None
    parser = None
    warning_records = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            with contextlib.redirect_stdout(output):
                loader = {"default": loaders["load_default"], "positional": loaders["load_positional"],
                          "keyword": loaders["load_keyword"]}[case["mode"]]
                parser = loader(stream, case.get("source"))
                print(json.dumps(dict(parser.items("app")), ensure_ascii=False, sort_keys=True))
                if case.get("query"):
                    print(parser.get("app", case["query"]))
        except Exception as exc:
            error = exception_record(exc)
        finally:
            position = position_error = None
            try:
                position = stream.tell()
            except Exception as exc:
                position_error = exception_record(exc)
            closed_after_call = stream.closed
            stream.close()
        warning_records = [{"category": type(w.message).__name__, "message": str(w.message),
                            "filename": Path(w.filename).name, "lineno": w.lineno}
                           for w in caught]
    serialized = None
    if parser is not None and error is None:
        saved = io.StringIO()
        parser.write(saved)
        serialized = saved.getvalue()
        Path("normalized.ini").write_bytes(serialized.encode("utf-8"))
    observed = {"stdout": output.getvalue(), "exception": error, "warnings": warning_records,
                "effects": {"stream_position": position, "stream_position_error": position_error,
                            "stream_closed_after_call": closed_after_call,
                            "stream_closed_after_cleanup": stream.closed,
                            "input_bytes_hex": path.read_bytes().hex(),
                            "normalized": serialized}}
    print(json.dumps(observed, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
