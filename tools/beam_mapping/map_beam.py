"""Compatibilidade geométrica documental; sem dimensionamento ou interpolação."""
import argparse
import copy
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
from support_context import resolve_support, interpret_origin


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('Dado numérico necessário ausente/inválido: ' + label)
    return Decimal(str(value))


def detail_to_tqs(x_cm, support_width_m):
    return float(number(x_cm, 'x_detail') / 100 + number(support_width_m, 'largura') / 2)


def series_identity(series):
    return {k: v for k, v in series.items() if k not in ('positions', 'sources')}


def selected(model, path, value, filename):
    """Seleciona alternativa já normalizada, com fonte explícita; não interpreta LST."""
    candidates = [(value, model.get('provenance', {}).get(path, []))]
    for warning in model.get('warnings', []):
        if warning.get('path') == path:
            candidates.extend((a['value'], a['sources']) for a in warning.get('alternatives', []))
    found = []
    for candidate, refs in candidates:
        refs = [r for r in refs if model['sources'][r.split('#')[0]]['file'].upper() == filename]
        if candidate is not None and refs:
            found.append((number(candidate, path), refs))
    if not found or len({v for v, refs in found}) != 1:
        raise ValueError('Fonte escolhida ausente ou conflitante: ' + filename + ' ' + path)
    refs = sorted({r for v, rr in found for r in rr})
    return found[0][0], {'input': 'tqs', 'json_pointer': path, 'selected_value': float(found[0][0]),
                         'unit': 'm', 'sources': refs,
                         'records': {r: model['sources'][r.split('#')[0]] for r in refs}}


