from pathlib import Path
import json,hashlib,shutil
O=Path(r'\\srvmaster\PUBLICO\Joao Severgnini\Simon\engineering-assistant\analises\atp_s07_vigas_terreo\rodada_05_relatorio_global');docs=Path(r'S:\PROJETOS EM EXECUÇÃO\25-208-WERT-ATP TERRA ALL RESORT-PORTO BELO-SC\PRANCHAS\APOIO\JOAO\ATP S07\DOCUMENTACAO ATP');base=docs/'10 VIGAS - TERREO';dest=base/'RODADA 05 - RELATORIO GLOBAL';dest.mkdir(exist_ok=True);count=0
for p in O.iterdir():
 if p.is_file() and p.suffix.lower() in ['.pdf','.md','.json','.py']:shutil.copy2(p,dest/p.name);count+=1
shutil.copytree(O/'fontes_retomada',dest/'fontes_retomada',dirs_exist_ok=True)
shutil.copytree(O/'historico_antes_negativos_por_lado_20261016',dest/'historico_antes_negativos_por_lado_20261016',dirs_exist_ok=True)
(dest/'evidencias').mkdir(exist_ok=True)
for p in (O/'evidencias').iterdir():
 if p.is_file() and (p.name.startswith('revisao_retomada_') or p.name.startswith('comparar_7403_') or p.name.endswith('_retomada.png') or p.name=='revisao_negativos_V43.png'):shutil.copy2(p,dest/'evidencias'/p.name)
