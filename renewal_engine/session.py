"""Retained comparison and explicitly authorized isolated execution workflows."""
import json
from .jsonio import loads as strict_loads
from pathlib import Path

from .artifacts import atomic_json, new_run, read_regular, snapshot
from .transformation import digest
from .comparison import differences


def compare_files(original, candidate, policy, destination):
    from .observations import compare_repeated
    inputs={name:read_regular(path) for name,path in [('original.json',original),('candidate.json',candidate),('policy.json',policy)]}
    result=compare_repeated(*(strict_loads(inputs[name]) for name in ('original.json','candidate.json','policy.json')))
    result_bytes=(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode()
    if len(result_bytes) > 8 * 1048576:
        raise ValueError('comparison result exceeds the 8 MiB retained evidence limit; reduce the supplied observation scope')
    new_run(destination)
    for name,data in inputs.items():
        (destination/name).write_bytes(data)
    atomic_json(destination/'manifest.json',{'schema':1,'mode':'repeated-comparison','inputs':{n:digest(d) for n,d in inputs.items()},
                                            'scope':'Comparison of supplied observations; origin and authenticity are not independently established'})
    atomic_json(destination/'results.json',result)
    atomic_json(destination/'state.json',{'stage':'COMPARED','complete':True,'result':result['status']})
    return result


def execute(source, entrypoint, destination, authorized=False):
    from .isolation import execute_python
    if authorized is not True:
        raise ValueError('pass --authorize-execution for this explicit Python snapshot and entrypoint')
    src=source.resolve();out=destination.resolve()
    if out == src or source.is_dir() and src in out.parents:
        raise ValueError('execution output must be outside the selected source')
    sources=snapshot(source)
    if entrypoint not in sources:
        raise ValueError('entrypoint must name an exact Python member of the snapshot')
    new_run(destination)
    try:
        saved=destination/'source';saved.mkdir()
        for name,data in sources.items():
            path=saved/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        capture=execute_python(saved,entrypoint,authorized=True)
        if {r['path']:r['sha256'] for r in capture['snapshot_manifest'] if r['type']=='file'} != {n:digest(d) for n,d in sources.items()}:
            raise ValueError('executed snapshot differs from retained source')
        status='EXECUTION FAILED' if capture['failure'] else 'APPLICATION ERROR' if capture['returncode'] != 0 else 'EXECUTED'
        result={'status':status,'behavior_measured':True,'equivalence_established':False,'capture':capture}
        atomic_json(destination/'results.json',result)
        atomic_json(destination/'manifest.json',{'schema':1,'mode':'isolated-execution','entrypoint':entrypoint,
                    'sources':{n:digest(d) for n,d in sources.items()},'results_sha256':digest(read_regular(destination/'results.json')),
                    'scope':'Python-only source snapshot; isolated single execution, no equivalence claim'})
        atomic_json(destination/'state.json',{'stage':'EXECUTED','complete':True,'result':status})
        return result
    except BaseException:
        atomic_json(destination/'state.json',{'stage':'INCOMPLETE','complete':False,'recovery':'Retain this attempt; restart into a new directory'})
        raise


def verify(directory):
    from .observations import compare_repeated
    manifest=strict_loads(read_regular(directory/'manifest.json'));state=strict_loads(read_regular(directory/'state.json'))
    data=read_regular(directory/'results.json',limit=8*1048576);result=strict_loads(data)
    if state.get('complete') is not True or state.get('result') != result.get('status'):
        raise ValueError('incomplete or inconsistent saved session')
    if manifest.get('mode') == 'repeated-comparison':
        if set(manifest['inputs']) != {'original.json','candidate.json','policy.json'} or state.get('stage') != 'COMPARED':
            raise ValueError('invalid repeated comparison manifest')
        inputs=[]
        for name in ('original.json','candidate.json','policy.json'):
            raw=read_regular(directory/name)
            if digest(raw) != manifest['inputs'][name]:
                raise ValueError('comparison input changed')
            inputs.append(strict_loads(raw))
        if differences(compare_repeated(*inputs), result):
            raise ValueError('saved repeated comparison differs from inputs')
        measured=False
    elif manifest.get('mode') == 'isolated-execution':
        if state.get('stage') != 'EXECUTED' or digest(data) != manifest['results_sha256']:
            raise ValueError('saved execution capture changed')
        sources=snapshot(directory/'source')
        if {n:digest(d) for n,d in sources.items()} != manifest['sources'] or manifest['entrypoint'] not in sources:
            raise ValueError('executed source snapshot changed')
        capture=result['capture']
        if {r['path']:r['sha256'] for r in capture['snapshot_manifest'] if r['type']=='file'} != manifest['sources']:
            raise ValueError('execution capture source identities disagree')
        for name in ('stdout','stderr'):
            raw=bytes.fromhex(capture[name+'_hex'])
            if raw.decode('utf-8',errors='backslashreplace') != capture[name]:
                raise ValueError('execution raw bytes disagree with decoded output')
        raw=bytes.fromhex(capture['work_output_hex'])
        if len(raw) != capture['work_output_size'] or digest(raw) != capture['work_output_sha256']:
            raise ValueError('execution output file integrity failed')
        status='EXECUTION FAILED' if capture['failure'] else 'APPLICATION ERROR' if capture['returncode'] != 0 else 'EXECUTED'
        if result.get('status') != status or result.get('equivalence_established') is not False or result.get('behavior_measured') is not True or not capture['probe']['verified']:
            raise ValueError('execution summary or isolation probe inconsistent')
        measured=True
    else:
        raise ValueError('unknown session mode')
    return {'status':'VERIFIED SAVED EVIDENCE','result':result['status'],'behavior_measured':measured}


def export_summary(directory, destination):
    from .workflow import verify_saved
    from .observations import shareable_summary
    verify_saved(directory)
    result=strict_loads(read_regular(directory/'results.json',limit=8*1048576))
    manifest=strict_loads(read_regular(directory/'manifest.json'))
    if manifest['mode'] == 'repeated-comparison':
        summary=shareable_summary(result)
        summary['behavior_measured']=False
        summary['observation_provenance']='Supplied observations; origin not independently established'
    else:
        status=result['status']
        allowed={'INSPECTION ONLY','PASS','REGRESSION','UNSTABLE','EXECUTED','EXECUTION FAILED','APPLICATION ERROR'}
        if status not in allowed:
            raise ValueError('unsupported export status')
        summary={'schema_version':1,'status':status,'files':len(result.get('files',[])),
                 'cases':len(result.get('cases',[])),'behavior_measured':result.get('behavior_measured',False),
                 'equivalence_established':False}
    # Export contains no relative/absolute member names, freeform strings, code,
    # stdout/stderr, policy reasons, environment, exception contents or raw data.
    summary['evidence_sha256']=digest(read_regular(directory/'results.json',limit=8*1048576))
    with destination.open('x',encoding='utf-8') as stream:
        json.dump(summary,stream,indent=2);stream.write('\n')
    return {'status':'EXPORTED SUMMARY','raw_evidence_included':False}
