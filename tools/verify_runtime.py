"""Real Linux runtime/recovery verification of a packaged CLI; no mock runtimes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    cli, baseline, target, root = [p.resolve() for p in (args.cli, args.baseline, args.target, args.out)]
    root.mkdir()
    records = []

    def run(argv, expected=0):
        process = subprocess.run([sys.executable, str(cli), *map(str, argv)], cwd=root,
                                 capture_output=True, text=True, timeout=120)
        records.append({'command': list(map(str, argv)), 'returncode': process.returncode,
                        'stdout': process.stdout, 'stderr': process.stderr})
        if process.returncode != expected:
            raise AssertionError(records[-1])
        return process

    def demo(name, negative=False):
        run(['demo', '--baseline', baseline, '--target', target, '--out', name]
            + (['--negative-control'] if negative else []), 1 if negative else 0)
        run(['verify', name])
        result = json.loads((root/name/'results.json').read_text())
        assert len(result['cases']) == 12
        assert result['status'] == ('REGRESSION' if negative else 'PASS')
        assert result['regressions'] == (2 if negative else 0)
        assert result['expected_changes'] == 12
        return result

    demo('normal')
    demo('negative', True)
    run(['demo', '--baseline', baseline, '--target', target, '--out', 'normal'], 2)
    run(['inspect', 'normal/candidate/program.py', '--out', 'repeat'])
    assert (root/'repeat/changes.patch').read_text() == ''
    run(['verify', 'repeat'])

    # Deterministic stage fault injection stops a real worker after a partial
    # candidate write, or at comparison after all 24 actual runtime executions.
    # The supervisor then delivers a real SIGINT. No runtime/output is replaced.
    worker = root/'interrupt_worker.py'
    worker.write_text('''import os, signal, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from renewal_engine import workflow
mode, destination, baseline, target = sys.argv[2:]
def stop():
    (Path(destination)/"fault-stage.txt").write_text(mode)
    os.kill(os.getpid(), signal.SIGSTOP)
if mode == "candidate":
    original = Path.write_bytes
    def write(self, data):
        if self == Path(destination)/"candidate/program.py":
            original(self, data[:len(data)//2])
            stop()
        return original(self, data)
    Path.write_bytes = write
else:
    original = workflow.compare_case
    def compare(*args):
        stop()
        return original(*args)
    workflow.compare_case = compare
try:
    workflow.demo(Path(destination), Path(baseline), Path(target))
except KeyboardInterrupt:
    raise SystemExit(130)
''')
    for stage in ('candidate', 'comparison'):
        destination = root/('interrupted-'+stage)
        with (root/(stage+'-worker.log')).open('w') as log:
            child = subprocess.Popen([sys.executable, str(worker), str(cli), stage,
                                      str(destination), str(baseline), str(target)], cwd=root,
                                     stdout=log, stderr=log)
            try:
                deadline = time.monotonic()+120
                while time.monotonic() < deadline:
                    if child.poll() is not None:
                        raise AssertionError('worker ended before interruption')
                    status = Path('/proc')/str(child.pid)/'status'
                    if '\nState:\tT' in status.read_text():
                        break
                    time.sleep(0.05)
                else:
                    raise AssertionError('worker did not stop at requested stage')
                child.send_signal(signal.SIGINT)
                child.send_signal(signal.SIGCONT)
                assert child.wait(timeout=10) == 130
            finally:
                if child.poll() is None:
                    child.kill()
                    child.wait()
        state = json.loads((destination/'state.json').read_text())
        assert state['stage'] == 'INCOMPLETE' and state['complete'] is False
        assert not (destination/'results.json').exists()
        assert not (destination/'report.html').exists()
        assert sha(destination/'original/program.py') == sha(root/'normal/original/program.py')
        assert len(list((destination/'observations/original').glob('*/process.json'))) == 12
        if stage == 'candidate':
            assert (destination/'candidate/program.py').stat().st_size < (root/'normal/candidate/program.py').stat().st_size
            assert not (destination/'observations/candidate').exists()
        else:
            assert len(list((destination/'observations/candidate').glob('*/process.json'))) == 12
        run(['verify', destination.name], 2)
        records.append({'check': 'real SIGINT during '+stage, 'result': 'PASS',
                        'original_preserved': True, 'state': state, 'exit_code': 130})
    demo('restart')
    assert sha(root/'restart/candidate/program.py') == sha(root/'normal/candidate/program.py')
    for relative in ('reference/cases.json', 'reference/policy.json', 'candidate/program.py'):
        path = root/'normal'/relative
        data = path.read_bytes()
        path.chmod(0o644)
        path.write_bytes(data+b'\n')
        run(['verify', 'normal'], 2)
        path.write_bytes(data)
    run(['verify', 'normal'])
    evidence = {'status': 'RUNTIME VERIFIED', 'cli_sha256': sha(cli),
                'scope': 'Real pinned runtimes on the same Linux host, packaged CLI, deterministic stage fault injection and real SIGINT; not external or human validation.',
                'checks': records}
    (root/'runtime-verification.json').write_text(json.dumps(evidence, indent=2)+'\n')
    print('PASS: packaged normal/negative, idempotence, tamper refusal, two real SIGINT stages and safe restart')


if __name__ == '__main__':
    main()
