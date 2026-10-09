"""V536 N2 correction study; reads historical diagnostics, writes own outputs only."""
from pathlib import Path
from copy import deepcopy
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT/'analises/pranchas'),str(ROOT.parent/'concretopy')]
import concretopy as api
from correction_engine import propose_corrections
from support_correction import extension_candidates,redistribution_candidates,evaluate_detail_candidate
from validar_v536_v565_correcao_apoio import load_detail_case

def run():
    base=ROOT/'analises/pranchas'
    read=lambda name:json.loads((base/name).read_text(encoding='utf8'))
    diag=read('V536_beam_diagnostic_updated.json');verified=read('V536_positive_diagnostic_reverification.json')
    occurrence=next(o for o in diag['occurrences'] if o['check_id']=='left_support/length')
    context,bars,diagram=load_detail_case('V536');context=deepcopy(context);bars=deepcopy(bars)
    n2=next(b for b in bars if b['mark']=='N2');n2.update(deepcopy(verified['interpreted_N2']));n2['d_cm']=next(b['d_cm'] for b in bars if b['mark']=='N2')
    # Conservative new-candidate scenario; previous authorized hook scenario stays historical.
    context.update(gancho_valido=False,extension_target_x_m=n2['x_start_common'])
    candidates=extension_candidates(bars,context['support_reference_x_m'],context['extension_target_x_m'])
    candidates+=redistribution_candidates(bars,api,context['section'],series=[12.5,16,20],max_steps=2,counts=(2,3))
    specs=[];by_id={}
    for c in candidates:
        by_id[c['id']]=c
        specs.append({'type':'EXTEND_OTHER_BARS' if c['origin']=='PROLONGAMENTO' else 'REDISTRIBUTE_BARS',
            'proposed_geometry':{'candidate_id':c['id'],'bars':deepcopy(c['bars'])},'changed_dimensions':deepcopy(c['changes']),
            'affected_checks':['support_anchorage','regional_positive_flexure','transverse_fit','node_interferences','affected_scaling'],
            'degree_of_intervention':'EXTEND_EXISTING_BARS' if c['origin']=='PROLONGAMENTO' else 'CHANGE_TWO_POSITIONS',
            'comparison_facts':{'changed_positions':1 if c['origin']=='PROLONGAMENTO' else 2,'reuses_existing_diameters':c['origin']=='PROLONGAMENTO'}})
    source={'path':'analises/pranchas/validar_v536_correction_engine.py','verifier':'evaluate_detail_candidate; Concretopy API','gancho_valido':False}
    def check(name,value):return {'check_id':name,'status':'PASS' if value is True else 'FAIL' if value is False else 'INCONCLUSIVE','source':source}
    def reverify(spec):
        if spec['type']=='END_BEND':return {'checks':[],'pending_information':['curved_anchorage_resistance_parameters_and_applicable_criterion'],'historical_hook_scenario_not_a_new_curve_validation':True}
        c=by_id[spec['proposed_geometry']['candidate_id']]
        r=evaluate_detail_candidate(context,bars,c,diagram,api)
        checks=[check('support_anchorage',r.get('support_check',{}).get('passes')),check('regional_positive_flexure',r.get('longitudinal_check',{}).get('compatibilidade_flexao_positiva')),check('transverse_fit',r.get('cabimento_transversal')),check('node_interferences',None),check('affected_scaling',None)]
        return {'checks':checks,'geometry_checks':[checks[2],checks[3]],'full_result':r,'pending_information':['node_interference_geometry','recheck_scaling_for_modified_longitudinal_configuration']}
    bend={'sources':{'support_geometry':verified['left_support']['geometry'],'endpoint_position':verified['endpoint_interpretation'],'cover':'V536_V565_support_context.json','bar_diameter':'V536_positive_diagnostic_reverification.json#/interpreted_N2'},
        'diameter_mm':n2['diameter_mm'],'cover_cm':context['section']['cobrimento'],
        'documentary_existing_bend_cm':58,'documentary_bend_source':'V536_V565_beam_model.json#/longitudinal_reinforcement/N2',
        'intent':'Evaluate or revise existing end bend; do not infer a new feasible curve from the documentary leg',
        'position_within_support':{'status':'INCONCLUSIVE'},'node_interferences':{'status':'INCONCLUSIVE'}}
    study=propose_corrections(diag,occurrence_id=occurrence['occurrence_id'],bar='N2',extremity='LEFT',original_geometry=verified['interpreted_N2'],bend_data=bend,secondary_candidates=specs,reverify=reverify,support_geometry=verified['left_support']['geometry'])
    study['source_files']={name:{'path':'analises/pranchas/'+name,'sha256':hashlib.sha256((base/name).read_bytes()).hexdigest()} for name in ('V536_beam_diagnostic_updated.json','V536_positive_diagnostic_reverification.json')}
    study['original_anchorage']=verified['left_support']['end_support_result']['anchorage']
    (base/'V536_N2_correction_engine.json').write_text(json.dumps(study,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    lines=['# V536 N2: motor inicial de correções','','Nenhuma solução selecionada ou aprovada. PDF e dados históricos preservados.','',
        'O cenário histórico autorizado de gancho continua auditado. As novas configurações usam gancho_valido=False, sem redução não comprovada. A N2 já possui dobra documental de 58 cm; a candidata prioritária avalia sua geometria e resistência, sem somar o desenvolvimento como ancoragem reta.','',
        '| Alternativa | Tipo | Geometria | Estrutura | Resultado | Pendências |','|---|---|---|---|---|---|']
    for a in study['alternatives']:lines.append('| '+' | '.join([a['proposed_geometry'].get('candidate_id','Revisar dobra existente N2'),a['intervention_type'],a['geometric_feasibility'],a['structural_feasibility'],a['status'],', '.join(a['pending_information'])])+' |')
    lines+=['','As alternativas secundárias reconstroem camadas e recalculam flexão regional, demanda por pares, d/x/z/al e ancoragem nas APIs existentes. Falhas comprovadas permanecem FAIL mesmo coexistindo pendências. Cabimento elementar não comprova interferências do nó. Escalonamentos afetados permanecem pendentes nesta integração, portanto nenhuma alternativa está pronta para detalhamento.','',
        'Comparação sem score: primeiro validade comprovada; depois reaproveitamento, simplicidade, posições alteradas, retrabalho e consumo racional. Prolongamentos reutilizam Ø20; redistribuições alteram duas posições. Nenhuma candidata está comprovadamente válida em todos os controles.','',
        'Faltam dimensão transversal e espaço interno comprovado do pilar, diâmetro interno/pino e critério correspondente, trajetória/trechos retos e curvos, interferências e parâmetros resistentes da ancoragem curva. Não se inventaram coordenadas PDF. selected_solution=null; aprovação=PENDING_ENGINEERING_APPROVAL.']
    (ROOT/'.codex/analises/V536_N2_correction_engine.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print([(a['intervention_type'],a['status']) for a in study['alternatives']])
if __name__=='__main__':run()
