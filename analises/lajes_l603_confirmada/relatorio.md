# L603 ? contorno informado pelo engenheiro

Jo?o confirmou a forma do per?metro de L603 pela imagem marcada em vermelho.
A laje constitui **um ?nico dom?nio conectado, abrangendo os dois lados de L607**,
com um recorte central aberto na borda inferior. Foram preservados os recortes
menores indicados na imagem; n?o foi substitu?da a geometria por um ret?ngulo.

## Origem e precis?o

- **Confirma??o humana:** identifica??o de L603 e topologia do per?metro marcado.
- **Digitaliza??o pelo assistente:** v?rtices do tra?o vermelho escolhidos visualmente
  na imagem de 1199 ? 607 px, registrados em `confirmacao_joao_L603.json`.
- **Alinhamento ao PDF:** regress?es separadas para X e Y com cinco refer?ncias
  por eixo, associadas a coordenadas vetoriais e IDs documentados no JSON.
- **Valida??o m?trica:** preliminar; Jo?o n?o confirmou separadamente as coordenadas
  num?ricas digitalizadas. N?o se presume precis?o equivalente ? planta de formas.

Os res?duos quadr?ticos do ajuste s?o aproximadamente 0,96 px em X e 1,08 px em Y.
Eles medem o ajuste dos pontos escolhidos, n?o o erro total do contorno. Para
triagem de sensibilidade foi adotada uma margem explorat?ria de **8 pt PDF**,
considerando tra?o vermelho, escolha manual e alinhamento. Essa margem n?o ?
crit?rio normativo, toler?ncia executiva ou intervalo estat?stico de confian?a.
A eros?o/dilata??o usada nessa an?lise n?o altera o pol?gono registrado ou as barras.

A imagem original da conversa n?o foi obtida como arquivo local; por isso n?o h?
hash do bitmap. O JSON identifica essa origem e preserva os v?rtices escolhidos,
os pontos de registro e o hash do PDF a que se referem.

## Armaduras distribu?das

Foram encontradas **18 ocorr?ncias com interse??o positiva e presen?a no interior**
mesmo na an?lise conservadora com a margem adotada. Correspondem a 12 posi??es:
N1, N2, N3, N10, N11, N12, N13, N14, N15, N25, N30 e N31.
Posi??es repetidas permanecem ocorr?ncias distintas.

| Ocorr?ncia | Posi??o | Parcela da regi?o gr?fica dentro de L603 |
|---|---|---:|
| O008 / R008 | N2 | 79.9% |
| O011 / R011 | N30 | 92.0% |
| O013 / R013 | N11 | 91.2% |
| O019 / R019 | N25 | 96.8% |
| O020 / R020 | N12 | 91.6% |
| O021 / R021 | N31 | 92.3% |
| O026 / R026 | N10 | 100.0% |
| O027 / R027 | N10 | 100.0% |
| O029 / R029 | N3 | 81.9% |
| O030 / R030 | N3 | 84.5% |
| O031 / R031 | N15 | 94.0% |
| O032 / R032 | N15 | 93.2% |
| O034 / R034 | N14 | 100.0% |
| O035 / R035 | N14 | 100.0% |
| O041 / R041 | N1 | 93.2% |
| O042 / R042 | N1 | 94.0% |
| O043 / R043 | N13 | 95.2% |
| O044 / R044 | N13 | 96.5% |

Os percentuais se referem ? **regi?o gr?fica da ocorr?ncia**, n?o ? ?rea de a?o,
n?mero de barras ou contribui??o resistente. Uma regi?o gr?fica que cruza a borda
n?o comprova automaticamente atribui??o integral da barra ? laje, nem ancoragem.

H? outros **oito casos de sensibilidade de borda**, sem interse??o positiva no
pol?gono nominal: O006/N9, O007/N32, O010/N29, O015 e O018/N4, O033 e O047/N24,
e O036/N26. S? entram na vizinhan?a dilatada usada para avaliar incerteza m?trica;
**n?o foram atribu?dos ? L603**. N24/O033 e N26/O036 continuam relacionados ? regi?o
de L607. N?o foi examinada a contribui??o de extremidades ou ancoragens.

Os grupos localizados existentes tamb?m foram intersectados geometricamente.
O JSON distingue tra?os interiores de casos de borda, sem criar barras/grupos,
atribuir automaticamente o grupo inteiro ou alterar as quantidades. O registro
N38 e as quatro classifica??es humanas das composi??es anteriores ficam intactos.

## Artefatos e preserva??o

- [Contorno vermelho alinhado ao PDF](L603_contorno_confirmado.png).
- [Interse??es das armaduras](L603_armaduras.png).
- [Registro da confirma??o e digitaliza??o](confirmacao_joao_L603.json).
- [Invent?rio das interse??es](L603_associacoes.json).

A sobreposi??o foi examinada visualmente no PDF renderizado. O registro ? uma
camada adicional: n?o substitui nem apaga a pend?ncia hist?rica do reconhecimento
autom?tico, n?o apresenta a interven??o humana como sucesso do algoritmo e n?o
modifica o PDF ou as coordenadas vetoriais anteriores. O SHA-256 do PDF foi
verificado antes e depois da gera??o. N?o foram feitos c?lculos resistentes.

Os testes verificam alinhamento, rejei??o de documento diferente, validade e
conectividade do pol?gono, exclus?o de L607/L605, preserva??o de ocorr?ncias
espelhadas e aus?ncia de altera??o das entradas. A su?te completa passou: **139 testes em 62,880 s** (134 anteriores + cinco novos).
Registro em `testes.txt`.
