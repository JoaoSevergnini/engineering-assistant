"""Text-first layer interpretation and existing transverse-fit precondition."""
from copy import deepcopy
from input_preflight import overlaps
from input_evidence import fact, validate_fact, PROVED
from physical_geometry import normalize_occurrence, project_occurrences
from support_correction import transverse_fit

CONVENTION = dict(origin='OFFICE_STANDARD', reference='João: sem indicação explícita, primeira camada', version='etapa1.1')


def interpret_layers(model, observations):
    out = deepcopy(model)
    ids = {b['occurrence_id'] for b in out['physical_geometry']['occurrences']}
    if set(observations) - ids:
        raise ValueError('layer_observation_unknown_occurrence')
    for bar in out['physical_geometry']['occurrences']:
        sources = observations.get(bar['occurrence_id'], {})
        text = sources.get('near_bar_text')
        section = sources.get('section')
        text = validate_fact(text) if text else None
        section = validate_fact(section) if section else None
        explicit = [s for s in (text, section) if s and s['state'] == 'DOCUMENTED_CONFIRMED']
        if any(s and s['state'] == 'CONFLICTING' for s in (text, section)) or (len(explicit) == 2 and text['value'] != section['value']):
            result = fact(state='CONFLICTING', provenance=[s for s in (text, section) if s])
        elif explicit:
            result = deepcopy(explicit[0])  # near-bar text precedes the complementary section
        elif sources.get('explicit_indication_absent') is True and sources.get('review_provenance') and bar['quantity']['state'] in PROVED:
            result = fact([bar['quantity']['value']], state='INFERRED_EXPLICIT_CONVENTION',
                          provenance=sources['review_provenance'], criterion=CONVENTION)
        else:
            # Missing extraction cannot justify declaring no explicit annotation.
            result = fact(provenance=[dict(reference='Layer annotation examination pending', original=bar['layers'])])
        bar['layers'] = result
        bar['layer_interpretation'] = dict(priority='NEAR_BAR_TEXT_THEN_SECTION', observations=deepcopy(sources),
            documental_proof=result['state'] == 'DOCUMENTED_CONFIRMED', convention=result['state'] == 'INFERRED_EXPLICIT_CONVENTION')
        bar.update(normalize_occurrence(bar))
    out.setdefault('operational_review', {})['require_layer_fit'] = True
    return out


def local_layer_fit(model, interval_m, control, api):
    """Combined occurrences by face/layer; never test each mark in isolation."""
    a, z = interval_m
    sign = 'negative' if control == 'negative_flexure' else 'positive' if control == 'positive_flexure' else None
    segments = [s for s in model['physical_geometry']['segments'] if
        s['x_start_m']['state'] in PROVED and s['x_end_m']['state'] in PROVED and
        s['x_start_m']['value'] <= a and s['x_end_m']['value'] >= z and s['geometry_type'] == 'CONSTANT']
    if len(segments) != 1:
        return dict(fits=None, diagnostics=['unique_constant_physical_segment'])
    geo = segments[0]['geometry']
    keys = dict(bw='width_cm', h='height_cm', cobrimento='cover_cm', diametro_estribo_mm='stirrup_diameter_mm')
    if geo['section_shape']['value'] not in ('RECTANGULAR', 'rectangular') or any(geo[k]['state'] not in PROVED for k in keys.values()):
        return dict(fits=None, diagnostics=['layer_fit_geometry_pending'])
    bars = [b for b in project_occurrences(model) if (sign is None or b['function'] == sign) and
            overlaps(b['x_start_common'], b['x_end_common'], a, z)]
    if not bars or any(b['x_start_common'] is None or b['x_end_common'] is None or b['layers'] is None or
                       b['diameter_mm'] is None or b['bars'] is None or b['face'] not in ('lower', 'upper') for b in bars):
        return dict(fits=None, diagnostics=['layer_fit_occurrences_pending'])
    # The interval must have been partitioned at bar events by the existing decomposer.
    if any(a < x < z for b in bars for x in (b['x_start_common'], b['x_end_common'])):
        return dict(fits=None, diagnostics=['layer_fit_requires_longitudinal_partition'])
    checks = []
    for face in sorted({b['face'] for b in bars}):
        layers = {}
        for bar in (b for b in bars if b['face'] == face):
            for i, count in enumerate(bar['layers'], 1):
                if count:
                    layers.setdefault(i, []).extend([bar['diameter_mm']] * count)
        checked = transverse_fit({k: geo[v]['value'] for k, v in keys.items()},
            [dict(layer=i, diameters_mm=phis) for i, phis in sorted(layers.items())], api)
        checks.append(dict(face=face, **checked))
    states = [c['cabimento_transversal'] for c in checks]
    return dict(fits=False if False in states else None if None in states else True, checks=checks,
                diagnostics=[d for c in checks for d in c['diagnostics']], resistant_methods_modified=False)
