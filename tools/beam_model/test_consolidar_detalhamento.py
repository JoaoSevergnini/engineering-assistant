"""Invariantes e casos documentados; sem PDF, LST ou verificacoes estruturais."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from consolidar_detalhamento import transform, validate, reinforcement_at

HERE=Path(__file__).resolve().parent
FIXTURE=HERE.parents[1]/'analises/pranchas/V502_detalhamento_prancha.json'
if not FIXTURE.exists():
    FIXTURE=HERE/'V502_detalhamento_prancha.json'  # Execucao isolada com fixture copiada.

class BeamModelTests(unittest.TestCase):
    def setUp(self):
        self.raw=json.loads(FIXTURE.read_text(encoding='utf-8-sig'))
        self.model=transform(self.raw,FIXTURE.name)

    def test_known_geometry_and_separate_overhang(self):
        m=self.model
        self.assertEqual(m['beam']['id'],'V502')
        self.assertEqual((m['section']['width_cm'],m['section']['height_cm']),(19,202))
        self.assertEqual(len(m['supports']),4)
        self.assertEqual(len(m['spans']),3)
        self.assertEqual(len(m['overhangs']),1)
        self.assertEqual(m['supports'][0]['x_right_cm'],0)
        self.assertEqual(m['overhangs'][0]['x_end_cm'],1940)

    def test_unique_cross_span_bars_and_layers(self):
        bars={b['mark']:b for b in self.model['longitudinal_reinforcement']}
        self.assertEqual(len(bars),7)
        self.assertEqual((bars['N2']['x_start_cm'],bars['N2']['x_end_cm']),(101,1301))
        self.assertEqual(bars['N3']['layers'],[0,1])
        self.assertEqual(bars['N5']['layers'],[0,1])
        self.assertEqual(bars['N7']['layers'],[3,1])
        for b in bars.values():self.assertEqual(sum(b['layers']),b['bars'])

    def test_skin_positions_not_aggregated(self):
        bars=self.model['skin_reinforcement']
        self.assertEqual({b['mark'] for b in bars},{'N10','N11','N12','N13'})
        for b in bars:self.assertEqual((b['bars_per_face'],b['faces'],b['bars']),(9,2,18))
        self.assertEqual(next(b for b in bars if b['mark']=='N11')['x_start_cm'],775)

    def test_known_stirrups(self):
        regions=self.model['stirrup_regions']
        self.assertEqual([r['quantity'] for r in regions],[55,18,44,15])
        for r in regions:
            self.assertEqual((r['mark'],r['diameter_mm'],r['spacing_cm'],r['legs']),('N9',5,14,2))
            self.assertIsNone(r['function'])

    def test_geometry_not_reconstructed_from_stirrups(self):
        self.raw['stirrups']['regions'][0]['region_length']['value']=123
        changed=transform(self.raw)
        self.assertEqual(changed['spans'][0]['clear_length_cm'],759)
        self.raw['geometry']['spans_and_overhang'][0]['geometric_length']['value']=None
        self.raw['geometry']['spans_and_overhang'][0]['extent']['value']=None
        changed=transform(self.raw)
        self.assertIsNone(changed['spans'][0]['clear_length_cm'])
        self.assertIsNone(changed['spans'][0]['x_end_cm'])

    def test_unknown_extents_and_section_query(self):
        result=reinforcement_at(self.model,1000)
        self.assertTrue({'N2','N3','N11'} <= set(result['present']))
        self.assertIn('N5',result['indeterminate'])
        self.assertFalse(result['complete'])
        self.assertIn('N2',reinforcement_at(self.model,101)['present'])
        self.assertIn('N2',reinforcement_at(self.model,1302)['absent'])

    def test_indirect_supports_and_no_invented_suspension(self):
        m=self.model
        self.assertEqual({a['id'] for a in m['indirect_supports']},{'IB1','IB2'})
        self.assertFalse({a['id'] for a in m['supports']} & {'IB1','IB2'})
        for a in m['indirect_supports']:
            self.assertIsNone(a['supported_beam'])
            self.assertIsNone(a['x_cm'])
            self.assertFalse(a['suspension_reinforcement_detailed'])
            self.assertEqual(a['suspension_marks'],[])
        self.assertNotIn('suspension_reinforcement_required',json.dumps(m))
        self.assertNotIn('suspension_reinforcement_sufficient',json.dumps(m))

    def test_unresolved_suspension_remains_unresolved(self):
        self.raw['indirect_supported_beams'][0]['suspension_reinforcement_detailed']['value']=True
        m=transform(self.raw)
        self.assertIsNone(m['indirect_supports'][0]['suspension_marks'])
        self.assertIn('unknown_suspension_association',[u['code'] for u in m['uncertainties']])

    def test_cut_not_extrapolated(self):
        section=self.model['sections'][0]
        self.assertIsNone(section['x_cm'])
        self.assertEqual(section['upper_layers'],[3,1])
        self.assertEqual(section['lower_layers'],[4])
        self.assertEqual(section['skin_bars_per_face'],9)

    def test_duplicate_rejected(self):
        group=next(iter(self.raw['longitudinal_reinforcement'].values()))
        group.append(copy.deepcopy(group[0]))
        with self.assertRaises(ValueError):transform(self.raw)

    def test_bad_layer_sum_rejected(self):
        self.raw['longitudinal_reinforcement']['negative'][0]['quantity']['value']=99
        with self.assertRaises(ValueError):transform(self.raw)

    def test_inverted_interval_rejected(self):
        self.raw['geometry']['spans_and_overhang'][0]['extent']['value']={'x_start':800,'x_end':759}
        with self.assertRaises(ValueError):transform(self.raw)

    def test_wrong_units_rejected(self):
        self.raw['section']['height']['unit']='m'
        with self.assertRaises(ValueError):transform(self.raw)

    def test_source_mutation_detected(self):
        self.model['stirrup_regions'][0]['spacing_cm']=20
        with self.assertRaises(ValueError):validate(self.model,self.raw)

    def test_input_unchanged_and_beam_not_hardcoded(self):
        before=copy.deepcopy(self.raw)
        transform(self.raw)
        self.assertEqual(before,self.raw)
        self.raw['identification']['beam']['value']='V999'
        self.assertEqual(transform(self.raw)['beam']['id'],'V999')

    def test_cli_valid_json_and_original_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'raw.json'
            output=Path(tmp)/'model.json'
            content=FIXTURE.read_bytes()
            source.write_bytes(content)
            result=subprocess.run([sys.executable,str(HERE/'consolidar_detalhamento.py'),str(source),'--output',str(output)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(source.read_bytes(),content)
            model=json.loads(output.read_text(encoding='utf-8'))
            self.assertEqual(len(model['document_sha256']),64)
            self.assertLess(output.stat().st_size,len(content))
            validate(model,self.raw)
            rejected=subprocess.run([sys.executable,str(HERE/'consolidar_detalhamento.py'),str(source),'--output',str(source)],capture_output=True,text=True)
            self.assertNotEqual(rejected.returncode,0)
            self.assertEqual(source.read_bytes(),content)

if __name__=='__main__':unittest.main()
