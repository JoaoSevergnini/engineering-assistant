"""Ensaio documental de positions: VGESFS + DEPEV de RELDTFPS.

Nao dimensiona, nao interpola e nao altera os consolidadores existentes.
"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path


def pointer(document, path):
    value = document
    for part in path.strip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def metres(field):
    normalized = field.get('normalizado') or {}
    value = normalized.get('valor')
    if normalized.get('unidade') != 'm' or isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('Operando ausente ou sem unidade normalizada m.')
    return value


def fill_positions(model, raw):
    """Retorna copia de ensaio com somente series VGESFS e positions em m.

    Origem local: eixo fisico esquerdo de cada vao. Sem offset global de viga.
    Conflitos na fonte escolhida impedem a saida; nenhuma fonte substituta.
    """
    out = copy.deepcopy(model)
    if model['units']['length'] != 'm':
        raise ValueError('Unidade de comprimento do modelo deve ser m.')
    records = [(sid, source, pointer(raw, source['raw_pointer']))
               for sid, source in out['sources'].items()]

    def unique(candidates, label):
        if not candidates:
            raise ValueError('Fonte escolhida ausente: ' + label)
        values = [metres(field) for field, ref in candidates]
        if any(v != values[0] for v in values):
            raise ValueError('Conflito na fonte escolhida: ' + label)
        return values[0], sorted(set(ref for field, ref in candidates))

    count = 0
    for index, span in enumerate(out['beam']['spans']):
        report_span = span['report_span_ids'].get('VGESFS.LST')
        names = span.get('support_ids')
        if report_span is None or not names or len(names) != 2:
            raise ValueError('Vao sem numeracao VGESFS ou orientacao dos apoios.')
        lengths, offsets = [], []
        for sid, source, record in records:
            data = record.get('normalizacao') or {}
            fields = data.get('campos') or {}
            if source['file'].upper() == 'VGESFS.LST' and data.get('tipo') == 'geometria_tabular' and fields['vao']['valor'] == report_span:
                lengths.append((fields['comprimento'], sid+'#/normalizacao/campos/comprimento'))
            if source['file'].upper() == 'RELDTFPS.LST' and data.get('tipo') == 'apoio' and fields.get('nome') == names[0]:
                offsets.append((fields['excentricidade'], sid+'#/normalizacao/campos/excentricidade'))
        length, length_refs = unique(lengths, 'comprimento VGESFS')
        offset, offset_refs = unique(offsets, 'DEPEV esquerdo RELDTFPS')
        if length <= 0 or offset < 0:
            raise ValueError('Comprimento nao positivo ou DEPEV negativo fora do padrao confirmado.')
        selected = []
        for series in span['internal_forces']:
            refs = [ref for ref in series['sources']
                    if out['sources'][ref.split('#')[0]]['file'].upper() == 'VGESFS.LST']
            if not refs:
                continue
            if series['sections'] != list(range(1, 14)) or len(series['values']) != 13:
                raise ValueError('Esperadas 13 secoes ordenadas com 13 valores.')
            for ref in refs:
                source = out['sources'][ref.split('#')[0]]
                record = pointer(raw, source['raw_pointer'])
                if record['normalizacao']['vao_original'] != report_span:
                    raise ValueError('Serie VGESFS associada a outro vao.')
            series['sources'] = refs
            series['positions'] = [offset + i * length / 12 for i in range(13)]
            series['positions'][-1] = offset + length
            path = f'/beam/spans/{index}/internal_forces/{len(selected)}/positions'
            out['provenance'][path] = sorted(set(length_refs + offset_refs + refs))
            selected.append(series)
            count += 1
        if not selected:
            raise ValueError('Sem series VGESFS no vao.')
        # Remap any existing force pointers after selecting only VGESFS series.
        prefix = f'/beam/spans/{index}/internal_forces/'
        old_paths = [p for p in model['provenance'] if p.startswith(prefix)]
        if old_paths:
            raise ValueError('Proveniencia por indice de serie exige remapeamento explicito.')
        span['internal_forces'] = selected
    out['policies']['forces'] = 'Ensaio: somente series VGESFS, valores e sinais preservados; sem interpolacao ou majoracao.'
    out['policies']['section_positions'] = 'Em m; origem local no eixo fisico esquerdo de cada vao; x_i=DEPEV_esq(RELDTFPS)+(i-1)*length(VGESFS)/12. Demais campos e warnings herdados do modelo anterior; nao representam migracao integral das politicas de fontes.'
    return out, count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    parser.add_argument('raw', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.resolve() in (args.model.resolve(), args.raw.resolve()):
        raise ValueError('Ensaio deve usar saida distinta das entradas.')
    model = json.loads(args.model.read_text(encoding='utf8'))
    raw_bytes = args.raw.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != model['raw_document']['sha256']:
        raise ValueError('Raw nao corresponde ao hash do modelo.')
    result, count = fill_positions(model, json.loads(raw_bytes))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf8')
    print(json.dumps({'beam':result['beam']['id'], 'series_with_positions':count, 'output':str(args.output)}))


if __name__ == '__main__':
    main()
