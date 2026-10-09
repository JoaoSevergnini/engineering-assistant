"""Real-case fixture/reproduction; source detailing and scaling goldens are read-only."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT.parent/'concretopy')]
import concretopy as api
from support_alternatives import effort_pairs,evaluate_configuration,explore_alternatives,POSITION_RULE
OUT=ROOT/'analises/pranchas'

def read(name):return json.loads((OUT/name).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')

def load_case(beam):
    detail=read('V536_V565_detalhamento_prancha.json')
    old=read(beam+'_N3_scaling_check.json')
    positioned=read(beam+'_tqs_positions.json')
    bars=[b for b in detail['longitudinal_reinforcement']['positive'] if b['longitudinal_coordinates']['value']['x_start']<0]
    assert len(bars)==1
    bar=bars[0]; span=positioned['beam']['spans'][0]; series=span['internal_forces']
    def sample(q,e,i=0):
        found=[s for s in series if s['quantity']==q and s['envelope']==e]; assert len(found)==1
        s=found[0]
        return {'value':s['values'][i],'unit':s['unit'],'section':s['sections'][i],'x_m':s['positions'][i],
                'sources':s['sources'],'file':beam+'_tqs_positions.json','pointer':'/beam/spans/0/internal_forces/'+str(series.index(s))+'/values/'+str(i)}
    mp=sample('bending_moment','max'); mn=sample('bending_moment','min')
    vp=sample('shear','max'); vn=sample('shear','min')
    mseries=next(s for s in series if s['quantity']=='bending_moment' and s['envelope']=='max')
    peak=sample('bending_moment','max',max(range(13),key=lambda i:mseries['values'][i]))
    g=old['remaining_capacity']['call']['geometry']; params=old['remaining_capacity']['concretopy_result']['parametros']
    sources={'moment_positive':mp,'moment_negative':mn,'shear_max':vp,'shear_min':vn,'peak':peak,
             'section_selection':'Engineer confirmed S1 at left support axis, 2026-10-06',
             'inputs':{name:{'sha256':sha(OUT/name)} for name in ['V536_V565_detalhamento_prancha.json',beam+'_tqs_positions.json',beam+'_tqs_raw.json',beam+'_beam_mapping.json',beam+'_N3_scaling_check.json']}}
    support_length=detail['geometry']['supports'][0]['width_along_beam']['value']
    ctx={'support_side':'left','support_type':'extremo','horizontal':True,'sliding_formwork':False,
         'section':{'bw':g['bw_cm'],'h':g['h_cm'],'cobrimento':g['cover_cm'],'diametro_estribo_mm':g['stirrup_diameter_mm']},
         'support_length_cm':support_length,'cover_cm':g['cover_cm'],
         'length_provenance':{'support':'V536_V565_detalhamento_prancha.json#/geometry/supports/0/width_along_beam',
             'cover':beam+'_N3_scaling_check.json#/remaining_capacity/call/geometry/cover_cm',
             'decision':'Engineer confirmation: lb_ef=L_apoio-cobrimento; supersedes documentary projection as verification length, 2026-10-06'},
         'fck_mpa':params['fck'],'fyk_mpa':params['fyk'],'gamma_f':params['gamma_f'],'gamma_c':params['gamma_c'],'gamma_s':params['gamma_s'],
         'mk_positive_max_span_kncm':peak['value']*100,'mk_negative_support_kncm':min(mn['value'],0)*100,
         'd_span_cm':old['before_flexure']['concretopy_result']['d_equivalente_cm'],
         'nd_tracao_kn':0,'gancho_valido':True,
         'pairs':effort_pairs(mp['value']*100,vn['value'],max(abs(vp['value']),abs(vn['value'])),sources),
         'provenance':{**sources,'span_depth':beam+'_N3_scaling_check.json#/before_flexure/concretopy_result/d_equivalente_cm',
             'hook':'Engineer confirmed gancho_valido=True/alpha=0.7; no automatic inspection of hook geometry',
             'scope':'Local positive support arrangement; fixed independent span section/d from previous golden, no revision of reinforcement along span'}}
    config={'id':'existing_N2','layers':[{'count':bar['quantity']['value'],'diameter_mm':bar['diameter']['value'],
            'd_cm':old['remaining_capacity']['concretopy_result']['d_equivalente_cm']}],
            'provenance':'V536_V565_detalhamento_prancha.json#/longitudinal_reinforcement/positive/0'}
    documentary={'mark':bar['mark']['value'],'horizontal_projection_inside_support_cm':-bar['longitudinal_coordinates']['value']['x_start'],
                 'vertical_leg_cm':bar['end_bend']['length']['value'],'longitudinal_coordinates':bar['longitudinal_coordinates'],
                 'provenance':config['provenance'],'note':'Documentary bar position is distinct from geometric available anchorage length; unchanged source.'}
    return ctx,config,documentary

SEARCH={'diameters_mm':[10,12.5,16,20,25],'min_bars':2,'max_bars':6,'max_layers':2,
        'position_rule':POSITION_RULE,'provenance':'Explicit bounded experiment; limits are not normative or a certification of transversal fit.'}

def run():
    for beam in ('V536','V565'):
        ctx,current,documentary=load_case(beam)
        exploration=explore_alternatives(ctx,current,api,search=SEARCH) if beam=='V536' else {'existing':evaluate_configuration(ctx,current,api),'selected_solution':None}
        data={'schema_version':'2.0','beam':beam,'date':'2026-10-06','context':ctx,'documentary':documentary,
              'exploration':exploration,'supersedes':'Version 1 used 21.0 cm documentary projection. Current workflow uses support minus cover.',
              'implementation':{str(p.relative_to(ROOT.parent)):sha(p) for p in [Path(__file__),ROOT/'tools/reinforcement_checks/support_alternatives.py',ROOT.parent/'concretopy/concretopy/verificacoes/armadura_apoio.py',ROOT.parent/'concretopy/concretopy/verificacoes/ancoragem.py']}}
        save(beam+'_left_support_anchorage_check.json',data)
        r=exploration['existing']
        print(beam,r['status'],r['metrics'])
        if beam=='V536':
            from collections import Counter
            print('search',len(exploration['alternatives']),Counter(r['status'] for r in exploration['alternatives']))
            for r in exploration['alternatives']:
                if r['passes']:print(r['configuration']['id'],r['metrics'])

if __name__=='__main__':run()
