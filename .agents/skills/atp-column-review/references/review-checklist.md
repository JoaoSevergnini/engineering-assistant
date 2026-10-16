# Checklist de revisão de pilares em ATP

Usar os controles por pilar/trecho/encontro/grupo de barras conforme sua unidade
física. Separar geometria e armaduras sem perder suas dependências. Definir a
matriz antes da leitura; aplicar os estados do [contrato](review-contract.md).
O checklist é procedimento de revisão documental/normativa, não motor resistente.

## Geometria

| ID | Controle | Unidade/evidência necessária |
|---|---|---|
| G01 | Seção detalhe × forma | Contorno, cotas, raios, orientação e faces do trecho correto |
| G02 | Troca de seção | Seções inferior/superior, nível e deslocamento da transição; porções que morrem/continuam |
| G03 | Comprimento dos lances | Cota direta, diferença dos níveis e extensões físicas separados |
| G04 | Níveis detalhe × forma | Datum e referências principais/locais correspondentes |
| G05 | Nível de interrupção | Término do concreto e das barras por grupo/marca, referência do receptor |
| G06 | Multiplicador de armadura | IDs das formas × abrangência do título; desdobrar todos os IDs |
| G07 | Pilar da forma sem detalhe | Confronto forma → detalhamento por ID e por trecho/pavimento |
| G08 | Detalhe sem pilar correspondente na forma | Confronto detalhamento → forma; não confundir nascimento, morte ou revisão |

G07/G08 são confrontos independentes: conciliar apenas a lista TQS com o detalhe
não comprova cobertura das formas. Não basta um mesmo ID aparecer uma vez;
conferir todos os trechos esperados, incluindo emendas entre pranchas.
Executar conforme [geometria](geometry-review.md).

## Armaduras

| ID | Controle | Procedimento |
|---|---|---|
| A01 | Taxa e configuração TQS × detalhe | [Comparação longitudinal](longitudinal-comparison.md); comparação nominal sem concluir esforços |
| A02 | Esperas do bloco/viga de transição × lance | [Esperas](starter-bars-review.md); quantidade por bitola e origem física |
| A03 | Estribos usuais | [Transversais](transverse-reinforcement-review.md); item integral, nós e condições aplicáveis |
| A04 | Transversal de pilares-parede | Mesma referência; enquadramento por lâmina e área por metro de face |
| A05 | Diâmetro longitudinal mínimo/máximo | [Detalhamento longitudinal](longitudinal-detailing-review.md) |
| A06 | Distribuição das barras longitudinais na seção | Mesma referência; não confundir com distribuição dos estribos |
| A07 | Posição do traspasse | [Posição](lap-splice-position.md); maior topo incidente e etapa de concretagem |
| A08 | Armaduras complementares entre lances | [Esperas](starter-bars-review.md); acréscimos, mudança de bitola/seção e transferência documentada |
| A09 | Comprimentos de traspasses e esperas | [Aderência](bond-and-lap-length-review.md); separar ancoragem, sobreposição e critério de triagem |

Manter também os controles já existentes de geometria das esperas nos blocos
e de remissões entre pranchas. Não confundir HB geométrico com ancoragem normativa.

## Aplicação e encerramento

Declarar quais controles foram executados, parcialmente executados ou não
executados. Dado disponível ou regra escrita na skill não comprova execução.
Concluir por controle; ambiguidades de identificação bloqueiam apenas os
resultados individuais dependentes. Não afirmar “pilar verificado” com base
apenas em A01, A02 ou nos limites de diâmetro/espaçamento de A03.

A verificação aos esforços é atribuição do engenheiro no modo atual. Requisitos
dependentes de solicitações exigem sua informação/decisão, sem extração de
esforços TQS para dimensionamento automático neste fluxo.
