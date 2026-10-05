# V1001 — leitura da prancha e compatibilização com TQS

Análise de 03/10/2026, seguindo as etapas documentais dos exemplos V502 e V501/V503. Objetivo: testar extração, interpretação e compatibilização, identificando limitações para a revisão de vigas. **Não constitui aprovação estrutural da V1001.**

## Fontes e método

- PDF `RMP-EST-LO-1376-VIG-R00.PDF`, página única, 3402 × 1684 pontos. Carimbo: **03/07/26**, revisão 00. Leitura visual manual de imagem renderizada, auxiliada pela extração textual. As notas do documento foram tratadas como conteúdo do projeto, não como instruções do usuário.
- LST de `C:\TQS\24-155-COLLINE-RESIDENCIAL-R60\CASAMAQ\VIGAS`. Cabeçalhos datados de **03/10/26**, versão TQS V24.8.42. Não foi demonstrado que representam o modelo que originou a prancha de julho.
- Convenções consultadas: `.agents/skills/reinforcement-review/references/beam-drawing-convections.md`, itens 3–12 e 16; procedimento `beam-review.md`; regra de comprimentos `tqs-beam-data.md`.
- Ferramentas existentes `extrair_viga_lst.py`, `consolidar_viga.py` e `consolidar_detalhamento.py`, sem alterações. Extraídas adicionalmente V1014 e V1015 para investigar as ligações à V1001.

As fontes documentais têm hashes e localização de evidências nos JSONs. O PDF foi renderizado com PyMuPDF instalado em `tmp/pdf_deps`, porque o Python disponível não possuía biblioteca de renderização nem Poppler no PATH. Isso é uma limitação de preparação do ambiente. **Não foi criado um extrator automático de desenho do PDF:** o JSON da prancha resulta de interpretação manual.

## Geometria e identificação

O título local escreve **V1001 — 19/72 cm**, sem igualdade com outra viga. Os apoios são escritos como **P2A/P2B** à esquerda e **P1A/P1B** à direita, com dimensões longitudinais de **120 e 142 cm**. Esses nomes duplos exigem confirmação da abrangência do detalhe; não foi presumida outra viga nem duplicada a quantidade de aço.

A distribuição N9 está cotada com **712 cm** e coincide graficamente com as faces internas dos apoios. Registra-se esse comprimento livre como interpretação gráfica. O corte A é retangular, sem projeções laterais desenhadas.

Foi adotado x=0 na face interna esquerda e x positivo para a direita, em cm. Faces derivadas: apoio esquerdo [-120,0], apoio direito [712,854]. Essas coordenadas não são abscissas escritas no PDF.

O TQS identifica V1001, um vão geral, seção 0,19 × 0,72 m e sequência P2A → P1A (`VGESFS.LST`, linhas 487–506; `RELDTVGS.LST`, bloco 1507–1572). O vão geral 1 corresponde ao vão interno 2 nos relatórios detalhados; registros extremos de comprimento zero não foram convertidos em vãos físicos.

Com os valores de `RELDTFPS.LST:4770–4771` e `RELDTFNG.LST:3595–3596`, aplica-se a regra de comprimentos já confirmada por João:

```
L_eixos = 7,552 + 0,384 + 0,494 = 8,430 m
L_livre = 8,430 − 1,20/2 − 1,42/2 = 7,120 m = 712 cm
```

**OK documental, para essas fontes:** o comprimento livre coincide com a prancha. ESTRIB imprime 8,43 m e faixas entre 60 e 772 cm; RELGER imprime intervalo 0–712 cm. Isso não autoriza tratar todos os comprimentos como a mesma grandeza. O consolidado conserva `support_axis_length=null` e `clear_span_length=null`, porque outras fontes divergem nas excentricidades. A conta por fonte acima não substitui esse consenso.

Planta de formas e modelo geométrico não foram fornecidos/consultados; seção, apoios e continuidade não foram validados contra uma fonte geométrica independente.

## Armaduras efetivamente detalhadas

Comprimentos e coordenadas em cm; diâmetros em mm. As formas longitudinais são retas. Camadas sem chamada adicional foram interpretadas pelo padrão do escritório; coordenadas foram derivadas das cotas locais e do comprimento de barras retas.

