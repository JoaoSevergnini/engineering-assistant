"""Etapa 2 da ATP de vigas - entrega padrão para a seleção de João (reporting.md, "Entrega da etapa 2").

Gera, da mesma versão dos resultados:
  1. Relatório PDF de verificações de TODAS as vigas (quadro geral + ficha por viga, uma linha por região verificada),
     com coluna "Rel." (checkbox interativo, desmarcado) e campo "Comentário (etapa 3)" em cada apontamento selecionável.
  2. Cópias anotadas das pranchas de detalhamento: página 1 = prancha original com marcadores AP clicáveis;
     páginas seguintes = elevação ampliada de cada viga com faixa avaliada e quadros que indicam
     solicitação característica / resistência equivalente (Mk / (MRd/γf), Vk / (VRd2/γf), Asw/s nec. / exist.).

Uso (py -3.11 com PYTHONPATH=%LOCALAPPDATA%\\Temp\\codex-pdf-tools, somente PyMuPDF):
  py -3.11 -B emitir_etapa2.py <pasta_analise> [--rev R00]
  py -3.11 -B emitir_etapa2.py <pasta_analise> --ler <pdf_preenchido> [--registrar]
      lê checkboxes/comentários; grava emissao_etapa2_<rev>/selecao_lida.json; com --registrar grava
      selecao_enviada em selecao_etapa2.json (só quando João declarar a seleção enviada).

Contrato de entrada (organização da skill, seção 6): indice_controles.json; premissas.json; selecao_etapa2.json
(itens por seção, IDs estáveis - define a numeração AP); resultados/<lote>/manifesto.json (interval_m e seção por job);
resultados/diagnostico_e1/resumo.json (situação por viga, opcional); dados/cadastro/<V>.json (painel, apoios, estribos);
dados/detalhamento/<painel>.json (folha, x_ref_dxf, escala, contorno, barras: DXF em cm de papel = PDF);
00_entrada/detalhamentos/*<folha>*.PDF.
Nada aqui recalcula: valores vêm do índice (Concretopy). VRd2/γf = Vk/ηbiela (razão do próprio motor).
"""
from pathlib import Path
import sys, json, re, math, hashlib, datetime, collections
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8')
A = sys.argv
if len(A) < 2:
    sys.exit(__doc__)
W = Path(A[1]).resolve()
arg = lambda k, d=None: A[A.index(k) + 1] if k in A else d
REV = arg('--rev', 'R00')
ld = lambda p: json.loads((W / p).read_text(encoding='utf-8'))
IDX, P, SEL = ld('indice_controles.json'), ld('premissas.json'), ld('selecao_etapa2.json')
DIAG = ld('resultados/diagnostico_e1/resumo.json') if (W / 'resultados/diagnostico_e1/resumo.json').exists() else {'vigas': {}}
PAV, SET = IDX.get('pavimento', P.get('pavimento')), IDX.get('setor', P.get('setor'))
OUT = W / f'emissao_etapa2_{REV}'
TAG = f'ATP_{SET}_{PAV}'
HOJE = datetime.date.today()

# ---------------------------------------------------------------- numeração AP (ordem da lista da etapa 2)
AP, ITEM = {}, {}
for k in SEL['secoes']:
    for it in SEL['itens'].get(k, []):
        AP[it['id']] = f'AP-{len(AP) + 1:03d}'
        ITEM[it['id']] = dict(it, secao=k)

