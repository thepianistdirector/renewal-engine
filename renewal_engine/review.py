"""Select exact line hunks into a new candidate; stale originals invalidate approval."""
import difflib
import json
from .jsonio import loads as strict_loads
from pathlib import Path

from .artifacts import atomic_json, new_run, read_regular, snapshot, metadata_snapshot
from .transformation import digest, patch


def _json_hash(value):
    return digest(json.dumps(value,sort_keys=True,separators=(',',':')).encode())


def _load(directory):
    from .workflow import verify_saved
    verify_saved(directory)
    manifest=strict_loads(read_regular(directory/'manifest.json'))
    if manifest['mode'] != 'inspection':
        raise ValueError('select hunks from an inspection; trusted demo patches have a frozen identity')
    return manifest


def hunks(directory):
    manifest=_load(directory)
    rows=[]
    for row in manifest['files']:
        old=read_regular(directory/'original'/row['path']).decode().splitlines(keepends=True)
        new=read_regular(directory/'candidate'/row['path']).decode().splitlines(keepends=True)
        for index,group in enumerate(difflib.SequenceMatcher(a=old,b=new,autojunk=False).get_grouped_opcodes(3)):
            group=[list(op) for op in group]
            identity=_json_hash({'path':row['path'],'original':row['source_sha256'],'candidate':row['candidate_sha256'],'group':group})
            rows.append({'id':identity,'path':row['path'],'index':index,'original_line':group[0][1]+1,
                         'candidate_line':group[0][3]+1,'operations':group})
    return rows


def approve(directory, source, selected_ids, destination):
    manifest=_load(directory)
    available=hunks(directory)
    selected_ids=list(selected_ids)
    if not selected_ids or len(set(selected_ids)) != len(selected_ids) or set(selected_ids)-{h['id'] for h in available}:
        raise ValueError('select distinct current hunk IDs')
    current=snapshot(source)
    expected={row['path']:row['source_sha256'] for row in manifest['files']}
    metadata={name:digest(raw) for name,raw in metadata_snapshot(source).items()}
    if metadata != manifest.get('metadata_sha256',{}):
        raise ValueError('stale metadata; inspect current configuration before approval')
    if {name:digest(raw) for name,raw in current.items()} != expected:
        raise ValueError('stale source; inspect and characterize the current source before approval')
    source_resolved=source.resolve()
    dest_resolved=destination.resolve()
    if dest_resolved == source_resolved or source.is_dir() and source_resolved in dest_resolved.parents or dest_resolved == directory.resolve() or directory.resolve() in dest_resolved.parents:
        raise ValueError('approval output must be outside source and inspection')
    new_run(destination)
    try:
        (destination/'candidate').mkdir()
        rows=[];patches=[]
        for row in manifest['files']:
            name=row['path'];original=current[name]
            old=original.decode().splitlines(keepends=True)
            new=read_regular(directory/'candidate'/name).decode().splitlines(keepends=True)
            operations=[op for h in available if h['path']==name and h['id'] in selected_ids for op in h['operations'] if op[0]!='equal']
            for _,a,b,c,d in sorted(operations,key=lambda op:op[1],reverse=True):
                old[a:b]=new[c:d]
            candidate=''.join(old).encode()
            path=destination/'candidate'/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(candidate)
            patches.append(patch(original,candidate,name))
            rows.append({'path':name,'source_sha256':digest(original),'candidate_sha256':digest(candidate)})
        (destination/'changes.patch').write_text(''.join(patches),newline='')
        approval={'schema':1,'inspection_manifest_sha256':digest(read_regular(directory/'manifest.json')),
                  'selected_hunks':sorted(selected_ids),'files':rows,'metadata_sha256':metadata,'patch_sha256':digest(read_regular(destination/'changes.patch')),
                  'behavior_measured':False,'requires_characterization':True}
        approval['approval_sha256']=_json_hash(approval)
        atomic_json(destination/'approval.json',approval)
        atomic_json(destination/'state.json',{'stage':'APPROVED CANDIDATE','complete':True,'behavior_measured':False})
        return {'status':'APPROVED CANDIDATE','approval_sha256':approval['approval_sha256'],'behavior_measured':False,'requires_characterization':True}
    except BaseException:
        atomic_json(destination/'state.json',{'stage':'INCOMPLETE','complete':False})
        raise


def verify_approval(directory, source, expected_approval):
    state=strict_loads(read_regular(directory/'state.json'))
    approval=strict_loads(read_regular(directory/'approval.json'))
    identity=approval.pop('approval_sha256')
    if identity != expected_approval or _json_hash(approval) != identity or state != {'stage':'APPROVED CANDIDATE','complete':True,'behavior_measured':False}:
        raise ValueError('exact approval identity or state changed')
    current=snapshot(source)
    if {n:digest(d) for n,d in metadata_snapshot(source).items()} != approval['metadata_sha256']:
        raise ValueError('stale metadata invalidates approval')
    if {n:digest(d) for n,d in current.items()} != {r['path']:r['source_sha256'] for r in approval['files']}:
        raise ValueError('stale source invalidates approval')
    candidate=snapshot(directory/'candidate')
    if {n:digest(d) for n,d in candidate.items()} != {r['path']:r['candidate_sha256'] for r in approval['files']}:
        raise ValueError('candidate changed since approval')
    if digest(read_regular(directory/'changes.patch')) != approval['patch_sha256']:
        raise ValueError('approved patch changed')
    expected=''.join(patch(current[r['path']],candidate[r['path']],r['path']) for r in approval['files'])
    if read_regular(directory/'changes.patch') != expected.encode():
        raise ValueError('approved patch does not represent the selected candidate')
    return {'status':'VERIFIED APPROVAL','approval_sha256':identity,'behavior_measured':False}
