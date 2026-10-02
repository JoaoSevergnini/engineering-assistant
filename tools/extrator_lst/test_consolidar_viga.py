"""Testes independentes da consolidacao: fixtures em memoria, sem TQS ou LST."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from consolidar_viga import consolidate, load_beam


def quantity(value, unit=None):
    result = {'valor': value, 'unidade_original': unit}
    conversions = {'m': ('m', 1), 'cm': ('m', .01), 'MPa': ('MPa', 1),
                   'kgf/cm2': ('MPa', .0980665), 'tf': ('kN', 9.80665),
                   'tf,cm': ('kN.m', .0980665), 'tf*m': ('kN.m', 9.80665)}
    if unit in conversions:
        target, factor = conversions[unit]
        result['normalizado'] = {'valor': round(value * factor, 12), 'unidade': target}
    return result


def field(key, value, unit=None):
    return {'chave': key, **quantity(value, unit)}


def record(file, line, data=None, explicit=None, section='inicio'):
    return {'origem': {'arquivo': file, 'linha_inicial': line, 'linha_final': line,
                       'texto': 'NAO INTERPRETAR ESTE TEXTO'},
            'normalizacao': data, 'campos_explicitos': explicit or [], 'secao': section}


def geometry(file, line, span, length=1.206, width=.14, height=.32, unit='m'):
    return record(file, line, {'tipo': 'geometria_tabular', 'campos': {
        'vao': quantity(span), 'comprimento': quantity(length, unit),
        'largura': quantity(width, unit), 'altura': quantity(height, unit), 'tipo_secao': quantity(1)}})


def support(file, line, name, width=.14, eccentricity=0, unit='m'):
    return record(file, line, {'tipo': 'apoio', 'campos': {
        'nome': name, 'largura': quantity(width, unit), 'excentricidade': quantity(eccentricity, unit),
        'continuidade': 'VIGA', 'alavanca': 'NAO'}})


def force(file, line, span, label='Vk,min', values=None, unit='tf', section='esforcos do modelo'):
    if values is None:
        values = [-i / 10 for i in range(13)]
    return record(file, line, {'tipo': 'serie_13_secoes', 'vao_original': span,
                              'grandeza_original': label, 'secoes': list(range(1, len(values) + 1)),
                              'valores': [quantity(v, unit) if v is not None else None for v in values]}, section=section)


def raw_fixture():
    rows = [geometry('RELDTVGS.LST', 10, 1), geometry('VGESFS.LST', 10, 1),
            support('RELDTVGS.LST', 20, 'V10'), support('RELDTVGS.LST', 21, 'P20', .24),
            record('FLEXPS.LST', 1, explicit=[field('fck', 40, 'MPa'), field('classe_aco', 'CA-50')]),
            record('RELDTVGS.LST', 2, explicit=[field('cobrimento_sup', 2.5, 'cm'), field('cobrimento_inf', 2.5, 'cm'), field('cobrimento_desta_viga', 0, 'cm')]),
            force('RELDTVGS.LST', 30, 1), force('VGESFS.LST', 30, 1, 'Q MN.')]
    return {'schema_version': '1.0', 'viga': 'V504', 'categorias': {'fixture': rows},
            'outros_dados': [], 'arquivos': [], 'trechos': [{'texto': 'IGNORADO'}]}


def add_details(raw, file='RELDTFNG.LST', spans=(10, 20, 30)):
    raw['categorias']['fixture'] += [
        geometry(file, 40, spans[0], 0, 100, 100, 'cm'),
        geometry(file, 41, spans[1], 120.6, 14, 32, 'cm'),
        geometry(file, 42, spans[2], 0, 100, 100, 'cm'),
        support(file, 50, 'V10', 14, unit='cm'), support(file, 51, 'P20', 24, unit='cm'),
    ]


class ConsolidationTests(unittest.TestCase):
    def test_direct_values_units_and_sources(self):
        model = consolidate(raw_fixture())
        beam = model['beam']
        self.assertEqual(beam['spans'][0]['geometry']['height'], .32)
        self.assertEqual(beam['spans'][0]['support_ids'], ['V10', 'P20'])
        self.assertEqual(beam['materials']['concrete']['fck'], 40)
        self.assertEqual(beam['cover']['top'], .025)
        refs = model['provenance']['/beam/spans/0/geometry/height']
        self.assertEqual(len(refs), 2)
        self.assertEqual({model['sources'][r.split('#')[0]]['file'] for r in refs}, {'RELDTVGS.LST', 'VGESFS.LST'})

    def test_no_source_mutation_or_original_text_in_model(self):
        raw = raw_fixture()
        before = copy.deepcopy(raw)
        model = consolidate(raw)
        self.assertEqual(raw, before)
        serialized = json.dumps(model)
        self.assertNotIn('NAO INTERPRETAR', serialized)
        self.assertNotIn('IGNORADO', serialized)
        self.assertNotIn('texto', serialized)

    def test_duplicate_categories_do_not_duplicate_observations(self):
        raw = raw_fixture()
        raw['categorias']['duplicated'] = copy.deepcopy(raw['categorias']['fixture'])
        model = consolidate(raw)
        self.assertEqual(len(model['provenance']['/beam/spans/0/geometry/height']), 2)
        self.assertEqual(len(model['beam']['spans'][0]['internal_forces']), 1)

    def test_conflicting_fck_is_null_not_rounded(self):
        raw = raw_fixture()
        raw['categorias']['fixture'].append(record('FLEXNG.LST', 3, explicit=[field('fck', 400, 'kgf/cm2')]))
        model = consolidate(raw)
        self.assertIsNone(model['beam']['materials']['concrete']['fck'])
        w = next(w for w in model['warnings'] if w['path'].endswith('/concrete/fck'))
        self.assertEqual({a['value'] for a in w['alternatives']}, {40, 39.2266})
        self.assertEqual(w['resolution'], 'unresolved')

    def test_steel_formatting_is_normalized_but_suffix_not_removed(self):
        raw = raw_fixture()
        raw['categorias']['fixture'].append(record('FLEXNG.LST', 3, explicit=[field('classe_aco', 'CA50')]))
        self.assertEqual(consolidate(raw)['beam']['materials']['steel']['grade'], 'CA-50')
        raw['categorias']['fixture'].append(record('RELDTFNG.LST', 3, explicit=[field('classe_aco', 'CA-50A')]))
        self.assertIsNone(consolidate(raw)['beam']['materials']['steel']['grade'])

    def test_reference_geometry_preference_is_explicit(self):
        raw = raw_fixture()
        add_details(raw)
        detail = next(r for r in raw['categorias']['fixture'] if r['origem']['arquivo']=='RELDTFNG.LST' and r['origem']['linha_inicial']==41)
        detail['normalizacao']['campos']['altura'] = quantity(33, 'cm')
        model = consolidate(raw)
        self.assertEqual(model['beam']['spans'][0]['geometry']['height'], .32)
        w = next(w for w in model['warnings'] if w['path'].endswith('/height'))
        self.assertEqual(w['resolution'], 'preferred_reference_geometry')
        self.assertEqual({a['value'] for a in w['alternatives']}, {.32, .33})

    def test_equal_priority_conflict_remains_null(self):
        raw = raw_fixture()
        raw['categorias']['fixture'][1]['normalizacao']['campos']['altura'] = quantity(.34, 'm')
        model = consolidate(raw)
        self.assertIsNone(model['beam']['spans'][0]['geometry']['height'])

    def test_numbering_mapping_uses_evidence_not_minus_one(self):
        raw = raw_fixture()
        add_details(raw, spans=(10, 20, 30))
        raw['categorias']['fixture'].append(force('RELDTFNG.LST', 60, 20, 'Mk,neg', unit='tf,cm'))
        model = consolidate(raw)
        self.assertEqual(len(model['beam']['spans']), 1)
        span = model['beam']['spans'][0]
        self.assertEqual(span['report_span_ids']['RELDTFNG.LST'], 20)
        self.assertEqual(len(span['internal_forces']), 2)
        self.assertEqual(model['unassigned_forces'], [])

    def test_ambiguous_mapping_preserves_unassigned_forces(self):
        raw = raw_fixture()
        add_details(raw)
        next(r for r in raw['categorias']['fixture'] if r['origem']['arquivo']=='RELDTFNG.LST' and r['origem']['linha_inicial']==51)['normalizacao']['campos']['nome'] = 'P999'
        raw['categorias']['fixture'].append(force('RELDTFNG.LST', 60, 20, 'Mk,neg', unit='tf,cm'))
        model = consolidate(raw)
        self.assertNotIn('RELDTFNG.LST', model['beam']['spans'][0]['report_span_ids'])
        self.assertEqual(len(model['unassigned_forces']), 1)
        self.assertIn('span_mapping_unresolved', {w['code'] for w in model['warnings']})

    def test_force_sign_null_and_duplicate_reports(self):
        raw = raw_fixture()
        for r in raw['categorias']['fixture']:
            if (r.get('normalizacao') or {}).get('tipo') == 'serie_13_secoes':
                r['normalizacao']['valores'][3] = None
        series = consolidate(raw)['beam']['spans'][0]['internal_forces']
        self.assertEqual(len(series), 1)
        self.assertEqual(len(series[0]['sources']), 2)
        self.assertEqual(series[0]['values'][0], 0)
        self.assertIsNone(series[0]['values'][3])
        self.assertEqual(series[0]['values'][-1], -11.76798)
        self.assertIsNone(series[0]['positions'])

    def test_processing_stages_are_not_merged(self):
        raw = raw_fixture()
        add_details(raw, 'RELDTVeT.LST')
        raw['categorias']['fixture'] += [
            force('RELDTVeT.LST', 60, 20, 'V,max', section='Forcas cortantes maximas iniciais em modulo'),
            force('RELDTVeT.LST', 70, 20, 'V,max', section='Forcas cortantes finais em modulo')]
        stages = {s['stage'] for s in consolidate(raw)['beam']['spans'][0]['internal_forces']}
        self.assertEqual(stages, {'model_input', 'shear_initial_absolute', 'shear_final_absolute'})

    def test_different_series_in_same_stage_warn_and_preserve_variants(self):
        raw = raw_fixture()
        raw['categorias']['fixture'][-1]['normalizacao']['valores'][0] = quantity(1, 'tf')
        model = consolidate(raw)
        self.assertEqual(len(model['beam']['spans'][0]['internal_forces']), 2)
        self.assertIn('conflicting_force_series', {w['code'] for w in model['warnings']})

    def test_cover_zero_is_not_missing_or_automatic_override(self):
        beam = consolidate(raw_fixture())['beam']
        self.assertEqual(beam['cover']['beam_parameter'], 0)
        self.assertEqual(beam['cover']['top'], .025)
        self.assertIsNone(beam['cover']['general'])

    def test_support_conflict_is_unresolved(self):
        raw = raw_fixture()
        raw['categorias']['fixture'].append(support('RELDTFPS.LST', 50, 'P20', .24, .024))
        model = consolidate(raw)
        self.assertIsNone(next(s for s in model['beam']['supports'] if s['id']=='P20')['eccentricity'])
        self.assertTrue(any(w['path'].endswith('/eccentricity') for w in model['warnings']))

    def test_missing_reference_geometry_does_not_invent_spans(self):
        raw = raw_fixture()
        raw['categorias']['fixture'] = [r for r in raw['categorias']['fixture'] if (r.get('normalizacao') or {}).get('tipo')!='geometria_tabular']
        model = consolidate(raw)
        self.assertEqual(model['beam']['spans'], [])
        self.assertEqual(len(model['unassigned_forces']), 2)

    def test_unknown_unit_not_assumed(self):
        raw = raw_fixture()
        for r in raw['categorias']['fixture']:
            for f in r['campos_explicitos']:
                if f['chave']=='fck':
                    f.pop('normalizado')
                    f['unidade_original'] = None
        model = consolidate(raw)
        self.assertIsNone(model['beam']['materials']['concrete']['fck'])
        self.assertIn('missing_or_incompatible_unit', {w['code'] for w in model['warnings']})

    def test_provenance_pointers_resolve_without_lst(self):
        raw = raw_fixture()
        model = consolidate(raw)
        for refs in model['provenance'].values():
            for ref in refs:
                if ref.startswith('raw#'): continue
                sid, _, field = ref.partition('#')
                src = model['sources'][sid]
                target = raw
                for token in (src['raw_pointer'] + field).strip('/').split('/'):
                    target = target[int(token)] if isinstance(target, list) else target[token]
                self.assertIsNotNone(target)

    def test_cli_attribute_access_and_raw_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            raw_path, output = Path(directory)/'sample_raw.json', Path(directory)/'sample.json'
            raw_path.write_text(json.dumps(raw_fixture()), encoding='utf-8')
            before = raw_path.read_bytes()
            command = [sys.executable, str(Path(__file__).with_name('consolidar_viga.py')), str(raw_path), '--saida', str(output)]
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(load_beam(output).spans[0].geometry.height, .32)
            self.assertEqual(raw_path.read_bytes(), before)
            model = json.loads(output.read_text(encoding='utf-8'))
            self.assertEqual(model['raw_document']['sha256'], hashlib.sha256(before).hexdigest())
            self.assertLess(len(output.read_bytes()), 30000)
            command[-1] = str(raw_path)
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(raw_path.read_bytes(), before)

    def test_multiple_spans_keep_support_order_and_report_numbering(self):
        raw = raw_fixture()
        raw['categorias']['fixture'] += [
            geometry('RELDTVGS.LST', 11, 2, length=2), geometry('VGESFS.LST', 11, 2, length=2),
            support('RELDTVGS.LST', 22, 'P30', .3),
            geometry('RELDTFNG.LST', 40, 10, 0, 100, 100, 'cm'),
            geometry('RELDTFNG.LST', 41, 20, 120.6, 14, 32, 'cm'),
            geometry('RELDTFNG.LST', 42, 40, 200, 14, 32, 'cm'),
            geometry('RELDTFNG.LST', 43, 90, 0, 100, 100, 'cm'),
            support('RELDTFNG.LST', 50, 'V10', 14, unit='cm'),
            support('RELDTFNG.LST', 51, 'P20', 24, unit='cm'),
            support('RELDTFNG.LST', 52, 'P30', 30, unit='cm'),
            force('RELDTFNG.LST', 60, 40, 'Mk,neg', unit='tf,cm')]
        spans = consolidate(raw)['beam']['spans']
        self.assertEqual(len(spans), 2)
        self.assertEqual(spans[1]['geometry']['length'], 2)
        self.assertEqual(spans[1]['report_span_ids']['RELDTFNG.LST'], 40)
        self.assertEqual(spans[1]['support_ids'], ['P20', 'P30'])
        self.assertEqual(len(spans[1]['internal_forces']), 1)

    def test_nonzero_forces_on_zero_length_span_not_discarded(self):
        raw = raw_fixture()
        add_details(raw)
        raw['categorias']['fixture'].append(force('RELDTFNG.LST', 60, 10, 'Mk,neg', unit='tf,cm'))
        model = consolidate(raw)
        self.assertEqual(len(model['unassigned_forces']), 1)
        self.assertIn('nonzero_force_on_zero_length_span', {w['code'] for w in model['warnings']})

    def test_duplicate_detail_span_ids_not_mapped(self):
        raw = raw_fixture()
        add_details(raw, spans=(1, 1, 3))
        model = consolidate(raw)
        self.assertNotIn('RELDTFNG.LST', model['beam']['spans'][0]['report_span_ids'])
        self.assertIn('span_mapping_unresolved', {w['code'] for w in model['warnings']})

    def test_invalid_schema_rejected(self):
        with self.assertRaises(ValueError): consolidate({'schema_version':'99', 'categorias':{}})


if __name__ == '__main__':
    unittest.main()
