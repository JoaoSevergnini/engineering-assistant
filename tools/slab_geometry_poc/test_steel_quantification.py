"""Nominal-rate tests; synthetic composition contracts and real PDF regressions."""
import copy
import json
import math
from pathlib import Path
import unittest
from unittest.mock import patch
from steel_quantification import load_concretopy,steel_rate,quantify_composition,quantify,thickness_cases


def composition_fixture():
    members={}
    for id,phi,role in [('A',8,'BASE'),('B',5,'REINFORCEMENT')]:
        members[id]={'region_id':id,'occurrence_id':'occ-'+id,'display_id':'O-'+id,'position':'N-'+id,
            'diameter_mm':phi,'spacing_cm':14,'as_cm2_per_m':math.pi*(phi/10)**2/4*100/14,
            'orientation':0,'source_layer':None,'graphic_identity_group':'I-'+id,'reinforcement_type':role,
            'source_area_composition_eligible':True,'same_layer_rule_applicable':True}
    cell={'id':'ACT-TEST','source_composition_id':'C-TEST','classification':'BASE_PLUS_REINFORCEMENT',
        'region_ids':['A','B'],'positions':['N-A','N-B'],'slabs':['L'],'thickness_options_cm':[20],
        'geometry_pdf_pt':{'type':'Polygon','coordinates':[[[0,0],[1,0],[1,1],[0,1],[0,0]]]},
        'direction_layer_key':[0,None],'documentary_lap_region_ids':[], 'joint_function_supported':True,
        'supported_joint_sets':[{'id':'relation','members':['A','B'],'classification':'BASE_PLUS_REINFORCEMENT'}],
        'physical_addition_authorized':False}
    return cell,members,{'id':'SYNTHETIC_SAME_LAYER','source':'SYNTHETIC_ENGINEER_RULE'}


class SyntheticSteelRateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        area,_=load_concretopy(Path(__file__).resolve().parents[2].parent/'concretopy')
        cls.area=staticmethod(area)

    def test_n13_n14_formula_and_precision(self):
        a=steel_rate(8,14,self.area);b=steel_rate(5,14,self.area)
        self.assertAlmostEqual(a,3.5903916041026207,places=13)
        self.assertAlmostEqual(b,1.4024967203525862,places=13)
        self.assertEqual(format(a,'.2f'),'3.59');self.assertEqual(format(b,'.2f'),'1.40')
        self.assertNotEqual(a,float(format(a,'.2f')))

    def test_different_diameters_and_spacings(self):
        for phi,s in [(6.3,20),(8,11),(10,12.5),(12.5,15),(5,7),(8,143)]:
            self.assertAlmostEqual(steel_rate(phi,s,self.area),math.pi*(phi/10)**2/4*100/s,places=13)

    def test_scaling_spacing_and_diameter(self):
        self.assertEqual(steel_rate(8,20,self.area)*2,steel_rate(8,10,self.area))
        self.assertEqual(steel_rate(10,14,self.area),steel_rate(5,14,self.area)*4)

    def test_invalid_inputs_not_coerced(self):
        for invalid in [None,True,False,0,-1,float('nan'),float('inf'),'14']:
            with self.assertRaises(ValueError):steel_rate(8,invalid,self.area)
            with self.assertRaises(ValueError):steel_rate(invalid,14,self.area)

    def test_bar_area_delegate_called(self):
        calls=[]
        def supplied_area(phi):calls.append(phi);return .5
        self.assertEqual(steel_rate(8,10,supplied_area),5)
        self.assertEqual(calls,[8])
        with self.assertRaises(ValueError):steel_rate(8,10,lambda phi:float('nan'))


