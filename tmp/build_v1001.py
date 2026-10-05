import json, hashlib, sys
from pathlib import Path
sys.path.insert(0, 'tmp/pdf_deps')
import pymupdf as fitz
OUT=Path('analises/pranchas')
PDF=Path(r'C:\Users\João Severgnini\Desktop\corrigir em casa\corrigir em casa\10 - CASA DE MAQUINAS - RESIDENCIAL\VIGAS\RMP-EST-LO-1376-VIG-R00.PDF')
def f(v, c='explicit', s='detail', unit=None, reason=None):
    d=dict(value=v, classification=c, sources=[s])
    if unit:d['unit']=unit
    if reason:d['reason']=reason
    return d
def coord(a,b,s,reason):return f(dict(x_start=a,x_end=b),'graphically_interpreted',s,'cm',reason)
d=dict(schema_version='1.2',type='beam_reinforcement_drawing_interpretation')
d['scope']=dict(beam='V1001',method='Leitura visual manual do PDF renderizado e texto auxiliar; não existe parser automático de desenho.',structural_checks_performed=False,tqs_results_used=False,document_instructions='Notas e remissões são conteúdo documental, não instruções do usuário.')
d['document']=dict(name=PDF.name,page=1,sha256=hashlib.sha256(PDF.read_bytes()).hexdigest(),page_size_pdf_points=[3402,1684],bbox_convention='Pontos PDF, origem superior esquerda; caixas aproximadas.')
d['identification']=dict(beam=f('V1001',s='title'),grouped_with_other_beams=f(None,'uncertain','title',reason='Título somente V1001, mas apoios P2A/P2B e P1A/P1B. Não presumir agrupamento nem multiplicidade.'))
d['section']=dict(written_label=f('19/72',s='title'),width=f(19,'graphically_interpreted','title','cm'),height=f(72,'graphically_interpreted','title','cm'),shape=f('rectangular','graphically_interpreted','section_A'),local_cover=f(None,'uncertain','section_A','cm','Sem cota local; detalhe geral será tratado separadamente.'),lateral_projections_dimensions=f([], 'graphically_interpreted','section_A',reason='Corte retangular sem projeções desenhadas.'))
d['geometry']=dict(coordinate_system=dict(origin='face interna do apoio esquerdo P2A/P2B',positive_direction='para a direita',unit='cm',type='derived_from_drawing_dimensions'),support_order=f(['P2A/P2B','P1A/P1B'],'graphically_interpreted','elevation'),supports=[],spans_and_overhang=[])
for name,w,a,b in [('P2A/P2B',120,-120,0),('P1A/P1B',142,712,854)]:
    d['geometry']['supports'].append(dict(id=f(name,s='elevation'),width_along_beam=f(w,s='elevation',unit='cm'),faces_coordinates=f(dict(left=a,right=b),'graphically_interpreted','elevation','cm','Derivação pelas faces internas e larguras escritas.'),model_restraint=f(None,'uncertain','elevation',reason='Não inferido vínculo do modelo.')))
d['geometry']['spans_and_overhang']=[dict(id='S1',type=f('between_supports','graphically_interpreted','elevation'),left_support='P2A/P2B',right_support='P1A/P1B',dimension_on_stirrup_line=f(712,s='stirrups',unit='cm'),geometric_length=f(712,'graphically_interpreted','stirrups','cm','Limites da distribuição coincidem com faces internas.'),extent=coord(0,712,'stirrups','Origem na face esquerda; comprimento cotado 712.'),section_label=f('19/72',s='title'))]
d['longitudinal_reinforcement']={'negative':[],'positive':[]}
bars=[('N1',2,12.5,195,[1,1],-48,147,'negative','início=-48; fim=-48+195'),('N2',2,12.5,300,[2],-48,252,'negative','início=-48; fim=-48+300'),('N4',2,16,225,[2],214,439,'negative','início=214; fim=214+225'),('N7',3,16,375,[3],399,774,'negative','fim=712+62; início=774-375'),('N8',3,16,235,[0,3],540,775,'negative','fim=712+63; início=775-235'),('N3',2,10,650,[2],-42,608,'positive','início=-42; fim=-42+650'),('N5',2,10,795,[2],-42,753,'positive','fim=712+41; início=753-795')]
for mark,n,diam,length,layers,a,b,group,reason in bars:
    item=dict(mark=f(mark,s=mark),quantity=f(n,s=mark),diameter=f(diam,s=mark,unit='mm'),length_per_bar=f(length,s=mark,unit='cm'),face=f('upper' if group=='negative' else 'lower','graphically_interpreted',mark),group=f(group,'graphically_interpreted',mark,reason='Posição gráfica; não atribui sinal de esforço.'),shape=f('straight','graphically_interpreted',mark),horizontal_length_shown=f(None,'uncertain',mark,'cm','Comprimento total escrito em barra reta; sem cota horizontal separada.'),longitudinal_coordinates=coord(a,b,mark,reason),layers=[])
    for i,q in enumerate(layers):
        item['layers'].append(dict(layer=i+1,quantity=f(q,'explicit' if mark in ['N1','N8'] and i==1 else 'interpreted_by_office_standard',mark,reason='Chamada de segunda camada e saldo na primeira; ausência de chamada adicional conforme convenção item 4.')))
    d['longitudinal_reinforcement'][group].append(item)
