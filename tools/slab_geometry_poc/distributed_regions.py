"""Traceable rectangular arrangement in original PDF points; no steel summation.

The backend deliberately rejects nonrectangular envelopes instead of repairing them.
Composition rectangles partition the union, not the structural slab domain.
"""
import copy
import math
from automatic import graphic_envelope, bar_axis_intersection


def rectangle(points):
    if not points or len(points) != 4 or any(len(p) != 2 for p in points):
        raise ValueError('INCOMPLETE_POLYGON')
    if not all(math.isfinite(v) for p in points for v in p):
        raise ValueError('NONFINITE_COORDINATES')
    xs=sorted(set(p[0] for p in points));ys=sorted(set(p[1] for p in points))
    if len(xs)!=2 or len(ys)!=2:
        raise ValueError('NOT_AXIS_ALIGNED_RECTANGLE')
    if len(set(map(tuple,points)))!=4 or any(a[0]!=b[0] and a[1]!=b[1] for a,b in zip(points,points[1:]+points[:1])):
        raise ValueError('INVALID_RING')
    return [xs[0],ys[0],xs[1],ys[1]]


def polygon(b):
    return [[b[0],b[1]],[b[2],b[1]],[b[2],b[3]],[b[0],b[3]]]


def area(b):return (b[2]-b[0])*(b[3]-b[1])


def intersection(a,b):
    c=[max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3])]
    return c if c[2]>c[0] and c[3]>c[1] else None


def partition(regions):
    """Exact edge arrangement, row runs merged vertically; no coordinate snapping.

    Disconnected pieces with the same membership intentionally retain distinct IDs.
    Membership uses graphic occurrences; physical identity is a separate relation.
    """
    regions=sorted(regions,key=lambda r:r['id'])
    xs=sorted({v for r in regions for v in (r['bbox'][0],r['bbox'][2])})
    ys=sorted({v for r in regions for v in (r['bbox'][1],r['bbox'][3])})
    finished=[];active={}
    for y0,y1 in zip(ys,ys[1:]):
        runs=[]
        for x0,x1 in zip(xs,xs[1:]):
            members=tuple(r['id'] for r in regions if r['bbox'][0]<=x0 and r['bbox'][2]>=x1 and r['bbox'][1]<=y0 and r['bbox'][3]>=y1)
            if not members:continue
            if runs and runs[-1][0]==members and runs[-1][1][2]==x0:runs[-1][1][2]=x1
            else:runs.append((members,[x0,y0,x1,y1]))
        current={}
        for members,b in runs:
            key=(members,b[0],b[2])
            if key in active:
                old=active.pop(key);old[1][3]=y1;current[key]=old
            else:current[key]=(members,b)
        finished.extend(active.values());active=current
    finished.extend(active.values())
    return [{'id':f'C{i:03d}','region_ids':list(m),'bbox':b,'polygon_pdf_pt':polygon(b),'area_pt2':area(b)}
            for i,(m,b) in enumerate(sorted(finished,key=lambda v:(v[1][1],v[1][0],v[0])),1)]


