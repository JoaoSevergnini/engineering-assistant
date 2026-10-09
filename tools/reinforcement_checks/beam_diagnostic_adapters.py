"""Explicit read-only adapters for the validated historical JSON contracts."""
from beam_diagnostic import STATES


def ref(source, *, pointer):
    return dict(source,pointer=source.get('pointer','').rstrip('/')+pointer)


def state(value):
    if value in STATES:return value
    if value is True:return 'PASS'
    if value is False:return 'FAIL'
    if value is None:return 'INCONCLUSIVE'
    raise ValueError('unknown_original_state')


def envelope(context,discipline,source,checks,*,complete=True,original_summary=None):
    return dict(discipline=discipline,beam_id=context['beam_id'],floor=context['floor'],
        coordinate_system=context['coordinate_system'],source=source,version='historical-json-adapter-v1',
        complete=complete,checks=checks,original_summary=original_summary)


def check(kind,key,data,source,*,span=None,interval=None,marks=(),required=None,provided=None,unit=None,comparison=None):
    status=state(data.get('status',data.get('passes')))
    return dict(check_id=key,check_type=kind,status=status,span_id=span,physical_interval=interval,
        drawing_reinforcement_ids=list(marks),required_value=required,provided_value=provided,units=unit,
        comparison=comparison,reason=data.get('reason') or data.get('criterion') or data.get('rule'),
        criterion=data.get('rule') or data.get('criterion'),
        evidence={'original_control':data,'original_status':data.get('status'),'source':source},
        demand_source=source,drawing_source=source,calculation_source=source,
        missing_information=([data.get('reason') or 'original check unresolved'] if status=='INCONCLUSIVE' else []))


def control_values(data):
    """Only known, paired values with identical units; never infer comparison."""
    for a,b,unit,op in (
        ('required_length_cm','available_length_cm','cm','provided_ge_required'),
        ('vertical_bend_required_cm','vertical_bend_provided_cm','cm','provided_ge_required'),
        ('required_cm','provided_cm','cm','provided_ge_required'),
        ('required_cm2_m','provided_cm2_m','cm2/m','provided_ge_required'),
        ('limit_cm','drawn_cm','cm','provided_le_required'),
        ('Vsd_kn','VRd2_kn','kN','provided_ge_required'),
        ('negative_terminal_demand_knm','Mk_equivalent_knm','kN.m','provided_ge_required'),
        ('max_negative_demand_knm','Mk_equivalent_knm','kN.m','provided_ge_required')):
        if a in data and b in data:return dict(required=data[a],provided=data[b],unit=unit,comparison=op)
    return {}


def positive_regions(data,context,source):
    if data['beam_id']!=context['beam_id']:raise ValueError('source_beam_mismatch')
    checks=[]
    for r in data['regions']:
        s=r['status'];comparison=r.get('comparison',{})
        v={'status':('NOT_APPLICABLE' if s=='no_positive_demand' else state(comparison.get('capacity_sufficient'))),
           'reason':s,'blockers':r.get('blockers',[])}
        demand=r.get('governing_demand') or {};capacity=r.get('capacity') or {}
        checks.append(check('flexural_capacity',r['region_id'],v,ref(source,pointer='/regions/'+str(data['regions'].index(r))),
            span=data['span_id'],interval=[r['x_start_m'],r['x_end_m']],marks=r['geometric_reinforcement']['marks'],
            required=demand.get('Msk_knm',demand.get('value_knm')),provided=capacity.get('Mk_equivalent'),unit='kN.m',comparison='provided_ge_required'))
    return envelope(context,'positive_flexure',source,checks,complete=not data['span_summary'].get('incomplete',True),original_summary=data['span_summary'])


