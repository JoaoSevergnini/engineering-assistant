import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from floor_review import review_floor, review_beam, STAGES
from form_geometry import apply_form, interpret_observation
from common_axis_registration import register_span
from layer_interpretation import interpret_layers, local_layer_fit
from input_preflight import preflight, EXTERNAL_DEPENDENCIES
from stage1_test_fixtures import model, proved
from input_evidence import fact
from test_longitudinal_negative import api, context


def form(m):
    segments = []
    for s in m['physical_geometry']['segments']:
        fields = {k: dict(documentary_state='PROVED', fact=v) for k,v in s['geometry'].items()
                  if k not in ('cover_cm','stirrup_diameter_mm') and v['state']=='DOCUMENTED_CONFIRMED'}
        fields.update({k: dict(documentary_state='PROVED', fact=s[k]) for k in ('x_start_m','x_end_m')})
        segments.append(dict(id=s['id'], geometry_type=s['geometry_type'], fields=fields))
    return dict(coordinate_system=m['physical_geometry']['coordinate_system'], provenance=[dict(fixture='SYNTHETIC_FORM')], segments=segments)


def span(sid=1, start=0, end=4):
    return dict(id=sid, internal_forces=[dict(quantity='bending_moment', envelope=e, unit='kN.m', stage='model_input',
        positions=[start,(start+end)/2,end], values=[0,v,0], sources=['synthetic.lst']) for e,v in (('max',20),('min',-20))])


def registration(m, sid=1, local=(0,4), common=(0,4)):
    return dict(span_id=sid, coordinate_system=m['physical_geometry']['coordinate_system'],
                anchors=[dict(local_m=proved(l,'m'), common_m=proved(c,'m')) for l,c in zip(local,common)])


class FormTests(unittest.TestCase):
    def test_absence_requires_actual_region_examination(self):
        with self.assertRaises(ValueError): interpret_observation(dict(documentary_state='ABSENT_IN_DRAWING'))
        value, note = interpret_observation(dict(documentary_state='ABSENT_IN_DRAWING', review=dict(
            relevant_region_examined=True, provenance=[dict(page=1,bbox=[0,0,10,10])], scope='transition G1/G2')))
        self.assertEqual(value['state'],'MISSING')
        self.assertEqual(note['documentary_state'],'ABSENT_IN_DRAWING')
    def test_not_extracted_is_distinct_from_not_examined(self):
        self.assertNotEqual(interpret_observation({})[1]['documentary_state'],
            interpret_observation(dict(documentary_state='PRESENT_NOT_EXTRACTED'))[1]['documentary_state'])
    def test_unlocated_transition_blocks_local_flexure(self):
        m=model();f=form(m);f['segments'][0]['fields'].pop('x_end_m')
        out=apply_form(m,f)
        plan=preflight(out,region_id='R',interval_m=[0,2],control='positive_flexure')
        self.assertIn('unique_constant_physical_segment',plan['pending'])
        self.assertEqual(out['form_interpretation']['fields'][1]['documentary_state'],'NOT_EXAMINED')
    def test_lst_conflict_retained(self):
        m=model();f=form(m);f['segments'][0]['comparisons']={'height_cm':[proved(60,'cm')]}
        out=apply_form(m,f)
        self.assertEqual(out['physical_geometry']['segments'][0]['geometry']['height_cm']['state'],'CONFLICTING')
    def test_form_missing_does_not_reuse_old_height_as_proof(self):
        m=model();f=form(m);f['segments'][0]['fields'].pop('height_cm')
        self.assertEqual(apply_form(m,f)['physical_geometry']['segments'][0]['geometry']['height_cm']['state'],'MISSING')
    def test_other_segment_remains_runnable_after_missing_transition(self):
        m=model();other=copy.deepcopy(m['physical_geometry']['segments'][0]);other.update(id='G2',x_start_m=proved(4,'m'),x_end_m=proved(8,'m'))
        m['physical_geometry']['segments'].append(other);f=form(m)
        f['segments'][1]['fields'].pop('x_end_m')
        p=preflight(apply_form(m,f),region_id='R',interval_m=[0,3],control='shear',
            inputs={k:proved(True) for k in EXTERNAL_DEPENDENCIES['shear']})
        self.assertEqual(p['readiness'],'RUNNABLE')
    def test_coordinate_mismatch_rejected(self):
        m=model();f=form(m);f['coordinate_system']={}
        with self.assertRaises(ValueError):apply_form(m,f)
    def test_proved_complete_form_inventory_replaces_unlocated_legacy_segments(self):
        m=model();old=copy.deepcopy(m['physical_geometry']['segments'][0]);old.update(id='OLD',x_start_m=fact(unit='m'),x_end_m=fact(unit='m'))
        m['physical_geometry']['segments'].append(old);f=form(model());f['segment_inventory_complete']=proved(True)
        out=apply_form(m,f)
        self.assertEqual([s['id'] for s in out['physical_geometry']['segments']],['G1'])
        f['segment_inventory_complete']=proved(False)
        self.assertEqual(len(apply_form(m,f)['physical_geometry']['segments']),2)


