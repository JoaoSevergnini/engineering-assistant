"""Evaluation only: manually registered reference never enters recognition."""
from polygonal_slabs import Polygon,Point,shape,geo


def compare(candidate,reference,tolerance_pt):
    if tolerance_pt<=0:raise ValueError('Positive evaluation tolerance required')
    candidate=shape(candidate);reference=shape(reference)
    intersection=candidate.intersection(reference);union=candidate.union(reference)
    exterior=Polygon(candidate.exterior);ref_exterior=Polygon(reference.exterior)
    deviations=[]
    for name,source,target in [('AUTOMATIC',exterior,ref_exterior),('REFERENCE',ref_exterior,exterior)]:
        deviations.extend((Point(p).distance(target.boundary),name,list(p)) for p in source.exterior.coords)
    distance,side,point=max(deviations)
    return {'intersection_over_union':intersection.area/union.area,
        'exterior_only_intersection_over_union':exterior.intersection(ref_exterior).area/exterior.union(ref_exterior).area,
        'symmetric_difference_area_pt2':candidate.symmetric_difference(reference).area,
        'area_relative_difference':(candidate.area-reference.area)/reference.area,
        'exterior_hausdorff_distance_pt':exterior.boundary.hausdorff_distance(ref_exterior.boundary),
        'largest_vertex_discrepancy':{'source':side,'point_pdf_pt':point,'distance_pt':distance},
        'evaluation_tolerance_pt':tolerance_pt,
        'candidate_exterior_within_reference_band_fraction':exterior.boundary.intersection(ref_exterior.boundary.buffer(tolerance_pt)).length/exterior.length,
        'reference_exterior_within_candidate_band_fraction':ref_exterior.boundary.intersection(exterior.boundary.buffer(tolerance_pt)).length/ref_exterior.length,
        'candidate_only_geometry_pdf_pt':geo(candidate.difference(reference)),
        'reference_only_geometry_pdf_pt':geo(reference.difference(candidate)),
        'reference_limit':'HUMAN_TOPOLOGY_WITH_APPROXIMATE_SCREENSHOT_METRIC_DIGITIZATION; NOT_GROUND_TRUTH_SURVEY',
        'automatic_validation_authorized':False}
