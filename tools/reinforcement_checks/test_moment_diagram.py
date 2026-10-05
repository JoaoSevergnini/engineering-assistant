import copy
from decimal import Decimal
import json
from pathlib import Path
import sys
import unittest
from moment_diagram import MomentDiagram, diagram_from_tqs
from v1001_moment_interpolation import analyze

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT.parent/'concretopy'))
import concretopy as api


def diagram(values, xs=None):
    xs=list(range(len(values))) if xs is None else xs
    return MomentDiagram([{'section':i+1,'x_m':x,'value_knm':m} for i,(x,m) in enumerate(zip(xs,values))],{'source':'synthetic'})


class LinearDiagramTests(unittest.TestCase):
    def test_increasing(self): self.assertEqual(diagram([2,6]).moment_at_x(.25)['value_knm'],3)
    def test_decreasing(self): self.assertEqual(diagram([6,2]).moment_at_x(.25)['value_knm'],5)
    def test_sign_preserved(self): self.assertEqual(diagram([3,-26]).moment_at_x(.5)['value_knm'],-11.5)
    def test_endpoints_original(self):
        d=diagram([.1,.2,.3]);q=d.moment_at_x(1)
        self.assertEqual(q['value_knm'],.2);self.assertEqual(q['source_type'],'tqs_section');self.assertEqual(q['segment_ids'],['SEG1','SEG2'])
    def test_outside(self):
        d=diagram([1,2]);self.assertEqual(d.moment_at_x(-.1)['status'],'outside_sampled_domain');self.assertIsNone(d.moment_at_x(1.1)['value_knm'])
    def test_missing_not_bridged(self):
        d=diagram([1,None,3]);self.assertTrue(all(s['segment_status']=='unresolved_missing_value' for s in d.segments))
        self.assertIsNone(d.moment_at_x(.5)['value_knm']);self.assertEqual(d.moment_at_x(0)['value_knm'],1)
        self.assertEqual(d.find_crossings(2)['status'],'incomplete_missing_values')
    def test_duplicate_conflicting(self):
        with self.assertRaisesRegex(ValueError,'strictly_increasing'):diagram([1,2],[0,0])
    def test_duplicate_equal(self):
        with self.assertRaisesRegex(ValueError,'strictly_increasing'):diagram([1,1],[0,0])
    def test_non_increasing(self):
        with self.assertRaisesRegex(ValueError,'strictly_increasing'):diagram([1,2],[1,0])
    def test_interior_crossing(self):
        e=diagram([2,6]).find_crossings(3)['crossings'][0];self.assertEqual(e['x_m'],.25);self.assertEqual(e['segments'][0]['direction'],'increasing')
    def test_endpoint_crossings(self):
        d=diagram([2,6]);self.assertEqual(d.find_crossings(2)['crossings'][0]['x_m'],0);self.assertEqual(d.find_crossings(6)['crossings'][0]['x_m'],1)
    def test_coincident_segment(self):
        e=diagram([2,2]).find_crossings(2)['crossings'][0];self.assertEqual(e['status'],'coincident_segment');self.assertNotIn('x_m',e)
    def test_constant_without_crossing(self):self.assertEqual(diagram([2,2]).find_crossings(3)['crossings'],[])
    def test_limit_outside(self):self.assertEqual(diagram([2,6]).find_crossings(7)['crossings'],[])
    def test_multiple(self):self.assertEqual([e['x_m'] for e in diagram([0,2,0,2]).find_crossings(1)['crossings']],[.5,1.5,2.5])
    def test_shared_endpoint_dedup(self):
        e=diagram([0,2,0]).find_crossings(2)['crossings'];self.assertEqual(len(e),1);self.assertEqual(len(e[0]['segments']),2)
    def test_plateau_endpoint_not_duplicated(self):
        events=diagram([0,2,2,0]).find_crossings(2)['crossings'];self.assertEqual(len(events),1);self.assertEqual(len(events[0]['boundary_segments']),2)
    def test_no_fixed_point_count(self):self.assertEqual(len(diagram([1,2,3,4]).segments),3)
    def test_invalid_numbers(self):
        for v in (float('nan'),float('inf'),True):
            with self.assertRaises(ValueError):diagram([1,v])
    def test_inputs_not_mutated_and_precision(self):
        points=[{'section':1,'x_m':0,'value_knm':0},{'section':2,'x_m':3,'value_knm':1}];before=copy.deepcopy(points)
        q=MomentDiagram(points).moment_at_x(1);self.assertEqual(points,before);self.assertGreater(len(q['value_decimal']),40)


