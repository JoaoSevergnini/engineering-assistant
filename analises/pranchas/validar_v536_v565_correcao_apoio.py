"""V536/V565 detail-oriented support correction fixture; prior goldens read-only."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/reinforcement_checks'),str(ROOT/'analises/pranchas'),str(ROOT.parent/'concretopy')]
import concretopy as api
from validar_v536_v565_apoio_esquerdo import load_case,read,OUT
from moment_diagram import diagram_from_tqs
from support_correction import correction_workflow

def load_detail_case(beam):
    context,current,doc=load_case(beam)
    mapping=read(beam+'_beam_mapping.json')
    golden=read(beam+'_N3_scaling_check.json')
    diagram=diagram_from_tqs(mapping,read(beam+'_tqs.json'),read(beam+'_tqs_positions.json'),read(beam+'_tqs_raw.json'))
    bars=[dict(b) for b in mapping['reinforcement'] if b.get('function')=='positive']
    for bar in bars:
        physical=[l for l in golden['d_for_al']['contributions'] if any(c['mark']==bar['mark'] for c in l['components'])]
        assert len(physical)==1
        bar['d_cm']=physical[0]['d_cm']
    context.update(support_reference_x_m=mapping['supports']['left']['axis_x'],
        extension_target_x_m=min(b['x_start_common'] for b in bars if b['x_start_common']<=mapping['supports']['left']['axis_x']),
        longitudinal_provenance={'mapping':beam+'_beam_mapping.json','physical_centers':beam+'_N3_scaling_check.json#/d_for_al/contributions',
          'section_hypothesis':'Uniform rectangular resistant section and layer parameterization of previous golden; not proof of actual stirrup distribution inside supports.',
          'demand':'Audited characteristic M MX. piecewise-linear diagram. Check all composition regions over sampled domain, no extrapolation.',
          'diagram_provenance':diagram.provenance})
    return context,bars,diagram

SEARCH={'series':[10,12.5,16,20,25],'max_steps':2,'counts':[2,3]}

def run():
    for beam in ('V536','V565'):
        context,bars,diagram=load_detail_case(beam)
        result=correction_workflow(context,bars,diagram,api,redistribution_search=SEARCH)
        result.update(beam=beam,date='2026-10-06',context=context,
            engineer_decision={'classification':'engineering_judgment','decision':'Engineer reported practical preference for complementary anchorage/staples for V536; not a forced computational conclusion. No staples designed.'} if beam=='V536' else None)
        paths=[Path(__file__),ROOT/'tools/reinforcement_checks/support_correction.py',ROOT/'tools/reinforcement_checks/support_alternatives.py']
        result['implementation']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        (OUT/(beam+'_support_correction.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
        print(beam,result['next_step'],result['diagnostics'])
        for c in [result['existing']]+result['extensions']+result['redistributions']:
            print(c['id'],c['technically_valid'],c['recomendavel_como_correcao'],c['cabimento_transversal'],c['reasons'])
            if c.get('support_check',{}).get('metrics'): print(c['support_check']['metrics'])

if __name__=='__main__':run()
