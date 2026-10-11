"""Shear-series adapter reusing existing linear interpolation/crossings intact."""
from copy import deepcopy
from moment_diagram import MomentDiagram,dec

RULE='engineer_confirmed_tqs_shear_domain_v1'

class ShearDiagram:
    def __init__(self,series):
        if not series:raise ValueError('missing_shear_series')
        self.series=deepcopy(series);self.diagrams=[];seen=set()
        for index,item in enumerate(series):
            if item.get('quantity')!='shear' or item.get('unit')!='kN' or not item.get('provenance'):
                raise ValueError('shear_quantity_units_or_source_unresolved')
            xs,values,sections=(item[k] for k in ('positions','values','sections'))
            if len(xs)!=len(values) or len(xs)!=len(sections) or len(set(sections))!=len(sections):raise ValueError('invalid_shear_lengths')
            identity=item.get('series_id',item.get('envelope'))
            if identity is None or identity in seen:raise ValueError('missing_or_duplicate_shear_series_identity')
            seen.add(identity)
            points=[{'x_m':x,'value_knm':v,'section':s,'provenance':{'sample_index':j,'series':deepcopy(item['provenance'])}} for j,(x,v,s) in enumerate(zip(xs,values,sections))]
            linear=MomentDiagram(points,{'quantity':'shear','unit':'kN','series_id':identity,'source':deepcopy(item['provenance']),
                                         'discontinuities_m':deepcopy(item.get('discontinuities_m', []))})
            self.diagrams.append((identity,linear))
        self.domain=[float(min(d.xs[0] for _,d in self.diagrams)),float(max(d.xs[-1] for _,d in self.diagrams))]

    def maximum(self,start,end,*,allow_intersection=False):
        a,b=dec(start),dec(end)
        if a>=b:raise ValueError('invalid_shear_interval')
        out={'status':'INCONCLUSIVE','requested_interval_m':[start,end],'series_coverage':[],
             'governing':[],'Vsk_abs_kn':None,'complete':False,'rule':RULE,'provenance':{'series':deepcopy(self.series)}}
        points=[];complete=True
        for identity,diagram in self.diagrams:
            x,y=max(a,diagram.xs[0]),min(b,diagram.xs[-1])
            coverage={'series_id':identity,'sampled_domain_m':[float(diagram.xs[0]),float(diagram.xs[-1])],
                'check_interval_m':None,'uncovered_intervals_m':[],'unresolved_queries':[]}
            if x>=y:
                complete=False;coverage['uncovered_intervals_m']=[[float(a),float(b)]]
            else:
                coverage['check_interval_m']=[float(x),float(y)]
                if x>a:coverage['uncovered_intervals_m'].append([float(a),float(x)])
                if y<b:coverage['uncovered_intervals_m'].append([float(y),float(b)])
                if coverage['uncovered_intervals_m']:complete=False
                queries=[diagram.moment_at_x(float(q)) for q in sorted({x,y,*[q for q in diagram.xs if x<=q<=y],
                    *[dec(q) for q in diagram.provenance.get('discontinuities_m', []) if x<=dec(q)<=y]})]
                for p in queries:
                    if p['status']!='resolved':
                        complete=False;coverage['unresolved_queries'].append(p);continue
                    value=p['value_knm']
                    points.append({'series_id':identity,'x_m':p['x_m'],'section':p.get('section'),
                        'Vsk_original_kn':value,'Vsk_abs_kn':abs(value),'sign':1 if value>0 else -1 if value<0 else 0,
                        'source_type':p['source_type'],'provenance':p})
            out['series_coverage'].append(coverage)
        if points:
            maximum=max(p['Vsk_abs_kn'] for p in points)
            out.update(Vsk_abs_kn=maximum,governing=[p for p in points if p['Vsk_abs_kn']==maximum])
        out.update(complete=complete,status='PASS' if complete else 'INCONCLUSIVE',
            partial_results_only=not complete,intersection_requested=allow_intersection)
        return out

    def capacity_crossings(self,capacity):
        if dec(capacity)<0:raise ValueError('negative_shear_capacity')
        out=[]
        for identity,diagram in self.diagrams:
            for sign in (1,-1):
                events=diagram.find_crossings(sign*capacity)
                for event in events['crossings']:
                    out.append({'series_id':identity,'signed_limit_kn':sign*capacity,
                        'Vsk_abs_limit_kn':capacity,'event':event,'incomplete_series':bool(events['unresolved_segments'])})
        return out
