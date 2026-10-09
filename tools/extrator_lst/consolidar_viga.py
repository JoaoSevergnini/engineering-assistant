"""Consolida JSON documental de vigas TQS sem reler LST ou verificar estruturas.

API: consolidate(raw) -> dict; load_beam(path) -> objeto com acesso por atributos.
Contrato, politicas de fontes e unidades: CONSOLIDACAO.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import unicodedata
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

SCHEMA_VERSION = '1.1'
REFERENCE_REPORTS = {'RELDTVGS.LST', 'VGESFS.LST'}
DETAIL_REPORTS = {'RELDTFPS.LST', 'RELDTFNG.LST', 'RELDTVET.LST'}
SUMMARY_REPORTS = {'FLEXPS.LST', 'FLEXNG.LST', 'ESTRIB.LST'}
GEOMETRY = {
    'comprimento': 'length', 'largura': 'width', 'altura': 'height',
    'mesa_superior': 'top_flange_width', 'mesa_inferior': 'bottom_flange_width',
    'tipo_secao': 'section_type', 'espessura_laje_superior': 'top_slab_thickness',
    'espessura_laje_inferior': 'bottom_slab_thickness',
    'face_superior_eixo': 'top_face_to_axis', 'face_lateral_eixo': 'side_face_to_axis',
}
COVER = {
    'cobrimento_geral': 'general', 'cobrimento_sup': 'top',
    'cobrimento_inf': 'bottom', 'cobrimento_contato_solo': 'soil_contact_parameter',
    'cobrimento_desta_viga': 'beam_parameter',
    'cobr_para_arm_compres': 'compression_reinforcement',
    'cobr_super_difer': 'additional_top', 'c_sup_adic': 'additional_top',
    'cobr': 'unspecified_face',
}
SUPPORT = {
    'largura': 'width', 'excentricidade': 'eccentricity',
    'continuidade': 'continuity_code', 'alavanca': 'lever_code',
    'dimensao_superior': 'upper_dimension', 'espessura_inferior': 'lower_thickness',
    'espessura_superior': 'upper_thickness',
}
POLICIES = {
    'tqs_semantics': '.agents/skills/reinforcement-review/references/tqs-beam-data.md',
    'derived_lengths': 'support_axis_length=L_TQS+DEPEV_left+DEPEV_right; clear_span_length=support_axis_length-b_left/2-b_right/2. Unresolved operands remain null; original geometry is preserved.',
    'reactions': 'Per-report paired max/min observations in kN, preserving signs, variants and sources; no assumed combinations or transfer to drawing supports.',
    'reference_geometry': 'RELDTVGS e VGESFS descrevem a geometria geral de entrada. Sao fontes de igual prioridade para a geometria de referencia, sem representar geometria final de detalhamento. Conflitos entre elas permanecem null; valores diferentes em etapas posteriores ficam em warnings.',
    'span_mapping': 'Numeracao de referencia vem das tabelas gerais. Tabelas detalhadas so sao relacionadas por ordem quando possuem dois registros extremos de comprimento zero, mesma quantidade de vaos positivos e mesma sequencia unica de apoios. Nao se aplica deslocamento numerico presumido.',
    'consensus': 'Sem prioridade documental especifica, somente valores iguais apos normalizacao sao consolidados. Conflitos ficam null, com alternativas e fontes em warnings. Nao se aplica tolerancia de arredondamento dos relatorios.',
    'cover': 'Cobrimentos por face, geral, adicional e parametros especificos sao propriedades distintas. Zero nao e interpretado como heranca ou ausencia. c em cabecalho permanece sem face especificada.',
    'forces': 'Series conservam sinal, secoes, lacunas e etapa documental. Somente series identicas da mesma etapa sao deduplicadas. Nao sao criadas abscissas, combinacoes ou envoltorias.',
}


def fold(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value) if not unicodedata.combining(c)).lower()


def equal(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=0, abs_tol=1e-10)
    return a == b


def scalar(value, unit=None):
    """Only consume normalization already performed in the documentary layer."""
    if not isinstance(value, dict):
        return value if unit is None else None
    if unit is None:
        return value.get('valor')
    normalized = value.get('normalizado', {})
    if normalized.get('unidade') == unit:
        return normalized.get('valor')
    if str(value.get('unidade_original', '')).lower() == unit.lower():
        return value.get('valor')
    return None


class Consolidator:
    def __init__(self, raw):
        if raw.get('schema_version') != '1.0' or not isinstance(raw.get('categorias'), dict):
            raise ValueError('Esperado JSON documental schema_version 1.0 com categorias.')
        if not isinstance(raw.get('viga'), str) or not raw['viga']:
            raise ValueError('Identificacao da viga ausente.')
        self.raw = raw
        self.warnings = []
        self.sources = {}
        self.provenance = {}
        self.records = []
        seen = set()
        for category, records in sorted(raw['categorias'].items()):
            for index, record in enumerate(records):
                self._register(record, f'/categorias/{category}/{index}', seen)
        for index, record in enumerate(raw.get('outros_dados', [])):
            self._register(record, f'/outros_dados/{index}', seen)
        self.records.sort(key=lambda r: (r['origem']['arquivo'].upper(), r['origem']['linha_inicial']))
        self.ids = {}
        for index, record in enumerate(self.records, 1):
            self.ids[id(record)] = f's{index:03}'
        self.mapping = {}
        self.zero_spans = set()
        self.zero_sources = []

    def _register(self, record, pointer, seen):
        origin = record['origem']
        key = (origin['arquivo'], origin['linha_inicial'], origin['linha_final'])
        if key not in seen:
            seen.add(key)
            # Copy only wrapper metadata, never modify the supplied extraction.
            self.records.append({**record, '_pointer': pointer})

    def source(self, record, field=''):
        sid = self.ids[id(record)]
        origin = record['origem']
        self.sources[sid] = {
            'file': origin['arquivo'], 'lines': [origin['linha_inicial'], origin['linha_final']],
            'raw_pointer': record['_pointer'],
        }
        return sid + ('#/' + field if field else '')

    def warn(self, code, path, **details):
        self.warnings.append({'code': code, 'path': path, **details})

    def resolve(self, path, candidates, preferred=False):
        """Candidate = (value, reference, preferred). No majority vote or first-file rule."""
        groups = []
        for value, source, priority in candidates:
            if value is None:
                continue
            group = next((g for g in groups if equal(g['value'], value)), None)
            if group is None:
                group = {'value': value, 'sources': [], '_preferred': False}
                groups.append(group)
            if source not in group['sources']:
                group['sources'].append(source)
            group['_preferred'] |= priority
        if not groups:
            self.provenance[path] = []
            return None
        eligible = [g for g in groups if g['_preferred']] if preferred else groups
        if preferred and not eligible:
            eligible = groups
        chosen = eligible[0] if len(eligible) == 1 else None
        self.provenance[path] = chosen['sources'] if chosen else sorted({s for g in groups for s in g['sources']})
        if len(groups) > 1:
            self.warn('conflicting_values', path,
                      resolution='preferred_reference_geometry' if chosen and preferred else 'unresolved',
                      selected=chosen['value'] if chosen else None,
                      alternatives=[{'value': g['value'], 'sources': g['sources']} for g in groups])
        return chosen['value'] if chosen else None

    def explicit(self, key):
        for record in self.records:
            for index, field in enumerate(record.get('campos_explicitos', [])):
                if field.get('chave') == key:
                    yield record, field, f'campos_explicitos/{index}'

    def property(self, path, keys, unit=None):
        candidates = []
        for key in keys:
            for record, field, loc in self.explicit(key):
                value = scalar(field, unit)
                ref = self.source(record, loc)
                if value is None:
                    self.warn('missing_or_incompatible_unit', path, sources=[ref], expected_unit=unit)
                candidates.append((value, ref, False))
        return self.resolve(path, candidates)

    def materials_and_cover(self):
        materials = {
            'concrete': {'fck': self.property('/beam/materials/concrete/fck', ['fck'], 'MPa')},
            'steel': {'grade': None},
            'aggregate_max_size': self.property('/beam/materials/aggregate_max_size', ['dagreg'], 'm'),
        }
        candidates = []
        for record, field, loc in self.explicit('classe_aco'):
            # Punctuation-only normalization; preserve A/B suffixes.
            value = str(field['valor']).replace(' ', '').upper()
            if value.startswith('CA') and not value.startswith('CA-'):
                value = 'CA-' + value[2:]
            candidates.append((value, self.source(record, loc), False))
        materials['steel']['grade'] = self.resolve('/beam/materials/steel/grade', candidates)
        cover = {}
        for key in dict.fromkeys(COVER.values()):
            cover[key] = self.property('/beam/cover/' + key, [k for k, v in COVER.items() if v == key], 'm')
        # c is meaningful as cover only in a beam header, not arbitrary calculation rows.
        generic = []
        for record, field, loc in list(self.explicit('c')) + list(self.explicit('cobr')):
            keys = {f.get('chave') for f in record.get('campos_explicitos', [])}
            if 'viga' in keys:
                generic.append((scalar(field, 'm'), self.source(record, loc), False))
        cover['unspecified_face'] = self.resolve('/beam/cover/unspecified_face', generic)
        return materials, cover

    def geometry_rows(self):
        result = defaultdict(list)
        for record in self.records:
            data = record.get('normalizacao') or {}
            if data.get('tipo') == 'geometria_tabular':
                result[record['origem']['arquivo'].upper()].append(record)
        return result

    def support_sequences(self):
        result = defaultdict(list)
        for record in self.records:
            data = record.get('normalizacao') or {}
            if data.get('tipo') == 'apoio':
                name = data['campos'].get('nome')
                if isinstance(name, str):
                    result[record['origem']['arquivo'].upper()].append((name, record))
        return result

    def spans(self):
        rows = self.geometry_rows()
        sequences = self.support_sequences()
        primary = {file: items for file, items in rows.items() if file in REFERENCE_REPORTS}
        id_sets = {tuple(scalar(r['normalizacao']['campos']['vao']) for r in items) for items in primary.values()}
        if not primary or len(id_sets) != 1:
            self.warn('span_topology_unresolved', '/beam/spans', reason='Tabelas de geometria geral ausentes ou com identificadores incompativeis.',
                      sources=[self.source(r) for items in rows.values() for r in items])
            return []
        reference_ids = list(next(iter(id_sets)))
        if len(set(reference_ids)) != len(reference_ids) or any(not isinstance(n, (int, float)) or n <= 0 or int(n) != n for n in reference_ids):
            self.warn('span_topology_unresolved', '/beam/spans', reason='Identificadores de vao invalidos ou repetidos.')
            return []
        spans = [{'id': int(n), 'geometry': {}, 'support_ids': None, 'report_span_ids': {}, 'internal_forces': []} for n in reference_ids]
        for file, items in primary.items():
            for position, r in enumerate(items):
                n = int(scalar(r['normalizacao']['campos']['vao']))
                self.mapping[(file, n)] = position
                spans[position]['report_span_ids'][file] = n
                self.provenance[f'/beam/spans/{position}/report_span_ids/{file}'] = [self.source(r, 'normalizacao/campos/vao')]
        general_supports = sequences.get('RELDTVGS.LST', [])
        base_names = [name for name, _ in general_supports]
        valid_topology = len(base_names) == len(spans) + 1 and len(set(base_names)) == len(base_names)
        if valid_topology:
            for position, span in enumerate(spans):
                span['support_ids'] = base_names[position:position + 2]
                self.provenance[f'/beam/spans/{position}/support_ids'] = [self.source(r, 'normalizacao/campos/nome') for _, r in general_supports[position:position + 2]]
        else:
            self.warn('support_connectivity_unresolved', '/beam/spans', reason='Sequencia de apoios gerais nao determina uma cadeia unica de n+1 apoios.')
        for file, items in rows.items():
            if file in REFERENCE_REPORTS:
                continue
            lengths = [scalar(r['normalizacao']['campos'].get('comprimento'), 'm') for r in items]
            for r, length in zip(items, lengths):
                if length == 0:
                    self.zero_spans.add((file, int(scalar(r['normalizacao']['campos']['vao']))))
                    self.zero_sources.append(self.source(r, 'normalizacao/campos/comprimento'))
            detail_ids = [scalar(r['normalizacao']['campos']['vao']) for r in items]
            padded = (len(set(detail_ids)) == len(detail_ids) and file in DETAIL_REPORTS and len(items) == len(spans) + 2 and lengths[0] == 0 and lengths[-1] == 0
                      and all(v is not None and v > 0 for v in lengths[1:-1]) and valid_topology
                      and [n for n, _ in sequences.get(file, [])] == base_names)
            if not padded:
                self.warn('span_mapping_unresolved', '/beam/spans', file=file,
                          sources=[self.source(r) for r in items], reason='Sem evidencia suficiente para associar numeracao detalhada a geometria geral.')
                continue
            for position, r in enumerate(items[1:-1]):
                n = int(scalar(r['normalizacao']['campos']['vao']))
                self.mapping[(file, n)] = position
                spans[position]['report_span_ids'][file] = n
                self.provenance[f'/beam/spans/{position}/report_span_ids/{file}'] = [self.source(r, 'normalizacao/campos/vao')] + [self.source(a, 'normalizacao/campos/nome') for _, a in sequences[file]]
        # Explicit summary geometry belongs to its printed span, only in known formats.
        summaries = defaultdict(list)
        for record in self.records:
            file = record['origem']['arquivo'].upper()
            fields = {f.get('chave'): (f, i) for i, f in enumerate(record.get('campos_explicitos', []))}
            if file in SUMMARY_REPORTS and {'vao', 'comprimento', 'largura', 'altura'} <= fields.keys():
                summaries[file].append((record, fields))
        for file, items in summaries.items():
            numbers = [scalar(f['vao'][0]) for _, f in items]
            if numbers == reference_ids:
                for position, (r, f) in enumerate(items):
                    self.mapping[(file, int(numbers[position]))] = position
                    spans[position]['report_span_ids'][file] = int(numbers[position])
                    self.provenance[f'/beam/spans/{position}/report_span_ids/{file}'] = [self.source(r, f'campos_explicitos/{f["vao"][1]}')]
            else:
                self.warn('span_mapping_unresolved', '/beam/spans', file=file, sources=[self.source(r) for r, _ in items])
        for position, span in enumerate(spans):
            self.provenance[f'/beam/spans/{position}/id'] = [self.source(r, 'normalizacao/campos/vao') for items in primary.values() for r in items if scalar(r['normalizacao']['campos']['vao']) == span['id']]
            for key, target in GEOMETRY.items():
                path = f'/beam/spans/{position}/geometry/{target}'
                unit = None if key == 'tipo_secao' else 'm'
                candidates = []
                for file, items in rows.items():
                    for record in items:
                        fields = record['normalizacao']['campos']
                        n = scalar(fields['vao'])
                        if self.mapping.get((file, n)) != position or key not in fields:
                            continue
                        value = scalar(fields[key], unit)
                        ref = self.source(record, f'normalizacao/campos/{key}')
                        if value is None:
                            self.warn('missing_or_incompatible_unit', path, sources=[ref], expected_unit=unit)
                        candidates.append((value, ref, file in REFERENCE_REPORTS))
                for file, items in summaries.items():
                    for record, fields in items:
                        n = scalar(fields['vao'][0])
                        if self.mapping.get((file, n)) == position and key in fields:
                            field, index = fields[key]
                            candidates.append((scalar(field, unit), self.source(record, f'campos_explicitos/{index}'), False))
                span['geometry'][target] = self.resolve(path, candidates, preferred=True)
        # Optional additive classification: B does not prove physical side/bounds.
        for position, span in enumerate(spans):
            observations = [r for r in rows.get('VGESFS.LST', [])
                            if scalar(r['normalizacao']['campos']['vao']) == span['id']
                            and 'tipo_vao_documental' in r['normalizacao']]
            if observations:
                kinds = {r['normalizacao']['tipo_vao_documental'] for r in observations}
                span['documentary_span_kind'] = next(iter(kinds)) if len(kinds) == 1 else None
                span['original_span_tokens'] = [r['normalizacao']['identificador_vao_original'] for r in observations]
                span['physical_span_validation'] = 'PENDING'
                self.provenance[f'/beam/spans/{position}/documentary_span_kind'] = [self.source(r, 'normalizacao/tipo_vao_documental') for r in observations]
                if len(kinds) != 1:
                    self.warn('span_kind_conflicting', f'/beam/spans/{position}/documentary_span_kind')
        if self.zero_spans:
            self.warn('zero_length_documentary_spans', '/beam/spans',
                      reason='Registros de comprimento zero permanecem no raw; nao sao convertidos em vaos fisicos.',
                      report_span_ids=[{'file': f, 'span': n} for f, n in sorted(self.zero_spans)],
                      sources=self.zero_sources)
        return spans

    def supports(self):
        grouped = defaultdict(list)
        for record in self.records:
            data = record.get('normalizacao') or {}
            if data.get('tipo') == 'apoio' and isinstance(data['campos'].get('nome'), str):
                grouped[data['campos']['nome']].append(record)
        result = []
        for index, (name, records) in enumerate(sorted(grouped.items())):
            support = {'id': name}
            prefix = f'/beam/supports/{index}'
            self.provenance[prefix + '/id'] = [self.source(r, 'normalizacao/campos/nome') for r in records]
            for key, target in SUPPORT.items():
                candidates = []
                for r in records:
                    field = r['normalizacao']['campos'].get(key)
                    if field is not None:
                        candidates.append((scalar(field, None if key in ('continuidade', 'alavanca') else 'm'), self.source(r, f'normalizacao/campos/{key}'), False))
                support[target] = self.resolve(prefix + '/' + target, candidates)
            result.append(support)
        return result

    def derived_lengths(self, spans, supports):
        # Semantics: references/tqs-beam-data.md. Never resolve conflicting operands here.
        index = {support['id']: i for i, support in enumerate(supports)}
        for i, span in enumerate(spans):
            base = f'/beam/spans/{i}/geometry'
            length_path = base + '/length'
            operands = {'L_TQS': length_path}
            values = {'L_TQS': span['geometry']['length']}
            names = span['support_ids']
            for side, name in zip(('left', 'right'), names or (None, None)):
                j = index.get(name)
                for prop in ('eccentricity', 'width'):
                    key = side + '_' + prop
                    operands[key] = f'/beam/supports/{j}/{prop}' if j is not None else None
                    values[key] = supports[j][prop] if j is not None else None
            for field, keys, formula in (
                ('support_axis_length', ('L_TQS','left_eccentricity','right_eccentricity'), 'L_TQS + DEPEV_left + DEPEV_right'),
                ('clear_span_length', ('L_TQS','left_eccentricity','right_eccentricity','left_width','right_width'), 'L_TQS + DEPEV_left + DEPEV_right - b_left/2 - b_right/2')):
                path = base + '/' + field
                refs = sorted({ref for key in keys for ref in self.provenance.get(operands[key], [])})
                self.provenance[path] = refs
                span['geometry'][field] = None
                if any(values[key] is None for key in keys):
                    self.warn('derived_geometry_unresolved', path, formula=formula,
                              inputs={key: {'path':operands[key], 'value':values[key]} for key in keys}, sources=refs)
                    continue
                value = values['L_TQS'] + values['left_eccentricity'] + values['right_eccentricity']
                if field == 'clear_span_length':value -= (values['left_width'] + values['right_width']) / 2
                if not math.isfinite(value) or value < 0:
                    self.warn('invalid_derived_geometry', path, value=value, formula=formula, sources=refs)
                    continue
                span['geometry'][field] = value

    def support_reactions(self, supports):
        # Keep per-report paired envelopes; no implicit load-case compatibility.
        result = []
        support_ids = {s['id'] for s in supports}
        for record in self.records:
            data = record.get('normalizacao') or {}
            if data.get('tipo') != 'reacao_apoio':continue
            fields = data['campos']
            name = fields.get('nome')
            support_id = name if isinstance(name,str) and name in support_ids else None
            row = {'support_id':support_id, 'reported_support_name':name,
                   'report_support_number':scalar(fields.get('numero')),
                   'unit':'kN', 'max':scalar(fields.get('maxima'),'kN'),
                   'min':scalar(fields.get('minima'),'kN'),
                   'file':record['origem']['arquivo'], 'sources':[self.source(record,'normalizacao')]}
            i = len(result)
            path = f'/beam/support_reactions/{i}'
            for key, original in [('max','maxima'),('min','minima'),('reported_support_name','nome')]:
                self.provenance[path+'/'+key] = [self.source(record,'normalizacao/campos/'+original)] if original in fields else []
            self.provenance[path+'/support_id'] = self.provenance[path+'/reported_support_name']
            if support_id is None:self.warn('reaction_support_unresolved',path,sources=row['sources'])
            for key in ('max','min'):
                if row[key] is None:self.warn('reaction_value_unresolved',path+'/'+key,sources=row['sources'],expected_unit='kN')
            result.append(row)
        by_name = defaultdict(list)
        for row in result:by_name[row['reported_support_name']].append(row)
        for name, rows in by_name.items():
            if len({(row['max'],row['min']) for row in rows})>1:
                self.warn('reaction_variants', '/beam/support_reactions', support_name=name,
                          reason='Paired max/min observations retained by report; no rounding tolerance or envelope selection.',
                          sources=[ref for row in rows for ref in row['sources']])
        return result

    def force_kind(self, record, data):
        label = fold(data['grandeza_original']).replace(' ', '')
        section = fold(record.get('secao', ''))
        file = record['origem']['arquivo'].upper()
        lookup = {'qmn.': ('shear', 'min'), 'qmx.': ('shear', 'max'), 'mmn.': ('bending_moment', 'min'),
                  'mmx.': ('bending_moment', 'max'), 'mtmx.': ('torsion', 'max'),
                  'vk,min': ('shear', 'min'), 'vk,max': ('shear', 'max'),
                  'mk,min': ('bending_moment', 'min'), 'mk,max': ('bending_moment', 'max'),
                  'mtk,max': ('torsion', 'max'), 'v,min': ('shear', 'min'), 'v,max': ('shear', 'max'),
                  'ts,max': ('torsion', 'max'), 'mk,neg': ('bending_moment', 'negative'),
                  'm,neg': ('bending_moment', 'negative'), 'm,pos': ('bending_moment', 'positive')}
        if label not in lookup:
            return None
        kind, envelope = lookup[label]
        if file in REFERENCE_REPORTS:
            stage = 'model_input'
        elif file == 'RELDTFNG.LST':
            stage = 'negative_flexure_after_positive_removal' if 'eliminacao' in section else 'negative_flexure_input'
        elif file == 'RELDTFPS.LST':
            stage = 'positive_flexure_input'
        elif file == 'RELDTVET.LST':
            stage = 'shear_final_absolute' if 'finais' in section else 'shear_initial_absolute' if 'iniciais' in section else 'shear_torsion_input'
        else:
            stage = 'unspecified'
        return kind, envelope, stage

    def forces(self, spans):
        groups = defaultdict(list)
        unassigned = []
        for record in self.records:
            data = record.get('normalizacao') or {}
            if data.get('tipo') != 'serie_13_secoes':
                continue
            description = self.force_kind(record, data)
            if description is None:
                continue  # Stirrup diameters/spacings are outside this initial model.
            key = (record['origem']['arquivo'].upper(), data['vao_original'])
            if key in self.zero_spans:
                ref = self.source(record, 'normalizacao')
                if any(v is not None and v.get('valor') not in (0, None) for v in data['valores']):
                    self.warn('nonzero_force_on_zero_length_span', '/unassigned_forces', sources=[ref])
                else:
                    continue
            position = self.mapping.get(key)
            kind, envelope, stage = description
            unit = 'kN' if kind == 'shear' else 'kN.m'
            values = [scalar(v, unit) if v is not None else None for v in data['valores']]
            ref = self.source(record, 'normalizacao')
            if any(v is not None and values[i] is None for i, v in enumerate(data['valores'])):
                self.warn('missing_or_incompatible_unit', '/beam/spans', sources=[ref], expected_unit=unit)
            if len(values) != len(data['secoes']):
                raise ValueError('Serie documental com quantidades diferentes de secoes e valores.')
            series = {'quantity': kind, 'envelope': envelope, 'stage': stage, 'unit': unit,
                      'sections': data['secoes'], 'positions': None, 'values': values, 'sources': [ref]}
            if position is None:
                unassigned.append({'file': key[0], 'report_span_id': key[1], **series})
                continue
            group = groups[(position, kind, envelope, stage)]
            identical = next((s for s in group if s['sections'] == series['sections'] and s['values'] == series['values']), None)
            if identical:
                identical['sources'].append(ref)
            else:
                group.append(series)
        for (position, kind, envelope, stage), variants in sorted(groups.items()):
            if len(variants) > 1:
                self.warn('conflicting_force_series', f'/beam/spans/{position}/internal_forces',
                          quantity=kind, envelope=envelope, stage=stage,
                          reason='Series distintas da mesma etapa mantidas como variantes, sem escolha de uma envoltoria.',
                          sources=[s for v in variants for s in v['sources']])
            spans[position]['internal_forces'].extend(variants)
        if unassigned:
            self.warn('unassigned_force_series', '/unassigned_forces', count=len(unassigned))
        return unassigned

    def run(self):
        materials, cover = self.materials_and_cover()
        spans = self.spans()
        supports = self.supports()
        self.derived_lengths(spans, supports)
        reactions = self.support_reactions(supports)
        unassigned = self.forces(spans)
        identity_refs = ['raw#/viga'] + [self.source(r, loc) for r, _, loc in self.explicit('viga')]
        self.provenance['/beam/id'] = identity_refs
        self.provenance['/beam/number'] = identity_refs
        beam_id = self.raw['viga']
        number = int(beam_id[1:]) if beam_id.startswith('V') and beam_id[1:].isdigit() else None
        files_used = {source['file'] for source in self.sources.values()}
        return {
            'schema_version': SCHEMA_VERSION,
            'model_type': 'consolidated_beam',
            'units': {'length': 'm', 'stress': 'MPa', 'force': 'kN', 'moment': 'kN.m'},
            'beam': {'id': beam_id, 'number': number, 'materials': materials, 'cover': cover, 'spans': spans, 'supports': supports, 'support_reactions': reactions},
            'warnings': self.warnings, 'unassigned_forces': unassigned,
            'provenance': self.provenance, 'sources': dict(sorted(self.sources.items())),
            'source_files': {f['arquivo']: {'sha256': f.get('sha256')} for f in self.raw.get('arquivos', []) if f['arquivo'] in files_used},
            'policies': POLICIES,
        }


def consolidate(raw):
    """Pure transformation: no LST access, source mutation or structural checks."""
    return Consolidator(raw).run()


def load_beam(path):
    """Return attribute-access beam, e.g. beam.spans[0].geometry.height (metres)."""
    model = json.loads(Path(path).read_text(encoding='utf-8-sig'), object_hook=lambda o: SimpleNamespace(**o))
    if model.model_type != 'consolidated_beam':
        raise ValueError('Esperado modelo consolidado.')
    return model.beam


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('entrada', type=Path, help='JSON documental *_raw.json')
    parser.add_argument('--saida', type=Path, required=True)
    args = parser.parse_args()
    if args.entrada.resolve() == args.saida.resolve():
        parser.error('Entrada documental e saida consolidada devem ser arquivos diferentes.')
    content = args.entrada.read_bytes()
    model = consolidate(json.loads(content.decode('utf-8-sig')))
    model['raw_document'] = {'file': args.entrada.name, 'sha256': hashlib.sha256(content).hexdigest()}
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(json.dumps(model, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    print(f'{model["beam"]["id"]}: {len(model["beam"]["spans"])} vao(s), {len(model["beam"]["supports"])} apoio(s), {len(model["warnings"])} aviso(s) documentais.')


if __name__ == '__main__':
    main()
