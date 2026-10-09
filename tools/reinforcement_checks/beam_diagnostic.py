"""Consolidate already computed beam checks; no resistant calculations/imports."""
from copy import deepcopy
import hashlib
import json
import math

DISCIPLINES = ('positive_flexure','negative_flexure','anchorage','shear','suspension')
STATES = ('PASS','FAIL','INCONCLUSIVE','REQUIRES_ENGINEERING_REVIEW','NOT_APPLICABLE')
CATEGORIES = {
 'flexural_capacity':'INSUFFICIENT_REINFORCEMENT_CAPACITY',
 'reinforcement_area':'INSUFFICIENT_REINFORCEMENT_AREA',
 'anchorage_length':'INSUFFICIENT_ANCHORAGE',
 'vertical_bend_geometry':'INSUFFICIENT_ANCHORAGE',
 'al_plus_lb':'INSUFFICIENT_DEVELOPMENT_LENGTH',
 'al_plus_10phi':'INSUFFICIENT_DEVELOPMENT_LENGTH',
 'condition_A':'INSUFFICIENT_DEVELOPMENT_LENGTH',
 'condition_B':'INSUFFICIENT_DEVELOPMENT_LENGTH',
 'shear_reinforcement':'INSUFFICIENT_STIRRUP_RATE',
 'maximum_code_spacing':'EXCESSIVE_STIRRUP_SPACING',
 'reaction':'MISSING_REACTION',
 'geometric_position':'MISSING_GEOMETRY',
 'drawing_coverage':'MISSING_DOCUMENTARY_EVIDENCE',
}


def aggregate(states):
    states = list(states)
    for state in ('FAIL','INCONCLUSIVE','REQUIRES_ENGINEERING_REVIEW'):
        if state in states:return state
    return 'PASS' if 'PASS' in states else 'NOT_APPLICABLE' if states else 'INCONCLUSIVE'


EXECUTION_STATES=('NOT_EXECUTED','PARTIALLY_EXECUTED','EXECUTED_INCONCLUSIVE','EXECUTED_COMPLETE')


def module_execution(module):
    if module.get('applicability')=='NOT_APPLICABLE' and module.get('applicability_evidence'):
        return 'EXECUTED_COMPLETE'
    if module.get('execution_state')=='NOT_EXECUTED':
        if module.get('checks'):raise ValueError('unexecuted_module_has_results')
        return 'NOT_EXECUTED'
    if module.get('complete') is not True:return 'PARTIALLY_EXECUTED'
    if not module.get('checks') or any(c['status']=='INCONCLUSIVE' and c.get('governing',True) for c in module['checks']):
        return 'EXECUTED_INCONCLUSIVE'
    return 'EXECUTED_COMPLETE'


def aggregate_execution(states):
    states=list(states)
    if not states or all(s=='NOT_EXECUTED' for s in states):return 'NOT_EXECUTED'
    if any(s in ('NOT_EXECUTED','PARTIALLY_EXECUTED') for s in states):return 'PARTIALLY_EXECUTED'
    return 'EXECUTED_INCONCLUSIVE' if 'EXECUTED_INCONCLUSIVE' in states else 'EXECUTED_COMPLETE'


def attach_execution(result):
    """Additive versioned view; technical statuses and original IDs are preserved."""
    r=deepcopy(result);states={d:[] for d in DISCIPLINES}
    for m in r['source_modules']:states[m['discipline']].append(module_execution(m))
    r['discipline_execution']={d:aggregate_execution(states[d]) for d in DISCIPLINES}
    r['execution_state']=aggregate_execution(r['discipline_execution'].values())
    for d,items in r['module_availability'].items():
        for i,item in enumerate(items):item['execution_state']=states[d][i] if states[d] else 'NOT_EXECUTED'
    for collection in ('checks','occurrences'):
        for c in r[collection]:
            c['execution_state']='NOT_EXECUTED' if c['check_type']=='module_availability' else 'EXECUTED_INCONCLUSIVE' if c['status']=='INCONCLUSIVE' else 'EXECUTED_COMPLETE'
    r['schema_version']='1.1'
    return r


