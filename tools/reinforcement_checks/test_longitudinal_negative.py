"""Contracts of negative review using real public Concretopy; no resistant formulas."""
from pathlib import Path
import sys,json
from copy import deepcopy
from unittest import TestCase
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT.parent/'concretopy'),str(ROOT/'analises/pranchas')]
import concretopy as api
from longitudinal_review import prepare_reinforcement,check_flexure_regions,composition_capacity,check_bar_event,basic_anchorage
from negative_detailing import check_stirrup_holder,check_intermediate_continuity,check_negative_end_node,check_cantilever_free_end
from moment_diagram import MomentDiagram,tension_diagram,terminal_tension_branch
from support_geometry import SupportGeometry,LongitudinalOrientation
from tqs_shear import select_span_shear
from validar_v1001_negativo import build_golden


def context():
 return {'section':{'bw':19,'h':72,'cobrimento':2.5,'diametro_estribo_mm':5},'fck_mpa':40,'fyk_mpa':500,
  'gamma_f':1.4,'gamma_c':1.4,'gamma_s':1.15,'horizontal':True,'sliding_formwork':False,
  'al_scope_confirmed':True,'longitudinal_provenance':{'synthetic':'explicit uniform geometry'},
  'layer_order_basis':'from_tension_face','layer_order_provenance':{'synthetic':'physical layers read from top face'},
  'support_element':'COLUMN','support_scenario_provenance':{'synthetic':'engineer supplied scenario'},
  'cantilever_type':'SINGLE_FIXED_COLUMN','span_count':1}


def bar(mark='B1',layer=1,count=2,phi=16,start=0,end=4):
 return {'mark':mark,'function':'negative','face':'upper','bars':count,'diameter_mm':phi,
  'layers':[0]*(layer-1)+[count],'shape':'straight','x_start_common':start,'x_end_common':end,'source':{'synthetic':'bar'}}


def diagram(values=(0,-180,0),xs=(0,2,4)):
 return MomentDiagram([{'section':i+1,'x_m':x,'value_knm':m,'source_type':'tqs_section','provenance':{'synthetic':True}} for i,(x,m) in enumerate(zip(xs,values))],{'synthetic':'signed characteristic moments'})


def shear():
 return select_span_shear([{'quantity':'shear','unit':'kN','envelope':e,'sections':[1,2],
  'positions':[0,4],'values':[125,-80],'provenance':{'synthetic':True}} for e in ('max','min')],[0,4])


