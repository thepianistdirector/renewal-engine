"""Actual runtime evidence for the shipped, digest-pinned Path migration only."""
from copy import deepcopy
from importlib.resources import files
import json
import re
from .jsonio import loads as strict_loads
from pathlib import Path
import stat

from .artifacts import atomic_json, new_run, read_regular
from .comparison import differences
from .execution import run_process, runtime_identity, validate_capture
from .recipes import PATHLIB, compose
from .transformation import digest, patch


def resources():
    root = files('renewal_engine').joinpath('hardlink_reference')
    trust = strict_loads(root.joinpath('trust.json').read_text())
    data = {name:root.joinpath(name).read_bytes() for name in ('program.py','harness.py','cases.json','policy.json')}
    if any(digest(value) != trust[name] for name,value in data.items()):
        raise ValueError('bundled hardlink reference digest mismatch')
    return trust, data


def effects(directory):
    content, identities, directories = {}, {}, []
    for path in sorted(directory.iterdir()):
        if path.name in {'process.json','observation.json'}:
            continue
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            if list(path.iterdir()):
                raise ValueError('unexpected nested hardlink effect')
            directories.append(path.name)
        elif stat.S_ISREG(info.st_mode):
            raw = read_regular(path)
            content[path.name] = {'sha256':digest(raw),'size':len(raw),'bytes_hex':raw.hex()}
            identities[path.name] = (info.st_dev, info.st_ino)
        else:
            raise ValueError('unexpected hardlink effect type')
    links = [[a,b] for a in identities for b in identities if a < b and identities[a] == identities[b]]
    return {'files':content,'directories':directories,'hardlinks':links}


def compare(records, cases, policy):
    results = []
    for case in cases:
        original = records['original'][case['id']]
        candidate = records['candidate'][case['id']]
        variance = []
        for side, observations in [('original',original),('candidate',candidate)]:
            for index in range(1,len(observations)):
                variance.extend({'side':side,'repetition':index,**d} for d in differences(observations[0],observations[index]))
        delta, expected = [], []
        for old, new in zip(original,candidate):
            left,right = deepcopy(old),deepcopy(new)
            if left['warnings'] == [policy['warning']] and right['warnings'] == []:
                left['warnings'] = []
                expected.append({'path':'$.warnings','reason':policy['reason']})
            else:
                delta.append({'path':'$.warnings','problem':'exact expected warning transition absent'})
            delta.extend(differences(left,right))
        results.append({'id':case['id'],'status':'UNSTABLE' if variance else 'REGRESSION' if delta else 'PASS',
                        'original':original,'candidate':candidate,'differences':delta,'variance':variance,'expected_changes':expected})
    return results


def demo(destination, baseline, target, negative=False):
    from . import __version__
    from .report import render
    trust, bundled = resources()
    policy,cases = strict_loads(bundled['policy.json']),strict_loads(bundled['cases.json'])
    new_run(destination)
    try:
        reference=destination/'reference';reference.mkdir()
        for name,data in bundled.items():
            (reference/name).write_bytes(data)
        atomic_json(reference/'trust.json',trust)
        identities = {'original':runtime_identity(baseline,policy['baseline'],destination),
                      'candidate':runtime_identity(target,policy['target'],destination)}
        (destination/'original').mkdir();(destination/'candidate').mkdir()
        source=bundled['program.py'];(destination/'original/program.py').write_bytes(source)
        records={'original':{},'candidate':{}}
        candidate=None
        for side,runtime in [('original',baseline),('candidate',target)]:
            if side == 'candidate':
                candidate,steps=compose(source,[PATHLIB])
                if negative:
                    candidate=source.replace(b's.link_to(t)',b's.hardlink_to(t)')
                if digest(candidate) != trust['negative_sha256' if negative else 'candidate_sha256']:
                    raise ValueError('independent candidate digest mismatch')
                (destination/'candidate/program.py').write_bytes(candidate)
                (destination/'changes.patch').write_text(patch(source,candidate,'program.py'))
            for case in cases:
                records[side][case['id']]=[]
                for repetition in range(policy['repetitions']):
                    cwd=destination/'observations'/side/case['id']/str(repetition);cwd.mkdir(parents=True)
                    capture=run_process([str(runtime.resolve()),'-I','-S','-B',str((reference/'harness.py').resolve()),str((destination/side/'program.py').resolve())],cwd,json.dumps(case).encode())
                    atomic_json(cwd/'process.json',capture);validate_capture(capture)
                    observation=strict_loads(capture['stdout']);observation['effects']=effects(cwd)
                    atomic_json(cwd/'observation.json',observation)
                    records[side][case['id']].append(observation)
        rows=[{'path':'program.py','source_sha256':digest(source),'candidate_sha256':digest(candidate),'changed':True,'edits':[] if negative else steps[0]['edits'],'findings':steps[0]['findings']}]
        comparisons=compare(records,cases,policy)
        status='UNSTABLE' if any(c['status']=='UNSTABLE' for c in comparisons) else 'REGRESSION' if any(c['status']=='REGRESSION' for c in comparisons) else 'PASS'
        manifest={'schema':2,'mode':'trusted-hardlink','tool_version':__version__,'files':rows,'runtimes':identities,'trust':trust,'negative_control':negative}
        result={'status':status,'behavior_measured':True,'files':rows,'cases':comparisons,'negative_control':negative,
                'negative_control_description':'The method is renamed without reversing source and destination. File and exception observations must reject this candidate.',
                'limitations':['Only the shipped trusted hardlink fixture ran on these exact runtimes.','Hard-link equality and retained bytes are observed; inode numbers are deliberately not cross-run identities.','No arbitrary project execution or human approval is implied.']}
        atomic_json(destination/'manifest.json',manifest);atomic_json(destination/'results.json',result)
        (destination/'report.html').write_text(render(result,manifest))
        atomic_json(destination/'state.json',{'stage':'COMPARED','complete':True,'behavior_measured':True,'result':status})
        return result
    except BaseException:
        atomic_json(destination/'state.json',{'stage':'INCOMPLETE','complete':False,'recovery':'Retain this attempt; restart into a new directory.'})
        raise