d['skin_reinforcement']=dict(skin_reinforcement_detailed=f(True,'explicit','N6'),positions=[dict(mark=f('N6',s='N6'),bars_per_face=f(3,s='N6'),total_quantity_per_position=f(6,'graphically_interpreted','N6',reason='2 x 3 = 6'),diameter=f(10,s='N6',unit='mm'),length_per_bar=f(794,s='N6',unit='cm'),shape=f('straight','graphically_interpreted','N6'),longitudinal_coordinates=coord(-24,770,'N6','início=-24; fim=-24+794'),vertical_spacing=f(None,'uncertain','N6','cm','Não cotado.'))])
d['stirrups']=dict(mark=f('N9',s='stirrups'),vertical_legs_drawn=f(2,'graphically_interpreted','stirrups'),shape_dimensions=f([14,67],s='stirrups',unit='cm'),length_per_piece=f(177,s='stirrups',unit='cm'),regions=[dict(id='ST1',mark=f('N9',s='stirrups'),function=f(None,'uncertain','stirrups',reason='Distribuição geral; função resistente não escrita.'),diameter=f(5,s='stirrups',unit='mm'),spacing=f(14,s='stirrups',unit='cm'),quantity=f(51,s='stirrups'),region_length=f(712,s='stirrups',unit='cm'),extent=coord(0,712,'stirrups','Limites cotados da distribuição, sem fixar primeiro/último estribo.'))])
d['anchorage_staples']=dict(anchorage_staples_detailed=f(False,'interpreted_by_office_standard','detail',reason='Sem forma ou chamada específica de grampo; convenção item 7.'),positions=[])
d['indirect_supported_beams']=[]
for i,desc in [(1,'No interior do vão, à esquerda de A-A'),(2,'No interior do vão, à direita de A-A, próximo do apoio direito')]:
    d['indirect_supported_beams'].append(dict(id='IB'+str(i),supported_beam_exists=f(True,'interpreted_by_office_standard','elevation',reason='Contorno retangular tracejado; convenção item 8.'),supported_beam_name=f(None,'uncertain','elevation',reason='Nome não escrito; não associado automaticamente ao TQS.'),receiving_beam='V1001',span='S1',position_description=f(desc,'graphically_interpreted','elevation'),exact_longitudinal_position=f(None,'uncertain','elevation','cm','Sem abscissa cotada.'),suspension_reinforcement_detailed=f(False,'interpreted_by_office_standard','stirrups',reason='Sem concentração/chamada específica no contorno; item 9. Não avalia necessidade.'),suspension_required_or_sufficient=f(None,'uncertain','elevation',reason='Não verificado numericamente.')))
d['section_views']=[dict(label=f('Corte A',s='section_A'),exact_abscissa=f(None,'uncertain','elevation','cm','Não cotada.'),upper_first_layer_quantity=f(2,'graphically_interpreted','section_A'),upper_second_layer_quantity=f(0,'graphically_interpreted','section_A'),upper_positions=f(dict(first_layer='N4',second_layer=None),'graphically_interpreted','section_A',reason='Associação pela região de A-A; sem rótulos nos pontos.'),lower_first_layer_quantity=f(4,'graphically_interpreted','section_A'),lower_position=f(['N3','N5'],'graphically_interpreted','section_A',reason='Quatro pontos; duas posições sobrepostas nesta região.'),skin_points_per_face=f(3,'graphically_interpreted','section_A'),skin_position_at_section=f('N6','graphically_interpreted','section_A'))]
d['uncertainties']=['Título singular e apoios com nomes duplos: confirmar abrangência do detalhamento.', 'Nomes/abscissas dos apoios indiretos e abscissa de A-A desconhecidos.', 'Cobrimento local e espaçamento vertical de pele não cotados.', 'Barras geométricas presentes não significam barras efetivamente ancoradas.']
d['sources']={}
boxes={'title':[105,65,260,100],'elevation':[100,120,685,205],'detail':[95,65,790,515],'stirrups':[130,245,660,276],'section_A':[710,130,765,258],'N1':[125,310,325,350],'N2':[125,280,385,315],'N4':[130,265,440,298],'N7':[390,280,625,315],'N8':[465,320,625,353],'N6':[135,360,625,403],'N3':[125,415,530,451],'N5':[125,450,625,490]}
for k,b in boxes.items():d['sources'][k]=dict(page=1,bbox_pdf=b,description='Ver recorte V1001_recorte.png; leitura manual da região '+k)
d['sources']['stirrup_shape']=dict(page=1,bbox_pdf=[705,335,790,425],description='Forma N9: 14 x 67, C=177, 51 peças; dois ramos verticais.')
d['stirrups']['vertical_legs_drawn']['sources']=['stirrup_shape']
d['stirrups']['shape_dimensions']['sources']=['stirrup_shape']
d['stirrups']['length_per_piece']['sources']=['stirrup_shape']
(OUT/'V1001_detalhamento_prancha.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
p=fitz.open(PDF)
p[0].get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(708,130,770,260)).save(str(OUT/'V1001_corte_A.png'))
print('Documental criado: 7 posições longitudinais, 1 pele, 1 região transversal, 2 apoios indiretos.')
