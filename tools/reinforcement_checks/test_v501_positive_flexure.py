import copy
import json
from pathlib import Path
import sys
import unittest

from v501_positive_flexure import check_case

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT.parent/'concretopy'))
import concretopy as api


class GoldenTests(unittest.TestCase):
    def setUp(self):
        self.inputs=[json.loads((ROOT/'analises/pranchas'/n).read_text(encoding='utf8')) for n in (
            'V501_V503_beam_model.json','V501_tqs.json','V501_tqs_positions.json','V501_beam_mapping.json','V501_tqs_raw.json')]

    def run_case(self,module=api):
        return check_case(*self.inputs,module)

    def test_actual_golden_completed_with_interpreted_steel(self):
        r=self.run_case()
        self.assertEqual(r['status'],'completed_at_governing_section')
        self.assertEqual(r['blockers'],[])
        self.assertEqual(r['material_interpretation']['derived_fyk_mpa'],500)
        self.assertTrue(r['concretopy_call']['executed'])
        self.assertEqual(r['concretopy_result']['d_por_camada_cm'],(68.375,65.125))
        self.assertAlmostEqual(r['capacity']['MRd'],139.2584839156713,places=10)
        self.assertAlmostEqual(r['capacity']['Mk_equivalent'],99.47034565405093,places=10)
        self.assertAlmostEqual(r['comparison']['utilization'],.618348196093708,places=12)

    def test_n5_layers_and_region(self):
        r=self.run_case()
        self.assertEqual(r['reinforcement']['bars'],4)
        self.assertEqual(r['concretopy_call']['layers'],[{'numero_barras':3,'diametro_mm':12.5,'d_cm':None},{'numero_barras':1,'diametro_mm':12.5,'d_cm':None}])
        self.assertEqual(r['region'],{'x_start':.07,'x_end':8.22,'unit':'m'})

    def test_positive_demand_not_absolute(self):
        r=self.run_case()
        d=r['governing_demand']
        self.assertEqual(d['section'],8)
        self.assertEqual(d['x'],4.789333333333333)
        self.assertEqual(d['value'],61.5073088)
        self.assertFalse(r['considered_points'][0]['eligible_positive'])
        self.assertFalse(r['considered_points'][-1]['eligible_positive'])
        self.assertEqual(len(r['considered_points']),13)

    def test_actual_concretopy_call_no_explicit_d(self):
        r=self.run_case()
        direct=api.verificar_flexao_viga_retangular(api.SecaoRetangular(19,72,2.5,5),api.Concreto(40),api.Aco(500),
            [api.CamadaArmaduraLongitudinal(3,api.Barra(12.5)),api.CamadaArmaduraLongitudinal(1,api.Barra(12.5))],gamma_f=1.4)
        self.assertEqual(r['concretopy_result']['d_por_camada_cm'],direct.d_por_camada_cm)
        self.assertEqual(r['capacity']['MRd'],direct.mrd_kncm/100)
        self.assertEqual(r['capacity']['Mk_equivalent'],direct.mk_equivalente_kncm/100)
        self.assertTrue(r['concretopy_call']['executed'])

    def test_utilization_and_separate_diagnostics(self):
        r=self.run_case()
        self.assertEqual(r['comparison']['utilization'],r['governing_demand']['value']/r['capacity']['Mk_equivalent'])
        self.assertEqual(r['comparison']['capacity_sufficient'],r['capacity']['Mk_equivalent']>=r['governing_demand']['value'])
        self.assertIsNone(r['diagnostics']['minimum_reinforcement'])
        self.assertFalse(r['diagnostics']['anchorage_checked'])
        self.assertFalse(r['diagnostics']['reinforcement_development_checked'])
        self.assertNotIn('beam_ok',r)

    def test_provenance(self):
        r=self.run_case()
        self.assertEqual(r['governing_demand']['series_evidence'][0]['source']['lines'],[1373,1373])
        self.assertTrue(r['governing_demand']['provenance']['position_sources'])
        self.assertEqual(r['provenance']['N5']['json_pointer'],'/longitudinal_reinforcement/positive/0')
        self.assertTrue(r['provenance']['fck'])
        self.assertTrue(r['provenance']['gamma_f'])
        self.assertTrue(r['provenance']['concretopy']['signature'])

    def test_no_series_proof_blocks_comparison(self):
        rec=self.inputs[4]['categorias']['esforcos_ao_longo_dos_vaos'][31]
        rec['normalizacao']['grandeza_original']='unknown'
        r=self.run_case()
        self.assertIsNone(r['governing_demand'])
        self.assertIsNone(r['comparison']['utilization'])
        self.assertFalse(r['concretopy_call']['executed'])

    def test_negative_only_cannot_govern(self):
        for model,path in ((self.inputs[3],'force_series'),(self.inputs[2],None)):
            series=model[path][0] if path else model['beam']['spans'][0]['internal_forces'][0]
            series['values']=[-abs(v) for v in series['values']]
        rec=self.inputs[4]['categorias']['esforcos_ao_longo_dos_vaos'][31]
        for v in rec['normalizacao']['valores']:
            v['normalizado']['valor']=-abs(v['normalizado']['valor'])
        r=self.run_case()
        self.assertIsNone(r['governing_demand'])
        self.assertIn('Sem momento positivo',r['blockers'][0]['detail'])

    def test_missing_cover_blocks(self):
        self.inputs[1]['beam']['cover']['bottom']=None
        r=self.run_case()
        self.assertIn('missing_cover',[b['code'] for b in r['blockers']])
        self.assertFalse(r['concretopy_call']['executed'])

    def test_missing_fck_blocks_not_kgf_conversion(self):
        for record in self.inputs[4]['categorias']['materiais']:
            record['campos_explicitos']=[f for f in record.get('campos_explicitos',[]) if not(f.get('chave')=='fck' and f.get('unidade_original')=='MPa')]
        r=self.run_case()
        self.assertIn('missing_fck',[b['code'] for b in r['blockers']])

    def test_missing_gamma_f_does_not_default_to_dimensioner(self):
        for record in self.inputs[4]['categorias']['materiais']:
            record['campos_explicitos']=[f for f in record.get('campos_explicitos',[]) if f.get('chave')!='gamaf']
        r=self.run_case()
        self.assertIn('missing_gamma_f',[b['code'] for b in r['blockers']])

    def test_incomplete_n5_coverage_rejected(self):
        self.inputs[3]['reinforcement'][-1]['covered_tqs_sections']=[8]
        with self.assertRaisesRegex(ValueError,'13 seções'):
            self.run_case()

    def test_bad_layer_interpretation_rejected(self):
        for entity in (self.inputs[0]['longitudinal_reinforcement'][-1],self.inputs[3]['reinforcement'][-1]):
            entity['layers']=[1,2]
        with self.assertRaisesRegex(ValueError,'Composição'):
            self.run_case()

    def test_unknown_steel_blocks_real_call(self):
        self.inputs[4]['categorias']['materiais'][0]['campos_explicitos'][-1]['valor']='CA-60'
        r=self.run_case()
        self.assertIn('unresolved_steel',[b['code'] for b in r['blockers']])
        self.assertFalse(r['concretopy_call']['executed'])
        self.assertIsNone(r['comparison']['utilization'])

    def test_missing_steel_blocks_without_default(self):
        for record in self.inputs[4]['categorias']['materiais']:
            record['campos_explicitos']=[f for f in record.get('campos_explicitos',[]) if f.get('chave')!='classe_aco']
        r=self.run_case()
        self.assertEqual(r['material_interpretation']['status'],'missing')
        self.assertFalse(r['concretopy_call']['executed'])
        self.assertIsNone(r['capacity'])

    def test_inputs_unchanged(self):
        before=copy.deepcopy(self.inputs)
        self.run_case()
        self.assertEqual(before,self.inputs)


if __name__=='__main__':
    unittest.main()
