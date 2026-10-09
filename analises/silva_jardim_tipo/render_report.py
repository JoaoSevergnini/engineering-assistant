from pathlib import Path
import sys
R=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant');sys.path.insert(0,str(R/'tmp/pdf_deps'));import pymupdf as f
P=R/'analises/silva_jardim_tipo'
story=f.Story((P/'Relatorio_revisao_vigas_TIPO.html').read_text(encoding='utf8'),archive=f.Archive(str(P)))
writer=f.DocumentWriter(str(P/'Relatorio_revisao_vigas_TIPO.pdf'))
page=f.paper_rect('a4');body=f.Rect(34,35,page.width-34,page.height-38)
def rectfn(n,filled):return page,body,None
story.write(writer,rectfn);writer.close()
doc=f.open(P/'Relatorio_revisao_vigas_TIPO.pdf')
for i,p in enumerate(doc):p.insert_text((34,page.height-21),f'Silva Jardim | Revisao de vigas TIPO | 08/10/2026 | {i+1}/{len(doc)}',fontsize=7,color=(.3,.4,.5))
doc.save(P/'Relatorio_revisao_vigas_TIPO_paginado.pdf');doc.close()
(P/'Relatorio_revisao_vigas_TIPO_FINAL.pdf').write_bytes((P/'Relatorio_revisao_vigas_TIPO_paginado.pdf').read_bytes())
doc=f.open(P/'Relatorio_revisao_vigas_TIPO_FINAL.pdf');print('PDF',len(doc),'pages',sum(len(p.get_text()) for p in doc),'text characters')
for i in (0,3,8,len(doc)-1):
 if i<len(doc):doc[i].get_pixmap(matrix=f.Matrix(1.3,1.3)).save(P/f'report_preview_{i+1}.png')
