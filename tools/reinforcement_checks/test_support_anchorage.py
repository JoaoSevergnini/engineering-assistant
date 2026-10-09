"""Oriented support contracts and real API integrations; no resistant formulas."""
import sys
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'analises/pranchas'),str(ROOT.parent/'concretopy')]
import concretopy as api
from validar_v536_v565_correcao_apoio import load_detail_case
from validar_v536_apoio_direito import build_golden
from support_geometry import SupportGeometry,normalize_type
from support_anchorage import check_support,terminal_section,termination,_control
from support_correction import extension_candidates,preserved_original_reinforcement
from moment_diagram import MomentDiagram
from tqs_shear import select_span_shear


def geom(side='RIGHT',width=120):
    sign=1 if side=='RIGHT' else -1
    return SupportGeometry('span','support',side,'INTERMEDIATE',sign*3,sign*(3+width/100),sign*(3+width/200),width,{'fixture':'synthetic'})


def make_diagram(values=(10,250,-10),xs=(0,2,3),side='RIGHT'):
    pairs=list(zip(xs,values))
    if side=='LEFT':pairs=[(-x,m) for x,m in reversed(pairs)]
    return MomentDiagram([{'section':i+1,'x_m':x,'value_knm':m,'provenance':{'synthetic':True}} for i,(x,m) in enumerate(pairs)],{'fixture':'synthetic characteristic sample'})


def bar(end=3.82,side='RIGHT',phi=20,count=3,shape='straight'):
    a,b=(-.1,end) if side=='RIGHT' else (-end,.1)
    return {'mark':'bar','function':'positive','face':'lower','shape':shape,'bars':count,
        'diameter_mm':phi,'layers':[count],'d_cm':68,'x_start_common':a,'x_end_common':b,
        'source':{'synthetic':True}}


class GeometryTests(TestCase):
    def test_right_directions(self):self.assertEqual((geom().direction_into_support,geom().direction_into_span),(1,-1))
    def test_left_directions(self):self.assertEqual((geom('LEFT').direction_into_support,geom('LEFT').direction_into_span),(-1,1))
    def test_oriented_right_distance(self):self.assertEqual(geom().distance_cm(3,3.82),82)
    def test_oriented_left_distance(self):self.assertEqual(geom('LEFT').distance_cm(-3,-3.82),82)
    def test_required_end_right(self):self.assertEqual(geom().required_end(3,55),3.55)
    def test_required_end_left(self):self.assertEqual(geom('LEFT').required_end(-3,55),-3.55)
    def test_negative_length_rejected(self):
        with self.assertRaises(ValueError):geom().required_end(3,-1)
    def test_before_face(self):self.assertFalse(geom().penetration(bar(2.9))['area_presente_na_face'])
    def test_exact_face(self):
        r=geom().penetration(bar(3));self.assertTrue(r['area_presente_na_face']);self.assertFalse(r['penetra_apoio']);self.assertFalse(r['cruza_face_interna'])
    def test_inside(self):self.assertEqual(geom().penetration(bar())['continuity'],'TERMINATES_IN_SUPPORT')
    def test_cross_support(self):self.assertEqual(geom().penetration(bar(4.3))['continuity'],'CONTINUES_THROUGH_SUPPORT')
    def test_through_preserves_full_interval(self):self.assertEqual(geom().penetration(bar(5))['comprimento_penetracao_cm'],200)
    def test_face_external(self):self.assertEqual(geom().external_face_m,4.2)
    def test_axis(self):self.assertEqual(geom().support_axis_m,3.6)
    def test_inverted_interval(self):
        b=bar();b['x_end_common']=-1
        with self.assertRaises(ValueError):geom().penetration(b)
    def test_width_inconsistent(self):
        with self.assertRaises(ValueError):SupportGeometry('s','p','RIGHT','END',3,4,3.5,120,{'test':1})
    def test_side_required(self):
        with self.assertRaises(ValueError):geom('OTHER')
    def test_identity_required(self):
        with self.assertRaises(ValueError):SupportGeometry(None,'p','RIGHT','END',3,4,3.5,100,{'test':1})
    def test_termination_unknown(self):
        b=bar(shape='bent');self.assertEqual(termination(b,geom(),geom().penetration(b)),'UNKNOWN')
    def test_termination_hook(self):
        b=bar(shape='bent');b['end_bend']={'side':'right'}
        self.assertEqual(termination(b,geom(),geom().penetration(b)),'HOOK')
    def test_straight(self):
        b=bar();self.assertEqual(termination(b,geom(),geom().penetration(b)),'STRAIGHT')
    def test_continuity_not_beam_label(self):
        b=bar();b['continuous_beam']=True
        self.assertEqual(termination(b,geom(),geom().penetration(b)),'STRAIGHT')
    def test_control_negative_geometry_blocks(self):self.assertIsNone(_control(geom(),2.9,3,20,'test')['passes'])
    def test_control_missing(self):self.assertIsNone(_control(geom(),3.8,None,20,'test')['passes'])
    def test_legacy_type_alias(self):self.assertEqual(normalize_type('extremo'),'END')
    def test_right_split_extension(self):
        b=bar(2.9);c=extension_candidates([b],3,3.8,'RIGHT')
        self.assertEqual(len(c),3);self.assertEqual([x['changes'][0]['extended_quantity'] for x in c],[1,2,3])
        self.assertTrue(all(preserved_original_reinforcement([b],x['bars']) for x in c))


