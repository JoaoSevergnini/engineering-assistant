"""PDF observations from explicitly declared zones. No longitudinal geometry inference.

PyMuPDF is optional, loaded only for PDF reads. An empty zone never proves absence.
"""
import hashlib
import re
from pathlib import Path

# Printed nominal C length, never a straight projected interval.
LABEL = re.compile(r'(?P<quantity>\d+)\s*(?:N(?P<mark>\d+)\s*)?[Øø∅Φ]\s*(?P<diameter>[\d.,]+)\s*(?:N(?P<after_mark>\d+)\s*)?C\s*=?\s*(?P<length>[\d.,]+)', re.I)
MARK_FIRST = re.compile(r'N(?P<mark>\d+)\s+(?P<quantity>\d+)\s*[Øø∅Φ]\s*(?P<diameter>[\d.,]+)\s*C\s*=?\s*(?P<length>[\d.,]+)', re.I)


def parse_label(text):
    m = MARK_FIRST.search(text) or LABEL.search(text)
    if not m:
        return None
    d = m.groupdict()
    mark = d.get('mark') or d.get('after_mark')
    if mark is None:
        return None
    number = lambda x: float(x.replace(',', '.'))
    return dict(mark='N' + mark, quantity=int(d['quantity']), diameter_mm=number(d['diameter']), nominal_length_cm=number(d['length']))


def extract_zones(path, zones):
    """zones: page (zero-based), bbox, view, quantity_scope, integrity, optional mark.

    Table extraction is line-based and header-declared; unsupported rows stay pending.
    It never associates a section count with an occurrence without an explicit ID.
    """
    import fitz
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    observations, coverage, pending = [], [], []
    with fitz.open(path) as doc:
        for zi, z in enumerate(zones):
            page = doc[z['page']]
            bbox = z['bbox']
            if len(bbox) != 4 or bbox[0] >= bbox[2] or bbox[1] >= bbox[3]:
                raise ValueError('invalid_pdf_zone')
            words = page.get_text('words', clip=fitz.Rect(bbox))
            # TQS tables encode each cell as a distinct PDF line/block.
            # Join only words on the same visual baseline within 1 point.
            lines = {}
            for w in sorted(words, key=lambda w: (w[1], w[0])):
                baseline = (w[1] + w[3]) / 2
                key = next((k for k in lines if abs(k - baseline) <= 1), baseline)
                lines.setdefault(key, []).append(w)
            provenance = dict(file=str(path), sha256=digest, page=z['page'] + 1, bbox=bbox, zone_id=z.get('id', str(zi)))
            coverage.append(dict(view=z['view'], marks=z.get('marks'), integrity=z.get('integrity', 'UNVERIFIED'),
                                 extraction='PARTIAL', provenance=provenance))
            for li, entries in enumerate(lines.values()):
                entries.sort(key=lambda w:w[0])
                text = ' '.join(w[4] for w in entries)
                label = parse_label(text)
                if label is None and z['view'] == 'STEEL_SCHEDULE' and z.get('columns') == ['mark', 'diameter_mm', 'quantity', 'nominal_length_cm', 'total_length_cm']:
                    cells = text.split()
                    if len(cells) == 5 and all(re.fullmatch(r'\d+(?:[.,]\d+)?', c) for c in cells):
                        label = dict(mark='N'+cells[0], diameter_mm=float(cells[1].replace(',','.')), quantity=int(cells[2]), nominal_length_cm=float(cells[3].replace(',','.')))
                if label:
                    observations.append(dict(**label, representation_id=f'Z{zi}-L{li}', view=z['view'],
                                             quantity_scope=z.get('quantity_scope'), occurrence_id=z.get('occurrence_id'),
                                             section_id=z.get('section_id'), provenance=[dict(provenance,text=text,
                                             text_bbox=[min(w[0] for w in entries), min(w[1] for w in entries), max(w[2] for w in entries), max(w[3] for w in entries)])]))
                elif text.strip():
                    pending.append(dict(code='UNPARSED_DOCUMENTARY_LINE', text=text, provenance=provenance))
    return dict(observations=observations, coverage=coverage, pending=pending)
