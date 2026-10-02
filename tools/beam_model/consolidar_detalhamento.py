"""Modelo longitudinal a partir do JSON documental de prancha (schema 1.2).
Somente biblioteca padrao. Nenhum acesso a PDF, LST ou calculo estrutural.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path


def at(doc, pointer):
    value = doc
    for part in pointer.strip('/').split('/') if pointer else []:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def val(value):
    return value.get('value') if isinstance(value, dict) and 'value' in value else value


class Builder:
    def __init__(self, raw, name):
        if raw.get('type') != 'beam_reinforcement_drawing_interpretation' or raw.get('schema_version') != '1.2':
            raise ValueError('Formato esperado: beam_reinforcement_drawing_interpretation schema 1.2. Outros formatos precisam de adaptador.')
        self.raw, self.name = raw, name
        self.issues = {}
        self.audit = []

    def issue(self, code, entity):
        self.issues.setdefault(code, []).append(entity)

    def source(self, pointer):
        return {'document_model': self.name, 'json_pointer': pointer}

    def get(self, pointer, unit=None):
        try:
            original = at(self.raw, pointer)
        except (KeyError, IndexError):
            return None
        result = val(original)
        if result is not None and unit and (not isinstance(original, dict) or original.get('unit') != unit):
            raise ValueError(f'Unidade ausente ou incompatível em {pointer}; esperado {unit}.')
        return result

    def copy(self, dst, key, pointer, unit=None):
        dst[key] = self.get(pointer, unit)
        self.audit.append((dst, key, pointer, unit))
        return dst[key]

    def coordinates(self, dst, pointer, entity):
        data = self.get(pointer)
        if data is not None and not isinstance(data, dict):
            raise ValueError('Intervalo longitudinal invalido: ' + pointer)
        dst['x_start_cm'] = data.get('x_start') if data else None
        dst['x_end_cm'] = data.get('x_end') if data else None
        if dst['x_start_cm'] is None or dst['x_end_cm'] is None:
            self.issue('unknown_longitudinal_extent', entity)

    def layers(self, pointer, entity):
        entries = at(self.raw, pointer).get('layers', [])
        if not entries:
            self.issue('unknown_layers', entity)
            return None
        result = []
        seen = set()
        for entry in entries:
            number, quantity = val(entry.get('layer')), val(entry.get('quantity'))
            if type(number) is not int or number < 1 or number in seen:
                raise ValueError('Camada invalida/repetida em ' + pointer)
            if type(quantity) is not int or quantity < 0:
                raise ValueError('Quantidade de camada invalida em ' + pointer)
            seen.add(number)
            result += [0] * max(0, number - len(result))
            result[number-1] = quantity
        return result

    def position(self, pointer, skin=False, staple=False):
        entity = self.get(pointer + '/mark')
        out = {'source': self.source(pointer)}
        self.copy(out, 'mark', pointer + '/mark')
        out['function'] = 'skin' if skin else 'anchorage_staple' if staple else self.get(pointer + '/group')
        self.copy(out, 'bars', pointer + ('/total_quantity_per_position' if skin else '/quantity'))
        self.copy(out, 'diameter_mm', pointer + '/diameter', 'mm')
        self.copy(out, 'length_cm', pointer + ('/length_per_piece' if staple else '/length_per_bar'), 'cm')
        self.copy(out, 'shape', pointer + '/shape')
        self.coordinates(out, pointer + ('/exact_longitudinal_coordinates' if staple else '/longitudinal_coordinates'), entity)
        if skin:
            count = self.copy(out, 'bars_per_face', pointer + '/bars_per_face')
            total = out['bars']
            # Arithmetic of documentary counts, never a geometric or structural assumption.
            if type(count) is int and count > 0 and type(total) is int and total % count == 0:
                out['faces'] = total // count
            else:
                out['faces'] = None
                self.issue('unknown_skin_faces', entity)
            self.copy(out, 'vertical_spacing_cm', pointer + '/vertical_spacing', 'cm')
            if out['vertical_spacing_cm'] is None:
                self.issue('unknown_skin_vertical_spacing', entity)
            self.copy(out, 'horizontal_length_cm', pointer + '/horizontal_length', 'cm')
            self.copy(out, 'left_return_cm', pointer + '/left_return_length', 'cm')
        elif staple:
            self.copy(out, 'longitudinal_dimension_cm', pointer + '/longitudinal_dimension', 'cm')
            self.copy(out, 'closing_dimension_cm', pointer + '/closing_dimension', 'cm')
            self.copy(out, 'layer_and_bar_association', pointer + '/exact_layer_and_bar_anchored')
            if out['layer_and_bar_association'] is None:
                self.issue('unknown_staple_association', entity)
        else:
            out['layers'] = self.layers(pointer, entity)
            self.copy(out, 'face', pointer + '/face')
            self.copy(out, 'horizontal_length_cm', pointer + '/horizontal_length_shown', 'cm')
            bend = at(self.raw, pointer).get('end_bend')
            if bend:
                out['end_bend'] = {}
                for key, field, unit in [('side','side',None),('direction','direction',None),('length_cm','length','cm')]:
                    self.copy(out['end_bend'], key, pointer + '/end_bend/' + field, unit)
        return out

    def run(self):
        coordinate = self.raw.get('geometry', {}).get('coordinate_system')
        if not coordinate or coordinate.get('unit') != 'cm':
            raise ValueError('Falta sistema global de coordenadas documentado em cm.')
        out = {'schema_version':'1.0', 'model_type':'longitudinal_beam_detail',
               'document_model':self.name,
               'conventions':{'length_unit':'cm','diameter_unit':'mm','layers':'Indice 0 = primeira camada; [0,1] = uma barra apenas na segunda.',
                              'intervals':'Extensao longitudinal fisica documentada; comprimento desenvolvido nao substitui a projecao em x.',
                              'geometry_basis':'Geometria ja interpretada no documental; nao reconstruida a partir de estribos.'},
               'beam': {'source':self.source('/identification')},
               'coordinate_system':{**coordinate,'source':self.source('/geometry/coordinate_system')},
               'section':{'source':self.source('/section')},
               'supports':[], 'spans':[], 'overhangs':[], 'longitudinal_reinforcement':[],
               'stirrup_regions':[], 'skin_reinforcement':[], 'anchorage_staples':[],
               'indirect_supports':[], 'suspension_reinforcement':[], 'sections':[]}
        self.copy(out['beam'],'id','/identification/beam')
        self.copy(out['beam'],'grouped','/identification/grouped_with_other_beams')
        for key, field in [('width_cm','width'),('height_cm','height'),('cover_cm','local_cover')]:
            self.copy(out['section'],key,'/section/'+field,'cm')
            if out['section'][key] is None:self.issue('unknown_section_dimension',key)
        self.copy(out['section'],'shape','/section/shape')
        self.copy(out['section'],'lateral_projections_dimensions','/section/lateral_projections_dimensions')
        if out['section']['lateral_projections_dimensions'] is None:
            self.issue('unknown_lateral_projection_dimensions','section')
        for i, original in enumerate(self.raw['geometry'].get('supports', [])):
            path = f'/geometry/supports/{i}'
            support = {'source':self.source(path)}
            self.copy(support,'id',path+'/id')
            self.copy(support,'type',path+'/type')  # No inference from P/V prefixes.
            self.copy(support,'width_cm',path+'/width_along_beam','cm')
            self.copy(support,'restraint',path+'/model_restraint')
            faces=self.get(path+'/faces_coordinates') or {}
            support.update(x_left_cm=faces.get('left'),x_right_cm=faces.get('right'))
            for field,code in [('type','unknown_support_nature'),('restraint','unknown_support_restraint'),('width_cm','unknown_support_dimension')]:
                if support[field] is None:self.issue(code,support['id'])
            if None in (support['x_left_cm'],support['x_right_cm']):self.issue('unknown_support_faces',support['id'])
            out['supports'].append(support)
        for i, original in enumerate(self.raw['geometry'].get('spans_and_overhang', [])):
            path=f'/geometry/spans_and_overhang/{i}'
            kind=self.get(path+'/type')
            if kind not in ('between_supports','overhang'):raise ValueError('Tipo geometrico desconhecido: '+str(kind))
            item={'source':self.source(path)}
            for key in ('id','left_support','right_support'):self.copy(item,key,path+'/'+key)
            self.copy(item,'clear_length_cm',path+'/geometric_length','cm')
            self.coordinates(item,path+'/extent',item['id'])
            if item['clear_length_cm'] is None:self.issue('unknown_geometric_length',item['id'])
            out['spans' if kind=='between_supports' else 'overhangs'].append(item)
        for group, items in self.raw.get('longitudinal_reinforcement', {}).items():
            if not isinstance(items,list):raise ValueError('Grupo de armadura invalido.')
            for i, item in enumerate(items):
                out['longitudinal_reinforcement'].append(self.position(f'/longitudinal_reinforcement/{group}/{i}'))
        for i in range(len(self.raw.get('skin_reinforcement',{}).get('positions',[]))):
            out['skin_reinforcement'].append(self.position(f'/skin_reinforcement/positions/{i}',skin=True))
        for i in range(len(self.raw.get('anchorage_staples',{}).get('positions',[]))):
            out['anchorage_staples'].append(self.position(f'/anchorage_staples/positions/{i}',staple=True))
        for i, raw_region in enumerate(self.raw.get('stirrups',{}).get('regions',[])):
            path=f'/stirrups/regions/{i}'
            item={'source':self.source(path)}
            for key, field, unit in [('id','id',None),('mark','mark',None),('function','function',None),('diameter_mm','diameter','mm'),('spacing_cm','spacing','cm'),('quantity','quantity',None),('region_length_cm','region_length','cm')]:
                self.copy(item,key,path+'/'+field,unit)
            if 'indirect_support' in raw_region:
                self.copy(item,'indirect_support',path+'/indirect_support')
            # Only share shape properties explicitly attached to the same mark.
            item['legs']=self.get(path+'/legs')
            if item['legs'] is None and item['mark']==self.get('/stirrups/mark'):
                item['legs']=self.get('/stirrups/vertical_legs_drawn')
                item['shape_source']=self.source('/stirrups')
            self.coordinates(item,path+'/extent',item['id'])
            if item['function'] is None:self.issue('unknown_stirrup_function',item['id'])
            if item['legs'] is None:self.issue('unknown_stirrup_legs',item['id'])
            out['stirrup_regions'].append(item)
        for i, original in enumerate(self.raw.get('indirect_supported_beams',[])):
            path=f'/indirect_supported_beams/{i}'
            item={'source':self.source(path)}
            for key,field,unit in [('id','id',None),('supported_beam','supported_beam_name',None),('span','span',None),('x_cm','exact_longitudinal_position','cm'),('suspension_reinforcement_detailed','suspension_reinforcement_detailed',None)]:
                self.copy(item,key,path+'/'+field,unit)
            self.coordinates(item,path+'/approximate_extent',item['id'])
            if item['supported_beam'] is None:self.issue('unknown_supported_beam_name',item['id'])
            if item['x_cm'] is None:self.issue('unknown_indirect_support_position',item['id'])
            marks=self.get(path+'/suspension_marks')
            if marks is None:marks=[] if item['suspension_reinforcement_detailed'] is False else None
            item['suspension_marks']=marks
            if item['suspension_reinforcement_detailed'] is not False and not marks:self.issue('unknown_suspension_association',item['id'])
            out['indirect_supports'].append(item)
            out['suspension_reinforcement'].append({'indirect_support':item['id'],'detailed':item['suspension_reinforcement_detailed'],'marks':marks,'source':self.source(path)})
        for i, original in enumerate(self.raw.get('section_views',[])):
            path=f'/section_views/{i}'
            item={'source':self.source(path)}
            for key,field,unit in [('id','label',None),('x_cm','exact_abscissa','cm'),('upper_positions','upper_positions',None),('lower_position','lower_position',None),('skin_bars_per_face','skin_points_per_face',None),('skin_position','skin_position_at_section',None)]:
                self.copy(item,key,path+'/'+field,unit)
            item['upper_layers']=[self.get(path+'/upper_first_layer_quantity'),self.get(path+'/upper_second_layer_quantity')]
            item['lower_layers']=[self.get(path+'/lower_first_layer_quantity')]
            if item['x_cm'] is None:self.issue('unknown_section_position',item['id'])
            out['sections'].append(item)
        out['uncertainties']=[{'code':k,'entities':list(dict.fromkeys(v))} for k,v in self.issues.items()]
        # Every copied scalar is audited against its source, including nulls.
        for dst,key,path,unit in self.audit:
            if dst[key]!=self.get(path,unit):raise ValueError('Divergencia de fonte: '+path)
        return out


def _unique(items,key,label):
    values=[x[key] for x in items]
    if any(v is None for v in values) or len(values)!=len(set(values)):
        raise ValueError('Identificador ausente/duplicado: '+label)


def validate(model, raw=None):
    """Consistencia documental/geometrica; nao dimensionamento."""
    json.dumps(model,allow_nan=False)
    positions=model['longitudinal_reinforcement']+model['skin_reinforcement']+model['anchorage_staples']
    _unique(positions,'mark','posicoes')
    for collection in ('supports','spans','overhangs','stirrup_regions','indirect_supports','sections'):
        _unique(model[collection],'id',collection)
    _unique(model['spans']+model['overhangs'],'id','geometria longitudinal')
    segment_ids={x['id'] for x in model['spans']+model['overhangs']}
    for item in model['indirect_supports']:
        if item['span'] is not None and item['span'] not in segment_ids:raise ValueError('Vao de apoio indireto inexistente.')
    main_ids={x['id'] for x in model['supports']}
    indirect_ids={x['id'] for x in model['indirect_supports']}
    if main_ids & indirect_ids:raise ValueError('Apoio indireto confundido com apoio principal.')
    for item in model['spans']+model['overhangs']:
        for key in ('left_support','right_support'):
            if item[key] is not None and item[key] not in main_ids:raise ValueError('Apoio inexistente: '+str(item[key]))
    for bar in model['longitudinal_reinforcement']:
        if bar['layers'] is not None and sum(bar['layers'])!=bar['bars']:raise ValueError('Soma de camadas difere das barras: '+bar['mark'])
    for bar in model['skin_reinforcement']:
        if bar['faces'] is not None and bar['faces']*bar['bars_per_face']!=bar['bars']:raise ValueError('Quantidade de pele inconsistente.')
    for region in model['stirrup_regions']:
        association=region.get('indirect_support')
        if association is not None:
            if association not in indirect_ids:raise ValueError('Associacao a apoio indireto inexistente.')
            support=next(x for x in model['indirect_supports'] if x['id']==association)
            if region['function']=='suspension' and (support['suspension_reinforcement_detailed'] is not True or region['mark'] not in (support['suspension_marks'] or [])):
                raise ValueError('Associacao de suspensao inconsistente.')
        for key in ('spacing_cm','diameter_mm'):
            value=region[key]
            if value is not None and (not isinstance(value,(int,float)) or isinstance(value,bool) or value<=0):raise ValueError('Valor invalido em estribos: '+key)
    def visit(value):
        if isinstance(value,dict):
            for start,end in [('x_start_cm','x_end_cm'),('x_left_cm','x_right_cm')]:
                a,b=value.get(start),value.get(end)
                if a is not None and b is not None and b<a:raise ValueError('Intervalo invertido.')
            if 'source' in value and raw is not None:at(raw,value['source']['json_pointer'])
            for child in value.values():visit(child)
        elif isinstance(value,list):
            for child in value:visit(child)
    visit(model)
    if raw is not None:
        # Full transformation replay audits that the output contains only the allowed
        # source projection and documented count arithmetic, never new coordinates.
        expected=build_document(raw,model['document_model'])
        comparable={k:v for k,v in model.items() if k!='document_sha256'}
        if comparable!=expected:raise ValueError('Modelo diverge da projecao documental permitida.')
    return {'valid_json':True,'unique_positions':len(positions),'longitudinal_positions':len(model['longitudinal_reinforcement']),
            'skin_positions':len(model['skin_reinforcement']),'main_supports':len(main_ids),'indirect_supports':len(indirect_ids),
            'stirrup_regions':len(model['stirrup_regions']),'source_projection_checked':raw is not None}


def build_document(raw, document_model):
    if raw.get('schema_version') == '1.1' and raw.get('type') == 'beam_reinforcement_drawing_interpretation':
        from legacy_document import build_legacy
        return build_legacy(raw, document_model, Builder)
    return Builder(raw,document_model).run()


def transform(raw, document_model='document_model.json'):
    model=build_document(raw,document_model)
    validate(model,raw)
    return model


def reinforcement_at(model,x_cm):
    """Interval membership only. Unknown extents remain indeterminate.
    Does not calculate resistance, anchorage, effective depth or steel area.
    """
    if not isinstance(x_cm,(int,float)) or isinstance(x_cm,bool) or not math.isfinite(x_cm):raise ValueError('x deve ser finito.')
    result={'present':[],'absent':[],'indeterminate':[]}
    for bar in model['longitudinal_reinforcement']+model['skin_reinforcement']:
        a,b=bar['x_start_cm'],bar['x_end_cm']
        state='absent' if (a is not None and x_cm<a) or (b is not None and x_cm>b) else 'indeterminate' if a is None or b is None else 'present'
        result[state].append(bar['mark'])
    result['complete']=not result['indeterminate']
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.input.resolve()==args.output.resolve() or (args.output.exists() and args.input.samefile(args.output)):
        parser.error('Entrada documental e saida devem ser diferentes.')
    content=args.input.read_bytes()
    raw=json.loads(content.decode('utf-8-sig'))
    model=transform(raw,args.input.name)
    issues=model.pop('uncertainties')
    model['document_sha256']=hashlib.sha256(content).hexdigest()
    model['uncertainties']=issues
    report=validate(model,raw)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(model,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    if args.input.read_bytes()!=content:raise RuntimeError('Entrada mudou durante a execucao.')
    print(json.dumps(report))


if __name__=='__main__':main()