class IntermediateTests(TestCase):
    def setUp(self):
        self.ctx,_,_=load_detail_case('V536')
        self.ctx.update(mk_negative_support_kncm=-1000,al_scope_confirmed=True,
                        transverse_geometry_resolved=False,node_interferences_verified=False)
        self.shear=select_span_shear([{'quantity':'shear','unit':'kN','envelope':e,
            'sections':[1,2],'positions':[0,3],'values':[125,-60], 'provenance':{'fixture':'synthetic'}} for e in ('max','min')],[0,3])
    def check(self,values=(10,250,-10),xs=(0,2,3),end=3.82,side='RIGHT',width=120,b=None,ctx=None,shear=True,corrections=False,chosen_api=api):
        return check_support(ctx or self.ctx,b or [bar(end,side)],make_diagram(values,xs,side),chosen_api,
            geometry=geom(side,width),shear=self.shear if shear else None,generate_corrections=corrections)
    def test_positive_classification(self):self.assertEqual(self.check(values=(10,100,180))['classification'],'INTERMEDIATE_WITH_POSITIVE_MOMENT')
    def test_positive_terminal_maximum(self):self.assertTrue(self.check(values=(10,100,180))['last_section_is_positive_maximum'])
    def test_basic_lb_governs_not_reduced(self):
        r=self.check(values=(10,100,180));b=r['longitudinal_bars'][0]
        self.assertEqual(b['controls']['basic_lb']['required_length_cm'],b['basic_lb_cm'])
        self.assertLess(b['lb_nec_cm'],b['basic_lb_cm'])
    def test_straight_alpha_one(self):self.assertEqual(self.check(values=(10,100,180))['longitudinal_bars'][0]['alpha'],1)
    def test_hook_not_credited(self):
        b=bar(shape='bent');b['end_bend']={'side':'right'}
        r=self.check(values=(10,100,180),b=[b]);self.assertIsNone(r['longitudinal_anchorage_passes'])
    def test_continued_not_terminated(self):self.assertIsNone(self.check(values=(10,100,180),end=4.3)['longitudinal_anchorage_passes'])
    def test_unknown_not_approved(self):self.assertIsNone(self.check(values=(10,100,180),b=[bar(shape='unknown')])['longitudinal_anchorage_passes'])
    def test_positive_length_sufficient(self):self.assertTrue(self.check(values=(10,100,180))['longitudinal_anchorage_passes'])
    def test_positive_length_insufficient(self):self.assertFalse(self.check(values=(10,100,180),end=3.4)['longitudinal_anchorage_passes'])
    def test_positive_nonmax_rule_pending(self):
        r=self.check(values=(10,180,100));self.assertIsNone(r['longitudinal_anchorage_passes']);self.assertTrue(r['flexural_demand_resolved'])
    def test_no_positive_C_only(self):
        r=self.check();d=r['concretopy']['support_demand']
        self.assertFalse(d['condicao_a']['aplicavel']);self.assertFalse(d['condicao_b']['aplicavel']);self.assertTrue(d['condicao_c']['aplicavel'])
    def test_positive_A_C_no_B(self):
        r=self.check(values=(10,100,180));d=r['concretopy']['support_demand']
        self.assertTrue(d['condicao_a']['aplicavel']);self.assertFalse(d['condicao_b']['aplicavel'])
    def test_independent_api_type(self):
        proxy=SimpleNamespace(**{name:getattr(api,name) for name in dir(api) if not name.startswith('_')})
        proxy.calcular_armadura_positiva_apoio=Mock(wraps=api.calcular_armadura_positiva_apoio)
        self.check(chosen_api=proxy)
        self.assertEqual(proxy.calcular_armadura_positiva_apoio.call_args.kwargs['tipo_apoio'],'intermediario')
        self.assertEqual(proxy.calcular_armadura_positiva_apoio.call_count,1)
    def test_zero_branch_selected(self):
        r=self.check(values=(-10,250,-10))
        self.assertGreater(r['zero_moment_check']['reference_x_m'],2)
        self.assertEqual(len(r['moment_references']['zero']['crossings']['crossings']),2)
    def test_zero_left_branch(self):
        r=self.check(values=(-10,250,-10),side='LEFT');self.assertLess(r['zero_moment_check']['reference_x_m'],-2)
    def test_mirror_same_lengths(self):
        a=self.check();b=self.check(side='LEFT')
        for key in ('base_penetration_check','zero_moment_check','full_utilization_check'):
            self.assertAlmostEqual(a[key]['available_length_cm'],b[key]['available_length_cm'])
            self.assertAlmostEqual(a[key]['required_length_cm'],b[key]['required_length_cm'])
    def test_shear_required(self):self.assertIsNone(self.check(shear=False)['longitudinal_anchorage_passes'])
    def test_al_centroid_from_concretopy(self):
        r=self.check();self.assertEqual(r['d_for_al']['d_cm'],r['concretopy']['flexure']['d_equivalente_cm'])
    def test_al_scope_unconfirmed(self):self.assertIsNone(self.check(ctx={**self.ctx,'al_scope_confirmed':False})['longitudinal_anchorage_passes'])
    def test_zero_controls_governs(self):self.assertIn('zero',self.check()['longitudinal_bars'][0]['governing_rules'])
    def test_full_utilization_governs(self):
        r=self.check(xs=(0,2.8,3),end=4.1);self.assertIn('full_utilization',r['longitudinal_bars'][0]['governing_rules'])
        self.assertGreater(r['longitudinal_bars'][0]['required_end_position_m']-3,.3)
    def test_absent_full_crossing_sufficient_not_fabricated(self):
        r=self.check(values=(10,100,-10));c=r['full_utilization_check']
        self.assertEqual(c['status'],'NOT_APPLICABLE');self.assertIsNone(c['reference_x_m']);self.assertTrue(c['passes'])
    def test_peak_plateau_blocks(self):self.assertIsNone(self.check(values=(250,250,-10))['longitudinal_anchorage_passes'])
    def test_missing_moment_blocks(self):self.assertIsNone(self.check(values=(10,250,None))['longitudinal_anchorage_passes'])
    def test_no_face_bars_blocks(self):self.assertIsNone(self.check(end=2.9)['longitudinal_anchorage_passes'])
    def test_face_area_not_anchored(self):
        r=self.check(values=(10,100,180),end=3)
        self.assertGreater(r['effective_area_at_face_cm2'],0);self.assertEqual(r['longitudinal_bars'][0]['area_anchored_cm2'],0)
    def test_area_insufficient(self):self.assertFalse(self.check(values=(10,250,350))['area_sufficient'])
    def test_no_correction_when_passes(self):
        r=self.check(values=(10,100,180),corrections=True);self.assertFalse(r['correction_required']);self.assertEqual(r['corrections'],[])
    def test_own_extension_rechecks(self):
        r=self.check(values=(10,100,180),end=3.4,corrections=True)
        self.assertTrue(r['correction_required']);self.assertTrue(r['corrections'][0]['result']['longitudinal_anchorage_passes'])
        self.assertIsNone(r['selected_solution'])
    def test_transverse_pending(self):self.assertIsNone(self.check(values=(10,100,180))['support_verified'])
    def test_terminal_first_for_left(self):self.assertEqual(terminal_section(make_diagram(side='LEFT'),geom('LEFT'))['x_m'],-3)
    def test_terminal_last_for_right(self):self.assertEqual(terminal_section(make_diagram(),geom())['x_m'],3)
    def test_max_basic_not_end_width_cover(self):self.assertEqual(self.check(values=(10,100,180))['anchorage_reference'],3)