if '--ler' in A:  # ------------------------------------------------ leitura do PDF preenchido por João
    doc = fitz.open(arg('--ler'))
    inv = {v: k for k, v in AP.items()}
    lido = {}
    for pg in doc:
        for w in pg.widgets():
            m = re.match(r'(AP-\d+)_(rel|com)$', w.field_name or '')
            if not m:
                continue
            e = lido.setdefault(m.group(1), {'id': inv.get(m.group(1)), 'rel': False, 'comentario': ''})
            if m.group(2) == 'rel':
                e['rel'] = w.field_value not in (False, None, '', 'Off')
            else:
                e['comentario'] = (w.field_value or '').strip()
    OUT.mkdir(exist_ok=True)
    sel = {'lido_em': HOJE.isoformat(), 'pdf': str(Path(arg('--ler')).resolve()),
           'pdf_sha256': hashlib.sha256(Path(arg('--ler')).read_bytes()).hexdigest(), 'premissas_versao': P['versao'],
           'marcados': sorted([v for v in lido.values() if v['rel']], key=lambda v: v['id']),
           'comentarios_sem_marcacao': sorted([v for v in lido.values() if v['comentario'] and not v['rel']], key=lambda v: v['id'])}
    (OUT / 'selecao_lida.json').write_text(json.dumps(sel, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"campos lidos: {len(lido)}; marcados: {len(sel['marcados'])}; comentários sem marcação: {len(sel['comentarios_sem_marcacao'])}")
    if '--registrar' in A:
        SEL['selecao_enviada'] = {'data': HOJE.isoformat(), 'premissas_versao': P['versao'], 'origem': sel['pdf'],
                                  'pdf_sha256': sel['pdf_sha256'], 'ids': [v['id'] for v in sel['marcados']],
                                  'secoes': sorted({ITEM[v['id']]['secao'] for v in sel['marcados'] if v['id'] in ITEM}),
                                  'comentarios': {v['id']: v['comentario'] for v in lido.values() if v['comentario']}}
        (W / 'selecao_etapa2.json').write_text(json.dumps(SEL, ensure_ascii=False, indent=1), encoding='utf-8')
        print('selecao_enviada registrada em selecao_etapa2.json')
    sys.exit()

# ---------------------------------------------------------------- dados
num = lambda s: int(''.join(ch for ch in str(s) if ch.isdigit()) or 0)
JOBS, ANY = collections.defaultdict(dict), {}
for f in sorted(W.glob('resultados/*/manifesto.json'), key=lambda f: f.stat().st_mtime):
    for b in json.loads(f.read_text(encoding='utf-8')).get('beams', []):
        for j in b['jobs']:
            sec = (j.get('context') or {}).get('section') or {}
            JOBS[f.parent.name][j['id']] = ANY[j['id']] = {'x': j.get('interval_m'), 'b': sec.get('bw'), 'h': sec.get('h')}
CAD = {f.stem: json.loads(f.read_text(encoding='utf-8')) for f in (W / 'dados/cadastro').glob('*.json')}
DET = {f.stem: json.loads(f.read_text(encoding='utf-8')) for f in (W / 'dados/detalhamento').glob('*.json')}
CTRL = {'geometria_forma_detalhamento': 'GEOM', 'flexao_positiva': 'POS', 'flexao_negativa': 'NEG', 'armadura_minima': 'MIN',
        'cortante_estribos': 'CORT', 'suspensao': 'SUSP'}
CONTROLES = IDX['controles']
receptora = lambda c: c['id'].split('->')[1].split('/')[0] if CTRL[c['controle']] == 'SUSP' else c['viga']
D32 = set((P.get('secoes', {}).get('sensibilidade', {}) or {}).get('D32', {}).keys())


def job_info(c, job):
    rv = c.get('resultado_vigente') or {}
    lots = [rv.get('lote'), Path(rv['base_retangular']).parent.name if rv.get('base_retangular') else None]
    lots += re.findall(r'resultados/([^/]+)/', (c.get('entrada_vigente') or '').replace('\\', '/'))
    for lo in lots:
        if lo and job in JOBS.get(lo, {}):
            return JOBS[lo][job]
    return ANY.get(job, {})


f2 = lambda x, n=2: '—' if x is None else f'{x:.{n}f}'.replace('.', ',')
pct = lambda x: '—' if x is None else f'{x:.0f}%'
xi = lambda v: f'{f2(v[0])}–{f2(v[1])}' if v and len(v) == 2 and None not in v else '—'
RES = {'PASS': 'ATENDE', 'FAIL': 'NÃO ATENDE', 'INCONCLUSIVE': 'INCONCLUSIVO', 'ATENDE': 'ATENDE', 'NAO_ATENDE': 'NÃO ATENDE',
       'INCONCLUSIVO': 'INCONCLUSIVO', 'NAO_SE_APLICA': 'NÃO SE APLICA', None: '—'}


def estribo(viga, x):
    if x is None or viga not in CAD:
        return '—'
    xm = (x[0] + x[1]) / 2 * 100
    for e in CAD[viga].get('estribos', []):
        if e.get('x0_cm') is not None and e['x0_cm'] - 1 <= xm <= e['x1_cm'] + 1:
            r = e.get('ramos') or e.get('ramos_derivados')
            return f"{r or '?'}R Ø{f2(e.get('phi_mm'), 1).replace(',0', '')} c/{f2(e.get('espacamento_cm'), 0)} {'+'.join(e.get('marcas') or [])}"
    return '—'


def regioes(c):
    """Uma linha por região verificada: dict com x, valores formatados, status, governante e dados p/ quadro."""
    k = CTRL[c['controle']]
    rv = c.get('resultado_vigente') or {}
    regs = [r for r in rv.get('regioes', []) or [] if isinstance(r, dict)]
    out = []
    if k in ('POS', 'NEG'):
        for r in regs:
            ji = job_info(c, r.get('job'))
            if r.get('estado') == 'SEM_DEMANDA_DE_TRACAO':
                out.append({'job': r['job'], 'x': ji.get('x'), 'b': ji.get('b'), 'h': ji.get('h'), 'st': 'SEM DEMANDA', 'eta': None})
                continue
            out.append({'job': r.get('job'), 'x': ji.get('x'), 'b': ji.get('b'), 'h': ji.get('h'), 'As': r.get('As_cm2'), 'd': r.get('d_cm'),
                        'S': r.get('Mk_tfm'), 'R': r.get('MRd_gf_tfm'), 'eta': r.get('eta_pct'), 'Rret': r.get('MRd_gf_retangular_tfm'),
                        'st': RES.get(r.get('status'), r.get('status') or '—') if r.get('Mk_tfm') is not None else 'SEM MOMENTO'})
    elif k == 'MIN':
        for r in regs:
            ji = job_info(c, r.get('job'))
            out.append({'job': r.get('job'), 'x': ji.get('x'), 'b': ji.get('b'), 'h': ji.get('h'), 'As': r.get('As_cm2'), 'Asmin': r.get('As_min_cm2'),
                        'S': r.get('Mk_tfm'), 'R': r.get('MRd_gf_tfm'), 'st': 'ATENDE' if r.get('atende') else 'NÃO ATENDE' if r.get('atende') is False else '—',
                        'sinal': 'NEG' if 'NEG' in str(r.get('job')) else 'POS', 'eta': None})
    elif k == 'CORT':
        for r in regs:
            ji = job_info(c, r.get('job'))
            vk, bp = r.get('Vk_tf'), r.get('biela_pct')
            out.append({'job': r.get('job'), 'x': ji.get('x'), 'b': ji.get('b'), 'h': ji.get('h'), 'd': r.get('d_cm'), 'S': vk,
                        'Rb': vk / (bp / 100) if vk and bp else None, 'biela': bp, 'nec': r.get('Asw_s_nec'), 'exi': r.get('Asw_s_exist'),
                        'eta': r.get('eta_asw_pct'), 'est': estribo(c['viga'], ji.get('x')),
                        'np': ', '.join(f'{CHK.get(a, a)}: {RES.get(b, b).lower()}' for a, b in (r.get('checks_nao_pass') or {}).items() if b != 'REQUIRES_ENGINEERING_REVIEW'),
                        'st': RES.get(r.get('status'), r.get('status') or '—')})
    elif k == 'SUSP':
        for r in regs:
            segs = r.get('d26_segmentos') or r.get('subintervalos') or []
            g = max((s for s in segs if s.get('req') and s.get('exist')), key=lambda s: s['req'] / s['exist'], default={})
            out.append({'x': r.get('distribuicao_m'), 'xe': (r.get('x_eixo_cm') or 0) / 100 if r.get('x_eixo_cm') is not None else None,
                        'Rk': r.get('R_total_tf'), 'As': r.get('As_suspensao_cm2'), 'asw_s': r.get('asw_s_suspensao'), 'Ase': r.get('As_especial_cm2'),
                        'nec': g.get('req'), 'exi': g.get('exist'), 'd26': bool(r.get('d26_segmentos')), 'eta': rv.get('eta_max_pct'),
                        'st': RES.get(c.get('conclusao_tecnica'))})
    return out


CHK = {'stirrup_holder': 'porta-estribo', 'maximum_code_spacing': 's máx. normativo', 'diagonal_compression': 'biela', 'shear_reinforcement': 'taxa Asw/s',
       'provided_stirrup_area': 'área de estribo', 'number_of_legs': 'nº de ramos', 'usual_minimum_spacing': 's mín. usual', 'drawing_coverage': 'cobertura da faixa',
       'transverse_spacing': 's transversal entre ramos'}


def ordem(c):
    rs = regioes(c)
    xs = [r['x'][0] for r in rs if r.get('x') and r['x'][0] is not None]
    return (min(xs) if xs else 1e9, c['id'])


def governante(k, rs):
    if not rs:
        return None
    if k == 'MIN':
        f = [r for r in rs if r['st'] == 'NÃO ATENDE']
        return min(f, key=lambda r: (r['As'] or 0) - (r['Asmin'] or 0)) if f else rs[0]
    return max(rs, key=lambda r: (r.get('eta') is not None, r.get('eta') or 0))


def cor_item(c, rs=None):
    """vermelho: não atende; âmbar: tolerância D13 (100<η≤110) ou revisão de João; azul: geometria/documental."""
    cid = c['id'] if isinstance(c, dict) else c
    it = ITEM.get(cid, {})
    if it.get('secao') in ('GEOM', 'DOC', 'LIM'):
        return (0.13, 0.36, 0.62)
    if it.get('secao') == 'D27':
        return (0.70, 0.45, 0.0)
    e = it.get('eta_max_pct')
    return (0.70, 0.45, 0.0) if e is not None and 100 < e <= 110 else (0.72, 0.13, 0.18)


def sk_rk(c, rs):
    """Linhas do quadro da prancha: solicitação característica / resistência equivalente."""
    k = CTRL[c['controle']]
    it = ITEM.get(c['id'], {})
    g = governante(k, rs) if k != 'GEOM' else None
    mk = ' '.join(str(m) for m in (c.get('resultado_vigente') or {}).get('marcas') or [])
    L = []
    if k in ('POS', 'NEG') and g:
        L.append(f"Mk / (MRd/γf) = {f2(g.get('S'))} / {f2(g.get('R'))} tf·m  →  ηM = {pct(g.get('eta'))}")
        L.append(f"As = {f2(g.get('As'))} cm²; d = {f2(g.get('d'), 1)} cm; seção {f2(g.get('b'), 0)}×{f2(g.get('h'), 0)}; x = {xi(g.get('x'))} m")
        if g.get('Rret'):
            L.append(f"seção T (mesa colaborante); retangular: MRd/γf = {f2(g['Rret'])} tf·m")
        if g.get('eta') and 100 < g['eta'] <= 110:
            L.append('faixa de tolerância 100% < η ≤ 110% (D13)')
    elif k == 'MIN' and g:
        L.append(f"As,exist / As,mín = {f2(g.get('As'))} / {f2(g.get('Asmin'))} cm² ({'negativa' if g['sinal'] == 'NEG' else 'positiva'})")
        L.append(f"Mk / (MRd/γf) = {f2(g.get('S'))} / {f2(g.get('R'))} tf·m; x = {xi(g.get('x'))} m")
    elif k == 'CORT' and g:
        if 'D29' in mk:
            L.append('Ramo interno de estribo sem barra longitudinal no canto (D29).')
        L.append(f"Vk / (VRd2/γf) = {f2(g.get('S'))} / {f2(g.get('Rb'))} tf  →  biela {pct(g.get('biela'))}")
        L.append(f"Asw/s nec. / exist. = {f2(g.get('nec'))} / {f2(g.get('exi'))} cm²/m  →  ηAsw = {pct(g.get('eta'))}")
        L.append(f"Estribo: {g.get('est')}; x = {xi(g.get('x'))} m" + (f"; {g['np']}" if g.get('np') else ''))
    elif k == 'SUSP' and g:
        if it.get('secao') == 'D27':
            L.append(f"Rk = {f2(g.get('Rk'))} tf; As,ref (100% da reação) = {f2(g.get('Ase'))} cm²")
            L.append('Suspensão especial: verificação posterior por João (D27).')
        else:
            L.append(f"Rk = {f2(g.get('Rk'))} tf → As,susp = {f2(g.get('As'))} cm² (Asw/s susp. = {f2(g.get('asw_s'))} cm²/m)")
            L.append(f"Asw/s nec. (cortante + suspensão) / exist. = {f2(g.get('nec'))} / {f2(g.get('exi'))} cm²/m  →  η = {pct(g.get('eta'))}")
            L.append(f"Distribuição x = {xi(g.get('x'))} m" + ('; taxas somadas na sobreposição (D26)' if g.get('d26') else ''))
    return L


# por viga
VIGAS = sorted({c['viga'] for c in CONTROLES} | {receptora(c) for c in CONTROLES}, key=num)
POR_VIGA = collections.defaultdict(list)
for c in CONTROLES:
    POR_VIGA[receptora(c) if CTRL[c['controle']] == 'SUSP' else c['viga']].append(c)
DOC_VIGA = collections.defaultdict(list)
for i, it in ITEM.items():
    if it['secao'] == 'DOC' and not any(x['id'] == i for x in CONTROLES):
        DOC_VIGA[it['viga']].append(it)

# ================================================================ PDF helpers
FR, FB = 'C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf'
FONT = {'r': fitz.Font(fontfile=FR), 'b': fitz.Font(fontfile=FB)}
NAVY, BLUE, GRID, ZEBRA, TXT = (0.09, 0.24, 0.31), (0.16, 0.33, 0.42), (0.80, 0.85, 0.87), (0.95, 0.97, 0.98), (0.12, 0.19, 0.23)
COR_ST = {'NÃO ATENDE': (0.72, 0.13, 0.18), 'ATENDE': (0.12, 0.45, 0.25), 'INCONCLUSIVO': (0.70, 0.45, 0.0),
          'IMPEDIMENTO': (0.45, 0.45, 0.45), 'REVISÃO JOÃO': (0.70, 0.45, 0.0)}


def fonts(pg):
    pg.insert_font(fontname='ar', fontfile=FR)
    pg.insert_font(fontname='ab', fontfile=FB)


def wrap(t, w, fs, f='r'):
    out = []
    for par in str(t).split('\n'):
        line = ''
        for wd in par.split(' '):
            cand = (line + ' ' + wd).strip()
            if FONT[f].text_length(cand, fontsize=fs) <= w or not line:
                line = cand
            else:
                out.append(line)
                line = wd
        out.append(line)
    return out


def put(pg, x, y, lines, fs, f='r', color=TXT, lead=1.22):
    for i, ln in enumerate(lines):
        pg.insert_text((x, y + fs + i * fs * lead), ln, fontname='ab' if f == 'b' else 'ar', fontsize=fs, color=color)
    return len(lines) * fs * lead


class Relatorio:
    W_, H_, M = 842, 595, 28

    def __init__(self):
        self.doc = fitz.open()
        self.pg, self.y, self.n = None, 0, 0
        self.links, self.toc, self.beam_page = [], [], {}
        self.titulo = ''

    def footer(self):
        p = self.pg
        p.draw_line((self.M, self.H_ - 24), (self.W_ - self.M, self.H_ - 24), color=GRID, width=0.6)
        put(p, self.M, self.H_ - 20, [f'{SET} | {PAV} | ATP DE VIGAS — VERIFICAÇÕES PARA SELEÇÃO (ETAPA 2) {REV} | {HOJE:%d/%m/%Y} | '
                                      'Não constitui conclusão global nem relatório de emissão'], 6.5, color=(0.3, 0.38, 0.43))
        p.insert_text((self.W_ - self.M - 20, self.H_ - 13.5), str(self.n), fontname='ar', fontsize=6.5, color=(0.3, 0.38, 0.43))

    def new(self, titulo, sub='Verificações de todas as vigas — selecione os apontamentos na coluna "Rel." e comente para a etapa 3'):
        if self.pg:
            self.footer()
        self.pg = self.doc.new_page(width=self.W_, height=self.H_)
        fonts(self.pg)
        self.n += 1
        self.titulo = titulo
        self.pg.draw_rect(fitz.Rect(0, 0, self.W_, 50), color=None, fill=NAVY)
        put(self.pg, self.M, 9, [titulo], 15, 'b', (1, 1, 1))
        put(self.pg, self.M, 31, [sub], 7.5, color=(0.85, 0.9, 0.93))
        self.y = 62

    def text(self, t, fs=8, f='r', color=TXT, gap=5):
        lines = wrap(t, self.W_ - 2 * self.M, fs, f)
        h = len(lines) * fs * 1.22
        if self.y + h > self.H_ - 34:
            self.new(self.titulo.split(' (cont.)')[0] + ' (cont.)')
        put(self.pg, self.M, self.y, lines, fs, f, color)
        self.y += h + gap

    def table(self, title, cols, rows, fs=6.6):
        """cols: [(cabeçalho, largura relativa)]; rows: dict(cells=[...], ap=id|None, bold=bool, color={i: rgb})."""
        tw = self.W_ - 2 * self.M
        ws = [tw * w / sum(w for _, w in cols) for _, w in cols]

        def rh(cells, f):
            return max(max(len(wrap(c, w - 6, fs, f)) for c, w in zip(cells, ws)) * fs * 1.22 + 6, 15)
        hh = rh([c for c, _ in cols], 'b')
        need = (fs + 8 if title else 0) + hh + (rh(rows[0]['cells'], 'r') if rows else 0)
        if self.y + need > self.H_ - 34:
            self.new(self.titulo.split(' (cont.)')[0] + ' (cont.)')
        if title:
            put(self.pg, self.M, self.y, [title], fs + 1.6, 'b', NAVY)
            self.y += fs + 8

        def header():
            x = self.M
            self.pg.draw_rect(fitz.Rect(self.M, self.y, self.M + tw, self.y + hh), color=None, fill=BLUE)
            for (c, _), w in zip(cols, ws):
                put(self.pg, x + 3, self.y + 2.5, wrap(c, w - 6, fs, 'b'), fs, 'b', (1, 1, 1))
                x += w
            self.y += hh
        header()
        for i, r in enumerate(rows):
            h = rh(r['cells'], 'b' if r.get('bold') else 'r')
            if r.get('ap'):
                h = max(h, 22)
            if self.y + h > self.H_ - 34:
                self.new(self.titulo.split(' (cont.)')[0] + ' (cont.)')
                header()
            x = self.M
            fill = (1.0, 0.97, 0.90) if r.get('ap') else (ZEBRA if i % 2 else (1, 1, 1))
            self.pg.draw_rect(fitz.Rect(self.M, self.y, self.M + tw, self.y + h), color=None, fill=fill)
            for j, (c, w) in enumerate(zip(r['cells'], ws)):
                col = (r.get('color') or {}).get(j, TXT)
                put(self.pg, x + 3, self.y + 3, wrap(c, w - 6, fs, 'b' if r.get('bold') else 'r'), fs, 'b' if r.get('bold') else 'r', col)
                self.pg.draw_rect(fitz.Rect(x, self.y, x + w, self.y + h), color=GRID, width=0.4)
                x += w
            if r.get('ap'):
                self.widgets(r['ap'], ws, h)
            if r.get('link'):
                self.links.append((self.n - 1, fitz.Rect(self.M, self.y, self.M + ws[0], self.y + h), r['link']))
            self.y += h
        self.y += 8

    def widgets(self, cid, ws, h):
        code = AP[cid]
        x_rel = self.M  # coluna 0 = Rel.
        cb = fitz.Widget()
        cb.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
        cb.field_name, cb.field_label, cb.field_value = f'{code}_rel', f'{code} {cid}', False
        s = 10
        cb.rect = fitz.Rect(x_rel + ws[0] / 2 - s / 2, self.y + h / 2 - s / 2, x_rel + ws[0] / 2 + s / 2, self.y + h / 2 + s / 2)
        cb.border_color, cb.border_width, cb.fill_color = (0.2, 0.2, 0.2), 0.8, (1, 1, 1)
        self.pg.add_widget(cb)
        xc = self.M + sum(ws[:-1])
        tx = fitz.Widget()
        tx.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        tx.field_name, tx.field_label, tx.field_value = f'{code}_com', f'Comentário {code} ({cid})', ''
        tx.field_flags = fitz.PDF_TX_FIELD_IS_MULTILINE
        tx.text_fontsize, tx.text_font = 6.5, 'Helv'
        tx.rect = fitz.Rect(xc + 1.5, self.y + 1.5, xc + ws[-1] - 1.5, self.y + h - 1.5)
        tx.border_color, tx.border_width, tx.fill_color = (0.62, 0.70, 0.74), 0.5, (1, 1, 1)
        self.pg.add_widget(tx)

    def close(self, path):
        self.footer()
        for pno, rect, beam in self.links:
            if beam in self.beam_page:
                self.doc[pno].insert_link({'kind': fitz.LINK_GOTO, 'from': rect, 'page': self.beam_page[beam], 'to': fitz.Point(0, 0)})
        self.doc.set_toc(self.toc)
        self.doc.set_metadata({'title': f'{TAG} - verificações para seleção (etapa 2) {REV}', 'author': 'Auxiliar de Engenharia - revisão de João',
                               'subject': f'premissas v{P["versao"]}'})
        self.doc.save(path, garbage=3, deflate=True)


# ================================================================ relatório
SIT = {'NAO_ATENDE': 'NÃO ATENDE', 'ATENDE': 'ATENDE', 'REVISAO_JOAO': 'REVISÃO JOÃO', 'IMPEDIMENTO': 'IMPEDIMENTO', None: '—'}


def st_ctrl(c):
    if c['estado_execucao'] == 'IMPEDIMENTO_DOCUMENTAL':
        return 'IMPEDIMENTO'
    if CTRL[c['controle']] == 'SUSP' and c['id'] in ITEM and ITEM[c['id']]['secao'] == 'D27':
        return 'REVISÃO JOÃO'
    return RES.get(c.get('conclusao_tecnica'), c.get('conclusao_tecnica') or '—')


def agg(cs):
    if not cs:
        return '—'
    s = [st_ctrl(c) for c in cs]
    n = s.count('NÃO ATENDE')
    if n:
        return f'NÃO ATENDE ({n})'
    for k in ('IMPEDIMENTO', 'REVISÃO JOÃO', 'INCONCLUSIVO'):
        if k in s:
            return f'{k} ({s.count(k)})'
    return 'ATENDE' if 'ATENDE' in s else s[0]


def rel_cell(cid):
    return [AP[cid] if cid in AP else '', ]


def gerar_relatorio():
    R = Relatorio()
    R.new(f'ATP de vigas — {SET} {PAV}: verificações para seleção (etapa 2) {REV}')
    R.toc.append([1, 'Abertura e convenções', 1])
    nc = len(CONTROLES)
    R.text(f"Obra: {P.get('obra', '')}. Projeto {P.get('projeto', '')}.", 8.5, 'b')
    R.text(f"Abrangência: {len(VIGAS)} vigas; {nc} controles (geometria, flexão positiva e negativa, armadura mínima, cortante/estribos e suspensão). "
           f"Resultados vigentes de indice_controles.json (premissas v{P['versao']}); lista de apontamentos de selecao_etapa2.json ({len(AP)} itens, AP-001 a AP-{len(AP):03d}). "
           f"Fontes: forma {P['fontes'].get('formas', {}).get('revisao', '')}; detalhamentos {', '.join(f'{k} {v}' for k, v in P['fontes'].get('detalhamentos', {}).get('pranchas', {}).items())}.")
    R.text('COMO USAR ESTE RELATÓRIO. Cada apontamento selecionável (linha com fundo creme e código AP) tem uma caixa na coluna "Rel." e um campo "Comentário (etapa 3)". '
           'Marque a caixa dos itens que devem ir para o relatório de emissão e escreva no campo o que orientar a redação (solução esperada, agrupamento, tom, item a omitir). '
           'Todas as caixas começam desmarcadas; caixa desmarcada não é decisão. Salve o PDF (Acrobat, Foxit ou Edge) e me devolva: os campos são lidos por código e registrados em selecao_etapa2.json. '
           'As pranchas anotadas (pasta PRANCHAS_ANOTADAS) usam os mesmos códigos AP e mostram a posição e os valores de cada apontamento.', 8, 'b', NAVY)
    R.text(f"Norma: {P['norma']['referencia']}. Materiais: fck = {P['materiais']['concreto']['fck_MPa']} MPa; {P['materiais']['aco']['classe']} (fyk = {P['materiais']['aco']['fyk_MPa']} MPa); "
           f"cobrimento {f2(P['cobrimento']['vigas_cm'], 1)} cm. γf = {f2(P['coeficientes']['gamma_f']['valor'], 1)} ({P['coeficientes']['gamma_f']['origem']}); γc = {f2(P['coeficientes']['gamma_c'], 1)}; γs = {f2(P['coeficientes']['gamma_s'], 2)}. "
           f"Esforços: {P['esforcos']['fonte']}, natureza {P['esforcos']['natureza']}.")
    R.text('Apresentação: solicitações características em tf e tf·m (Mk, Vk, Rk). Resistências apresentadas como equivalente para comparação Rd/γf (MRd/γf; VRd2/γf), não como resistência característica; '
           'a verificação de segurança permanece na base de cálculo. Resultado oficial: Concretopy (floor_review, verificadores de flexão, cortante e suspensão), registrado no índice; este relatório não recalcula.')
    R.text('Índices: ηM = 100·Mk/(MRd/γf) — 120% significa solicitação 20% acima da resistência equivalente, não 20% de aço faltante. ηAsw = 100·(Asw/s necessário)/(Asw/s existente), incluindo o mínimo quando governante. '
           'Biela = 100·Vk/(VRd2/γf), separada da armadura; VRd2/γf é obtido pela razão do próprio motor (Vk/ηbiela). Suspensão: η = taxa necessária (cortante calculado + suspensão, ou mínimo) / taxa existente. '
           'Amarelo: 100% < η ≤ 110% (faixa de tolerância D13), vermelho: não atende, azul: geometria/documental. "SEM DEMANDA": trecho sem momento de tração do sinal.')
    R.text('Escopo e limites: ' + '; '.join(e['item'] + (f" — {e['efeito']}" if e.get('efeito') else '') for e in P['escopo'].get('exclusoes', [])) +
           '. Furos verificados com seção plena (D14). Positiva sem contribuição das barras superiores. Negativa com o máximo do TQS de cada lado do apoio, sem redução à face.')

    # quadro geral
    R.new('Quadro geral por viga')
    R.toc.append([1, 'Quadro geral por viga', R.n])
    R.text('Situação por disciplina no escopo (número de controles que não atendem entre parênteses). Clique na viga para abrir a ficha. Suspensão: a viga como receptora.', 7.5)
    rows = []
    for v in VIGAS:
        cs = POR_VIGA[v]
        by = lambda k: [c for c in cs if CTRL[c['controle']] == k]
        sit = (DIAG.get('vigas', {}).get(v, {}) or {}).get('situacao_escopo') or ('IMPEDIMENTO' if any(c['estado_execucao'] == 'IMPEDIMENTO_DOCUMENTAL' for c in cs) else '—')
        nap = sum(1 for c in cs if c['id'] in AP) + len(DOC_VIGA.get(v, []))
        cells = [v, (CAD.get(v, {}).get('painel') or '—').split('_')[0], agg(by('GEOM')), agg(by('POS')), agg(by('NEG')), agg(by('MIN')), agg(by('CORT')),
                 agg(by('SUSP')), SIT.get(sit, sit.replace('_', ' ')), str(nap or '—')]
        rows.append({'cells': cells, 'link': v, 'color': {j: COR_ST.get(cells[j].split(' (')[0], TXT) for j in range(2, 9)} | {0: BLUE}})
    R.table(None, [('Viga', .5), ('Folha', .5), ('Geometria', 1), ('Positiva', 1), ('Negativa', 1), ('Mínimo', 1), ('Cortante', 1), ('Suspensão (receptora)', 1.1),
                   ('Situação no escopo', 1), ('Apont.', .45)], rows)

    # registros gerais (LIM e DOC sem viga)
    R.new('Registros gerais — escopo, limitações e documentais')
    R.toc.append([1, 'Registros gerais', R.n])
    rows = [{'cells': ['', AP[i], it['viga'], it['local'], it['problema'], ''], 'ap': i} for i, it in ITEM.items() if it['secao'] == 'LIM' or (it['secao'] == 'DOC' and it['viga'] not in VIGAS)]
    R.table('Itens gerais (selecionáveis)', [('Rel.', .35), ('AP', .5), ('Viga', .45), ('Local', 1.2), ('Registro', 5.2), ('Comentário (etapa 3)', 2.2)], rows)

    # fichas
    for v in VIGAS:
        cs = POR_VIGA[v]
        cad = CAD.get(v, {})
        R.new(f'{v} — ficha de verificação', f"Painel {cad.get('painel', '—')} | apoios: {' / '.join(a['nome'] for a in cad.get('apoios', [])) or '—'} | "
                                            f"situação no escopo: {SIT.get((DIAG.get('vigas', {}).get(v) or {}).get('situacao_escopo'), '—')}")
        R.beam_page[v] = R.n - 1
        R.toc.append([1, v, R.n])
        if v in D32:
            R.text(f'D32: as falhas desta viga ficam consolidadas no apontamento de geometria ({", ".join(AP[c["id"]] for c in cs if c["id"] in AP and CTRL[c["controle"]] == "GEOM")}). '
                   'Os controles abaixo usam a seção do detalhamento (25×71) e os esforços TQS; a sensibilidade com 40×61 está no texto do apontamento.', 7.5, 'b', (0.13, 0.36, 0.62))
        # geometria + documentais
        rows = []
        for c in [c for c in cs if CTRL[c['controle']] == 'GEOM']:
            rv = c.get('resultado_vigente') or {}
            t = ITEM[c['id']]['problema'] if c['id'] in ITEM else '; '.join((rv.get('apontamentos') or []) + (rv.get('limitacoes') or [])) or 'seções, vãos e apoios conferidos'
            if c['estado_execucao'] == 'IMPEDIMENTO_DOCUMENTAL':
                t = c.get('obstaculo') or t
            rows.append({'cells': ['', AP.get(c['id'], ''), 'Geometria forma × detalhamento', st_ctrl(c), t, ''], 'ap': c['id'] if c['id'] in AP else None,
                         'color': {3: COR_ST.get(st_ctrl(c), TXT)}})
        for c in [c for c in cs if c['estado_execucao'] == 'IMPEDIMENTO_DOCUMENTAL' and CTRL[c['controle']] != 'GEOM' and c['id'] in AP]:
            rows.append({'cells': ['', AP[c['id']], c['local'], 'IMPEDIMENTO', c.get('obstaculo') or '', ''], 'ap': c['id']})
        for it in DOC_VIGA.get(v, []):
            rows.append({'cells': ['', AP[it['id']], it['local'], it['conclusao'].replace('_', ' '), it['problema'], ''], 'ap': it['id'], 'color': {3: (0.13, 0.36, 0.62)}})
        if rows:
            R.table('Geometria e registros documentais', [('Rel.', .35), ('AP', .5), ('Item', 1.4), ('Resultado', .9), ('Constatação', 5.0), ('Comentário (etapa 3)', 2.2)], rows)
        # flexão
        for k, tit in (('POS', 'Flexão positiva'), ('NEG', 'Flexão negativa — cada lado do apoio')):
            rows = []
            for c in sorted([c for c in cs if CTRL[c['controle']] == k], key=ordem):
                rs = regioes(c)
                g = governante(k, rs)
                if c['estado_execucao'] == 'IMPEDIMENTO_DOCUMENTAL' or not rs:
                    rows.append({'cells': ['', AP.get(c['id'], ''), c['local'], '—', '—', '—', '—', '—', '—', '—', st_ctrl(c) + (': ' + (c.get('obstaculo') or '') if c.get('obstaculo') else ''), ''],
                                 'ap': c['id'] if c['id'] in AP else None})
                    continue
                for i, r in enumerate(rs):
                    first = i == 0
                    e = r.get('eta')
                    cor = (0.72, 0.13, 0.18) if r['st'] == 'NÃO ATENDE' and not (e and e <= 110) else (0.70, 0.45, 0.0) if r['st'] == 'NÃO ATENDE' else TXT
                    rows.append({'cells': ['', AP.get(c['id'], '') if first else '', (c['local'] + '\n' if first else '') + (r.get('job') or ''), xi(r.get('x')),
                                           f"{f2(r.get('b'), 0)}×{f2(r.get('h'), 0)}" if r.get('b') else '—', f2(r.get('As')), f2(r.get('d'), 1), f2(r.get('S')), f2(r.get('R')),
                                           pct(e), r['st'] + (' (seção T)' if r.get('Rret') else ''), ''],
                                 'ap': c['id'] if first and c['id'] in AP else None, 'bold': r is g and c['id'] in AP and len(rs) > 1, 'color': {9: cor, 10: cor}})
            if rows:
                R.table(tit, [('Rel.', .35), ('AP', .5), ('Local / região', 1.5), ('x (m)', .75), ('b×h cm', .55), ('As cm²', .5), ('d cm', .45), ('Mk tf·m', .55),
                              ('MRd/γf tf·m', .6), ('ηM', .45), ('Resultado', .95), ('Comentário (etapa 3)', 2.0)], rows)
        # mínimo
        rows = []
        for c in sorted([c for c in cs if CTRL[c['controle']] == 'MIN'], key=ordem):
            rs = regioes(c)
            g = governante('MIN', rs)
            if not g:
                rows.append({'cells': ['', AP.get(c['id'], ''), c['local'], '—', '—', '—', '—', st_ctrl(c), ''], 'ap': c['id'] if c['id'] in AP else None})
                continue
            nf = sum(1 for r in rs if r['st'] == 'NÃO ATENDE')
            rows.append({'cells': ['', AP.get(c['id'], ''), c['local'] + f"\n{g.get('job')}", xi(g.get('x')), f2(g.get('As')), f2(g.get('Asmin')),
                                   f"{len(rs)} regiões; {nf} abaixo do mínimo" + (' (dispensado pela D19: momento pequeno)' if 'MIN_DISPENSADO_D19' in ' '.join(map(str, (c.get('resultado_vigente') or {}).get('marcas') or [])) and st_ctrl(c) == 'ATENDE' else '') if nf else f'{len(rs)} regiões', st_ctrl(c), ''],
                         'ap': c['id'] if c['id'] in AP else None, 'color': {7: COR_ST.get(st_ctrl(c), TXT)}})
        if rows:
            R.table('Armadura mínima de flexão (região governante)', [('Rel.', .35), ('AP', .5), ('Local / região governante', 1.9), ('x (m)', .75), ('As cm²', .55),
                                                                         ('As,mín cm²', .6), ('Regiões', 1.3), ('Resultado', .9), ('Comentário (etapa 3)', 2.0)], rows)
        # cortante
        rows = []
        for c in sorted([c for c in cs if CTRL[c['controle']] == 'CORT'], key=ordem):
            rs = regioes(c)
            mk = ' '.join(str(m) for m in (c.get('resultado_vigente') or {}).get('marcas') or [])
            if not rs:
                rows.append({'cells': ['', AP.get(c['id'], ''), c['local'], '—', '—', '—', '—', '—', '—', '—', '—', '—', st_ctrl(c) + (': ' + c['obstaculo'] if c.get('obstaculo') else ''), ''],
                             'ap': c['id'] if c['id'] in AP else None})
                continue
            for i, r in enumerate(rs):
                first = i == 0
                obs = (f"{st_ctrl(c)} (controle)" + (' — D29: ramo interno sem barra no canto' if 'D29' in mk else '') + '; região: ' if first and c['id'] in AP else '') + r['st'] + (f" ({r['np']})" if r.get('np') else '')
                rows.append({'cells': ['', AP.get(c['id'], '') if first else '', (c['local'] + '\n' if first else '') + (r.get('job') or ''), xi(r.get('x')), r.get('est'),
                                       f2(r.get('d'), 1), f2(r.get('S')), f2(r.get('Rb')), pct(r.get('biela')), f2(r.get('nec')), f2(r.get('exi')), pct(r.get('eta')), obs, ''],
                             'ap': c['id'] if first and c['id'] in AP else None, 'color': {12: COR_ST.get(r['st'], TXT)}})
        if rows:
            R.table('Cortante e estribos — taxas em cm²/m', [('Rel.', .35), ('AP', .5), ('Local / faixa', 1.45), ('x (m)', .75), ('Estribo desenhado', 1.0), ('d cm', .42),
                                                            ('Vk tf', .45), ('VRd2/γf tf', .55), ('Biela', .42), ('Asw/s nec.', .5), ('Asw/s exist.', .5), ('ηAsw', .42),
                                                            ('Resultado', 1.25), ('Comentário (etapa 3)', 1.8)], rows)
        # suspensão (receptora)
        rows = []
        for c in sorted([c for c in cs if CTRL[c['controle']] == 'SUSP'], key=ordem):
            rs = regioes(c)
            lig = c['id'].split('/SUSP/')[1]
            if not rs or c['estado_execucao'] == 'IMPEDIMENTO_DOCUMENTAL':
                rows.append({'cells': ['', AP.get(c['id'], ''), lig, '—', '—', '—', '—', '—', '—', st_ctrl(c) + (': ' + c['obstaculo'] if c.get('obstaculo') else ''), ''],
                             'ap': c['id'] if c['id'] in AP else None})
                continue
            r = rs[0]
            d27 = c['id'] in ITEM and ITEM[c['id']]['secao'] == 'D27'
            rows.append({'cells': ['', AP.get(c['id'], ''), lig, f2(r.get('xe')), f2(r.get('Rk')), f2(r.get('Ase') if d27 else r.get('As')) + (' (ref. 100%)' if d27 else ''),
                                   xi(r.get('x')), f"{f2(r.get('nec'))} / {f2(r.get('exi'))}", pct(r.get('eta')),
                                   st_ctrl(c) + (' — D26 (sobreposição)' if r.get('d26') else ''), ''],
                         'ap': c['id'] if c['id'] in AP else None, 'color': {9: COR_ST.get(st_ctrl(c), TXT)}})
        if rows:
            R.table('Suspensão — viga como receptora (cortante + suspensão)', [('Rel.', .35), ('AP', .5), ('Apoiada → receptora / apoio', 1.6), ('x eixo m', .55), ('Rk tf', .5),
                                                                                ('As,susp cm²', .75), ('Distribuição x (m)', .85), ('Asw/s nec. / exist. cm²/m', 1.1),
                                                                                ('η', .42), ('Resultado', 1.4), ('Comentário (etapa 3)', 2.0)], rows)
        if not cs and not DOC_VIGA.get(v):
            R.text('Sem controles registrados para esta viga.')
    OUT.mkdir(exist_ok=True)
    path = OUT / f'{TAG}_VERIFICACOES_SELECAO_ETAPA2_{REV}.pdf'
    R.close(path)
    return path, R.n


# ================================================================ pranchas
K = 72 / 2.54  # cm de papel -> pt


def niveis(D):
    tot = collections.defaultdict(float)
    xs = [e['x0_cm'] for e in D.get('contorno', [])] + [e['x1_cm'] for e in D.get('contorno', [])]
    if not xs:
        return D['faixa_y_contorno_dxf'][1], D['faixa_y_contorno_dxf'][0]
    L = max(xs) - min(xs)
    for e in D['contorno']:
        tot[round(e['y_dxf'], 3)] += e['x1_cm'] - e['x0_cm']
    cand = [y for y, s in tot.items() if s >= 0.25 * L] or list(tot)
    return max(cand), min(cand)


def posicoes():
    """Para cada apontamento localizável: folha, painel, x_dxf, y_dxf, intervalo (x0,x1 em dxf)."""
    pos = {}
    for cid, it in ITEM.items():
        if it['secao'] == 'LIM':
            continue
        v = it['viga']
        cad = CAD.get(v)
        if not cad or cad.get('painel') not in DET:
            continue
        D = DET[cad['painel']]
        esc, xr = D.get('escala', 50.0), D['x_ref_dxf']
        top, bot = niveis(D)
        c = next((x for x in CONTROLES if x['id'] == cid), None)
        x = None
        y = top
        if c and CTRL[c['controle']] != 'GEOM' and c['estado_execucao'] != 'IMPEDIMENTO_DOCUMENTAL':
            k = CTRL[c['controle']]
            rs = regioes(c)
            g = governante(k, rs)
            if g:
                x = g.get('x')
                if k == 'SUSP' and g.get('xe') is not None:
                    x = x or [g['xe'], g['xe']]
                y = {'NEG': top, 'POS': bot, 'CORT': (top + bot) / 2, 'SUSP': top - 0.3 * (top - bot)}.get(k, top if g.get('sinal') == 'NEG' else bot)
        elif it['secao'] == 'DOC':
            m = re.search(r'x≈\s*(\d+(?:[.,]\d+)?)(?:\s*[–-]\s*(\d+(?:[.,]\d+)?))?\s*cm', it['local'])
            if m:
                a = float(m.group(1).replace(',', '.')) / 100
                x = [a, float(m.group(2).replace(',', '.')) / 100 if m.group(2) else a]
                y = bot if 'inferior' in it['local'] else top
        if x is None or None in x:
            x0 = x1 = xr + 0.5
            y = top + 1.2
        else:
            x0, x1 = xr + x[0] * 100 / esc, xr + x[1] * 100 / esc
        pos[cid] = {'folha': str(D.get('folha')), 'painel': cad['painel'], 'x0': x0, 'x1': x1, 'y': y, 'top': top, 'bot': bot, 'D': D}
    return pos


def rotulo(ocup, x, y, w, h):
    """Retângulo do rótulo sem sobrepor os já colocados (sobe em degraus)."""
    r = fitz.Rect(x, y, x + w, y + h)
    for _ in range(12):
        if not any(r.intersects(o) for o in ocup):
            break
        r = fitz.Rect(r.x0, r.y0 - h - 1, r.x1, r.y1 - h - 1)
    ocup.append(r)
    return r


def gerar_pranchas():
    pos = posicoes()
    od = OUT / f'PRANCHAS_ANOTADAS_ETAPA2_{REV}'
    od.mkdir(parents=True, exist_ok=True)
    feitos, sem = [], [i for i, it in ITEM.items() if it['secao'] != 'LIM' and i not in pos]
    folhas = sorted({p['folha'] for p in pos.values()})
    for fo in folhas:
        src_path = next(p for p in (W / '00_entrada/detalhamentos').glob('*.PDF') if f'-{fo}-' in p.name)
        src = fitz.open(src_path)
        doc = fitz.open()
        doc.insert_pdf(src)
        ov = doc[0]
        fonts(ov)
        SH = ov.rect.height
        its = sorted([i for i, p in pos.items() if p['folha'] == fo], key=lambda i: (num(AP[i]),))
        paineis = sorted({pos[i]['painel'] for i in its}, key=lambda p: num(p.split('_', 1)[1]))
        page_of, links = {}, []
        for pa in paineis:
            D = DET[pa]
            esc, xr = D.get('escala', 50.0), D['x_ref_dxf']
            Lp = max([e['x1_cm'] for e in D.get('contorno', [])] or [0]) / esc
            ys = [b['y_dxf'] for b in D.get('barras', [])] + [D['faixa_y_contorno_dxf'][0]]
            top, bot = niveis(D)
            y_lo, y_hi = max(min(ys) - 1.2, bot - 9), D['faixa_y_contorno_dxf'][1] + 2.2
            seg_n = max(1, math.ceil((Lp + 2) / 42))
            seg_w = (Lp + 2) / seg_n
            pi = [i for i in its if pos[i]['painel'] == pa]
            for s in range(seg_n):
                sx0 = xr - 1 + s * seg_w
                sx1 = sx0 + seg_w
                si = [i for i in pi if sx0 <= (pos[i]['x0'] + pos[i]['x1']) / 2 < sx1 or (s == seg_n - 1 and (pos[i]['x0'] + pos[i]['x1']) / 2 >= sx1) or
                      (s == 0 and (pos[i]['x0'] + pos[i]['x1']) / 2 < sx0)]
                if not si:
                    continue
                for b0 in range(0, len(si), 8):
                    bloco = si[b0:b0 + 8]
                    pg = doc.new_page(width=1190.55, height=841.89)
                    fonts(pg)
                    pno = pg.number
                    for i in bloco:
                        page_of.setdefault(i, pno)
                    PW, PH = pg.rect.width, pg.rect.height
                    pg.draw_rect(fitz.Rect(0, 0, PW, 52), color=None, fill=NAVY)
                    vig = D.get('titulo') or pa.split('_', 1)[1]
                    put(pg, 30, 9, [f'{vig} — localização dos apontamentos' + (f' (trecho {s + 1}/{seg_n})' if seg_n > 1 else '')], 16, 'b', (1, 1, 1))
                    put(pg, 30, 32, [f"Prancha {fo} | {', '.join(AP[i] for i in bloco)} | marcador no elemento; barra colorida = faixa avaliada; "
                                     f"quadro = solicitação característica / resistência equivalente"], 8.5, color=(0.85, 0.9, 0.93))
                    clip = fitz.Rect(sx0 * K, SH - y_hi * K, sx1 * K, SH - y_lo * K)
                    aw, ah = PW - 60, 430
                    sc = min(aw / clip.width, ah / clip.height)
                    tgt = fitz.Rect(30, 62, 30 + clip.width * sc, 62 + clip.height * sc)
                    pg.show_pdf_page(tgt, src, 0, clip=clip)
                    pg.draw_rect(tgt, color=GRID, width=0.6)
                    T = lambda xd, yd: fitz.Point(tgt.x0 + (xd * K - clip.x0) * sc, tgt.y0 + ((SH - yd * K) - clip.y0) * sc)
                    bw, bh, gap = (PW - 60 - 3 * 12) / 4, 128, 12
                    by0 = max(tgt.y1 + 40, 520) if len(bloco) <= 4 else tgt.y1 + 34
                    if by0 + (2 if len(bloco) > 4 else 1) * (bh + gap) > PH - 36:
                        bh = (PH - 36 - by0) / (2 if len(bloco) > 4 else 1) - gap
                    ocup = []
                    for n_, i in enumerate(bloco):
                        p = pos[i]
                        col = cor_item(i)
                        a, b = T(p['x0'], p['y']), T(p['x1'], p['y'])
                        if b.x - a.x > 2:
                            pg.draw_line(a, b, color=col, width=2.2)
                        m = fitz.Point((a.x + b.x) / 2, a.y)
                        pg.draw_circle(m, 4.5, color=col, width=1.2)
                        rl = rotulo(ocup, m.x + 5, m.y - 13, FONT['b'].text_length(AP[i], fontsize=7) + 2, 10)
                        put(pg, rl.x0, rl.y0, [AP[i]], 7, 'b', col)
                        if rl.y0 < m.y - 14:
                            pg.draw_line(m, fitz.Point(rl.x0, rl.y1), color=col, width=0.4)
                        bx = 30 + (n_ % 4) * (bw + gap)
                        byy = by0 + (n_ // 4) * (bh + gap)
                        box = fitz.Rect(bx, byy, bx + bw, byy + bh)
                        pg.draw_line(fitz.Point(bx + bw / 2, byy), m, color=col, width=0.6)
                        pg.draw_rect(box, color=col, fill=(1, 1, 1), width=1)
                        quadro(pg, box, i, col)
                    pg.insert_text((30, PH - 22), f'Resultados oficiais: Concretopy (índice da etapa 1, premissas v{P["versao"]}). Esforços característicos em tf e tf·m; '
                                                  'resistências como equivalente Rd/γf. Não constitui conclusão global nem emissão.', fontname='ar', fontsize=7, color=(0.3, 0.38, 0.43))
                    pg.insert_text((30, PH - 12), f'{TAG} | ANOTAÇÕES ETAPA 2 {REV} | Vermelho: não atende | Âmbar: tolerância D13 (η ≤ 110%) ou revisão de João | '
                                                  'Azul: geometria/documental | Clique no título para voltar à prancha', fontname='ar', fontsize=7, color=(0.3, 0.38, 0.43))
                    pg.insert_link({'kind': fitz.LINK_GOTO, 'from': fitz.Rect(0, 0, PW, 52), 'page': 0, 'to': fitz.Point(0, 0)})
        # marcadores na prancha original (reabrir a página: new_page invalida a referência anterior)
        ov = doc[0]
        fonts(ov)
        ocup = []
        for i in its:
            p = pos[i]
            col = cor_item(i)
            x0, x1, y = p['x0'] * K, p['x1'] * K, SH - p['y'] * K
            if x1 - x0 > 2:
                ov.draw_line((x0, y), (x1, y), color=col, width=2.5)
            cx = (x0 + x1) / 2
            ov.draw_circle((cx, y), 6, color=col, width=1.5)
            lab = rotulo(ocup, cx + 6, y - 22, FONT['b'].text_length(AP[i], fontsize=9) + 6, 13)
            if lab.y1 < y - 10:
                ov.draw_line((cx, y), (lab.x0, lab.y1), color=col, width=0.6)
            ov.draw_rect(lab, color=col, fill=(1, 1, 1), width=0.8)
            ov.insert_text((lab.x0 + 3, lab.y1 - 3), AP[i], fontname='ab', fontsize=9, color=col)
            if i in page_of:
                ov.insert_link({'kind': fitz.LINK_GOTO, 'from': lab, 'page': page_of[i], 'to': fitz.Point(0, 0)})
            feitos.append(i)
        ov.insert_text((60, 16), f'{TAG} | PRANCHA {fo} | ANOTAÇÕES ETAPA 2 {REV} | {len(its)} apontamentos | clique no código AP para abrir o quadro com valores '
                                 '(solicitação característica / resistência equivalente)', fontname='ab', fontsize=12, color=NAVY)
        doc.set_metadata({'title': f'{TAG} prancha {fo} - anotações etapa 2 {REV}', 'author': 'Auxiliar de Engenharia - revisão de João',
                          'subject': f'cópia anotada de {src_path.name} (sha256 {hashlib.sha256(src_path.read_bytes()).hexdigest()[:16]})'})
        doc.save(od / f'{TAG}_{fo}_ANOTADA_ETAPA2_{REV}.pdf', garbage=3, deflate=True)
    return od, feitos, sem


def quadro(pg, box, cid, col):
    it = ITEM[cid]
    c = next((x for x in CONTROLES if x['id'] == cid), None)
    sec = {'GEOM': 'Geometria', 'POS': 'Flexão positiva', 'NEG': 'Flexão negativa', 'MIN': 'Armadura mínima', 'CORT': 'Cortante / estribos',
           'SUSP': 'Suspensão', 'D27': 'Suspensão especial (D27)', 'DOC': 'Registro documental'}[it['secao']]
    x, y, w = box.x0 + 7, box.y0 + 6, box.width - 14
    y += put(pg, x, y, wrap(f"{AP[cid]} | {it['viga']} — {sec}", w, 9.5, 'b'), 9.5, 'b', col)
    y += put(pg, x, y, wrap(it['local'], w, 7.5), 7.5, color=(0.25, 0.32, 0.36)) + 2
    L = sk_rk(c, regioes(c)) if c and CTRL[c['controle']] != 'GEOM' and c['estado_execucao'] != 'IMPEDIMENTO_DOCUMENTAL' else [it['problema']]
    for j, ln in enumerate(L):
        fs, f = (8.2, 'b') if j == 0 else (7.3, 'r')
        lines = wrap(ln, w, fs, f)
        room = int((box.y1 - 14 - y) // (fs * 1.22))
        if room <= 0:
            break
        if len(lines) > room:
            lines = lines[:room]
            lines[-1] = lines[-1][:max(0, len(lines[-1]) - 3)] + '…'
        y += put(pg, x, y, lines, fs, f, TXT if j else col) + 1.5
    put(pg, x, box.y1 - 11, [f'ID {cid}'], 6.2, color=(0.4, 0.46, 0.5))


if __name__ == '__main__':
    so_rel, so_pr = '--so-relatorio' in A, '--so-pranchas' in A
    res = {}
    if not so_pr:
        path, n = gerar_relatorio()
        res['relatorio'] = {'arquivo': path.name, 'paginas': n}
    if not so_rel:
        od, feitos, sem = gerar_pranchas()
        res['pranchas'] = {'pasta': od.name, 'apontamentos_marcados': len(feitos), 'sem_posicao_em_prancha': sem}
    res.update({'data': HOJE.isoformat(), 'premissas_versao': P['versao'], 'apontamentos': len(AP),
                'fontes_sha256': {f: hashlib.sha256((W / f).read_bytes()).hexdigest() for f in ('indice_controles.json', 'selecao_etapa2.json', 'premissas.json')}})
    OUT.mkdir(exist_ok=True)
    (OUT / 'assinatura.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: v for k, v in res.items() if k != 'fontes_sha256'}, ensure_ascii=False))
