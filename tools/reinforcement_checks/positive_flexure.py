"""Flexão positiva por regiões geométricas; apenas orquestra a API Concretopy."""
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

from flexure_regions import decompose_regions, contains, decimal
from materials import interpret_steel, documented_fields
from tqs_moments import audited_moment_series


def implementation_provenance(api):
    path=Path(inspect.getfile(api.verificar_flexao_viga_retangular)).resolve()
    return {'interface':api.verificar_flexao_viga_retangular.__module__+'.verificar_flexao_viga_retangular',
            'signature':str(inspect.signature(api.verificar_flexao_viga_retangular)),
            'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'version_metadata':{'file':str(path.parents[2]/'pyproject.toml'),
                                'sha256':hashlib.sha256((path.parents[2]/'pyproject.toml').read_bytes()).hexdigest()}}


def check_positive_flexure(detail,tqs,positioned,mapping,raw,api,*,transverse_regions=None):
    """Um vão físico mapeado; vários intervalos/marcas e configurações transversais.

    transverse_regions opcional é dado explícito/proveniente do chamador, não
    inferência de cortes ou forma alternativa de completar dado desconhecido.
    """
    beam=tqs['beam']['id']
    if mapping['beam_id']!=beam or positioned['beam']['id']!=beam or beam not in detail['beam'].get('ids',[detail['beam']['id']]):
        raise ValueError('Identidades dos modelos incompatíveis.')
    if len(tqs['beam']['spans'])!=1 or len(detail['spans'])!=1 or detail.get('overhangs'):
        raise ValueError('Esta integração requer um vão físico mapeado sem balanços.')
    if tqs['units']['length']!='m' or positioned['units']['length']!='m' or mapping['coordinate_system']!={'origin':'left_support_axis','positive_direction':'left_to_right','unit':'m'}:
        raise ValueError('Sistema comum incompatível.')
    if detail['section'].get('shape')!='rectangular':
        raise ValueError('Seção não retangular fora do contrato atual.')
    if mapping['force_series']!=positioned['beam']['spans'][0]['internal_forces'] or tqs.get('raw_document')!=positioned.get('raw_document'):
        raise ValueError('Mapping/posicionado/origem raw incompatíveis.')
    for b in mapping['reinforcement']:
        originals=[d for d in detail['longitudinal_reinforcement'] if d['mark']==b['mark']]
        if len(originals)!=1 or any(b.get(k)!=v for k,v in originals[0].items()):
            raise ValueError('Armadura mapeada diverge do beam_model.')
    if {b['mark'] for b in mapping['reinforcement']}!={b['mark'] for b in detail['longitudinal_reinforcement']}:
        raise ValueError('Mapping omitiu marcas do detalhamento.')
    bars=[b for b in mapping['reinforcement'] if b.get('function') not in ('negative','skin','anchorage_staple')]
    # null/unknown são candidatos não classificados e bloqueiam sua composição.
    steel=interpret_steel(raw)
    fck,fp=documented_fields(raw,'fck','MPa'); gamma_f,gp=documented_fields(raw,'gamaf')
    cover_cm=detail['section'].get('cover_cm')
    cover_source={'input':'beam_model','pointer':'/section/cover_cm'}
    if cover_cm is None:
        value=tqs['beam']['cover'].get('bottom')
        cover_cm=float(decimal(value)*100) if value is not None else None
        cover_source={'input':'tqs','pointer':'/beam/cover/bottom','sources':tqs['provenance'].get('/beam/cover/bottom',[]),
                      'interpretation':'Dado do modelo, não confirmação do cobrimento PDF/executado.'}
    base={'bw_cm':detail['section'].get('width_cm'),'h_cm':detail['section'].get('height_cm'),'cover_cm':cover_cm}
    geometry_issues=[]
    for dkey,tkey in (('bw_cm','width'),('h_cm','height')):
        value=tqs['beam']['spans'][0]['geometry'].get(tkey)
        if value is not None and base[dkey] is not None and decimal(value)*100!=decimal(base[dkey]):
            geometry_issues.append('section_geometry_mismatch:'+dkey)
    if transverse_regions is None:
        transverse_regions=[{**base,'stirrup_diameter_mm':s.get('diameter_mm'),
                             'x_start_common':s.get('x_start_common'),'x_end_common':s.get('x_end_common'),
                             'provenance':{'geometry':copy.deepcopy(detail['section']),'cover':copy.deepcopy(cover_source),
                                           'stirrup':{'id':s.get('id'),'mark':s['mark'],'source':copy.deepcopy(s.get('source')),
                                                      'mapping':copy.deepcopy(s.get('mapping_provenance'))}}} for s in mapping['stirrup_regions']]
    elif any(not r.get('provenance') for r in transverse_regions):
        raise ValueError('Configuração transversal explícita requer proveniência.')
    domain=(mapping['supports']['left']['axis_x'],mapping['supports']['right']['axis_x'])
    regions=decompose_regions(bars,domain,transverse_regions)
    moment=None;series_issue=None
    try:
        index,moment,proofs=audited_moment_series(mapping,tqs,raw)
        if moment['sections']!=list(range(1,14)) or len(moment['values'])!=13 or len(moment.get('positions') or [])!=13:
            raise ValueError('Esperadas 13 seções/positions/valores existentes.')
        source_series={k:copy.deepcopy(v) for k,v in moment.items() if k not in ('values','positions','sections')}
        source_series['label_original']='M MX.'
        source_series['provenance']={'input':'positioned_tqs','pointer':f'/beam/spans/0/internal_forces/{index}',
                                    'evidence':[{'reference':p['reference'],'source':p['source'],'record_text':p['record']['origem']['texto'],
                                                 'label_original':p['record']['normalizacao']['grandeza_original']} for p in proofs],
                                    'characteristic_level':'Msk confirmado pelo engenheiro neste fluxo'}
    except (ValueError,KeyError,TypeError) as error:
        moment=None;source_series=None;series_issue=str(error)
    sig=inspect.signature(api.verificar_flexao_viga_retangular)
    defaults={k:sig.parameters[k].default for k in ('gamma_c','gamma_s')}
    cp=implementation_provenance(api)
    for region in regions:
        region.update(tqs_sections=[],governing_demand=None,concretopy_result=None,capacity=None,
                      comparison={'utilization':None,'capacity_sufficient':None},blockers=[],status='unresolved',
                      diagnostics={'model_assumptions_valid':None,'ductility':None,'minimum_reinforcement':None,
                                   'anchorage_checked':False,'reinforcement_development_checked':False})
        region['provenance'].update(materials={'shared_pointer':'/material_interpretation'},moment_series={'shared_pointer':'/source_series'},
                                    concretopy={'shared_pointer':'/concretopy_interface'})
        region['blockers'].extend(region['geometric_reinforcement']['issues'])
        if region['transverse_status']!='resolved': region['blockers'].append('unresolved_transverse_geometry')
        region['blockers'].extend(geometry_issues)
        if steel['status']!='consistent': region['blockers'].append('unresolved_steel:'+steel['status'])
        if fck is None: region['blockers'].append('missing_fck')
        if gamma_f is None: region['blockers'].append('missing_gamma_f')
        if series_issue: region['blockers'].append('unresolved_moment_series:'+series_issue)
    if moment:
        for j,(section,x,value) in enumerate(zip(moment['sections'],moment['positions'],moment['values'])):
            owners=[r for r in regions if contains(r,x)]
            if len(owners)!=1:
                raise ValueError('Seção TQS fora do domínio físico ou associação não única: '+str(section))
            point={'section':section,'x_m':x,'value_knm':value,
                   'eligible_positive':value is not None and not isinstance(value,bool) and isinstance(value,(int,float)) and math.isfinite(value) and value>0,
                   'provenance':{'series_pointer':f'/beam/spans/0/internal_forces/{index}',
                                 'value_pointer':f'/beam/spans/0/internal_forces/{index}/values/{j}',
                                 'position_pointer':f'/beam/spans/0/internal_forces/{index}/positions/{j}',
                                 'sources':copy.deepcopy(moment['sources']),
                                 'position_sources':copy.deepcopy(positioned['provenance'].get(f'/beam/spans/0/internal_forces/{index}/positions',[]))}}
            owners[0]['tqs_sections'].append(point)
    for region in regions:
        points=region['tqs_sections']
        eligible=[p for p in points if p['eligible_positive']]
        if any(p['value_knm'] is None or isinstance(p['value_knm'],bool) or not isinstance(p['value_knm'],(int,float)) or not math.isfinite(p['value_knm']) for p in points):
            region['blockers'].append('missing_sampled_demand')
        if moment and not points:
            region['status']='demand_not_sampled';continue
        if moment and points and not eligible:
            region['status']='no_positive_demand' if 'missing_sampled_demand' not in region['blockers'] else 'unresolved';continue
        if not eligible: continue
        governing=max(eligible,key=lambda p:p['value_knm'])
        region['governing_demand']={**copy.deepcopy(governing),'type':'Msk_positive','unit':'kN.m','source_series_pointer':'/source_series'}
        if region['blockers']: continue
        g=region['transverse_geometry'];layers=region['geometric_reinforcement']['layers']
        region['concretopy_call']={'geometry':copy.deepcopy(g),'fck_mpa':fck,'fyk_mpa':steel['derived_fyk_mpa'],
                                  'Es_mpa':inspect.signature(api.Aco).parameters['es'].default,
                                  'layers':[{'numero_barras':c['numero_barras'],'diametro_mm':c['diametro_mm'],'d_cm':None} for c in layers],
                                  'coefficients':{**defaults,'gamma_f':gamma_f},'verificar_armadura_minima':False}
        try:
            response=api.verificar_flexao_viga_retangular(
                api.SecaoRetangular(g['bw_cm'],g['h_cm'],g['cover_cm'],g['stirrup_diameter_mm']),
                api.Concreto(fck),api.Aco(steel['derived_fyk_mpa']),
                [api.CamadaArmaduraLongitudinal(c['numero_barras'],api.Barra(c['diametro_mm'])) for c in layers],
                gamma_f=gamma_f,verificar_armadura_minima=False)
        except (ValueError,TypeError) as error:
            region['blockers'].append('concretopy_rejected_input:'+str(error));continue
        region['concretopy_result']=asdict(response)
        region['capacity']={'MRd':None if response.mrd_kncm is None else response.mrd_kncm/100,
                            'Mk_equivalent':None if response.mk_equivalente_kncm is None else response.mk_equivalente_kncm/100,'unit':'kN.m'}
        region['diagnostics'].update(model_assumptions_valid=response.hipoteses_validas,ductility=response.ductilidade_atendida,minimum_reinforcement=response.armadura_minima_atendida)
        mk=region['capacity']['Mk_equivalent']
        if response.hipoteses_validas and mk is not None and math.isfinite(mk) and mk>0:
            region['status']='checked'; region['comparison']={'utilization':governing['value_knm']/mk,'capacity_sufficient':mk>=governing['value_knm']}
        else:
            region['blockers'].append('invalid_capacity')
    checked=[r for r in regions if r['status']=='checked']
    maximum=max(checked,key=lambda r:r['comparison']['utilization']) if checked else None
    summary={'regions_total':len(regions),'regions_checked':len(checked),'regions_unresolved':sum(bool(r['blockers']) for r in regions),
             'regions_without_sampled_demand':sum(r['status']=='demand_not_sampled' for r in regions),
             'regions_without_positive_demand':sum(r['status']=='no_positive_demand' for r in regions),
             'regions_not_checked':len(regions)-len(checked),
             'all_checked_regions_capacity_sufficient':all(r['comparison']['capacity_sufficient'] for r in checked) if checked else None,
             'maximum_utilization':None if maximum is None else {'value':maximum['comparison']['utilization'],'region_id':maximum['region_id'],
                                                               'tqs_section':maximum['governing_demand']['section'],'x_m':maximum['governing_demand']['x_m']},
             'incomplete':len(checked)!=len(regions)}
    return {'model_type':'positive_flexure_regions_check','schema_version':'1.0','beam_id':beam,'span_id':tqs['beam']['spans'][0]['id'],
            'coordinate_system':copy.deepcopy(mapping['coordinate_system']),'domain_m':list(domain),
            'regions':regions,'span_summary':summary,'source_series':source_series,'series_issue':series_issue,
            'material_interpretation':steel,'material_parameters':{'fck_mpa':fck,'fck_provenance':fp,'gamma_f':gamma_f,'gamma_f_provenance':gp},
            'concretopy_interface':cp,'geometry_comparison':copy.deepcopy(mapping['geometry']),
            'policies':{'bounds':'closed_bar_intervals; compatible endpoint to right then left; otherwise isolated closed point; no epsilon',
                        'demand':'Msk positivo somente em posições TQS existentes; sem interpolação',
                        'scope':'presença geométrica; sem desenvolvimento/ancoragem ou aprovação global'}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('detail','tqs','positioned','mapping','raw'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--concretopy-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();paths=[getattr(args,n) for n in ('detail','tqs','positioned','mapping','raw')]
    try:
        if any(args.output.resolve()==p.resolve() or args.output.exists() and args.output.samefile(p) for p in paths):
            raise ValueError('Saída não pode sobrescrever entrada.')
        data=[json.loads(p.read_text(encoding='utf8')) for p in paths]
        root=Path(__file__).resolve().parents[2]
        for entry in data[3].get('inputs',{}).values():
            source=Path(entry['path']);source=source if source.is_absolute() else root/source
            if hashlib.sha256(source.read_bytes()).hexdigest()!=entry['sha256']:
                raise ValueError('Mapping desatualizado: hash diverge.')
        if hashlib.sha256(paths[-1].read_bytes()).hexdigest()!=data[1]['raw_document']['sha256']:
            raise ValueError('Raw não corresponde ao consolidado.')
        sys.path.insert(0,str(args.concretopy_root.resolve()));api=importlib.import_module('concretopy')
        if not Path(api.__file__).resolve().is_relative_to(args.concretopy_root.resolve()):
            raise ValueError('Concretopy importado fora da raiz indicada.')
        out=check_positive_flexure(*data,api)
        out['inputs']={n:{'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for n,p in zip(('detail','tqs','positioned','mapping','raw'),paths)}
        out['implementation']={n:hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in ('positive_flexure.py','flexure_regions.py','materials.py','tqs_moments.py')}
        args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
        print(out['span_summary'])
    except (ValueError,KeyError,TypeError,OSError) as error:
        parser.error(str(error))


if __name__=='__main__': main()
