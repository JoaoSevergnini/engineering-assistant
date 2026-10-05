import copy
import json
from pathlib import Path
import sys
import unittest

from positive_flexure import check_positive_flexure
from test_flexure_regions import bar,transverse

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT.parent/'concretopy'))
import concretopy as api


class GenericCheckTests(unittest.TestCase):
    def test_V1001_real_regions(self):
        data=[json.loads((ROOT/'analises/pranchas'/n).read_text(encoding='utf8')) for n in (
            'V1001_beam_model.json','V1001_tqs.json','V1001_tqs_positions.json','V1001_beam_mapping.json','V1001_tqs_raw.json')]
        out=check_positive_flexure(*data,api)
        checked=[r for r in out['regions'] if r['status']=='checked'];self.assertEqual(len(checked),1)
        r=checked[0];self.assertEqual(r['geometric_reinforcement']['marks'],['N3','N5'])
        self.assertEqual(r['concretopy_call']['layers'],[{'numero_barras':4,'diametro_mm':10,'d_cm':None}])
        self.assertEqual(r['governing_demand']['section'],6)
        self.assertEqual(r['governing_demand']['value_knm'],59.8401783)
        self.assertEqual(r['capacity']['Mk_equivalent'],65.387969862408)
        self.assertEqual(r['comparison']['utilization'],.9151557759924052)
        single=next(q for q in out['regions'] if q['region_id']=='R4')
        self.assertEqual(single['geometric_reinforcement']['marks'],['N5'])
        self.assertEqual(single['status'],'no_positive_demand');self.assertIsNone(single['concretopy_result'])
        self.assertTrue(out['span_summary']['incomplete'])
        self.assertTrue(all(not q['diagnostics']['anchorage_checked'] and not q['diagnostics']['reinforcement_development_checked'] for q in out['regions']))

    def setUp(self):
        self.data=[json.loads((ROOT/'analises/pranchas'/n).read_text(encoding='utf8')) for n in (
            'V501_V503_beam_model.json','V501_tqs.json','V501_tqs_positions.json','V501_beam_mapping.json','V501_tqs_raw.json')]

    def check(self,geometry=None):
        return check_positive_flexure(*self.data,api,transverse_regions=geometry)

    def replace_bars(self,bars):
        # Dado sintético explícito, sem modificar arquivos de projeto.
        self.data[3]['reinforcement']=bars
        self.data[0]['longitudinal_reinforcement']=copy.deepcopy(bars)

    def uniform(self):
        return [transverse(0,8.43)]

    def test_V501_exact_golden_and_stirrup_per_region(self):
        out=self.check(); maximum=out['span_summary']['maximum_utilization']
        r=next(r for r in out['regions'] if r['region_id']==maximum['region_id'])
        self.assertEqual(r['governing_demand']['value_knm'],61.5073088)
        self.assertEqual(r['governing_demand']['section'],8)
        self.assertEqual(r['governing_demand']['x_m'],4.789333333333333)
        self.assertEqual(r['capacity']['Mk_equivalent'],99.47034565405093)
        self.assertEqual(maximum['value'],.618348196093708)
        checked=[r for r in out['regions'] if r['status']=='checked']
        self.assertEqual(len(checked),3)
        self.assertEqual([r['transverse_geometry']['stirrup_diameter_mm'] for r in checked],[5,6.3,5])
        self.assertTrue(out['span_summary']['incomplete'])
        self.assertEqual(sum(len(r['tqs_sections']) for r in out['regions']),13)

    def test_F_unsampled_region_retained(self):
        self.replace_bars([bar('A',0,8.43),bar('B',.7,.8)])
        out=self.check(self.uniform())
        r=next(r for r in out['regions'] if r['geometric_reinforcement']['marks']==['A','B'])
        self.assertEqual(r['status'],'demand_not_sampled')
        self.assertIsNone(r['capacity'])
        self.assertIsNone(r['governing_demand'])

    def test_G_negative_only_and_points_preserved(self):
        self.replace_bars([bar('A',0,.5),bar('B',.5,8.43)])
        r=next(r for r in self.check(self.uniform())['regions'] if r['x_start_m']==0)
        self.assertEqual(r['status'],'no_positive_demand')
        self.assertEqual(r['tqs_sections'][0]['value_knm'],-22.03554255)
        self.assertFalse(r['tqs_sections'][0]['eligible_positive'])
        self.assertIsNone(r['comparison']['utilization'])

    def test_mixed_layer_blocks_concretopy_call(self):
        self.replace_bars([bar('A',0,8.43,diameter=12.5),bar('B',0,8.43,diameter=16)])
        out=self.check(self.uniform())
        self.assertEqual(out['span_summary']['regions_checked'],0)
        self.assertIsNone(out['span_summary']['all_checked_regions_capacity_sufficient'])
        self.assertTrue(any('mixed_diameters' in x for x in out['regions'][0]['blockers']))
        self.assertNotIn('concretopy_call',out['regions'][0])

    def test_distinct_diameters_distinct_layers_supported(self):
        self.replace_bars([bar('A',0,8.43,[2],12.5),bar('B',0,8.43,[0,1],16)])
        r=self.check(self.uniform())['regions'][0]
        self.assertEqual(r['status'],'checked')
        self.assertEqual([l['diametro_mm'] for l in r['concretopy_call']['layers']],[12.5,16])

    def test_unknown_layers_block_not_fused_by_diameter(self):
        bars=[bar('A',0,8.43),bar('B',0,8.43)];bars[1]['layers']=None
        self.replace_bars(bars)
        self.assertEqual(self.check(self.uniform())['span_summary']['regions_checked'],0)

    def test_exact_tqs_breakpoint_both_closed_bars(self):
        x=4.789333333333333
        self.replace_bars([bar('A',0,x),bar('B',x,8.43)])
        out=self.check(self.uniform())
        owners=[r for r in out['regions'] if any(p['section']==8 for p in r['tqs_sections'])]
        self.assertEqual(len(owners),1)
        self.assertEqual(owners[0]['kind'],'boundary_point')
        self.assertEqual(owners[0]['geometric_reinforcement']['marks'],['A','B'])

    def test_exact_stirrup_interface_is_unresolved(self):
        x=4.789333333333333
        out=self.check([transverse(0,x,5),transverse(x,8.43,6.3)])
        owner=next(r for r in out['regions'] if any(p['section']==8 for p in r['tqs_sections']))
        self.assertEqual(owner['status'],'unresolved')
        self.assertIn('unresolved_transverse_geometry',owner['blockers'])
        self.assertIsNone(owner['capacity'])

    def test_missing_value_blocks_only_local_region(self):
        # Atualização sintética consistente da série e sua evidência raw.
        self.data[3]['force_series'][0]['values'][7]=None
        self.data[2]['beam']['spans'][0]['internal_forces'][0]['values'][7]=None
        self.data[4]['categorias']['esforcos_ao_longo_dos_vaos'][31]['normalizacao']['valores'][7]['normalizado']['valor']=None
        out=self.check()
        r=next(r for r in out['regions'] if any(p['section']==8 for p in r['tqs_sections']))
        self.assertEqual(r['status'],'unresolved')
        self.assertIn('missing_sampled_demand',r['blockers'])
        self.assertEqual(out['span_summary']['regions_checked'],2)

    def test_unidentified_series_no_calls_and_explicit_issue(self):
        self.data[4]['categorias']['esforcos_ao_longo_dos_vaos'][31]['normalizacao']['grandeza_original']='unknown'
        out=self.check()
        self.assertIsNotNone(out['series_issue'])
        self.assertEqual(out['span_summary']['regions_checked'],0)
        self.assertTrue(all(r['capacity'] is None for r in out['regions']))

    def test_materials_missing_keep_regions(self):
        for record in self.data[4]['categorias']['materiais']:
            record['campos_explicitos']=[f for f in record.get('campos_explicitos',[]) if f.get('chave')!='classe_aco']
        out=self.check()
        self.assertEqual(len(out['regions']),9)
        self.assertEqual(out['span_summary']['regions_checked'],0)

    def test_provenance_and_input_immutability(self):
        before=copy.deepcopy(self.data);out=self.check()
        self.assertEqual(self.data,before)
        for r in out['regions']:
            self.assertFalse(r['diagnostics']['anchorage_checked'])
            self.assertFalse(r['diagnostics']['reinforcement_development_checked'])
            self.assertIsNone(r['diagnostics']['minimum_reinforcement'])
            self.assertTrue(r['provenance']['concretopy'])
            for p in r['tqs_sections']: self.assertTrue(p['provenance']['value_pointer'])
        self.assertTrue(out['concretopy_interface']['sha256'])
        self.assertNotIn('beam_ok',out)

    def test_wrong_input_and_nonrectangular_rejected(self):
        self.data[3]['beam_id']='wrong'
        with self.assertRaises(ValueError): self.check()
        self.data[3]['beam_id']='V501';self.data[0]['section']['shape']='T'
        with self.assertRaises(ValueError): self.check()


if __name__=='__main__': unittest.main()
