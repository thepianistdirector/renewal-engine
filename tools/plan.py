#!/usr/bin/env python3
"""Validate and render Renewal Engine's sole mutable planning ledger (stdlib only)."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
RELEASE_ORDER = {'0.1': 0, 'later 0.x': 1, 'long-term': 2, 'exploratory': 3}
STATUSES = {'PLANNED', 'IN PROGRESS', 'IMPLEMENTED', 'AUTOMATED PASS',
            'RUNTIME VERIFIED', 'USER VALIDATED', 'RELEASE VERIFIED',
            'BLOCKED', 'FAILED', 'NOT TESTED'}
TASK_FIELDS = {'id', 'title', 'outcome', 'featureArea', 'wave', 'targetRelease',
               'prerequisiteIds', 'prerequisiteOutcomeCoverage', 'acceptanceCriteria',
               'sourceRefs', 'decisionRefs', 'basis', 'riskEvidenceNeeds', 'status',
               'evidence', 'platformId'}
GENERATED = ('ROADMAP.md', 'TASKS.md', 'task-contracts.json',
             'docs/publication/tanduna-plan-export.json',
             'docs/planning/source-mapping.md')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_text(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'


def validate(plan, root=ROOT, check_lineage=True):
    """Return errors; never repair a malformed ledger or infer completion."""
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    require(plan.get('schemaVersion') == 2, 'Unsupported schemaVersion')
    require(plan.get('slug') == 'renewal-engine', 'Wrong project scope')
    require(plan.get('canonicalSource') == 'project-plan.json', 'Wrong canonical source')
    tasks, waves = plan.get('tasks', []), plan.get('waves', [])
    require(200 <= len(tasks) <= 400, 'Task count outside owner range; document a source-grounded shortfall')
    require(20 <= len(waves) <= 40, 'Outcome wave count outside reviewed range')
    ids = [t.get('id') for t in tasks]
    wids = [w.get('id') for w in waves]
    require(len(ids) == len(set(ids)), 'Duplicate task IDs')
    require(len(wids) == len(set(wids)), 'Duplicate wave IDs')
    byid = {t.get('id'): t for t in tasks}
    bywave = {w.get('id'): w for w in waves}
    positions = {t.get('id'): n for n, t in enumerate(tasks)}
    for key in ('title', 'outcome'):
        normalized = [' '.join(str(t.get(key, '')).lower().split()) for t in tasks]
        require(len(normalized) == len(set(normalized)), f'Duplicate task {key} / outcome')
    assigned = []
    for n, wave in enumerate(waves, 1):
        wid = wave.get('id')
        require(wave.get('order') == n, f'{wid}: inconsistent wave order')
        for key in ('title', 'outcome', 'taskIds', 'exitEvidence', 'releaseHorizon'):
            require(bool(wave.get(key)), f'{wid}: missing {key}')
        members = wave.get('taskIds', [])
        assigned += members
        require(all(t in byid for t in members), f'{wid}: dangling assigned task')
        require(wave.get('releaseHorizon') in RELEASE_ORDER, f'{wid}: unknown release horizon')
        depwaves = wave.get('dependsOnWaves', [])
        expected_entries = []
        for d in depwaves:
            require(d in bywave, f'{wid}: dangling prerequisite wave {d}')
            if d in bywave:
                require(bywave[d].get('order', 0) < n, f'{wid}: wave prerequisite not earlier')
                expected_entries += bywave[d].get('taskIds', [])[-1:]
        require(wave.get('entryDependencies') == expected_entries, f'{wid}: entry dependency coverage differs from prerequisite waves')
        if members and members[0] in byid:
            require(byid[members[0]].get('prerequisiteIds') == expected_entries, f'{wid}: entry task does not consume wave prerequisites')
        if members and members[-1] in byid:
            require(set(members[:-1]).issubset(byid[members[-1]].get('prerequisiteIds', [])), f'{wid}: exit lacks peer outcome evidence')
    require(sorted(assigned) == sorted(ids), 'Orphan task or task assigned to more than one wave')
    for task in tasks:
        tid = task.get('id')
        require(TASK_FIELDS.issubset(task), f'{tid}: missing required fields {sorted(TASK_FIELDS - task.keys())}')
        require(bool(re.fullmatch(r'renewal-engine:N\d{2}-\d{2}', str(tid))), f'{tid}: unstable or unscoped ID')
        for key in ('title', 'outcome', 'featureArea', 'acceptanceCriteria', 'sourceRefs', 'riskEvidenceNeeds'):
            require(bool(task.get(key)), f'{tid}: empty {key}')
        require(all(isinstance(a, str) and len(a.split()) >= 8 for a in task.get('acceptanceCriteria', [])), f'{tid}: acceptance too vague or empty')
        require(task.get('status') in STATUSES, f'{tid}: unknown evidence status')
        if task.get('status') in {'IMPLEMENTED', 'AUTOMATED PASS', 'RUNTIME VERIFIED', 'USER VALIDATED', 'RELEASE VERIFIED'}:
            require(any(isinstance(e, dict) and e.get('level') == task['status']
                        and isinstance(e.get('path'), str) and bool(e['path'])
                        for e in task.get('evidence', [])),
                    f'{tid}: claimed evidence level lacks a matching artifact record')
        require(task.get('targetRelease') in RELEASE_ORDER, f'{tid}: unknown target release')
        wid = task.get('wave')
        require(wid in bywave, f'{tid}: missing wave')
        if wid in bywave:
            require(tid in bywave[wid].get('taskIds', []), f'{tid}: wave assignment mismatch')
            require(task.get('targetRelease') == bywave[wid].get('releaseHorizon'), f'{tid}: release scope differs from wave')
        if task.get('basis') == 'exploratory':
            require(task.get('targetRelease') == 'exploratory', f'{tid}: exploratory work is promised in a release')
        deps = task.get('prerequisiteIds', [])
        require(len(deps) == len(set(deps)), f'{tid}: duplicate prerequisites')
        coverage = task.get('prerequisiteOutcomeCoverage', [])
        require([c.get('id') for c in coverage] == deps, f'{tid}: missing prerequisite outcome coverage')
        for c in coverage:
            if c.get('id') in byid:
                require(c.get('neededOutcome') == byid[c['id']].get('outcome'), f'{tid}: stale prerequisite outcome description')
        for d in deps:
            require(d in byid, f'{tid}: dangling prerequisite {d}')
            if d not in byid:
                continue
            require(positions[d] < positions[tid], f'{tid}: prerequisite not earlier in execution order')
            require(RELEASE_ORDER.get(byid[d].get('targetRelease'), 99) <= RELEASE_ORDER.get(task.get('targetRelease'), -1), f'{tid}: release depends on a later or exploratory outcome')
        for ref in task.get('sourceRefs', []):
            require(ref in plan.get('sources', {}), f'{tid}: unresolved source reference {ref}')
        for ref in task.get('decisionRefs', []):
            require(ref in plan.get('decisions', {}), f'{tid}: unresolved decision reference {ref}')
        needs = task.get('riskEvidenceNeeds', {})
        require(bool(needs.get('risk')) and bool(needs.get('requiredEvidence')), f'{tid}: missing risk / evidence requirement')
    colors = {}
    def visit(tid):
        if colors.get(tid) == 1:
            errors.append(f'Dependency cycle through {tid}')
            return
        if colors.get(tid) == 2:
            return
        colors[tid] = 1
        for d in byid.get(tid, {}).get('prerequisiteIds', []):
            if d in byid:
                visit(d)
        colors[tid] = 2
    for tid in ids:
        visit(tid)
    mappings = plan.get('sourceMappings', [])
    expected_keys = {f'W{i}-T{j}' for i in range(1, 7) for j in (1, 2)}
    require(len(mappings) == 12 and {m.get('sourceKey') for m in mappings} == expected_keys, 'Missing / duplicate original source mapping')
    native_ids = {m.get('platformId'): m.get('sourceId') for m in mappings}
    for m in mappings:
        sid = m.get('sourceId')
        require(sid == 'renewal-engine:' + str(m.get('sourceKey')), f'{sid}: incorrect source scope')
        require(bool(m.get('reason')) and bool(m.get('treatment')), f'{sid}: missing lineage treatment')
        require(bool(m.get('successorIds')), f'{sid}: no successors')
        require(all(x in byid for x in m.get('successorIds', [])), f'{sid}: dangling successor')
        require(len(m.get('criterionCoverage', [])) == len(m.get('originalAcceptanceCriteria', [])), f'{sid}: missing criterion coverage')
        for original, coverage in zip(m.get('originalAcceptanceCriteria', []), m.get('criterionCoverage', [])):
            require(coverage.get('originalCriterion') == original, f'{sid}: altered acceptance in coverage')
            require(bool(coverage.get('successorIds')), f'{sid}: uncovered original criterion')
            require(all(x in byid and x in m.get('successorIds', []) for x in coverage.get('successorIds', [])), f'{sid}: criterion successor not mapped')
        require(all(d in native_ids for d in m.get('nativeStructuredPrerequisites', [])), f'{sid}: dangling frozen native prerequisite')
        expected_text_only = [d for d in m.get('textualPrerequisites', []) if d not in m.get('repositoryStructuredPrerequisites', [])]
        require(m.get('textualOnlyPrerequisites') == expected_text_only, f'{sid}: textual-only dependency distinction lost')
    critical = plan.get('criticalPath', [])
    scopewaves = [w for w in waves if w.get('releaseHorizon') == '0.1']
    require([c.get('wave') for c in critical] == [w['id'] for w in scopewaves], 'Critical path does not cover the narrow release waves')
    for c in critical:
        w = bywave.get(c.get('wave'))
        if w:
            require(c.get('entry') == w['taskIds'][0] and c.get('exit') == w['taskIds'][-1], 'Critical path endpoints differ from wave outcome gates')
    require(plan.get('coverageReview', {}).get('taskCount') == len(tasks), 'Recorded task count is stale')
    require(plan.get('coverageReview', {}).get('waveCount') == len(waves), 'Recorded wave count is stale')
    if check_lineage:
        for record in plan.get('lineageFiles', []):
            path = root / record['path']
            require(path.is_file() and digest(path.read_bytes()) == record['sha256'], f'Frozen lineage bytes changed: {record["path"]}')
        old_path = root / 'docs/lineage/2026-09-07/project-plan.json'
        if old_path.is_file():
            old = json.loads(old_path.read_text())
            originals = {t['id']: t for t in old['tasks']}
            for m in mappings:
                original = originals.get(m.get('sourceKey'))
                if original:
                    require(m.get('originalAcceptanceCriteria') == original['acceptanceCriteria'], f'{m["sourceId"]}: frozen acceptance changed')
                    require(m.get('repositoryStructuredPrerequisites') == ['renewal-engine:' + x for x in original['dependencies']], f'{m["sourceId"]}: frozen repository graph changed')
                brief = root / m['lineageBrief']
                if not brief.is_file():
                    errors.append(f'{m["sourceId"]}: missing frozen brief')
                    continue
                data = brief.read_bytes()
                require(digest(data) == m['briefSha256'], f'{m["sourceId"]}: brief bytes changed')
                text = data.decode()
                for field, heading in [('platformId', 'Task ID'), ('savedRevision', 'Saved revision'), ('publicationContentHash', 'Publication content hash'), ('snapshotStatus', 'Status')]:
                    match = re.search(r'### ' + heading + r'\n\n```text\n(.*?)\n```', text, re.S)
                    require(match is not None and str(m.get(field)) == match.group(1), f'{m["sourceId"]}: frozen {field} changed')
                match = re.search(r'### Prerequisites\n(.*?)### Required model', text, re.S)
                if match:
                    deps = re.findall(r'```text\n(tsk_[^\n]+)', match.group(1))
                    require(m.get('nativeStructuredPrerequisites') == deps, f'{m["sourceId"]}: frozen native graph changed')
    return errors


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def render(plan):
    tasks = plan['tasks']
    byid = {t['id']: t for t in tasks}
    stamp = digest(json_text(plan).encode())
    preamble = f'Generated from `project-plan.json` by `python3 tools/plan.py generate`. Do not edit this view. Canonical SHA-256: `{stamp}`.\n'
    counts = {h: sum(t['targetRelease'] == h for t in tasks) for h in RELEASE_ORDER}
    roadmap = ['# Renewal Engine roadmap', '', preamble, plan['stage'], '',
               f'{len(tasks)} outcome tasks in {len(plan["waves"])} waves. ' + '; '.join(f'{k}: {v}' for k, v in counts.items()) + '.', '',
               'The 12 historical contracts remain immutable in [lineage](docs/lineage/2026-09-07). Their original graph is separate from the new narrow 0.1 path. Later outcomes require accepted scope and evidence; exploratory options are not promised delivery.', '',
               '## Narrow 0.1 path', '', plan['criticalPathNote'], '',
               ' → '.join(c['wave'] for c in plan['criticalPath']), '',
               '## Release access and unresolved decisions', '', plan['release']['accessInstructions'], '']
    roadmap += [f'- **{key} · {value["status"]}:** {value["proposal"]}' for key, value in plan['decisions'].items()]
    roadmap += ['', '## Outcome waves', '']
    for wave in plan['waves']:
        roadmap += [f'### {wave["id"]} — {wave["title"]}', '',
                    f'**Horizon:** {wave["releaseHorizon"]}. **Basis:** {wave["classification"]}.', '',
                    f'**Outcome:** {wave["outcome"]}', '',
                    '**Entry dependencies:** ' + (', '.join(wave['entryDependencies']) or 'None; exact cut still requires owner decisions.'), '',
                    '**Assigned outcomes:**', '']
        roadmap += [f'- `{tid}` — {byid[tid]["title"]} ({byid[tid]["status"]})' for tid in wave['taskIds']]
        roadmap += ['', '**Exit evidence:** ' + ' '.join(wave['exitEvidence']), '']
    roadmap += ['## Publication boundary', '', plan['publication']['gate'], '',
                'The generated [publication export](docs/publication/tanduna-plan-export.json) is a local review artifact, not a supported API payload or proof of native publication. See the [source mapping](docs/planning/source-mapping.md).', '']
    taskdoc = ['# Renewal Engine task outcomes', '', preamble,
               'Statuses are evidence levels, not a claim that planning proves implementation. Change `project-plan.json`, retain evidence, then regenerate all views. Frozen historical contracts are preserved separately.', '',
               ' | '.join(['ID', 'Title', 'Release', 'Status']), ' | '.join(['---'] * 4)]
    taskdoc += [' | '.join(cell(t[k]) for k in ('id', 'title', 'targetRelease', 'status')) for t in tasks]
    for t in tasks:
        taskdoc += ['', f'## {t["id"]} — {t["title"]}', '', t['outcome'], '',
                    f'Wave: {t["wave"]}. Area: {t["featureArea"]}. Target: {t["targetRelease"]}. Basis: {t["basis"]}. Status: **{t["status"]}**.', '',
                    'Prerequisites: ' + (', '.join(t['prerequisiteIds']) or 'None.'), '',
                    'Acceptance:', ''] + ['- ' + x for x in t['acceptanceCriteria']]
        taskdoc += ['', 'Sources: ' + ', '.join(t['sourceRefs']) + '. Decisions: ' + (', '.join(t['decisionRefs']) or 'No additional decision is inferred.') , '',
                    'Risk: ' + t['riskEvidenceNeeds']['risk'], '',
                    'Evidence needed: ' + t['riskEvidenceNeeds']['requiredEvidence'], '',
                    t['riskEvidenceNeeds']['humanEvidence'], '',
                    'Retained evidence: ' + (json.dumps(t['evidence'], ensure_ascii=False) if t['evidence'] else 'None recorded for this proposed task.')]
    mapping = ['# Preserved source-to-successor mapping', '', preamble,
               'The frozen repository files and downloaded native briefs are retained byte-for-byte. Revision 3 is a reviewed textual plan; it establishes no executed product. Fable fields remain historical bytes and are overridden for current execution by the owner’s Astra-only policy.', '',
               'Original base `8af461149e2c4b6b3b17d54a10b3559168f8b32f` and briefing HEAD `f434e00913f5df6c78721300ca68625401d87a41` identify different states. No predecessor revision is invented when the source does not state one.', '']
    for m in plan['sourceMappings']:
        mapping += [f'## {m["sourceId"]}', '',
                    f'Platform: [{m["platformId"]}]({m["platformUrl"]}/brief), saved revision {m["savedRevision"]}, status {m["snapshotStatus"]}.', '',
                    f'Frozen publication hash: `{m["publicationContentHash"]}`. Brief SHA-256: `{m["briefSha256"]}`.', '',
                    f'Treatment: **{m["treatment"]}**. {m["reason"]}', '',
                    'Repository structured prerequisites: ' + (', '.join(m['repositoryStructuredPrerequisites']) or 'None recorded.'), '',
                    'Native structured prerequisites: ' + (', '.join(m['nativeStructuredPrerequisites']) or 'Not configured.'), '',
                    'Textual prerequisites: ' + (', '.join(m['textualPrerequisites']) or 'None recorded.'), '',
                    'Additional textual-only prerequisites: ' + (', '.join(m['textualOnlyPrerequisites']) or 'None recorded.'), '',
                    'Successors: ' + ', '.join(m['successorIds']), '', 'Original acceptance and successor coverage:', '']
        mapping += [f'- **Original:** {c["originalCriterion"]} **Mapped outcomes:** {", ".join(c["successorIds"])}. **Historical acceptance state:** {c["acceptanceState"]}.' for c in m['criterionCoverage']]
        mapping += ['']
    contracts = {'schemaVersion': 2, 'generatedFrom': 'project-plan.json', 'canonicalSha256': stamp,
                 'meaning': 'Generated new outcome contracts and mappings; frozen original contracts remain in lineage.',
                 'sourceMappings': plan['sourceMappings'], 'tasks': tasks}
    export = {'schemaVersion': 1, 'artifactKind': 'publication-review-export',
              'notAnApiPayload': True, 'generatedFrom': 'project-plan.json', 'canonicalSha256': stamp,
              'project': {'slug': plan['slug'], 'name': plan['name'], 'id': plan['publication']['projectId']},
              'publication': plan['publication'], 'release': plan['release'], 'decisions': plan['decisions'],
              'counts': {'tasks': len(tasks), 'waves': len(plan['waves']), 'releaseHorizons': counts},
              'criticalPath': plan['criticalPath'], 'waves': plan['waves'], 'tasks': tasks,
              'sourceMappings': plan['sourceMappings'], 'lineageFiles': plan['lineageFiles'],
              'limitations': plan['coverageReview']['limits']}
    return {'ROADMAP.md': '\n'.join(roadmap), 'TASKS.md': '\n'.join(taskdoc) + '\n',
            'task-contracts.json': json_text(contracts),
            'docs/publication/tanduna-plan-export.json': json_text(export),
            'docs/planning/source-mapping.md': '\n'.join(mapping)}


def self_test(plan):
    """Mutation checks exercise meaningful ledger failure modes, not task constants."""
    mutations = [
        ('duplicate ID', lambda p: p['tasks'][1].update(id=p['tasks'][0]['id'])),
        ('duplicate outcome', lambda p: p['tasks'][1].update(outcome=p['tasks'][0]['outcome'])),
        ('missing acceptance', lambda p: p['tasks'][0].update(acceptanceCriteria=[])),
        ('dangling prerequisite', lambda p: p['tasks'][1].update(prerequisiteIds=['renewal-engine:N99-99'])),
        ('cycle', lambda p: p['tasks'][0].update(prerequisiteIds=[p['tasks'][1]['id']])),
        ('orphan task', lambda p: p['waves'][0]['taskIds'].pop()),
        ('missing original mapping', lambda p: p['sourceMappings'].pop()),
        ('lost original criterion', lambda p: p['sourceMappings'][0]['criterionCoverage'].pop()),
        ('changed frozen acceptance', lambda p: p['sourceMappings'][0]['originalAcceptanceCriteria'].__setitem__(0, 'Weakened requirement.')),
        ('changed native graph', lambda p: p['sourceMappings'][1].update(nativeStructuredPrerequisites=[])),
        ('lost textual distinction', lambda p: p['sourceMappings'][1].update(textualOnlyPrerequisites=p['sourceMappings'][1]['textualPrerequisites'])),
        ('stale coverage', lambda p: p['tasks'][1]['prerequisiteOutcomeCoverage'][0].update(neededOutcome='Wrong prerequisite.')),
        ('later dependency in 0.1', lambda p: p['tasks'][1].update(prerequisiteIds=[p['tasks'][-1]['id']])),
        ('exploratory promise', lambda p: p['tasks'][0].update(basis='exploratory')),
        ('unsupported completion', lambda p: p['tasks'][0].update(status='RELEASE VERIFIED')),
        ('missing wave entry', lambda p: p['waves'][1].update(entryDependencies=[])),
        ('wrong critical path', lambda p: p['criticalPath'].pop()),
        ('stale count', lambda p: p['coverageReview'].update(taskCount=300)),
        ('changed frozen hash', lambda p: p['sourceMappings'][0].update(publicationContentHash='0' * 64)),
        ('changed lineage digest', lambda p: p['lineageFiles'][0].update(sha256='0' * 64)),
    ]
    missed = []
    for name, mutate in mutations:
        damaged = copy.deepcopy(plan)
        mutate(damaged)
        if not validate(damaged):
            missed.append(name)
    if missed:
        raise ValueError('Validation missed mutations: ' + ', '.join(missed))
    print(f'PASS: {len(mutations)} malformed-plan mutations rejected; original ledger remains unchanged.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'generate', 'check', 'self-test'])
    args = parser.parse_args()
    plan = json.loads((ROOT / 'project-plan.json').read_text())
    problems = validate(plan)
    if problems:
        print('\n'.join('ERROR: ' + e for e in problems), file=sys.stderr)
        return 1
    if args.command == 'self-test':
        self_test(plan)
        return 0
    if args.command in {'generate', 'check'}:
        for path, content in render(plan).items():
            target = ROOT / path
            if args.command == 'generate':
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            elif not target.is_file() or target.read_text() != content:
                problems.append(f'Generated view differs from canonical state: {path}')
        if problems:
            print('\n'.join(problems), file=sys.stderr)
            return 1
    print(f'PASS: {len(plan["tasks"])} tasks, {len(plan["waves"])} waves, 12 frozen source mappings; {args.command}.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