def verify(directory):
    from .execution import validate_runtime_record
    manifest=strict_loads(read_regular(directory/'manifest.json'))
    state=strict_loads(read_regular(directory/'state.json'))
    result=strict_loads(read_regular(directory/'results.json'))
    trust,bundled=resources()
    if manifest.get('mode') != 'trusted-hardlink' or manifest.get('trust') != trust or not state.get('complete') or state.get('stage') != 'COMPARED':
        raise ValueError('invalid or incompatible hardlink evidence')
    for name,data in bundled.items():
        if read_regular(directory/'reference'/name) != data:
            raise ValueError('saved hardlink reference changed')
    negative=manifest.get('negative_control')
    if type(negative) is not bool or result.get('negative_control') is not negative:
        raise ValueError('invalid negative-control label')
    source=read_regular(directory/'original/program.py');candidate=read_regular(directory/'candidate/program.py')
    if digest(source) != trust['program.py'] or digest(candidate) != trust['negative_sha256' if negative else 'candidate_sha256']:
        raise ValueError('hardlink source or candidate changed')
    if read_regular(directory/'changes.patch') != patch(source,candidate,'program.py').encode():
        raise ValueError('hardlink patch changed')
    if result.get('files') != manifest.get('files') or len(manifest['files']) != 1 or manifest['files'][0]['source_sha256'] != digest(source) or manifest['files'][0]['candidate_sha256'] != digest(candidate):
        raise ValueError('hardlink source manifest changed')
    policy,cases=strict_loads(bundled['policy.json']),strict_loads(bundled['cases.json'])
    records={'original':{},'candidate':{}}
    for side in records:
        validate_runtime_record(manifest['runtimes'][side],policy['baseline' if side=='original' else 'target'])
        if not re.fullmatch(r'[0-9a-f]{64}',manifest['runtimes'][side].get('pathlib_sha256','')):
            raise ValueError('hardlink runtime lacks its relevant standard-library identity')
        for case in cases:
            records[side][case['id']]=[]
            for index in range(policy['repetitions']):
                cwd=directory/'observations'/side/case['id']/str(index)
                capture=strict_loads(read_regular(cwd/'process.json'));validate_capture(capture)
                record=strict_loads(capture['stdout']);record['effects']=effects(cwd)
                if differences(record,strict_loads(read_regular(cwd/'observation.json'))):
                    raise ValueError('hardlink observation differs from independent saved effects')
                records[side][case['id']].append(record)
    comparisons=compare(records,cases,policy)
    expected='UNSTABLE' if any(c['status']=='UNSTABLE' for c in comparisons) else 'REGRESSION' if any(c['status']=='REGRESSION' for c in comparisons) else 'PASS'
    if differences(comparisons,result.get('cases')) or result.get('status') != expected or state.get('result') != expected or result.get('behavior_measured') is not True or state.get('behavior_measured') is not True:
        raise ValueError('hardlink saved comparison changed')
    return {'status':'VERIFIED SAVED EVIDENCE','result':expected,'behavior_measured':True}
