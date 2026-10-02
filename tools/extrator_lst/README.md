# Extrator de relatorios LST de vigas TQS

Python 3.10+, somente biblioteca padrao. Extracao documental, sem regras de verificacao estrutural. Desenvolvido e testado com os LST de COLLINE R60 / DIFERENCIADO, V504.

## Executar

```powershell
python extrair_viga_lst.py "C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\DIFERENCIADO\VIGAS" --viga V504 --saida V504_raw.json
python test_extrair_viga_lst.py
```

Leitura CP1252 estrita por padrao; `--encoding` permite substituicao. Arquivos de origem nao sao alterados. A saida informada e sobrescrita.

## JSON documental (`V504_raw.json`)

- `categorias`: as 13 categorias solicitadas; um registro pode pertencer a mais de uma.
- `origem`: arquivo, linhas fisicas (base 1) e texto exato da linha.
- `campos_explicitos`: rotulos originais e chaves normalizadas, valores numericos, unidades explicitas, conversao literal quando suportada e campos logicos.
- `normalizacao`: tabelas reconhecidas de geometria, apoios, reacoes, series de 13 secoes, barras negativas, faixas de estribos, flexao por posicao e vetores documentais. null quando nao existe parser especifico.
- `secao`, `vao_contexto_original`, `lado_contexto`: contexto sequencial local do relatorio; nao sao identificadores globais. Para tabelas, prevalecem seus campos proprios.
- `outros_dados`: registros preservados que nao receberam categoria especifica.
- `trechos`: blocos integrais da viga e cabecalhos globais, incluindo legendas e criterios. Nao omite linhas so por nao reconhecer sua sintaxe.
- `arquivos`: inventario, caminho, tamanho, codificacao e SHA-256.
- `cobertura`: contagens documentais, nao verificacao de completude semantica.

A normalizacao e incremental: todas as linhas dos blocos sao preservadas, mas parte do conteudo permanece como texto/tokens ou campos genericos. Nao se deve tratar todo registro documental como resultado final de dimensionamento. Grampos citados como parametro de ancoragem nao implicam grampos efetivamente adotados. Marcadores de asteriscos ficam preservados sem inferir erro. Mensagens impressas de verificacao sao dados do TQS, nao verificacoes executadas por esta ferramenta.

## Particularidades encontradas na V504

- 13 LST lidos; 11 com blocos da V504; CONVF2.LST e RESESTERR.LST vazios.
- RELDTVGS e VGESFS indicam vao 1 com 1,206 m, secao 0,14 x 0,32 m. Relatorios detalhados usam vao interno 2 e linhas de comprimento zero nas extremidades. Numeracao original preservada, sem fusao automatica.
- ESTRIB informa comprimento 1,23 m; resumos de flexao informam 1,21 m. Nao se escolhe um valor unico.
- RELDTVeT imprime geometria em [cm] com valores 1,2 / 0,1 / 0,3; a unidade impressa e mantida com ressalva, sem corrigir por conjectura.
- Espacamentos intermediarios diferem: RELDTFPS registra 6 cm e RELDTFNG/ESTRIB registram 15 cm. Etapas e fontes permanecem separadas.
- Ha unidades inconsistentes em campos de resistencia, inclusive tfm para VRd2. Conversao literal nao valida a unidade original.
- Celulas vazias nas series sao null, nunca zero. Sinais sao mantidos. Nao sao inventadas abscissas nem combinacoes de carregamento.

Os testes usam os relatorios locais: inventario, cobertura de todas as linhas significativas, identidade dos trechos, ausencia de contaminacao por outras vigas, series densas/esparsas e valores conhecidos de geometria, reacoes e estribos. Sao ignorados se a pasta original nao existir. Generalizacao para outras versoes de LST requer validacao com seus arquivos.


## Segunda camada: modelo consolidado

O extrator permanece responsavel pela leitura e normalizacao documental. Para gerar o modelo de entidades, execute:

```powershell
python consolidar_viga.py V504_raw.json --saida V504.json
python -m unittest test_consolidar_viga
```

Veja [CONSOLIDACAO.md](CONSOLIDACAO.md) para o contrato de dados, unidades, fontes preferenciais, divergencias e exemplos de consumo. O V504.json passa a ser o consolidado; a saida documental anterior foi preservada integralmente como V504_raw.json. O codigo e os testes existentes da extracao nao foram alterados.


## TQS data semantics

Consult [tqs-beam-data.md](../../.agents/skills/reinforcement-review/references/tqs-beam-data.md) for span length, DEPEV, support axes and clear spans. Consolidated schema 1.1 adds derived lengths and per-report support reactions; see CONSOLIDACAO.md.