class NegativeGeometryAndFlexureTests(TestCase):
 def setUp(self):self.ctx=context()
 def prepare(self,bars):return prepare_reinforcement(bars,self.ctx,api,flexure_sign='NEGATIVE')
 def test_one_layer(self):self.assertEqual(len(self.prepare([bar()])[0]['d_by_layer_cm']),1)
 def test_two_layers(self):self.assertAlmostEqual(self.prepare([bar(),bar('B2',2)])[1]['d_cm'],64.6)
 def test_three_layers(self):self.assertAlmostEqual(self.prepare([bar(),bar('B2',2),bar('B3',3)])[2]['d_cm'],61)
 def test_one_mark_multiple_layers(self):
  b=bar(count=3);b['layers']=[2,1]
  p=self.prepare([b])[0];self.assertAlmostEqual(p['d_by_layer_cm'][0],68.2);self.assertAlmostEqual(p['d_by_layer_cm'][1],64.6);self.assertIsNone(p['d_cm'])
 def test_bottom_coordinate_is_negative_depth(self):
  self.ctx['layer_centers']=[{'documentary_layer':1,'origin':'BOTTOM','value_cm':68,'provenance':{'drawing':1}}]
  self.assertEqual(self.prepare([bar()])[0]['d_cm'],68)
 def test_top_coordinate_transforms(self):
  self.ctx['layer_centers']=[{'documentary_layer':1,'origin':'TOP','value_cm':4,'provenance':{'drawing':1}}]
  self.assertEqual(self.prepare([bar()])[0]['d_cm'],68)
 def test_layer_order_geometrical(self):
  self.ctx['layer_centers']=[{'documentary_layer':1,'origin':'BOTTOM','value_cm':60,'provenance':{'drawing':1}},
   {'documentary_layer':2,'origin':'BOTTOM','value_cm':68,'provenance':{'drawing':1}}]
  p=self.prepare([bar('N99'),bar('N1',2)]);self.assertEqual(p[1]['layers'],[2,0]);self.assertEqual(p[0]['layers'],[0,2])
 def test_unknown_coordinate_blocks(self):
  self.ctx.pop('layer_order_provenance')
  with self.assertRaises(ValueError):self.prepare([bar()])
 def test_face_mismatch(self):
  b=bar();b['face']='lower'
  with self.assertRaises(ValueError):self.prepare([b])
 def test_source_missing(self):
  b=bar();b.pop('source')
  with self.assertRaises(ValueError):self.prepare([b])
 def test_diagram_original_not_mutated(self):
  d=diagram();old=d.as_dict();v=tension_diagram(d,'NEGATIVE');self.assertEqual(d.as_dict(),old);self.assertEqual(v.ms[1],180)
 def test_opposite_sign_not_absolute(self):self.assertEqual(tension_diagram(diagram((10,-100,20)),'NEGATIVE').ms[0],-10)
 def test_signed_negative_demand(self):
  r=check_flexure_regions([bar(count=3)],self.ctx,diagram((0,-100,0)),api,flexure_sign='NEGATIVE')
  self.assertEqual(r['regions'][0]['governing_moment_signed'],-100);self.assertEqual(r['regions'][0]['governing_moment_abs'],100)
 def test_capacity_passes(self):self.assertTrue(check_flexure_regions([bar(count=3)],self.ctx,diagram((0,-100,0)),api,flexure_sign='NEGATIVE')['passes'])
 def test_capacity_fails(self):self.assertFalse(check_flexure_regions([bar()],self.ctx,diagram((0,-400,0)),api,flexure_sign='NEGATIVE')['passes'])
 def test_regional_composition(self):
  r=check_flexure_regions([bar(count=3),bar('B2',2,start=1,end=3)],self.ctx,diagram((0,-150,0)),api,flexure_sign='NEGATIVE')
  self.assertEqual([r['configuration']['provenance']['composition']['marks'] for r in r['regions']],[['B1'],['B1','B2'],['B1']])
 def test_remaining_positions_preserved(self):
  bars=self.prepare([bar(),bar('B2',2),bar('B3',3)])
  full=composition_capacity(bars,2,self.ctx,api,flexure_sign='NEGATIVE')
  reduced=composition_capacity(bars[:2],2,self.ctx,api,flexure_sign='NEGATIVE')
  self.assertEqual(reduced['concretopy']['d_por_camada_cm'],full['concretopy']['d_por_camada_cm'][:2])
 def test_more_than_three_layers_not_hardcoded(self):self.assertEqual(len(self.prepare([bar('L'+str(i),i) for i in range(1,5)])[-1]['layers']),4)
 def test_positive_generic_face(self):
  b=bar();b.update(function='positive',face='lower')
  p=prepare_reinforcement([b],self.ctx,api,flexure_sign='POSITIVE');self.assertEqual(p[0]['d_cm'],68.2)
 def test_negative_mixed_bond_not_inferred(self):
  r=basic_anchorage(16,self.ctx,api,flexure_sign='NEGATIVE');self.assertEqual(r['bond_condition'],'POOR');self.assertEqual(r['result']['eta2'],.7)
 def test_missing_moment_unresolved(self):self.assertIsNone(check_flexure_regions([bar()],self.ctx,diagram((0,None,0)),api,flexure_sign='NEGATIVE')['passes'])
 def test_branch_terminal_right(self):self.assertEqual(terminal_tension_branch(diagram((-50,10,-100)),'NEGATIVE','RIGHT'),[2,4])
 def test_branch_terminal_left(self):self.assertEqual(terminal_tension_branch(diagram((-50,10,-100)),'NEGATIVE','LEFT'),[0,2])
 def test_nonnegative_region_not_applicable(self):
  r=check_flexure_regions([bar()],self.ctx,diagram((10,20,30)),api,flexure_sign='NEGATIVE');self.assertEqual(r['regions'][0]['status'],'NOT_APPLICABLE')