| Posição | Face / função gráfica | Chamada | Camadas [1ª,2ª] | Intervalo x | Derivação |
|---|---|---|---|---|---|
| N1 | Superior / negativa | 2 Ø12,5 C=195 | [1,1] | [-48,147] | início=-48; fim=-48+195; 1 barra em 2ª explícita |
| N2 | Superior / negativa | 2 Ø12,5 C=300 | [2,0] | [-48,252] | início=-48; fim=-48+300 |
| N4 | Superior / negativa | 2 Ø16 C=225 | [2,0] | [214,439] | início=214; fim=214+225 |
| N7 | Superior / negativa | 3 Ø16 C=375 | [3,0] | [399,774] | fim=712+62; início=774−375 |
| N8 | Superior / negativa | 3 Ø16 C=235 | [0,3] | [540,775] | fim=712+63; início=775−235; 3 barras em 2ª explícitas |
| N3 | Inferior / positiva | 2 Ø10 C=650 | [2,0] | [-42,608] | início=-42; fim=-42+650 |
| N5 | Inferior / positiva | 2 Ø10 C=795 | [2,0] | [-42,753] | fim=712+41; início=753−795 |
| N6 | Pele | 2×3 Ø10 C=794 | 3 por face lateral | [-24,770] | início=-24; fim=-24+794 |

O corte A confirma **2 pontos superiores, 4 inferiores na primeira camada e 3 de pele por face**. A associação superior é N4 e a inferior N3+N5, por cruzamento com a região de A-A. A abscissa exata do corte não está cotada. O corte não foi extrapolado para os apoios.

A N4 é uma posição superior curta no interior do vão. Não deve ser descartada por ausência de momento negativo máximo nessa região nem classificada apenas pela bitola; sua função resistente/constructiva precisa ser avaliada com o diagrama e a montagem dos estribos.

**Verificar montagem nas sobreposições:** as coordenadas derivadas produzem N2+N4 entre x=214 e 252 e N4+N7 entre x=399 e 439. Aplicar a primeira camada a ambas as marcas, pela ausência de outra chamada, leva respectivamente a 4 barras superiores (2 Ø12,5 + 2 Ø16) e 5 Ø16 na alma de 19 cm. O corte A mostra apenas a região de N4 isolada e não resolve esses encontros. É necessário confirmar a posição física das barras e os espaçamentos locais; o modelo atual atribui camadas por marca e não representa rearranjos locais. Não foi concluído que as barras caibam nem que a solução deva ser alterada de uma maneira específica.

### Configurações locais e áreas geométricas

Usando `As=n·π·φ²/400`, com φ em mm e As em cm²:

- Apoio esquerdo x=0: N1+N2, **4 Ø12,5 = 4,909 cm²**, com 3 barras na 1ª camada e 1 na 2ª.
- Região inferior em 0<x<608: N3+N5, **4 Ø10 = 3,142 cm²**, primeira camada.
- Região inferior em 608<x≤712: apenas N5, **2 Ø10 = 1,571 cm²**.
- Apoio direito x=712: N7+N8, **6 Ø16 = 12,064 cm²**, 3 barras em cada camada.
- Pele: **3 Ø10 = 2,356 cm² por face**, 4,712 cm² no conjunto de duas faces.

São áreas geométricas das barras que atravessam a seção. Não demonstram ancoragem, efetividade resistente, armadura mínima ou capacidade. A interrupção de N3 em x=608 exige compatibilização com a envoltória e a ancoragem; índices de pontos do TQS não permitem verificar isso automaticamente.

### Estribos e grampos

**N9 — 51 Ø5 c/14**, região 712 cm. Forma: **14 × 67 cm, C=177 cm**, dois ramos verticais desenhados. Quantidade regional e quantidade da forma coincidem. O comprimento total inclui os trechos da forma; não foram inventados comprimentos ou ângulos de ganchos. Não se obtiveram os afastamentos do primeiro e último estribos às faces pela conta 712/14.

**Grampos adicionais não detalhados**, conforme convenção do escritório. Isso não significa que sejam desnecessários. As barras inferiores penetram geometricamente 42 cm no apoio esquerdo; no direito somente N5 chega, penetrando 41 cm. Esses valores não são comprimentos de ancoragem efetivos automaticamente.

## Confronto com o dimensionamento do TQS

