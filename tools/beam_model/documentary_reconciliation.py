"""Reconcile documentary representations; marks are not physical occurrences."""
from copy import deepcopy
from collections import defaultdict

VIEWS = ('ELEVATION', 'SECTION', 'STEEL_SCHEDULE')
FIELDS = ('quantity', 'diameter_mm', 'nominal_length_cm', 'shape')


def reconcile(observations, coverage, *, expected_marks=()):
    ids = [o['representation_id'] for o in observations]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate_documentary_representation')
    grouped = defaultdict(list)
    for original in observations:
        o = deepcopy(original)
        if o['view'] not in VIEWS or not o.get('provenance') or not o.get('mark'):
            raise ValueError('documentary_view_mark_provenance_required')
        grouped[o['mark']].append(o)
    for mark in expected_marks:
        grouped.setdefault(mark, [])
    results = []
    for mark, obs in sorted(grouped.items()):
        issues, comparisons = [], []
        for view in VIEWS:
            local = [c for c in coverage if c['view'] == view and (c.get('marks') is None or mark in c['marks'])]
            broken = [c for c in local if c.get('integrity') in ('TRUNCATED', 'UNREADABLE')]
            if broken:
                issues.append(dict(code='PLOTTING_INTEGRITY' if any(c['integrity'] == 'TRUNCATED' for c in broken) else 'UNREADABLE_DOCUMENT', view=view, provenance=broken))
            if not any(o['view'] == view for o in obs):
                code = 'REPRESENTATION_NOT_FOUND_IN_COMPLETE_READING' if local and all(c.get('extraction') == 'COMPLETE' and c.get('integrity') == 'INTACT' for c in local) else 'REPRESENTATION_NOT_EXTRACTED'
                issues.append(dict(code=code, view=view, physical_absence_proved=False))
        for field in FIELDS:
            buckets = defaultdict(list)
            for o in obs:
                if field not in o or o[field] is None:
                    continue
                if field == 'quantity':
                    scope = o.get('quantity_scope')
                    if scope not in ('POSITION_TOTAL', 'OCCURRENCE', 'SECTION_COUNT'):
                        issues.append(dict(code='QUANTITY_SCOPE_MISSING', representation_id=o['representation_id']))
                        continue
                    key = (scope, o.get('occurrence_id') if scope == 'OCCURRENCE' else o.get('section_id') if scope == 'SECTION_COUNT' else None)
                    if scope != 'POSITION_TOTAL' and key[1] is None:
                        issues.append(dict(code='QUANTITY_ASSOCIATION_MISSING', representation_id=o['representation_id']))
                        continue
                else:
                    key = ('POSITION', None)
                buckets[key].append(o)
            for scope, entries in buckets.items():
                values = [o[field] for o in entries]
                conflict = any(v != values[0] for v in values[1:])
                comparisons.append(dict(field=field, scope=list(scope), state='CONFLICTING' if conflict else 'DOCUMENTED_CONFIRMED', value=None if conflict else deepcopy(values[0]), representation_ids=[o['representation_id'] for o in entries]))
                if conflict:
                    issues.append(dict(code='DOCUMENTARY_DIVERGENCE', field=field, representation_ids=[o['representation_id'] for o in entries]))
        # Totals only against a complete, explicitly identified physical inventory.
        total = [o for o in obs if o.get('quantity_scope') == 'POSITION_TOTAL' and o.get('quantity') is not None]
        per = [o for o in obs if o.get('quantity_scope') == 'OCCURRENCE' and o.get('occurrence_id') and o.get('quantity') is not None and o.get('physical_inventory_complete') is True]
        if per:
            occurrences = defaultdict(set)
            for o in per:
                occurrences[o['occurrence_id']].add(o['quantity'])
            if all(len(v) == 1 for v in occurrences.values()):
                count = sum(next(iter(v)) for v in occurrences.values())
                if any(o['quantity'] != count for o in total):
                    issues.append(dict(code='PHYSICAL_TOTAL_DIVERGENCE', physical_quantity=count, representation_ids=[o['representation_id'] for o in total + per]))
        for o in obs:
            if o.get('revision_status') == 'PROVEN_STALE':
                issues.append(dict(code='STALE_DOCUMENT_PROVED', representation_id=o['representation_id'], provenance=o['provenance']))
        results.append(dict(mark=mark, representations=obs, comparisons=comparisons, issues=issues,
                            physical_absence_proved=False,
                            state='CONFLICTING' if any(i['code'] in ('DOCUMENTARY_DIVERGENCE', 'PHYSICAL_TOTAL_DIVERGENCE', 'STALE_DOCUMENT_PROVED') for i in issues) else 'INCOMPLETE' if issues else 'RECONCILED'))
    return dict(schema_version='1.0', positions=results, coverage=deepcopy(coverage), source_priority_applied=False)
