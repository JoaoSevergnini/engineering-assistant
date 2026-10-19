"""Synthetic association evidence; frozen real-sheet regressions are separate."""
import copy
import json
from pathlib import Path
import unittest
from polygonal_slabs import box, geo, LineString
from slab_assignment import partition_domains
from refine_slab_assignment import refine


def domain(id='A',bounds=(0,0,10,10),h=20):
    return {'id':id,'slab':id,'geometry_pdf_pt':geo(box(*bounds)),'thickness_cm':h,'confirmed':False,'review_flag':False,
        'source':{'label':{'text':id,'bbox':[200,200,210,210]},'thickness_text_ids':['h-'+id]}}


def fixture(ds=None):
    ds=ds or [domain()]
    region=box(-2,-2,12,12)
    segments=partition_domains(region,ds)
    for i,s in enumerate(segments):s.update(id='S'+str(i),quantity_reference='occ')
    source={'bar':{'a':[-2,5],'b':[12,5],'source_ids':['bar']},
        'distribution_axis':{'a':[5,-2],'b':[5,12],'source_ids':['axis']}}
    slabs=sorted({s for p in segments for s in p['slabs']})
    item={'occurrence_id':'occ','display_id':'O001','documentary_mark':'N1','representation_kind':'DISTRIBUTED',
        'state':'INDETERMINATE','geometry_sources':[source],'segments':segments,'slabs':slabs,
        'thickness_options_cm':sorted({d['thickness_cm'] for d in ds}),
        'multiple_slabs':len(slabs)>1,'different_thickness_domains':len({d['thickness_cm'] for d in ds})>1}
    return {'domains':ds,'occurrences':[item],'human_confirmations':[]}


class SyntheticRefinementTests(unittest.TestCase):
    def test_external_parts_do_not_downgrade_supported_association(self):
        d=fixture();before=copy.deepcopy(d);o=refine(d)['occurrences'][0]
        self.assertEqual(o['state'],'RELIABLE');self.assertFalse(o['requires_engineer_decision'])
        self.assertEqual(o['contour_confidence'],{'A':'CANDIDATE_NOT_CONFIRMED'})
        self.assertEqual(o['segments'],before['occurrences'][0]['segments'])
        self.assertTrue(o['exterior_segment_ids']);self.assertEqual(d,before)
        self.assertEqual(o['exterior_interpretation'],'UNKNOWN_NOT_AUTOMATICALLY_ANCHORAGE')

    def test_no_containment_area_threshold(self):
        d=fixture();o=d['occurrences'][0]
        o['geometry_sources'][0]['bar'].update(a=[-100,5],b=[100,5])
        self.assertEqual(refine(d)['occurrences'][0]['state'],'RELIABLE')

    def test_overlap_without_bar_or_axis_interior_is_not_enough(self):
        d=fixture();s=d['occurrences'][0]['geometry_sources'][0]
        s['bar'].update(a=[-2,-2],b=[12,-2]);s['distribution_axis'].update(a=[-2,-2],b=[-2,12])
        self.assertEqual(refine(d)['occurrences'][0]['state'],'INDETERMINATE')

    def test_only_one_entity_support_is_probable(self):
        d=fixture();d['occurrences'][0]['geometry_sources'][0]['distribution_axis'].update(a=[-2,-2],b=[-2,12])
        self.assertEqual(refine(d)['occurrences'][0]['state'],'PROBABLE')

    def test_crossing_different_thicknesses_preserves_domains(self):
        d=fixture([domain('A',(0,0,5,10),12),domain('B',(5,0,10,10),20)])
        o=refine(d)['occurrences'][0]
        self.assertEqual(o['slabs'],['A','B']);self.assertTrue(o['different_thickness_domains'])
        self.assertNotEqual(o['state'],'INDETERMINATE');self.assertFalse(o['association_conflicts'])
        self.assertEqual(o['segments'],d['occurrences'][0]['segments'])
        self.assertTrue(all(s['quantity_allocation'] is None for s in o['segments']))

    def test_competing_thicknesses_in_same_part_remain_indeterminate(self):
        o=refine(fixture([domain('A',h=12),domain('B',h=20)]))['occurrences'][0]
        self.assertEqual(o['state'],'INDETERMINATE');self.assertTrue(o['association_conflicts'][0]['different_thicknesses'])

    def test_topology_warning_separate_from_full_confirmation(self):
        d=fixture();d['domains'][0]['review_flag']=True
        self.assertEqual(refine(d)['occurrences'][0]['state'],'PROBABLE')

    def test_documentary_source_required(self):
        d=fixture();d['domains'][0]['source']['thickness_text_ids']=[]
        self.assertEqual(refine(d)['occurrences'][0]['state'],'INDETERMINATE')

    def test_text_distance_not_assignment_rule(self):
        d=fixture();a=refine(d)
        d['domains'][0]['source']['label']['bbox']=[10000,10000,10010,10010]
        self.assertEqual(refine(d)['occurrences'][0]['state'],a['occurrences'][0]['state'])
        d['domains'][0]['geometry_pdf_pt']=geo(box(100,100,110,110))
        d['occurrences'][0]['segments']=partition_domains(box(-2,-2,12,12),d['domains'])
        for i,s in enumerate(d['occurrences'][0]['segments']):s['id']='X'+str(i)
        self.assertEqual(refine(d)['occurrences'][0]['state'],'INDETERMINATE')

    def test_localized_vertical_trace_extends_outside(self):
        d=fixture();o=d['occurrences'][0];g=LineString([(5,-3),(5,13)])
        o.update(representation_kind='LOCALIZED',geometry_sources=[{'physical_group_id':'G1','geometry_pdf_pt':geo(g)}],segments=partition_domains(g,d['domains'],1))
        for i,s in enumerate(o['segments']):s['id']='L'+str(i)
        self.assertEqual(refine(d)['occurrences'][0]['state'],'RELIABLE')

    def test_localized_disconnected_group_not_invented_as_supported(self):
        d=fixture();o=d['occurrences'][0]
        o['representation_kind']='LOCALIZED'
        o['geometry_sources']=[{'physical_group_id':'G1','geometry_pdf_pt':geo(LineString([(5,-2),(5,12)]))},
            {'physical_group_id':'G2','geometry_pdf_pt':geo(LineString([(20,-2),(20,12)]))}]
        self.assertEqual(refine(d)['occurrences'][0]['state'],'PROBABLE')

    def test_order_color_and_determinism(self):
        d=fixture([domain('A',(0,0,5,10)),domain('B',(5,0,10,10))]);a=refine(d)
        d['domains'].reverse()
        for domain_ in d['domains']:domain_['color']='irrelevant'
        self.assertEqual(a['occurrences'],refine(d)['occurrences'])


class RealSheetRefinementRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2]
        cls.old=json.loads((root/'analises/lajes_associacao_espessuras/inventario.json').read_text(encoding='utf8'))
        cls.new=json.loads((root/'analises/lajes_associacao_refinada/inventario.json').read_text(encoding='utf8'))
        cls.before=cls.old['slab_reinforcement_assignment'];cls.after=cls.new['refined_slab_assignment']

    def test_all_previous_layers_and_human_confirmations_unchanged(self):
        for key,value in self.old.items():self.assertEqual(self.new[key],value,key)
        self.assertEqual(self.before['human_confirmations'],self.after['human_confirmations'])
        byid={o['display_id']:o for o in self.after['occurrences']}
        for id in ['O034','O035']:self.assertEqual(byid[id]['structural_interpretation']['active_classification'],'REINFORCEMENT')
        self.assertEqual(byid['O053']['structural_interpretation']['active_classification'],'LAP_SPLICE')

    def test_all_original_geometries_and_exterior_parts_exactly_preserved(self):
        for old,new in zip(self.before['occurrences'],self.after['occurrences']):
            self.assertEqual(old['occurrence_id'],new['occurrence_id'])
            for key in ['segments','geometry_sources','call','slabs','thickness_options_cm']:
                self.assertEqual(old.get(key),new.get(key),(old['display_id'],key))

    def test_59_results_and_pending_cases(self):
        self.assertEqual(self.after['metrics']['states'],{'RELIABLE':40,'INDETERMINATE':11,'PROBABLE':8})
        self.assertEqual(len(self.after['comparison']),59)
        self.assertEqual(self.after['metrics']['changed'],47)
        self.assertEqual(self.after['metrics']['requires_engineer_decision'],19)
        self.assertTrue(all(o['state']!='RELIABLE' for o in self.after['occurrences'] if o['documentary_mark']=='N40'))

    def test_n26_now_associated_without_claiming_anchorage(self):
        o=next(o for o in self.after['occurrences'] if o['documentary_mark']=='N26')
        self.assertEqual(o['stage9_state'],'INDETERMINATE');self.assertEqual(o['state'],'RELIABLE')
        self.assertEqual(o['slabs'],['L607']);self.assertEqual(o['thickness_options_cm'],[20.0])
        self.assertTrue(o['exterior_segment_ids'])

    def test_reexecution_and_original_domain_confidence(self):
        self.assertEqual(refine(self.before),self.after)
        self.assertTrue(all(not d['confirmed'] for d in self.after['domains']))


if __name__=='__main__':unittest.main()
