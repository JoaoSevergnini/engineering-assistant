# Selecao de cortante para decalagem longitudinal

Identificador: `engineer_confirmed_al_shear_selection_v1`.
Origem: regra de workflow confirmada expressamente pelo engenheiro em
2026-10-05. Nao e transcricao nem requisito normativo independente.
Status atual: selecao automatica do vao implementada em `tqs_shear.py` e
integrada em `bar_scaling.py`, validada pelos goldens V1001/V536/V565.
A verificacao de ancoragem em apoio continua fora desse workflow.

Atualizacao documental em 05/10/2026: o status anterior, "selecao automatica
e verificacao N3 nao implementadas", descrevia a etapa anterior a integracao.
Foi superado pela implementacao e goldens; nenhuma regra fisica foi alterada.

## A. Escalonamento da armadura ao longo do vao

Para interrupcao/escalonamento de armadura longitudinal dentro de um vao:

```text
Vk_used = max(abs(Vk(x))) em todo o vao fisico analisado
```

A magnitude caracteristica governante e a de todo o vao, nao somente a do
ponto onde uma barra termina. No fluxo validado, usar os valores discretos
validos de ambas as envoltorias caracteristicas VGESFS Q MX./Q MN., nas
13 positions existentes, inclusive pontos internos aos apoios do mesmo vao.
Nao extrapolar aos eixos nem gerar discretizacao adicional: em cada segmento
linear, o maximo de modulo ocorre em um endpoint. Conservar todos os empates,
serie, secao, x, Vk com sinal, magnitude, fontes e regra. Serie faltante,
incompleta, ambigua ou divergente do raw bloqueia a selecao dependente.

## B. Ancoragem em apoio

Para ancoragem em determinado apoio:

```text
Vk_used = max(abs(Vk(x))) somente na regiao do apoio analisado
```

Nao utilizar automaticamente o maximo de todo o vao para verificar apoio.
PENDENCIA EXPLICITA: a definicao espacial exata da regiao do apoio sera
formalizada quando implementada a verificacao de apoio. Nao se inventam
limites por eixo, face, largura, altura util ou outra extensao nesta etapa.

## Fronteira de responsabilidades

engineering-assistant: diagrama Vk(x) -> contexto -> seleciona Vk_used.
Concretopy: Vk_used + concreto + b + d explicito -> calcula al.

O chamador deve entregar `vk_abs_kn` como magnitude nao negativa em kN,
com `gamma_f` para obter Vsd. A API nao aplica abs(), nao recebe diagramas,
vao/apoio/x, nao escolhe regioes e nao sabe por que o esforco foi selecionado.
A selecao do d tambem pertence ao chamador; nao misturar d global e d de
camadas em etapas de uma mesma chamada.

A API `calcular_al` fornece al_base e al limitado, separadamente de
fbd/lb/lb_min/lb_nec. Nao soma al+lb ou al+10phi nem decide corte ou aprova
ancoragem. A primitiva Concretopy nao seleciona esforcos ou pontos TQS. A orquestracao
de escalonamento e implementada pelo assistente, conforme
[procedimento operacional da Skill](../../.agents/skills/reinforcement-review/references/positive-bar-scaling.md).
Apoio e grampos continuam fora dessa verificacao.

## Atualização de apoio em 06/10/2026

A exploração de apoio agora usa pares selecionados pelo chamador conforme
[procedimento de apoio positivo](../../.agents/skills/reinforcement-review/references/positive-end-support.md).
No golden V536/V565, S1 no eixo esquerdo foi confirmada. A pendência de uma
definição espacial genérica permanece; não transportar o máximo de todo o
vão do escalonamento para o apoio. P1 e P2 exigem chamadas independentes,
cada uma com seu Vk e al recalculado pela API.

Para controles longitudinais equivalentes de apoio INTERMEDIATE sem positivo, consultar [support_anchorage.md](support_anchorage.md): evento explícito de entrada na face interna e composição anterior, confirmação do chamador, máximo módulo das duas séries do vão. Esta extensão não altera o cálculo B dos apoios END nem cria regra de redução de ancoragem.
