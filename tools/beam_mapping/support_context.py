"""Resolução de labels em contexto documental confirmado, sem heurística por '/'."""
import copy


def resolve_support(label, support_id, beam_id, side, context):
    if label == support_id:
        return {'document_label': label, 'candidates': [label], 'resolved_support_id': support_id,
                'method': 'direct_identity'}
    if not context or context.get('type') != 'engineer_confirmed_shared_detail_towers':
        raise ValueError('unrecognized_grouped_support_context: ' + label)
    if not context.get('evidence'):
        raise ValueError('missing_support_context_evidence')
    labels = [s for s in context.get('support_labels', []) if s.get('label') == label and s.get('side') == side]
    members = [m for m in context.get('members', []) if m.get('beam_id') == beam_id]
    if len(labels) != 1 or len(members) != 1:
        raise ValueError('ambiguous_support_mapping: ' + label)
    candidates = labels[0].get('candidates', [])
    if not candidates or len(set(candidates)) != len(candidates):
        raise ValueError('ambiguous_support_mapping: candidates')
    expected = members[0].get('support_ids', {}).get(side)
    if expected != support_id or support_id not in candidates:
        raise ValueError('support_context_mismatch: ' + label)
    return {'document_label': label, 'candidates': copy.deepcopy(candidates),
            'resolved_support_id': support_id, 'beam_id': beam_id, 'side': side,
            'method': 'engineer_confirmed_tower_member_and_ordered_tqs_support',
            'tower': members[0].get('tower'), 'evidence': copy.deepcopy(context['evidence'])}


def interpret_origin(original, left_label):
    base = 'face interna do apoio esquerdo'
    if original == base:
        return {'original': original, 'origin_type': 'left_support_inner_face', 'origin_support_label': None}
    if original == base + ' ' + left_label:
        return {'original': original, 'origin_type': 'left_support_inner_face', 'origin_support_label': left_label}
    raise ValueError('Convenção do detalhamento não suportada.')
