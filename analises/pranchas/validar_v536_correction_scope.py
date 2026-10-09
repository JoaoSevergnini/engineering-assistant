"""V536 N2 correction study; reads historical diagnostics, writes own outputs only."""
from pathlib import Path
from copy import deepcopy
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT/'analises/pranchas'),str(ROOT.parent/'concretopy')]
import concretopy as api
from correction_engine import propose_corrections,SCOPE_RULE,EXCLUDED_NODE_CONTROLS
from support_staples import evaluate_staple
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
    context.update(gancho_valido=True,extension_target_x_m=n2['x_start_common'])
    candidates=extension_candidates(bars,context['support_reference_x_m'],context['extension_target_x_m'])
    candidates+=redistribution_candidates(bars,api,context['section'],series=[12.5,16,20],max_steps=2,counts=(2,3))
    specs=[];by_id={'existing_area_correction':{'id':'existing_area_correction','origin':'EXISTENTE','bars':deepcopy(bars),'changes':[]}}
    for c in candidates:
        by_id[c['id']]=c
        specs.append({'type':'EXTEND_OTHER_BARS' if c['origin']=='PROLONGAMENTO' else 'REDISTRIBUTE_BARS',
            'proposed_geometry':{'candidate_id':c['id'],'bars':deepcopy(c['bars'])},'changed_dimensions':deepcopy(c['changes']),
            'affected_checks':['support_anchorage','regional_positive_flexure','transverse_fit','node_interferences','affected_scaling','corrected_steel_area','longitudinal_continuity'],
            'degree_of_intervention':'EXTEND_EXISTING_BARS' if c['origin']=='PROLONGAMENTO' else 'CHANGE_TWO_POSITIONS',
            'comparison_facts':{'changed_positions':1 if c['origin']=='PROLONGAMENTO' else 2,'reuses_existing_diameters':c['origin']=='PROLONGAMENTO'}})
    source={'path':'analises/pranchas/validar_v536_correction_engine.py','verifier':'evaluate_detail_candidate; Concretopy API','gancho_valido':True}
    def check(name,value):return {'check_id':name,'status':'PASS' if value is True else 'FAIL' if value is False else 'INCONCLUSIVE','source':source}
    def reverify(spec):
        if spec['type']=='END_BEND':return {'checks':[],'pending_information':['curved_anchorage_resistance_parameters_and_applicable_criterion'],'historical_hook_scenario_not_a_new_curve_validation':True}
        c=by_id[spec['proposed_geometry']['candidate_id']]
        r=evaluate_detail_candidate(context,bars,c,diagram,api)
        metrics=r.get('support_check',{}).get('metrics') or {}
        area_ok=metrics.get('As_effective_cm2')>=metrics.get('As_corr_cm2') if metrics.get('As_effective_cm2') is not None and metrics.get('As_corr_cm2') is not None else None
        checks=[check('support_anchorage',r.get('support_check',{}).get('passes')),check('regional_positive_flexure',r.get('longitudinal_check',{}).get('compatibilidade_flexao_positiva')),check('transverse_fit',r.get('cabimento_transversal')),check('node_interferences',None),check('affected_scaling',None),check('corrected_steel_area',area_ok),check('longitudinal_continuity',r.get('original_span_capacity_not_reduced') if c['origin']=='PROLONGAMENTO' else r.get('longitudinal_check',{}).get('compatibilidade_flexao_positiva'))]
        return {'checks':checks,'geometry_checks':[checks[2],checks[3]],'full_result':r,'pending_information':['recheck_scaling_for_modified_longitudinal_configuration']}
    bend={'sources':{'support_geometry':verified['left_support']['geometry'],'endpoint_position':verified['endpoint_interpretation'],'cover':'V536_V565_support_context.json','bar_diameter':'V536_positive_diagnostic_reverification.json#/interpreted_N2'},
        'diameter_mm':n2['diameter_mm'],'cover_cm':context['section']['cobrimento'],
        'documentary_existing_bend_cm':58,'documentary_bend_source':'V536_V565_beam_model.json#/longitudinal_reinforcement/N2',
        'intent':'Evaluate or revise existing end bend; do not infer a new feasible curve from the documentary leg',
        'position_within_support':{'status':'INCONCLUSIVE'},'node_interferences':{'status':'INCONCLUSIVE'}}
    primary={'type':'AREA_CORRECTION','proposed_geometry':{'candidate_id':'existing_area_correction','bars':deepcopy(bars)},'changed_dimensions':[],'affected_checks':['support_anchorage','regional_positive_flexure','transverse_fit','node_interferences','affected_scaling','corrected_steel_area','longitudinal_continuity'],'degree_of_intervention':'EXISTING_CONFIGURATION_BASELINE'}
    decision={'rule':SCOPE_RULE,'source':'Engineer scope clarification: pin, curved trajectory and column reinforcement interference excluded; corrected area plus regional resistance and detailing required','excluded_controls':list(EXCLUDED_NODE_CONTROLS)}
    study=propose_corrections(diag,occurrence_id=occurrence['occurrence_id'],bar='N2',extremity='LEFT',original_geometry=verified['interpreted_N2'],bend_data=bend,secondary_candidates=specs,reverify=reverify,support_geometry=verified['left_support']['geometry'],primary_candidate=primary,scope_decision=decision)
    study['source_files']={name:{'path':'analises/pranchas/'+name,'sha256':hashlib.sha256((base/name).read_bytes()).hexdigest()} for name in ('V536_beam_diagnostic_updated.json','V536_positive_diagnostic_reverification.json')}
    study['original_anchorage']=verified['left_support']['end_support_result']['anchorage']
    anchor=study['original_anchorage']
    study['complementary_staples']=[evaluate_staple(context,anchor['as_adicional_cm2'],anchor['comprimento_disponivel_cm'],phi,api,bond_scenario={'boa_aderencia':True,'status':'confirmed','provenance':'Engineer confirmed good bond for staples'},contributing_legs=2,leg_provenance='Engineer confirmed two contributing legs',target_provenance={'source':'original_anchorage.as_adicional_cm2; Concretopy'}) for phi in (6.3,8,10)]
    for staple in study['complementary_staples']:
        staple['scope_audit_original_diagnostics']=deepcopy(staple['diagnostics'])
        staple['diagnostics']=[d for d in staple['diagnostics'] if d!='interferencias_no_no_nao_verificadas']
        staple['not_executed_by_scope']=[{'check_id':name,'execution_state':'NOT_EXECUTED','technical_status':None,'source':decision} for name in EXCLUDED_NODE_CONTROLS]
    study['staple_resistant_contribution_credited']=False
    study['staple_pending_information']=['compatible_combined_anchorage_force_transfer_model','explicit_geometric_position_and_distribution']
    (base/'V536_N2_correction_engine_scope_updated.json').write_text(json.dumps(study,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
    lines=['# V536 N2: correções por área corrigida — escopo atualizado','','Pino, trajetória curva e interferência com armadura do pilar: NOT_EXECUTED_BY_SCOPE_DECISION; não são PASS nem pendências bloqueantes. Demais controles permanecem independentes.','',
        'Cenário de gancho previamente confirmado pelo engenheiro é preservado. Não se soma desenvolvimento horizontal+vertical como ancoragem. As_corr e As_adicional vêm exclusivamente do Concretopy.','',
        '| Configuração | Tipo | Geometria no escopo | Estrutura | Resultado | Pendências |','|---|---|---|---|---|---|']
    for a in study['alternatives']:lines.append('| '+' | '.join([a['proposed_geometry']['candidate_id'],a['intervention_type'],a['geometric_feasibility'],a['structural_feasibility'],a['status'],', '.join(a['pending_information'])])+' |')
    lines+=['','Cada candidata registra separadamente executados/aprovados, executados/reprovados, não executados por escopo e inconclusivos. Auditoria anterior à exclusão preservada. Área corrigida não comprova todas as condições construtivas. Escalonamentos alterados permanecem pendentes; não se presume atendimento.','',
        'Grampos: calculados Ø6,3/Ø8/Ø10 usando As_adicional da N2 original, dois ramos, boa aderência e API de lb existente. Contribuição resistente conjunta NÃO creditada: falta modelo compatível de transferência e posição física da distribuição.','',
        'Prioridade: alterar barras existentes; depois avaliar complementação compatível. Nenhuma solução escolhida ou aprovada. selected_solution=null. PDF e históricos preservados.']
    (ROOT/'.codex/analises/V536_N2_correction_engine_scope_updated.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print([(a['intervention_type'],a['status']) for a in study['alternatives']])
if __name__=='__main__':run()
