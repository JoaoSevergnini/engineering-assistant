import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()))
from tools.extrator_lst.extrair_viga_lst import HEADER, extract
from tools.extrator_lst.consolidar_viga import consolidate
from tools.beam_mapping.indirect_supports import lst_relations, associate
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('folder',type=Path)
parser.add_argument('--floor',required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
folder=args.folder
report = folder / 'VGESFS.LST'
ids = sorted({f'V{int(m.group(1))}' for line in report.read_text(encoding='cp1252').splitlines()
              if (m := HEADER.match(line))}, key=lambda s:int(s[1:]))
models = [consolidate(extract(folder, beam)) for beam in ids]
relations = lst_relations(models)
import hashlib
for row in relations:
    for source in row['reaction_source']:
        data=(folder/source['file']).read_bytes()
        lines=data.decode('cp1252').splitlines()
        start,end=source['lines']
        source.update(original_text='\n'.join(lines[start-1:end]),
                      file_sha256=hashlib.sha256(data).hexdigest(),encoding='cp1252')
result = {'floor':args.floor, 'geometry_inventory_complete':False,
          'plant_reading_deferred_by_engineer':True, 'beams_examined':ids,
          'lst_directory':str(folder), 'connections':associate([],relations,floor=args.floor)}
args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2),encoding='utf8')
print('beams',len(ids),'observations',len(relations))
