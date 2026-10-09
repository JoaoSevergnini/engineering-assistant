"""Reproduce consolidated diagnostics from historical files without recalculation."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/reinforcement_checks'))
from beam_diagnostic import consolidate,markdown
import beam_diagnostic_adapters as adapters

BASE=ROOT/'analises/pranchas'

def load(name):
    p=BASE/name
    raw=p.read_bytes()
    return json.loads(raw.decode('utf-8-sig')),{'path':str(p.relative_to(ROOT)), 'sha256':hashlib.sha256(raw).hexdigest()}


def make(beam):
    tqs,tqs_source=load(beam+'_tqs.json')
    ctx={'beam_id':beam,'floor':'DIFERENCIADO','floor_source':{'project_directory':r'C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\DIFERENCIADO\VIGAS'},
         'coordinate_system':{'origin':'left_support_axis','positive_direction':'left_to_right','unit':'m'},
         'geometry':[{'id':s.get('id'),'geometry':s.get('geometry')} for s in tqs['beam']['spans']],'materials':tqs['beam']['materials'],
         'tqs_source':tqs_source,'data_version':tqs.get('schema_version'),'drawing_source':None}
    modules=[];audit=[]
    if (BASE/(beam+'_beam_mapping.json')).exists():
        mapping,mapping_source=load(beam+'_beam_mapping.json')
        if mapping['beam_id']!=beam or mapping['coordinate_system']!=ctx['coordinate_system']:raise ValueError('mapping identity mismatch')
        ctx['coordinate_source']=mapping_source
        ctx['drawing_source']=mapping.get('inputs',{}).get('detail')
        ctx['physical_geometry']=mapping.get('geometry')
    if (BASE/(beam+'_negative_reinforcement_review.json')).exists():
        data,src=load(beam+'_negative_reinforcement_review.json')
        if data['beam_id']!=beam:raise ValueError('historical identity mismatch')
        ctx.update(drawing_source=data['document'],physical_supports=data['ordered_supports'])
        modules += [adapters.regional(data,ctx,src),adapters.negative_anchorage(data,ctx,src)]
        audit += [{'excluded_history':data['event_interpretations'],'reason':'explicit SUPERSEDED controls preserved in original sources'}]
    if (BASE/(beam+'_positive_flexure_regions.json')).exists():
        data,src=load(beam+'_positive_flexure_regions.json')
        if data['coordinate_system']!=ctx['coordinate_system']:raise ValueError('source coordinate mismatch')
        modules.append(adapters.positive_regions(data,ctx,src))
        ctx['drawing_source']=data.get('inputs',{}).get('detail')
    if (BASE/(beam+'_positive_reinforcement_complete_golden.json')).exists():
        data,src=load(beam+'_positive_reinforcement_complete_golden.json')
        if data['beam_id']!=beam:raise ValueError('historical identity mismatch')
        stages=data['stages']
        modules.append(adapters.positive_regions(stages['positive_flexure_documentary']['result'],ctx,dict(src,pointer='/stages/positive_flexure_documentary/result')))
        sampled=stages['positive_flexure_sampled_model']['result']
        groups=[]
        for r in sampled['regions']:
            g=r['geometry'];groups.append(dict(span=1,start_m=g['x_start_m'],end_m=g['x_end_m'],
                marks=g['geometric_reinforcement']['marks'],result={'regions':[r]}))
        modules.append(adapters.regional({'regions':groups,'source_layout':'flat_regions'},ctx,dict(src,pointer='/stages/positive_flexure_sampled_model/result'),'positive_flexure'))
        ctx['drawing_source']=data['inputs'].get('V536_V565_detalhamento_prancha.json')
        ctx['coverage']=data['coverage']
        audit.append({'exploration_not_governing':['generic_anchorage_exploration','correction_alternatives','complementary_staples'],
                      'reason':'unselected alternatives do not change drawn configuration','source':src})
    if (BASE/(beam+'_left_support_anchorage_check.json')).exists():
        data,src=load(beam+'_left_support_anchorage_check.json')
        if data['beam']!=beam:raise ValueError('historical identity mismatch')
        modules.append(adapters.end_support_existing(data,ctx,src))
    if (BASE/(beam+'_right_support_anchorage_check.json')).exists():
        data,src=load(beam+'_right_support_anchorage_check.json')
        geom=data['geometry'];marks=[b['bar']['mark'] for b in data['longitudinal_bars']]
        checks=[adapters.check('reinforcement_area','right/area',{'passes':data['area_sufficient']},src,
            span=geom['span_id'],interval=sorted([geom['internal_face_m'],geom['external_face_m']]),marks=marks,
            required=data['required_area_cm2'],provided=data['effective_area_at_face_cm2'],unit='cm2',comparison='provided_ge_required')]
        for kind in ('base_penetration_check','zero_moment_check','full_utilization_check'):
            if isinstance(data.get(kind),dict):
                checks.append(adapters.check(kind,'right/'+kind,data[kind],dict(src,pointer='/'+kind),
                    span=geom['span_id'],interval=sorted([geom['internal_face_m'],geom['external_face_m']]),marks=marks,**adapters.control_values(data[kind])))
        for bar in data['longitudinal_bars']:
            for kind,control in bar['controls'].items():
                checks.append(adapters.check(kind,'right/'+bar['bar']['mark']+'/'+kind,control,src,span=geom['span_id'],interval=sorted([geom['internal_face_m'],geom['external_face_m']]),marks=[bar['bar']['mark']],**adapters.control_values(control)))
        checks.append(adapters.check('support_complete','right/node',{'passes':data['support_verified'],'reason':data['diagnostics']},src,
                    span=geom['span_id'],interval=sorted([geom['internal_face_m'],geom['external_face_m']]),marks=marks))
        modules.append(adapters.envelope(ctx,'anchorage',src,checks,complete=data['support_verified'] is not None))
    if (BASE/(beam+'_N3_scaling_check.json')).exists():
        data,src=load(beam+'_N3_scaling_check.json')
        if data['beam_id']!=beam:raise ValueError('historical identity mismatch')
        checks=[]
        for kind in ('condition_A','condition_B'):
            control=data[kind];end=data['event_x_m']
            checks.append(adapters.check(kind,'scaling/'+data['interrupted_mark']+'/'+kind,control,dict(src,pointer='/'+kind),
                span=1,interval=[end,end],marks=[data['interrupted_mark']],**adapters.control_values(control)))
        modules.append(adapters.envelope(ctx,'anchorage',src,checks,complete=data['overall']['complete']))
    for suffix,adapter in [('shear_reinforcement_review',adapters.shear),('suspension_review',adapters.suspension)]:
        if (BASE/(beam+'_'+suffix+'.json')).exists():
            data,src=load(beam+'_'+suffix+'.json')
            if data.get('beam_id',data.get('receiving_beam_id'))!=beam:raise ValueError('historical identity mismatch')
            modules.append(adapter(data,ctx,src))
    result=consolidate(ctx,modules);result['historical_interpretation_audit']=audit
    return result

if __name__=='__main__':
    for beam in ('V501','V516','V517','V536','V565'):
        result=make(beam)
        (BASE/(beam+'_beam_diagnostic.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
        (ROOT/'.codex/analises'/(beam+'_beam_diagnostic.md')).write_text(markdown(result),encoding='utf8')
        print(beam,result['overall_status'],result['discipline_status'],'failures',len(result['proven_nonconformities']))
