"""Experimental PDF geometry only. No resistance or automatic sheet-wide reading.

All coordinates are unrotated PyMuPDF page points, origin top left, y down.
The caller must select one label occurrence. Color and PDF drawing order are
deliberately excluded from association decisions.
"""
import math
import re


CALL = re.compile(r'N(?P<mark>\d+)\s+(?P<quantity>\d+)\s+[Øø∅Φ\ufffd]\s*(?P<diameter>[\d.,]+)\s+C/(?P<spacing>[\d.,]+)\s+C=(?P<length>[\d.,]+)', re.I)


def parse_call(text):
    m = CALL.fullmatch(text.strip())
    if not m:
        return None
    v = m.groupdict()
    return dict(mark='N'+v['mark'], quantity=int(v['quantity']),
                diameter_mm=float(v['diameter'].replace(',', '.')),
                spacing_cm=float(v['spacing'].replace(',', '.')),
                nominal_length_cm=float(v['length'].replace(',', '.')),
                diameter_symbol_decoded='\ufffd' not in text)


def extract_page(page):
    texts = []
    for bi, block in enumerate(page.get_text('dict')['blocks']):
        for li, line in enumerate(block.get('lines', [])):
            texts.append(dict(id=f'T{bi}:{li}', text=''.join(s['text'] for s in line['spans']),
                              bbox=list(line['bbox']), direction=list(line['dir'])))
    paths, segments = [], []
    for di, drawing in enumerate(page.get_drawings()):
        items = []
        for ii, item in enumerate(drawing['items']):
            # Retain curves, rectangles and quads too, without flattening them.
            values = [list(v) if hasattr(v, '__len__') else v for v in item[1:]]
            items.append([item[0], *values])
            if item[0] == 'l':
                a, b = [list(v) for v in item[1:3]]
                segments.append(dict(id=f'D{di}:{ii}', path_id=f'D{di}', a=a, b=b,
                                     length_pt=math.dist(a, b),
                                     angle_deg=math.degrees(math.atan2(b[1]-a[1], b[0]-a[0]))))
        paths.append(dict(id=f'D{di}', seqno=drawing.get('seqno'), items=items,
                          bbox=list(drawing['rect']), color=drawing.get('color'),
                          fill=drawing.get('fill'), width=drawing.get('width'),
                          closePath=drawing.get('closePath'), dashes=drawing.get('dashes')))
    return dict(texts=texts, paths=paths, segments=segments)


def arrow_wings(axis, segments, tolerance=.15):
    """Two short non-collinear wings sharing each endpoint, directed inward.

    Restricted to vertical axes. This is a shape predicate, not a general arrow
    recognizer. Return actual segment IDs so the result can be audited.
    """
    if abs(axis['a'][0]-axis['b'][0]) > tolerance:
        return None
    result = []
    ends = sorted([axis['a'], axis['b']], key=lambda p: p[1])
    for ei, tip in enumerate(ends):
        wings = []
        for s in segments:
            if not 2 < s['length_pt'] < 10:
                continue
            for at, other in ((s['a'], s['b']), (s['b'], s['a'])):
                dx, dy = other[0]-tip[0], other[1]-tip[1]
                if math.dist(at, tip) <= tolerance and .2 < abs(dx) < 3 and (dy > 0 if ei == 0 else dy < 0):
                    wings.append((dx, s['id']))
        if not any(a[0]*b[0] < 0 for a in wings for b in wings):
            return None
        result.append(sorted(w[1] for w in wings))
    return result


def associate(label, data, scale_denominator=50):
    """Enumerate candidates; never silently choose among surviving alternatives.

    Label alignment only nominates bars. Acceptance also requires an intersecting
    double-arrow axis, small curved junction marker, and nominal-length agreement.
    All thresholds are experimental graphical tolerances, not normative limits.
    """
    call = parse_call(label['text'])
    if call is None or scale_denominator <= 0:
        raise ValueError('unsupported_call_or_scale')
    x0, y0, x1, y1 = label['bbox']
    segs = data['segments']
    candidates, pairs = [], []
    for bar in segs:
        a, b = bar['a'], bar['b']
        left, right = sorted([a[0], b[0]])
        if abs(a[1]-b[1]) > .15 or bar['length_pt'] < 20:
            continue
        gap = a[1]-y1
        if not (-2 <= gap <= 8 and left <= x0 and right >= x1):
            continue
        cm = bar['length_pt']*2.54/72*scale_denominator
        candidate = dict(bar_id=bar['id'], text_gap_pt=gap,
                         projected_length_cm=cm,
                         nominal_length_relative_error=abs(cm-call['nominal_length_cm'])/call['nominal_length_cm'],
                         distribution_candidates=[])
        candidates.append(candidate)
        for axis in segs:
            if abs(axis['a'][0]-axis['b'][0]) > .15 or axis['length_pt'] < 20:
                continue
            x = axis['a'][0]
            lo, hi = sorted([axis['a'][1], axis['b'][1]])
            if not (left < x < right and lo < a[1] < hi):
                continue
            wings = arrow_wings(axis, segs)
            if wings is None:
                continue
            markers = []
            for path in data['paths']:
                box = path['bbox']
                if (len(path['items']) >= 3 and all(it[0] == 'c' for it in path['items'])
                        and .5 < box[2]-box[0] < 4 and .5 < box[3]-box[1] < 4
                        and abs((box[0]+box[2])/2-x) < .3
                        and abs((box[1]+box[3])/2-a[1]) < .3):
                    markers.append(path['id'])
            ev = dict(axis_id=axis['id'], arrow_wing_ids=wings, junction_path_ids=markers)
            candidate['distribution_candidates'].append(ev)
            if markers and candidate['nominal_length_relative_error'] <= .01:
                pairs.append(dict(bar=bar, axis=axis, evidence=ev,
                                  region_pdf_pt=[[left,lo],[right,lo],[right,hi],[left,hi]]))
    return dict(call=call, label=label, candidates=candidates, accepted_pairs=pairs,
                status='UNIQUE_GRAPHICAL_INTERPRETATION_REQUIRES_ENGINEER_REVIEW' if len(pairs)==1 else 'AMBIGUOUS_OR_UNRESOLVED',
                thresholds=dict(axis_pt=.15, text_gap_pt=[-2,8], nominal_length_relative=.01,
                                junction_center_pt=.3, arrow_length_pt=[2,10]),
                scale_denominator=scale_denominator)
