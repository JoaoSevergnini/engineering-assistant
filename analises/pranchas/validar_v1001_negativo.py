"""Real V1001 right negative lobe; original positive goldens are read-only."""
from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT.parent/'concretopy')]
import concretopy as api
from moment_diagram import diagram_from_tqs,terminal_tension_branch
from tqs_shear import shear_from_tqs
from longitudinal_review import check_flexure_regions,check_bar_event
OUT=ROOT/'analises/pranchas'
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))

def build_golden():
    names=['V1001_beam_model.json','V1001_beam_mapping.json','V1001_tqs.json','V1001_tqs_positions.json','V1001_tqs_raw.json','V1001_N3_scaling_check.json']
    detail,mapping,tqs,positioned,raw,old=[read(name) for name in names]
    diagram=diagram_from_tqs(mapping,tqs,positioned,raw,flexure_sign='NEGATIVE')
    branch=terminal_tension_branch(diagram,'NEGATIVE','RIGHT')
    bars=[b for b in mapping['reinforcement'] if b.get('function')=='negative' and b['x_start_common']<branch[1] and b['x_end_common']>branch[0]]
    geometry=old['remaining_capacity']['call']['geometry'];params=old['remaining_capacity']['concretopy_result']['parametros']
    context={'section':{'bw':geometry['bw_cm'],'h':geometry['h_cm'],'cobrimento':geometry['cover_cm'],'diametro_estribo_mm':geometry['stirrup_diameter_mm']},
        'fck_mpa':params['fck'],'fyk_mpa':params['fyk'],'gamma_f':params['gamma_f'],'gamma_c':params['gamma_c'],'gamma_s':params['gamma_s'],
        'horizontal':True,'sliding_formwork':False,'al_scope_confirmed':True,'layer_order_basis':'from_tension_face',
        'layer_order_provenance':{'drawing':mapping['reinforcement'],'office_convention':'negative upper layer vectors read from top face; centers by public Concretopy convention'},
        'longitudinal_provenance':{'section':'previously audited rectangular geometry over sampled right lobe',
            'transverse_geometry':'uniform audit hypothesis; documentary support-region stirrup geometry remains unresolved'},
        'provenance':{'material_source':'V1001_N3_scaling_check.json (audited fck/fyk/gammas)','geometry_source':'beam_model + prior audited section',
            'branch':'connected negative lobe at right sampled terminal; adjacent opposite-sign sample retained, no extrapolation'}}
    shear=shear_from_tqs(mapping,tqs,positioned,raw)
    resistance=check_flexure_regions(bars,context,diagram,api,flexure_sign='NEGATIVE',domain=branch)
    scaling=check_bar_event(bars,context,diagram,shear,api,mark='N8',cut_side='LEFT',mode='SCALING',branch_domain=branch)
    return {'beam_id':'V1001','scope':'right negative lobe and N8 left interruption, not full beam negative approval',
        'context':context,'branch_domain_m':branch,'flexure':resistance,'scaling':scaling,
        'inputs':{name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in names},
        'selected_solution':None,'global_negative_approval':None,
        'limitations':['left negative lobe not part of this golden','no adjacent-span diagram to prove support continuity',
            'strict transverse geometry inside support unresolved','no end-frame/cantilever case in this golden']}

if __name__=='__main__':
    result=build_golden()
    (OUT/'V1001_negative_reinforcement_golden.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print('flexure',result['flexure']['passes'],'scaling',result['scaling']['passes'],'diagnostics',result['scaling']['diagnostics'])
    print('region capacities',[(r.get('Mk_equivalent_knm'),r.get('governing_moment_signed')) for r in result['flexure']['regions']])
    print('scaling checks',result['scaling']['checks'])
