import copy
from dataclasses import replace
from functools import wraps
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

from bar_scaling import check_scaling_event, check_bar_scaling, classify_bond, locate_references, SUPPORTED_SCOPE, DEPTH_RULE
from flexure_regions import decompose_regions
from moment_diagram import MomentDiagram
from tqs_shear import select_span_shear, shear_from_tqs
from test_flexure_regions import bar, transverse
from v1001_scaling import analyze, NAMES, SCOPE

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.parent/'concretopy'))
import concretopy as api


def diagram(points):
    return MomentDiagram([{'section': i+1, 'x_m': x, 'value_knm': m,
                           'provenance': {'input': 'synthetic', 'index': i}}
                          for i, (x, m) in enumerate(points)], {'input': 'synthetic'})


def shear(values=(20, -30)):
    return select_span_shear([{'quantity': 'shear', 'unit': 'kN', 'envelope': 'synthetic',
        'sections': list(range(1, len(values)+1)), 'positions': list(range(len(values))),
        'values': list(values), 'provenance': {'input': 'synthetic'}}], [0, 6])


def altered_api(name, function):
    # Preserve the actual public signature/defaults for the production adapter.
    wrapped = wraps(getattr(api, name))(function)
    return SimpleNamespace(**{**vars(api), name: wrapped})


