import unittest
from copy import deepcopy
from input_preflight import preflight, execute, prepare_local_batches, correction_readiness, EXTERNAL_DEPENDENCIES, execute_control
from stage1_test_fixtures import model, proved
from input_evidence import fact
from physical_geometry import apply_end_convention

class PreflightTests(unittest.TestCase):
    def inputs(self,control='positive_flexure'):
        return {k:proved(True) for k in EXTERNAL_DEPENDENCIES[control]+('physical_inventory_complete',)}
    def plan(self,m=None,control='positive_flexure',inputs=None,**kw):
        return preflight(m or model(),region_id='R1',interval_m=[0,4],control=control,inputs=inputs or self.inputs(control),**kw)
    def test_constant_runnable(self):self.assertEqual(self.plan()['readiness'],'RUNNABLE')
    def test_cover_missing_blocks_dependent_control(self):
        m=model();m['physical_geometry']['segments'][0]['geometry']['cover_cm']=fact(unit='cm')
        self.assertEqual(self.plan(m)['readiness'],'PENDING');self.assertEqual(self.plan(m,'suspension')['readiness'],'RUNNABLE')
    def test_force_mapping_required(self):
        i=self.inputs();i.pop('force_position_mapping');self.assertIn('force_position_mapping',self.plan(inputs=i)['pending'])
    def test_inventory_complete_required(self):
        i=self.inputs();i.pop('physical_inventory_complete');self.assertEqual(self.plan(inputs=i)['readiness'],'PENDING')
    def test_unknown_end_not_absence(self):
        m=model();m['physical_geometry']['occurrences'][0]['x_end_m']=fact(unit='m');self.assertEqual(self.plan(m)['readiness'],'PENDING')
    def test_assumption_conditional_optin(self):
        m=model();m['physical_geometry']['occurrences'][0]['layers']=fact([2],state='ENGINEERING_ASSUMPTION',provenance=['synthetic hypothesis'])
        self.assertEqual(self.plan(m)['readiness'],'PENDING');self.assertEqual(self.plan(m,allow_assumptions=True)['readiness'],'RUNNABLE_WITH_ASSUMPTIONS')
    def test_geometry_overlap_conflicting(self):
        m=model();b=deepcopy(m['physical_geometry']['segments'][0]);b['id']='G2';b['geometry']['height_cm']=proved(47,'cm');m['physical_geometry']['segments'].append(b);self.assertEqual(self.plan(m)['readiness'],'PENDING')
    def test_variable_geometry_blocked(self):
        m=model();m['physical_geometry']['segments'][0]['geometry_type']='VARIABLE';self.assertEqual(self.plan(m)['readiness'],'PENDING')
    def test_local_independence(self):
        m=model();bad=deepcopy(m['physical_geometry']['segments'][0]);bad.update(id='G2',x_start_m=proved(4,'m'),x_end_m=proved(8,'m'),geometry_type='VARIABLE');m['physical_geometry']['segments'].append(bad)
        self.assertEqual(self.plan(m)['readiness'],'RUNNABLE')
    def test_blocked_checker_never_called(self):
        p=self.plan(inputs={k:fact() for k in self.inputs()});calls=[]
        r=execute(p,lambda:calls.append(1));self.assertFalse(calls);self.assertEqual(r['execution_state'],'NOT_EXECUTED')
    def test_pass_not_fabricated(self):
        self.assertEqual(execute(self.plan(),lambda:dict(status='FAIL'))['status'],'FAIL')
    def test_legacy_flexure_state(self):self.assertEqual(execute(self.plan(),lambda:dict(passes=True))['status'],'PASS')
    def test_shear_status(self):self.assertEqual(execute(self.plan(control='shear'),lambda:dict(overall_structural_result='FAIL'))['status'],'FAIL')
    def test_all_control_callbacks(self):
        for control in EXTERNAL_DEPENDENCIES:
            m=model()
            if control=='negative_flexure':m['physical_geometry']['occurrences'][0].update(function='negative',face='upper')
            r=execute_control(m,region_id='R1',interval_m=[0,4],control=control,inputs=self.inputs(control),checker=lambda:dict(status='PASS'))
            self.assertEqual(r['execution_state'],'EXECUTED_COMPLETE',control)
    def test_not_applicable_proved(self):
        p=self.plan(applicability=fact(state='NOT_APPLICABLE',provenance=['synthetic no indirect support']));self.assertEqual(p['readiness'],'NOT_APPLICABLE')
    def test_correction_guard(self):
        p=self.plan(inputs={k:fact() for k in self.inputs()});self.assertFalse(correction_readiness([p])['eligible']);self.assertFalse(correction_readiness([self.plan()])['correction_generation_enabled'])
    def test_transition_isolated(self):
        m=model();a=m['physical_geometry']['segments'][0];a['x_end_m']=proved(2,'m');b=deepcopy(a);b.update(id='G2',x_start_m=proved(2,'m'),x_end_m=proved(4,'m'));b['geometry']['height_cm']=proved(47,'cm');m['physical_geometry']['segments'].append(b)
        r=prepare_local_batches(m);self.assertTrue(any(x['kind']=='boundary_point' and x['x_start_m']==2 for x in r['regions']))
    def test_optional_checks_not_required(self):
        p=self.plan(control='anchorage');self.assertEqual(p['readiness'],'RUNNABLE');self.assertFalse(p['scope']['mandatory_pin_check'])
    def test_end_convention_reused(self):
        b=model()['physical_geometry']['occurrences'][0]
        ends={'LEFT':dict(explicit_x_m=0,explicit_dimension_source='synthetic dimension'), 'RIGHT':dict(terminates_in_support=True,support_type='END',support_element='COLUMN',source='synthetic column face',external_face_m=4)}
        r=apply_end_convention(b,ends);self.assertEqual(r['x_end_m']['state'],'INFERRED_EXPLICIT_CONVENTION');self.assertEqual(r['x_start_m']['state'],'DOCUMENTED_CONFIRMED')
    def test_internal_support_pending(self):
        b=model()['physical_geometry']['occurrences'][0];b['x_end_m']=fact(unit='m');r=apply_end_convention(b,{'RIGHT':dict(terminates_in_support=True,support_type='INTERNAL',support_element='COLUMN',source='synthetic')});self.assertEqual(r['x_end_m']['state'],'MISSING')
    def test_diagnostic_preserves_evidence(self):
        from beam_diagnostic import consolidate
        d=consolidate(dict(beam_id='SYNTHETIC',floor='TEST',coordinate_system={'unit':'m'}),[],input_validation=[self.plan()]);self.assertEqual(d['context']['input_validation'][0]['readiness'],'RUNNABLE')

if __name__=='__main__':unittest.main()