class BasePenetrationTests(TestCase):
    setUp=IntermediateTests.setUp
    check=IntermediateTests.check
    def test_support_20_external_face(self):self.assertEqual(self.check(width=20,end=3.19)['base_penetration_check']['required_length_cm'],20)
    def test_support_25_external_face(self):self.assertEqual(self.check(width=25,end=3.24)['base_penetration_check']['required_length_cm'],25)
    def test_support_30(self):self.assertEqual(self.check(width=30,end=3.29)['base_penetration_check']['required_length_cm'],30)
    def test_support_50_cap_base_only(self):self.assertEqual(self.check(width=50,end=3.49)['base_penetration_check']['required_length_cm'],30)
    def test_ten_phi_governs_small_support(self):self.assertEqual(self.check(width=15,end=3.14)['base_penetration_check']['required_length_cm'],20)


class RealRightGoldenTests(TestCase):
    @classmethod
    def setUpClass(cls):cls.result=build_golden()
    def test_identity(self):
        g=self.result['geometry'];self.assertEqual(g['support_side'],'RIGHT');self.assertEqual(g['support_type'],'INTERMEDIATE');self.assertEqual(g['support_id'],'P7A')
    def test_terminal_S13(self):self.assertEqual(self.result['last_span_section']['section'],13)
    def test_terminal_maximum(self):self.assertTrue(self.result['last_section_is_positive_maximum'])
    def test_n2_n3(self):self.assertEqual([r['bar']['mark'] for r in self.result['longitudinal_bars']],['N2','N3'])
    def test_penetration(self):self.assertEqual(self.result['available_penetration_cm'],82)
    def test_basic_real_api(self):self.assertAlmostEqual(self.result['basic_lb_cm'],55.0716891039194)
    def test_straight_no_hook(self):self.assertTrue(all(r['termination_type']=='STRAIGHT' and r['alpha']==1 for r in self.result['longitudinal_bars']))
    def test_pass_no_correction(self):self.assertTrue(self.result['longitudinal_anchorage_passes']);self.assertFalse(self.result['correction_required']);self.assertEqual(self.result['corrections'],[])
    def test_node_unresolved(self):self.assertFalse(self.result['transverse_geometry_resolved']);self.assertFalse(self.result['node_interferences_verified']);self.assertIsNone(self.result['support_verified'])


