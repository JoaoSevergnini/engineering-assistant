"""Contrato auditado da serie VGESFS M MX., reutilizado pelo golden e regioes."""
import copy

def at(doc, pointer):
    for part in pointer.strip('/').split('/'):
        doc = doc[int(part)] if isinstance(doc, list) else doc[part]
    return doc


def audited_moment_series(mapping, tqs, raw, *, flexure_sign="POSITIVE"):
    if flexure_sign not in ("POSITIVE","NEGATIVE"):
        raise ValueError("unknown_flexure_sign")
    label,envelope=("M MX.","max") if flexure_sign=="POSITIVE" else ("M MN.","min")
    candidates = []
    for i, series in enumerate(mapping['force_series']):
        if series.get('quantity') != 'bending_moment':
            continue
        proofs = []
        for ref in series['sources']:
            src = tqs['sources'][ref.split('#')[0]]
            rec = at(raw, src['raw_pointer'])
            norm = rec.get('normalizacao') or {}
            if src['file'] == 'VGESFS.LST' and norm.get('grandeza_original') == label and norm.get('vao_original') == tqs['beam']['spans'][0]['report_span_ids']['VGESFS.LST']:
                if series.get('envelope') != envelope or series.get('stage') != 'model_input' or series.get('unit') != 'kN.m':
                    raise ValueError('Contrato da série M MX. incompatível.')
                if [v['normalizado']['valor'] for v in norm['valores']] != series['values']:
                    raise ValueError('Valores da série divergem da origem raw.')
                proofs.append({'reference': ref, 'source': copy.deepcopy(src), 'record': copy.deepcopy(rec)})
        if proofs:
            candidates.append((i,series,proofs))
    if len(candidates) != 1:
        raise ValueError('Envelope positivo característico não identificado univocamente por registro VGESFS M MX.')
    return candidates[0]
