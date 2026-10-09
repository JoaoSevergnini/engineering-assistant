"""Per-mark termination identity; physical compositions, never ordered removals."""
from moment_diagram import dec
RULE='engineer_confirmed_independent_longitudinal_mark_termination_v1'
def describe_termination(before_marks,after_marks,mark,actual_end,cut_side):
    before,after=set(before_marks),set(after_marks)
    removed=before-after
    if mark not in removed or after-before:
        raise ValueError('inconsistent_termination_or_replacement_composition')
    side=cut_side.upper()
    if side not in ('LEFT','RIGHT'):raise ValueError('invalid_termination_side')
    dec(actual_end)
    return {'event_key':{'bar_mark':mark,'cut_side':side,'actual_end_m':actual_end},
        'selected_mark':mark,'provided_end_m':actual_end,
        'geometrically_terminated_marks':sorted(removed),
        'other_coincident_marks':sorted(removed-{mark}),'ordered_cut_sequence':None,
        'remaining_composition_basis':'physical_after_all_documented_terminations_at_this_coordinate',
        'rule':RULE,'provenance':{'before_marks':sorted(before),'after_marks':sorted(after),
        'interpretation':'Independent per-mark check; no fictitious intermediate composition and no removal priority'}}
