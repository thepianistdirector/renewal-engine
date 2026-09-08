"""Exercise an actual packaged 0.5 CLI in a new private output directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('cli','baseline','target','out'):
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    cli=args.cli.resolve(strict=True);baseline=args.baseline.resolve(strict=True);target=args.target.resolve(strict=True)
    root=args.out.resolve();root.mkdir(mode=0o700)
    checks=[]
    def call(label,arguments,expected=0):
        capture=subprocess.run([str(target),str(cli),*map(str,arguments)],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
        (root/(label+'.stdout')).write_bytes(capture.stdout);(root/(label+'.stderr')).write_bytes(capture.stderr)
        if capture.returncode != expected:
            raise RuntimeError(label+' returned '+str(capture.returncode)+': '+capture.stderr.decode(errors='replace'))
        checks.append({'id':label,'exitcode':capture.returncode,'expected':expected,'passed':True})
        return capture.stdout
    call('version',['--version']);call('conformance',['conformance'])
    source=root/'input';source.mkdir()
    original=b'def link(source, target):\n    from pathlib import Path\n    s = Path(source)\n    t = Path(target)\n    s.link_to(t)\n'
    (source/'link.py').write_bytes(original)
    (source/'entry.py').write_text('from link import link\n')
    (source/'pyproject.toml').write_text('[project]\nname="packaged-fixture"\nversion="0.0.0"\nrequires-python=">=3.11"\n')
    call('inspection',['inspect',source,'--recipe','pathlib-local-hardlink-v1','--recipe','configparser-local-prefix-v1','--out',root/'inspection'])
    call('inspection-reopen',['verify',root/'inspection'])
    if (source/'link.py').read_bytes()!=original:
        raise RuntimeError('source modified')
    impact=json.loads((root/'inspection/impact.json').read_text())
    if 'entry.py' not in impact['impacted_paths']:
        raise RuntimeError('missing reverse dependency')
    choices=json.loads(call('hunks',['hunks',root/'inspection']))
    approval=json.loads(call('approval',['approve',root/'inspection','--source',source,'--hunk',choices[0]['id'],'--out',root/'approved']))
    call('approval-reopen',['verify-approval',root/'approved','--source',source,'--sha256',approval['approval_sha256']])
    (source/'link.py').write_bytes(original+b'# concurrent change\n')
    call('stale-refused',['verify-approval',root/'approved','--source',source,'--sha256',approval['approval_sha256']],2)
    call('inspection-updated',['inspect',source,'--recipe','pathlib-local-hardlink-v1','--out',root/'updated'])
    for command,name in [('demo','configparser'),('hardlink-demo','hardlink')]:
        for negative in (False,True):
            label=name+('-negative' if negative else '-normal')
            arguments=[command,'--baseline',baseline,'--target',target,'--out',root/label]
            if negative:arguments+=['--negative-control']
            call(label,arguments,1 if negative else 0)
            call(label+'-reopen',['verify',root/label])
    old=[{'value':True,'stdout':'PRIVATE-CANARY'}]*2
    policy={'schema_version':1,'owner':'PRIVATE-OWNER','reason':'exact','rules':[]}
    for name,value in [('old',old),('new',old),('policy',policy)]:
        (root/(name+'.json')).write_text(json.dumps(value))
    call('comparison',['compare','--original',root/'old.json','--candidate',root/'new.json','--policy',root/'policy.json','--out',root/'comparison'])
    call('comparison-reopen',['verify',root/'comparison'])
    call('summary',['export-summary',root/'comparison','--out',root/'summary.json'])
    if 'PRIVATE' in (root/'summary.json').read_text():
        raise RuntimeError('private canary leaked into summary')
    (root/'new.json').write_text(json.dumps([{'value':False,'stdout':'PRIVATE-CANARY'}]*2))
    call('comparison-regression',['compare','--original',root/'old.json','--candidate',root/'new.json','--policy',root/'policy.json','--out',root/'regression'],1)
    (root/'new.json').write_text(json.dumps([{'value':True,'stdout':'PRIVATE-CANARY'},{'value':True,'stdout':'different'}]))
    call('comparison-unstable',['compare','--original',root/'old.json','--candidate',root/'new.json','--policy',root/'policy.json','--out',root/'unstable'],1)
    executable=root/'exec-input';executable.mkdir()
    (executable/'main.py').write_text('from pathlib import Path\nPath("/work/output").write_bytes(b"exact file effect")\nprint("isolated output")\n')
    call('execution-authorization-refused',['execute',executable,'--entrypoint','main.py','--out',root/'unauthorized'],2)
    if (root/'unauthorized').exists():
        raise RuntimeError('unauthorized execution created artifacts')
    probe=json.loads(call('isolation-probe',['isolation-probe']))
    if not probe['verified']:raise RuntimeError('isolation unavailable')
    call('execution',['execute',executable,'--entrypoint','main.py','--authorize-execution','--out',root/'executed'])
    call('execution-reopen',['verify',root/'executed'])
    execution=json.loads((root/'executed/results.json').read_text())
    if bytes.fromhex(execution['capture']['work_output_hex'])!=b'exact file effect':
        raise RuntimeError('independent file observation mismatch')
    # Retained evidence tamper must not reopen. Keep the damaged attempt separate.
    saved=json.loads((root/'comparison/results.json').read_text());saved['raw']['original'][0]['value']=1
    (root/'comparison/results.json').write_text(json.dumps(saved))
    call('strict-tamper-refused',['verify',root/'comparison'],2)
    summary={'status':'PASS','cli_sha256':hashlib.sha256(cli.read_bytes()).hexdigest(),
             'checks':checks,'check_count':len(checks),'environment':'Local Linux x86_64; actual packaged CLI with CPython 3.11.16 / 3.12.14',
             'human_observation':False,'external_observation':False,'public_artifact':False}
    (root/'summary-checks.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