class ScalingTests(unittest.TestCase):
    def setup_case(self, end=4.5, points=None, side='right'):
        bars = [bar('CUT', .1, end, diameter=10), bar('KEEP', .1, 5.9, diameter=10)]
        for b in bars:
            b['shape'] = 'straight'
        points = points or [(0, 0), (1, 100), (4, 0), (6, -10)]
        if side == 'left':
            for b in bars:
                b['x_start_common'], b['x_end_common'] = 6-b['x_end_common'], 6-b['x_start_common']
            points = [(6-x, m) for x, m in reversed(points)]
        mapping = {'beam_id': 'SYNTHETIC', 'reinforcement': bars,
                   'supports': {'left': {'axis_x': 0, 'inner_face_x': 0},
                                'right': {'axis_x': 6, 'inner_face_x': 6}}}
        review = {'regions': decompose_regions(bars, [0, 6], [transverse(0, 6)]),
                  'material_parameters': {'fck_mpa': 40, 'gamma_f': 1.4, 'provenance': 'synthetic'},
                  'material_interpretation': {'status': 'consistent', 'derived_fyk_mpa': 500, 'provenance': 'synthetic'}}
        kwargs = {'interrupted_mark': 'CUT', 'cut_side': side,
                  'scope': {**SUPPORTED_SCOPE, 'provenance': {'input': 'synthetic'}}}
        return [mapping, review, diagram(points), shear(), api], kwargs

    def run_case(self, **kwargs):
        args, options = self.setup_case(**kwargs)
        return check_scaling_event(*args, **options)

    def assert_conditions(self, out, a, b):
        self.assertEqual(out['diagnostics'], [])
        self.assertTrue(out['overall']['complete'])
        self.assertIs(out['condition_A']['passes'], a)
        self.assertIs(out['condition_B']['passes'], b)
        self.assertIs(out['overall']['scaling_passes'], a and b)
        self.assertEqual(out['condition_A']['al_cm'], out['condition_B']['al_cm'])
        self.assertEqual(out['concretopy']['al_result']['al_cm'], 68.5)

    def test_A_right_both_pass(self):
        out = self.run_case()
        self.assert_conditions(out, True, True)
        self.assertEqual(out['composition_before']['marks'], ['CUT', 'KEEP'])
        self.assertEqual(out['composition_after']['marks'], ['KEEP'])
        self.assertEqual(out['remaining_capacity']['concretopy_result']['as_total_cm2'], api.Barra(10).area_cm2*2)

    def test_B_only_A_fails(self):
        self.assert_conditions(self.run_case(end=3.4), False, True)

    def test_C_only_B_fails(self):
        self.assert_conditions(self.run_case(end=1.88, points=[(0, 0), (1, 100), (1.1, 10), (6, -10)]), True, False)

    def test_D_both_fail(self):
        self.assert_conditions(self.run_case(end=1.5, points=[(0, 0), (1, 100), (1.1, 10), (6, -10)]), False, False)

    def test_E_left_symmetric(self):
        right, left = self.run_case(), self.run_case(side='left')
        self.assert_conditions(left, True, True)
        for key in ('condition_A', 'condition_B'):
            self.assertAlmostEqual(left[key]['available_length_cm'], right[key]['available_length_cm'])
        self.assertEqual(left['composition_after']['marks'], ['KEEP'])

    def test_F_no_valid_crossing(self):
        out = self.run_case(points=[(0, 50), (1, 100), (6, 50)])
        self.assertIsNone(out['overall']['scaling_passes'])
        self.assertIn('no_valid_crossing', [d['code'] for d in out['diagnostics']])

    def test_G_two_crossings_selected_by_side(self):
        for side in ('left', 'right'):
            out = self.run_case(side=side)
            m = out['moment_diagram']
            self.assertEqual(len(m['crossings']['crossings']), 2)
            self.assertEqual(len(m['candidates']), 1)
            self.assertIn(side, m['selection_reason'])
            self.assertEqual(m['selected_crossing']['segments'][0]['direction'], 'decreasing' if side == 'right' else 'increasing')

    def test_H_ambiguous_crossings_all_retained(self):
        out = self.run_case(points=[(0, 0), (1, 100), (2, 0), (3, 60), (6, 0)])
        self.assertEqual(len(out['moment_diagram']['candidates']), 2)
        self.assertIn('ambiguous_crossing', [d['code'] for d in out['diagnostics']])
        self.assertIsNone(out['overall']['scaling_passes'])

    def test_I_peak_plateau(self):
        out = self.run_case(points=[(0, 0), (1, 100), (2, 100), (6, 0)])
        self.assertIn('positive_peak_plateau', [d['code'] for d in out['diagnostics']])
        self.assertIsNone(out['condition_B']['reference_x_m'])
        self.assertIsNone(out['overall']['scaling_passes'])

    def test_J_remaining_insufficient_entire_branch(self):
        out = self.run_case(points=[(0, 50), (1, 100), (6, 50)])
        self.assertIn('remaining_insufficient_entire_branch', [d['code'] for d in out['diagnostics']])

    def test_K_remaining_sufficient_entire_branch(self):
        out = self.run_case(points=[(0, 0), (1, 10), (6, 0)])
        self.assertIn('remaining_sufficient_entire_branch', [d['code'] for d in out['diagnostics']])
        self.assertIsNone(out['overall']['scaling_passes'])

    def test_L_shear_positive_governs(self):
        out = shear((40, -30))
        self.assertEqual(out['Vk_used_kn'], 40)
        self.assertEqual(out['governing'][0]['Vk_signed_kn'], 40)

    def test_M_shear_negative_governs(self):
        out = shear((20, -30))
        self.assertEqual(out['Vk_used_kn'], 30)
        self.assertEqual(out['governing'][0]['Vk_signed_kn'], -30)

    def test_N_shear_all_ties(self):
        out = shear((30, -30, 30))
        self.assertEqual([p['section'] for p in out['governing']], [1, 2, 3])
        self.assertEqual(out['samples_considered'], 3)

    def test_O_good_bond_geometric(self):
        self.assertTrue(classify_bond(50, 3.5)['boa_aderencia'])
        self.assertEqual(self.run_case()['bond_condition']['bar_center_from_bottom_cm'], 3.5)

    def test_P_poor_bond(self):
        self.assertFalse(classify_bond(50, 31)['boa_aderencia'])
        self.assertFalse(classify_bond(72, 43)['boa_aderencia'])

    def test_Q_bond_boundary_inclusive(self):
        for h, y in ((50, 30), (60, 30), (72, 42)):
            self.assertTrue(classify_bond(h, y)['boa_aderencia'])
            self.assertFalse(classify_bond(h, y+.00001)['boa_aderencia'])

    def test_R_unresolved_d_preserves_independent_results(self):
        args, options = self.setup_case()
        def unresolved_before(*a, **k):
            if sum(c.numero_barras for c in a[3]) == 4:
                raise ValueError('Before centroid unavailable')
            return api.verificar_flexao_viga_retangular(*a, **k)
        args[-1] = altered_api('verificar_flexao_viga_retangular', unresolved_before)
        out = check_scaling_event(*args, **options)
        self.assertEqual([d['code'] for d in out['diagnostics']], ['d_for_al_unresolved'])
        self.assertIsNotNone(out['remaining_capacity'])
        self.assertIsNotNone(out['condition_A']['available_length_cm'])
        self.assertGreater(out['condition_B']['lb_cm'], 25)
        self.assertIsNone(out['condition_A']['passes'])
        self.assertIsNone(out['condition_B']['passes'])
        self.assertIsNone(out['overall']['scaling_passes'])

    def test_S_concretopy_invalid_assumptions(self):
        args, options = self.setup_case()
        def reject(*a, **k):
            return replace(api.verificar_flexao_viga_retangular(*a, **k), hipoteses_validas=False, mrd_kncm=None, mk_equivalente_kncm=None)
        args[-1] = altered_api('verificar_flexao_viga_retangular', reject)
        out = check_scaling_event(*args, **options)
        self.assertIn('concretopy_capacity_rejected', [d['code'] for d in out['diagnostics']])
        self.assertIsNotNone(out['concretopy']['anchorage_result'])
        self.assertIsNone(out['overall']['scaling_passes'])

    def test_T_inconsistent_geometric_interval(self):
        args, options = self.setup_case()
        args[0]['reinforcement'][0]['x_start_common'] = 5
        out = check_scaling_event(*args, **options)
        self.assertEqual(out['diagnostics'][0]['code'], 'inconsistent_geometric_interval')
        self.assertIsNone(out['overall']['scaling_passes'])

    def test_negative_available_length_blocks(self):
        out = self.run_case(end=2)
        self.assertLess(out['condition_A']['available_length_cm'], 0)
        self.assertIsNone(out['overall']['scaling_passes'])
        self.assertIn('negative_available_length', [d['code'] for d in out['diagnostics']])

    def test_scope_rejections(self):
        for key, value in (('horizontal', False), ('hooks', True), ('welds', True),
                           ('sliding_formwork', True), ('special_longitudinal_compression', True),
                           ('vertical_stirrups', False), ('flexure', 'negative')):
            with self.subTest(key=key):
                args, options = self.setup_case()
                options['scope'][key] = value
                out = check_scaling_event(*args, **options)
                self.assertIsNone(out['overall']['scaling_passes'])
                self.assertEqual(out['diagnostics'][0]['code'], 'unsupported_or_unresolved_scope')

    def test_multiple_simultaneous_cuts(self):
        args, options = self.setup_case()
        b = bar('CUT2', .1, 4.5, diameter=10)
        b['shape'] = 'straight'
        args[0]['reinforcement'].append(b)
        args[1]['regions'] = decompose_regions(args[0]['reinforcement'], [0, 6], [transverse(0, 6)])
        out = check_scaling_event(*args, **options)
        self.assertEqual(out['termination_event']['other_coincident_marks'],['CUT2'])
        self.assertEqual(out['remaining_composition']['marks'],['KEEP'])

    def test_invalid_before_centroid_blocks_al(self):
        for invalid in (float('nan'), -1, True, 100):
            args, options = self.setup_case()
            def invalid_centroid(*a, **k):
                result = api.verificar_flexao_viga_retangular(*a, **k)
                return replace(result, d_equivalente_cm=invalid) if sum(c.numero_barras for c in a[3]) == 4 else result
            args[-1] = altered_api('verificar_flexao_viga_retangular', invalid_centroid)
            out = check_scaling_event(*args, **options)
            self.assertIsNone(out['overall']['scaling_passes'])
            self.assertIn('d_for_al_unresolved', [d['code'] for d in out['diagnostics']])
            self.assertIsNone(out['concretopy']['al_result'])

    def test_multilayer_before_centroid_not_isolated_cut_or_remaining(self):
        for side in ('left', 'right'):
            args, options = self.setup_case(side=side)
            bars = args[0]['reinforcement']
            bars[0].update(diameter_mm=16, layers=[0, 2])
            args[1]['regions'] = decompose_regions(bars, [0, 6], [transverse(0, 6)])
            out = check_scaling_event(*args, **options)
            selection = out['d_for_al']
            self.assertEqual(selection['rule'], DEPTH_RULE)
            self.assertEqual(selection['composition_marks'], ['CUT', 'KEEP'])
            contributions = selection['contributions']
            expected = sum(c['As_cm2']*c['d_cm'] for c in contributions)/sum(c['As_cm2'] for c in contributions)
            self.assertAlmostEqual(selection['d_cm'], expected)
            self.assertGreater(selection['d_cm'], min(c['d_cm'] for c in contributions))
            self.assertLess(selection['d_cm'], max(c['d_cm'] for c in contributions))
            self.assertNotEqual(selection['d_cm'], out['remaining_capacity']['concretopy_result']['d_equivalente_cm'])
            self.assertEqual(out['concretopy']['al_call']['d_cm'], selection['d_cm'])
            self.assertEqual(out['condition_A']['al_cm'], out['condition_B']['al_cm'])

    def test_cached_before_flexure_reused_for_centroid_and_geometry(self):
        args, options = self.setup_case()
        before = next(r for r in args[1]['regions'] if r['kind'] == 'interval' and r['x_end_m'] == 4.5)
        response = api.verificar_flexao_viga_retangular(api.SecaoRetangular(19,72,2.5,5), api.Concreto(40), api.Aco(500),
            [api.CamadaArmaduraLongitudinal(4,api.Barra(10))], gamma_f=1.4)
        from dataclasses import asdict
        before.update(status='checked', concretopy_result=asdict(response))
        def no_repeat(*a, **k):
            if sum(c.numero_barras for c in a[3]) == 4:
                raise AssertionError('Before resistance recomputed despite cached result')
            return api.verificar_flexao_viga_retangular(*a, **k)
        args[-1] = altered_api('verificar_flexao_viga_retangular', no_repeat)
        def no_layer_recompute(*a, **k):
            raise AssertionError('Physical layers recomputed despite cached result')
        args[-1].calcular_alturas_uteis_camadas = wraps(api.calcular_alturas_uteis_camadas)(no_layer_recompute)
        out = check_scaling_event(*args, **options)
        self.assert_conditions(out, True, True)
        self.assertEqual(out['before_flexure']['provenance']['method'], 'reuse_before_region_flexure')
        self.assertEqual(out['physical_layer_positions']['provenance']['method'], 'reuse_validated_before_flexure_layers')

    def test_al_and_lb_rejections_independent(self):
        for name, code in (('calcular_al', 'concretopy_al_rejected'), ('calcular_ancoragem', 'concretopy_anchorage_rejected')):
            args, options = self.setup_case()
            def reject(*a, **k):
                raise ValueError('synthetic refusal')
            args[-1] = altered_api(name, reject)
            out = check_scaling_event(*args, **options)
            self.assertIn(code, [d['code'] for d in out['diagnostics']])
            self.assertIsNone(out['overall']['scaling_passes'])

    def test_lb_basic_not_lb_nec(self):
        args, options = self.setup_case(end=1.88, points=[(0, 0), (1, 100), (1.1, 10), (6, -10)])
        def reduced(*a, **k):
            return replace(api.calcular_ancoragem(*a, **k), lb_nec_cm=1, atende=True)
        args[-1] = altered_api('calcular_ancoragem', reduced)
        out = check_scaling_event(*args, **options)
        self.assertFalse(out['condition_B']['passes'])
        self.assertGreater(out['condition_B']['lb_cm'], 25)

    def test_ten_phi_uses_interrupted_diameter(self):
        args, options = self.setup_case()
        bars = args[0]['reinforcement']
        bars[0].update(diameter_mm=16, layers=[0, 2])
        args[1]['regions'] = decompose_regions(bars, [0, 6], [transverse(0, 6)])
        out = check_scaling_event(*args, **options)
        self.assertEqual(out['condition_A']['ten_phi_cm'], 16)
        self.assertEqual(out['composition_after']['bars'][0]['diameter_mm'], 10)
        self.assertEqual(out['concretopy']['anchorage_call']['bitola_mm'], 16)

    def test_diagram_gap_and_distinct_equal_maxima(self):
        for points, code in (([(0, 0), (1, 100), (2, None), (6, 0)], 'incomplete_moment_diagram'),
                             ([(0, 0), (1, 100), (2, 20), (3, 100), (6, 0)], 'multiple_positive_peaks')):
            out = self.run_case(points=points)
            self.assertIn(code, [d['code'] for d in out['diagnostics']])
            self.assertIsNone(out['overall']['scaling_passes'])

    def test_coincident_crossing_is_ambiguous(self):
        out = locate_references(diagram([(0, 0), (1, 100), (2, 30), (3, 30), (6, 0)]), 30, 'right', 4)
        self.assertIn('ambiguous_crossing', out['diagnostics'])
        self.assertIsNone(out['selected_x_nec_m'])

    def test_shear_missing_invalid_outside(self):
        for values in ((20, None), (True, 30), (float('inf'), 30)):
            with self.assertRaises(ValueError):
                shear(values)
        with self.assertRaises(ValueError):
            shear(tuple(range(8)))

    def test_outside_sampled_domain_blocks(self):
        out = self.run_case(points=[(0, 0), (1, 100), (4, 0)])
        self.assertIn('event_outside_sampled_moment_domain', [d['code'] for d in out['diagnostics']])
        self.assertIsNone(out['overall']['scaling_passes'])

    def test_bar_shape_and_support_cuts_blocked(self):
        args, options = self.setup_case()
        args[0]['reinforcement'][1]['shape'] = 'hook'
        out = check_scaling_event(*args, **options)
        self.assertIn('unsupported_bar_shape_or_bend', [d['code'] for d in out['diagnostics']])
        args, options = self.setup_case()
        args[0]['supports']['right']['inner_face_x'] = 4
        out = check_scaling_event(*args, **options)
        self.assertIn('cut_outside_clear_span_support_checks_not_supported', [d['code'] for d in out['diagnostics']])

    def test_endpoint_peak_outgoing_branch_only(self):
        for points, side, event, expected in (([(0,100),(3,0)],'right',2,True),
                                              ([(0,0),(3,100)],'left',1,True),
                                              ([(0,0),(3,100)],'right',2,False)):
            out = locate_references(diagram(points),30,side,event)
            self.assertEqual(out['selected_x_nec_m'] is not None, expected)
            if expected:
                self.assertEqual(out['diagnostics'], [])
            else:
                self.assertIn('event_branch_not_identifiable',out['diagnostics'])

    def test_remaining_external_bend_does_not_credit_anchorage(self):
        args, options = self.setup_case()
        keep=args[0]['reinforcement'][1]
        keep.update(shape='bent',x_start_common=-.1,horizontal_length_cm=600,
                    end_bend={'side':'left','direction':'up','length_cm':35})
        args[1]['regions']=decompose_regions(args[0]['reinforcement'],[0,6],[transverse(0,6)])
        out=check_scaling_event(*args,**options)
        self.assert_conditions(out,True,True)
        self.assertEqual(out['external_bends_not_checked'][0]['mark'],'KEEP')
        for change in ({'horizontal_length_cm':635},
                       {'end_bend':{'side':'right','direction':'up','length_cm':35}},
                       {'end_bend':{'side':'left','direction':'up','length_cm':None}}):
            bad=copy.deepcopy(args[:4])+[api]
            bad[0]['reinforcement'][1].update(change)
            blocked=check_scaling_event(*bad,**options)
            self.assertIsNone(blocked['overall']['scaling_passes'])

    def test_missing_shear_still_checks_lb(self):
        args, options = self.setup_case()
        args[3] = {'status': 'unresolved', 'diagnostic': 'missing'}
        out = check_scaling_event(*args, **options)
        self.assertIsNotNone(out['condition_B']['lb_cm'])
        self.assertIsNone(out['concretopy']['al_result'])
        self.assertIsNone(out['overall']['scaling_passes'])

    def test_changing_geometry_between_peak_and_cut_blocks(self):
        args, options = self.setup_case()
        args[1]['regions'] = decompose_regions(args[0]['reinforcement'], [0, 6],
                                              [transverse(0, 2, height=70), transverse(2, 6)])
        out = check_scaling_event(*args, **options)
        self.assertIn('changing_configuration_between_references_and_cut', [d['code'] for d in out['diagnostics']])
        self.assertIsNone(out['overall']['scaling_passes'])

    def test_inputs_immutable_and_json_finite(self):
        args, options = self.setup_case()
        snapshot = copy.deepcopy(args[:2])
        out = check_scaling_event(*args, **options)
        self.assertEqual(args[:2], snapshot)
        json.dumps(out, allow_nan=False)
        self.assertTrue(out['remaining_capacity']['provenance']['interface']['sha256'])


