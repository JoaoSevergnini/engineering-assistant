"""Real complementary staple study; previous fixtures/goldens are read-only."""
import sys, json, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools/reinforcement_checks'), str(ROOT/'analises/pranchas'), str(ROOT.parent/'concretopy')]
from validar_v536_v565_correcao_apoio import load_detail_case, SEARCH, api, OUT
from support_staples import staple_workflow, DEFAULT_STAPLE_DIAMETERS_MM

DIAMETERS = list(DEFAULT_STAPLE_DIAMETERS_MM)
BOND = [{'id': 'good_confirmed', 'boa_aderencia': True, 'status': 'confirmed',
    'provenance': {'source': 'Engineer reply in staple implementation session, 2026-10-06',
        'decision': 'Boa aderencia para grampos', 'scope': 'V536 staple longitudinal legs; physical placement not verified'}}]
LEGS = {'source': 'Engineer reply 2026-10-06', 'decision': 'Duas areas por grampo (dois ramos)',
        'scope': 'Two contributing longitudinal legs per piece; bend geometry remains unresolved'}

def study(beam):
    context, bars, diagram = load_detail_case(beam)
    result = staple_workflow(context, bars, diagram, api, redistribution_search=SEARCH,
        diameters_mm=DIAMETERS, bond_scenarios=BOND, contributing_legs=2,
        leg_provenance=LEGS, study_with_valid_extension=True)
    result.update(beam=beam, date='2026-10-06', context=context,
        engineer_decision={'source': 'Earlier correction session',
            'decision': 'Practical preference for staples; distinct from computed valid N3 prolongation'},
        documentary_sources={'detail': 'V536_V565_detalhamento_prancha.json',
            'mapping': beam+'_beam_mapping.json', 'scaling': beam+'_N3_scaling_check.json',
            'prior_correction': beam+'_support_correction.json',
            'historical_exploratory_staples': beam+'_support_staples_exploratory_historical.json',
            'geometry_decision': 'Engineer pasted request 2026-10-06: U, own usual diameters, connector width and usual maximum three pieces'})
    result['implementation'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [Path(__file__), ROOT/'tools/reinforcement_checks/support_staples.py']}
    return result

def run():
    for beam in ('V536', 'V565'):
        result = study(beam)
        (OUT/(beam+'_support_staples.json')).write_text(json.dumps(result, ensure_ascii=False,
            indent=2, allow_nan=False)+'\n', encoding='utf8')
        print(beam, 'initial additional area:', result['As_grampo_required_cm2'], 'next step:', result['next_step'])
        for c in result['staples']:
            print(c['id'], c['status'], c['quantity'], c.get('As_supplied_cm2'), c.get('lb_grampo_cm'), c.get('L_grampo_min_cm'), c['diagnostics'])

if __name__ == '__main__':
    run()
