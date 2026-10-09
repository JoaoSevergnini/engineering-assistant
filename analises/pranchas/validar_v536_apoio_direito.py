"""Real V536 RIGHT intermediate anchorage fixture; no writes to historical goldens."""
import sys,json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT/'analises/pranchas'),str(ROOT.parent/'concretopy')]
from validar_v536_v565_correcao_apoio import load_detail_case,read,api,OUT
from support_geometry import SupportGeometry
from support_anchorage import check_support
from tqs_shear import shear_from_tqs

def build_golden():
    context,bars,diagram=load_detail_case('V536')
    mapping=read('V536_beam_mapping.json')
    support=mapping['supports']['right']
    detail=read('V536_V565_detalhamento_prancha.json')
    width=detail['geometry']['supports'][1]['width_along_beam']['value']
    from decimal import Decimal
    external=float(Decimal(str(support['inner_face_x']))+Decimal(str(width))/100)
    geometry=SupportGeometry('V536:1',support['resolution']['resolved_support_id'],'RIGHT','INTERMEDIATE',
        support['inner_face_x'],external,support['axis_x'],width,
        {'mapping':'analises/pranchas/V536_beam_mapping.json','support':deepcopy(support),
         'classification':'Engineer confirmed RIGHT INTERMEDIATE P7A',
         'external_face':'internal face + audited physical support width'})
    # Only N2 has an opposite-side bend; the audited right ends are straight.
    for bar in bars:
        bar['termination_by_side']={'RIGHT':'STRAIGHT'}
        bar['termination_provenance']={'source':'V536/V565 audited drawing; single left bend, right longitudinal ends straight',
            'original_shape':bar.get('shape'),'end_bend':deepcopy(bar.get('end_bend'))}
    context.update(support_side='RIGHT',support_type='INTERMEDIATE',transverse_geometry_resolved=False,
        node_interferences_verified=False,al_scope_confirmed=True)
    # Read actual negative envelope in terminal TQS section; no effort mirroring.
    from tqs_moments import at
    tqs,raw=read('V536_tqs.json'),read('V536_tqs_raw.json')
    candidates=[]
    for series in mapping['force_series']:
        if series.get('quantity')!='bending_moment' or series.get('envelope')!='min': continue
        for ref in series['sources']:
            source=tqs['sources'][ref.split('#')[0]]
            record=at(raw,source['raw_pointer']); norm=record.get('normalizacao') or {}
            if source['file']=='VGESFS.LST' and norm.get('grandeza_original')=='M MN.':
                if series['values'] != [v['normalizado']['valor'] for v in norm['valores']]: raise ValueError('negative_envelope_raw_mismatch')
                candidates.append((series,source,record))
    if len(candidates)!=1: raise ValueError('negative_terminal_series_unresolved')
    series,source,record=candidates[0]
    context['mk_negative_support_kncm']=min(0,series['values'][-1])*100
    context['intermediate_negative_moment_provenance']={'series':series,'source':source,'record':record,'section':'S13'}
    shear=shear_from_tqs(mapping,read('V536_tqs.json'),read('V536_tqs_positions.json'),read('V536_tqs_raw.json'))
    return check_support(context,bars,diagram,api,geometry=geometry,shear=shear)

if __name__=='__main__':
    r=build_golden()
    (OUT/'V536_right_support_anchorage_check.json').write_text(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps({k:r.get(k) for k in ('last_span_section','required_area_cm2','basic_lb_cm','available_penetration_cm','longitudinal_anchorage_passes','diagnostics')},ensure_ascii=True,indent=2))