| Região | Prancha | Resultado documental TQS | Classificação |
|---|---|---|---|
| Flexão positiva, região com N3+N5 | 4 Ø10; 3,142 cm² | FLEXPS: 4 Ø10, As calculada 2,95 cm² | OK de quantidade local; verificar MRd, mínimo e extensões |
| Apoio superior esquerdo | 4 Ø12,5, 3+1 | FLEXNG: 4 Ø12,5, As=4,89 cm² | OK de quantidade; verificar ancoragem e cortes |
| Apoio superior direito | 6 Ø16, 3+3 | FLEXNG: 5 Ø16, As=10,34 cm² | Verificar diferença; possível simplificação/alteração de versão |
| Pele | 2×3 Ø10 | FLEXPS/RELGER: 2×3 Ø8, área total real 3,02 cm² | Verificar aumento de bitola; não concluir excesso indevido |
| Estribos gerais | Ø5 c/14, 2 ramos | ESTRIB: Ø5 c/14, 2 ramos nas três faixas | OK documental; resistência independente pendente |

Fontes: `FLEXPS.LST:200–208`, `FLEXNG.LST:239–248`, `ESTRIB.LST:242–251`, `RELGER.LST:35–63`. No apoio direito, 6 Ø16 somam 12,064 cm² contra 10,053 cm² de 5 Ø16; isso é cerca de 20% a mais de área em relação ao arranjo do TQS. A diferença não autoriza retirar uma barra: o TQS registra área necessária maior que a área geométrica de 5 Ø16, e a altura útil, as camadas, as ancoragens e a versão do projeto precisam ser verificadas.

O relatório detalhado negativo agrupa no apoio direito **2 barras C=237,0** e **3 barras C=376,7** (`RELDTFNG:3713–3714`), enquanto a prancha tem 3 C=235 e 3 C=375. À esquerda registra 2 C=196,9 e 2 C=300,9 contra 195/300 na prancha (`3708–3709`). As diferenças foram mantidas. Os números de posição do LST não são as marcas N da prancha, e as abscissas do apoio direito não foram convertidas para o x global sem esclarecer a origem.

Na positiva, o TQS imprime 2 barras C=648 e 2 C=795 após compatibilização (`RELDTFPS:4934–4940`); a prancha tem 650/795. O LST imprime x,i=-20 para essas barras, enquanto a prancha usa início=-42 em referência à face interna. São referências que precisam de transformação documentada; não se concluiu deslocamento físico de 22 cm por subtração direta.

## Esforços: unidade não basta para definir a solicitação

O modelo consolidado possui 14 séries atribuídas ao vão, com 13 índices cada, `positions=null` e nenhuma série não atribuída na V1001. Foram preservadas etapas e sinais.

As entradas de `RELDTVGS` declaram **esforços característicos**; as tabelas de flexão escrevem **Mk**. Portanto, os valores abaixo não foram chamados de MSd:

| Grandeza / fonte | Valor documental | Conversão literal |
|---|---:|---:|
| Máximo positivo de entrada, VGESFS:500 | 6,102 tf·m | 59,840 kN·m |
| Negativo esquerdo, VGESFS:496 | −9,905 tf·m | −97,135 kN·m |
| Negativo direito, VGESFS:496 | −19,878 tf·m | −194,937 kN·m |
| Maior módulo de cortante de entrada, VGESFS:494 | 11,563 tf | 113,394 kN |
| Maior cortante final em módulo, RELDTVeT | 11,28 tf | 110,619 kN |
| Vsd no resumo RELGER, intervalo 0–712 | 16,19 tf | 158,770 kN |

Conversões: 1 tf=9,80665 kN; 1 tf·cm=0,0980665 kN·m. Os relatórios detalhados imprimem Gamaf=1,4. A relação entre 11,563 e 16,19 é coerente com essa majoração, mas não foi criada regra geral de multiplicar todos os esforços por 1,4: faltam combinações e definição dos casos aplicáveis. Também há etapas com redução do cortante e verificação da biela com cortante original (`RELDTVeT:3527–3578`).

ESTRIB registra Vsd=9,1/5,3/16,2 tf e VRd2=84,0/84,0/83,6 tf nas três faixas. São **resultados do TQS**, não verificações realizadas pelo auxiliar. O resumo RELGER registra VRd2=84,02 tf; não se escolheu esse valor como mínimo global porque a terceira faixa traz valor menor. A comparação documental não substitui cálculo independente.

