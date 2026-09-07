import argparse
import sys
from pathlib import Path

from . import __version__
from .artifacts import inspect


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect a bounded ConfigParser migration locally. Selected source is never executed.")
    parser.add_argument("--version", action="version", version="Renewal Engine " + __version__)
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("inspect", help="save an inspection, focused patch and candidate Python source snapshot")
    scan.add_argument("source", type=Path, help="a .py file or bounded directory")
    scan.add_argument("--out", type=Path, required=True, help="new directory outside the selected source, with an existing parent")
    demo_parser = commands.add_parser("demo", help="execute only the bundled trusted reference with two explicit runtimes")
    demo_parser.add_argument("--baseline", type=Path, required=True, help="trusted Linux CPython 3.11.16 executable")
    demo_parser.add_argument("--target", type=Path, required=True, help="trusted Linux CPython 3.12.14 executable")
    demo_parser.add_argument("--out", type=Path, required=True, help="new directory with an existing parent")
    demo_parser.add_argument("--negative-control", action="store_true", help="deliberately corrupt the diagnostic source; comparison must fail")
    verify = commands.add_parser("verify", help="reopen saved evidence without executing source")
    verify.add_argument("run", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect(args.source, args.out)
        elif args.command == "demo":
            from .workflow import demo
            result = demo(args.out, args.baseline, args.target, args.negative_control)
        else:
            from .workflow import verify_saved
            result = verify_saved(args.run)
    except KeyboardInterrupt:
        print("Interrupted. Retain any incomplete run; restart into a new output directory.", file=sys.stderr)
        return 130
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("Renewal Engine: " + str(exc), file=sys.stderr)
        return 2
    if args.command == "verify":
        print(result["status"] + ": " + result["result"])
    else:
        print(result["status"] + ": saved report.html, changes.patch, manifest.json and candidate/.")
    return 1 if result["status"] == "REGRESSION" else 0


if __name__ == "__main__":
    sys.exit(main())
