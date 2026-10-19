"""Human contour registration regressions, not independent metric acceptance."""
import copy
import json
from pathlib import Path
import unittest
from confirmed_slab_outline import fit_axis,register_outline,analyze
from polygonal_slabs import Point


class SyntheticRegistrationTests(unittest.TestCase):
    def test_known_scale_offset_and_degenerate_anchors(self):
        fit=fit_axis([[0,10],[10,30],[20,50]])
        self.assertEqual(fit['pdf_to_image_scale'],2);self.assertEqual(fit['offset_px'],10)
        with self.assertRaises(ValueError):fit_axis([[1,2],[1,3]])


class RealHumanContourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2]
        cls.inv=json.loads((root/'analises/lajes_relacoes_contornos/inventario.json').read_text(encoding='utf-8'))
        cls.profile=json.loads((root/'analises/lajes_l603_confirmada/confirmacao_joao_L603.json').read_text(encoding='utf-8'))
        cls.result=analyze(cls.inv,cls.profile)

    def test_connected_perimeter_excludes_l607_and_lower_l605(self):
        poly,registration=register_outline(self.profile)
        self.assertTrue(poly.is_valid);self.assertEqual(poly.geom_type,'Polygon')
        self.assertTrue(poly.contains(Point(600,800)));self.assertTrue(poly.contains(Point(1400,800)))
        self.assertFalse(poly.contains(Point(970,740)));self.assertFalse(poly.contains(Point(970,1050)))
        self.assertEqual(registration['metric_validation'],'APPROXIMATE_PDF_REGISTRATION_PENDING_ENGINEER_REVIEW')

    def test_mirrored_representations_kept_and_no_nominal_n26_assignment(self):
        hits={h['display_id']:h for h in self.result['distributed_intersections']}
        for id in ('O034','O035','O043','O044','O031','O032'):
            self.assertEqual(hits[id]['state'],'INTERIOR_INTERSECTION_SUPPORTED')
        self.assertEqual(hits['O036']['intersection_area_pt2'],0)
        self.assertEqual(self.result['metrics']['distributed_nominal_intersections'],18)

    def test_wrong_document_confirmation_rejected(self):
        profile=copy.deepcopy(self.profile);profile['pdf_sha256']='different-document'
        with self.assertRaises(ValueError):analyze(self.inv,profile)

    def test_input_preserved_no_resistant_calculations(self):
        prior=copy.deepcopy(self.inv);result=analyze(self.inv,self.profile)
        self.assertEqual(self.inv,prior);self.assertFalse(result['structural_calculations_performed'])
        self.assertTrue(all(not h['physical_assignment_of_entire_bar_confirmed'] for h in result['distributed_intersections']))


if __name__=='__main__':unittest.main()
