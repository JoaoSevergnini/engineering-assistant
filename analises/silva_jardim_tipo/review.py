from pathlib import Path
import sys,json,copy,inspect,hashlib
from dataclasses import asdict
ROOT=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');OUT=ROOT/'analises/silva_jardim_tipo'
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT.parent/'concretopy')]
import concretopy as api
from moment_diagram import MomentDiagram,tension_diagram
from shear_diagram import ShearDiagram
from flexure_regions import decompose_regions
from longitudinal_review import check_flexure_regions
from shear_review import public_shear_api,design_shear,select_shear_depth
from materials import documented_fields,interpret_steel
D=json.loads((OUT/'drawing_inventory.json').read_text(encoding='utf8'));T=json.loads((OUT/'operational_tqs.json').read_text(encoding='utf8'))
OUTPUT={};RUNTIME={}
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
def context(raw,bw,h,phi):
 fck,fp=documented_fields(raw,'fck','MPa');gf,gfp=documented_fields(raw,'gamaf');gc,gcp=documented_fields(raw,'gamac');steel=interpret_steel(raw)
 return {'section':{'bw':bw,'h':h,'cobrimento':2.5,'diametro_estribo_mm':phi},'fck_mpa':fck,'fyk_mpa':steel['derived_fyk_mpa'],'gamma_f':gf,'gamma_c':gc,'gamma_s':1.15,'horizontal':True,'sliding_formwork':False,'al_scope_confirmed':True,'layer_order_basis':'from_tension_face','layer_order_provenance':{'source':'drawing visual reading and office convention'},'longitudinal_provenance':{'drawing':'drawing_inventory.json','cover':'2.5cm from TQS and typical PDF detail','coordinate_status':'graphical vector reading; centimeter sensitivity retained'},'provenance':{'fck':fp,'gamma_f':gfp,'gamma_c':gcp,'steel':steel}}
def prepare(active,allbars,ctx):
 count=max(len(b['layers']) for b in active);centers=[];layers=[]
 for i in range(count):
  phis={b['diameter_mm'] for b in active if len(b['layers'])>i and b['layers'][i]}
  if len(phis)>1:raise ValueError('mixed_diameters_in_one_physical_layer')
  if not phis:
   phis={b['diameter_mm'] for b in allbars if len(b['layers'])>i and b['layers'][i]}
   if len(phis)!=1:raise ValueError('unoccupied_reference_layer_geometry_unresolved')
  layers.append(api.CamadaArmaduraLongitudinal(1,api.Barra(next(iter(phis)))))
 ds=api.calcular_alturas_uteis_camadas(api.SecaoRetangular(**ctx['section']),layers)
 for i,d in enumerate(ds):centers.append({'documentary_layer':i+1,'origin':'COMPRESSION_FACE','value_cm':d,'provenance':{'method':'Concretopy nominal layer-position convention','diameters_per_layer_mm':[x.barra.diametro_mm for x in layers],'fixed_order':'from tension face; empty layer position retained'}})
 result=copy.deepcopy(ctx);result['layer_centers']=centers
 return result
