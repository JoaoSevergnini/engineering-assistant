import json,unittest
from pathlib import Path
from physical_geometry import at_x, project_occurrences
from consolidar_detalhamento import transform

ROOT=Path(__file__).resolve().parents[2]
CASE=ROOT/'analises/etapa1_leitura_geometria'

class RealStage1Tests(unittest.TestCase):
    def load(self,beam,suffix):return json.loads((CASE/(beam+'_'+suffix+'_stage1.json')).read_text(encoding='utf-8-sig'))
    def test_real_contract_replay(self):
        for beam in ('V606','V610','V611','V623','V626'):
            d=self.load(beam,'document');m=self.load(beam,'model');self.assertEqual(transform(d,beam+'_document_stage1.json'),m)
    def test_V623_exists_but_longitudinal_extent_unknown(self):
        m=self.load('V623','model');n2=next(b for b in m['physical_geometry']['occurrences'] if b['mark']=='N2')
        self.assertEqual((n2['quantity']['value'],n2['diameter_mm']['value'],n2['nominal_length_cm']),(4,16,464));self.assertEqual(n2['x_end_m']['state'],'MISSING')
        p=next(p for p in m['documentary_reconciliation']['positions'] if p['mark']=='N2')
        self.assertIn('PLOTTING_INTEGRITY',[i['code'] for i in p['issues']]);self.assertFalse(p['physical_absence_proved'])
        self.assertTrue(any(b['mark']=='N2' for b in at_x(m,2)['indeterminate']))
    def test_V623_repeated_N1_kept(self):
        m=self.load('V623','model');bars=[b for b in project_occurrences(m) if b['documentary_mark']=='N1'];self.assertEqual(len(bars),2);self.assertNotEqual(bars[0]['mark'],bars[1]['mark'])
    def test_V610_V611_V626_local_heights_not_average(self):
        for beam,heights in [('V610',[129.5,47,122]),('V611',[57,47]),('V626',[47,57])]:
            m=self.load(beam,'model');self.assertEqual([s['geometry']['height_cm']['value'] for s in m['physical_geometry']['segments']],heights)
            self.assertTrue(all(s['x_start_m']['state']=='MISSING' for s in m['physical_geometry']['segments']))
    def test_real_graphics_not_confirmed(self):
        for beam in ('V606','V610','V611','V626'):
            m=self.load(beam,'model');self.assertTrue(all(b['x_start_m']['state']=='ENGINEERING_ASSUMPTION' for b in m['physical_geometry']['occurrences']))
    def test_pdf_schedule_independent_extraction(self):
        r=json.loads((CASE/'V623_pdf_table_observations.json').read_text(encoding='utf-8-sig'));n2=next(o for o in r['observations'] if o['mark']=='N2')
        self.assertEqual((n2['quantity'],n2['diameter_mm'],n2['nominal_length_cm']),(4,16,464));self.assertTrue(n2['provenance'][0]['sha256'])
    def test_real_B_left_V626_not_terminal_column(self):
        m=self.load('V626','model');b=next(s for s in m['physical_geometry']['spans'] if s['tqs_span_token']=='1B');self.assertEqual(b['documentary_kind'],'CANTILEVER');self.assertNotEqual(b['kind'],'COLUMN_TERMINATION')
    def test_real_no_false_numeric_reapproval(self):
        r=json.loads((CASE/'comparativo_real.json').read_text(encoding='utf-8-sig'))
        for beam,v in r.items():
            self.assertFalse(v['numerical_recalculation']);self.assertTrue(all(p['readiness']=='PENDING' for p in v['input_validation']))

if __name__=='__main__':unittest.main()
