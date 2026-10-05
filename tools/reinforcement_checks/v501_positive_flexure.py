"""Golden case V501/N5: orquestração auditável, sem equações resistentes."""
import argparse
import copy
from dataclasses import asdict
import hashlib
import importlib
import inspect
import json
import math
from pathlib import Path
import sys
from materials import interpret_steel, documented_fields
from tqs_moments import audited_moment_series


def positive_demand(mapping, tqs, raw, bar):
    index, series, proofs = audited_moment_series(mapping, tqs, raw)
    points = []
    for section, x, value in zip(series['sections'],series['positions'],series['values']):
        if section in bar['covered_tqs_sections']:
            if value is None or not math.isfinite(value):
                raise ValueError('Solicitação ausente na região analisada.')
            points.append({'section':section,'x':x,'value':value,'eligible_positive':value>0})
    positive = [p for p in points if p['eligible_positive']]
    if not positive:
        raise ValueError('Sem momento positivo na região; nenhum negativo pode governar.')
    governing = max(positive,key=lambda p:p['value'])
    point = next(p for p in bar['covered_tqs_points'] if p['section']==governing['section'])
    force = next(f for f in point['forces'] if f['provenance']['series_pointer']==f'/beam/spans/0/internal_forces/{index}')
    return {**governing,'type':'Msk_positive','unit':series['unit'],
            'source_series':copy.deepcopy(series),'provenance':copy.deepcopy(force['provenance']),
            'series_evidence':proofs,'characteristic_level_source':'Instrução explícita de João nesta etapa: solicitações TQS deste fluxo são Msk.'}, points