def map_beam(detail, tqs, positioned, related_models=(), *, support_context=None):
    """Retorna novo diagnóstico. Primeira versão: um vão, sem balanços."""
    if detail.get('model_type') != 'longitudinal_beam_detail' or tqs.get('model_type') != 'consolidated_beam' or positioned.get('model_type') != 'consolidated_beam':
        raise ValueError('Tipos de modelo incompatíveis.')
    if detail.get('schema_version') != '1.0' or any(m.get('schema_version') != '1.1' for m in (tqs, positioned)):
        raise ValueError('Versão de modelo não suportada.')
    beam_id = tqs['beam']['id']
    detail_ids = detail['beam'].get('ids', [detail['beam']['id']])
    if support_context is not None:
        if support_context.get('detail_beam_id') != detail['beam']['id']:
            raise ValueError('Contexto não corresponde ao detalhamento.')
        detail_ids = [m.get('beam_id') for m in support_context.get('members', [])]
        if detail['beam']['id'] not in detail_ids:
            raise ValueError('Contexto não inclui a viga documental.')
    if positioned['beam']['id'] != beam_id or beam_id not in detail_ids:
        raise ValueError('Identidade da viga incompatível.')
    if tqs.get('raw_document') != positioned.get('raw_document'):
        raise ValueError('Origem raw dos modelos TQS incompatível.')
    if any(m['units']['length'] != 'm' for m in (tqs, positioned)):
        raise ValueError('Unidade TQS deve ser m.')
    cs = detail['coordinate_system']
    if cs.get('unit') != 'cm' or cs.get('positive_direction') != 'para a direita':
        raise ValueError('Convenção do detalhamento não suportada.')
    origin = interpret_origin(cs.get('origin'), detail['spans'][0]['left_support'])
    policy = positioned.get('policies', {}).get('section_positions', '')
    if 'eixo fisico esquerdo' not in policy or 'Em m' not in policy:
        raise ValueError('Modelo sem política confirmada de positions.')
    if any(len(m['beam']['spans']) != 1 for m in (tqs, positioned)) or len(detail['spans']) != 1 or detail.get('overhangs'):
        raise ValueError('Esta versão requer um vão sem balanços; não presume offsets globais.')
    span = tqs['beam']['spans'][0]
    ps = positioned['beam']['spans'][0]
    ds = detail['spans'][0]
    if ds.get('x_start_cm') != 0 or span['support_ids'] != ps['support_ids'] or span['id'] != ps['id']:
        raise ValueError('Origem ou associação do vão incompatível.')
    if len(span['support_ids']) != 2 or len(set(span['support_ids'])) != 2:
        raise ValueError('Ordem dos apoios ausente/ambígua.')
    length, lp = selected(tqs, '/beam/spans/0/geometry/length', span['geometry']['length'], 'VGESFS.LST')
    operands = {'length': lp}
    supports = {}
    widths, offsets = [], []
    for side, support_id, detail_id in zip(('left', 'right'), span['support_ids'], (ds['left_support'], ds['right_support'])):
        matches = [(i, s) for i, s in enumerate(tqs['beam']['supports']) if s['id'] == support_id]
        drawings = [s for s in detail['supports'] if s['id'] == detail_id]
        if len(matches) != 1 or len(drawings) != 1:
            raise ValueError('Apoio sem associação documental única: ' + support_id)
        resolution = None
        if support_context is not None or (support_id != detail_id and support_id not in (drawings[0].get('written_names') or [])):
            resolution = resolve_support(detail_id, support_id, beam_id, side, support_context)
        index, support = matches[0]
        base = '/beam/supports/' + str(index)
        width, wp = selected(tqs, base + '/width', support.get('width'), 'RELDTFPS.LST')
        offset, ep = selected(tqs, base + '/eccentricity', support.get('eccentricity'), 'RELDTFPS.LST')
        if width <= 0 or offset < 0:
            raise ValueError('Dimensão de apoio/DEPEV fora da política.')
        widths.append(width)
        offsets.append(offset)
        operands[side] = {'width': wp, 'depev': ep}
        supports[side] = {'id': support_id, 'width': float(width), 'depev': float(offset),
                          'detailing_support': copy.deepcopy(drawings[0])}
        if resolution is not None:
            supports[side]['resolution'] = resolution
            if number(drawings[0].get('width_cm'), 'largura apoio documental') / 100 != width:
                raise ValueError('Grouped support geometry mismatch: ' + detail_id)
    if support_context is not None:
        origin['resolved_origin_support'] = supports['left']['id']
        operands['support_context'] = copy.deepcopy(support_context)
        operands['documental_origin'] = origin
    if length <= 0:
        raise ValueError('Comprimento TQS não positivo.')
    axes = offsets[0] + length + offsets[1]
    clear = axes - sum(widths) / 2
    if clear <= 0:
        raise ValueError('Distância livre TQS não positiva.')
    detail_clear = number(ds['clear_length_cm'], 'comprimento livre detalhamento') / 100
    if number(ds['x_end_cm'], 'face direita detalhamento') / 100 != detail_clear:
        raise ValueError('Geometria interna do detalhamento inconsistente.')
    supports['left'].update(axis_x=0.0, inner_face_x=float(widths[0]/2), detailing_inner_face_x=float(widths[0]/2))
    supports['right'].update(axis_x=float(axes), inner_face_x=float(axes-widths[1]/2), detailing_inner_face_x=float(widths[0]/2+detail_clear))
    series = copy.deepcopy(ps['internal_forces'])
    if not series:
        raise ValueError('Nenhuma série posicionada.')
    positions = series[0].get('positions')
    if not isinstance(positions, list) or len(positions) != 13:
        raise ValueError('Esperadas 13 positions existentes.')
    decimals = [number(x, 'position') for x in positions]
    if any(b <= a for a, b in zip(decimals, decimals[1:])) or decimals[0] != offsets[0] or decimals[-1] != offsets[0]+length:
        raise ValueError('Positions incompatíveis com origem/extremidades selecionadas.')
    for s in series:
        if any(s.get(k) is None for k in ('quantity', 'envelope', 'stage', 'unit')):
            raise ValueError('Série sem metadados necessários.')
        if s.get('sections') != list(range(1,14)) or s.get('positions') != positions or len(s.get('values', [])) != 13:
            raise ValueError('Série sem 13 seções/positions compatíveis.')
        originals = [o for o in span['internal_forces'] if series_identity(o) == series_identity(s) and set(s['sources']).issubset(o['sources'])]
        if not originals:
            raise ValueError('Esforços posicionados divergem do modelo consolidado.')
        for v in s['values']:
            if v is not None:
                number(v, 'esforço')
    sections = []
    for j, x in enumerate(positions):
        forces = []
        for k, s in enumerate(series):
            forces.append({**{key: copy.deepcopy(value) for key, value in s.items() if key not in ('sections','positions','values','sources')},
                           'section': j+1, 'position': x, 'value': s['values'][j],
                           'provenance': {'input': 'positioned_tqs', 'series_pointer': f'/beam/spans/0/internal_forces/{k}',
                                          'value_pointer': f'/beam/spans/0/internal_forces/{k}/values/{j}',
                                          'position_pointer': f'/beam/spans/0/internal_forces/{k}/positions/{j}',
                                          'sources': s['sources'],
                                          'position_sources': positioned['provenance'].get(f'/beam/spans/0/internal_forces/{k}/positions', [])}})
        sections.append({'section': j+1, 'x': x, 'forces': forces})

    def mapped_entities(key):
        result = []
        for i, entity in enumerate(detail.get(key, [])):
            item = copy.deepcopy(entity)
            start, end = entity.get('x_start_cm'), entity.get('x_end_cm')
            item['mapping_provenance'] = {'input': 'detailing', 'json_pointer': f'/{key}/{i}', 'translation_operand': operands['left']['width']}
            if start is None or end is None:
                item.update(mapping_status='unresolved', x_start_common=None, x_end_common=None, covered_tqs_sections=None, covered_tqs_points=None)
            else:
                a = number(start, 'início barra')/100 + widths[0]/2
                b = number(end, 'fim barra')/100 + widths[0]/2
                if a > b:
                    raise ValueError('Intervalo longitudinal invertido.')
                covered = [copy.deepcopy(s) for s, x in zip(sections, decimals) if a <= x <= b]
                item.update(mapping_status='mapped', x_start_common=float(a), x_end_common=float(b),
                            covered_tqs_sections=[s['section'] for s in covered], covered_tqs_points=covered)
            result.append(item)
        return result

    relations = []
    for related in related_models:
        if related['units']['length'] != 'm':
            raise ValueError('Modelo relacionado sem unidade m.')
        for reaction in related['beam'].get('support_reactions', []):
            if reaction.get('file', '').upper() == 'VGESFS.LST' and (reaction.get('support_id') or '').replace('\x00','') == beam_id:
                relations.append({'supported_beam': related['beam']['id'], 'receiving_beam': beam_id,
                                  'x': None, 'drawing_indirect_support_id': None, 'reinforcement_mark': None,
                                  'reaction': copy.deepcopy(reaction), 'raw_document': copy.deepcopy(related.get('raw_document')),
                                  'source_records': {r: related['sources'][r.split('#')[0]] for r in reaction['sources']}})
    unmapped = [copy.deepcopy(s) for s in span['internal_forces'] if not any(series_identity(s)==series_identity(p) for p in series)]
    return {'model_type': 'beam_geometry_mapping', 'schema_version': '1.0', 'beam_id': beam_id,
            'coordinate_system': {'origin': 'left_support_axis', 'positive_direction': 'left_to_right', 'unit': 'm'},
            'geometry': {'detailing_clear_span': float(detail_clear), 'tqs_clear_span': float(clear),
                         'difference': float(abs(clear-detail_clear)), 'tqs_minus_detail': float(clear-detail_clear),
                         'status': 'exact' if clear==detail_clear else 'mismatch', 'tqs_length': float(length), 'support_axis_length': float(axes)},
            'selected_geometry_operands': operands, 'supports': supports, 'tqs_sections': sections,
            'force_series': series, 'unmapped_tqs_series': unmapped,
            'reinforcement': mapped_entities('longitudinal_reinforcement'), 'skin_reinforcement': mapped_entities('skin_reinforcement'),
            'stirrup_regions': mapped_entities('stirrup_regions'),
            'drawing_indirect_supports': copy.deepcopy(detail.get('indirect_supports', [])), 'indirect_relations': relations,
            'drawing_context': {k: copy.deepcopy(detail.get(k)) for k in ('section','sections','suspension_reinforcement','anchorage_staples','uncertainties')},
            'input_diagnostics': {'tqs_warnings': copy.deepcopy(tqs.get('warnings', [])), 'positioned_warnings': copy.deepcopy(positioned.get('warnings', []))},
            'source_catalogs': {'tqs': copy.deepcopy(tqs['sources']), 'positioned_tqs': copy.deepcopy(positioned['sources'])},
            'policies': {'translation': 'x_common=x_detail_cm/100+b_left_m/2; sem DEPEV adicional',
                         'coverage': 'intervalo fechado; comparação decimal dos números publicados; sem interpolação',
                         'geometry_diagnosis': 'igualdade exata: exact; diferença não nula: mismatch; sem tolerância de engenharia',
                         'support_selection': 'ordem span.support_ids; largura e DEPEV RELDTFPS; comprimento VGESFS',
                         'scope': 'diagnóstico geométrico de um vão; nenhuma verificação estrutural'}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('detailing', type=Path)
    parser.add_argument('tqs', type=Path)
    parser.add_argument('positioned_tqs', type=Path)
    parser.add_argument('--related-model', action='append', type=Path, default=[])
    parser.add_argument('--support-context', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    paths = [args.detailing, args.tqs, args.positioned_tqs, *args.related_model]
    try:
        if any(args.output.resolve() == p.resolve() or (args.output.exists() and args.output.samefile(p)) for p in paths):
            raise ValueError('Saída não pode sobrescrever entrada.')
        data = [json.loads(p.read_text(encoding='utf-8')) for p in paths]
        context = None if args.support_context is None else json.loads(args.support_context.read_text(encoding='utf-8'))
        if args.support_context is not None and args.output.resolve() == args.support_context.resolve():
            raise ValueError('Saída não pode sobrescrever contexto.')
        out = map_beam(*data[:3], related_models=data[3:], support_context=context)
        out['inputs'] = {role: {'path': p.as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for role,p in zip(['detailing','tqs','positioned_tqs',*[f'related_{i}' for i in range(len(args.related_model))]], paths)}
        if args.support_context is not None:
            out['inputs']['support_context'] = {'path': args.support_context.as_posix(), 'sha256': hashlib.sha256(args.support_context.read_bytes()).hexdigest()}
        args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
        print(f"{out['beam_id']}: {out['geometry']['status']}, diferença {out['geometry']['difference']} m; {len(out['reinforcement'])} posições longitudinais.")
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
