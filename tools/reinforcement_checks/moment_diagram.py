"""Diagrama Msk linear por trechos, derivado de pontos primários auditados."""
import copy
from decimal import Decimal, localcontext
import math
from tqs_moments import audited_moment_series

RULE = {'id': 'engineer_confirmed_tqs_linear_interpolation_v1',
        'author': 'João Severgnini', 'date': '2026-10-04',
        'source': 'Decisão explícita do engenheiro na conversa: interpolação linear entre pontos consecutivos; sem extrapolação.',
        'reference': '.agents/skills/reinforcement-review/references/tqs-beam-data.md',
        'decimal_precision': 50}


def dec(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError('invalid_numeric_value')
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('invalid_numeric_value')
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError('invalid_numeric_value')
    return result


class MomentDiagram:
    def __init__(self, points, provenance=None):
        if len(points) < 2:
            raise ValueError('at_least_two_sample_points_required')
        self.points = copy.deepcopy(points)
        self.provenance = copy.deepcopy(provenance or {})
        self.xs = [dec(p['x_m']) for p in self.points]
        self.ms = [None if p.get('value_knm') is None else dec(p['value_knm']) for p in self.points]
        if any(b <= a for a, b in zip(self.xs, self.xs[1:])):
            raise ValueError('positions_must_be_strictly_increasing_no_duplicates')
        self.segments = []
        with localcontext() as ctx:
            ctx.prec = RULE['decimal_precision']
            for i in range(len(points)-1):
                a, b = self.ms[i:i+2]
                slope = None if a is None or b is None else (b-a)/(self.xs[i+1]-self.xs[i])
                self.segments.append({'segment_id': f'SEG{i+1}', 'start_section': points[i]['section'],
                    'end_section': points[i+1]['section'], 'x_start_m': points[i]['x_m'], 'x_end_m': points[i+1]['x_m'],
                    'm_start_knm': points[i].get('value_knm'), 'm_end_knm': points[i+1].get('value_knm'),
                    'slope_knm_per_m': None if slope is None else float(slope),
                    'slope_decimal': None if slope is None else str(slope),
                    'segment_status': 'unresolved_missing_value' if slope is None else 'resolved',
                    'base_points': copy.deepcopy(self.points[i:i+2])})

    def as_dict(self):
        return {'model_type': 'piecewise_linear_characteristic_moment', 'unit': 'kN.m',
                'domain_m': [self.points[0]['x_m'], self.points[-1]['x_m']],
                'points': copy.deepcopy(self.points), 'segments': copy.deepcopy(self.segments),
                'provenance': copy.deepcopy(self.provenance), 'rule': copy.deepcopy(RULE)}

    def moment_at_x(self, x):
        q = dec(x)
        out = {'x_m': float(q), 'x_decimal': str(q), 'value_knm': None,
               'value_decimal': None, 'provenance': copy.deepcopy(self.provenance), 'rule': copy.deepcopy(RULE)}
        if q < self.xs[0] or q > self.xs[-1]:
            return {**out, 'status': 'outside_sampled_domain', 'source_type': None}
        if q in self.xs:
            i = self.xs.index(q)
            return {**out, 'status': 'unresolved_missing_value' if self.ms[i] is None else 'resolved',
                    'source_type': 'tqs_section', 'section': self.points[i]['section'],
                    'value_knm': self.points[i].get('value_knm'),
                    'value_decimal': None if self.ms[i] is None else str(self.ms[i]),
                    'base_points': [copy.deepcopy(self.points[i])],
                    'segment_ids': [s['segment_id'] for j,s in enumerate(self.segments) if j == i or j+1 == i]}
        i = next(i for i in range(len(self.segments)) if self.xs[i] < q < self.xs[i+1])
        out.update(source_type='linear_interpolation', segment_ids=[self.segments[i]['segment_id']],
                   base_points=copy.deepcopy(self.points[i:i+2]), status=self.segments[i]['segment_status'])
        if self.ms[i] is not None and self.ms[i+1] is not None:
            with localcontext() as ctx:
                ctx.prec = RULE['decimal_precision']
                m = self.ms[i] + (self.ms[i+1]-self.ms[i])*(q-self.xs[i])/(self.xs[i+1]-self.xs[i])
            out.update(value_knm=float(m), value_decimal=str(m))
        return out

    def find_crossings(self, m_limit):
        limit = dec(m_limit)
        events, gaps = {}, []
        with localcontext() as ctx:
            ctx.prec = RULE['decimal_precision']
            for i,s in enumerate(self.segments):
                a,b = self.ms[i:i+2]; x1,x2 = self.xs[i:i+2]
                if a is None or b is None:
                    gaps.append(s['segment_id']); continue
                direction = 'constant' if a == b else 'increasing' if b > a else 'decreasing'
                origin = {'segment_id': s['segment_id'], 'direction': direction, 'base_points': copy.deepcopy(s['base_points'])}
                if a == b:
                    if a == limit:
                        events[('interval',x1,x2)] = {'status': 'coincident_segment', 'x_start_m': float(x1),
                            'x_end_m': float(x2), 'segments': [origin], 'source_type': 'linear_interpolation'}
                    continue
                if not min(a,b) <= limit <= max(a,b): continue
                x = x1 if limit == a else x2 if limit == b else x1+(limit-a)*(x2-x1)/(b-a)
                key = ('point',x,x)
                if key not in events:
                    events[key] = {'status': 'crossing', 'x_m': float(x), 'x_decimal': str(x),
                        'source_type': 'tqs_section' if x in self.xs else 'linear_interpolation', 'segments': []}
                events[key]['segments'].append(origin)
            # Endpoints on a coincident interval belong to that interval event.
            for key in list(events):
                if key[0] == 'point':
                    intervals = [k for k in events if k[0]=='interval' and k[1]<=key[1]<=k[2]]
                    if intervals:
                        for k in intervals: events[k].setdefault('boundary_segments',[]).extend(events[key]['segments'])
                        del events[key]
        result = []
        for key in sorted(events, key=lambda k:(k[1],k[2])):
            result.append({**events[key], 'm_limit_knm': float(limit), 'm_limit_decimal': str(limit),
                           'provenance': copy.deepcopy(self.provenance), 'rule': copy.deepcopy(RULE)})
        return {'status': 'incomplete_missing_values' if gaps else 'resolved', 'crossings': result,
                'unresolved_segments': gaps, 'no_crossings_in_evaluable_segments': not result,
                'm_limit_knm': float(limit)}

    def positive_maximum(self):
        eligible = [p for p in self.points if p.get('value_knm') is not None and dec(p['value_knm']) > 0]
        maximum = max(eligible, key=lambda p:dec(p['value_knm'])) if eligible else None
        return {'Msk_max_discrete': copy.deepcopy(maximum),
                'interpolated_piecewise_max': copy.deepcopy(maximum) if all(m is not None for m in self.ms) else None,
                'piecewise_max_status': 'resolved' if all(m is not None for m in self.ms) else 'unresolved_missing_value',
                'interpretation': 'Máximo da representação linear; não máximo exato do diagrama estrutural real.'}


def diagram_from_tqs(mapping, tqs, positioned, raw):
    if mapping['beam_id'] != tqs['beam']['id'] or positioned['beam']['id'] != tqs['beam']['id']:
        raise ValueError('incompatible_beam_identity')
    if mapping['force_series'] != positioned['beam']['spans'][0]['internal_forces']:
        raise ValueError('mapping_positions_mismatch')
    index, series, proofs = audited_moment_series(mapping, tqs, raw)
    if len({len(series[k]) for k in ('sections','positions','values')}) != 1:
        raise ValueError('series_lengths_mismatch')
    points = [{'section':s, 'x_m':x, 'value_knm':m, 'source_type':'tqs_section',
               'provenance': {'series_pointer':f'/beam/spans/0/internal_forces/{index}',
                 'value_pointer':f'/beam/spans/0/internal_forces/{index}/values/{j}',
                 'position_pointer':f'/beam/spans/0/internal_forces/{index}/positions/{j}',
                 'sources':copy.deepcopy(series['sources']),
                 'position_sources':copy.deepcopy(positioned['provenance'].get(f'/beam/spans/0/internal_forces/{index}/positions',[]))}}
              for j,(s,x,m) in enumerate(zip(series['sections'],series['positions'],series['values']))]
    provenance = {'beam_id':tqs['beam']['id'], 'span_id':tqs['beam']['spans'][0]['id'],
        'series':{k:copy.deepcopy(v) for k,v in series.items() if k not in ('sections','positions','values')},
        'label_original':'M MX.', 'characteristic_level':'Msk confirmado pelo engenheiro',
        'evidence':[{'reference':p['reference'],'source':p['source']} for p in proofs]}
    return MomentDiagram(points, provenance)