## Apoios indiretos e suspensão

Há **dois contornos retangulares tracejados**, um à esquerda de A-A e outro à direita, próximo do apoio direito. Conforme o padrão, representam vigas apoiadas na V1001. Nomes e posições exatas não são cotados. N9 permanece uniforme; **não há suspensão específica desenhada em nenhum dos dois contornos**.

A investigação nominal nos outros LST revelou:

| Origem TQS | Apoio na V1001 | Reação máxima/mínima | Fonte |
|---|---|---|---|
| V1014 | nº 2 | 2,817 / 2,292 tf | VGESFS:184 |
| V1015 | nº 3 | 5,027 / 0,874 tf | VGESFS:212 |

Essas são ligações nominais do TQS. Não foram associadas automaticamente a IB1/IB2 do PDF; a ordem gráfica, o nome e a abscissa na receptora precisam de confirmação geométrica. Reações máximas não foram somadas como se pertencessem à mesma combinação.

**Informação relevante que exige leitura do relatório detalhado:** `RELDTVeT:3486–3500` calcula suspensão para duas cargas, com K66=2:

| Carga do relatório | dfcsa | Faixa de pesquisa | Comprimento | As,susp do TQS |
|---|---:|---|---:|---:|
| 1 | 32 cm | 278,6–366,1 cm | 87,5 cm | 0,46 cm² |
| 2 | 52 cm | 597,1–679,6 cm | 82,5 cm | 1,42 cm² |

O próprio relatório descreve K66=2 como adoção de Asw **ou** Asusp para a condição indicada. Depois adota Ø5 c/14 e o resumo informa AsSus=0,0. Logo, **ausência de armadura adicional na prancha ou AsSus=0 no resumo não prova que não houve demanda de suspensão**: os valores intermediários existem e o software fez uma compatibilização. Não foi validado independentemente se os estribos gerais atendem às duas transferências, nem se é apropriado compartilhar sua capacidade no caso real.

As cargas concentradas de 2,82 e 5,03 tf são numericamente compatíveis com as reações máximas de V1014/V1015. Isso é indício de correspondência, não comprovação da associação com os contornos do PDF.

## Limitações reproduzidas e melhorias propostas

| Prioridade | Limitação demonstrada | Consequência | Próxima melhoria verificável |
|---|---|---|---|
| 1 | Apoios com identificadores internos `@AP;`, `@AP~`, `@AP?` são rejeitados pelo reconhecimento `^[VP]` | V1014 consolida apenas 1 apoio de 2; V1015 nenhum de 3; cadeias e séries ficam sem associação | Reconhecer linhas válidas pela estrutura da tabela, preservar ID interno e relacionar ao apoio numerado; testar os dois casos sem inventar nomes |
| 1 | Reações trazem `V1001\u0000` | Nome nominal preservado, `support_id=null`; junção nominal simples falha | Criar chave canônica documentada para NUL terminal, mantendo texto e nome originais, e verificar colisões |
| 1 | Esquema de séries conserva etapa/unidade, mas não declara explicitamente natureza característica/de cálculo e combinações | Risco de comparar MRd com Mk ou adotar 110,619 kN como Vsd | Modelar natureza, coeficientes, reduções e origem de cada esforço; não inferir por nome “final” |
| 1 | 13 pontos sem abscissas | Não permite cruzar término de N3 ou escalonamento N1/N8 com demanda local | Obter coordenadas confiáveis do TQS e documentar referência; não preencher por distribuição uniforme |
| 2 | Materiais conflitantes: 400 kgf/cm² vira 39,2266 MPa, enquanto outro trecho escreve 40 MPa; CA-50A/CA-50 | fck e aço ficam null | Documentar política de equivalência de apresentação, distinguindo conversão física e nominal; preservar alternativas |
| 2 | Unidades impressas incoerentes em RELDTVeT | Conversões literais geram geometria 0,076/0,002/0,007 m; outras linhas escrevem distâncias incompatíveis | Criar diagnóstico de unidade suspeita e impedir consumo resistente sem resolução documentada |
| 2 | Geometria mistura comprimentos de referência, de eixo e livre; excentricidades também conflitam | Comprimentos derivados globais ficam null apesar de uma conta por fonte coerente | Expor geometria derivada por fonte/etapa antes do consenso, sem escolher automaticamente |
| 2 | Demanda intermediária de suspensão não está no modelo consolidado | Perde-se As,susp=0,46/1,42 e critério K66 ao consumir só o modelo | Consolidar carga, reação, faixa, mecanismo, demanda e decisão do TQS em entidades separadas |
| 2 | Título singular com apoios duplos | Associação automática a grupo é insegura | Suportar nomes alternativos/pares e abrangência não resolvida; resolver pelo projeto |
| 3 | PDF não possui parser geométrico automático | Texto sozinho perde camada, face, tracejado, cortes e associação de cotas | Usar este documental validado visualmente como caso de referência de um futuro extrator |
| 2 | Camadas atribuídas globalmente por marca; N4 se sobrepõe a N2 e N7 | O corte A não verifica os arranjos nas sobreposições; podem existir conflitos de alojamento | Verificar configuração por intervalos e admitir camada local não resolvida, sem extrapolar o corte |
| 3 | Ferramentas resistentes independentes/planilha não disponíveis nesta análise | Não há MRd, mínimo, ancoragem ou suspensão independentemente verificados | Integrar a planilha/ferramenta validada com entradas resolvidas e casos de referência |

