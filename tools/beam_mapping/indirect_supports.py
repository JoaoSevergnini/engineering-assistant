"""Match sourced plan encounters to existing consolidated TQS reactions.
No load direction from graphics, inferred reactions or resistant equations.
"""
import math


def lst_relations(models):
    result = []
    for model in models:
        for reaction in model['beam'].get('support_reactions', []):
            name = (reaction.get('reported_support_name') or '').strip().strip('\x00')
            if not name.startswith('V'):
                continue
            sources = [dict(model['sources'][ref.split('#')[0]], reference=ref)
                       for ref in reaction.get('sources', [])
                       if ref.split('#')[0] in model.get('sources', {})]
            result.append(dict(supported_beam=model['beam']['id'], supporting_beam=name,
                supported_beam_support_id=reaction.get('report_support_number'),
                reaction_unit=reaction.get('unit'), reaction_observations={
                    'max': reaction.get('max'), 'min': reaction.get('min')},
                support_relation_source=sources, reaction_source=sources,
                file=reaction.get('file'), status='INCONCLUSIVE'))
    return result


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def associate(encounters, relations, *, floor, semantics=None):
    """Keep all encounters and unmatched LST observations; never merge cases.

    Encounters explicitly associate beam IDs/support ID with sourced point and
    receiving-axis position. Semantics keys are (supported beam, support, file).
    Totality, nature, sign, case and envelope choice require documentary evidence.
    """
    semantics = semantics or {}
    results, used = [], set()
    for encounter in encounters:
        matched = False
        for i, relation in enumerate(relations):
            if set(encounter['beams']) != {relation['supported_beam'], relation['supporting_beam']}:
                continue
            if encounter.get('supported_beam_support_id') != relation['supported_beam_support_id']:
                continue
            matched = True
            used.add(i)
            row = dict(relation, floor=floor, geometry_source=encounter.get('source'),
                       intersection_coordinates=encounter.get('point'),
                       supporting_beam_axis_position=encounter.get('axis_position_m'))
            issues = []
            if relation['supported_beam_support_id'] is None:
                issues.append('lst_support_id_unresolved')
            same_support = [e for e in encounters if (e.get('supported_beam'), e.get('supported_beam_support_id')) == (encounter.get('supported_beam'), encounter.get('supported_beam_support_id'))]
            if len(same_support) != 1:
                issues.append('geometric_association_ambiguous')
            if (encounter.get('supported_beam'), encounter.get('supporting_beam')) != (
                    relation['supported_beam'], relation['supporting_beam']):
                issues.append('direction_or_identifier_conflict')
            if not encounter.get('source') or encounter.get('same_elevation_confirmed') is not True:
                issues.append('geometry_or_elevation_unconfirmed')
            point = encounter.get('point')
            if not isinstance(point, (list, tuple)) or len(point) != 2 or not all(map(finite, point)):
                issues.append('intersection_coordinates_unresolved')
            if not finite(encounter.get('axis_position_m')):
                issues.append('axis_position_unresolved')
            meta = semantics.get((relation['supported_beam'], relation['supported_beam_support_id'], relation['file']), {})
            row['reaction_metadata'] = meta
            if (not meta.get('source') or meta.get('is_total') is not True
                    or meta.get('nature') not in ('CHARACTERISTIC', 'DESIGN')
                    or not meta.get('load_case') or meta.get('downward_sign') not in (-1, 1)):
                issues.append('reaction_semantics_unresolved')
            value = relation['reaction_observations'].get(meta.get('selected_envelope'))
            if not finite(value) or relation['reaction_unit'] != 'kN':
                issues.append('reaction_selection_unresolved')
            else:
                row['reaction_value'] = value
                if value * meta.get('downward_sign', 0) < 0:
                    issues.append('uplift_not_applicable_to_suspension')
            siblings = [r for r in relations if (r['supported_beam'], r['supporting_beam'],
                        r['supported_beam_support_id']) == (relation['supported_beam'],
                        relation['supporting_beam'], relation['supported_beam_support_id'])]
            if len(siblings) > 1 and not meta.get('governing_selection_source'):
                issues.append('reaction_variants_require_selection')
            if not relation['support_relation_source']:
                issues.append('lst_source_unresolved')
            row.update(status='CONFIRMED' if not issues else 'INCONCLUSIVE', diagnostics=issues)
            results.append(row)
        if not matched:
            results.append(dict(encounter, floor=floor, status='INCONCLUSIVE',
                diagnostics=['geometric_encounter_without_matching_lst_support']))
    for i, relation in enumerate(relations):
        if i not in used:
            results.append(dict(relation, floor=floor, geometry_source=None,
                intersection_coordinates=None, supporting_beam_axis_position=None,
                diagnostics=['plan_geometry_pending']))
    return results

def suspension_connection(record, *, connection_id, supported_geometry, applicability_source, placement):
    """Bridge only fully confirmed associations into the existing verifier.

    Applicability/geometry are independent sourced inputs. The downstream
    verifier still checks physical domains, material context and real stirrups.
    """
    if record.get('status') != 'CONFIRMED':
        raise ValueError('indirect_support_not_confirmed')
    if not applicability_source or not supported_geometry.get('source'):
        raise ValueError('suspension_context_unresolved')
    meta = record['reaction_metadata']
    return dict(id=connection_id,type='BEAM_ON_BEAM',
        supported_beam_id=record['supported_beam'],receiving_beam_id=record['supporting_beam'],
        transfer_confirmed=True,transfer_source=record['support_relation_source'],
        suspension_applicable=True,applicability_source=applicability_source,
        supported_geometry=supported_geometry,placement=placement,
        projected_axis_m=record['supporting_beam_axis_position'],axis_source=record['geometry_source'],
        reaction=dict(value=record['reaction_value'],unit='kN',nature=meta['nature'],
            is_total=True,total_source=meta['source'],combination=meta['load_case'],
            downward_sign=meta['downward_sign'],source=record['reaction_source'],
            supported_beam_id=record['supported_beam'],receiving_beam_id=record['supporting_beam']))
