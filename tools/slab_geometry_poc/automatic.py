"""Small experimental sheet reader. No structural decisions; no color predicates.

The layout detector is an explicit sheet-family heuristic, not a universal layout
model. Failed anchors require a declared ROI, never silently use the whole page.
The original geometry.associate remains unchanged for the N26 experiment.
"""
import math
import re
from collections import Counter, defaultdict
from geometry import arrow_wings

MARK = re.compile(r'^N\s*(\d+)\b', re.I)
NUM = r'\d+(?:[.,]\d+)?'
SYMBOL = r'[Øø∅Φ\ufffd]'
FULL = re.compile(rf'^N\s*(\d+)\s+(\d+(?:\s*[x×]\s*\d+)*)\s*{SYMBOL}\s*({NUM})(?:\s+C/\s*({NUM}))?(?:\s+C\s*=\s*({NUM}))?$', re.I)


def center(box):
    return [(box[0]+box[2])/2, (box[1]+box[3])/2]


def contains(box, point):
    return box[0] <= point[0] <= box[2] and box[1] <= point[1] <= box[3]


def union(boxes):
    return [min(b[0] for b in boxes),min(b[1] for b in boxes),
            max(b[2] for b in boxes),max(b[3] for b in boxes)]


def local_box(box, direction):
    u=direction; v=[-u[1],u[0]]
    corners=[(box[0],box[1]),(box[2],box[1]),(box[2],box[3]),(box[0],box[3])]
    xs=[p[0]*u[0]+p[1]*u[1] for p in corners]
    ys=[p[0]*v[0]+p[1]*v[1] for p in corners]
    return [min(xs),min(ys),max(xs),max(ys)]


def detect_layout(texts, page_rect):
    headers={}
    for name in ('POS','BIT','QUANT','UNIT','TOTAL'):
        hits=[t for t in texts if t['text'].strip().upper()==name and t['bbox'][1]<page_rect[3]*.25]
        if len(hits)!=1:
            raise ValueError('layout_anchor_'+name+': declare ROI/table zone for this sheet')
        headers[name]=hits[0]
    title=[t for t in texts if 'Armadura positiva horizontal' in t['text'] and t['bbox'][0]<headers['POS']['bbox'][0]*.5]
    scales=[t for t in texts if re.search(r'ESCALA:\s*1/\d+',t['text']) and t['bbox'][0]<headers['POS']['bbox'][0]*.5]
    notes=[t for t in texts if t['text'].strip().startswith(('DETALHE ','COBRIMENTO ARMADURA'))]
    if not title or len(scales)!=1 or not notes:
        raise ValueError('main_plan_anchors_missing')
    summaries=[t['bbox'][1] for t in texts if 'RESUMO' in t['text'] and t['bbox'][0]>headers['POS']['bbox'][0]-150]
    table_bottom=min(summaries) if summaries else page_rect[3]
    rows=[t for t in texts if re.fullmatch(r'\d+',t['text'].strip())
          and abs(center(t['bbox'])[0]-center(headers['POS']['bbox'])[0])<20
          and headers['POS']['bbox'][3]+40<t['bbox'][1]<table_bottom]
    if not rows:
        raise ValueError('steel_table_rows_missing')
    table_box=[headers['POS']['bbox'][0]-4,min(t['bbox'][1] for t in rows)-1,
               headers['TOTAL']['bbox'][2]+15,max(t['bbox'][3] for t in rows)+1]
    # Main plan ends before right-side table and bottom construction-detail strip.
    roi=[page_rect[0]+30,max(scales[0]['bbox'][3],min(t['bbox'][3] for t in title))+10,
         headers['POS']['bbox'][0]-110,min(t['bbox'][1] for t in notes)-20]
    return dict(detail_roi_pt=roi,steel_table_roi_pt=table_box,
                scale_denominator=int(re.search(r'1/(\d+)',scales[0]['text'])[1]),
                source='SHEET_FAMILY_TEXT_ANCHORS',
                anchor_ids=[t['id'] for t in headers.values()]+[scales[0]['id']]+[t['id'] for t in notes],
                limitation='Layout uses this sheet family header words and main plan title; not a universal detector.')