As unidades suspeitas não são apenas hipótese: `RELDTVeT:3411–3412` imprime **Larg.=19,00 m / 14,00 m** e **Dist.=322,40 m / 638,40 m**, incompatíveis com um vão de aproximadamente 7,55 m e com as dimensões locais. Depois imprime Dist.=284,00/600,00 cm (`3445–3446`). Esses números não foram corrigidos silenciosamente nem usados como coordenadas finais.

Os IDs internos estão em `RELDTVGS:556` para V1014 e `622–624` para V1015. O arquivo documental preserva essas linhas, mas elas não viram entidades `apoio`; isso demonstra que cobertura textual não equivale a completude semântica. Os NUL terminais aparecem nas reações `VGESFS:184/212` e permanecem nos JSONs adicionais.

Também há cabeçalhos gerais que citam NBR6118:2014 enquanto relatórios detalhados indicam NBR6118:2023. Foi registrada a informação documental; não se concluiu qual edição governa todos os cálculos apenas pelos cabeçalhos. **O texto normativo não foi consultado e nenhuma conclusão normativa foi emitida.**

## Estado da revisão

- **OK documental:** seção, vão livre por RELDTFPS/RELDTFNG, arranjo local positivo, quantidade negativa esquerda e estribos gerais compatíveis com as fontes citadas.
- **Verificar:** versões julho/outubro, abrangência dos nomes duplos, 6 Ø16 versus 5 Ø16 à direita, pele Ø10 versus Ø8, comprimentos e referências das barras.
- **Caso especial / verificar:** dois apoios indiretos, critérios de compartilhamento dos estribos entre cisalhamento e suspensão e identidade/posição das vigas apoiadas.
- **Pendente:** flexão resistente, mínimo, espaçamentos resistentes, ancoragem positiva/negativa, decalagem, VRd2 e suspensão por ferramenta independente. Ausência de grampo não foi classificada como erro.
- **Corrigir na ferramenta:** reconhecimento de apoios internos e normalização rastreável de identidade. Não foi determinada nesta etapa uma alteração segura de armadura para execução.

## Artefatos e validação

Criados `V1001_detalhamento_prancha.json`, `V1001_beam_model.json`, `V1001_tqs_raw.json`, `V1001_tqs.json`, recorte e corte renderizados, além de raw/consolidado de V1014 e V1015. O modelo de desenho permanece independente do TQS; o cruzamento está neste relatório.

O consolidador do desenho validou 7 posições longitudinais, 1 de pele, 2 apoios principais, 2 indiretos, 1 região de estribos, unicidade e fidelidade à projeção documental. `lower_position` do corte conserva a lista N3/N5 e o agrupamento fica null; consumidores precisam aceitar esses estados sem transformá-los em valor escalar ou false.

**64 testes existentes passaram**: 35 do extrator/consolidador LST e 29 do modelo de detalhamento, sem skips. Esses testes não abrangem a falha descoberta dos identificadores internos: passar na suíte não demonstra generalização suficiente para CASAMAQ. Não houve alteração de parsers, schemas, skills ou testes nesta análise.