class SyntheticCompositionRateTests(unittest.TestCase):
    def test_confirmed_joint_nominal_sum_same_layer(self):
        c,m,r=composition_fixture();before=copy.deepcopy(c);q=quantify_composition(c,m,r)
        self.assertTrue(q['nominal_addition_authorized'])
        self.assertAlmostEqual(q['nominal_total_cm2_per_m'],4.992888324455207,places=13)
        self.assertEqual(q['extra_stacked_layers_assumed_for_reinforcement'],0)
        self.assertEqual({a['physical_layer_id'] for a in q['individual_areas']},{r['id']})
        self.assertEqual([a['diameter_mm'] for a in q['individual_areas']],[8,5])
        self.assertTrue(all(a['center_from_tension_face_cm'] is None for a in q['individual_areas']))
        self.assertEqual(c,before);self.assertFalse(q['resistant_area_or_capacity_validated'])

    def test_lap_blocks_addition_even_if_source_joint_function_set(self):
        c,m,r=composition_fixture();c['classification']='LAP_SPLICE'
        q=quantify_composition(c,m,r);self.assertIsNone(q['nominal_total_cm2_per_m'])
        self.assertFalse(q['nominal_addition_authorized']);self.assertEqual(q['quantification_kind'],'NON_ADDITIVE_LAP')

    def test_lap_representation_blocks_pending_overlap(self):
        c,m,r=composition_fixture();c['documentary_lap_region_ids']=['A'];m['A']['reinforcement_type']='LAP_SPLICE'
        self.assertIsNone(quantify_composition(c,m,r)['nominal_total_cm2_per_m'])

    def test_unresolved_keeps_individual_rates_but_no_total(self):
        c,m,r=composition_fixture();c['classification']='UNRESOLVED_COMPOSITION'
        q=quantify_composition(c,m,r);self.assertTrue(all(x['as_cm2_per_m'] for x in q['individual_areas']))
        self.assertIsNone(q['nominal_total_cm2_per_m'])

    def test_no_nominal_sum_from_unsupported_graphic_overlap(self):
        c,m,r=composition_fixture();c['supported_joint_sets']=[]
        self.assertIsNone(quantify_composition(c,m,r)['nominal_total_cm2_per_m'])

    def test_directions_or_known_layers_conflict(self):
        for change in ['direction','layers']:
            c,m,r=composition_fixture()
            if change=='direction':m['B']['orientation']=1
            else:m['A']['source_layer']='LOWER';m['B']['source_layer']='UPPER'
            self.assertIsNone(quantify_composition(c,m,r)['nominal_total_cm2_per_m'])

    def test_unknown_spacing_or_geometry_or_layer_rule_blocks_sum(self):
        for change in ['spacing','geometry','layer_rule']:
            c,m,r=composition_fixture()
            if change=='spacing':m['B']['as_cm2_per_m']=None
            elif change=='geometry':m['B']['source_area_composition_eligible']=False
            else:m['B']['same_layer_rule_applicable']=False
            self.assertIsNone(quantify_composition(c,m,r)['nominal_total_cm2_per_m'])

    def test_duplicate_source_identity_never_doubles_area(self):
        c,m,r=composition_fixture();m['B']['graphic_identity_group']=m['A']['graphic_identity_group']
        self.assertIsNone(quantify_composition(c,m,r)['nominal_total_cm2_per_m'])
        c,m,r=composition_fixture();c['region_ids']=['A','A']
        self.assertIsNone(quantify_composition(c,m,r)['nominal_total_cm2_per_m'])

    def test_single_region_has_nominal_value_without_addition(self):
        c,m,r=composition_fixture();c['region_ids']=['A'];c['classification']='SINGLE_REINFORCEMENT'
        q=quantify_composition(c,m,r);self.assertEqual(q['nominal_total_cm2_per_m'],m['A']['as_cm2_per_m'])
        self.assertFalse(q['nominal_addition_authorized'])

    def test_multiple_reinforcements_still_require_complete_supported_set(self):
        c,m,r=composition_fixture();c['classification']='MULTIPLE_REINFORCEMENTS'
        c['supported_joint_sets'][0]['classification']='MULTIPLE_REINFORCEMENTS'
        self.assertTrue(quantify_composition(c,m,r)['nominal_addition_authorized'])
        c['supported_joint_sets'][0]['members']=['A']
        self.assertFalse(quantify_composition(c,m,r)['nominal_addition_authorized'])


class RealSheetSteelQuantificationRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2];out=root/'analises/lajes_quantificacao_positiva'
        cls.old=json.loads((root/'analises/lajes_composicao_atuacao/inventario.json').read_text(encoding='utf8'))
        cls.new=json.loads((out/'inventario.json').read_text(encoding='utf8'));cls.a=cls.new['positive_steel_quantification']
        cls.profile=json.loads((out/'criterios_documentais.json').read_text(encoding='utf8'))
        cls.texts=json.loads((root/'analises/lajes_geometria_lideres/entidades_pagina.json').read_text(encoding='utf8'))['texts']
        area,_=load_concretopy(root.parent/'concretopy');cls.area=staticmethod(area)
        cls.byid={o['display_id']:o for o in cls.a['occurrences']};cls.cells={c['source_composition_id']:c for c in cls.a['compositions']}

    def test_all_prior_layers_and_source_geometry_and_classes_preserved(self):
        for k,v in self.old.items():self.assertEqual(self.new[k],v,k)
        old={c['id']:c for c in self.old['acting_composition_analysis']['compositions']}
        for c in self.a['compositions']:
            self.assertEqual(c['source_classification'],old[c['id']]['classification'])
            self.assertEqual(c['geometry_pdf_pt'],old[c['id']]['geometry_pdf_pt'])

    def test_n13_n14_individuals_and_joint_left_right(self):
        for id in ['O043','O044']:self.assertEqual(format(self.byid[id]['as_cm2_per_m'],'.2f'),'3.59')
        for id in ['O034','O035']:self.assertEqual(format(self.byid[id]['as_cm2_per_m'],'.2f'),'1.40')
        for id in ['C083','C088']:self.assertEqual(format(self.cells[id]['nominal_total_cm2_per_m'],'.2f'),'4.99')
        self.assertEqual(self.cells['C059']['positions'],['N14','N15'])
        self.assertEqual(self.a['metrics']['nominal_joint_totals_authorized'],3)

    def test_real_counts_and_missing_spacing_never_inferred_from_quantity(self):
        self.assertEqual(self.a['metrics']['individual_rates_calculated'],38)
        self.assertEqual(self.a['metrics']['rates_pending'],21)
        for o in self.a['occurrences']:
            if o['spacing_cm'] is None:self.assertIsNone(o['as_cm2_per_m'])
        changed=copy.deepcopy(self.old)
        for r in changed['acting_composition_analysis']['acting_regions']:r['original_call']['quantity']=999999
        result=quantify(changed,self.profile,self.texts,self.area)
        self.assertEqual([o['as_cm2_per_m'] for o in result['occurrences']],[o['as_cm2_per_m'] for o in self.a['occurrences']])

    def test_pending_association_can_have_individual_rate_not_reliable_thickness(self):
        for id in ['O009','O014','O057']:
            o=self.byid[id];self.assertIsNotNone(o['as_cm2_per_m']);self.assertIsNone(o['thickness_cm'])
            self.assertFalse(o['nominal_composition_eligible'])
        self.assertEqual(self.byid['O057']['documentary_thickness_options_cm'],[18.0])

    def test_n40_and_confirmed_lap_no_sum_and_pending_triples(self):
        self.assertEqual(self.byid['O053']['reinforcement_type'],'LAP_SPLICE')
        for id in ['C092','C109','C110','C115','C116','C071','C076']:
            c=self.cells[id];self.assertIsNone(c['nominal_total_cm2_per_m']);self.assertFalse(c['nominal_addition_authorized'])

    def test_same_layer_different_diameters_no_common_center_or_d(self):
        a,b=self.byid['O043'],self.byid['O034']
        self.assertEqual(a['depth_preparation']['physical_layer_id'],b['depth_preparation']['physical_layer_id'])
        self.assertEqual(a['depth_preparation']['bar_radius_cm'],.4);self.assertEqual(b['depth_preparation']['bar_radius_cm'],.25)
        for o in self.a['occurrences']:
            self.assertIsNone(o['depth_preparation']['effective_depth_cm'])
            self.assertIsNone(o['depth_preparation']['center_from_tension_face_cm'])
        for id in ['O003','O039','O059']:self.assertFalse(self.byid[id]['same_layer_rule_applicable'])

    def test_documentary_cover_and_reliable_h_without_contour_confirmation(self):
        for id,h in [('O043',20),('O050',18),('O047',20)]:
            o=self.byid[id];self.assertEqual(o['thickness_cm'],h)
            self.assertEqual(o['depth_preparation']['nominal_cover_cm'],2)
        self.assertEqual(self.a['cover_evidence']['value_text_id'],'T166:0')
        self.assertEqual(self.a['cover_evidence']['units_text_id'],'T265:0')

    def test_multiple_reliable_thicknesses_remain_separate(self):
        p=copy.deepcopy(self.old);a=next(o for o in p['documentary_spatial_assignment']['occurrences'] if o['display_id']=='O043')
        extra=copy.deepcopy(a['slab_associations'][0]);extra.update(slab='SYNTHETIC_SECOND_SLAB',domain_id='SYNTHETIC_DOMAIN',thickness_cm=12)
        a['slab_associations'].append(extra)
        q=next(o for o in quantify(p,self.profile,self.texts,self.area)['occurrences'] if o['display_id']=='O043')
        self.assertIsNone(q['thickness_cm']);self.assertTrue(q['different_reliable_thicknesses'])
        self.assertEqual({c['h_cm'] for c in q['depth_preparation']['cases_by_thickness']},{12,20})

    def test_outside_contour_geometry_does_not_change_area_rate(self):
        o=self.byid['O036'];self.assertEqual(o['thickness_cm'],20)
        old=next(r for r in self.old['acting_composition_analysis']['acting_regions'] if r['display_id']=='O036')
        self.assertEqual(o['geometry_pdf_pt'],old['geometry_pdf_pt'])
        self.assertAlmostEqual(o['as_cm2_per_m'],math.pi*(6.3/10)**2/4*100/12,places=13)

    def test_concretopy_not_called_for_flexure_or_d_and_units_not_direct_layers(self):
        with patch('concretopy.verificar_flexao_viga_retangular',side_effect=AssertionError('no flexure')),patch('concretopy.calcular_alturas_uteis_camadas',side_effect=AssertionError('no depth')):
            self.assertEqual(quantify(self.old,self.profile,self.texts,self.area),self.a)
        q=self.byid['O043']['concretopy_preparation']
        self.assertIsNone(q['numero_barras_for_api']);self.assertAlmostEqual(q['bar_density_per_meter'],100/14)
        self.assertFalse(q['direct_flexure_api_ready'])

    def test_document_scope_and_cover_text_changes_rejected(self):
        p=copy.deepcopy(self.profile);p['source_pdf_sha256']='other'
        with self.assertRaises(ValueError):quantify(self.old,p,self.texts,self.area)
        p=copy.deepcopy(self.profile);p['cover_evidence']['value_cm']=3
        with self.assertRaises(ValueError):quantify(self.old,p,self.texts,self.area)
        p=copy.deepcopy(self.profile);p['same_layer_rule']['extra_stacked_layers_for_reinforcement']=1
        with self.assertRaises(ValueError):quantify(self.old,p,self.texts,self.area)

    def test_missing_cover_does_not_prevent_steel_rate(self):
        p=copy.deepcopy(self.profile);p['cover_evidence']=None
        q=quantify(self.old,p,self.texts,self.area)
        self.assertEqual([o['as_cm2_per_m'] for o in q['occurrences']],[o['as_cm2_per_m'] for o in self.a['occurrences']])
        self.assertTrue(all(o['depth_preparation']['nominal_cover_cm'] is None for o in q['occurrences']))

    def test_determinism_color_and_order_invariance(self):
        p=copy.deepcopy(self.old);p['acting_composition_analysis']['acting_regions'].reverse()
        for r in p['acting_composition_analysis']['acting_regions']:r['color']=[1,0,1]
        self.assertEqual(quantify(p,self.profile,self.texts,self.area),self.a)


if __name__=='__main__':unittest.main()