class V1001InterpolationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=[json.loads((ROOT/'analises/pranchas'/n).read_text(encoding='utf8')) for n in (
            'V1001_beam_model.json','V1001_tqs.json','V1001_tqs_positions.json','V1001_beam_mapping.json','V1001_tqs_raw.json')]
        cls.out=analyze(*cls.data,api)
        cls.d=diagram_from_tqs(cls.data[3],cls.data[1],cls.data[2],cls.data[4])
    def test_real_segment_and_endpoints(self):
        s=self.d.segments[10];self.assertEqual((s['start_section'],s['end_section']),(11,12))
        self.assertEqual(self.d.moment_at_x(s['x_start_m'])['value_knm'],3.16754795)
        self.assertEqual(self.d.moment_at_x(s['x_end_m'])['value_knm'],-26.0072358)
    def test_zero_golden(self):
        e=next(e for e in self.out['zero_crossings']['crossings'] if e['segments'][0]['segment_id']=='SEG11')
        self.assertEqual(e['x_m'],6.745660952380952)
        self.assertLess(abs(Decimal(self.d.moment_at_x(Decimal(e['x_decimal']))['value_decimal'])),Decimal('1e-45'))
    def test_n3_event_interpolation(self):
        q=self.out['reinforcement_event_query'];self.assertEqual(q['x_m'],6.68);self.assertEqual(q['value_knm'],3.0439259849576117)
        self.assertEqual(q['source_type'],'linear_interpolation');self.assertEqual([p['section'] for p in q['base_points']],[11,12])
        self.assertEqual(q['reinforcement_event']['source_type'],'reinforcement_event_point')
    def test_all_original_13_values(self):
        self.assertEqual(len(self.d.segments),12)
        for p in self.d.points:self.assertEqual(self.d.moment_at_x(p['x_m'])['value_knm'],p['value_knm'])
    def test_capacity_real_api(self):
        c=self.out['remaining_reinforcement_capacity'];self.assertEqual(c['Mk_equivalent_knm'],33.054996873280636)
        self.assertEqual(c['MRd_knm'],46.276995622592885)
        self.assertEqual(c['concretopy_result']['d_por_camada_cm'],(68.5,))
        self.assertEqual(c['concretopy_call']['layers'],[{'numero_barras':2,'diametro_mm':10,'d_cm':None}])
        self.assertFalse(c['diagnostics']['bar_cut_checked']);self.assertFalse(c['diagnostics']['anchorage_checked'])
    def test_capacity_crossings(self):
        e=self.out['capacity_crossings']['crossings'];self.assertEqual([p['x_m'] for p in e],[2.1857211018870064,5.709168751478622])
        self.assertEqual([p['segments'][0]['direction'] for p in e],['increasing','decreasing'])
        for p in e:
            m=Decimal(self.d.moment_at_x(Decimal(p['x_decimal']))['value_decimal'])
            self.assertLess(abs(m-Decimal(p['m_limit_decimal'])),Decimal('1e-44'))
    def test_maximum(self):
        m=self.out['maximum'];self.assertEqual(m['Msk_max_discrete']['section'],6)
        self.assertEqual(m['Msk_max_discrete']['value_knm'],59.8401783);self.assertEqual(m['Msk_max_discrete'],m['interpolated_piecewise_max'])
    def test_series_unidentified_blocks(self):
        mapping=copy.deepcopy(self.data[3]);mapping['force_series']=[]
        with self.assertRaises(ValueError):diagram_from_tqs(mapping,self.data[1],self.data[2],self.data[4])


if __name__=='__main__':unittest.main()