class LayerTests(unittest.TestCase):
    def test_multiple_layers_text(self):
        m=model();m['physical_geometry']['occurrences'][0]['quantity']=proved(4)
        out=interpret_layers(m,{'O1':dict(near_bar_text=proved([2,2]))})
        self.assertEqual(out['physical_geometry']['occurrences'][0]['layers']['value'],[2,2])
        self.assertTrue(local_layer_fit(out,[0,4],'positive_flexure',api)['fits'])
    def test_no_layer_annotation_uses_explicit_convention(self):
        out=interpret_layers(model(),{'O1':dict(explicit_indication_absent=True,review_provenance=[dict(fixture='annotation examined')])})
        self.assertEqual(out['physical_geometry']['occurrences'][0]['layers']['state'],'INFERRED_EXPLICIT_CONVENTION')
        self.assertTrue(local_layer_fit(out,[0,4],'positive_flexure',api)['fits'])
    def test_no_extraction_does_not_claim_no_indication(self):
        self.assertEqual(interpret_layers(model(),{})['physical_geometry']['occurrences'][0]['layers']['state'],'MISSING')
    def test_text_section_conflict(self):
        out=interpret_layers(model(),{'O1':dict(near_bar_text=proved([2]),section=proved([1,1]))})
        self.assertEqual(out['physical_geometry']['occurrences'][0]['layers']['state'],'CONFLICTING')
        self.assertIsNone(local_layer_fit(out,[0,4],'positive_flexure',api)['fits'])
    def test_impossible_convention_not_redistributed(self):
        m=model();m['physical_geometry']['occurrences'][0]['quantity']=proved(8)
        out=interpret_layers(m,{'O1':dict(explicit_indication_absent=True,review_provenance=[dict(fixture='examined')])})
        self.assertFalse(local_layer_fit(out,[0,4],'positive_flexure',api)['fits'])
        self.assertEqual(out['physical_geometry']['occurrences'][0]['layers']['value'],[8])
    def test_combined_marks_fit_checked_together(self):
        m=model();m['physical_geometry']['occurrences'][0]['quantity']=proved(3)
        bar=copy.deepcopy(m['physical_geometry']['occurrences'][0]);bar.update(mark='N2',occurrence_id='O2')
        m['physical_geometry']['occurrences'].append(bar)
        out=interpret_layers(m,{k:dict(near_bar_text=proved([3])) for k in ('O1','O2')})
        self.assertFalse(local_layer_fit(out,[0,4],'positive_flexure',api)['fits'])
    def test_fit_false_blocks_preflight(self):
        m=interpret_layers(model(),{'O1':dict(near_bar_text=proved([2]))})
        inputs={k:proved(True) for k in EXTERNAL_DEPENDENCIES['positive_flexure']+('physical_inventory_complete',)}
        inputs['layer_fit']=proved(False)
        self.assertIn('layer_fit',preflight(m,region_id='R',interval_m=[0,4],control='positive_flexure',inputs=inputs)['pending'])
    def test_fit_requires_partition_at_bar_end(self):
        m=model();m['physical_geometry']['occurrences'][0]['x_end_m']=proved(2,'m')
        self.assertIsNone(local_layer_fit(m,[0,4],'positive_flexure',api)['fits'])
    def test_anchorage_using_resistant_layers_requires_fit_and_inventory(self):
        m=interpret_layers(model(),{'O1':dict(near_bar_text=proved([2]))})
        inputs={k:proved(True) for k in EXTERNAL_DEPENDENCIES['anchorage']}
        plan=preflight(m,region_id='N',interval_m=[0,4],control='anchorage',inputs=inputs,uses_layers_for_resistance=True)
        self.assertIn('layer_fit',plan['pending']);self.assertIn('physical_inventory_complete',plan['pending'])
        inputs.update(layer_fit=proved(True),layer_order=proved(True),physical_inventory_complete=proved(True))
        self.assertEqual(preflight(m,region_id='N',interval_m=[0,4],control='anchorage',inputs=inputs,
            uses_layers_for_resistance=True)['readiness'],'RUNNABLE')