class NegativeEventTests(TestCase):
 def setUp(self):
  self.ctx=context();self.bars=[bar('B1',1,end=4),bar('B2',2,end=3.9),bar('B3',3,end=3.6)]
 def check(self,mark='B3',side='RIGHT',mode='SCALING',bars=None,d=None,ctx=None,v=True):
  return check_bar_event(bars or self.bars,ctx or self.ctx,d or diagram(),shear() if v else None,api,mark=mark,cut_side=side,mode=mode)
 def test_unresolved_positions_preserve_independent_lb(self):
  ctx=deepcopy(self.ctx);ctx.pop('layer_order_provenance')
  result=self.check(ctx=ctx);self.assertIsNone(result['passes']);self.assertGreater(result['lb_basic_cm'],0);self.assertEqual(result['ten_phi_cm'],16)
 def test_third_layer_remaining_two(self):self.assertEqual([b['mark'] for b in self.check()['reinforcement_after_cut']],['B1','B2'])
 def test_second_layer_remaining_first(self):self.assertEqual([b['mark'] for b in self.check('B2')['reinforcement_after_cut']],['B1'])
 def test_successive_second_cut_allows_extra_upstream(self):self.assertTrue(self.check('B2')['complete']);self.assertTrue(self.check('B2')['upstream_additional_reinforcement'])
 def test_before_centroid_used(self):
  r=self.check();self.assertEqual(r['d_for_al']['d_cm'],r['before_capacity']['concretopy']['d_equivalente_cm']);self.assertNotEqual(r['d_for_al']['d_cm'],r['capacity_remaining']['concretopy']['d_equivalente_cm'])
 def test_basic_lb_not_reduced(self):
  r=self.check();self.assertEqual(r['checks']['al_plus_lb']['required_length_cm'],r['al']['result']['al_cm']+r['anchorage']['result']['lb_cm'])
 def test_ten_phi(self):self.assertEqual(self.check()['ten_phi_cm'],16)
 def test_negative_peak_internal(self):self.assertEqual(self.check()['peak_or_decay_reference']['peak_location'],'internal')
 def test_peak_preserves_signed(self):self.assertEqual(self.check()['peak_or_decay_reference']['Msk_signed'],-180)
 def test_crossing_interpolated(self):self.assertEqual(self.check()['capacity_crossing']['selected_crossing']['status'],'crossing')
 def test_crossing_exact(self):
  first=self.check();cap=first['capacity_remaining']['Mk_equivalent_knm'];r=self.check(d=diagram((0,-180,-cap,0),(0,1,2,4)))
  self.assertEqual(r['capacity_crossing']['selected_x_nec_m'],2)
 def test_all_crossings_preserved(self):self.assertEqual(len(self.check()['capacity_crossing']['crossings']['crossings']),2)
 def test_correct_right_branch(self):self.assertGreater(self.check()['capacity_crossing']['selected_x_nec_m'],2)
 def test_mirrored_left(self):
  bars=deepcopy(self.bars)
  for b in bars:b['x_start_common'],b['x_end_common']=-b['x_end_common'],-b['x_start_common']
  a=self.check();b=self.check(side='LEFT',bars=bars,d=diagram((0,-180,0),(-4,-2,0)))
  for key in ('al_plus_lb','al_plus_10phi'):self.assertAlmostEqual(a['checks'][key]['available_length_cm'],b['checks'][key]['available_length_cm'])
 def test_missing_shear_partial(self):r=self.check(v=False);self.assertIsNone(r['passes']);self.assertIsNotNone(r['anchorage'])
 def test_plateau_unresolved(self):self.assertIsNone(self.check(d=diagram((-180,-180,0)))['passes'])
 def test_no_capacity_crossing(self):self.assertIsNone(self.check(d=diagram((0,-50,0)))['passes'])
 def test_no_zero_termination(self):self.assertIsNone(self.check('B1',mode='SPAN_TERMINATION',d=diagram((-10,-180,-10)))['passes'])
 def test_termination_zero_selected(self):
  r=self.check('B1',mode='SPAN_TERMINATION');self.assertEqual(r['checks']['al_plus_10phi']['reference_x_m'],4)
 def test_termination_uses_own_capacity_crossing(self):
  r=self.check('B1',mode='SPAN_TERMINATION');self.assertEqual(r['checks']['al_plus_lb']['reference_x_m'],r['capacity_crossing']['selected_x_nec_m'])
 def test_no_full_utilization_legitimate_not_applicable(self):
  r=self.check('B1',mode='SPAN_TERMINATION',d=diagram((0,-50,0)));self.assertEqual(r['checks']['al_plus_lb']['status'],'NOT_APPLICABLE')
 def test_peak_endpoint(self):
  r=self.check(d=diagram((-180,-100,0),(0,1,4)));self.assertEqual(r['peak_or_decay_reference']['peak_location'],'endpoint')
 def test_required_end_not_changed_to_actual(self):
  r=self.check('B2');self.assertNotEqual(r['required_end_position_m'],r['actual_end_position_m'])
 def test_original_bar_not_mutated(self):old=deepcopy(self.bars);self.check();self.assertEqual(self.bars,old)
 def test_coincident_cuts_independent(self):
  b=deepcopy(self.bars);b[1]['x_end_common']=3.6;r=self.check(bars=b);self.assertEqual(r['termination_event']['other_coincident_marks'],['B2']);self.assertEqual([x['mark'] for x in r['reinforcement_after_cut']],['B1'])