def parse_extended(text):
    """Preserve incomplete data; a printed 2x3 is factors, not physical grouping."""
    text=' '.join(text.split())
    mark=MARK.match(text)
    if not mark:
        return None
    result=dict(mark='N'+mark[1],quantity=None,quantity_expression=None,
                quantity_factors=None,diameter_mm=None,spacing_cm=None,nominal_length_cm=None,
                parse_complete=False,diameter_symbol_decoded='\ufffd' not in text)
    m=FULL.fullmatch(text)
    if m:
        _,expr,diam,spacing,length=m.groups()
        factors=[int(v) for v in re.split(r'\s*[x×]\s*',expr)]
        result.update(quantity_expression=expr,quantity_factors=factors,
                      quantity=math.prod(factors),diameter_mm=float(diam.replace(',','.')),
                      spacing_cm=float(spacing.replace(',','.')) if spacing else None,
                      nominal_length_cm=float(length.replace(',','.')) if length else None,
                      parse_complete=length is not None)
    else:
        q=re.match(r'^N\s*\d+\s+(\d+(?:\s*[x×]\s*\d+)*)\s*'+SYMBOL,text,re.I)
        if q:
            fs=[int(v) for v in re.split(r'\s*[x×]\s*',q[1])]
            result.update(quantity_expression=q[1],quantity_factors=fs,quantity=math.prod(fs))
        for key,pattern in [('diameter_mm',SYMBOL+rf'\s*({NUM})'),('spacing_cm',rf'C/\s*({NUM})'),('nominal_length_cm',rf'C\s*=\s*({NUM})')]:
            match=re.search(pattern,text,re.I)
            if match: result[key]=float(match[1].replace(',','.'))
    result['missing_fields']=[key for key in ('quantity','diameter_mm','nominal_length_cm') if result[key] is None]
    if not result['parse_complete'] and not result['missing_fields']:
        result['missing_fields']=['unsupported_text_syntax']
    return result


def inventory(texts, roi, excluded_zones=()):
    eligible=[t for t in texts if contains(roi,center(t['bbox'])) and not any(contains(z,center(t['bbox'])) for z in excluded_zones)]
    seeds=[t for t in eligible if MARK.match(t['text'].strip())]
    continuations=[t for t in eligible if re.match(rf'^\s*(?:{SYMBOL}|C\s*[/=])',t['text'],re.I)]
    # Continuation belongs to a seed only if it has exactly one plausible owner.
    owners=defaultdict(list)
    for t in continuations:
        for seed in seeds:
            if sum(a*b for a,b in zip(t['direction'],seed['direction']))<.995:
                continue
            a=local_box(seed['bbox'],seed['direction']); b=local_box(t['bbox'],seed['direction'])
            h=a[3]-a[1]
            if .3*h <= b[1]-a[1] <= 2.4*h and max(a[0],b[0]) <= min(a[2],b[2])+h:
                owners[t['id']].append(seed['id'])
    occurrences=[]
    for seed in sorted(seeds,key=lambda t:(t['bbox'][1],t['bbox'][0],t['id'])):
        parts=[seed]+[t for t in continuations if owners[t['id']]==[seed['id']]]
        parts.sort(key=lambda t:local_box(t['bbox'],seed['direction'])[1])
        text=' '.join(t['text'].strip() for t in parts)
        call=parse_extended(text)
        occurrence=dict(occurrence_id='P1-'+seed['id'],documentary_mark=call['mark'],
            physical_occurrence_id=None,identity_state='TEXTUAL_REPRESENTATION_NOT_PROVED_PHYSICAL_IDENTITY',
            text=text,text_ids=[t['id'] for t in parts],bbox=union([t['bbox'] for t in parts]),
            direction=seed['direction'],call=call,continuation_alternatives=[t['id'] for t in continuations if seed['id'] in owners[t['id']] and len(owners[t['id']])>1],
            manual_validation=dict(status='PENDING',reviewer=None,method=None,selected_pair=None,notes=None),
            status='UNRESOLVED',candidates=[],associations=[],region_pdf_pt=None)
        occurrences.append(occurrence)
    used={id for o in occurrences for id in o['text_ids']}
    return dict(occurrences=occurrences,excluded_call_like=[t for t in texts if MARK.match(t['text'].strip()) and t not in eligible],
                unowned_continuations=[dict(**t,plausible_owner_ids=owners[t['id']]) for t in continuations if t['id'] not in used])