class AxisTests(unittest.TestCase):
    def test_multiple_spans_and_cantilever_preserve_forces(self):
        m=model()
        for sid,common in ((1,(-2,0)),(2,(0,2)),(3,(2,4))):
            original=span(sid,0,2);r=register_span(original,registration(m,sid,local=(0,2),common=common),m['physical_geometry']['coordinate_system'])
            self.assertEqual(r['internal_forces'][0]['positions'],[common[0],sum(common)/2,common[1]])
            self.assertEqual(r['internal_forces'][1]['values'],original['internal_forces'][1]['values'])
            self.assertEqual(original['internal_forces'][0]['positions'],[0,1,2])
    def test_scale_or_orientation_not_presumed(self):
        m=model()
        for common in ((0,8),(4,0)):
            with self.assertRaises(ValueError):register_span(span(),registration(m,common=common),m['physical_geometry']['coordinate_system'])
    def test_unproved_anchor_blocks(self):
        m=model();r=registration(m);r['anchors'][1]['common_m']=fact(unit='m')
        with self.assertRaises(ValueError):register_span(span(),r,m['physical_geometry']['coordinate_system'])


class FloorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        path=Path(self.tmp.name)/'extraction.json';path.write_text(json.dumps(dict(source_sha256='synthetic-original',provenance=[dict(fixture='SYNTHETIC_ARCHIVE')],observations=[],coverage=[])))
        source=dict(extraction_archive=str(path),archive_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        m=model();self.case=dict(beam_id='SYNTHETIC',model=m,form=form(m),review_interval_m=[0,4],
            layer_observations={'O1':dict(near_bar_text=proved([2]))},positioned_tqs=dict(beam=dict(spans=[span()])),
            registrations={'1':registration(m)},jobs=[dict(id='R',control='positive_flexure',span_id=1,interval_m=[0,4],
                context=context(),inputs={k:proved(True) for k in EXTERNAL_DEPENDENCIES['positive_flexure']+('physical_inventory_complete',)})])
        self.spec=dict(floor='SYNTHETIC',beams=[self.case],sources={k:source for k in ('form','detailing','tqs')})
    def run_case(self,**kwargs):return review_floor(self.spec,**kwargs)['beams'][0]
    def test_real_engine_runs_after_guard(self):
        out=self.run_case(api=api)
        result=out['controls'][0]
        self.assertEqual(result['input_validation']['readiness'],'RUNNABLE')
        self.assertEqual(result['status'],'PASS')
        self.assertTrue(result['result']['regions'])
        self.assertEqual(out['stages'],list(STAGES))

    def section_case(self, bounds=(0,2,4), heights=(57,47)):
        m=self.case['model'];base=copy.deepcopy(m['physical_geometry']['segments'][0]);segments=[]
        for i,(a,z,h) in enumerate(zip(bounds,bounds[1:],heights)):
            s=copy.deepcopy(base);s.update(id='G'+str(i+1),x_start_m=proved(a,'m'),x_end_m=proved(z,'m'));s['geometry']['height_cm']=proved(h,'cm');segments.append(s)
        m['physical_geometry']['segments']=segments
        negative=copy.deepcopy(m['physical_geometry']['occurrences'][0]);negative.update(mark='N2',occurrence_id='O2',function='negative',face='upper')
        m['physical_geometry']['occurrences'].append(negative)
        self.case['layer_observations']['O2']=dict(section=proved([2]))
        self.case['form']=form(m);self.case['jobs']=[];self.case['context']=context()
        self.case['context'].update(stirrup_angle_degrees=90,axial_force_kn=0,al_scope_provenance={'fixture':'vertical stirrups, Vc=Vc0, no normal force'})
        self.case['control_inputs']={c:{k:proved(True) for k in EXTERNAL_DEPENDENCIES[c]+('physical_inventory_complete',)} for c in ('positive_flexure','negative_flexure','shear','suspension')}
        xs=[0,1,2,2.1,3,4];series=[]
        for quantity,unit,env,values in (('bending_moment','kN.m','max',[0,10,20,40,25,0]),('bending_moment','kN.m','min',[0,-30,-10,-5,-25,0]),('shear','kN','max',[10,20,30,200,50,20]),('shear','kN','min',[-5,-10,-20,-100,-30,-5])):
            series.append(dict(quantity=quantity,unit=unit,envelope=env,stage='model_input',positions=xs,sections=list(range(1,7)),values=values,sources=['synthetic-reviewed-TQS']))
        self.case['positioned_tqs']['beam']['spans'][0]['internal_forces']=series
        self.case['section_checks']=dict(domains=[dict(span_id=1,interval_m=proved([0,4],'m'))],
            drawn_stirrup_regions=[dict(id='E',interval_m=[0,4],diameter_mm=6.3,spacing_cm=12,legs=2,
                physical_function='CONVENTIONAL_SHEAR_STIRRUP',source={'fixture':'documented closed stirrup throughout synthetic beam'})])
        return self.case
    def test_two_sections_physical_shear_before_moment_expansion(self):
        self.section_case();out=self.run_case(api=api)['section_checks'];a,b=out['sections']
        self.assertEqual(a['shear_selection']['Vsk_abs_kn'],30);self.assertEqual(b['shear_selection']['Vsk_abs_kn'],200)
        self.assertEqual(a['shear_selection']['governing'][0]['x_m'],2)
        self.assertEqual(a['al']['result']['parameters']['vk_abs_kn'],30)
        self.assertNotEqual(a['al']['result']['parameters']['al_cm'],b['al']['result']['parameters']['al_cm'])
        self.assertEqual(a['expanded_moment_extrema']['positive_flexure']['positive']['x_m'],2.1)
        self.assertEqual(a['expanded_moment_extrema']['negative_flexure']['negative']['x_m'],1)
        self.assertGreater(a['moment_search_interval_m'][1],2.1)
        self.assertEqual(a['expanded_flexure'][0]['result']['regions'][0]['concretopy']['parametros']['h_cm'],57)
        self.assertEqual(a['shear_checks'][0]['result']['demand']['Vsk_abs_kn'],30)
        self.assertEqual(a['shear_checks'][0]['shear_search_interval_m'],[0,2])
        self.assertIsNone(out['beam_approval']);self.assertIsNone(out['local_discontinuity_approval'])
    def test_three_sections_expand_both_internal_sides_once(self):
        self.section_case((0,1.5,3,4),(57,47,67));sections=self.run_case(api=api)['section_checks']['sections']
        self.assertEqual(len(sections),3)
        self.assertLess(sections[1]['moment_search_interval_m'][0],1.5)
        self.assertGreater(sections[1]['moment_search_interval_m'][1],3)
        self.assertEqual(sections[0]['moment_search_interval_m'][0],0)
        self.assertEqual(sections[-1]['moment_search_interval_m'][1],4)
    def test_bar_interruption_does_not_extend_bar_by_al(self):
        self.section_case();self.case['model']['physical_geometry']['occurrences'][0]['x_end_m']=proved(2.05,'m')
        a=self.run_case(api=api)['section_checks']['sections'][0]
        positive=next(c for c in a['expanded_flexure'] if c['control']=='positive_flexure')
        self.assertEqual(positive['execution_state'],'NOT_EXECUTED')
        self.assertIn('longitudinal_continuity_not_proved_for_expanded_search',positive['input_validation']['pending'])
        self.assertEqual(self.case['model']['physical_geometry']['occurrences'][0]['x_end_m']['value'],2.05)
    def test_shear_discontinuity_blocks_interpolation_and_al(self):
        self.section_case();self.case['section_checks']['domains'][0]['discontinuities_m']=[proved(1.9,'m')]
        a=self.run_case(api=api)['section_checks']['sections'][0]
        self.assertFalse(a['shear_selection']['complete']);self.assertEqual(a['al']['execution_state'],'NOT_EXECUTED')
        self.assertIsNone(a['moment_search_interval_m'])
        self.assertTrue(all(c['execution_state']=='NOT_EXECUTED' for c in a['shear_checks']))
    def test_unknown_transition_preserves_physical_checks_but_no_expansion(self):
        self.section_case((0,1.8,4),(57,47))
        self.case['model']['physical_geometry']['segments'][1]['x_start_m']=proved(2.2,'m');self.case['form']=form(self.case['model'])
        self.case['form']['transitions']=[dict(physical_interval_m=[1.8,2.2],position_state='PRESENT_NOT_EXTRACTED')]
        a=self.run_case(api=api)['section_checks']['sections'][0]
        self.assertEqual(a['al']['status'],'PASS');self.assertIsNone(a['moment_search_interval_m'])
        self.assertIn('transition_position_unproved_for_expanded_search',a['diagnostics'])
        self.assertTrue(a['physical_flexure'])
    def test_missing_geometric_endpoint_is_reported_not_dropped(self):
        self.section_case();self.case['form']['segments'][0]['fields'].pop('x_end_m')
        out=self.run_case(api=api)['section_checks']
        self.assertEqual(out['pending_segments'][0]['segment_id'],'G1')
    def test_transition_suspension_uses_lower_height_and_local_shear_contexts(self):
        from test_suspension_review import connection
        self.section_case()
        for s in self.case['positioned_tqs']['beam']['spans'][0]['internal_forces']:
            if s['quantity']=='shear':s['values']=[30 if s['envelope']=='max' else -20]*6
        c=connection(20);c['receiving_beam_id']=self.case['beam_id'];c['reaction']['receiving_beam_id']=self.case['beam_id']
        self.case['section_checks'].update(suspension_connections=[c],suspension_inventory_source={'fixture':'complete supported beam inventory'})
        out=self.run_case(api=api)['section_checks']['suspension'][0]
        self.assertEqual(out['execution_state'],'EXECUTED_COMPLETE')
        r=out['result']['connections'][0]
        self.assertEqual(r['distribution']['length_cm'],47)
        self.assertEqual(r['distribution']['interval_m'],[1.765,2.235])
        self.assertEqual(r['suspension']['reaction'],c['reaction'])
        self.assertEqual({p['physical_section']['context']['section']['h'] for p in r['subintervals']},{57,47})
        self.assertIsNone(r['local_discontinuity_approval'])
    def test_section_procedure_cannot_be_silently_omitted_for_changed_geometry(self):
        self.section_case();self.case.pop('section_checks')
        out=self.run_case(api=api)['section_checks']
        self.assertEqual(len(out['sections']),2)
        self.assertIn('unique_documented_applicable_domain_required',out['sections'][0]['diagnostics'])
    def test_suspension_existing_detailing_alert_requires_engineering_review(self):
        from test_suspension_review import connection
        self.section_case()
        for s in self.case['positioned_tqs']['beam']['spans'][0]['internal_forces']:
            if s['quantity']=='shear':s['values']=[30 if s['envelope']=='max' else -20]*6
        self.case['section_checks']['drawn_stirrup_regions'][0]['spacing_cm']=6
        c=connection(20);c['receiving_beam_id']=self.case['beam_id'];c['reaction']['receiving_beam_id']=self.case['beam_id']
        self.case['section_checks'].update(suspension_connections=[c],suspension_inventory_source={'fixture':'complete synthetic inventory'})
        out=self.run_case(api=api)['section_checks']['suspension'][0]
        self.assertEqual(out['status'],'REQUIRES_ENGINEERING_REVIEW')
        self.assertTrue(out['result']['connections'][0]['engineering_review_required'])
    def test_section_review_preserves_input_envelopes_and_bar_intervals(self):
        self.section_case();before=copy.deepcopy(self.spec);self.run_case(api=api);self.assertEqual(self.spec,before)
    def test_effective_depth_units_are_not_silently_reinterpreted(self):
        self.section_case();self.case['section_checks']['effective_depths']={'G1':proved(.5,'m')}
        a=self.run_case(api=api)['section_checks']['sections'][0]
        self.assertEqual(a['al']['execution_state'],'NOT_EXECUTED')
        self.assertIn('physical_unit_required:cm',a['diagnostics'])
    def test_al_scope_is_not_assumed_from_material_data(self):
        self.section_case();self.case['context'].pop('al_scope_provenance')
        a=self.run_case(api=api)['section_checks']['sections'][0]
        self.assertEqual(a['al']['execution_state'],'NOT_EXECUTED')
        self.assertIn('al_scope',a['al']['input_validation']['pending'])
    def test_section_domain_requires_common_axis_metre_units(self):
        self.section_case();self.case['section_checks']['domains'][0]['interval_m']['unit']='cm'
        out=self.run_case(api=api)['section_checks']
        self.assertIn('unique_documented_applicable_domain_required',out['sections'][0]['diagnostics'])
    def test_transition_method_separate_from_documentary_position(self):
        self.case['form']['transitions']=[dict(physical_interval_m=[3,4],position_state='ABSENT_IN_DRAWING')]
        out=self.run_case(api=api)
        p=out['controls'][0]['input_validation']
        self.assertIn('transition_resistant_method_not_implemented',p['pending'])
        self.assertEqual(p['limitations'][0]['implementation'],'NOT_IMPLEMENTED')
        self.assertEqual(out['controls'][0]['execution_state'],'NOT_EXECUTED')
        self.case['jobs'][0]['interval_m']=[0,2]
        out=self.run_case(api=api)
        self.assertEqual(out['controls'][0]['status'],'PASS')
        self.assertEqual(out['regional_method_scope'][-1]['position_state'],'ABSENT_IN_DRAWING')
    def test_plotting_failure_suspends_unrelated_resistant_controls(self):
        m=self.case['model']
        m['documentary_reconciliation']['positions'].append(dict(mark='N2',representations=[dict(view='STEEL_SCHEDULE',quantity=4)],
            issues=[dict(code='PLOTTING_INTEGRITY',view='ELEVATION',provenance=[dict(fixture='proved truncated elevation')])]))
        before=copy.deepcopy(m);called=[]
        out=self.run_case(api=api,adapters={'positive_flexure':lambda p:called.append(p)})
        self.assertFalse(called);self.assertTrue(out['documentary_review']['suspended'])
        self.assertIsNone(out['controls'][0]['layer_fit']['fits'])
        self.assertEqual(out['documentary_review']['affected_marks'],['N2'])
        self.assertTrue(all(c['execution_state']=='NOT_EXECUTED' for c in out['controls']))
        self.assertIn('documentary_plotting_failure_beam_review_suspended',out['controls'][0]['input_validation']['pending'])
        self.assertEqual(m,before)
    def test_missing_extraction_alone_does_not_claim_plotting_failure(self):
        self.case['model']['documentary_reconciliation']['positions'].append(dict(mark='N2',issues=[dict(code='REPRESENTATION_NOT_EXTRACTED',view='ELEVATION')]))
        self.assertFalse(self.run_case(api=api)['documentary_review']['suspended'])
    def test_missing_form_never_calls_checker(self):
        self.spec['sources'].pop('form');called=[]
        out=self.run_case(adapters={'positive_flexure':lambda p:called.append(p)},api=api)
        self.assertFalse(called)
        self.assertIn('form_source_unavailable',out['controls'][0]['input_validation']['pending'])
        self.assertEqual(out['diagnosis']['execution_state'],'NOT_EXECUTED')
    def test_fit_failure_never_calls_resistant_checker(self):
        self.case['model']['physical_geometry']['occurrences'][0]['quantity']=proved(8)
        self.case['layer_observations']['O1']=dict(explicit_indication_absent=True,review_provenance=[dict(fixture='examined')])
        called=[];out=self.run_case(adapters={'positive_flexure':lambda p:called.append(p)},api=api)
        self.assertFalse(called);self.assertFalse(out['controls'][0]['layer_fit']['fits'])
    def test_missing_registration_cannot_be_overridden_by_true_input(self):
        self.case['registrations']={}
        called=[];out=self.run_case(adapters={'positive_flexure':lambda p:called.append(p)},api=api)
        self.assertFalse(called);self.assertIn('force_position_mapping',out['controls'][0]['input_validation']['pending'])
    def test_sources_required_even_for_inapplicability(self):
        self.spec['sources'].pop('form')
        self.case['jobs'][0]['applicability']=fact(state='NOT_APPLICABLE',provenance=[dict(fixture='scope')])
        out=self.run_case(api=api)
        self.assertEqual(out['controls'][0]['status'],'INCONCLUSIVE')
    def test_source_hash_tampering_rejected(self):
        self.spec['sources']['form']['archive_sha256']='wrong'
        with self.assertRaises(ValueError):self.run_case(api=api)
    def test_no_jobs_still_runs_preflight_for_every_control(self):
        self.case['jobs']=[];out=self.run_case()
        self.assertEqual(len(out['controls']),6)
        self.assertTrue(all(c['input_validation'] for c in out['controls']))
    def test_does_not_modify_input(self):
        before=copy.deepcopy(self.spec);self.run_case(api=api)
        self.assertEqual(before,self.spec)
    def test_duplicates_cannot_hide_checks(self):
        self.case['jobs'].append(copy.deepcopy(self.case['jobs'][0]))
        with self.assertRaises(ValueError):self.run_case(api=api)
    def test_unrelated_suspension_runs_despite_missing_transition(self):
        self.case['form']['segments'][0]['fields'].pop('x_end_m')
        self.case['jobs']=[dict(id='S',control='suspension',interval_m=[0,4],
            inputs={k:proved(True) for k in EXTERNAL_DEPENDENCIES['suspension']})]
        called=[]
        out=self.run_case(adapters={'suspension':lambda p:(called.append(p) or dict(passes=True))})
        self.assertEqual(len(called),1)
        self.assertEqual(out['controls'][0]['status'],'PASS')
    def test_each_existing_control_adapter_passes_through_preflight(self):
        for control in ('anchorage','shear','scaling','suspension'):
            self.case['jobs']=[dict(id=control,control=control,span_id=1,interval_m=[0,4],
                inputs={k:proved(True) for k in EXTERNAL_DEPENDENCIES[control]+('physical_inventory_complete',)})]
            called=[]
            out=self.run_case(adapters={control:lambda p:(called.append(p) or dict(passes=True))},api=api)
            self.assertEqual(len(called),1,control)
            self.assertEqual(out['controls'][0]['input_validation']['readiness'],'RUNNABLE')
    def test_multiple_spans_and_cantilever_through_floor_pipeline(self):
        m=self.case['model'];g=m['physical_geometry'];g['segments'][0].update(x_start_m=proved(-2,'m'),x_end_m=proved(8,'m'))
        g['occurrences'][0].update(x_start_m=proved(-2,'m'),x_end_m=proved(8,'m'))
        g['spans']=[dict(id=1,tqs_span_token='1B',physical_kind=proved('CANTILEVER'),orientation=proved('LEFT'),
            physical_bounds=dict(x_start_m=proved(-2,'m'),x_end_m=proved(0,'m')))]
        self.case['form']=form(m);self.case['form']['spans']=g['spans']
        self.case['positioned_tqs']['beam']['spans']=[span(1,0,2),span(2,0,4),span(3,0,4)]
        self.case['registrations']={str(i):registration(m,i,local=l,common=c) for i,l,c in
            ((1,(0,2),(-2,0)),(2,(0,4),(0,4)),(3,(0,4),(4,8)))}
        self.case['jobs']=[];self.case['context']=context()
        self.case['review_interval_m']=[-2,8]
        self.case['control_inputs']={'positive_flexure':{k:proved(True) for k in EXTERNAL_DEPENDENCIES['positive_flexure']+('physical_inventory_complete',)}}
        out=self.run_case(api=api)
        self.assertEqual(len(out['registered_spans']),3)
        self.assertEqual(out['model']['physical_geometry']['spans'][0]['physical_validation'],'VALIDATED')
        checks=[c for c in out['controls'] if c['control']=='positive_flexure']
        self.assertEqual(len(checks),3)
        self.assertTrue(all(c['execution_state']=='EXECUTED_COMPLETE' for c in checks))


if __name__=='__main__':unittest.main()
