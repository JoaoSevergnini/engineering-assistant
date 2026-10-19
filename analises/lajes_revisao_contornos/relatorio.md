> Atualiza??o posterior: Jo?o forneceu o contorno vermelho de L603. A forma foi registrada como confirma??o humana, com digitaliza??o m?trica aproximada em [L603 ? confirma??o e associa??es](../lajes_l603_confirmada/relatorio.md). A pend?ncia descrita abaixo ? o resultado hist?rico da leitura autom?tica.

# Revisão da Etapa 7 — contornos e associação das armaduras

**Resultado:** foi possível obter oito contornos candidatos vinculados aos nove
nomes da prancha e encontrar 16 ocorrências distribuídas com interseção positiva
nesses candidatos. **L603 permanece sem contorno fechado recuperado.** Os resultados
são uma revisão geométrica independente, não confirmação do engenheiro nem nova
versão do inventário oficial da Etapa 7.

## O que foi revisto

Foram inspecionados código, README, inventários e mapas das Etapas 6/7, entidades
vetoriais/textuais e os trechos da prancha. A Etapa 7 acrescentou relações entre
ocorrências, limites espaciais de confirmação e investigação de faces poligonais.
O resultado oficial continua com 35 regiões, 119 células, 77 blocos e 44 células
indeterminadas. O modelo de relações não resolveu sozinho os contornos.

Os arquivos da PoC/análises estão **não rastreados pelo Git**. Portanto não há um
diff versionado completo que permita atribuir cada alteração entre mensagens.
A comparação foi feita com os artefatos preservados e a proveniência da Etapa 7,
não por suposição a partir das datas de modificação.

Nesta revisão foram adicionados somente `review_slab_contours.py`, seus testes,
esta documentação e novos resultados. O reconhecimento principal, as relações,
os contornos oficiais anteriores e o PDF não foram substituídos.

## Achados da revisão do código

1. **Conexão da etiqueta incompleta:** `reconstruct_slabs` procura extremidades
   de linhas junto à caixa do **nome** da laje. Em L611/L612 o indicador começa junto
   à **espessura** abaixo do nome. D1884:0 fica a cerca de 13,56 pt do nome L612,
   mas apenas 2,22 pt do bloco completo. D1885:0 apresenta o mesmo padrão em L611.
   O critério original de 4 pt não os recupera. O experimento considera a caixa
   conjunta dos textos documentalmente pareados de nome e espessura.
2. **Faces fechadas não incorporadas:** a rede vetorial contém uma face interna
   fechada para L601 e outra para L607. O filtro de apoio de bordas da Etapa 7 não
   as incorporou, mantendo apenas os retângulos anteriores como alternativas.
   A face de L607 usa x = 862,32 a 1115,40 e y = 575,20 a 948,40 pt. Ela não é
   idêntica aos quatro candidatos anteriores, que incluem faces exteriores.
   Isso reduz a ambiguidade geométrica, mas não comprova por si o limite estrutural.
3. **L605 não pode ser resolvida pela esbeltez:** há indicação documental apontando
   para o polígono em U. Sua pouca área em relação à envoltória não demonstra que
   seja uma viga, nem que seja uma laje. Mantive a hipótese de contorno com a
   ressalva, sem rejeitá-la ou confirmá-la apenas por esse índice.
4. **L603 não foi resolvida com ajuste numérico:** o ensaio de normalização de
   0,001 pt não produziu movimentos na rede ensaiada nem fechou a face. Incluir
   barras como limites gera uma região artificial em torno do texto, limitada
   justamente pelas barras/eixos N13/N15. Esse resultado foi rejeitado.

O próximo ajuste do reconhecimento deve tratar o bloco nome+espessura como unidade
documental e separar reconhecimento de face de confirmação do domínio estrutural.
Não basta reduzir o rigor de fechamento, aumentar tolerâncias ou selecionar a
menor região pela proximidade.

## Método do experimento

Reutilizou-se a rede de segmentos da prancha, excluindo entidades aceitas de barras,
faixas e líderes, e eixos com setas reconhecidos pelo procedimento existente.
Bordas com apoio de hachuras mantêm sua evidência. As conexões das etiquetas foram
procuradas no bloco nome+espessura; foi exigida uma extremidade junto ao bloco e
a outra no interior da face. Não houve seleção pela distância da armadura ao nome.

As faces foram recuperadas com o Shapely já instalado, sem snapping, sem reparar
polígonos e sem alterar coordenadas. O nome está dentro da face em L601/L602/L607;
nos demais candidatos há um indicador entrando na face. Identificadores dos
segmentos do contorno e do indicador estão em `revisao.json`.

A rede produziu 85 faces, com 104 pontas pendentes e nenhum anel inválido; essas
faces **não são 85 lajes**. Apenas oito foram vinculadas a etiquetas nesta revisão.
Os vazios não foram descontados a partir de um inventário supostamente completo.