index='''# Vigas do térreo - revisão vigente

[Relatório global revisado em PDF](RODADA%2005%20-%20RELATORIO%20GLOBAL/relatorio_global_vigas_S07.pdf)

[Relatório em texto](RODADA%2005%20-%20RELATORIO%20GLOBAL/relatorio_global_vigas_S07.md) | [Pendências discriminadas](RODADA%2005%20-%20RELATORIO%20GLOBAL/pendencias_verificacao.md)

Revisão de retomada em 16/10/2026: 79 páginas, 50 vigas, 95 intervalos de cálculo, 190 consultas negativas e 102 faixas de cortante. Resultados oficiais do Concretopy. Solicitações características em tf e tf·m; resistências equivalentes Rd/γf. C35 uniforme na seção final, conforme simplificação confirmada.

Incorporados: V31 apoiada na V12; V41 apoiada na V13; início do balanço no eixo V12/V13; V49 apoiada diretamente no bloco PC21C. V49/V50 verificadas por regiões de 50 e 87 cm. Corrigida a armadura negativa no P778 para 4Ø16 N16 da V24 e conferidos separadamente os lados do P785.

Positivas insuficientes em pelo menos uma seção: V16, V21, V24, V25, V35, V37, V49 e V50. Cortante insuficiente: V18 e V35. Suspensão V33–V19 e V40–V20 insuficiente; distribuição uniforme 75/25 em V41–V13 não atende. Consultar fichas para mínimas longitudinais, demais negativas e limites das conclusões.

João reservou para sua análise separada V17–V23, V17–V42, V35–V15 e V36–V5, mediante casos de gravidade e vento. Não considerar esses quatro encontros automaticamente como levantamento pelo sinal mínimo da envoltória.

Esta revisão ainda não encerra a ATP: faltam a comparação integral de cotas de todos os vãos, transições internas V23/V24/V42 e os controles de suspensão/detalhamento identificados no relatório. Trabalho ainda não concluído pelo assistente está distinguido de dados ausentes no projeto e das quatro pendências assumidas por João. Não há aprovação global das vigas. Rodadas anteriores preservadas.

Fontes desta revisão arquivadas em fontes_retomada; arquivos recebidos originais preservados. Conferências de fontes e PDF em auditoria_retomada.json e auditoria_fontes_congeladas_retomada.json.
'''
index+='\nCorreção de16/10/2026: negativos verificados por lado do apoio, sem unificação entre vãos. Auditadas190extremidades;45solicitações corrigidas e14resultados de capacidade alterados emC35. V43/P723:3/D=8,697tf·m e4/E=12,707tf·m. Resistências Concretopy arquivadas preservadas; nenhuma nova execução resistente. Revisão detalhada emrevisao_negativos_por_lado.md e.json.\n'
(base/'LEIA-ME - RODADA VIGENTE.md').write_text(index,encoding='utf8')
context=docs/'CONTEXTO ATP S07.md';addition='''

## Vigas do térreo — revisão da retomada em 16/10/2026

Esta atualização substitui as classificações anteriores de levantamento nas ligações V12–V31 e V13–V41. João confirmou: V31 descarrega na V12 e V41 descarrega na V13; início do intervalo 1B no eixo V12/V13. Reações originalmente negativas foram invertidas por ação-reação: Rk máximo24,46tf e30,52tf. Não são levantamento nessas duas ligações. V49 tem apoio direto confirmado no blocoPC21C, retirado da suspensão sobreV26. Usar somente os detalhes recebidos das peças de estribo138/50cm, sem presumir fechamento complementar.

João esclareceu o critério: reação negativa em permanentes+sobrecarga indica apoio invertido; negativa com vento pode indicar levantamento. Autorizou deixar V17–V23,V17–V42,V35–V15 eV36–V5 para sua análise separada. Mantidos os extremos da listagem, sem concluir o sentido físico pela envoltória total. Localizado caso1 noFOR0001.POR; FOR0001.LST disponível contém reações das restrições/fundações, sem os esforços de barras necessários a essas quatro interfaces.

Suspensões das V7/V9 naV31 eV8/V10 naV41 recalculadas com eixos confirmados e cortantes regionais; soma conservadora dos dois tirantes+cortante atende nas duas receptoras. V31→V12 atende numericamente à repartição75/25:8,7973cm²/m naV12 contra10,0531;3,3400cm²/m naV31 contra3,6673. V41→V13:distribuição uniforme75/25 não atende11,0468 contra10,0531 naV13 e5,0642 contra3,6673 naV41; outras distribuições admissíveis não avaliadas. Funcionamento/ancoragem das peças138/50cm permanece separado da área nominal.

Positivas regionais V49/V50 agora localizadas pela cota130cm: transições xTQS1,465m e3,005m; trechosh50 insuficientes e trechosh87 atendem. V24/P778:usar4Ø16N16, capacidade10,7804tf·m supera8,565tf·m; retirada a falha anterior criada por2Ø10 porta-estribo. Apoio compartilhadoP785 V23/V24:maior negativo12,997tf·m, sem redução à face. Resultado principal positivo insuficiente emV16,V21,V24,V25,V35,V37,V49,V50; cortante insuficienteV18,V35. Demais negativas/mínimos discriminados nas fichas.

Relatório revisado publicado na mesma pastaRODADA05,80páginas. Continua parcial quanto à conclusão integral daATP: comparação completa das cotas dos vãos e algumas transições/suspensões ainda não encerradas pelo assistente. Não apresentar essas leituras pendentes como falta de informação do engenheiro. Quatro interfaces acima reservadas porJoão são pendências distintas.

7402 e7403 regravadas: desenhos avaliados preservados, com comparação vetorial/visual registrada. 7402 SHA1cd6c36614998eaba8b223e8daafedbaed3e08cffbb9d73c5c3fd17a73a03c2a;7403 SHA4b9c730139418a54de9fcd14fa1ffd4ec92b2677fec413edc3c1f43a6842bc5c. Na7403,16recortes por identidade de pixels em configuração equivalente eV33 por conferência visual; não afirmar igualdade de todos os recortes sem anotações. Cópias das fontes arquivadas emfontes_retomada. ModeloVGESFS permaneceu comSHAf0bd8b39543e76e0be317035ba3315418c4d8159086a1ff16be547f167436d38.
'''
old=context.read_text(encoding='utf8')
if '## Vigas do térreo — revisão da retomada em 16/10/2026' not in old:context.write_text(old+addition,encoding='utf8')
expected=json.loads((O/'auditoria_retomada.json').read_text(encoding='utf8'))['pdf_sha256'];actual=hashlib.sha256((dest/'relatorio_global_vigas_S07.pdf').read_bytes()).hexdigest();assert actual==expected;print(json.dumps({'published':str(dest/'relatorio_global_vigas_S07.pdf'),'top_level_files_updated':count,'pdf_sha256':actual,'context_updated':True},ensure_ascii=True))