def regional(data,context,source,discipline='negative_flexure'):
    checks=[]
    for group_index,group in enumerate(data['regions']):
        items=group['result']['regions']
        for i,r in enumerate(items):
            g=r['geometry'];d=r.get('governing_demand') or {}
            region_path=f'/regions/{group_index}' if data.get('source_layout')=='flat_regions' else f'/regions/{group_index}/result/regions/{i}'
            provided=r.get('Mk_equivalent_knm')
            if provided is None and r.get('concretopy',{}).get('mk_equivalente_kncm') is not None:
                provided=r['concretopy']['mk_equivalente_kncm']/100
            c=check('flexural_capacity',f'region/{group["span"]}/{group["start_m"]}/{group["end_m"]}/{g["region_id"]}',
                {'passes':r.get('capacity_sufficient'),'reason':'original regional capacity comparison'},
                ref(source,pointer=region_path),
                span=group['span'],interval=[g['x_start_m'],g['x_end_m']],marks=group['marks'],
                required=r.get('governing_moment_abs',d.get('value_knm')),provided=provided,unit='kN.m',comparison='provided_ge_required')
            checks.append(c)
            fit=r.get('transverse_fit',{})
            for layer in fit.get('layers',[]):
                checks.append(check('transverse_fit',c['check_id']+'/layer/'+str(layer['layer']),
                    {'passes':layer.get('fits'),'rule':fit.get('rule')},
                    ref(source,pointer=region_path+'/transverse_fit'),
                    span=group['span'],interval=c['physical_interval'],marks=group['marks'],
                    required=layer.get('required_width_cm'),provided=layer.get('available_width_cm'),unit='cm',comparison='provided_ge_required'))
            for flag,kind in (('hipoteses_validas','flexure_model_assumptions'),('ductilidade_atendida','ductility')):
                if flag in r.get('concretopy',{}):
                    checks.append(check(kind,c['check_id']+'/'+kind,{'passes':r['concretopy'][flag]},
                        ref(source,pointer=region_path+'/concretopy/'+flag),
                        span=group['span'],interval=c['physical_interval'],marks=group['marks']))
        if not items:
            checks.append(check('flexural_capacity',f'region/{group["span"]}/{group["start_m"]}/{group["end_m"]}/unresolved',
                {'passes':None,'reason':group['result'].get('diagnostics')},ref(source,pointer=f'/regions/{group_index}'),
                span=group['span'],interval=[group['start_m'],group['end_m']],marks=group['marks']))
    return envelope(context,discipline,source,checks,complete=False,original_summary=data.get('global_negative_approval'))


def negative_anchorage(data,context,source):
    checks=[]
    replaced={(e['mark'],e['cut_side'],e['span']) for e in data.get('event_interpretations',[]) if e.get('status')=='SUPERSEDED'}
    for i,event in enumerate(data['events']):
        if (event['mark'],event['cut_side'],event['span']) in replaced:continue
        r=event['result'];end=r.get('provided_end_position_m',r.get('actual_end_position_m'))
        for kind,control in r['checks'].items():
            checks.append(check(kind,f'event/{event["mark"]}/{event["cut_side"]}/{event["span"]}/{kind}',control,
                ref(source,pointer=f'/events/{i}/result/checks/{kind}'),span=event['span'],
                interval=[end,end] if end is not None else None,marks=[event['mark']],**control_values(control)))
        if not r['checks']:
            checks.append(check('termination',f'event/{event["mark"]}/{event["cut_side"]}/{event["span"]}/unresolved',
                {'passes':None,'reason':r.get('diagnostics')},ref(source,pointer=f'/events/{i}/result'),
                span=event['span'],interval=[end,end] if end is not None else None,marks=[event['mark']]))
    for i,node in enumerate(data['end_nodes']):
        v=node['verification'];geom=node['geometry']
        for kind,control in v['checks'].items():
            c=check(kind,f'node/{node["mark"]}/{node["support"]}/{kind}',control,
                ref(source,pointer=f'/end_nodes/{i}/verification/checks/{kind}'),span=geom['span_id'],
                interval=sorted([geom['internal_face_m'],geom['external_face_m']]),marks=[node['mark']],**control_values(control))
            c['physical_reference']=geom
            if kind=='straight_anchorage_geometry' and v.get('anchorage_mode')=='VERTICAL_BEND':
                c.update(governing=False,role='MODE_SELECTION_OBSERVATION')
                c['evidence']['anchorage_mode']=v['anchorage_mode']
            checks.append(c)
    for i,r in enumerate(data.get('negative_support_relations',[])):
        for kind in ('overlap_length_check','overlap_flexural_capacity','local_spacing_geometry','vibrator_access_spacing'):
            if kind not in r:continue
            control=r[kind]
            overlap=r.get('physical_overlap') or {}
            interval=overlap.get('interval_m') if isinstance(overlap,dict) else None
            marks=[r[k] if isinstance(r[k],str) else r[k].get('mark') for k in ('bar_a','bar_b')]
            checks.append(check(kind,f'relation/{"/".join(marks)}/{kind}',control,
                ref(source,pointer=f'/negative_support_relations/{i}/{kind}'),span=r.get('span'),interval=interval,marks=marks,**control_values(control)))
    return envelope(context,'anchorage',source,checks,complete=data.get('full_negative_verification_complete',False))


