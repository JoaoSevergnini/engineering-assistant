"""New diagnostic revision: existing-configuration reverification only, no search/PDF IO."""
from copy import deepcopy
from decimal import Decimal
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'tools/reinforcement_checks'),str(ROOT/'analises/pranchas'),str(ROOT.parent/'concretopy')]
import concretopy as api
from tools.beam_mapping.termination_geometry import interpret_endpoints
from validar_diagnostico_vigas import make,BASE
from validar_v536_v565_correcao_apoio import load_detail_case,read
from beam_diagnostic import consolidate,attach_execution,markdown,occurrence_groups
import beam_diagnostic_adapters as adapters
from support_geometry import SupportGeometry
from support_anchorage import check_support
from support_correction import check_longitudinal
from positive_flexure import check_positive_flexure
from bar_scaling import check_bar_scaling,SUPPORTED_SCOPE
from tqs_shear import shear_from_tqs
from detailing_change_contracts import detailing_preferences,proposal_template


def source(path,pointer=''):
    p=BASE/path
    return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pointer':pointer}


def reverify_v536():
    mapping=deepcopy(read('V536_beam_mapping.json'));model=deepcopy(read('V536_V565_beam_model.json'))
    n2=next(b for b in mapping['reinforcement'] if b['mark']=='N2')
    support=mapping['supports']['left']
    face=float(Decimal(str(support['axis_x']))-Decimal(str(support['width']))/2)
    interpretation=interpret_endpoints({
        'LEFT':{'terminates_in_support':True,'support_type':'END','support_element':'COLUMN',
            'external_face_m':face,'graphical_x_m':n2['x_start_common'],
            'source':{'mapping':'V536_beam_mapping.json#/supports/left','engineer_decision':'N2 left undimensioned end coincides with external column face'}},
        'RIGHT':{'terminates_in_support':True,'support_type':'INTERMEDIATE','support_element':'COLUMN',
            'explicit_x_m':n2['x_end_common'],
            'explicit_dimension_source':{'input':'V536_V565_detalhamento_prancha.json#/longitudinal_reinforcement/positive/0/longitudinal_coordinates',
                'basis':'Existing audited right-end reconstruction: inner face 294 cm + dimension 82 cm = 376 cm; preserved independently from undimensioned left end'}}})
    if interpretation['status']!='PASS':raise ValueError('N2 interpretation unresolved')
    original=deepcopy(n2)
    x=interpretation['resolved']['LEFT']['x_m']
    local=float((Decimal(str(x))-Decimal(str(support['width']))/2)*100)
    projection=float((Decimal(str(n2['x_end_common']))-Decimal(str(x)))*100)
    for bar in [n2,next(b for b in model['longitudinal_reinforcement'] if b['mark']=='N2')]:
        bar['x_start_cm']=local;bar['horizontal_length_cm']=projection
        bar['source']=dict(bar['source'],endpoint_interpretation=interpretation,
            projection_provenance={'rule':'physical endpoint difference, not developed bar length or equivalent anchorage',
                'original_projection_cm':original['horizontal_length_cm'],'original_developed_length_cm':original['length_cm'],
                'developed_length_and_bend_consistency_verified':False})
    n2['x_start_common']=x
    context,bars,diagram=load_detail_case('V536')
    updated=next(b for b in bars if b['mark']=='N2')
    updated.update({k:deepcopy(n2[k]) for k in ('x_start_common','x_start_cm','horizontal_length_cm','source')})
    context['longitudinal_provenance']['endpoint_interpretation']=interpretation
    tqs,positioned,raw=read('V536_tqs.json'),read('V536_tqs_positions.json'),read('V536_tqs_raw.json')
    strict=check_positive_flexure(model,tqs,positioned,mapping,raw,api)
    sampled=check_longitudinal(bars,context,diagram,api)
    scaling=check_bar_scaling(model,tqs,positioned,mapping,raw,api,interrupted_mark='N3',cut_side='left',scope=dict(SUPPORTED_SCOPE,provenance={'source':'Existing validated V536 N3 straight-bar scaling hypotheses'}))
    shear=shear_from_tqs(mapping,tqs,positioned,raw)
    left=SupportGeometry('V536:1',support['resolution']['resolved_support_id'],'LEFT','END',support['inner_face_x'],face,
        support['axis_x'],support['width']*100,{'support':support,'endpoint_interpretation':interpretation})
    left_result=check_support(context,bars,diagram,api,geometry=left,shear=shear,generate_corrections=False)
    right_data=read('V536_right_support_anchorage_check.json');g=right_data['geometry']
    right=SupportGeometry(g['span_id'],g['support_id'],g['support_side'],g['support_type'],g['internal_face_m'],g['external_face_m'],g['support_axis_m'],g['support_width_cm'],g['provenance'])
    for b in bars:
        b['termination_by_side']={'RIGHT':'STRAIGHT'}
        b['termination_provenance']={'source':'Existing audited right straight ends; no geometric bend inferred by endpoint convention'}
    context_right=deepcopy(context)
    negative=next(s for s in mapping['force_series'] if s['quantity']=='bending_moment' and s['envelope']=='min')
    context_right.update(support_side='RIGHT',support_type='INTERMEDIATE',transverse_geometry_resolved=False,
        node_interferences_verified=False,al_scope_confirmed=True,mk_negative_support_kncm=min(0,negative['values'][-1])*100)
    right_result=check_support(context_right,bars,diagram,api,geometry=right,shear=shear,generate_corrections=False)
    return {'beam_id':'V536','endpoint_interpretation':interpretation,'original_N2':original,
        'interpreted_N2':n2,'prepared_inputs':{'beam_model':model,'mapping':mapping},
        'positive_flexure_documentary':strict,'positive_flexure_sampled':sampled,'positive_scaling':scaling,
        'left_support':left_result,'right_support':right_result,'selected_solution':None,'detailing_optimization':None,
        'limitations':['developed_length_and_bend_consistency_not_verified','endpoint_convention_does_not_verify_bend_or_resistant_anchorage',
            'no_correction_generation','no_pdf_read_or_write'],
        'inputs':{name:source(name) for name in ('V536_beam_mapping.json','V536_V565_beam_model.json','V536_tqs.json','V536_tqs_positions.json','V536_tqs_raw.json')}}