class HolderTests(TestCase):
 def holder(self,phi=6.3,start=0,end=4):return {'mark':'H','function':'stirrup_holder','function_provenance':{'drawing':'holder convention'},'diameter_mm':phi,'x_start_common':start,'x_end_common':end}
 def stir(self,phi=5,start=0,end=4):return {'x_start_common':start,'x_end_common':end,'diameter_mm':phi,'provenance':{'drawing':'regional stirrup'}}
 def check(self,phi=5,h=None,regions=None):return check_stirrup_holder(h or self.holder(phi=max(6.3,phi)),regions if regions is not None else [self.stir(phi)],diagram((0,100,0)))
 def test_phi_5(self):self.assertEqual(self.check(5)['required_diameter_mm'],6.3)
 def test_phi_6_3(self):self.assertEqual(self.check(6.3)['required_diameter_mm'],6.3)
 def test_phi_8(self):self.assertEqual(self.check(8)['required_diameter_mm'],8)
 def test_phi_10(self):self.assertEqual(self.check(10)['required_diameter_mm'],10)
 def test_local_region_only(self):self.assertEqual(self.check(h=self.holder(start=0,end=1),regions=[self.stir(5,0,2),self.stir(10,2,4)])['required_diameter_mm'],6.3)
 def test_crosses_change_pending(self):r=self.check(regions=[self.stir(5,0,2),self.stir(8,2,4)]);self.assertIsNone(r['passes']);self.assertEqual(len(r['regions']),2)
 def test_missing_stirrups(self):self.assertIsNone(self.check(regions=[])['passes'])
 def test_missing_interval(self):self.assertIsNone(self.check(regions=[{'diameter_mm':5}])['passes'])
 def test_negative_demand_not_holder(self):self.assertIsNone(check_stirrup_holder(self.holder(),[self.stir()],diagram())['passes'])
 def test_unknown_upper_function(self):h=self.holder();h.pop('function_provenance');self.assertEqual(self.check(h=h)['classification'],'UNKNOWN')
 def test_skin_explicit(self):h=self.holder();h['explicit_skin']=True;self.assertEqual(self.check(h=h)['classification'],'SKIN')
 def test_area_not_inferred_as_skin(self):h=self.holder();h['cut_dots_at_sides']=True;self.assertEqual(self.check(h=h)['classification'],'STIRRUP_HOLDER')
 def test_skin_without_documentary_identity_unknown(self):
  self.assertEqual(self.check(h={**self.holder(),'function':'skin','function_provenance':None})['classification'],'UNKNOWN')
 def test_holder_diameter_insufficient(self):self.assertFalse(self.check(10,h=self.holder())['passes'])