def check_case(detail, tqs, positioned, mapping, raw, api):
    if mapping['beam_id'] != 'V501' or tqs['beam']['id'] != 'V501' or positioned['beam']['id'] != 'V501' or len(tqs['beam']['spans']) != 1:
        raise ValueError('Golden case exclusivo V501/N5, vão único.')
    bars = [b for b in mapping['reinforcement'] if b['mark']=='N5']
    original = [b for b in detail['longitudinal_reinforcement'] if b['mark']=='N5']
    if len(bars)!=1 or len(original)!=1:
        raise ValueError('N5 ausente/ambígua.')
    bar = bars[0]
    for key in original[0]:
        if bar.get(key)!=original[0][key]:
            raise ValueError('N5 no mapping difere do beam_model.')
    if bar['function']!='positive' or bar['face']!='lower' or bar['bars']!=4 or bar['diameter_mm']!=12.5 or bar['layers']!=[3,1]:
        raise ValueError('Composição documental diverge do golden N5.')
    if bar['covered_tqs_sections']!=list(range(1,14)):
        raise ValueError('Golden requer N5 atravessando as 13 seções; não infere efetividade parcial.')
    if mapping['force_series']!=positioned['beam']['spans'][0]['internal_forces']:
        raise ValueError('Mapping diverge do modelo posicionado.')
    result = {'schema_version':'1.0','model_type':'positive_flexure_golden_check', 'beam':'V501',
              'span':tqs['beam']['spans'][0]['id'],'check':'positive_flexure','status':'blocked',
              'reinforcement':copy.deepcopy(bar),
              'region':{'x_start':bar['x_start_common'],'x_end':bar['x_end_common'],'unit':'m'},
              'governing_demand':None,'considered_points':[], 'capacity':None,'concretopy_result':None,
              'comparison':{'utilization':None,'capacity_sufficient':None}, 'blockers':[],
              'diagnostics':{'model_assumptions_valid':None,'ductility':None,'minimum_reinforcement':None,
                             'anchorage_checked':False,'reinforcement_development_checked':False,
                             'geometry_comparison':copy.deepcopy(mapping['geometry'])},
              'provenance':{'geometry':copy.deepcopy(detail['section']), 'N5':copy.deepcopy(bar['source']),
                            'interval':copy.deepcopy(bar['mapping_provenance']), 'tqs_source_catalog':copy.deepcopy(tqs['sources'])}}
    try:
        demand,points = positive_demand(mapping,tqs,raw,bar)
        result.update(governing_demand=demand,considered_points=points)
    except ValueError as error:
        result['blockers'].append({'code':'unresolved_demand_series','detail':str(error)})
    fck,fck_evidence = documented_fields(raw,'fck','MPa')
    gamma_f,gamma_evidence = documented_fields(raw,'gamaf')
    cover = tqs['beam']['cover'].get('bottom')
    if detail['section'].get('cover_cm') is not None:
        cover_cm=detail['section']['cover_cm']
        cover_evidence={'input':'beam_model','pointer':'/section/cover_cm'}
    else:
        cover_cm=cover*100 if cover is not None else None
        cover_evidence={'input':'tqs','pointer':'/beam/cover/bottom','sources':tqs['provenance'].get('/beam/cover/bottom',[]),
                        'interpretation':'cobrimento inferior do modelo TQS; não confirmação do cobrimento executado/documental PDF'}
    demand=result['governing_demand']
    stirrups=[r for r in mapping['stirrup_regions'] if demand and r['x_start_common'] is not None and r['x_start_common']<=demand['x']<=r['x_end_common']]
    diameter=stirrups[0]['diameter_mm'] if len(stirrups)==1 else None
    signature=inspect.signature(api.verificar_flexao_viga_retangular)
    coefficients={k:signature.parameters[k].default for k in ('gamma_c','gamma_s')}
    steel = interpret_steel(raw)
    fyk = steel['derived_fyk_mpa']
    result['material_interpretation'] = steel
    if steel['status'] != 'consistent':
        result['blockers'].append({'code':'unresolved_steel','detail':'Interpretação de aço bloqueada: '+steel['status']})
    call={'geometry':{'bw':detail['section'].get('width_cm'),'h':detail['section'].get('height_cm'),
                      'cobrimento':cover_cm,'diametro_estribo_mm':diameter,'unit':'cm (diâmetro em mm)'},
          'materials':{'fck_mpa':fck,'fyk_mpa':fyk,'Es_mpa':inspect.signature(api.Aco).parameters['es'].default},
          'layers':[{'numero_barras':n,'diametro_mm':bar['diameter_mm'],'d_cm':None} for n in bar['layers']],
          'coefficients':{**coefficients,'gamma_f':gamma_f},'verificar_armadura_minima':False,
          'scope':'seção governante; estribo da região que contém esse ponto; não certifica todas as regiões com estribos distintos'}
    result['concretopy_call']={**call,'executed':False}
    result['provenance'].update(fck=fck_evidence,fyk=copy.deepcopy(steel),gamma_f=gamma_evidence,cover=cover_evidence,
                                stirrup_at_governing=copy.deepcopy(stirrups),
                                steel_conflicts=[w for w in tqs['warnings'] if w.get('path')=='/beam/materials/steel/grade'],
                                concretopy={'interface':api.verificar_flexao_viga_retangular.__module__+'.verificar_flexao_viga_retangular',
                                            'signature':str(signature),'module_file':str(Path(inspect.getfile(api.verificar_flexao_viga_retangular)).resolve()),
                                            'defaults_used':['gamma_c','gamma_s','Aco.es'], 'gamma_f_default':None})
    for name,value in {'bw':call['geometry']['bw'],'h':call['geometry']['h'],'fck':fck,'fyk':fyk,'cover':cover_cm,'stirrup_diameter':diameter,'gamma_f':gamma_f}.items():
        if value is None:
            result['blockers'].append({'code':'missing_'+name,'detail':'Dado necessário sem definição documental inequívoca: '+name})
    if result['blockers']:
        return result
    try:
        response=api.verificar_flexao_viga_retangular(
            api.SecaoRetangular(call['geometry']['bw'],call['geometry']['h'],cover_cm,diameter),
            api.Concreto(fck),api.Aco(fyk),
            [api.CamadaArmaduraLongitudinal(c['numero_barras'],api.Barra(c['diametro_mm'])) for c in call['layers']],
            gamma_f=gamma_f, verificar_armadura_minima=False)
    except (ValueError,TypeError) as error:
        result['blockers'].append({'code':'concretopy_rejected_input','detail':str(error)})
        return result
    full=asdict(response)
    result['concretopy_call']['executed']=True
    result['concretopy_result']=full
    result['capacity']={'MRd':None if response.mrd_kncm is None else response.mrd_kncm/100,
                        'Mk_equivalent':None if response.mk_equivalente_kncm is None else response.mk_equivalente_kncm/100,'unit':'kN.m'}
    result['diagnostics'].update(model_assumptions_valid=response.hipoteses_validas,ductility=response.ductilidade_atendida,minimum_reinforcement=response.armadura_minima_atendida)
    mk=result['capacity']['Mk_equivalent']
    if response.hipoteses_validas and mk is not None and mk>0:
        result['comparison']={'utilization':demand['value']/mk,'capacity_sufficient':mk>=demand['value']}
        result['status']='completed_at_governing_section'
    else:
        result['blockers'].append({'code':'invalid_capacity','detail':'Concretopy não disponibilizou capacidade válida para comparação.'})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--concretopy-root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    root=Path(__file__).resolve().parents[2]
    names=['V501_V503_beam_model.json','V501_tqs.json','V501_tqs_positions.json','V501_beam_mapping.json','V501_tqs_raw.json']
    paths=[root/'analises/pranchas'/n for n in names]
    if any(args.output.resolve()==f.resolve() for f in paths):
        p.error('Saída não pode sobrescrever entrada.')
    sys.path.insert(0,str(args.concretopy_root.resolve()))
    api=importlib.import_module('concretopy')
    if not Path(api.__file__).resolve().is_relative_to(args.concretopy_root.resolve()):
        p.error('Concretopy importado fora do repositório explicitado.')
    data=[json.loads(f.read_text(encoding='utf8')) for f in paths]
    for entry in data[3]['inputs'].values():
        if hashlib.sha256((root/entry['path']).read_bytes()).hexdigest()!=entry['sha256']:
            p.error('Mapping desatualizado: hash da entrada diverge.')
    if hashlib.sha256(paths[4].read_bytes()).hexdigest()!=data[1]['raw_document']['sha256']:
        p.error('Raw diverge do hash consolidado.')
    out=check_case(*data,api)
    out['inputs']={f.name:{'path':str(f.resolve()),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in paths}
    out['provenance']['material_interpreter']={'file':str(Path(__file__).with_name('materials.py').resolve()),
        'sha256':hashlib.sha256(Path(__file__).with_name('materials.py').read_bytes()).hexdigest()}
    implementation=Path(inspect.getfile(api.verificar_flexao_viga_retangular))
    out['provenance']['concretopy']['implementation_sha256']=hashlib.sha256(implementation.read_bytes()).hexdigest()
    out['provenance']['concretopy']['pyproject_sha256']=hashlib.sha256((args.concretopy_root/'pyproject.toml').read_bytes()).hexdigest()
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(out['status'],out['comparison'],[b['code'] for b in out['blockers']])


if __name__=='__main__':
    main()