class EndOrientationTests(TestCase):
    def test_right_local_pairs_preserved(self):
        from support_alternatives import evaluate_configuration
        from validar_v536_v565_apoio_esquerdo import load_case
        ctx,cfg,_=load_case('V536')
        left=evaluate_configuration(ctx,cfg,api)
        ctx.update(support_side='RIGHT',support_type='END')
        right=evaluate_configuration(ctx,cfg,api)
        self.assertEqual(right['metrics'],left['metrics'])
        self.assertEqual(right['states'],left['states'])
    def test_v565_end_existing_stops(self):
        from support_correction import correction_workflow
        ctx,bars,diagram=load_detail_case('V565')
        ctx['support_side']='RIGHT'
        mirrored=deepcopy(bars)
        for b in mirrored:
            b['x_start_common'],b['x_end_common']=-b['x_end_common'],-b['x_start_common']
        ctx['support_reference_x_m']=-ctx['support_reference_x_m']
        ctx['extension_target_x_m']=-ctx['extension_target_x_m']
        points=[{**deepcopy(p),'x_m':-p['x_m']} for p in reversed(diagram.points)]
        reflected=MomentDiagram(points,{'fixture':'synthetic geometry/force reflection for symmetry only'})
        result=correction_workflow(ctx,mirrored,reflected,api,redistribution_search={'series':[10,12.5,16,20,25],'counts':[2,3],'max_steps':2})
        # With complete mirrored synthetic regional evidence, the existing configuration passes without correction.
        self.assertTrue(result['existing']['support_check']['passes'])
        self.assertEqual(result['extensions'],[])
    def test_end_geometry_uses_face_composition(self):
        ctx,bars,diagram=load_detail_case('V536')
        g=SupportGeometry('V536:1','left','LEFT','END',.12,-.12,0,24,{'fixture':'audited'})
        r=check_support(ctx,bars,diagram,api,geometry=g,generate_corrections=False)
        self.assertFalse(r['longitudinal_anchorage_passes'])
        self.assertEqual(r['available_penetration_cm'],21.5)
        self.assertEqual(r['effective_area_at_face_cm2'],api.Barra(20).area_cm2*3)
