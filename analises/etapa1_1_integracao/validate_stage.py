"""Replay preserved real documents and run all suites without touching history."""
from pathlib import Path
import ast
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
OLD = ROOT / 'analises/etapa1_leitura_geometria'
for part in ('reinforcement_checks','beam_model','beam_mapping','extrator_lst'):
    sys.path.insert(0,str(ROOT/'tools'/part))
from floor_review import review_floor


def write(name, data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def historical_hashes():
    roots = [OLD, ROOT/'analises/silva_jardim_tipo', ROOT.parent/'concretopy/concretopy']
    hashes={str(p):sha(p) for root in roots if root.exists() for p in root.rglob('*') if p.is_file() and
            '__pycache__' not in p.parts and p.suffix.lower() in ('.py','.json','.md','.pdf','.png','.txt')}
    source=Path('C:/Users/João Severgnini/Documents/arquivos/051-SJ-EST-EX-010-PLB-TP-R01.pdf')
    if source.is_file():hashes[str(source)]=sha(source)
    return hashes


def call_audit():
    rows=[]
    for root in (ROOT/'tools', ROOT/'analises'):
        for path in root.rglob('*.py'):
            if OUT in path.parents or path.name.startswith('test_'):continue
            try:tree=ast.parse(path.read_text(encoding='utf-8-sig'))
            except (SyntaxError,UnicodeError):continue
            guarded=any(isinstance(n,ast.ImportFrom) and n.module in ('input_preflight','floor_review') for n in ast.walk(tree))
            calls=[]
            for n in ast.walk(tree):
                if isinstance(n,ast.Call):
                    name=n.func.id if isinstance(n.func,ast.Name) else n.func.attr if isinstance(n.func,ast.Attribute) else ''
                    if name.startswith(('check_','review_')) or name in ('map_beam','evaluate_configuration'):
                        calls.append(dict(line=n.lineno,function=name))
            if calls:rows.append(dict(file=path.relative_to(ROOT).as_posix(),imports_guard=guarded,
                classification='GUARD_IMPORT_REQUIRES_PATH_REVIEW' if guarded else 'LEGACY_OR_LOW_LEVEL_NO_PREFLIGHT_IMPORT',calls=calls))
    write('legacy_callers_audit.json',dict(method='AST inventory; guard import alone is not proof of protected execution',files=rows))


def replay():
    cases=[];comparisons={}
    form_source=Path('C:/Users/João Severgnini/Documents/arquivos/051-SJ-EST-EX-010-PLB-TP-R01.pdf')
    forms={}
    if form_source.is_file():
        from extract_real_form import build
        forms=build()
    baseline=json.loads((OLD/'comparativo_real.json').read_text(encoding='utf-8-sig'))
    for name in ('V610','V611','V623','V626'):
        doc=json.loads((OLD/(name+'_document_stage1.json')).read_text(encoding='utf-8-sig'))
        case=dict(beam_id=name,document=doc,review_interval_m=baseline[name]['input_validation'][0]['interval_m'])
        if name in forms:
            doc['physical_extension']['coordinate_system']=forms[name]['coordinate_system']
            case['form']=forms[name]
            from section_positions import fill_positions
            tqs=json.loads((OLD/(name+'_tqs_stage1.json')).read_text(encoding='utf-8-sig'))
            raw=json.loads((ROOT/'analises/silva_jardim_tipo'/(name+'_tqs_raw.json')).read_text(encoding='utf-8-sig'))
            try:
                positioned,_=fill_positions(tqs,raw)
                case['positioned_tqs']=positioned
                supports={s['support_id']:s for s in forms[name]['support_faces']}
                registrations={}
                for s in positioned['beam']['spans']:
                    left,right=[supports.get(k) for k in s['support_ids']]
                    if left is None or right is None:continue
                    from input_evidence import fact
                    start,end=left['axis_m'],right['axis_m']
                    distance=end['value']-start['value']
                    if distance<=0:continue
                    from map_beam import selected
                    offsets=[];operands=[]
                    span_index=next(i for i,q in enumerate(tqs['beam']['spans']) if q['id']==s['id'])
                    length,lp=selected(tqs,'/beam/spans/'+str(span_index)+'/geometry/length',s['geometry']['length'],'VGESFS.LST')
                    for support_id in s['support_ids']:
                        si,record=next((i,q) for i,q in enumerate(tqs['beam']['supports']) if q['id']==support_id)
                        offset,op=selected(tqs,'/beam/supports/'+str(si)+'/eccentricity',record.get('eccentricity'),'RELDTFPS.LST')
                        offsets.append(offset);operands.append(op)
                    tqs_axis_distance=float(length+sum(offsets))
                    if abs(tqs_axis_distance-distance)>1e-8:
                        case.setdefault('axis_distance_conflicts',[]).append(dict(span_id=s['id'],form_distance_m=distance,tqs_distance_m=tqs_axis_distance))
                        continue
                    registrations[str(s['id'])]=dict(span_id=s['id'],coordinate_system=forms[name]['coordinate_system'],
                        anchors=[dict(local_m=fact(0,state='DOCUMENTED_CONFIRMED',unit='m',provenance=[dict(reference='section_positions: origin at left physical support axis')]),common_m=start),
                                 dict(local_m=fact(tqs_axis_distance,state='DOCUMENTED_CONFIRMED',unit='m',provenance=[dict(reference='VGESFS length + both RELDTFPS DEPEV; checked independently against printed form support axes',operands=[lp]+operands)]),common_m=end)])
                case['registrations']=registrations
            except (ValueError,KeyError,TypeError) as error:
                case['positioning_pending']=str(error)
        cases.append(case)
    sources={}
    if forms:
        details=ROOT/'analises/silva_jardim_tipo/drawing_inventory.json'
        tqs=ROOT/'analises/silva_jardim_tipo/operational_tqs.json'
        sources=dict(form=dict(path=str(form_source),sha256=sha(form_source)),
            detailing=dict(path=str(details),sha256=sha(details)),tqs=dict(path=str(tqs),sha256=sha(tqs)))
    spec=dict(floor='TIPO',beams=cases,sources=sources,beam_inventory_complete=False)
    write('real_replay_manifest.json',spec)
    sys.path.insert(0,str(ROOT.parent/'concretopy'))
    import concretopy as api
    result=review_floor(spec,api=api)
    write('real_replay.json',result)
    for beam in result['beams']:
        name=beam['beam_id'];m=beam['model']
        old=json.loads((OLD/(name+'_model_stage1.json')).read_text(encoding='utf-8-sig'))
        tqs=json.loads((OLD/(name+'_tqs_stage1.json')).read_text(encoding='utf-8-sig'))
        comparisons[name]=dict(fixture_kind='REAL_FORM_REVIEW_WITH_PRESERVED_DETAILING_AND_TQS' if forms else 'REAL_PRESERVED_DOCUMENTARY_EXTRACTION_NO_NEW_FORM_PROOF',
            stage1_readiness={p['control']:p['readiness'] for p in baseline[name]['input_validation']},
            stage1_1_readiness={p['control']:p['input_validation']['readiness'] for p in beam['controls']},
            occurrences_before=len(old['physical_geometry']['occurrences']),occurrences_after=len(m['physical_geometry']['occurrences']),
            documentary_reconciliation_preserved=old['documentary_reconciliation']==m['documentary_reconciliation'],
            layer_states_before=[b['layers']['state'] for b in old['physical_geometry']['occurrences']],
            layer_states_after=[b['layers']['state'] for b in m['physical_geometry']['occurrences']],
            physical_regions_certified=False,local_constant_regions_documented=bool(forms),resistant_recalculation=False,numeric_change=None,
            certified_constant_segments=[dict(id=s['id'],start=s['x_start_m']['value'],end=s['x_end_m']['value'],height=s['geometry']['height_cm']['value']) for s in m['physical_geometry']['segments'] if s['geometry_type']=='CONSTANT' and s['x_start_m']['state']=='DOCUMENTED_CONFIRMED' and s['x_end_m']['state']=='DOCUMENTED_CONFIRMED'],
            registered_force_spans=list(beam['registered_spans']),positioning_pending=next(c for c in cases if c['beam_id']==name).get('positioning_pending'),
            form_state='EXAMINED_RELEVANT_REGIONS' if forms else 'SOURCE_UNAVAILABLE_IN_SESSION_NOT_EXAMINED',
            tqs_preserved_sha256=sha(OLD/(name+'_tqs_stage1.json')),
            tqs_documentary_cantilevers=[s.get('original_span_tokens') for s in tqs['beam']['spans'] if any(str(t).endswith('B') for t in s.get('original_span_tokens',[]))],
            pending=[dict(control=e['control'],missing=e['input_validation']['pending']) for e in beam['controls']])
    write('comparativo_real.json',comparisons)
    call_audit()


def tests():
    suites=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
    for name in ('beam_model','extrator_lst','beam_mapping','reinforcement_checks'):
        command=[sys.executable,'-m','unittest','discover','-s','tools/'+name,'-p','test_*.py','-q']
        run=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
        output=run.stdout+run.stderr;match=re.search(r'Ran (\d+) tests? in ([\d.]+)s',output)
        suites.append(dict(suite=name,command=command,tests=int(match[1]) if match else None,exit_code=run.returncode,output=output))
        print(name,suites[-1]['tests'],run.returncode,flush=True)
    result=dict(suites=suites,total=sum(s['tests'] or 0 for s in suites),all_passed=all(s['exit_code']==0 for s in suites),interpreter=sys.version)
    write('test_results.json',result)
    return result['all_passed']


if __name__=='__main__':
    before=historical_hashes()
    replay()
    passed=tests()
    after=historical_hashes()
    write('preservation.json',dict(unchanged=before==after,files=len(before),hashes=before))
    if before!=after or not passed:raise SystemExit(1)
