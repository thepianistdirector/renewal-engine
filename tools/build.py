"""Build deterministic source/CLI candidate assets using the standard library."""

import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def main():
    import sys
    sys.path.insert(0,str(ROOT))
    from renewal_engine import __version__
    version=__version__
    destination=ROOT/'dist'/version;destination.mkdir(parents=True,exist_ok=True)
    archive=destination/'renewal-engine.pyz'
    content=io.BytesIO()
    content.write(b'#!/usr/bin/env python3\n')
    members={p.relative_to(ROOT).as_posix():p.read_bytes() for p in (ROOT/'renewal_engine').rglob('*')
             if p.is_file() and '__pycache__' not in p.parts and p.suffix in {'.py','.json','.md'}}
    members['__main__.py']=b'from renewal_engine.__main__ import main\nraise SystemExit(main())\n'
    members['LICENSE']=(ROOT/'LICENSE').read_bytes()
    with zipfile.ZipFile(content,'w',compression=zipfile.ZIP_DEFLATED) as zip:
        for name,data in sorted(members.items()):
            info=zipfile.ZipInfo(name,(2026,9,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644 << 16;zip.writestr(info,data)
    archive.write_bytes(content.getvalue());archive.chmod(0o755)
    source_files={}
    for name in ['README.md','CONTRIBUTING.md','LICENSE','THIRD_PARTY.md','ROADMAP.md','TASKS.md','project-plan.json','task-contracts.json','install.py','HANDOFF.md','GOAL.md']:
        source_files[name]=(ROOT/name).read_bytes()
    for directory in ['renewal_engine','tests','tools','docs']:
        for path in (ROOT/directory).rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts and (path.suffix in {'.py','.json','.md','.txt','.html','.png','.yml'} or path.name.endswith('LICENSE')):
                source_files[path.relative_to(ROOT).as_posix()]=path.read_bytes()
    for path in (ROOT/'examples').rglob('*'):
        if path.is_file():source_files[path.relative_to(ROOT).as_posix()]=path.read_bytes()
    source_files['renewal-engine.pyz']=archive.read_bytes()
    target=destination/f'renewal-engine-{version}.tar.gz'
    with target.open('wb') as output, gzip.GzipFile(fileobj=output,mode='wb',mtime=0,filename='') as compressed:
        with tarfile.open(fileobj=compressed,mode='w') as tar:
            for name,data in sorted(source_files.items()):
                info=tarfile.TarInfo(f'renewal-engine-{version}/'+name)
                info.size=len(data);info.mode=0o755 if name.endswith('.pyz') else 0o644
                info.mtime=0;tar.addfile(info,io.BytesIO(data))
    checksums={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [archive,target]}
    (destination/'SHA256SUMS').write_text(''.join(f'{value}  {name}\n' for name,value in checksums.items()))
    print(json.dumps({'status':'LOCAL RELEASE CANDIDATE','sha256':checksums},indent=2))


if __name__=='__main__':main()
