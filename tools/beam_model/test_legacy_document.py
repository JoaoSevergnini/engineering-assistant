import json
from pathlib import Path
import unittest
from consolidar_detalhamento import transform,validate,reinforcement_at
HERE=Path(__file__).resolve().parent
FIXTURE=HERE.parents[1]/'analises/pranchas/V501_V503_detalhamento_prancha.json'
if not FIXTURE.exists():FIXTURE=HERE/'V501_V503_detalhamento_prancha.json'
class LegacyTests(unittest.TestCase):
 def setUp(self):
  self.raw=json.loads(FIXTURE.read_text(encoding='utf-8-sig'))
  self.m=transform(self.raw,FIXTURE.name)
 def test_group_quantities_per_beam(self):
  self.assertEqual(self.m['beam']['ids'],['V501','V503'])
  bars={x['mark']:x for x in self.m['longitudinal_reinforcement']}
  self.assertEqual(len(bars),5)
  self.assertEqual(bars['N5']['bars'],4)
  self.assertEqual(bars['N5']['layers'],[3,1])
  self.assertEqual(bars['N2']['layers'],[1,1])
 def test_coordinates_and_active_bars(self):
  self.assertEqual(self.m['spans'][0]['clear_length_cm'],711)
  self.assertEqual(self.m['spans'][0]['x_end_cm'],711)
  self.assertEqual(self.m['overhangs'],[])
  q=reinforcement_at(self.m,350)
  self.assertEqual(set(q['present']),{'N1','N3','N5','N8'})
  self.assertTrue(q['complete'])
 def test_geometry_independent_from_distribution(self):
  self.raw['stirrups']['regions'][0]['region_length']['value']=100
  self.assertEqual(transform(self.raw)['spans'][0]['clear_length_cm'],711)
 def test_support_mapping_not_invented(self):
  for s in self.m['supports']:
   self.assertIsNone(s['individual_beam_mapping'])
   self.assertIsNone(s['width_cm'])
  self.assertEqual(self.m['supports'][0]['written_names'],['P2A','P2B'])
 def test_skin_and_cut(self):
  skin=self.m['skin_reinforcement'][0]
  self.assertEqual((skin['mark'],skin['bars_per_face'],skin['faces'],skin['bars']),('N8',3,2,6))
  self.assertEqual((skin['x_start_cm'],skin['x_end_cm']),(-24,736))
  self.assertEqual(self.m['sections'][0]['lower_layers'],[3,1])
  self.assertIsNone(self.m['sections'][0]['x_cm'])
 def test_special_region_not_automatically_suspension(self):
  regions=self.m['stirrup_regions']
  self.assertEqual([r['quantity'] for r in regions],[39,5,8])
  self.assertEqual((regions[1]['diameter_mm'],regions[1]['spacing_cm']),(6.3,15))
  self.assertEqual(regions[1]['function'],'suspension')
  self.assertEqual(regions[1]['indirect_support'],'IB1')
  self.assertTrue(self.m['suspension_reinforcement_detailed'])
  self.assertFalse(self.m['anchorage_staples_detailed'])
  self.assertEqual(self.m['unresolved_drawing_observations'],[])
 def test_indirect_supports_are_separate_and_unknowns_preserved(self):
  self.assertEqual({x['id'] for x in self.m['supports']},{'left','right'})
  indirect={x['id']:x for x in self.m['indirect_supports']}
  self.assertEqual(set(indirect),{'IB1','IB2'})
  self.assertEqual(indirect['IB1']['suspension_marks'],['N7'])
  self.assertTrue(indirect['IB1']['suspension_reinforcement_detailed'])
  self.assertIsNone(indirect['IB2']['suspension_reinforcement_detailed'])
  self.assertIsNone(indirect['IB2']['suspension_marks'])
  for support in indirect.values():
   for key in ('supported_beam','x_cm','x_start_cm','x_end_cm'):self.assertIsNone(support[key])
 def test_function_independent_of_diameter_spacing(self):
  region=self.raw['stirrups']['regions'][1]
  region['diameter']['value']=5
  region['spacing']['value']=14
  m=transform(self.raw)
  self.assertEqual(m['stirrup_regions'][1]['function'],'suspension')
  self.assertEqual(m['stirrup_regions'][1]['indirect_support'],'IB1')
 def test_different_diameter_does_not_create_function_or_association(self):
  region=self.raw['stirrups']['regions'][1]
  region.pop('function')
  region.pop('indirect_support')
  self.raw['indirect_supported_beams'][0]['suspension_reinforcement_detailed']['value']=None
  self.raw['indirect_supported_beams'][0]['suspension_marks']['value']=None
  self.raw['special_details']['suspension_reinforcement_detailed']['value']=None
  m=transform(self.raw)
  self.assertIsNone(m['stirrup_regions'][1]['function'])
  self.assertNotIn('indirect_support',m['stirrup_regions'][1])
  self.assertIsNone(m['indirect_supports'][0]['suspension_marks'])
 def test_spatial_association_provenance(self):
  region=self.raw['stirrups']['regions'][1]
  self.assertIn('associacao_N7_contorno',region['function']['sources'])
  self.assertIn('elevacao',region['indirect_support']['sources'])
  self.assertEqual(region['function']['classification'],'interpreted_by_office_standard')
  for support in self.raw['indirect_supported_beams']:
   self.assertEqual(support['role']['value'],'indirect_supported_beam')
   self.assertIn('conv_apoios_indiretos',support['role']['sources'])
 def test_invalid_suspension_association_rejected(self):
  self.raw['stirrups']['regions'][1]['indirect_support']['value']='IB2'
  with self.assertRaises(ValueError):transform(self.raw)
 def test_references_and_fidelity(self):
  validate(self.m,self.raw)
  self.assertEqual(self.m['skin_reinforcement'][0]['source']['json_pointer'],'/skin_reinforcement')
  self.m['longitudinal_reinforcement'][0]['x_start_cm']=-100
  with self.assertRaises(ValueError):validate(self.m,self.raw)
 def test_input_preserved(self):
  before=json.dumps(self.raw,sort_keys=True)
  transform(self.raw)
  self.assertEqual(json.dumps(self.raw,sort_keys=True),before)
if __name__=='__main__':unittest.main()