class NegativeNodeTests(TestCase):
 def setUp(self):self.ctx=context();self.b=bar(start=-.9,end=2);self.g=SupportGeometry('s','p','LEFT','END',0,-1,-.5,100,{'synthetic':True})
 def check(self,scenario='FRAME_END',width=100,b=None,ctx=None,leg=None):
  g=SupportGeometry('s','p','LEFT','END',0,-width/100,-width/200,width,{'synthetic':True})
  return check_negative_end_node(b or (bar(start=-.2,end=2) if width==24 else self.b),ctx or self.ctx,g,api,scenario=scenario,bend_leg_cm=leg,bend_provenance={'drawing':'leg'})
 def test_straight_possible(self):self.assertTrue(self.check()['straight_anchorage_passes'])
 def test_straight_short(self):self.assertFalse(self.check(b=bar(start=-.2,end=2))['passes'])
 def test_bend_required(self):self.assertEqual(self.check(width=24,b=bar(start=-.2,end=2))['anchorage_mode'],'BEND_REQUIRED')
 def test_bend_geometry_governs(self):self.assertEqual(self.check(width=24)['bend_governing'],'GEOMETRY')
 def test_bend_two_lb_governs(self):
  ctx=deepcopy(self.ctx);ctx['section']['h']=180
  self.assertEqual(self.check(width=24,ctx=ctx)['bend_governing'],'TWO_BASIC_LB')
 def test_bend_no_fabrication_C(self):r=self.check(width=24);self.assertFalse(r['fabrication_geometry_complete']);self.assertNotIn('fabrication_C_cm',r)
 def test_bend_not_anchorage_approval(self):self.assertIsNone(self.check(width=24,leg=70)['passes'])
 def test_no_positive_staples(self):self.assertNotIn('staples',self.check(width=24))
 def test_single_cantilever_1_5lb(self):
  r=self.check('SINGLE_CANTILEVER_COLUMN');self.assertEqual(r['straight_required_cm'],1.5*r['anchorage']['result']['lb_cm'])
 def test_single_cantilever_fits(self):self.assertTrue(self.check('SINGLE_CANTILEVER_COLUMN',b=bar(start=-1,end=2),width=120)['passes'])
 def test_single_cantilever_no_space_bend(self):self.assertEqual(self.check('SINGLE_CANTILEVER_COLUMN',width=24)['anchorage_mode'],'BEND_REQUIRED')
 def test_area_excess_not_reduce(self):
  a=self.check('SINGLE_CANTILEVER_COLUMN');b=self.check('SINGLE_CANTILEVER_COLUMN',b=bar(count=10,start=-.9,end=2))
  self.assertEqual(a['straight_required_cm'],b['straight_required_cm'])
 def test_non_single_scope_blocked(self):self.assertIsNone(self.check('SINGLE_CANTILEVER_COLUMN',ctx={**self.ctx,'span_count':2})['passes'])
 def test_other_cantilever_blocked(self):self.assertIsNone(self.check('SINGLE_CANTILEVER_COLUMN',ctx={**self.ctx,'cantilever_type':'CONTINUOUS_OVERHANG'})['passes'])
 def test_free_tail(self):r=check_cantilever_free_end(self.ctx,bend_leg_cm=66.5,provenance={'drawing':'free bend'});self.assertTrue(r['passes']);self.assertEqual(r['required_leg_cm'],66.5)
 def test_free_tail_short_governs(self):r=check_cantilever_free_end(self.ctx,bend_leg_cm=20,provenance={'drawing':1});self.assertFalse(r['passes']);self.assertEqual(r['governing_conditions'],['FREE_END_TAIL'])
 def test_other_control_fails(self):self.assertFalse(check_cantilever_free_end(self.ctx,bend_leg_cm=70,provenance={'drawing':1},other_checks=[{'passes':False,'rule':'AL_LB'}])['passes'])
 def test_missing_tail_unknown(self):self.assertIsNone(check_cantilever_free_end(self.ctx)['passes'])
 def test_free_end_does_not_invent_longitudinal_tail(self):self.assertEqual(check_cantilever_free_end(self.ctx)['tail_mode'],'FREE_END_BEND_LEG')
 def test_node_mirror_right(self):
  b=bar(start=-2,end=.9);g=SupportGeometry('s','p','RIGHT','END',0,1,.5,100,{'synthetic':True})
  self.assertEqual(check_negative_end_node(b,self.ctx,g,api)['straight_anchorage_passes'],self.check()['straight_anchorage_passes'])