def updated_v536(result):
    old=make('V536');ctx=old['context'];src=source('V536_positive_diagnostic_reverification.json')
    ctx['endpoint_interpretation']=result['endpoint_interpretation'];ctx['diagnostic_revision']='1.1'
    modules=[]
    modules.append(adapters.positive_regions(result['positive_flexure_documentary'],ctx,dict(src,pointer='/positive_flexure_documentary')))
    groups=[]
    for r in result['positive_flexure_sampled']['regions']:
        g=r['geometry'];groups.append({'span':1,'start_m':g['x_start_m'],'end_m':g['x_end_m'],'marks':g['geometric_reinforcement']['marks'],'result':{'regions':[r]}})
    modules.append(adapters.regional({'regions':groups,'source_layout':'flat_regions'},ctx,dict(src,pointer='/positive_flexure_sampled'),'positive_flexure'))
    for key in ('left_support','right_support'):
        r=result[key];geom=r['geometry'];checks=[]
        for bar in r['longitudinal_bars']:
            for kind,c in bar.get('controls',{}).items():
                checks.append(adapters.check(kind,key+'/'+bar['bar']['mark']+'/'+kind,c,dict(src,pointer='/'+key),
                    span=1,interval=sorted([geom['internal_face_m'],geom['external_face_m']]),marks=[bar['bar']['mark']],**adapters.control_values(c)))
        checks.append(adapters.check('support_area',key+'/area',{'passes':r['area_sufficient']},dict(src,pointer='/'+key),
            span=1,interval=sorted([geom['internal_face_m'],geom['external_face_m']]),marks=[bar['bar']['mark'] for bar in r['longitudinal_bars']],
            required=r['required_area_cm2'],provided=r['effective_area_at_face_cm2'],unit='cm2',comparison='provided_ge_required'))
        if key=='left_support':
            local=r.get('end_support_result')
            if local is None:raise ValueError('existing_end_support_contract_unresolved')
            a=local['anchorage']
            checks.append(adapters.check('anchorage_length',key+'/length',{'passes':a['comprimento_suficiente'],'reason':'existing support anchorage'},dict(src,pointer='/'+key),
                span=1,interval=sorted([geom['internal_face_m'],geom['external_face_m']]),marks=['N2'],required=a['lb_nec_cm'],provided=a['comprimento_disponivel_cm'],unit='cm',comparison='provided_ge_required'))
        checks.append(adapters.check('node_complete',key+'/node',{'passes':r['support_verified'],'reason':r['diagnostics']},dict(src,pointer='/'+key),span=1,interval=sorted([geom['internal_face_m'],geom['external_face_m']])))
        modules.append(adapters.envelope(ctx,'anchorage',dict(src,pointer='/'+key),checks,complete=False))
    checks=[]
    for kind in ('condition_A','condition_B'):
        c=result['positive_scaling'][kind];end=result['positive_scaling']['event_x_m']
        checks.append(adapters.check(kind,'scaling/N3/'+kind,c,dict(src,pointer='/positive_scaling/'+kind),span=1,interval=[end,end] if end is not None else None,marks=['N3'],**adapters.control_values(c)))
    modules.append(adapters.envelope(ctx,'anchorage',dict(src,pointer='/positive_scaling'),checks,complete=result['positive_scaling']['overall']['complete']))
    out=attach_execution(consolidate(ctx,modules));out['previous_diagnostic_source']=source('V536_beam_diagnostic.json')
    out['occurrence_groups']=occurrence_groups(out)
    return out


def run():
    r=reverify_v536();p=BASE/'V536_positive_diagnostic_reverification.json'
    p.write_text(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    for beam in ('V536','V516','V517'):
        d=updated_v536(r) if beam=='V536' else attach_execution(make(beam))
        d['occurrence_groups']=occurrence_groups(d)
        (BASE/(beam+'_beam_diagnostic_updated.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
        (ROOT/'.codex/analises'/(beam+'_beam_diagnostic_updated.md')).write_text(markdown(d),encoding='utf8')
        print(beam,d['overall_status'],d['execution_state'])
    (BASE/'future_detailing_contracts.json').write_text(json.dumps({'preferences':detailing_preferences([5,6.3,8,10,12.5,16,20,25]),'proposal_contract':proposal_template(),'generated_real_proposals':[]},ensure_ascii=False,indent=2),encoding='utf8')

if __name__=='__main__':run()