def occurrence_groups(result):
    """Presentation grouping only; retain every original occurrence in JSON."""
    groups={}
    for o in result['occurrences']:
        if o.get('governing') is False:continue
        marks=tuple(sorted(o['drawing_reinforcement_ids']))
        reference=o.get('physical_reference') or {}
        support=reference.get('support_id')
        if marks:key=('REINFORCEMENT',marks,support)
        elif support:key=('SUPPORT',support)
        elif o.get('physical_interval') is not None:key=('REGION',o.get('span_id'),tuple(o['physical_interval']))
        else:key=('DISCIPLINE',o['discipline'])
        group=groups.setdefault(key,{'label':str(key),'occurrence_ids':[],'statuses':[]})
        group['occurrence_ids'].append(o['occurrence_id']);group['statuses'].append(o['status'])
    return [dict(g,status=aggregate(g['statuses'])) for k,g in sorted(groups.items(),key=lambda p:str(p[0]))]


def _id(parts):
    return hashlib.sha256(json.dumps(parts,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:24]


def consolidate(context, modules, *, input_validation=None):
    """Strict normalized contract. Missing disciplines are required/pending.

    Module envelope: discipline, beam_id, floor, source, version, coordinate_system,
    complete, checks. Explicit NOT_APPLICABLE additionally requires evidence.
    Check IDs are stable logical IDs within a source/discpline, never list indexes.
    No diagnosis automatically selects a correction.
    """
    ctx=deepcopy(context)
    if input_validation is not None:
        ctx['input_validation'] = deepcopy(input_validation)
    if not ctx.get('beam_id') or not ctx.get('floor') or not ctx.get('coordinate_system'):
        raise ValueError('beam_floor_or_coordinate_identity_missing')
    checks=[];availability={};seen=set();snapshots=[]
    for module in modules:
        m=deepcopy(module);discipline=m['discipline']
        if discipline not in DISCIPLINES:raise ValueError('unknown_discipline')
        if m.get('beam_id')!=ctx['beam_id'] or m.get('floor')!=ctx['floor']:
            raise ValueError('beam_or_floor_mismatch')
        if m.get('coordinate_system')!=ctx['coordinate_system']:
            raise ValueError('coordinate_system_mismatch')
        if not m.get('source') or not m.get('version'):raise ValueError('module_source_or_version_missing')
        snapshots.append(m)
        availability.setdefault(discipline,[]).append({k:m.get(k) for k in ('source','version','complete','applicability','applicability_evidence')})
        items=m.get('checks',[])
        if m.get('applicability')=='NOT_APPLICABLE':
            if not m.get('applicability_evidence'):raise ValueError('inapplicability_unproven')
            if items:raise ValueError('inapplicable_module_has_checks')
            items=[dict(check_id='applicability',check_type='module_applicability',status='NOT_APPLICABLE',
                        reason='inapplicability_proven',evidence=m['applicability_evidence'])]
        elif m.get('complete') is not True or not items:
            items=list(items)+[dict(check_id='module_coverage',check_type='module_coverage',status='INCONCLUSIVE',
                reason='module_scope_incomplete',missing_information=m.get('missing_information',['applicable checks not completely documented']))]
        for item in items:
            c=deepcopy(item)
            if c.get('status') not in STATES or not c.get('check_id') or not c.get('check_type'):
                raise ValueError('invalid_normalized_check')
            if c.get('beam_id',ctx['beam_id'])!=ctx['beam_id']:raise ValueError('check_beam_mismatch')
            if c.get('coordinate_system',ctx['coordinate_system'])!=ctx['coordinate_system']:
                raise ValueError('check_coordinate_mismatch')
            source_identity={k:m['source'][k] for k in ('path','pointer') if k in m['source']} if isinstance(m['source'],dict) else m['source']
            uid=_id([ctx['floor'],ctx['beam_id'],discipline,source_identity,c['check_id']])
            if uid in seen:raise ValueError('duplicate_check_identity')
            seen.add(uid)
            c.update(id=uid,beam_id=ctx['beam_id'],discipline=discipline,
                     calculation_source=c.get('calculation_source') or {'module':m['source'],'version':m['version']},
                     coordinate_system=ctx['coordinate_system'])
            for key in ('span_id','physical_interval','required_value','provided_value','units','demand_source','drawing_source'):
                c.setdefault(key,None)
            for key in ('drawing_reinforcement_ids','missing_information'):
                c.setdefault(key,[])
            c.setdefault('reason',None);c.setdefault('evidence',{})
            if c['status']=='NOT_APPLICABLE' and not c.get('evidence'):
                raise ValueError('check_inapplicability_unproven')
            if c.get('governing') is False and not (c['check_type']=='straight_anchorage_geometry' and c.get('role')=='MODE_SELECTION_OBSERVATION' and c['evidence'].get('anchorage_mode')=='VERTICAL_BEND'):
                raise ValueError('non_governing_failure_without_mode_evidence')
            interval=c['physical_interval']
            if interval is not None:
                if not isinstance(interval,list) or len(interval)!=2 or any(type(x) not in (float,int) or not math.isfinite(x) for x in interval) or interval[0]>interval[1]:
                    raise ValueError('invalid_physical_interval')
            elif c['status'] not in ('NOT_APPLICABLE',) and 'physical_location_not_documented' not in c['missing_information']:
                c['missing_information'].append('physical_location_not_documented')
            checks.append(c)
    for discipline in DISCIPLINES:
        if discipline not in availability:
            availability[discipline]=[{'availability':'NOT_EXECUTED'}]
            checks.append(dict(id=_id([ctx['floor'],ctx['beam_id'],discipline,'missing']),beam_id=ctx['beam_id'],
                discipline=discipline,check_type='module_availability',check_id='missing',status='INCONCLUSIVE',
                reason='module_not_executed',missing_information=['module results unavailable'],
                span_id=None,physical_interval=None,drawing_reinforcement_ids=[],required_value=None,provided_value=None,
                units=None,demand_source=None,drawing_source=None,calculation_source=None,evidence={}))
    checks.sort(key=lambda c:c['id'])
    occurrences=[]
    for c in checks:
        if c['status'] not in ('FAIL','INCONCLUSIVE','REQUIRES_ENGINEERING_REVIEW'):continue
        if c.get('category'): category=c['category']
        elif c['status']=='REQUIRES_ENGINEERING_REVIEW': category='ENGINEERING_REVIEW_REQUIRED'
        elif c['status']=='FAIL': category=CATEGORIES.get(c['check_type'],'STRUCTURAL_OR_DETAILING_NONCONFORMITY')
        elif c['check_type'] in ('reaction','total_support_reaction','reaction_nature'): category='MISSING_REACTION'
        elif c['check_type'] in ('support_geometry','geometric_position','column_interference_spacing'): category='MISSING_GEOMETRY'
        elif c['discipline']=='suspension': category='UNVERIFIED_SUSPENSION'
        else: category='MISSING_DOCUMENTARY_EVIDENCE'
        occurrence=deepcopy(c);occurrence.update(occurrence_id='occ-'+c['id'],category=category,related_checks=[])
        # Only explicitly comparable scalar quantities, never convert units here.
        required,provided=c['required_value'],c['provided_value']
        occurrence['provided_minus_required']=(provided-required if type(required) in (int,float) and type(provided) in (int,float) and isinstance(c.get('units'),str) and c.get('comparison') in ('provided_ge_required','provided_le_required') else None)
        occurrences.append(occurrence)
    relations=[]
    for i,a in enumerate(occurrences):
        for b in occurrences[i+1:]:
            shared=sorted(set(a['drawing_reinforcement_ids'])&set(b['drawing_reinforcement_ids']))
            overlap=False
            if a['physical_interval'] and b['physical_interval'] and a['span_id']==b['span_id']:
                overlap=max(a['physical_interval'][0],b['physical_interval'][0])<min(a['physical_interval'][1],b['physical_interval'][1])
            if shared or overlap:
                relations.append({'occurrences':[a['occurrence_id'],b['occurrence_id']],
                    'shared_reinforcement':shared,'physical_overlap':overlap,'single_correction_proven':False})
                a['related_checks'].append(b['id']);b['related_checks'].append(a['id'])
    summary={d:aggregate(c['status'] for c in checks if c['discipline']==d and c.get('governing',True)) for d in DISCIPLINES}
    state=aggregate(summary.values())
    return dict(schema_version='1.0',model_type='BEAM_STRUCTURAL_DIAGNOSTIC',context=ctx,
        module_availability=availability,source_modules=snapshots,checks=checks,occurrences=occurrences,
        proven_nonconformities=[o['occurrence_id'] for o in occurrences if o['status']=='FAIL' and o.get('governing',True)],
        pending_occurrences=[o['occurrence_id'] for o in occurrences if o['status']=='INCONCLUSIVE'],
        engineering_review_occurrences=[o['occurrence_id'] for o in occurrences if o['status']=='REQUIRES_ENGINEERING_REVIEW'],
        relations=relations,discipline_status=summary,overall_status=state,
        beam_checks_approval=False if state=='FAIL' else True if state in ('PASS','NOT_APPLICABLE') else None,
        structural_safety_declaration=None,selected_solution=None,detailing_optimization=None)


def markdown(result):
    """Grouped readable report; pairwise evidence stays solely in the JSON."""
    ctx=result['context']
    def cell(v):return str(v).replace('|','/').replace('\n',' ') if v is not None else 'não documentado'
    lines=[f'# Diagnóstico consolidado — {ctx["beam_id"]}', '',f'Pavimento: {ctx["floor"]}.',
        '',f'Estado técnico: **{result["overall_status"]}**. Execução: **{result.get("execution_state","estado legado não separado")}**.',
        '', '| Disciplina | Execução | Resultado técnico |','|---|---|---|']
    lines += [f'| {d} | {result.get("discipline_execution",{}).get(d,"legado")} | {v} |' for d,v in result['discipline_status'].items()]
    lines += ['', 'Geometria, materiais, fontes e versões constam no contexto do JSON associado.', '']
    lookup={o['occurrence_id']:o for o in result['occurrences']}
    for group in occurrence_groups(result):
        lines += ['## '+cell(group['label']), '', '| Ocorrência | Controle | Estado | Vão / intervalo | Necessário | Fornecido | Unidade | Motivo / pendência |','|---|---|---|---|---|---|---|---|']
        for oid in group['occurrence_ids']:
            o=lookup[oid]
            lines.append('| '+' | '.join(map(cell,[oid,o['check_type'],o['status'],[o['span_id'],o['physical_interval']],o['required_value'],o['provided_value'],o['units'],[o['reason'],o['missing_information']]]))+' |')
        lines.append('')
    observations=[o for o in result['occurrences'] if o.get('governing') is False]
    lines += ['## Auditoria dos modos de ancoragem', '']
    lines += [f'{cell(o["drawing_reinforcement_ids"])}: {o["check_type"]} = {o["status"]} original; observação não governante porque a peça é verificada em VERTICAL_BEND. A dobra e a resistência curva permanecem controles independentes.' for o in observations] or ['Nenhuma observação de modo não governante.']
    lines += ['', f'{len(result["relations"])} relações individuais preservadas no JSON, sem expandir todas as combinações neste relatório.', '', 'Nenhuma correção proposta ou selecionada; selected_solution=null e detailing_optimization=null. Não é declaração de segurança global da estrutura.']
    return '\n'.join(lines)+'\n'