def shear(data,context,source):
    checks=[]
    for i,region in enumerate(data['shear_drawn_regions']):
        for kind,control in region['checks'].items():
            checks.append(check(kind,region['region']['id']+'/'+kind,control,
                ref(source,pointer=f'/shear_drawn_regions/{i}/checks/{kind}'),span=region['span_id'],
                interval=region['region']['interval_m'],marks=[region['region']['mark']],**control_values(control)))
    for i,coverage in enumerate(data['coverage_reviews']):
        for j,part in enumerate(coverage['intervals']):
            checks.append(check('drawing_coverage',f'coverage/{coverage["span_id"]}/{part["interval_m"]}',
                {'status':part['status'],'reason':part['classification']},
                ref(source,pointer=f'/coverage_reviews/{i}/intervals/{j}'),span=coverage['span_id'],interval=part['interval_m']))
    return envelope(context,'shear',source,checks,complete=data['global_shear_approval'] is not None,original_summary=data['global_shear_approval'])


def suspension(data,context,source):
    if data['receiving_beam_id']!=context['beam_id']:raise ValueError('source_beam_mismatch')
    checks=[]
    for i,connection in enumerate(data['connections']):
        identifier=connection['connection']['id']
        for kind,control in connection['checks'].items():
            checks.append(check(kind,identifier+'/'+kind,control,ref(source,pointer=f'/connections/{i}/checks/{kind}'),
                interval=connection.get('distribution',{}).get('interval_m'),**control_values(control)))
        for j,part in enumerate(connection.get('subintervals',[])):
            for kind,control in part.get('checks',{}).items():
                checks.append(check(kind,identifier+f'/subinterval/{j}/'+kind,control,
                    ref(source,pointer=f'/connections/{i}/subintervals/{j}/checks/{kind}'),
                    interval=part.get('interval_m'),**control_values(control)))
    if not checks:
        checks=[check('suspension_inventory','inventory',{'status':data['overall_result'],
            'reason':'suspension inventory incomplete' if not data['inventory']['complete'] else 'documented suspension inventory'},source)]
    return envelope(context,'suspension',source,checks,complete=data['inventory']['complete'],original_summary=data['overall_result'])


def end_support_existing(data,context,source):
    original=data.get('exploration',{}).get('existing',data)
    a=original['anchorage'];marks=[data.get('documentary',{}).get('mark','unknown')]
    checks=[]
    for kind,flag,required,provided,unit in (
        ('reinforcement_area','area_suficiente',a['as_calculada_cm2'],a['as_efetiva_cm2'],'cm2'),
        ('anchorage_length','comprimento_suficiente',a['lb_nec_cm'],a['comprimento_disponivel_cm'],'cm')):
        checks.append(check(kind,'existing/'+kind,{'passes':a[flag],'reason':original['status']},source,
            marks=marks,required=required,provided=provided,unit=unit,comparison='provided_ge_required'))
    for limitation in original.get('limitations',[]):
        checks.append(check('support_geometry',limitation,{'passes':None,'reason':limitation},source,marks=marks))
    return envelope(context,'anchorage',source,checks,complete=not original.get('limitations'),original_summary=original['status'])