def reconstruct(inventory):
    result=copy.deepcopy(inventory);regions=[];pending=[]
    for o in sorted(inventory['occurrences'],key=lambda o:o['display_id']):
        if o.get('representation_kind')!='DISTRIBUTED':continue
        try:
            if o['status']!='ASSOCIATED':raise ValueError('ASSOCIATION_NOT_COMPLETE')
            leader=o.get('leader_association')
            if leader:
                bar=leader['target'];choices=leader['distribution_candidates']
                if len(choices)!=1:raise ValueError('MULTIPLE_DISTRIBUTIONS')
                axis=choices[0]['axis'];source='leader_association'
            else:
                choices=o['associations']
                if len(choices)!=1:raise ValueError('MULTIPLE_ASSOCIATIONS')
                bar=choices[0]['bar'];axis=choices[0]['evidence']['axis'];source='associations[0]'
            for line in (bar,axis):
                k=line['orientation']
                if k not in (0,1) or line['a'][1-k]!=line['b'][1-k] or line['a'][k]==line['b'][k]:
                    raise ValueError('INCONSISTENT_LINE_ORIENTATION')
            if bar_axis_intersection(bar,axis) is None:raise ValueError('NO_INTERIOR_CROSSING')
            b=rectangle(o.get('region_pdf_pt'));expected=rectangle(graphic_envelope(bar,axis))
            if any(abs(a-c)>1e-7 for a,c in zip(b,expected)):raise ValueError('ENVELOPE_CONTRADICTS_LINES')
            call=o['call'];signature=(o['documentary_mark'],tuple(sorted(bar.get('source_ids',[bar['id']]))),tuple(sorted(axis.get('source_ids',[axis['id']]))),call.get('diameter_mm'),call.get('spacing_cm'),call.get('nominal_length_cm'))
            regions.append({'id':'R'+o['display_id'][1:],'occurrence_id':o['occurrence_id'],'display_id':o['display_id'],
                'position':o['documentary_mark'],'bbox':b,'polygon_pdf_pt':copy.deepcopy(o['region_pdf_pt']),
                'area_pt2':area(b),'bar':copy.deepcopy(bar),'distribution_axis':copy.deepcopy(axis),
                'orientation':bar['orientation'],'longitudinal_extent_pt':abs(bar['b'][bar['orientation']]-bar['a'][bar['orientation']]),
                'transverse_extent_pt':abs(axis['b'][axis['orientation']]-axis['a'][axis['orientation']]),
                'diameter_mm':call.get('diameter_mm'),'spacing_cm':call.get('spacing_cm'),
                'nominal_length_cm':call.get('nominal_length_cm'),'layer':None,
                'reinforcement_role':'POSITIVE_HORIZONTAL_SHEET_CONTEXT','source':{'branch':source,'text_ids':o['text_ids'],'text':o['text']},
                'confidence':'EXPERIMENTAL_GRAPHIC_INTERPRETATION_PENDING_ENGINEER',
                '_identity':signature,'physical_independence_proved':False})
        except (KeyError,ValueError,TypeError,IndexError) as error:
            pending.append({'display_id':o['display_id'],'occurrence_id':o['occurrence_id'],'reason':str(error),'bbox':o['bbox']})
    identities={};groups=[]
    for r in regions:
        signature=r.pop('_identity')
        if signature not in identities:
            identities[signature]=f'I{len(identities)+1:03d}'
            groups.append({'id':identities[signature],'region_ids':[],'basis':'SAME_DOCUMENTARY_PROPERTIES_AND_RAW_BAR_AXIS_ENTITIES','physical_identity_engineer_confirmed':False})
        r['identity_group']=identities[signature];groups[int(r['identity_group'][1:])-1]['region_ids'].append(r['id'])
    cells=partition(regions);lookup={r['id']:r for r in regions}
    for c in cells:
        members=[lookup[id] for id in c['region_ids']]
        c.update(positions=sorted(set(r['position'] for r in members)),occurrences=[r['display_id'] for r in members],
                 identity_groups=sorted(set(r['identity_group'] for r in members)),
                 direction_layer_sets=[{'orientation':k,'layer':None,'region_ids':[r['id'] for r in members if r['orientation']==k]} for k in sorted(set(r['orientation'] for r in members))],
                 contributors=[{k:r[k] for k in ('id','position','occurrence_id','orientation','diameter_mm','spacing_cm','layer','source')} for r in members],
                 physical_addition_authorized=False,confidence='GEOMETRIC_PARTITION_OF_EXPERIMENTAL_ENVELOPES')
        c['possible_duplicate_pairs']=[[a['id'],b['id']] for i,a in enumerate(members) for b in members[i+1:] if a['position']==b['position'] and a['identity_group']!=b['identity_group']]
    holes=inventory.get('localized_reconstruction',{}).get('openings',[])
    impacts=[]
    for r in regions:
        for h in holes:
            b=intersection(r['bbox'],h['bbox'])
            if b:impacts.append({'region_id':r['id'],'opening_id':h['id'],'intersection_pdf_pt':polygon(b),'area_pt2':area(b),'subtracted':False,'opening_validation':h.get('validation')})
    n38=[o for o in inventory['occurrences'] if o.get('documentary_mark')=='N38']
    ledger=[{'position':'N38','original_calls':[{'text':o['text'],'call':o['call']} for o in n38],
             'engineer_confirmation':{'groups':4,'bars_per_group':3,'total_bars':12,'source':'João, solicitação Etapa 5, seção 10'},
             'state':'DOCUMENTARY_MULTIPLICITY_CONFLICT','physical_groups_created':False,'original_data_corrected':False}]
    result['distributed_spatial_analysis']={'backend':'EXACT_AXIS_ALIGNED_RECTANGLE_EDGE_ARRANGEMENT','units':'PDF_PT_AND_PT2','regions':regions,'pending':pending,
        'composition_regions':cells,'identity_groups':groups,'opening_intersections':impacts,
        'structural_domain':{'state':'UNRESOLVED_REQUIRES_FORMWORK_PLAN','slab_assignments':[],'openings_complete':False,'opening_subtraction':False},
        'metrics':{'distributed_candidates':len(regions)+len(pending),'valid_regions':len(regions),'pending':len(pending),'composition_regions':len(cells),'overlap_regions':sum(len(c['identity_groups'])>1 for c in cells),'union_area_pt2':sum(c['area_pt2'] for c in cells),'opening_intersections':len(impacts),'accuracy':None,'independently_validated_compositions':0}}
    result['stage5_documentary_consistency']=ledger
    return result
