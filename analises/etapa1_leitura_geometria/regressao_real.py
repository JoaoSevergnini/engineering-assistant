"""Reproducible real-case migration, outputs exclusively in this stage directory.

Original reviews and PDFs are read-only. Graphical coordinates stay assumptions.
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
for part in ('beam_model','extrator_lst','reinforcement_checks'):
    sys.path.insert(0,str(ROOT/'tools'/part))
from input_evidence import fact
from consolidar_detalhamento import transform
from extrair_viga_lst import extract
from consolidar_viga import consolidate
from input_preflight import preflight,EXTERNAL_DEPENDENCIES

CASE=ROOT/'analises/silva_jardim_tipo'
TQS=Path(r'C:\TQS\TGD - SILVA JARDIM\24-212-TGD-SILVA JARDIM-R35\TIPO\VIGAS')
PDFS=Path(r'S:\PROJETOS EM EXECUÇÃO\24-212-TGD-SILVA JARDIM-POA-RS\APOIO\JOÃO\TIPO')

def write(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def evidence(value, unit=None, state='DOCUMENTED_CONFIRMED', provenance=None):
    return fact(value,state=state,unit=unit,provenance=provenance or [{'case':'Silva Jardim','reference':'documentary interpretation'}])

def migrate():
    inventory=json.loads((CASE/'drawing_inventory.json').read_text(encoding='utf-8-sig'))
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [CASE/'drawing_inventory.json',CASE/'operational_tqs.json']}
    cases={}
    for name in ('V606','V610','V611','V623','V626'):
        drawing=inventory[name]
        observations=[];bars=[]
        for b in drawing['bars']:
            identity=name+'-'+b['mark']+'-'+str(b['instance'])
            source={'file':drawing['pdf'],'page':1,'bbox':b['source']['label']['bbox'],'text':b['source']['label']['text'],
                    'inventory':str((CASE/'drawing_inventory.json').relative_to(ROOT)),'inventory_sha256':hashes['analises/silva_jardim_tipo/drawing_inventory.json'],'instance':b['instance']}
            observations.append(dict(mark=b['mark'],representation_id=identity,view='ELEVATION',quantity=b['bars'],quantity_scope='OCCURRENCE',occurrence_id=identity,
                                     diameter_mm=b['diameter_mm'],nominal_length_cm=b.get('total_length_cm'),provenance=[source]))
            graphics={'reference':'historical graphical trace','original':b['source'],'warning':'not substituted for explicit dimensions'}
            bars.append(dict(mark=b['mark'],occurrence_id=identity,function=b['function'],face=b['face'],
                             quantity=evidence(b['bars'],provenance=[source]),diameter_mm=evidence(b['diameter_mm'],'mm',provenance=[source]),
                             layers=evidence(b['layers'],state='ENGINEERING_ASSUMPTION',provenance=[{'reference':'historical manual layer interpretation; section association requires confirmation','original':b['source']['layers']}]),
                             x_start_m=evidence(b['x_start_common'],'m','ENGINEERING_ASSUMPTION',[graphics]),x_end_m=evidence(b['x_end_common'],'m','ENGINEERING_ASSUMPTION',[graphics]),
                             provenance=[source],nominal_length_cm=b.get('total_length_cm')))
        coverage=[dict(view=v,extraction='PARTIAL' if v=='ELEVATION' else 'NOT_EXTRACTED',integrity='UNVERIFIED',provenance=[dict(file=drawing['pdf'],page=1,bbox=drawing['bbox'])]) for v in ('ELEVATION','SECTION','STEEL_SCHEDULE')]
        if name=='V623':
            # Direct table row observed in original PDF, independently of old inventory.
            pdf=PDFS/drawing['pdf']; pdfsha=hashlib.sha256(pdf.read_bytes()).hexdigest()
            observations.append(dict(mark='N2',representation_id='V623-N2-SCHEDULE',view='STEEL_SCHEDULE',quantity=4,quantity_scope='POSITION_TOTAL',diameter_mm=16,nominal_length_cm=464,
                                     provenance=[dict(file=str(pdf),sha256=pdfsha,page=1,bbox=[2370,250,2575,262],text='2 16 4 464 1856',reference='row read from PDF')]))
            observations.append(dict(mark='N2',representation_id='V623-N2-SECTION-A',view='SECTION',quantity=4,quantity_scope='SECTION_COUNT',section_id='A',
                                     provenance=[dict(file=str(pdf),sha256=pdfsha,page=1,bbox=[1480,110,1520,175],reference='four lower points in Corte A; association N2 confirmed by user in stage request')]))
            coverage[0].update(integrity='TRUNCATED',marks=['N2'],affected_scope='N2 lower elevation/longitudinal extent',
                               unverifiable=['x_start','x_end','cuts','extensions','laps','longitudinal layers'],
                               provenance=[dict(reference='User stage-1 request',text='elevação da V623 foi cortada na plotagem do PDF')])
            bars.append(dict(mark='N2',occurrence_id='V623-N2-UNLOCATED',function='positive',face='lower',quantity=evidence(4,provenance=observations[-2]['provenance']),
                             diameter_mm=evidence(16,'mm',provenance=observations[-2]['provenance']),layers=fact(),x_start_m=fact(unit='m'),x_end_m=fact(unit='m'),provenance=observations[-2]['provenance'],nominal_length_cm=464))
        heights={'V606':[37],'V610':[129.5,47,122],'V611':[57,47],'V623':[57],'V626':[47,57]}[name]
        # Only known local heights are retained. Their boundaries are NOT manufactured.
        segments=[]
        for i,h in enumerate(heights):
            segments.append(dict(id=name+'-G'+str(i+1),geometry_type='CONSTANT' if len(heights)==1 else 'UNRESOLVED',
                                 x_start_m=fact(unit='m'),x_end_m=fact(unit='m'),
                                 geometry=dict(section_shape=evidence('RECTANGULAR',provenance=[dict(file=drawing['pdf'],page=1,bbox=drawing['bbox'],reference='rectangular elevation/section views')]),width_cm=evidence(14 if name=='V606' else 19,'cm',provenance=[{'file':drawing['pdf'],'page':1,'bbox':drawing['bbox'],'reference':'section label / prior visual review'}]),
                                               height_cm=evidence(h,'cm',state='DOCUMENTED_CONFIRMED' if len(heights)==1 else 'ENGINEERING_ASSUMPTION',provenance=[{'file':drawing['pdf'],'page':1,'bbox':drawing['bbox'],'reference':'local section noted in prior review; explicit boundaries pending'}])),
                                 provenance=[dict(file=drawing['pdf'],page=1,bbox=drawing['bbox'])]))
        raw=extract(TQS,name)
        cons=consolidate(raw)
        # Preserve the TQS envelope chain; no combination reconstruction.
        tqs_spans=[dict(id=s['id'],tqs_span_token=token,provenance=cons['provenance'].get('/beam/spans/'+str(j)+'/documentary_span_kind',[]))
                   for j,s in enumerate(cons['beam']['spans']) for token in s.get('original_span_tokens',[])]
        if name == 'V626':
            for span in tqs_spans:
                if span['tqs_span_token'] == '1B':
                    span['physical_kind'] = evidence('CANTILEVER',provenance=[dict(file=drawing['pdf'],page=1,bbox=drawing['bbox'],reference='free extension left of P31 in elevation')])
                    span['orientation'] = evidence('LEFT',provenance=[dict(file=drawing['pdf'],page=1,bbox=drawing['bbox'],reference='visual side relative to P31; no length from scale')])
        ext=dict(schema_version='1.0',coordinate_system=dict(unit='m',origin='historical drawing left face; registration to TQS remains pending',positive_direction='right',provenance=[{'inventory_sha256':hashes['analises/silva_jardim_tipo/drawing_inventory.json']}]),segments=segments,occurrences=bars,observations=observations,coverage=coverage,spans=tqs_spans)
        doc=dict(type='beam_reinforcement_drawing_interpretation',schema_version='1.3',identification=dict(beam=name,grouped_with_other_beams=False),
                 geometry=dict(coordinate_system=dict(unit='cm',origin='drawing left face',positive_direction='right')),section={},longitudinal_reinforcement={},physical_extension=ext)
        m=transform(doc,name+'_document_stage1.json')
        domain=[min([b['x_start_common'] for b in drawing['bars']]+[0]),max(b['x_end_common'] for b in drawing['bars'])]
        plans=[preflight(m,region_id=name+'-DOCUMENTARY-DOMAIN',interval_m=domain,control=c,inputs={}) for c in EXTERNAL_DEPENDENCIES]
        cases[name]=dict(beam=name,fixture_kind='REAL_DOCUMENTS_WITH_EXPLICIT_UNRESOLVED_GEOMETRY',prior_bar_occurrences=len(drawing['bars']),current_bar_occurrences=len(bars),
                         plotting_integrity_issue=name=='V623',observed_heights_cm=heights,
                         documentary_cantilevers=[s['tqs_span_token'] for s in m['physical_geometry']['spans'] if s['documentary_kind']=='CANTILEVER'],
                         numerical_recalculation=False,physical_regions_certified=False,input_validation=plans)
        write(name+'_document_stage1.json',doc);write(name+'_model_stage1.json',m);write(name+'_tqs_stage1.json',cons)
    # Actual B rows from all beams and original exact tokens/lines.
    balances=[]
    for name in ('V617','V620','V622','V625','V626','V627','V629'):
        raw=extract(TQS,name)
        records=raw['categorias']['geometria']
        for r in records:
            d=r.get('normalizacao') or {}
            if d.get('tipo_vao_documental')=='CANTILEVER':
                balances.append(dict(beam=name,token=d['identificador_vao_original'],normalization=d,provenance=r['origem'],
                    physical_kind=evidence('CANTILEVER',provenance=[dict(file=inventory[name]['pdf'],page=1,bbox=inventory[name]['bbox'],reference='free extension verified in elevation')]),
                    orientation=evidence('LEFT' if name=='V626' else 'RIGHT',provenance=[dict(file=inventory[name]['pdf'],page=1,bbox=inventory[name]['bbox'],reference='visual side; no coordinate derived from scale')]),
                    physical_bounds_state='MISSING'))
    write('balancos_reais.json',balances)
    write('comparativo_real.json',cases)
    for name,sha in hashes.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise RuntimeError('historical input modified')
    write('historical_inputs_preserved.json',hashes)
    print(json.dumps(dict(cases=list(cases),real_cantilevers=len(balances),historical_inputs_unchanged=True)))

if __name__=='__main__':migrate()

