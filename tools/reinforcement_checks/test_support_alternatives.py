"""Contract/orchestration tests with current real public Concretopy APIs."""
import importlib.util
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock

from support_alternatives import (generate_alternatives, evaluate_configuration,
    explore_alternatives, effort_pairs, available_length, POSITION_RULE, VALID)

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('left_support_fixture',ROOT/'analises/pranchas/validar_v536_v565_apoio_esquerdo.py')
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
api=fixture.api

class SupportAlternativesTests(TestCase):
    def setUp(self):
        self.ctx,self.current,self.doc=fixture.load_case('V536')
    def configuration(self,n=3,phi=20,counts=None,depths=None,auto=True):
        counts=counts or [n]
        return {'id':'test','layers':[{'count':c,'diameter_mm':phi,'d_cm':None if depths is None else depths[i]} for i,c in enumerate(counts)],'position_rule':POSITION_RULE if auto else None}
    def evaluate(self,config=None,context=None):
        return evaluate_configuration(context or self.ctx,config or self.current,api)
    def test_generation_configurable(self):
        cs=generate_alternatives(diameters_mm=[12.5,16],min_bars=2,max_bars=3,max_layers=2,position_rule=POSITION_RULE)
        self.assertEqual(len(cs),10)
        self.assertEqual({c['layers'][0]['diameter_mm'] for c in cs},{12.5,16})
        self.assertTrue(all(2<=sum(e['count'] for e in c['layers'])<=3 for c in cs))
    def test_search_limits_not_normative(self):
        with self.assertRaises(ValueError):generate_alternatives(diameters_mm=[20],min_bars=4,max_bars=2,max_layers=1)
    def test_one_layer_uses_public_positions(self):
        r=self.evaluate(self.configuration(5,16))
        expected=api.calcular_alturas_uteis_camadas(api.SecaoRetangular(**self.ctx['section']),(api.CamadaArmaduraLongitudinal(5,api.Barra(16)),))
        self.assertEqual(r['flexure']['d_por_camada_cm'],expected)
    def test_multilayer_explicit_positions(self):
        r=self.evaluate(self.configuration(phi=20,counts=[2,2],depths=[68,64],auto=False))
        self.assertTrue(r['complete']);self.assertEqual(r['flexure']['d_por_camada_cm'],(68,64))
    def test_multilayer_automatic_known_convention(self):
        r=self.evaluate(self.configuration(phi=16,counts=[3,2]))
        self.assertTrue(r['complete']);self.assertEqual(len(r['resolved_layers']),2)
        self.assertLess(r['metrics']['d_cm'],r['flexure']['d_por_camada_cm'][0])
    def test_recalculate_d_for_diameter(self):
        self.assertNotEqual(self.evaluate(self.configuration(5,16))['metrics']['d_cm'],self.evaluate()['metrics']['d_cm'])
    def test_recalculate_x_z_for_quantity(self):
        old=self.evaluate()['metrics'];new=self.evaluate(self.configuration(4,20))['metrics']
        self.assertNotEqual(old['x_cm'],new['x_cm']);self.assertNotEqual(old['z_cm'],new['z_cm'])
    def test_independent_pair_calls_and_layers(self):
        spy=Mock(wraps=api.calcular_armadura_positiva_apoio)
        proxy=SimpleNamespace(**{name:getattr(api,name) for name in dir(api) if not name.startswith('_')})
        proxy.calcular_armadura_positiva_apoio=spy
        # provenance expects a callable name/signature; attach name to the spy.
        spy.__name__='calcular_armadura_positiva_apoio'
        r=evaluate_configuration(self.ctx,self.configuration(5,16),proxy)
        self.assertEqual(spy.call_count,2)
        self.assertNotEqual(spy.call_args_list[0].kwargs['vk_apoio_kn'],spy.call_args_list[1].kwargs['vk_apoio_kn'])
        self.assertEqual(spy.call_args_list[1].kwargs['mk_apoio_kncm'],0)
        self.assertTrue(r['complete'])
    def test_greatest_demand_and_ties(self):
        r=self.evaluate()
        self.assertEqual(r['metrics']['As_support_cm2'],max(s['result']['as_necessaria_cm2'] for s in r['states']))
        self.assertEqual(len(r['governing_pairs']),2)
    def test_non_tied_pair_selection(self):
        calls=[]
        def controlled(**kwargs):
            real=api.calcular_armadura_positiva_apoio(**kwargs)
            calls.append(kwargs)
            return replace(real,as_necessaria_cm2=7 if len(calls)==2 else 6)
        proxy=SimpleNamespace(**{name:getattr(api,name) for name in dir(api) if not name.startswith('_')})
        proxy.calcular_armadura_positiva_apoio=controlled
        r=evaluate_configuration(self.ctx,self.current,proxy)
        self.assertEqual(r['metrics']['As_support_cm2'],7)
        self.assertEqual(r['governing_pairs'],['zero_moment_max_abs_shear'])
    def test_no_artificial_positive_moment(self):
        ps=effort_pairs(-20,-30,120,{'source':'test'})
        self.assertEqual(len(ps),1);self.assertEqual(ps[0]['mk_apoio_kncm'],0)
    def test_recalculate_lb_by_diameter(self):
        a=self.evaluate(self.configuration(5,16));b=self.evaluate()
        self.assertNotEqual(a['anchorage']['lb_cm'],b['anchorage']['lb_cm'])
    def test_recalculate_lb_min(self):
        a=self.evaluate(self.configuration(4,25));b=self.evaluate()
        self.assertNotEqual(a['anchorage']['lb_min_cm'],b['anchorage']['lb_min_cm'])
    def test_bond_position_good_poor_boundary(self):
        from bar_scaling import classify_bond
        for d,good in [(68,True),(30,True),(29,False)]:
            r=self.evaluate(self.configuration(2,10,depths=[d],auto=False))
            self.assertEqual(r['bond_by_layer'][0]['boa_aderencia'],good)
        self.assertTrue(classify_bond(50,30)['boa_aderencia'])
    def test_mixed_bond_not_averaged(self):
        r=self.evaluate(self.configuration(phi=10,counts=[1,1],depths=[68,20],auto=False))
        self.assertEqual(r['status'],'NAO_AVALIAVEL_GEOMETRIA');self.assertIsNone(r['passes'])
        self.assertIn('mixed_bond',r['diagnostics'][0]['detail'])
    def test_area_insufficient(self):
        r=self.evaluate(self.configuration(2,10));self.assertEqual(r['status'],'AREA_INSUFICIENTE')
    def test_anchorage_insufficient(self):
        self.assertEqual(self.evaluate()['status'],'ANCORAGEM_INSUFICIENTE')
    def test_below_minimum(self):
        r=self.evaluate(self.configuration(4,25))
        self.assertTrue(r['anchorage']['comprimento_menor_lb_min'])
        self.assertEqual(r['status'],'ABAIXO_LB_MIN')
    def test_valid_zero_additional_area(self):
        r=self.evaluate(self.configuration(5,16));self.assertEqual(r['status'],VALID)
        self.assertEqual(r['anchorage']['as_adicional_cm2'],0);self.assertTrue(r['passes'])
    def test_multiple_diagnostics(self):
        ctx=deepcopy(self.ctx);ctx['support_length_cm']=10
        r=self.evaluate(self.configuration(1,20),ctx)
        codes={d['code'] for d in r['diagnostics']}
        self.assertTrue({'AREA_INSUFICIENTE','ABAIXO_LB_MIN','ANCORAGEM_INSUFICIENTE'}<=codes)
    def test_no_solution(self):
        r=explore_alternatives(self.ctx,self.current,api,search={'diameters_mm':[10],'min_bars':2,'max_bars':3,'max_layers':1,'position_rule':POSITION_RULE})
        self.assertEqual(r['valid_alternative_ids'],[]);self.assertIsNone(r['selected_solution'])
    def test_unknown_layer_position(self):
        r=self.evaluate(self.configuration(3,20,auto=False))
        self.assertEqual(r['status'],'NAO_AVALIAVEL_GEOMETRIA');self.assertIsNone(r['passes'])
    def test_invalid_geometry_or_scope(self):
        for change in [{'support_side':'invalid'},{'cover_cm':24},{'horizontal':False}]:
            ctx={**self.ctx,**change};r=self.evaluate(context=ctx)
            self.assertFalse(r['complete']);self.assertIsNone(r['passes'])
    def test_transverse_limitation_even_when_passing(self):
        r=self.evaluate(self.configuration(5,16))
        self.assertIn('geometria_transversal_nao_verificada',r['limitations'])
        self.assertTrue(r['metrics']['geometria_transversal_nao_verificada'])
    def test_concretopy_rejection_preserved(self):
        r=self.evaluate(self.configuration(8,25))
        self.assertEqual(r['status'],'NAO_AVALIAVEL_GEOMETRIA');self.assertTrue(r['diagnostics'])
    def test_length_distinct_from_documentary(self):
        r=self.evaluate();self.assertEqual(r['available_length']['lb_ef_cm'],21.5)
        self.assertEqual(self.doc['horizontal_projection_inside_support_cm'],21)
    def test_length_validation(self):
        self.assertEqual(available_length(24,2.5,{'source':'test'})['lb_ef_cm'],21.5)
        with self.assertRaises(ValueError):available_length(24,24,{})
    def test_v536_golden_full_bounded_search(self):
        actual=explore_alternatives(self.ctx,self.current,api,search=fixture.SEARCH)
        golden=fixture.read('V536_left_support_anchorage_check.json')['exploration']
        self.assertEqual(len(actual['alternatives']),100)
        self.assertEqual(actual['valid_alternative_ids'],golden['valid_alternative_ids'])
        for a,g in zip(actual['alternatives'],golden['alternatives']):
            with self.subTest(a['configuration']['id']):
                self.assertEqual(a['status'],g['status'])
                if a['complete']:
                    for key,value in a['metrics'].items():
                        if isinstance(value,(int,float)) and not isinstance(value,bool):self.assertAlmostEqual(value,g['metrics'][key],places=10)
                    self.assertEqual(a['governing_pairs'],g['governing_pairs'])
        self.assertFalse(actual['existing']['passes']);self.assertIsNone(actual['selected_solution'])
    def test_v565_corrected_control(self):
        ctx,c,doc=fixture.load_case('V565');r=evaluate_configuration(ctx,c,api)
        golden=fixture.read('V565_left_support_anchorage_check.json')['exploration']['existing']
        self.assertTrue(r['passes']);self.assertEqual(r['anchorage']['as_adicional_cm2'],0)
        self.assertEqual(r['available_length']['lb_ef_cm'],21.5)
        self.assertAlmostEqual(r['metrics']['anchorage_margin_cm'],golden['metrics']['anchorage_margin_cm'])
        ctx['support_length_cm']=23.5
        self.assertFalse(evaluate_configuration(ctx,c,api)['passes'])
    def test_existing_passes_search_not_needed(self):
        ctx,c,doc=fixture.load_case('V565')
        r=explore_alternatives(ctx,c,api,search=fixture.SEARCH)
        self.assertFalse(r['search_executed']);self.assertEqual(r['alternatives'],[])