def line_geometry(segments, tolerance=.15, max_gap=.3):
    """Merge endpoint-connected, collinear fragments, retaining all source IDs.

    No bridging of wider gaps or reconstruction from nominal C. Coincident copies
    coalesce; partially overlapping distinct segments stay as alternatives.
    """
    # Adjacent distribution axes can touch at opposing arrowheads. Joining at
    # these tips would incorrectly extend the N26 region into its neighbour.
    short_diagonals=[s for s in segments if 2<s['length_pt']<10 and
                     .2<abs(s['a'][0]-s['b'][0])<10 and .2<abs(s['a'][1]-s['b'][1])<10]
    endpoint_counts=Counter((round(p[0],1),round(p[1],1)) for s in short_diagonals for p in (s['a'],s['b']))
    protected=[p for p,n in endpoint_counts.items() if n>=2]
    groups=defaultdict(list)
    for s in segments:
        a,b=s['a'],s['b']
        orientation=0 if abs(a[1]-b[1])<=tolerance else 1 if abs(a[0]-b[0])<=tolerance else None
        if orientation is None or s['length_pt']<.5: continue
        v=1-orientation
        groups[(orientation,round((a[v]+b[v])/2,1))].append((min(a[orientation],b[orientation]),max(a[orientation],b[orientation]),s))
    result=[]
    for (orientation,constant),members in sorted(groups.items()):
        clusters=[]
        for lo,hi,s in sorted(members,key=lambda m:(m[0],m[1],m[2]['id'])):
            exact=next((c for c in clusters if abs(lo-c[0])<tolerance and abs(hi-c[1])<tolerance),None)
            if exact is not None: exact[2].append(s); continue
            joint=[lo,constant] if orientation==0 else [constant,lo]
            has_arrow_tip=any(math.dist(joint,p)<.25 for p in protected)
            adjacent=next((c for c in reversed(clusters) if -.01<=lo-c[1]<=max_gap),None) if not has_arrow_tip else None
            if adjacent is not None: adjacent[1]=hi; adjacent[2].append(s)
            else: clusters.append([lo,hi,[s]])
        for lo,hi,ss in clusters:
            if len(ss)==1:
                a,b=ss[0]['a'],ss[0]['b']
            else:
                value=sum((s['a'][1-orientation]+s['b'][1-orientation])/2 for s in ss)/len(ss)
                a,b=([lo,value],[hi,value]) if orientation==0 else ([value,lo],[value,hi])
            result.append(dict(id='+'.join(sorted(s['id'] for s in ss)),source_ids=sorted(s['id'] for s in ss),
                a=a,b=b,length_pt=math.dist(a,b),orientation=orientation,
                angle_deg=math.degrees(math.atan2(b[1]-a[1],b[0]-a[0])),fragment_count=len(ss)))
    return result


def distribution_axes(lines, segments):
    # Reuse legacy arrow recognizer. Rotate horizontal axes/segments into its frame.
    rotated=[dict(s,a=[-s['a'][1],s['a'][0]],b=[-s['b'][1],s['b'][0]]) for s in segments]
    result=[]
    for line in lines:
        if line['length_pt']<12: continue
        axis=line if line['orientation']==1 else dict(line,a=[-line['a'][1],line['a'][0]],b=[-line['b'][1],line['b'][0]])
        wings=arrow_wings(axis,segments if line['orientation']==1 else rotated)
        if wings: result.append(dict(**line,arrow_wing_ids=wings))
    return result


