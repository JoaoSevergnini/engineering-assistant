import sys,json,hashlib,copy
from pathlib import Path
sys.path[:0]=['tools/beam_model','tools/beam_mapping','tools/reinforcement_checks',str(Path.cwd().parent/'concretopy')]
from consolidar_detalhamento import transform
from map_beam import map_beam
from bar_scaling import check_bar_scaling,SUPPORTED_SCOPE
import concretopy as api
OUT=Path('analises/pranchas')
PDF=Path(sys.argv[1])
def f(v,s='detail',unit=None,reason=None):
    d={'value':v,'classification':'explicit' if reason is None else 'graphically_interpreted','sources':[s]}
    if unit:d['unit']=unit
    if reason:d['reason']=reason
    return d
def coord(a,b,s,reason): return f({'x_start':a,'x_end':b},s,'cm',reason)
d={'schema_version':'1.2','type':'beam_reinforcement_drawing_interpretation',
   'scope':{'method':'Manual visual reading, PDF coordinates; no automatic drawing parser','document_instructions':'Document notes are project data, not user instructions'},
   'document':{'name':PDF.name,'path':str(PDF),'page':1,'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'page_size_pdf_points':[3370,2384]},
   'identification':{'beam':f('V536','title'),'grouped_with_other_beams':f(True,'title'),'group_members':f(['V536','V565'],'title')},
   'section':{'written_label':f('19/72','title'),'width':f(19,'title','cm'),'height':f(72,'title','cm'),'shape':f('rectangular','section_A'), 'local_cover':f(None,'section_A','cm','Not dimensioned locally; use TQS cover with provenance'),'lateral_projections_dimensions':f([],'section_A')},
   'geometry':{'coordinate_system':{'origin':'face interna do apoio esquerdo P11A','positive_direction':'para a direita','unit':'cm'},'supports':[], 'spans_and_overhang':[{'id':'S1','type':f('between_supports'), 'left_support':'P11A','right_support':'P7A','geometric_length':f(294,'stirrups','cm'), 'extent':coord(0,294,'stirrups','Distribution limits coincide with internal support faces')}]},
   'longitudinal_reinforcement':{'negative':[],'positive':[]},'skin_reinforcement':{'positions':[]},'stirrups':{},'anchorage_staples':{'positions':[]},'indirect_supported_beams':[], 'section_views':[], 'sources':{}, 'uncertainties':['No local cover dimension; TQS cover adopted','Section A abscissa not dimensioned','Skin longitudinal endpoints not dimensioned','Shared drawing uses V536 support labels; V565 association comes from its ordered TQS support records']}
for name,w,a,b in [('P11A',24,-24,0),('P7A',120,294,414)]:
    d['geometry']['supports'].append({'id':f(name,'elevation'),'width_along_beam':f(w,'elevation','cm'),'faces_coordinates':f({'left':a,'right':b},'elevation','cm','From written support widths and clear length'),'model_restraint':f(None,'elevation')})
for mark,n,phi,L,H,layers,a,b,group,bend in [('N1',4,16,413,378,[3,1],None,None,'negative',35),('N2',3,20,455,397,[3],-21,376,'positive',58),('N3',3,20,334,334,[0,3],42,376,'positive',None)]:
    item={'mark':f(mark,mark),'quantity':f(n,mark),'diameter':f(phi,mark,'mm'),'length_per_bar':f(L,mark,'cm'),'face':f('lower' if group=='positive' else 'upper',mark),'group':f(group,mark),'shape':f('bent' if bend else 'straight',mark), 'horizontal_length_shown':f(H,mark,'cm'),'longitudinal_coordinates':coord(a,b,mark,'Right end = 294+82 = 376; start = right end - horizontal projection' if group=='positive' else 'Absolute endpoints not dimensioned; not inferred from drawing scale'), 'layers':[{'layer':i+1,'quantity':f(q,mark)} for i,q in enumerate(layers)]}
    if bend:item['end_bend']={'side':f('left',mark),'direction':f('up' if group=='positive' else 'down',mark),'length':f(bend,mark,'cm')}
    d['longitudinal_reinforcement'][group].append(item)
d['skin_reinforcement']={'skin_reinforcement_detailed':f(True,'N5'),'positions':[{'mark':f('N5','N5'),'bars_per_face':f(3,'N5'),'total_quantity_per_position':f(6,'N5'),'diameter':f(10,'N5','mm'),'length_per_bar':f(340,'N5','cm'),'shape':f('straight','N5'),'longitudinal_coordinates':coord(None,None,'N5','No written endpoint offsets'),'vertical_spacing':f(None,'N5','cm')}]}
d['stirrups']={'mark':f('N4','stirrups'),'vertical_legs_drawn':f(2,'stirrup_shape'),'shape_dimensions':f([14,67],'stirrup_shape','cm'),'length_per_piece':f(177,'stirrup_shape','cm'),'regions':[{'id':'ST1','mark':f('N4','stirrups'),'function':f(None,'stirrups'),'diameter':f(5,'stirrups','mm'),'spacing':f(14,'stirrups','cm'),'quantity':f(21,'stirrups'),'region_length':f(294,'stirrups','cm'),'extent':coord(0,294,'stirrups','Written distribution limits; support detailing not inferred')}]}
d['section_views']=[{'label':f('Corte A','section_A'),'exact_abscissa':f(None,'section_A','cm'),'upper_first_layer_quantity':f(3,'section_A'),'upper_second_layer_quantity':f(1,'section_A'),'upper_positions':f({'first_layer':'N1','second_layer':'N1'},'section_A'),'lower_first_layer_quantity':f(3,'section_A'),'lower_second_layer_quantity':f(3,'section_A'),'lower_position':f(['N2','N3'],'section_A'),'skin_points_per_face':f(3,'section_A'),'skin_position_at_section':f('N5','section_A')}]
for name,box in {'detail':[2470,720,2870,1120],'title':[2480,724,2600,770],'elevation':[2480,786,2760,884],'stirrups':[2490,899,2680,923],'N1':[2474,940,2710,978],'N5':[2480,998,2695,1035],'N3':[2510,1048,2720,1089],'N2':[2470,1068,2720,1115],'section_A':[2780,788,2840,900],'stirrup_shape':[2765,911,2850,1036]}.items():
    d['sources'][name]={'page':1,'bbox_pdf':box,'description':'Manual reading, approximate PDF bbox; V536_V565_hit_0.png'}
def save(name,obj):
    p=OUT/name;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8');return p
p=save('V536_V565_detalhamento_prancha.json',d)
model=transform(d,p.as_posix());model['document_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
pmodel=save('V536_V565_beam_model.json',model)
context={'type':'documented_shared_detail_members','detail_beam_id':'V536', 'evidence':{'drawing_title':{'document':p.as_posix(),'pointer':'/identification/group_members','label':'V536=V565'},'support_association':'Ordered support IDs from each beam TQS; widths 24/120 cm and clear length 294 cm coincide exactly. No A/B suffix heuristic.'},'support_labels':[{'label':'P11A','side':'left','candidates':['P11A','P12B']},{'label':'P7A','side':'right','candidates':['P7A','P8B']}], 'members':[{'beam_id':'V536','support_ids':{'left':'P11A','right':'P7A'}},{'beam_id':'V565','support_ids':{'left':'P12B','right':'P8B'}}]}
pcontext=save('V536_V565_support_context.json',context)
for beam in ('V536','V565'):
    pt=OUT/(beam+'_tqs.json');pp=OUT/(beam+'_tqs_positions.json');pr=OUT/(beam+'_tqs_raw.json')
    t,pos,raw=[json.loads(x.read_text(encoding='utf8')) for x in (pt,pp,pr)]
    mapping=map_beam(model,t,pos,support_context=context)
    mapping['inputs']={role:{'path':x.as_posix(),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for role,x in [('detailing',pmodel),('tqs',pt),('positioned_tqs',pp),('support_context',pcontext)]}
    pm=save(beam+'_beam_mapping.json',mapping)
    scope={**SUPPORTED_SCOPE,'provenance':{'drawing':p.as_posix(),'hypotheses':'Horizontal ribbed positive bars; straight interrupted mark N3; no welds or special compression; no sliding formwork documented; vertical stirrups; Vc0. External N2 bend excluded from check.'}}
    result=check_bar_scaling(model,t,pos,mapping,raw,api,interrupted_mark='N3',cut_side='left',scope=scope)
    result['inputs']={role:{'path':x.as_posix(),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for role,x in [('detailing',pmodel),('tqs',pt),('positioned_tqs',pp),('mapping',pm),('raw',pr),('support_context',pcontext)]}
    result['implementation'] = {str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path('tools/reinforcement_checks/bar_scaling.py'),Path('tools/beam_mapping/support_context.py'),Path('tools/beam_model/consolidar_detalhamento.py'),Path(__file__)]}
    save(beam+'_N3_scaling_check.json',result)
    print(beam,json.dumps({k:result[k] for k in ['event_x_m','d_for_al','remaining_capacity','moment_diagram','shear_for_al','bond_condition','concretopy','condition_A','condition_B','overall','diagnostics']},ensure_ascii=True)[:16000])