class RealGoldenTests(unittest.TestCase):
    def setUp(self):
        self.data = [json.loads((ROOT/'analises/pranchas'/n).read_text(encoding='utf8')) for n in NAMES]

    def test_V1001_golden(self):
        out = analyze(self.data, api)
        self.assertEqual(out['event_x_m'], 6.68)
        self.assertEqual(out['composition_before']['marks'], ['N3', 'N5'])
        self.assertEqual(out['composition_after']['marks'], ['N5'])
        old = json.loads((ROOT/'analises/pranchas/V1001_moment_linear_interpolation.json').read_text(encoding='utf8'))
        self.assertEqual(out['remaining_capacity']['Mk_equivalent_knm'], old['remaining_reinforcement_capacity']['Mk_equivalent_knm'])
        self.assertEqual(out['moment_diagram']['crossings'], old['capacity_crossings'])
        self.assertAlmostEqual(out['moment_diagram']['selected_x_nec_m'], 5.709168751478622)
        self.assertEqual(out['moment_diagram']['peak']['section'], 6)
        self.assertEqual(out['shear_for_al']['Vk_used_kn'], 113.39429395)
        self.assertEqual(out['shear_for_al']['governing'][0]['section'], 13)
        self.assertEqual(out['shear_for_al']['governing'][0]['Vk_signed_kn'], -113.39429395)
        self.assertEqual(out['bond_condition']['bar_center_from_bottom_cm'], 3.5)
        self.assertEqual(out['bond_condition']['classification'], 'good')
        self.assertAlmostEqual(out['condition_B']['lb_cm'], 27.5358445519597)
        self.assertEqual(out['condition_A']['ten_phi_cm'], 10)
        self.assertAlmostEqual(out['condition_A']['available_length_cm'], 97.0831248521378)
        self.assertAlmostEqual(out['condition_B']['available_length_cm'], 314.93333333333334)
        self.assertEqual(out['diagnostics'], [])
        self.assertEqual(out['d_for_al']['rule'], DEPTH_RULE)
        self.assertEqual(out['d_for_al']['composition_marks'], ['N3', 'N5'])
        self.assertEqual(out['d_for_al']['d_cm'], 68.5)
        self.assertEqual(out['before_flexure']['provenance']['method'], 'reuse_before_region_flexure')
        self.assertEqual(out['concretopy']['al_result']['al_cm'], 68.5)
        self.assertEqual(out['condition_A']['required_length_cm'], 78.5)
        self.assertAlmostEqual(out['condition_B']['required_length_cm'], 96.0358445519597)
        self.assertTrue(out['condition_A']['passes'])
        self.assertTrue(out['condition_B']['passes'])
        self.assertTrue(out['overall']['complete'])
        self.assertTrue(out['overall']['scaling_passes'])

    def test_shared_provenance_pointers_resolve(self):
        out = analyze(self.data, api)
        def visit(node):
            if isinstance(node, dict):
                if 'shared_pointer' in node:
                    target = out
                    for part in node['shared_pointer'].strip('/').split('/'):
                        target = target[int(part)] if isinstance(target, list) else target[part]
                    self.assertIsNotNone(target)
                for v in node.values():
                    visit(v)
            elif isinstance(node, list):
                for v in node:
                    visit(v)
        visit(out)

    def test_V1001_no_hardcoded_names(self):
        for doc in (self.data[0]['longitudinal_reinforcement'], self.data[3]['reinforcement']):
            for b in doc:
                b['mark'] = {'N3': 'INTERRUPTED', 'N5': 'REMAINING'}.get(b['mark'], b['mark'])
        out = check_bar_scaling(*self.data, api, interrupted_mark='INTERRUPTED', cut_side='right', scope=SCOPE)
        self.assertEqual(out['composition_after']['marks'], ['REMAINING'])
        self.assertAlmostEqual(out['moment_diagram']['selected_x_nec_m'], 5.709168751478622)

    def test_shear_audits_raw(self):
        self.data[3]['force_series'][2]['values'][0] += 1
        self.data[2]['beam']['spans'][0]['internal_forces'][2]['values'][0] += 1
        with self.assertRaisesRegex(ValueError, 'shear_raw_values_mismatch'):
            shear_from_tqs(self.data[3], self.data[1], self.data[2], self.data[4])

    def test_missing_envelope_blocks_only_al(self):
        self.data[3]['force_series'].pop(3)
        self.data[2]['beam']['spans'][0]['internal_forces'].pop(3)
        out = analyze(self.data, api)
        self.assertIsNotNone(out['condition_B']['lb_cm'])
        self.assertIsNotNone(out['moment_diagram']['selected_x_nec_m'])
        self.assertIn('shear_for_al_unresolved', [d['code'] for d in out['diagnostics']])


if __name__ == '__main__':
    unittest.main()