def junctions(paths):
    return [p for p in paths if len(p['items'])>=3 and all(it[0]=='c' for it in p['items'])
            and .5<p['bbox'][2]-p['bbox'][0]<4 and .5<p['bbox'][3]-p['bbox'][1]<4]


def bar_axis_intersection(bar, axis, tolerance=.15):
    """Interior orthogonal crossing, shared by baseline and leader readers."""
    k=bar['orientation'];j=1-k
    if axis['orientation']==k:return None
    point=[0,0];point[k]=axis['a'][k];point[j]=bar['a'][j]
    if (min(bar['a'][k],bar['b'][k])+tolerance<point[k]<max(bar['a'][k],bar['b'][k])-tolerance
            and min(axis['a'][j],axis['b'][j])+tolerance<point[j]<max(axis['a'][j],axis['b'][j])-tolerance):
        return point
    return None


def graphic_envelope(bar,axis):
    k=bar['orientation'];j=1-k
    lo,hi=sorted([axis['a'][j],axis['b'][j]])
    bl,bh=sorted([bar['a'][k],bar['b'][k]])
    return [[bl,lo],[bh,lo],[bh,hi],[bl,hi]] if k==0 else [[lo,bl],[hi,bl],[hi,bh],[lo,bh]]


def associate_occurrence(o, lines, axes, markers, scale=50):
    """Candidate enumeration independent of color, C equivalence and nearest choice."""
    direction=o['direction']; box=local_box(o['bbox'],direction)
    call=o['call']; candidates=[]; pairs=[]
    if max(abs(direction[0]),abs(direction[1]))<.995:
        o['reason']='OBLIQUE_TEXT_UNSUPPORTED'; return o
    for bar in lines:
        if bar['length_pt']<8: continue
        ab=local_box(union([[*bar['a'],*bar['a']],[*bar['b'],*bar['b']]]),direction)
        if ab[3]-ab[1]>.2: continue
        gap=ab[1]-box[3]
        overlap=max(0,min(ab[2],box[2])-max(ab[0],box[0]))
        if not (-3<=gap<=22 and overlap>=min(15,(box[2]-box[0])*.35)):
            continue
        cm=bar['length_pt']*2.54/72*scale
        length=call['nominal_length_cm']
        candidate=dict(bar=bar,text_gap_pt=gap,text_overlap_pt=overlap,
                       projected_length_cm=cm,nominal_length_relative_error=abs(cm-length)/length if length else None,
                       projected_exceeds_nominal=bool(length and cm>length*1.05),
                       distribution_candidates=[])
        candidates.append(candidate)
        k=bar['orientation']; j=1-k
        for axis in axes:
            point=bar_axis_intersection(bar,axis)
            if point is None:continue
            mark_ids=[p['id'] for p in markers if math.dist(center(p['bbox']),point)<.42]
            evidence=dict(axis=axis,junction_path_ids=mark_ids,intersection_pt=point,
                          label_alignment='NEAR_BASELINE' if gap<=8 else 'DISPLACED_TEXT',
                          length_agreement_auxiliary=candidate['nominal_length_relative_error'] is not None and candidate['nominal_length_relative_error']<.015)
            candidate['distribution_candidates'].append(evidence)
            # Marker absence never fabricates a positive result: keep partial.
            sufficient=bool(mark_ids) and gap<=8 and call['parse_complete'] and not candidate['projected_exceeds_nominal']
            if sufficient:
                polygon=graphic_envelope(bar,axis)
                pairs.append(dict(bar=bar,evidence=evidence,region_pdf_pt=polygon,
                                  region_nature='GRAPHIC_ENVELOPE_NOT_PROVED_PHYSICAL_GEOMETRY'))
    o['candidates']=candidates;o['associations']=pairs
    # Multiple marked intersections are ambiguous even for displaced or incomplete text.
    plausible=[(c,e) for c in candidates for e in c['distribution_candidates'] if e['junction_path_ids']]
    if any(c['projected_exceeds_nominal'] for c,e in plausible):
        o['status']='AMBIGUOUS';o['reason']='MARKED_LINK_WITH_PROJECTED_LENGTH_CONTRADICTION'
    elif len(plausible)>1 or len(pairs)>1 or o['continuation_alternatives']:
        o['status']='AMBIGUOUS';o['reason']='MULTIPLE_PLAUSIBLE_LINKS_OR_TEXT_CONTINUATIONS'
    elif len(pairs)==1:
        o['status']='ASSOCIATED';o['region_pdf_pt']=pairs[0]['region_pdf_pt'];o['reason']='ALIGNED_CALL_DOUBLE_ARROW_AND_JUNCTION'
    elif len(candidates)>1:
        o['status']='AMBIGUOUS';o['reason']='MULTIPLE_WEAK_BAR_CANDIDATES'
    elif candidates:
        o['status']='PARTIAL';o['reason']='BAR_CANDIDATES_WITHOUT_SUFFICIENT_COMPLETE_LINK'
    else:
        o['status']='UNRESOLVED';o['reason']='NO_SUPPORTED_BAR_CANDIDATE'
    return o


