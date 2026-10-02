"""Adaptador do documental 1.1; nao relê desenhos nem resolve interpretacoes pendentes."""
from copy import deepcopy


def build_legacy(raw, name, builder):
    def v(x):return x.get('value') if isinstance(x,dict) and 'value' in x else x
    def fact(value, unit=None):return {'value':value, **({'unit':unit} if unit else {})}
    def src(path):return {'document_model':name,'json_pointer':path}
    if v(raw['span']['number_of_spans_shown']) != 1:
        raise ValueError('Adaptador 1.1 requer documental de vao unico.')
    normalized=deepcopy(raw)
    normalized['schema_version']='1.2'
    normalized['identification']={'beam':raw['identification']['drawing_label'],'grouped_with_other_beams':raw['identification']['same_detail_applies_to_each_beam']}
    normalized['section']['local_cover']=raw['section'].get('local_cover_dimension')
    coord=deepcopy(raw['span']['coordinate_system'])
    coord['origin']=v(coord['origin'])
    length=v(raw['span']['clear_length'])
    # The origin is documented at the left inner face; only that convention permits these translations.
    if coord['origin']!='face interna do apoio esquerdo' or coord['positive_direction']!='para a direita':
        raise ValueError('Origem 1.1 nao suportada; exige adaptador explicito.')
    supports=[]
    for original in raw['supports']:
        side=original['side']
        if side not in ('left','right'):raise ValueError('Lado de apoio invalido.')
        supports.append({'id':side,'width_along_beam':original['dimension_shown'],
                         'model_restraint':original.get('model_restraint'),
                         'faces_coordinates':fact({'left':None if side=='left' else length,'right':0 if side=='left' else None},'cm')})
    # dimension_shown is retained, but is not asserted to be the longitudinal support width.
    for s in supports:s['width_along_beam']=fact(None,'cm')
    normalized['geometry']={'coordinate_system':coord,'supports':supports,'spans_and_overhang':[
        {'id':'S1','type':fact('between_supports'),'left_support':'left','right_support':'right',
         'geometric_length':raw['span']['clear_length'],'extent':fact({'x_start':0,'x_end':length},'cm')}]}
    for group,items in normalized['longitudinal_reinforcement'].items():
        for item in items:
            item['quantity']=item.pop('bar_count')
            item['group']=item.pop('reinforcement_group')
            item['longitudinal_coordinates']=item.pop('longitudinal_extent')
            item['layers']=[{'layer':x['number'],'quantity':x['bar_count']} for x in item['layers']]
    skin=deepcopy(raw['skin_reinforcement'])
    skin['bars_per_face']=skin.pop('bars_per_side')
    skin['total_quantity_per_position']=skin.pop('total_bar_count_per_beam')
    skin['longitudinal_coordinates']=skin.pop('longitudinal_extent')
    normalized['skin_reinforcement']={'positions':[skin] if v(skin.get('skin_reinforcement_detailed')) else []}
    # No numeric indirect-support location/association is present in this schema.
    normalized['section_views']=[]
    for cut in raw.get('sections',[]):
        normalized['section_views'].append({'label':cut['label'],'exact_abscissa':cut['exact_abscissa'],
            'upper_first_layer_quantity':cut['upper_first_row_bars'],
            'upper_positions':cut['upper_bar_association'],
            'lower_first_layer_quantity':cut['lower_first_row_bars'],
            'lower_position':cut['lower_bar_association'],
            'skin_points_per_face':cut['skin_points_per_side']})
    model=builder(normalized,name).run()
    # Restore references to the original schema, never to an intermediate document.
    mappings={'/geometry/coordinate_system':'/span/coordinate_system','/geometry/supports':'/supports',
              '/geometry/spans_and_overhang/0':'/span','/skin_reinforcement/positions/0':'/skin_reinforcement',
              '/section_views':'/sections'}
    def remap(value):
        if isinstance(value,dict):
            if 'document_model' in value and 'json_pointer' in value:
                path=value['json_pointer']
                for old,new in mappings.items():
                    if path==old or path.startswith(old+'/'):
                        value['json_pointer']=new+path[len(old):];break
            for child in value.values():remap(child)
        elif isinstance(value,list):
            for child in value:remap(child)
    remap(model)
    model['beam'].update(ids=v(raw['identification']['beams']),quantity_basis='per_beam')
    for i,support in enumerate(model['supports']):
        original=raw['supports'][i]
        support.update(written_names=v(original['written_names']),
                       individual_beam_mapping=v(original['individual_beam_to_support_mapping']),
                       dimension_shown_cm=v(original['dimension_shown']))
    model['stirrup_shape_observation']={'vertical_legs_drawn':v(raw['stirrups'].get('vertical_legs_drawn')), 'dimensions_cm':v(raw['stirrups'].get('shape_dimensions_shown')), 'source':src('/stirrups')}
    model['special_details_source']=src('/special_details')
    for support in model['supports']:support['coordinate_source']=src('/span')
    model['anchorage_staples_detailed']=v(raw['special_details'].get('anchorage_staples_detailed'))
    model['suspension_reinforcement_detailed']=v(raw['special_details'].get('suspension_reinforcement_detailed'))
    for i,cut in enumerate(model['sections']):
        original=raw['sections'][i]
        cut['lower_layers']=[v(original['lower_first_row_bars']),v(original['lower_second_row_bars'])]
        cut['scope']=v(original.get('scope_limit'))
    # Only retain observations still unresolved in the updated documentary source.
    model['unresolved_drawing_observations']=[]
    if not raw.get('indirect_supported_beams'):
        model['unresolved_drawing_observations'].append({'description':v(raw['span'].get('unlabelled_dashed_contours')), 'source':src('/span')})
    if v(raw['special_details'].get('suspension_reinforcement_detailed')) is None:
        model['unresolved_drawing_observations'].append({'description':v(raw['special_details'].get('N7_local_role')), 'source':src('/special_details')})
    model['uncertainties']=[u for u in model['uncertainties'] if u['code']!='unknown_lateral_projection_dimensions']
    model['uncertainties'] += [
        {'code':'unknown_group_support_mapping','entities':['left','right']},
        {'code':'support_dimension_direction_unconfirmed','entities':['left','right']},
        {'code':'unknown_first_last_stirrup_offsets','source':src('/stirrups/first_last_stirrup_offsets')}]
    for observation in model['unresolved_drawing_observations']:
        model['uncertainties'].append({'code':'unresolved_drawing_interpretation','source':observation['source']})
    return model
