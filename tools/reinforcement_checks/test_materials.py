import copy
import unittest
from materials import interpret_steel, RULE_ID


def raw(*names):
    return {'categorias':{'materiais':[
        {'campos_explicitos':[{'chave':'classe_aco','valor':name}],
         'origem':{'arquivo':'RELDTFPS.LST','linha_inicial':i+1,'linha_final':i+1,'texto':'Aço '+str(name)}}
        for i,name in enumerate(names)]}}


class SteelTests(unittest.TestCase):
    def test_confirmed_aliases_without_fyk_conflict(self):
        r=interpret_steel(raw('CA50','CA-50','CA-50A'))
        self.assertEqual(r['status'],'consistent')
        self.assertEqual(r['normalized_class'],'CA-50')
        self.assertEqual(r['derived_fyk_mpa'],500)
        self.assertEqual([o['original_text'] for o in r['observations']],['CA50','CA-50','CA-50A'])
        self.assertTrue(all(o['derivation_rule']==RULE_ID and o['derived_fyk_mpa']==500 for o in r['observations']))

    def test_single_alias_and_original_whitespace_preserved(self):
        for name in ('CA50','CA-50','CA-50A',' CA50 '):
            r=interpret_steel(raw(name))
            self.assertEqual(r['derived_fyk_mpa'],500)
            self.assertEqual(r['observations'][0]['original_text'],name)

    def test_unknown_even_alongside_known_blocks(self):
        for name in ('CA-60','CA-50B','CA500','',None,500):
            r=interpret_steel(raw('CA50',name))
            self.assertEqual(r['status'],'unrecognized')
            self.assertIsNone(r['derived_fyk_mpa'])

    def test_missing_steel_is_not_defaulted(self):
        self.assertEqual(interpret_steel(raw())['status'],'missing')
        self.assertIsNone(interpret_steel(raw())['derived_fyk_mpa'])

    def test_excluded_report_does_not_govern(self):
        data=raw('CA50','CA-60')
        data['categorias']['materiais'][1]['origem']['arquivo']='RELDTVeT.LST'
        r=interpret_steel(data)
        self.assertEqual(r['status'],'consistent')
        self.assertEqual(r['excluded_observations'][0]['original_text'],'CA-60')

    def test_provenance_and_immutability(self):
        data=raw('CA-50A');before=copy.deepcopy(data)
        r=interpret_steel(data)
        self.assertEqual(r['observations'][0]['provenance']['json_pointer'],'/categorias/materiais/0/campos_explicitos/0')
        self.assertEqual(r['observations'][0]['provenance']['record'],data['categorias']['materiais'][0]['origem'])
        r['observations'][0]['provenance']['record']['texto']='changed'
        self.assertEqual(data,before)


if __name__=='__main__':
    unittest.main()
