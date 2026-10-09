"""Real shared-detail, two-layer, left-cut regression. Physics stays in Concretopy."""
import json
from pathlib import Path
import sys
import unittest
from bar_scaling import check_bar_scaling,SUPPORTED_SCOPE
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT.parent/'concretopy'))
import concretopy as api

def load(name): return json.loads((ROOT/'analises/pranchas'/name).read_text(encoding='utf8'))
def run(beam):
    return check_bar_scaling(load('V536_V565_beam_model.json'),load(beam+'_tqs.json'),
        load(beam+'_tqs_positions.json'),load(beam+'_beam_mapping.json'),load(beam+'_tqs_raw.json'),api,
        interrupted_mark='N3',cut_side='left',scope={**SUPPORTED_SCOPE,'provenance':{'source':'real fixture hypotheses; interrupted N3 straight, external N2 bend excluded'}})

class SharedMultilayerGolden(unittest.TestCase):
    def test_both_beams_independent_efforts_same_centroid(self):
        for beam,x,v,section in [('V536',1.8854092813869217,125.1524673,2),('V565',2.088569899792843,113.98269295,1)]:
            with self.subTest(beam=beam):
                r=run(beam)
                self.assertTrue(r['overall']['scaling_passes'])
                self.assertEqual(r['diagnostics'],[])
                self.assertEqual(r['composition_before']['marks'],['N2','N3'])
                self.assertEqual(r['composition_after']['marks'],['N2'])
                self.assertEqual(r['event_x_m'],.54)
                self.assertAlmostEqual(r['moment_diagram']['selected_x_nec_m'],x)
                self.assertEqual(r['shear_for_al']['Vk_used_kn'],v)
                self.assertEqual(r['shear_for_al']['governing'][0]['section'],section)
                self.assertEqual(r['d_for_al']['d_cm'],66)
                self.assertEqual([c['d_cm'] for c in r['d_for_al']['contributions']],[68,64])
                self.assertEqual(r['concretopy']['al_result']['al_cm'],66)
                self.assertAlmostEqual(r['condition_B']['lb_cm'],55.0716891039194)
                self.assertEqual(r['condition_A']['ten_phi_cm'],20)
                self.assertEqual(r['bond_condition']['bar_center_from_bottom_cm'],8)
                self.assertEqual(r['bond_condition']['classification'],'good')
    def test_peak_reference_inside_support_not_a_support_check(self):
        r=run('V536');p=r['moment_diagram']['peak']
        self.assertEqual((p['section'],p['x_m'],p['location_relative_to_clear_span']),(13,3.276,'right_support'))
        self.assertEqual(r['condition_B']['available_length_cm'],273.6)
        self.assertEqual(len(r['moment_diagram']['crossings']['crossings']),1)
    def test_developed_length_does_not_replace_projection(self):
        r=run('V536');bars={b['mark']:b for b in r['composition_before']['bars']}
        self.assertEqual((bars['N2']['length_cm'],bars['N2']['horizontal_length_cm']),(455,397))
        self.assertEqual((bars['N3']['x_start_common'],bars['N3']['x_end_common']),(.54,3.88))
        self.assertEqual(r['external_bends_not_checked'][0]['bend_x_m'],-.09)
    def test_remaining_first_layer_capacity_preserved(self):
        r=run('V565');c=r['remaining_capacity']
        self.assertAlmostEqual(c['MRd_knm'],260.4506073942584)
        self.assertAlmostEqual(c['Mk_equivalent_knm'],186.036148138756)
        self.assertEqual(list(c['concretopy_result']['d_por_camada_cm']),[68])
        self.assertNotEqual(c['concretopy_result']['d_equivalente_cm'],r['d_for_al']['d_cm'])
    def test_shared_group_maps_each_ordered_support(self):
        m=load('V565_beam_mapping.json')
        self.assertEqual(m['geometry']['status'],'exact')
        self.assertEqual(load('V536_V565_beam_model.json')['sections'][0]['lower_layers'],[3,3])
        self.assertEqual((m['supports']['left']['id'],m['supports']['right']['id']),('P12B','P8B'))
        self.assertEqual(m['supports']['left']['resolution']['method'],'drawing_group_and_ordered_tqs_support')

if __name__=='__main__': unittest.main()
