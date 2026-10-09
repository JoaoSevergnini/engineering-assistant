"""Cortante caracteristico VGESFS auditado; selecao discreta do vao inteiro."""
import copy
from moment_diagram import dec
from tqs_moments import at

RULE = 'engineer_confirmed_al_shear_selection_v1'


def select_span_shear(series, domain):
    """Recebe series caracteristicas ja auditadas. Conserva todos os empates."""
    start, end = map(dec, domain)
    if start >= end or not series:
        raise ValueError('invalid_shear_domain_or_missing_series')
    points = []
    for item in series:
        if item.get('unit') != 'kN' or item.get('quantity') != 'shear':
            raise ValueError('invalid_shear_units_or_quantity')
        sections, xs, values = (item[k] for k in ('sections', 'positions', 'values'))
        if len(xs) < 2 or len({len(xs), len(values), len(sections)}) != 1:
            raise ValueError('invalid_shear_series_lengths')
        positions = list(map(dec, xs))
        if any(b <= a for a, b in zip(positions, positions[1:])) or len(set(sections)) != len(sections):
            raise ValueError('invalid_shear_positions_or_sections')
        for j, (section, x, v) in enumerate(zip(sections, xs, values)):
            value = dec(v)  # missing/NaN is not silently discarded
            if not start <= dec(x) <= end:
                raise ValueError('shear_sample_outside_physical_span')
            points.append({'section': section, 'x_m': x, 'Vk_signed_kn': float(value),
                           'Vk_abs_kn': float(abs(value)), 'series': item.get('envelope'),
                           'provenance': {'series': copy.deepcopy(item.get('provenance')),
                                          'sample_index': j, 'source': 'discrete_TQS_endpoint'}})
    maximum = max(p['Vk_abs_kn'] for p in points)
    return {'status': 'resolved', 'Vk_used_kn': maximum,
            'governing': [p for p in points if p['Vk_abs_kn'] == maximum],
            'rule': RULE, 'physical_domain_m': list(domain),
            'series': copy.deepcopy(series), 'samples_considered': len(points),
            'provenance': {'selection': 'max(abs(Vk_i)) over every supplied span sample, both envelopes; all ties retained',
                           'reference': 'tools/reinforcement_checks/al_shear_selection.md',
                           'domain_note': 'TQS sampled domain retained; no extrapolation toward support axes or resampling'}}


def shear_from_tqs(mapping, tqs, positioned, raw):
    if mapping['beam_id'] != tqs['beam']['id'] or positioned['beam']['id'] != tqs['beam']['id']:
        raise ValueError('incompatible_shear_beam_identity')
    if mapping['force_series'] != positioned['beam']['spans'][0]['internal_forces']:
        raise ValueError('shear_mapping_positions_mismatch')
    found = {}
    for i, series in enumerate(mapping['force_series']):
        if series.get('quantity') != 'shear':
            continue
        envelope = series.get('envelope')
        label = {'max': 'Q MX.', 'min': 'Q MN.'}.get(envelope)
        proofs = []
        for ref in series['sources']:
            src = tqs['sources'][ref.split('#')[0]]
            rec = at(raw, src['raw_pointer'])
            norm = rec.get('normalizacao') or {}
            if src['file'] != 'VGESFS.LST' or norm.get('vao_original') != tqs['beam']['spans'][0]['report_span_ids']['VGESFS.LST']:
                continue
            if norm.get('grandeza_original') != label or label is None:
                continue
            if series.get('stage') != 'model_input' or series.get('unit') != 'kN':
                raise ValueError('invalid_characteristic_shear_contract')
            if [v['normalizado']['valor'] for v in norm['valores']] != series['values']:
                raise ValueError('shear_raw_values_mismatch')
            proofs.append({'reference': ref, 'source': copy.deepcopy(src), 'record': copy.deepcopy(rec)})
        if not proofs or envelope in found:
            raise ValueError('unidentified_or_ambiguous_characteristic_shear')
        item = copy.deepcopy(series)
        pointer = f'/beam/spans/0/internal_forces/{i}'
        item['provenance'] = {'input': 'positioned_tqs', 'pointer': pointer,
                              'position_sources': copy.deepcopy(positioned['provenance'].get(pointer+'/positions', [])),
                              'evidence': proofs, 'label_original': label,
                              'level': 'Vk characteristic, engineer-confirmed workflow'}
        found[envelope] = item
    if set(found) != {'max', 'min'}:
        raise ValueError('missing_characteristic_shear_envelope')
    # Same physical span/positions; neither M MX nor the cut side selects a V envelope.
    moment = next(s for s in mapping['force_series'] if s['quantity'] == 'bending_moment' and s['envelope'] == 'max')
    if any(s['positions'] != moment['positions'] or s['sections'] != moment['sections'] for s in found.values()):
        raise ValueError('shear_moment_span_positions_mismatch')
    domain = [mapping['supports'][side]['axis_x'] for side in ('left', 'right')]
    return select_span_shear(list(found.values()), domain)