# Explicit physical stirrup runs reconstructed from printed distribution lengths.
OVERRIDE={604:[(0,5.70,5,20),(5.70,7.35,5,18),(7.59,9.23,5,12),(9.23,14.925,5,20)],605:[(0,1.20,5,9),(1.20,3.60,5,14)],610:[(0,1.22,5,14),(1.22,2.38,5,14),(2.38,3.60,5,14),(3.79,11.16,5,14),(11.35,18.715,5,14)],611:[(0,2.82,5,14),(3.52,3.88,5,10),(3.88,5.43,5,8),(5.43,6.19,5,10),(6.89,9.31,5,14)],616:[(0,1.925,5,14),(2.115,3.225,6.3,11),(3.225,4.34,6.3,13)],623:[(0,2.64,6.3,16),(2.64,3.76,6.3,10)],626:[(0,1.43,5,8),(1.43,4.29,5,10)],629:[(0,3.76,5,14),(4.96,5.74,6.3,8),(5.74,6.51,6.3,10),(7.31,10.19,5,14)]}
SPECIAL={610:['first span stair-level section changes 129.5/47/122 unresolved; no global approval'],611:['height 47cm within middle span; conservative full-middle-span bound evaluated, 47cm interval reconstructed from 36+155+76cm stirrup dimensions; source kept separately'],623:['positive N2 2phi16 C456 is listed in steel schedule but not called/dimensioned in elevation; no positive bars assigned'],626:['19/47 and 19/57 transition and left support overhang unresolved; main span h57 corroborated by N8 stirrup height52; h47 left stub and its load path remain separate']}
for beam,t in T.items():
 number=int(beam[1:]);raw=json.loads((OUT/(beam+'_tqs_raw.json')).read_text(encoding='utf8'));bars=copy.deepcopy(D[beam]['bars']);supports=copy.deepcopy(t['supports']);geos=t['geometry'];result={'beam':beam,'drawing':D[beam]['pdf'],'geometry':[],'spans':[],'pending':SPECIAL.get(number,[]),'selected_solution':None,'detailing_optimization':None};views=[]
 for j,b in enumerate(bars):b['documentary_mark']=b['mark'];b['mark']=b['mark']+'@'+str(j+1)
 axes=[-supports[0]['width_cm']/200]
 for i,g in enumerate(geos):axes.append(round(axes[-1]+g['campos']['comprimento']['valor']+(supports[i]['depev_cm']+supports[i+1]['depev_cm'])/100,6))
 for i,g in enumerate(geos):
  fields=g['campos'];span=int(fields['vao']['valor']);length=fields['comprimento']['valor'];bw=fields['largura']['valor']*100;h=fields['altura']['valor']*100
  clear=[round(axes[i]+supports[i]['width_cm']/200,6),round(axes[i+1]-supports[i+1]['width_cm']/200,6)];xs=[round(axes[i]+supports[i]['depev_cm']/100+j*length/12,10) for j in range(13)]
  ss={s['label']:s for s in t['series'] if s['span']==span}
  def diagram(label):return MomentDiagram([{'x_m':x,'value_knm':v,'section':j+1,'provenance':ss[label]['source']} for j,(x,v) in enumerate(zip(xs,ss[label]['values']))],{'source':ss[label]['source'],'beam':beam,'span':span,'nature':'characteristic; corroborated by RELDTFPS Mk legend and gamma_f=1.4; no additional load combination created','positions':'VGESFS length/12 and ordered RELDTFPS DEPEV; first inner face origin'})
  mdpos,mdneg=diagram('M MX.'),diagram('M MN.')
  shseries=[{'quantity':'shear','unit':'kN','positions':xs,'sections':list(range(1,14)),'values':ss[label]['values'],'series_id':label,'provenance':ss[label]['source']} for label in ('Q MX.','Q MN.')];sd=ShearDiagram(shseries)
  height=h;bound=False
  if number==611 and i==1:height=57;bound=False
  if number==626:height=57;bound=False
  phi=6.3 if number==616 and i==1 or number==623 else 5
  ctx=context(raw,bw,height,phi);ctx['span_domain_m']=[xs[0],xs[-1]]
  geo={'span':span,'left':supports[i]['name'],'right':supports[i+1]['name'],'clear_span_m':round(clear[1]-clear[0],6),'width_cm':bw,'model_height_cm':h,'calculation_height_cm':height,'conservative_bound_only':bound,'axes_m':axes[i:i+2],'clear_domain_m':clear,'sampled_domain_m':[xs[0],xs[-1]],'DEPEV_cm':[supports[i]['depev_cm'],supports[i+1]['depev_cm']]};result['geometry'].append(geo)
  sr={'span':span,'geometry':geo,'flexure':{},'shear':[],'positive_supports':[],'negative_terminations':[]}
  for sign,diag in [('POSITIVE',mdpos),('NEGATIVE',mdneg)]:
   subset=[b for b in bars if b['function']==('positive' if sign=='POSITIVE' else 'negative')];regions=decompose_regions(subset,(xs[0],xs[-1]),flexure_sign=sign);out=[]
   if number==611 and i==1:
    split=[]
    for rr in regions:
     cuts=sorted({rr['x_start_m'],rr['x_end_m'],*[x for x in (3.88,5.43) if rr['x_start_m']<x<rr['x_end_m']]})
     for x,y in zip(cuts,cuts[1:]):
      copyr=copy.deepcopy(rr);copyr.update(x_start_m=x,x_end_m=y);split.append(copyr)
    regions=split
   for rg in regions:
    a,b=rg['x_start_m'],rg['x_end_m'];mid=(a+b)/2;active=[q for q in subset if q['x_start_common']<=mid<=q['x_end_common']];entry={'start_m':a,'end_m':b,'marks':[q['documentary_mark'] for q in active],'source_region':rg,'status':'INCONCLUSIVE','checks':None}
    demand=max([diag.moment_at_x(x)['value_knm']*(1 if sign=='POSITIVE' else -1) for x in sorted({a,b,*[x for x in xs if a<=x<=b]})]);entry['Msk_demand_knm']=max(0,demand)
    if demand<=0:entry.update(status='NOT_APPLICABLE',capacity_sufficient=None)
    elif number==610 and i==0:entry['diagnostics']=['geometry_and_bar_elevations_unresolved_for_stair_first_span']
    elif not active:entry['diagnostics']=['no_documented_longitudinal_composition_at_demand']
    else:
     try:
      rc=copy.deepcopy(ctx)
      if number==611 and i==1 and 3.88<=mid<=5.43:rc['section']['h']=47
      rc=prepare(active,subset,rc);check=check_flexure_regions(active,rc,diag,api,flexure_sign=sign,domain=[a,b]);entry['checks']=check
      records=[r for r in check['regions'] if not r.get('not_applicable')]
      entry['capacity_sufficient']=check['passes'];entry['status']='PASS' if check['passes'] is True else 'FAIL' if check['passes'] is False else 'INCONCLUSIVE';entry['diagnostics']=check['diagnostics']
      if records:
       controlling=max(records,key=lambda x:x.get('utilization') or 0);entry.update(MRd_knm=controlling['MRd_knm'],Mk_equivalent_knm=controlling['Mk_equivalent_knm'],utilization=controlling.get('utilization'),transverse_fit=controlling.get('transverse_fit'))
       cfg=controlling['configuration']['layers'];layers=tuple(api.CamadaArmaduraLongitudinal(e['count'],api.Barra(e['diameter_mm']),e['d_cm']) for e in cfg)
       minimum=api.verificar_flexao_viga_retangular(api.SecaoRetangular(**rc['section']),api.Concreto(ctx['fck_mpa']),api.Aco(ctx['fyk_mpa']),layers,gamma_f=ctx['gamma_f'],gamma_c=ctx['gamma_c'],gamma_s=ctx['gamma_s'],verificar_armadura_minima=True);entry['minimum_check']=asdict(minimum)
     except (ValueError,KeyError,TypeError,IndexError) as e:entry['diagnostics']=[str(e)]
    out.append(entry)
   sr['flexure'][sign]=out
  # Effective d chosen from independently calculated regional centroids by the skill rule.
  wrappers=[{'span':span,'start_m':r['start_m'],'end_m':r['end_m'],'marks':r['marks'],'result':{'regions':r['checks']['regions']}} for regs in sr['flexure'].values() for r in regs if r.get('checks')]
  depth=select_shear_depth(wrappers);ctx['effective_depth']=depth;sr['shear_effective_depth']=depth
  intervals=OVERRIDE.get(number,[(a,b,phi,20 if number in (602,603,606,607) else 12 if number==622 else 14) for a,b in [clear]])
  for j,(a,b,p,s) in enumerate(intervals):
   lo,hi=max(a,clear[0],xs[0]),min(b,clear[1],xs[-1])
   if lo>=hi:continue
   q=sd.maximum(lo,hi);entry={'drawn_interval_m':[a,b],'checked_interval_m':[lo,hi],'phi_mm':p,'spacing_cm':s,'legs':2,'Vsk_abs_kn':q['Vsk_abs_kn'],'source':'explicit PDF distribution lengths; source geometry in drawing_inventory.json; no extension within columns','demand':q}
   if number==610 and i==0:entry.update(status='INCONCLUSIVE',diagnostic='stair_section_changes_unresolved')
   else:
    design=design_shear(ctx,public_shear_api(),q['Vsk_abs_kn'],p);provided=2*api.Barra(p).area_cm2/s*100;entry.update(design=design,provided_Asw_per_s_cm2_m=provided)
    required=design.get('governing_Asw_per_s_cm2_m');sm=design.get('maximum_spacing_code_cm');entry.update(area_sufficient=None if required is None else provided>=required,spacing_sufficient=None if sm is None else s<=sm,diagonal_compression=design['diagonal_compression']);states=[entry['area_sufficient'],entry['spacing_sufficient'],design['diagonal_compression']['passes']];entry['status']='FAIL' if False in states else 'INCONCLUSIVE' if None in states else 'PASS'
   sr['shear'].append(entry)
  views.append((ctx,mdpos,mdneg,sd,bars,supports,axes,clear,sr));result['spans'].append(sr)
 OUTPUT[beam]=result;RUNTIME[beam]=views
 dump(beam+'_review.json',result)
 print(beam,[(s['span'],{sg:{st:sum(r['status']==st for r in regs) for st in ('PASS','FAIL','INCONCLUSIVE')} for sg,regs in s['flexure'].items()},[r['status'] for r in s['shear']]) for s in result['spans']])
dump('review_all.json',OUTPUT)
