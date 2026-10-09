"""Synthetic contract fixtures, explicitly not structural geometry of real beams."""
from input_evidence import fact


def proved(value, unit=None):
    return fact(value,state='DOCUMENTED_CONFIRMED',unit=unit,provenance=[{'fixture':'SYNTHETIC_CONTRACT_TEST','reference':'explicit test datum'}])


def extension():
    segment = dict(id='G1',x_start_m=proved(0,'m'),x_end_m=proved(4,'m'), geometry_type='CONSTANT',
                   geometry={k:proved(v,'mm' if k.endswith('_mm') else 'cm') for k,v in dict(width_cm=19,height_cm=57,cover_cm=2.5,stirrup_diameter_mm=6.3).items()},
                   provenance=[{'fixture':'SYNTHETIC_CONTRACT_TEST'}])
    segment['geometry']['section_shape'] = proved('RECTANGULAR')
    bar = dict(mark='N1',occurrence_id='O1',function='positive',face='lower', quantity=proved(2),diameter_mm=proved(16,'mm'),
               layers=proved([2]),x_start_m=proved(0,'m'),x_end_m=proved(4,'m'),provenance=[{'fixture':'SYNTHETIC_CONTRACT_TEST'}])
    return dict(schema_version='1.0',coordinate_system=dict(unit='m',origin='synthetic left face',positive_direction='right',provenance=[{'fixture':'SYNTHETIC_CONTRACT_TEST'}]),
                segments=[segment],occurrences=[bar],observations=[],coverage=[])


def document():
    return dict(type='beam_reinforcement_drawing_interpretation',schema_version='1.3',
                identification=dict(beam='SYNTHETIC',grouped_with_other_beams=False),
                geometry=dict(coordinate_system=dict(unit='cm',origin='left face',positive_direction='right')),
                section={},longitudinal_reinforcement={},physical_extension=extension())


def model():
    from physical_geometry import extend
    return extend(dict(longitudinal_reinforcement=[dict(mark='N1')],skin_reinforcement=[]),extension())
