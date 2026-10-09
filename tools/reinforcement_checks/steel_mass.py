"""Unique mass primitive. Area from Concretopy; explicitly sourced caller density."""
from moment_diagram import dec

def steel_mass(area_cm2, total_length_m, *, density_kg_m3, provenance):
    if not provenance or dec(area_cm2)<=0 or dec(total_length_m)<0 or dec(density_kg_m3)<=0:
        raise ValueError('invalid_steel_mass_input_or_source')
    linear=dec(area_cm2)*dec(density_kg_m3)/10000
    return {'linear_mass_kg_m':float(linear),'total_length_m':total_length_m,
        'mass_kg':float(linear*dec(total_length_m)),
        'provenance':{'area_cm2':area_cm2,'density_kg_m3':density_kg_m3,'source':provenance}}