def read_sheet(data, layout):
    result=inventory(data['texts'],layout['detail_roi_pt'],[layout['steel_table_roi_pt']])
    lines=line_geometry(data['segments']);axes=distribution_axes(lines,data['segments']);markers=junctions(data['paths'])
    for o in result['occurrences']:
        associate_occurrence(o,lines,axes,markers,layout['scale_denominator'])
    # Detect complete links claimed by different textual representations; do not
    # decide that they are distinct physical occurrences or silently deduplicate.
    owners=defaultdict(list)
    for o in result['occurrences']:
        if o['status']=='ASSOCIATED':
            pair=o['associations'][0]
            owners[(pair['bar']['id'],pair['evidence']['axis']['id'])].append(o)
    for group in owners.values():
        if len(group)>1:
            for o in group:
                o.update(status='AMBIGUOUS',reason='GEOMETRY_SHARED_BY_TEXTUAL_REPRESENTATIONS',region_pdf_pt=None)
    result['geometry_counts']=dict(lines=len(lines),double_arrow_axes=len(axes),junction_paths=len(markers))
    result['status_counts']=dict(Counter(o['status'] for o in result['occurrences']))
    result['layout']=layout
    return result


def compare_schedule(occurrences, observations):
    """Keep repeated quantities separate; never sum textual representations."""
    calls=defaultdict(list);table=defaultdict(list)
    for o in occurrences: calls[o['documentary_mark']].append(o)
    for row in observations: table[row['mark']].append(row)
    rows=[]
    for mark in sorted(set(calls)|set(table),key=lambda m:int(m[1:])):
        local=calls[mark];schedule=table[mark];issues=[]
        for o in local:
            for row in schedule:
                for key in ('diameter_mm','nominal_length_cm'):
                    value=o['call'][key]
                    if value is not None and value!=row[key]: issues.append(dict(occurrence_id=o['occurrence_id'],field=key,call=value,table=row[key]))
        amounts=[o['call']['quantity'] for o in local]
        rows.append(dict(mark=mark,occurrence_ids=[o['occurrence_id'] for o in local],
            schedule=schedule,call_quantities=amounts,
            quantity_comparison='NOT_COMPARED_REPEATED_REPRESENTATIONS' if len(local)>1 else 'SINGLE_REPRESENTATION_DOCUMENTARY_COMPARISON',
            single_call_quantity_matches_table=(amounts[0]==schedule[0]['quantity']) if len(local)==len(schedule)==1 and amounts[0] is not None else None,
            physical_quantity_comparison='NOT_CONCLUDED_NO_PROVED_OCCURRENCE_IDENTITY_OR_MULTIPLICITY',
            discrepancies=issues,missing_in_table=not schedule,missing_call=not local))
    return dict(rows=rows,positions_without_call=[r['mark'] for r in rows if r['missing_call']],
                calls_without_table=[r['mark'] for r in rows if r['missing_in_table']])
