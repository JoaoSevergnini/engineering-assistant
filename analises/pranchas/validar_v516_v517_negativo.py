"""Documented V516/V517 case adapter; existing structural primitives unchanged."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal as D
import sys,json,hashlib,inspect
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'analises/pranchas'
sys.path[:0]=[str(ROOT/'tools/extrator_lst'),str(ROOT/'tools/reinforcement_checks'),str(ROOT.parent/'concretopy')]
from section_positions import fill_positions
from moment_diagram import diagram_from_tqs,terminal_tension_branch,tension_diagram
from tqs_shear import shear_from_tqs
from flexure_regions import decompose_regions
from longitudinal_review import check_flexure_regions,check_bar_event,basic_anchorage
from intermediate_support_review import check_intermediate_bar_event
from negative_end_support_review import review_negative_end_support
from negative_detailing import check_negative_end_node,check_intermediate_continuity
from negative_reinforcement_relations import review_negative_relation
from termination_event import describe_termination
from support_geometry import SupportGeometry
from materials import documented_fields,interpret_steel
import concretopy as api
PDF=Path('s:/PROJETOS EM EXECUÇÃO/24-155-INTEGRA-MIGUEL PEREIRA-RJ/APOIO/JOÃO/05 - TIPO DIFERENCIADO - RESIDENCIAL/VIGAS/RMP-EST-EX-1348-VIG-R00 - Copia.PDF')
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def save(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
def add(a,b):return float(D(str(a))+D(str(b)))
def sub(a,b):return float(D(str(a))-D(str(b)))
def bars():
    # End-face cover hypothesis explicitly authorized by engineer in this session.
    result=[]
    for mark,n,phi,vec,a,b,shape,bend in [('N4',3,16,[3],-.095,5.015,'bent',40),('N3',1,16,[0,1],.48,3.67,'straight',None),('N7',2,20,[2],3.635,13.775,'bent',45),('N8',1,20,[1],5.83,12.84,'straight',None),('N9',1,20,[0,1],8.94,12.84,'straight',None)]:
        result.append({'mark':mark,'bars':n,'diameter_mm':phi,'layers':vec,'function':'negative','face':'upper','x_start_common':a,'x_end_common':b,'shape':shape,'bend_leg_cm':bend,
            'source':{'document':PDF.name,'page':1,'bbox_pdf':[90,1800,735,2130],'label':mark,
             'coordinates':'N3: left internal face +36cm and length319; N8/N9: right internal face minus72cm and lengths701/390; N4/N7: external support face minus nominal cover2.5cm with horizontal511/1014',
             'end_cover_hypothesis':'engineer explicitly authorized 2.5cm on 2026-10-06',
             'layers':'section A and explicit second-layer labels; N4/N7 overlap layer arrangement unresolved'},
            'trajectory_id':mark+'-single-drawn-piece','physical_layer_id':vec,'continuity_documentation':{'drawing':mark,'basis':'single continuous piece drawn over support; not inferred from matching diameter'}})
    return result

def local_models(beam):
    original=read(beam+'_tqs.json');raw=read(beam+'_tqs_raw.json');supports=[]
    for r in raw['categorias']['apoios']:
        norm=r.get('normalizacao') or {}
        if r['origem']['arquivo']=='RELDTFPS.LST' and norm.get('tipo')=='apoio':
            fields=norm['campos'];supports.append({'label':fields['nome'],'width_m':fields['largura']['normalizado']['valor'],'depev_m':fields['excentricidade']['normalizado']['valor'],'source':deepcopy(r['origem'])})
    assert len(supports)==5 and len(original['beam']['spans'])==4
    axes=[0.0];views=[]
    for i,span in enumerate(original['beam']['spans']):
        axes.append(add(axes[-1],add(span['geometry']['length'],add(supports[i]['depev_m'],supports[i+1]['depev_m']))))
    for i,support in enumerate(supports):
        support.update(occurrence=i+1,id=f'{beam}/support-{i+1}/{support["label"]}',axis_m=axes[i],left_face_m=sub(axes[i],support['width_m']/2),right_face_m=add(axes[i],support['width_m']/2))
    assert axes==[0.0,2.08,6.62,11.0,13.68]
    for i,span in enumerate(original['beam']['spans']):
        local=deepcopy(original);local['beam']['spans']=[deepcopy(span)];local['beam']['spans'][0]['support_ids']=[supports[i]['label'],supports[i+1]['label']]
        local['case_adapter']={'source_span_index':i,'source_span_id':span['id'],'ordered_support_occurrences':[i+1,i+2],'original_consolidated_support_ids':span['support_ids'],'reason':'consolidator deduplicates repeated P2 names; ordered RELDTFPS rows prove distinct support instances','source_support_records':[supports[i]['source'],supports[i+1]['source']]}
        positioned,count=fill_positions(local,raw)
        for j,series in enumerate(positioned['beam']['spans'][0]['internal_forces']):
            series['positions']=[add(x,axes[i]) for x in series['positions']]
            positioned['provenance'][f'/beam/spans/0/internal_forces/{j}/positions']+=['case_adapter:global_origin_from_ordered_lengths_and_RELDTFPS_DEPEV']
        positioned['case_adapter']['global_axis_offset_m']=axes[i]
        positioned['case_adapter']['global_axis_operands']={'previous_VGESFS_lengths_m':[s['geometry']['length'] for s in original['beam']['spans'][:i]],'ordered_support_records':deepcopy(supports[:i+1]),'derivation':'sum previous span lengths + left/right RELDTFPS DEPEV; first beam support axis is zero'}
        positioned['coordinate_system']={'frame':'beam_global','origin':'axis of first support of the beam','unit':'m','span_local_axis_offset_m':axes[i]}
        positioned['policies']['section_positions']+=' CASE ADAPTER: stored positions are global beam abscissas after adding the explicitly recorded span-axis offset; not input to the one-span general mapper.'
        mapping={'beam_id':beam,'force_series':deepcopy(positioned['beam']['spans'][0]['internal_forces']),'supports':{'left':{'axis_x':axes[i]},'right':{'axis_x':axes[i+1]}},'case_adapter':deepcopy(positioned['case_adapter'])}
        diagram=diagram_from_tqs(mapping,local,positioned,raw,flexure_sign='NEGATIVE');shear=shear_from_tqs(mapping,local,positioned,raw)
        views.append((local,positioned,mapping,diagram,shear))
        save(f'{beam}_span_{i+1}_tqs_positions.json',positioned)
    return original,raw,supports,views

def monotone_support_branch(diagram,support_side):
    branch=terminal_tension_branch(diagram,'NEGATIVE',support_side)
    # Preserve the sampled decline toward the first trough/zero; an opposite
    # support rise is another branch, not an ambiguity of the selected support.
    indices=[i for i,x in enumerate(diagram.xs) if D(str(branch[0]))<=x<=D(str(branch[1]))]
    if support_side=='RIGHT':indices.reverse()
    taken=[indices[0]]
    for index in indices[1:]:
        if -diagram.ms[index]>-diagram.ms[taken[-1]]:break
        taken.append(index)
    if len(taken)<2:return branch
    return [float(diagram.xs[min(taken)]),float(diagram.xs[max(taken)])]

def context(raw,phi,domain):
    fck,fp=documented_fields(raw,'fck','MPa');gf,gfp=documented_fields(raw,'gamaf');gc,gcp=documented_fields(raw,'gamac');steel=interpret_steel(raw)
    return {'section':{'bw':19,'h':52,'cobrimento':2.5,'diametro_estribo_mm':phi},'fck_mpa':fck,'fyk_mpa':steel['derived_fyk_mpa'],'gamma_f':gf,'gamma_c':gc,'gamma_s':inspect.signature(api.verificar_flexao_viga_retangular).parameters['gamma_s'].default,
      'horizontal':True,'sliding_formwork':False,'al_scope_confirmed':True,'layer_order_basis':'from_tension_face','layer_order_provenance':{'drawing':'section A + explicit 1 bar second layer labels','unresolved_exception':'N4/N7 mixed overlap not assumed in one layer'},'span_domain_m':domain,
      'longitudinal_provenance':{'drawing':PDF.name,'section':'19/52; upper flange is in tension for negative flexure, rectangular web model','cover':'TQS 2.5cm; not local PDF dimension','stirrup':'regional written drawing diameter; extension to sampled support interior is an audit hypothesis'},
      'provenance':{'fck':fp,'gamma_f':gfp,'gamma_c':gcp,'steel':steel},'support_element':'COLUMN','support_scenario_provenance':{'PDF':'named P5/P6 supports','TQS':'ordered pillar records'}}

def run(beam):
    original,raw,supports,views=local_models(beam);reinforcement=bars();regions_out=[];span_summaries=[]
    for i,(local,pos,mapping,diagram,shear) in enumerate(views):
        phi=8 if i in (0,3) else 5;ctx=context(raw,phi,[supports[i]['axis_m'],supports[i+1]['axis_m']]);domain=[float(diagram.xs[0]),float(diagram.xs[-1])]
        cuts={*domain,*[x for b in reinforcement for x in (b['x_start_common'],b['x_end_common']) if domain[0]<x<domain[1]]}
        if i==2:cuts.update([8.64,9.16]) # written 191+52+113 cm stirrup regions, not artificial sampling.
        rr=[]
        for a,b in zip(sorted(cuts),sorted(cuts)[1:]):
            active=[r for r in reinforcement if r['x_start_common']<(a+b)/2<r['x_end_common']]
            names=[r['mark'] for r in active];regional_phi=8 if i==2 and a>=8.64 and b<=9.16 else phi;rc=context(raw,regional_phi,ctx['span_domain_m'])
            if 'N4' in names and 'N7' in names:
                result={'passes':None,'diagnostics':['resistant_positions_not_defined_for_tail_overlap'],'regions':[], 'tail_overlap_engineer_accepted':True,'engineering_decision':{'authority':'engineer explicit clarification in this session','basis':'bars are already anchorage tails; may touch or lie immediately underneath one another','does_not_define':'exact centers or centroid for al'},'capacity_sum_credited':False,'review_status':'ENGINEER_ACCEPTED_TAIL_OVERLAP'}
                independent=[]
                for primary in ('N4','N7'):
                    one=check_flexure_regions([r for r in active if r['mark']==primary],rc,diagram,api,flexure_sign='NEGATIVE',domain=[a,b])
                    independent.append({'mark':primary,'hypothesis':'original isolated group position; not simultaneous mixed-layer arrangement','result':one})
                result['independent_reference_checks']=independent
            else:result=check_flexure_regions(active,rc,diagram,api,flexure_sign='NEGATIVE',domain=[a,b])
            item={'span':i+1,'start_m':a,'end_m':b,'marks':names,'stirrup_mm':regional_phi,'result':result};rr.append(item);regions_out.append(item)
        span_summaries.append({'span':i+1,'supports':[supports[i]['id'],supports[i+1]['id']],'sampled_domain_m':domain,'physical_axes_m':ctx['span_domain_m'],'clear_length_cm':(supports[i+1]['left_face_m']-supports[i]['right_face_m'])*100,'diagram':diagram.as_dict(),'shear':shear,'regional_results':rr})
    events=[]
    # Straight span segments of globally bent bars; original shape/source preserved.
    for mark,side,idx,support_side,mode in [('N3','LEFT',0,'RIGHT','SCALING'),('N3','RIGHT',1,'LEFT','SCALING'),('N4','RIGHT',1,'LEFT','SPAN_TERMINATION'),('N7','LEFT',1,'RIGHT','SPAN_TERMINATION'),('N8','LEFT',1,'RIGHT','SCALING'),('N9','LEFT',2,'RIGHT','SCALING'),('N8','RIGHT',3,'LEFT','SCALING'),('N9','RIGHT',3,'LEFT','SCALING')]:
        diagram=views[idx][3];shear=views[idx][4];branch=monotone_support_branch(diagram,support_side)
        phi=8 if idx in (0,3) else 5
        if mark=='N9' and side=='LEFT':phi=8 # event occurs inside the explicit suspension interval.
        ctx=context(raw,phi,[supports[idx]['axis_m'],supports[idx+1]['axis_m']])
        active=[deepcopy(r) for r in reinforcement if r['x_start_common']<float(diagram.xs[-1]) and r['x_end_common']>float(diagram.xs[0])]
        for r in active:
            if r['mark'] in ('N4','N7'):r['source']['segment_interpretation']='straight horizontal span segment; end bend excluded';r['shape']='straight'
        ctx['negative_support_side']=support_side
        target=next(r for r in reinforcement if r['mark']==mark)
        if idx==1 and mark!='N8':
            result={'passes':None,'complete':False,'checks':{},'diagnostics':['d_for_al_unresolved_in_engineer_accepted_tail_overlap'],'actual_end_position_m':target['x_start_common' if side=='LEFT' else 'x_end_common'],'anchorage':basic_anchorage(target['diameter_mm'],ctx,api,flexure_sign='NEGATIVE')}
        else:
            if idx==1:active=[r for r in active if r['mark'] in ('N7','N8')]
            # physical cut happens inside actual span; bars may extend into adjacent ones.
            support_index=idx if support_side=='LEFT' else idx+1
            if mode=='SCALING' and 0<support_index<len(supports)-1:
                support=supports[support_index]
                g=SupportGeometry(idx+1,support['id'],support_side,'INTERMEDIATE',support['right_face_m' if support_side=='LEFT' else 'left_face_m'],support['left_face_m' if support_side=='LEFT' else 'right_face_m'],support['axis_m'],float(D(str(support['width_m']))*100),{'ordered_support':support})
                previous_idx=idx-1 if support_side=='LEFT' else idx+1
                previous_diagram=views[previous_idx][3]
                previous_active=[deepcopy(r) for r in reinforcement if r['x_start_common']<float(previous_diagram.xs[-1]) and r['x_end_common']>float(previous_diagram.xs[0])]
                for r in previous_active:
                    if r['shape']=='bent':r['source']['segment_interpretation']='straight horizontal span segment; end bend excluded';r['shape']='straight'
                previous_ctx=context(raw,phi,[supports[previous_idx]['axis_m'],supports[previous_idx+1]['axis_m']])
                result=check_intermediate_bar_event(active,ctx,diagram,shear,api,mark=mark,cut_side=side,support=g,previous_bars=previous_active,previous_context=previous_ctx,previous_diagram=previous_diagram,branch_domain=branch)
            else:
                result=check_bar_event(active,ctx,diagram,shear,api,mark=mark,cut_side=side,mode=mode,branch_domain=branch)
        events.append({'mark':mark,'cut_side':side,'span':idx+1,'mode':result.get('mode',mode),'branch_domain_m':branch,'stirrup_mm':phi,'result':result})
    nodes=[]
    for mark,side,j,idx,leg in [('N4','LEFT',0,0,40),('N7','RIGHT',4,3,45)]:
        support=supports[j];g=SupportGeometry(idx+1,support['id'],side,'END',support['right_face_m' if side=='LEFT' else 'left_face_m'],support['left_face_m' if side=='LEFT' else 'right_face_m'],support['axis_m'],float(D(str(support['width_m']))*100),{'ordered_support':support})
        node=check_negative_end_node(next(r for r in reinforcement if r['mark']==mark),context(raw,8,[supports[idx]['axis_m'],supports[idx+1]['axis_m']]),g,api,bend_leg_cm=leg,bend_provenance={'PDF':PDF.name,'mark':mark,'written_leg_cm':leg})
        node_context=context(raw,8,[supports[idx]['axis_m'],supports[idx+1]['axis_m']])
        node_bars=[deepcopy(r) for r in reinforcement if r['x_start_common']<float(views[idx][3].xs[-1]) and r['x_end_common']>float(views[idx][3].xs[0])]
        end_review=review_negative_end_support(node_bars,node_context,views[idx][3],api,geometry=g,
            bend_documents={mark:{'side':side,'orientation':'vertical','vertical_leg_cm':leg,
                'provenance':{'PDF':PDF.name,'page':1,'mark':mark,'written_leg_cm':leg,
                    'basis':'written vertical end leg audited in shared drawing'}}},
            transverse_layout=None,column_geometry=None)
        verification=next(r for r in end_review['marks'] if r['bar']==mark)
        nodes.append({'mark':mark,'support':support['id'],'geometry':g.as_dict(),'result':node,'verification':verification})
    continuity=[]
    for j in (1,2,3):
        support=supports[j]
        gl=SupportGeometry(j,support['id'],'RIGHT','INTERMEDIATE',support['left_face_m'],support['right_face_m'],support['axis_m'],float(D(str(support['width_m']))*100),{'ordered_support':support})
        gr=SupportGeometry(j+1,support['id'],'LEFT','INTERMEDIATE',support['right_face_m'],support['left_face_m'],support['axis_m'],float(D(str(support['width_m']))*100),{'ordered_support':support})
        for bar in reinforcement:
            if bar['x_start_common']<support['left_face_m'] and bar['x_end_common']>support['right_face_m']:
                pending={'passes':None,'diagnostics':['independent_full_termination_controls_not_all_resolved'],'span_id':j}
                other={**deepcopy(pending),'span_id':j+1}
                c=check_intermediate_continuity(bar,bar,gl,gr,pending,other)
                continuity.append({'mark':bar['mark'],'support':support['id'],'result':c})
    # Semantic relations preserve all previous deterministic results as history.
    by_mark={b['mark']:b for b in reinforcement}
    relations=[]
    for span_idx,mark_a,mark_b,role in [(1,'N4','N7','adjacent_support_tails'),(2,'N7','N7','same_physical_piece')]:
        pair=deepcopy(supports[span_idx:span_idx+2])
        for support in pair:support['provenance']=deepcopy(support['source'])
        evidence={'support_ids':[s['id'] for s in pair],'role':role,
            'existing_tail_meeting_confirmed':role=='adjacent_support_tails',
            'provenance':{'drawing':PDF.name,'marks':[mark_a,mark_b],
                'structural_association':'documentary negative pieces associated with these adjacent support regions',
                'tail_meeting':'engineer confirmed N4/N7 are anchorage tails; exact mixed centers not supplied'}}
        ctx=context(raw,5,[supports[span_idx]['axis_m'],supports[span_idx+1]['axis_m']])
        relation=review_negative_relation(by_mark[mark_a],by_mark[mark_b],ctx,views[span_idx][3],api,
            support_pair=pair,evidence=evidence,regional_checks=[r for r in regions_out if r['span']==span_idx+1])
        relation['span']=span_idx+1
        relations.append(relation)
    interpretations=[]
    for event in events:
        if event['span']==2 and (event['mark'],event['cut_side']) in [('N3','RIGHT'),('N4','RIGHT'),('N7','LEFT')]:
            scaling=event['mark']=='N3'
            current=None
            if scaling:
                # Conservative proof uses the isolated N4 group throughout the
                # adjacent branch, including overlap. N7 stays physically present
                # but receives no resistant credit; no mixed centroid or al used.
                proof_bars=[deepcopy(by_mark[m]) for m in ('N4','N3')]
                for proof_bar in proof_bars:
                    proof_bar['shape']='straight'
                    proof_bar['source']['segment_interpretation']='horizontal span segment; isolated proof subset, not removal of physically present N7'
                support=supports[1]
                g=SupportGeometry(2,support['id'],'LEFT','INTERMEDIATE',support['right_face_m'],support['left_face_m'],support['axis_m'],float(D(str(support['width_m']))*100),{'ordered_support':support})
                current=check_intermediate_bar_event(proof_bars,context(raw,5,[supports[1]['axis_m'],supports[2]['axis_m']]),views[1][3],views[1][4],api,
                    mark=event['mark'],cut_side=event['cut_side'],support=g,
                    previous_bars=proof_bars,previous_context=context(raw,8,[supports[0]['axis_m'],supports[1]['axis_m']]),previous_diagram=views[0][3],branch_domain=event['branch_domain_m'])
                for old,new in [('reinforcement_before_cut','proof_subset_before_cut'),('reinforcement_after_cut','proof_subset_after_cut'),('capacity_remaining','capacity_remaining_proven_lower_bound'),('termination_event','proof_subset_termination_event')]:
                    if old in current:current[new]=current.pop(old)
                current['documentary_composition_at_end']=[deepcopy(r) for r in reinforcement if r['x_start_common']<by_mark['N3']['x_end_common']<=r['x_end_common']]
                actual_before=[r['mark'] for r in current['documentary_composition_at_end']]
                actual_after=[m for m in actual_before if m!=event['mark']]
                current['documentary_termination_event']=describe_termination(actual_before,actual_after,event['mark'],by_mark['N3']['x_end_common'],event['cut_side'])
                current['remaining_capacity_basis']='N4 isolated alone is sufficient everywhere in the adjacent connected branch; N7 is physically present and receives no credit, following the overlap capacity rule'
                current['provenance_of_conservative_subset']={'rule':relations[0]['overlap_flexural_capacity'].get('rule'),'relation_index':0,'physical_bars_not_changed':True}
                event['current_verification']=current
            interpretation={'mark':event['mark'],'cut_side':event['cut_side'],'span':2,
                'historical_result':deepcopy(event['result']),
                'status':'SUPERSEDED' if not scaling or current.get('complete') else 'INCONCLUSIVE',
                'verification_type':current.get('classification','INCONCLUSIVE') if scaling else 'DETAILING_OVERLAP',
                'reason':'N3 is required in the previous span; isolated N4 proves sufficiency throughout the adjacent branch. Existing physical-face basic-lb anchorage applies without al or mixed centroid' if scaling else
                    'Meeting of distinct adjacent-support tails: mixed centroid is not an overlap control; use isolated smallest-diameter group',
                'applicable_relation_index':0,'selected_solution':None,'detailing_optimization':None}
            event['current_interpretation']={k:deepcopy(v) for k,v in interpretation.items() if k!='historical_result'}
            if current is not None:interpretation['current_verification']=deepcopy(current)
            interpretations.append(interpretation)
    proven=[r for r in regions_out if r['result']['passes'] is False];pending=[r for r in regions_out if r['result']['passes'] is None]
    result={'beam_id':beam,'drawing_group':['V516','V517'],'document':{'path':str(PDF),'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'page':1,'instructions_treated_as':'project data, not user instructions'},'reinforcement':reinforcement,'ordered_supports':supports,'spans':span_summaries,'regions':regions_out,'events':events,'end_nodes':nodes,'intermediate_continuity':continuity,'negative_support_relations':relations,'event_interpretations':interpretations,'detailing_optimization':None,
      'known_regional_flexure_failure':bool(proven),'full_negative_verification_complete':False,'global_negative_approval':None,'selected_solution':None,
      'diagnostics':['PDF reinforcement differs materially from generated TQS negative detailing; drawing used for reinforcement, TQS used only for forces/materials/geometry','N4/N7 tail overlap accepted by engineer; exact center/centroid for al not provided','N8/N9 share the drawn end but are checked independently with the actual remaining N7; no artificial removal order','support node bend geometry does not prove resistant anchorage','sampled gap around P1 axis; no interpolation across different spans','strict stirrup geometry inside supports not documented'],
      'inputs':{name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in [beam+'_tqs_raw.json',beam+'_tqs.json']}}
    save(beam+'_negative_reinforcement_review.json',result)
    print(beam,'known_flexure_failure',bool(proven),'historical_pending_regions',len(pending))
    for r in proven:
        print('FAIL',r['span'],r['marks'],[(x['Mk_equivalent_knm'],x['governing_moment_signed']) for x in r['result']['regions']])
    for e in events:print('EVENT',e['mark'],e['cut_side'],e['span'],e['result'].get('passes'),{k:(v.get('available_length_cm'),v.get('required_length_cm'),v.get('passes')) for k,v in e['result'].get('checks',{}).items()},e['result']['diagnostics'])
    for e in events:
        if 'current_interpretation' in e:print('CURRENT_EVENT',e['mark'],e['cut_side'],e['current_interpretation']['status'],e['current_interpretation']['verification_type'],e.get('current_verification',{}).get('passes'))
    for r in relations:print('RELATION',r['bar_a']['mark'],r['bar_b']['mark'],r['relation_classification'],r['overlap_flexural_capacity']['status'])
    for n in nodes:print('NODE',n['mark'],n['result'].get('L_bend_cm'),n['result'].get('bend_geometry_passes'),n['result']['passes'])
    return result
if __name__=='__main__':
    for beam in ('V516','V517'):run(beam)
