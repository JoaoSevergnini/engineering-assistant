import copy
import unittest
from flexure_regions import decompose_regions,compose_layers,contains


def bar(mark,a,b,layers=None,diameter=12.5):
    layers=[2] if layers is None else layers
    return {'mark':mark,'function':'positive','face':'lower','bars':sum(layers),'layers':layers,
            'diameter_mm':diameter,'x_start_common':a,'x_end_common':b,
            'source':{'document_model':'synthetic','json_pointer':'/'+mark}}


def transverse(a,b,diameter=5,cover=2.5,height=72):
    return {'x_start_common':a,'x_end_common':b,'bw_cm':19,'h_cm':height,
            'cover_cm':cover,'stirrup_diameter_mm':diameter,
            'provenance':{'input':'synthetic','pointer':f'/{a}/{b}'}}


class RegionTests(unittest.TestCase):
    def test_A_single_bar_one_region_closed_domain(self):
        regions=decompose_regions([bar('N1',0,10)],(0,10))
        self.assertEqual(len(regions),1)
        self.assertTrue(regions[0]['include_start'] and regions[0]['include_end'])

    def test_B_two_partially_overlapping_three_regions(self):
        regions=decompose_regions([bar('N1',0,7),bar('N2',3,10)],(0,10))
        self.assertEqual([r['geometric_reinforcement']['marks'] for r in regions],[['N1'],['N1','N2'],['N2']])
        self.assertEqual([r['x_start_m'] for r in regions],[0,3,7])
        self.assertEqual(len([r for r in regions if contains(r,3)]),1)
        self.assertEqual(next(r for r in regions if contains(r,7))['geometric_reinforcement']['marks'],['N1','N2'])

    def test_C_three_overlaps_correct_each_interval(self):
        regions=decompose_regions([bar('N1',0,10),bar('N2',2,6),bar('N3',4,8)],(0,10))
        self.assertEqual([r['geometric_reinforcement']['marks'] for r in regions],[['N1'],['N1','N2'],['N1','N2','N3'],['N1','N3'],['N1']])

    def test_D_same_endpoints_one_region_both_marks(self):
        regions=decompose_regions([bar('N1',0,10),bar('N2',0,10)],(0,10))
        self.assertEqual(len(regions),1)
        self.assertEqual(regions[0]['geometric_reinforcement']['layers'][0]['numero_barras'],4)

    def test_E_touching_closed_bars_create_unique_point_composition(self):
        regions=decompose_regions([bar('N1',0,5),bar('N2',5,10)],(0,10))
        owner=next(r for r in regions if contains(r,5))
        self.assertEqual(owner['kind'],'boundary_point')
        self.assertEqual(owner['geometric_reinforcement']['marks'],['N1','N2'])
        self.assertEqual(len([r for r in regions if contains(r,5)]),1)
        self.assertFalse(contains(regions[0],5))

    def test_H_stirrup_change_and_ambiguous_exact_interface(self):
        regions=decompose_regions([bar('N1',0,10)],(0,10),[transverse(0,5,5),transverse(5,10,6.3)])
        self.assertEqual([r['kind'] for r in regions],['interval','boundary_point','interval'])
        self.assertEqual(regions[0]['transverse_geometry']['stirrup_diameter_mm'],5)
        self.assertEqual(regions[-1]['transverse_geometry']['stirrup_diameter_mm'],6.3)
        self.assertEqual(regions[1]['transverse_status'],'unresolved')
        self.assertEqual(len([r for r in regions if contains(r,5)]),1)

    def test_I_mixed_diameters_same_layer_not_equivalent(self):
        composition=compose_layers([bar('N1',0,10,diameter=12.5),bar('N2',0,10,diameter=16)])
        self.assertEqual(composition['status'],'unresolved')
        self.assertEqual(len(composition['layers'][0]['components']),2)
        self.assertNotIn('diametro_mm',composition['layers'][0])
        self.assertTrue(any('unsupported_reinforcement_composition' in x for x in composition['issues']))

    def test_same_diameter_distinct_physical_layers_not_fused(self):
        composition=compose_layers([bar('N1',0,10,[2]),bar('N2',0,10,[0,2])])
        self.assertEqual(composition['status'],'resolved')
        self.assertEqual([l['numero_barras'] for l in composition['layers']],[2,2])

    def test_missing_face_or_layers_not_guessed(self):
        a=bar('N1',0,10);a['face']=None
        self.assertEqual(compose_layers([a])['status'],'unresolved')
        a['face']='lower';a['layers']=None
        self.assertEqual(compose_layers([a])['status'],'unresolved')

    def test_gap_in_layers_not_collapsed_for_automatic_d(self):
        self.assertIn('unsupported_missing_physical_layer',compose_layers([bar('N1',0,10,[0,2])])['issues'])

    def test_unknown_extent_blocks_every_possible_region(self):
        regions=decompose_regions([bar('N1',0,10),bar('N2',None,7)],(0,10))
        self.assertTrue(all(r['geometric_reinforcement']['status']=='unresolved' for r in regions))

    def test_cover_and_height_changes_create_boundaries(self):
        for change in ({'cover':3},{'height':75}):
            regions=decompose_regions([bar('N1',0,10)],(0,10),[transverse(0,5),transverse(5,10,**change)])
            self.assertEqual(len(regions),3)
            self.assertIsNone(next(r for r in regions if contains(r,5))['transverse_geometry'])

    def test_zero_length_bar_preserved_at_point(self):
        regions=decompose_regions([bar('N1',0,10),bar('N2',5,5)],(0,10))
        self.assertEqual(next(r for r in regions if contains(r,5))['geometric_reinforcement']['marks'],['N1','N2'])

    def test_duplicate_inverted_and_domain_rejected(self):
        for bars,domain in (([bar('N1',0,5),bar('N1',5,10)],(0,10)),([bar('N1',5,0)],(0,10)),([],(1,1))):
            with self.assertRaises(ValueError): decompose_regions(bars,domain)

    def test_gaps_preserved_not_filled(self):
        regions=decompose_regions([bar('N1',2,4)],(0,6))
        self.assertEqual([r['geometric_reinforcement']['marks'] for r in regions],[[],['N1'],[]])

    def test_partition_unique_original_intervals_unchanged(self):
        bars=[bar('N1',0,5),bar('N2',5,10)];before=copy.deepcopy(bars)
        regions=decompose_regions(bars,(0,10))
        for x in (0,2.5,5,7.5,10):
            self.assertEqual(len([r for r in regions if contains(r,x)]),1)
        self.assertEqual(bars,before)
