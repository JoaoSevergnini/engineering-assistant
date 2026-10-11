"""Reviewed cotas on supplied form. No graphical coordinate becomes a metre.

Bounding boxes are PDF display coordinates (rotation 90); measurements below
are printed cotas, with explicit arithmetic and reviewed scope.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/beam_model'))
from input_evidence import fact

SOURCE=Path('C:/Users/João Severgnini/Documents/arquivos/051-SJ-EST-EX-010-PLB-TP-R01.pdf')


def build():
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    def proof(value, unit, bbox, text):
        return fact(value,state='DOCUMENTED_CONFIRMED',unit=unit,provenance=[dict(file=str(SOURCE),sha256=digest,
            page=1,page_rotation=90,bbox_display=bbox,text=text,method='printed dimension/label and explicit arithmetic; no graphical scale')])
    def field(value, unit, bbox, text):return dict(documentary_state='PROVED',fact=proof(value,unit,bbox,text))
    forms={}
    for name in ('V610','V611','V623','V626'):
        doc=json.loads((ROOT/'analises/etapa1_leitura_geometria'/(name+'_document_stage1.json')).read_text(encoding='utf-8-sig'))
        cs=doc['physical_extension']['coordinate_system']
        box={'V610':[1480,1420,2650,2050],'V611':[200,760,340,1450],
             'V623':[1710,1100,1840,2030],'V626':[2110,1080,2310,1570]}[name]
        origin={'V610':'Face de P35 voltada a P32; x positivo ao longo da V610 para P33',
                'V611':'Face de P28 voltada a P19 (Y=2115 cm); x=(Y-2115)/100',
                'V623':'Face de P32 voltada a P23 (Y=2007 cm); x=(Y-2007)/100',
                'V626':'Face de P31 voltada a P24 (Y=1994 cm); x=(Y-1994)/100'}[name]
        cs['physical_origin_registration']=proof(origin,None,box,'Origem física explicitada pela forma; extremos históricos das barras continuam não comprovados.')
        # The existing axis contract is reused. Historical graphical bar coordinates
        # remain assumptions and cannot feed numerical resistance.
        form=dict(coordinate_system=cs,provenance=proof(origin,None,box,origin)['provenance'],segments=[],
            segment_inventory_complete=proof(True,None,box,'Região completa da viga na planta e detalhes pertinentes examinados; nós não definidos têm segmentos pendentes próprios.'),
            support_faces=[],transitions=[])
        def add(sid,a,z,h,level=3808,kind='CONSTANT',note='printed section label and cotas'):
            fields=dict(x_start_m=field(a,'m',box,note),x_end_m=field(z,'m',box,note),
                section_shape=field('RECTANGULAR',None,box,'Seção b/h da viga; não reconstrói mesa de laje nem amplia o método resistente.'),
                width_cm=field(19,'cm',box,note),height_cm=field(h,'cm',box,note) if h else dict(documentary_state='ABSENT_IN_DRAWING',
                    review=dict(relevant_region_examined=True,scope=sid+' localização da mudança dentro do apoio',provenance=form['provenance']),
                    clarification='Cotar na forma a posição longitudinal da transição dentro do apoio e indicar seção/níveis de cada lado.'),
                top_level_cm=field(level,'cm',box,note) if level is not None else dict(documentary_state='PRESENT_NOT_EXTRACTED',clarification='Associar explicitamente nível ao trecho.'),
                bottom_level_cm=field(level-h,'cm',box,note) if level is not None and h else dict(documentary_state='NOT_EXAMINED'),
                lateral_offset_cm=dict(documentary_state='PRESENT_NOT_EXTRACTED',clarification='Registrar eixo/offset transversal da viga e faces dos pilares.'))
            form['segments'].append(dict(id=sid,geometry_type=kind,fields=fields))
        def support(sid,lo,hi,axis,text):
            form['support_faces'].append(dict(support_id=sid,x_start_m=proof(lo,'m',box,text),x_end_m=proof(hi,'m',box,text),axis_m=proof(axis,'m',box,text),provenance=form['provenance']))
        if name=='V610':
            add('V610-FORM-STAIR-1',0,1.22,129.5,note='DET ESCADA: primeiro trecho 122 cm, 19/129,5')
            add('V610-FORM-STAIR-2',1.22,2.38,47,note='122+116 cm: região central 19/47 na planta')
            add('V610-FORM-STAIR-3',2.38,3.60,122,3883,note='122+116+122=360 cm; 19/122 D:+75 cm')
            add('V610-P35-NODE',-.19,0,None,level=None,kind='UNRESOLVED')
            add('V610-P32-NODE',3.60,3.79,None,level=None,kind='UNRESOLVED')
            add('V610-FORM-RIGHT',3.79,18.715,None,level=None,kind='UNRESOLVED',
                note='Cota externa total P35–P33 1909,5 cm; origem na face interna P35: face externa P33 em 18,905 m e interna em 18,715 m.')
            form['segments'][-1]['fields']['height_cm']=dict(documentary_state='PRESENT_NOT_EXTRACTED',clarification='Associar explicitamente seção nominal h=47 cm dos LST aos trechos à direita de P32; não usar rótulos das vigas transversais V624/V628 como prova da seção da V610.')
            support('P35',-.19,0,-.095,'P35 19/107; largura longitudinal 19 cm')
            support('P32',3.60,3.79,3.695,'P32 19/125; vão livre P35–P32 360 cm')
            support('V626',11.16,11.35,11.255,'Eixo V626 X=824 cm e P35 X=-311 cm: 1135 cm entre eixos; origem face interna P35 a +9,5 cm do eixo. V626 largura 19 cm; geometria do encontro não prova direção de carga.')
            support('P33',18.715,18.905,18.81,'Cota externa P35–P33 1909,5 cm; ambos com largura longitudinal 19 cm')
            form['transitions']=[dict(x_m=proof(x,'m',box,'DET ESCADA: 122 e 122+116 cm'),position_state='PROVED') for x in (1.22,2.38)]
        elif name=='V611':
            add('V611-FORM-1',0,2.82,57,note='P28–P19: livre 282 cm, seção 19/57')
            add('V611-FORM-2',3.52,6.19,47,note='282+70=352 cm; P19–P10 livre 267 cm, seção 19/47')
            add('V611-FORM-3',6.89,9.31,57,note='352+267+70=689 cm; P10–P1 livre 242 cm, seção 19/57')
            for sid,lo,hi,axis in (('P28',-.7,0,-.35),('P19',2.82,3.52,3.17),('P10',6.19,6.89,6.54),('P1',9.31,10.01,9.66)):
                add('V611-'+sid+'-NODE',lo,hi,None,level=None,kind='UNRESOLVED');support(sid,lo,hi,axis,'Pilar 19/70; faces pela cota longitudinal e coordenada Y impressa')
            form['transitions']=[dict(physical_interval_m=[2.82,3.52],position_state='ABSENT_IN_DRAWING',
                clarification='Cotar a mudança 57→47 dentro de P19.'),dict(physical_interval_m=[6.19,6.89],position_state='ABSENT_IN_DRAWING',clarification='Cotar mudança 47→57 dentro de P10.')]
        elif name=='V623':
            add('V623-FORM-CLEAR',0,3.76,57,note='P32–P23 livre 376 cm; seção 19/57. Coordenadas Y 1944,5 e 2443; faces 62,5 e 60 cm')
            support('P32',-1.25,0,-.625,'P32 19/125; Y=1944,5 cm')
            support('P23',3.76,4.96,4.36,'P23 19/120; Y=2443 cm')
            add('V623-P32-NODE',-1.25,0,None,level=None,kind='UNRESOLVED');add('V623-P23-NODE',3.76,4.96,None,level=None,kind='UNRESOLVED')
        else:
            add('V626-FORM-FREE',-.93,-.80,47,note='P31 80 cm; prolongamento livre após face externa 13 cm: livre -93 a -80 cm em relação à face interna')
            add('V626-P31-NODE',-.80,0,None,level=None,kind='UNRESOLVED')
            add('V626-FORM-CLEAR',0,4.29,57,note='P31–P24: livre 429 cm; seção 19/57; Y=1954 e 2463 cm, pilares 24/80')
            add('V626-P24-NODE',4.29,5.09,None,level=None,kind='UNRESOLVED')
            support('P31',-.80,0,-.40,'P31 24/80; Y=1954 cm');support('P24',4.29,5.09,4.69,'P24 24/80; Y=2463 cm')
            form['spans']=[dict(id=1,tqs_span_token='1B',physical_kind=proof('CANTILEVER',None,box,'Extensão livre abaixo de P31'),
                orientation=proof('LEFT',None,box,'Livre no sentido negativo do eixo comum'),physical_bounds=dict(x_start_m=proof(-.93,'m',box,'80+13 cm'),x_end_m=proof(-.4,'m',box,'Eixo P31 a -40 cm')),provenance=form['provenance'])]
            form['transitions']=[dict(physical_interval_m=[-.80,0],position_state='ABSENT_IN_DRAWING',clarification='Cotar mudança 47→57 na região de P31; forma de seção variável não localizada.')]
        forms[name]=form
        (OUT/(name+'_form_reviewed.json')).write_text(json.dumps(form,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return forms


if __name__=='__main__':build()
