import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .artifacts import inspect


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect and review bounded Python migrations locally; execution requires its explicit command.")
    parser.add_argument("--version", action="version", version="Renewal Engine " + __version__)
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("inspect", help="save an inspection, focused patch and candidate Python source snapshot")
    scan.add_argument("source", type=Path, help="a .py file or bounded directory")
    scan.add_argument("--out", type=Path, required=True, help="new directory outside the selected source, with an existing parent")
    scan.add_argument("--recipe", action="append", help="exact recipe ID; repeat for ordered composition (default: configparser-local-prefix-v1)")
    demo_parser = commands.add_parser("demo", help="execute only the bundled trusted reference with two explicit runtimes")
    demo_parser.add_argument("--baseline", type=Path, required=True, help="trusted Linux CPython 3.11.16 executable")
    demo_parser.add_argument("--target", type=Path, required=True, help="trusted Linux CPython 3.12.14 executable")
    demo_parser.add_argument("--out", type=Path, required=True, help="new directory with an existing parent")
    demo_parser.add_argument("--negative-control", action="store_true", help="deliberately corrupt the diagnostic source; comparison must fail")
    verify = commands.add_parser("verify", help="reopen saved evidence without executing source")
    verify.add_argument("run", type=Path)
    commands.add_parser('recipes',help='list versioned shipped recipe contracts')
    commands.add_parser('conformance',help='check shipped recipe fixtures without executing selected code')
    hardlink=commands.add_parser('hardlink-demo',help='measure only the bundled hardlink fixture on two explicit runtimes')
    hardlink.add_argument('--baseline',type=Path,required=True)
    hardlink.add_argument('--target',type=Path,required=True)
    hardlink.add_argument('--out',type=Path,required=True)
    hardlink.add_argument('--negative-control',action='store_true')
    review=commands.add_parser('hunks',help='list exact selectable hunks from a saved inspection')
    review.add_argument('run',type=Path)
    approval=commands.add_parser('approve',help='save selected hunks as an exact approved candidate; original stays unchanged')
    approval.add_argument('run',type=Path);approval.add_argument('--source',type=Path,required=True)
    approval.add_argument('--hunk',action='append',required=True);approval.add_argument('--out',type=Path,required=True)
    check_approval=commands.add_parser('verify-approval',help='check exact approval against current original and candidate')
    check_approval.add_argument('run',type=Path);check_approval.add_argument('--source',type=Path,required=True)
    check_approval.add_argument('--sha256',required=True)
    comparison=commands.add_parser('compare',help='compare supplied repeated JSON observations with a frozen narrow policy')
    for name in ('original','candidate','policy','out'):
        comparison.add_argument('--'+name,type=Path,required=True)
    execute=commands.add_parser('execute',help='explicitly execute a Python snapshot in the verified narrow Linux isolation profile')
    execute.add_argument('source',type=Path);execute.add_argument('--entrypoint',required=True)
    execute.add_argument('--out',type=Path,required=True);execute.add_argument('--authorize-execution',action='store_true')
    commands.add_parser('isolation-probe',help='run trusted denial probes; no selected project code runs')
    export=commands.add_parser('export-summary',help='export only allowlisted counts/status/hashes from verified evidence')
    export.add_argument('run',type=Path);export.add_argument('--out',type=Path,required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect(args.source, args.out, args.recipe)
        elif args.command == "demo":
            from .workflow import demo
            result = demo(args.out, args.baseline, args.target, args.negative_control)
        elif args.command == 'verify':
            from .workflow import verify_saved
            result = verify_saved(args.run)
        elif args.command == 'recipes':
            from .recipes import registry
            print(json.dumps(registry(),indent=2));return 0
        elif args.command == 'conformance':
            from .recipes import conformance
            result=conformance()
        elif args.command == 'hardlink-demo':
            from .hardlink import demo
            result=demo(args.out,args.baseline,args.target,args.negative_control)
        elif args.command == 'hunks':
            from .review import hunks
            print(json.dumps(hunks(args.run),indent=2));return 0
        elif args.command == 'approve':
            from .review import approve
            result=approve(args.run,args.source,args.hunk,args.out)
        elif args.command == 'verify-approval':
            from .review import verify_approval
            result=verify_approval(args.run,args.source,args.sha256)
        elif args.command == 'compare':
            from .session import compare_files
            result=compare_files(args.original,args.candidate,args.policy,args.out)
        elif args.command == 'execute':
            from .session import execute
            result=execute(args.source,args.entrypoint,args.out,args.authorize_execution)
        elif args.command == 'isolation-probe':
            from .isolation import probe_isolation
            result=probe_isolation()
            print(json.dumps(result,indent=2));return 0 if result['verified'] else 2
        elif args.command == 'export-summary':
            from .session import export_summary
            result=export_summary(args.run,args.out)
    except KeyboardInterrupt:
        print("Interrupted. Retain any incomplete run; restart into a new output directory.", file=sys.stderr)
        return 130
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("Renewal Engine: " + str(exc), file=sys.stderr)
        return 2
    if args.command == "verify":
        print(result["status"] + ": " + result["result"])
    elif args.command in {'inspect','demo','hardlink-demo'}:
        print(result['status'] + ': saved report.html, changes.patch, manifest.json and candidate/.')
    else:
        print(json.dumps({k:v for k,v in result.items() if k not in {'raw','capture','expected_changes','variance','regressions'}},indent=2))
    return 1 if result['status'] in {'REGRESSION','UNSTABLE','FAIL','EXECUTION FAILED','APPLICATION ERROR'} else 0


if __name__ == "__main__":
    sys.exit(main())