## Associação preliminar das armaduras distribuídas

São interseções entre contorno candidato e região gráfica da ocorrência. Não são
prova de que a barra inteira esteja fisicamente limitada à laje. Percentuais são
da **região gráfica original**, não área de aço ou fração resistente.

| Laje | Armaduras com evidência geométrica mais direta | Fonte da vinculação |
|---|---|---|
| L601, h12 | N27 — O001/R001; 90,5% da região gráfica | Nome dentro de face fechada |
| L602, h12 | N28 — O002/R002; 84,6% | Nome dentro de face fechada |
| L603, h20 | Não atribuídas neste ensaio | Sem contorno fechado recuperado |
| L604, h12 | N34 — O051/R051; 100% | Indicador D1886:0 |
| L605, h18 | N36 — O058/R058; 100%; outras incidências parciais abaixo | Indicador D1888:0, contorno em U ainda discutível |
| L606, h12 | N34 — O052/R052; 100% | Indicador D1887:0 |
| L607, h20 | N24 — O033/R033; 85,4%; N26 — O036/R036; 88,3% | Nome dentro de face fechada interna |
| L611, h12 | N32 — O007/R007; 99,3%; N29 — O010/R010; 63,4%; N4 — O018/R018; 55,0% | Indicador D1885:0 ligado ao bloco nome+h |
| L612, h12 | N9 — O006/R006; 99,3%; N4 — O015/R015; 55,4% | Indicador D1884:0 ligado ao bloco nome+h |

As ocorrências N4/O015 e N4/O018, assim como N34/O051 e N34/O052, são preservadas
separadamente. A marca igual não foi usada para atribuir uma à laje da outra.

**L605:** também existem interseções parciais com N25/O050 (2,2%), N40/O053 (18,4%),
N35/O055 (4,8%) e N39/O056 (4,8%). Elas foram registradas, mas não transformadas em
atribuições integrais à laje, nem automaticamente classificadas como residuais.
A diferença entre o contorno estreito em U e as regiões gráficas maiores precisa
de esclarecimento documental. A própria posição N36 está desenhada e distribuída
na faixa inferior apontada pelo indicador, o que constitui evidência adicional
para investigar esse contorno, sem confirmar a geometria física completa.

**L603:** o ponto da etiqueta está dentro das envoltórias N14/R034 e N13/R043,
mas isso é apenas uma indicação local, insuficiente para atribuir toda a armadura.
Há grande área da planta cuja continuidade em torno de L607 ainda não foi delimitada.
Não foi atribuído o restante das 35 ocorrências à L603 por exclusão ou por falta
de outro nome próximo.

## Armaduras localizadas

Também foram consultados os grupos localizados existentes, sem redistribuir barras:
há interseções de traços N21/N22 com o candidato de L607 e de um grupo N38 com o
candidato de L605. O JSON registra comprimentos gráficos intersectados, **não**
quantidade de barras nem atribuição integral do grupo. Contatos em bordas podem
envolver armaduras junto a interfaces e precisam de revisão específica.
O registro de inconsistência N38 permanece inalterado.

## Material para conferência

- [Mapa geral revisado](contornos_revisados.png).
- [Inventário do experimento](revisao.json), com áreas, percentuais, fontes e geometrias.
- Ampliações: [L601](L601_associacoes.png), [L602](L602_associacoes.png),
  [L604](L604_associacoes.png), [L605](L605_associacoes.png),
  [L606](L606_associacoes.png), [L607](L607_associacoes.png),
  [L611](L611_associacoes.png), [L612](L612_associacoes.png).

Roxo tracejado indica contorno candidato; azul indica apontador documental.
Nas ampliações, ciano mostra interseções das armaduras. Foram conferidos visualmente
o mapa geral e os trechos L611/L612. As bordas recuperadas têm vínculo documental
mais forte que a seleção por proximidade, mas todas continuam pendentes de confirmação
do engenheiro. Nenhuma nova validação humana foi inventada.

## Conclusão da avaliação

Conseguimos avançar na **associação preliminar**, especialmente L611/L612 e a face
interna de L607. O resultado da Etapa 7 subestimava o que o PDF permite recuperar
por causa do tratamento incompleto das etiquetas. Ainda não conseguimos associar
todas as armaduras a todas as lajes com segurança: L603 é a principal pendência,
e L605 exige distinguir a faixa em U do domínio interno adjacente.

Recomendo conferir primeiro os oito contornos desenhados, confirmar o significado
dos apontadores L605/L611/L612 e obter o limite de L603 na planta de formas. Só após
essa conferência deve-se integrar o ajuste ao inventário oficial. A revisão não
autoriza recortar barras, somar contribuições ou emitir apontamento resistente.

Os testes sintéticos e regressões desta revisão estão separados em
`test_review_slab_contours.py`; o resultado da suíte está em `testes.txt`.