class ContinuityTests(TestCase):
 def setUp(self):
  self.left=SupportGeometry('s1','p','RIGHT','INTERMEDIATE',0,1,.5,100,{'synthetic':True})
  self.right=SupportGeometry('s2','p','LEFT','INTERMEDIATE',1,0,.5,100,{'synthetic':True})
  self.b=bar(start=-2,end=3);self.b.update(trajectory_id='line1',physical_layer_id='TOP1',continuity_documentation={'drawing':'single physical piece'})
 def check(self,a=True,b=True,left=None,right=None):return check_intermediate_continuity(left or self.b,right or self.b,self.left,self.right,{'passes':a,'required_end_position_m':-1.3},{'passes':b,'required_end_position_m':2.8})
 def test_continuous_both_pass(self):self.assertTrue(self.check()['passes'])
 def test_independent_one_fails(self):self.assertFalse(self.check(b=False)['passes'])
 def test_one_unknown_not_approval(self):self.assertIsNone(self.check(b=None)['passes'])
 def test_physical_continuity_alone_insufficient(self):self.assertIsNone(self.check(a=None,b=None)['passes'])
 def test_different_extensions_preserved(self):r=self.check();self.assertNotEqual(r['required_extension_left_span'],r['required_extension_right_span'])
 def test_unknown_evidence(self):b=deepcopy(self.b);b.pop('continuity_documentation');self.assertEqual(self.check(right=b)['continuity'],'UNKNOWN')
 def test_different_phi_not_continuous(self):b=deepcopy(self.b);b['diameter_mm']=20;self.assertEqual(self.check(right=b)['continuity'],'UNKNOWN')
 def test_different_layer_not_continuous(self):b=deepcopy(self.b);b['physical_layer_id']='TOP2';self.assertEqual(self.check(right=b)['continuity'],'UNKNOWN')
 def test_terminates_in_support(self):b=deepcopy(self.b);b['x_end_common']=.9;self.assertEqual(self.check(left=b)['continuity'],'TERMINATES_IN_SUPPORT')


class V1001NegativeRealGoldenTests(TestCase):
 @classmethod
 def setUpClass(cls):cls.result=build_golden()
 def test_real_two_layers(self):self.assertEqual([b['mark'] for b in self.result['flexure']['physical_reinforcement']],['N7','N8'])
 def test_capacity_real(self):self.assertTrue(self.result['flexure']['passes']);self.assertAlmostEqual(self.result['flexure']['regions'][-1]['governing_moment_signed'],-194.9365887)
 def test_scaling_real(self):self.assertTrue(self.result['scaling']['passes']);self.assertEqual(self.result['scaling']['actual_end_position_m'],6)
 def test_poor_bond_real(self):self.assertEqual(self.result['scaling']['anchorage']['bond_condition'],'POOR')
 def test_before_after_real(self):self.assertEqual([b['mark'] for b in self.result['scaling']['reinforcement_after_cut']],['N7'])
 def test_no_global_approval(self):self.assertIsNone(self.result['global_negative_approval']);self.assertIsNone(self.result['selected_solution'])
 def test_persisted_physical_results(self):
  saved=json.loads((ROOT/'analises/pranchas/V1001_negative_reinforcement_golden.json').read_text(encoding='utf-8-sig'))
  self.assertEqual({name:{key:actual[key] for key in saved['scaling']['checks'][name]} for name,actual in self.result['scaling']['checks'].items()},saved['scaling']['checks'])
