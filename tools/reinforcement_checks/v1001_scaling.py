"""Fixture/golden real: interrupcao direita N3. Nenhuma regra por marca na producao."""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys
from bar_scaling import check_bar_scaling

ROOT = Path(__file__).resolve().parents[2]
NAMES = ('V1001_beam_model.json', 'V1001_tqs.json', 'V1001_tqs_positions.json',
         'V1001_beam_mapping.json', 'V1001_tqs_raw.json')
SCOPE = {'flexure': 'positive', 'horizontal': True, 'hooks': False, 'welds': False,
         'special_longitudinal_compression': False, 'sliding_formwork': False,
         'ribbed': True, 'vertical_stirrups': True, 'vc_model': 'Vc0',
         'provenance': {'engineer_request': '2026-10-05, V1001/N3: horizontal, lower first layer, straight; initial scope without hooks/welds/special compression; no sliding formwork documented',
                        'drawing': 'V1001_detalhamento_prancha.json /longitudinal_reinforcement/positive/0 and /stirrups',
                        'model_scope': 'Concretopy docs/ancoragem.md: ribbed tension bars, vertical stirrups, Vc=Vc0; adopted workflow hypotheses, not execution inspection'}}


def analyze(data, api):
    return check_bar_scaling(*data, api, interrupted_mark='N3', cut_side='right', scope=SCOPE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--concretopy-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    paths = [ROOT/'analises/pranchas'/n for n in NAMES]
    try:
        data = [json.loads(p.read_text(encoding='utf8')) for p in paths]
        protected = list(paths)
        input_audit = []
        for entry in data[3]['inputs'].values():
            p = Path(entry['path'])
            p = p if p.is_absolute() else ROOT/p
            protected.append(p)
            content = p.read_bytes()
            actual = hashlib.sha256(content).hexdigest()
            normalized = hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest()
            if entry['sha256'] not in (actual, normalized):
                raise ValueError('Mapping desatualizado: '+str(p))
            input_audit.append({'path': str(p), 'expected_sha256': entry['sha256'],
                                'actual_sha256': actual, 'validation': 'exact_bytes' if actual == entry['sha256'] else 'CRLF_to_LF_only_hash_match'})
        if any(args.output.resolve() == p.resolve() or args.output.exists() and args.output.samefile(p) for p in protected):
            raise ValueError('Saida sobre entrada/contexto nao permitida.')
        if hashlib.sha256(paths[-1].read_bytes()).hexdigest() != data[1]['raw_document']['sha256']:
            raise ValueError('Raw incompatível.')
        sys.path.insert(0, str(args.concretopy_root.resolve()))
        api = importlib.import_module('concretopy')
        if not Path(api.__file__).resolve().is_relative_to(args.concretopy_root.resolve()):
            raise ValueError('Concretopy fora da raiz indicada.')
        out = analyze(data, api)
        out['mapping_input_audit'] = input_audit
        out['inputs'] = {n: {'path': str(p.resolve()), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                         for n, p in zip(NAMES, paths)}
        out['implementation'] = {n: hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest()
                                for n in ('bar_scaling.py', 'tqs_shear.py', 'v1001_scaling.py', 'flexure_regions.py',
                                          'positive_flexure.py', 'moment_diagram.py', 'materials.py', 'tqs_moments.py')}
        out['d_for_al']['audit_reference'] = 'tools/reinforcement_checks/al_effective_depth.md; engineer_confirmed_al_effective_depth_v1, 2026-10-05'
        args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf8')
        print(json.dumps({k: out[k] for k in ('event_x_m', 'd_for_al', 'bond_condition', 'condition_A', 'condition_B', 'overall', 'diagnostics')}, ensure_ascii=True, indent=2))
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
