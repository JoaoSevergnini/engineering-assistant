"""Integrated real V536 positive workflow golden; existing inputs are read-only.

This fixture composes validated checks. It introduces no structural formulas,
oriented intermediate-support anchorage and no automatic selection of a correction.
"""
import sys, json, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/reinforcement_checks'), str(ROOT/'analises/pranchas'), str(ROOT.parent/'concretopy')]
from validar_v536_v565_correcao_apoio import load_detail_case, read, api, OUT
from validar_v536_v565_grampos import study
from positive_flexure import check_positive_flexure
from validar_v536_v565_apoio_esquerdo import load_case, SEARCH as GENERIC_SEARCH
from support_alternatives import explore_alternatives
from support_correction import transverse_fit
from validar_v536_apoio_direito import build_golden as build_right_support
from bar_scaling import check_bar_scaling, SUPPORTED_SCOPE

INPUTS = ['V536_V565_detalhamento_prancha.json','V536_V565_beam_model.json',
    'V536_tqs.json','V536_tqs_positions.json','V536_tqs_raw.json','V536_beam_mapping.json',
    'V536_V565_support_context.json','V536_N3_scaling_check.json']


def build_golden():
    context, bars, diagram = load_detail_case('V536')
    data = {name: read(name) for name in INPUTS}
    inputs = {name: {'path': 'analises/pranchas/'+name,
        'sha256': hashlib.sha256((OUT/name).read_bytes()).hexdigest()} for name in INPUTS}
    mapping = data['V536_beam_mapping.json']
    for entry in mapping.get('inputs', {}).values():
        p = Path(entry['path'])
        if not p.is_absolute(): p = ROOT/p
        if hashlib.sha256(p.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('stale_mapping_input:' + str(p))
    if inputs['V536_tqs_raw.json']['sha256'] != data['V536_tqs.json']['raw_document']['sha256']:
        raise ValueError('raw_hash_mismatch')
    strict = check_positive_flexure(data['V536_V565_beam_model.json'], data['V536_tqs.json'],
        data['V536_tqs_positions.json'], mapping, data['V536_tqs_raw.json'], api)
    scaling = check_bar_scaling(data['V536_V565_beam_model.json'],data['V536_tqs.json'],
        data['V536_tqs_positions.json'],mapping,data['V536_tqs_raw.json'],api,
        interrupted_mark='N3',cut_side='left',scope={**SUPPORTED_SCOPE,
        'provenance': {'fixture': 'V536 positive integrated golden',
            'hypotheses': 'Previously audited straight horizontal interrupted N3; N2 support bend not part of scaling; no welds, sliding formwork or special longitudinal compression'}})
    local_context, current_configuration, documentary = load_case('V536')
    generic = explore_alternatives(local_context, current_configuration, api, search=GENERIC_SEARCH)
    for candidate in generic['alternatives']:
        candidate['integration_transverse_fit'] = transverse_fit(context['section'], candidate['configuration']['layers'], api)
        candidate['longitudinal_compatibility_verified_by_generic_search'] = False
        candidate['ready_for_detailing'] = False
    alternatives = study('V536')
    correction = alternatives['correction']
    existing = correction['existing']
    regional = existing['longitudinal_check']
    span_left, span_right = strict['domain_m']
    sample_left, sample_right = float(diagram.xs[0]), float(diagram.xs[-1])
    coverage_complete = sample_left <= span_left and sample_right >= span_right
    sampled_flexure = regional['compatibilidade_flexao_positiva']
    failures = []
    if existing['support_check']['passes'] is False: failures.append('existing_left_support_anchorage_fails')
    if scaling['overall']['scaling_passes'] is False: failures.append('positive_scaling_fails')
    if sampled_flexure is False: failures.append('sampled_positive_flexure_fails')
    right = build_right_support()
    if right['longitudinal_anchorage_passes'] is False: failures.append('existing_right_support_anchorage_fails')
    pending = [
        {'code': 'right_support_transverse_geometry_unresolved',
         'detail': 'Longitudinal anchorage evaluated; documentary transverse geometry and complete node remain unresolved.'},
        {'code': 'node_interferences_and_bends_pending',
         'detail': 'Staple spacing defined; initial position/window, node interference, bend geometry and force transfer not fully verified.'},
        {'code': 'correction_selection_pending', 'detail': 'Engineer decision required; no solution selected or original drawing changed.'}]
    if strict['span_summary']['incomplete']:
        pending.append({'code': 'documentary_flexure_geometry_incomplete',
            'detail': 'Documented stirrup distribution covers clear span only; strict flexure preserves unresolved transverse geometry inside supports.',
            'regions': [r['region_id'] for r in strict['regions'] if r['blockers']]})
    if not coverage_complete:
        pending.append({'code': 'moment_diagram_does_not_cover_whole_physical_domain',
            'physical_domain_m': strict['domain_m'], 'sampled_domain_m': [sample_left,sample_right],
            'detail': 'No extrapolation beyond adopted TQS samples.'})
    stages = {
        'geometry_and_composition': {'status': 'AUDITADO', 'mapping_geometry': mapping['geometry'],
            'principal_bars': bars, 'supports': mapping['supports'], 'context': context, 'left_documentary_anchorage': documentary},
        'positive_flexure_documentary': {'status': 'INCONCLUSIVO' if strict['span_summary']['incomplete'] else 'VERIFICADO', 'result': strict},
        'positive_flexure_sampled_model': {'status': 'ATENDE' if sampled_flexure is True else 'NAO_ATENDE' if sampled_flexure is False else 'INCONCLUSIVO',
            'scope': 'Previously adopted uniform section/layer hypothesis over sampled domain only; independent from strict documentary geometry.', 'result': regional},
        'positive_scaling': {'status': 'ATENDE' if scaling['overall']['scaling_passes'] is True else 'NAO_ATENDE' if scaling['overall']['scaling_passes'] is False else 'INCONCLUSIVO', 'result': scaling},
        'left_support_and_anchorage': {'status': 'ATENDE' if existing['support_check']['passes'] is True else 'NAO_ATENDE' if existing['support_check']['passes'] is False else 'INCONCLUSIVO', 'result': existing['support_check']},
        'generic_anchorage_exploration': {'status': 'EXPLORACAO_LOCAL_SEM_RECOMENDACAO', 'result': generic},
        'correction_alternatives': {'status': 'ALTERNATIVAS_PARA_DECISAO', 'result': correction},
        'complementary_staples': {'status': 'CALCULADOS_NO_PENDENTE', 'result': alternatives},
        'right_support_and_anchorage': {'status': 'ANCORAGEM_LONGITUDINAL_ATENDE_NO_PENDENTE' if right['longitudinal_anchorage_passes'] is True else 'INCONCLUSIVO' if right['longitudinal_anchorage_passes'] is None else 'NAO_ATENDE', 'support': mapping['supports']['right'], 'passes': right['longitudinal_anchorage_passes'], 'result': right}}
    summary = {'sampled_positive_flexure_passes': sampled_flexure,
        'scaling_passes': scaling['overall']['scaling_passes'],
        'existing_left_anchorage_passes': existing['support_check']['passes'],
        'existing_right_longitudinal_anchorage_passes': right['longitudinal_anchorage_passes'],
        'verified_original_checks_pass': False if failures else True,
        'recommended_extension_ids': correction['recommended_ids'],
        'next_step': correction['next_step'], 'selected_solution': None,
        'complete_positive_approval': False, 'positive_reinforcement_approved': None,
        'original_condition': 'FALHA_VERIFICADA' if failures else 'SEM_FALHA_NOS_CONTROLES_EXECUTADOS',
        'correction_ready_for_detailing': False, 'failures': failures, 'pending': pending}
    files = [Path(__file__), ROOT/'tools/reinforcement_checks'/ 'positive_flexure.py',
        *[ROOT/'tools/reinforcement_checks'/n for n in ('bar_scaling.py','support_alternatives.py','support_correction.py','support_staples.py','support_geometry.py','support_anchorage.py')]]
    return {'model_type': 'integrated_positive_reinforcement_golden', 'schema_version': '1.0',
        'beam_id': 'V536', 'date': '2026-10-06', 'inputs': inputs,
        'implementation': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'coverage': {'physical_domain_m': strict['domain_m'], 'sampled_domain_m': [sample_left,sample_right],
            'whole_physical_domain_sampled': coverage_complete, 'extrapolation': False},
        'stages': stages, 'summary': summary,
        'provenance_policy': 'Keep each original check full response/provenance; no orphan resistant values or new formula.',
        'limitations': ['node_not_fully_verified','no_global_beam_approval',
                        'no_automatic_correction_selection','no_negative_shear_suspension_or_minimum_check']}


def run():
    result = build_golden()
    (OUT/'V536_positive_reinforcement_complete_golden.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps(result['summary'],ensure_ascii=True,indent=2))

if __name__ == '__main__': run()
