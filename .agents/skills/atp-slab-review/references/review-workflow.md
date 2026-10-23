# Fluxo operacional de ATP de lajes

Este procedimento pode ser conduzido pelo agente com ferramentas compatíveis,
leitura documental assistida e intervenção do engenheiro. As oito etapas são
procedimentos de engenharia; sua documentação não implementa os algoritmos.
Consultar [ferramentas](existing-tools.md) antes de executar um recurso e
[critérios](review-criteria.md) para os controles G01–A08.

## Preparação e registros mínimos

Definir projeto, pavimento, lajes/regiões incluídas e destino dos registros.
Abrir matriz por objeto físico, região, direção/face e controle esperado.
Manter inventário documental, observações, geometrias/referências, decisões,
cálculos/diagramas e resultados em arquivos revisáveis do projeto; não há
estrutura de pastas ou formato único obrigatório.

Usar os [contratos 1A](contracts.md) onde correspondam aos dados. Campos ainda
não representados (quantidade, comprimento, face, materiais, conjuntos físicos,
diagramas locais) ficam em evidências e registros complementares referenciados,
sem alegar que já existem atributos ou motores para eles em tools/slab_review.
Identificar unidades e sistema de coordenadas de cada geometria.

## Etapa 1 — Inventário documental

Localizar formas, positivas H/V, negativas H/V, diagramas DXF e detalhes
complementares, inclusive vigas, cortes, bordas, furos e juntas referenciados.
Registrar ID, caminho, tipo, revisão, abrangência, página e hash quando disponível.
Separar revisão do desenho, processamento TQS e comentários do revisor.

Reconciliar lajes presentes em cada fonte, títulos das pranchas e regiões
sobrepostas; documento mais recente isoladamente não prova emissão coordenada.
Registrar incompatibilidades e o par de fontes. Documento faltante mantém
visível o controle dependente; não encerra a revisão dos demais elementos.

**Saída:** inventário, escopo, revisões em conflito e matriz inicial de controles.
O manifesto S07 serve como exemplo documental, sem transferir seus parâmetros.

## Etapa 2 — Geometria das lajes

Ler primeiramente as formas: nome, contorno, espessura, nível, aberturas, apoios
por vigas/cintas e encontros. Comparar nome/h/nível com pranchas de armadura,
registrando cada leitura e divergência separadamente.

O nível indicado corresponde à face superior. Obter a face inferior por
z_inferior[m] = z_superior[m] − h[cm]/100, somente com h e datum compatíveis.
Preservar nível original, espessura local e cálculo derivado. Um rebaixo ou
zona espessada pertence à mesma laje quando essa for a identidade do projeto;
não criar lajes artificiais para acomodar espessuras diferentes.

Distinguir contorno estrutural, zona de espessura, abertura confirmada,
envoltória de distribuição e região de ancoragem. Identificar faces dos apoios,
não apenas eixos, e registrar lajes incidentes de cada lado. Para extensão de
borda, obter o menor vão livre global entre faces das vigas de apoio. Lajes
irregulares ou apoio não esclarecido podem exigir decisão do engenheiro sobre
esse vão; manter pendente somente o controle correspondente.

Contorno parcial permite análises locais com limites comprovados, sem concluir
cobertura integral. Candidatos do PoC não se tornam formas confirmadas.

**Saída:** cadastro de lajes e zonas, referências físicas e conflitos G01–G02.

## Etapa 3 — Identificação das armaduras

Extrair automaticamente o que a ferramenta reconhecer e completar por leitura
assistida: marca, bitola, espaçamento, quantidade, comprimento nominal e suas
parcelas, direção, distribuição, face superior/inferior, detalhes e remissões.
Confrontar chamadas e tabelas; não deduzir espaçamento da quantidade sem
convenção demonstrada. Comprimento desenvolvido, projeção reta e comprimento
eficaz ancorado são distintos.

Conservar alternativas de chamada–barra–eixo e geometrias sem associação.
Registrar armadura localizada como tal, sem impor faixa fictícia por metro.
Marca N, ocorrência gráfica e conjunto físico têm identidades diferentes.

Identificar base, complemento, traspasse ou função desconhecida com evidência.
Positivas de base e complemento podem estar intercaladas na mesma camada;
confirmar essa disposição e a ordem entre direções no próprio projeto.
Na S07, H primeiro/V segundo foi decisão local, não regra universal.

Procurar detalhes inclinados, chamadas não extraídas e instruções como
“VER ARMADURA NAS VIGAS”. Confirmar visualmente dados decisivos e permitir
informação manual atribuída ao engenheiro.

**Saída:** ocorrências, fontes, geometrias candidatas e pendências de leitura.

## Etapa 4 — Composição das regiões resistentes

Reconstruir onde cada conjunto atua e particionar quando mudarem membros,
espessura, material ou posição vertical. Preservar ocorrências individuais,
identidades físicas, relações, geometrias, materiais e composições.

Sobreposição gráfica não prova independência nem atuação conjunta. Evitar dupla
contagem da mesma base, chamadas repetidas e emendas tratadas como aço adicional.
A atuação de base com um reforço não autoriza automaticamente soma de um terceiro.

Distinguir presença gráfica/física de contribuição resistente desenvolvida.
Sem ancoragem ou composição comprovada, manter capacidade conjunta pendente;
capacidades individuais podem continuar sendo examinadas. A localização
documental de uma barra não é validação de seu comprimento eficaz.

**Saída:** regiões de composição comprovada, alternativas e membros remanescentes
necessários à revisão das interrupções.

## Etapa 5 — Resistência à flexão

Para cada região/direção/face, reunir h, cobrimento, bitolas, espaçamentos,
materiais, centros das barras, d e largura de referência. Espessura ou posição
não confirmada impede apenas os cálculos dependentes, sem apagar As documental.

Selecionar API do Concretopy compatível, conforme existing-tools. Usar d explícito
quando necessário para representar a posição real e não herdar empilhamento de
vigas. Se houver intercalação de bitolas, justificar a representação equivalente
e seus limites antes de utilizá-la; sem representação válida, encaminhar o caso
ao engenheiro e manter a capacidade pendente.

Compatibilizar largura da faixa e momento por unidade de largura. Guardar inputs,
unidades, versão/hash da função, coeficientes, resultado bruto e diagnósticos de
hipóteses, escoamento, ductilidade e mínimo. Valor MRd disponível não aprova todos
esses controles. O mínimo de vigas do motor não valida As,min de lajes.

**Saída:** resistências aplicáveis e diagnósticos por região, ou pendência técnica
específica; apresentação conforme A02 em review-criteria.

## Etapa 6 — Diagramas DXF e associação espacial

Identificar fonte/processamento, direção, layers, unidade, sinal e natureza.
Separar linha de referência da deformação gráfica do diagrama. Calibrar amplitude
contra rótulos e geometria; verificar linhas regulares e eixos locais irregulares,
sem impor escala ou passo da S07 a outra exportação.

Registrar linha física com ID persistente, referência espacial, segmentos e
valores locais. Não contar um segmento como outra linha nem usar só uma coordenada
de eixo como prova de identidade. Preservar trechos sem informação, filtros,
alternativas e evidências de calibração.

Alinhar DXF, formas e armaduras com âncoras físicas independentes, transformações,
unidades e resíduos. Escala gráfica de momento e transformação da planta são
operações distintas. Não remover apoios da demanda sem critério justificado.
Não interpolar espacialmente entre linhas como condição de início da análise.

Recortar cada linha pela região e obter os indicadores definidos em A02:
média dos máximos por linha e média dos três maiores máximos de linhas distintas,
além de picos individuais e máximo absoluto. Usar valores locais para cortes.
Preservar segmentos/posição longitudinal para futura análise em seções
transversais alinhadas, que ainda não possui procedimento automatizado integrado.

Os scripts S07 de médias são parciais: não fornecem cadastro completo de linhas
nem o segundo indicador. Onde não houver ferramenta validada, realizar avaliação
assistida com memória rastreável ou registrar controle não executado/inconclusivo;
não inventar um processamento que não ocorreu.

**Saída:** diagramas/associações e indicadores com cobertura e limitações explícitas.

## Etapa 7 — Controles independentes

Aplicar G01–G02 e A01–A08 de review-criteria, por laje, região e direção.
Concluir somente o controle sustentado pelos dados. Uma falha conhecida não
desaparece porque outro controle está pendente. Registrar também controles
ainda não executados e inaplicabilidades justificadas.

Quando uma ferramenta não cobrir o caso, verificar por leitura/cálculo assistido
compatível ou solicitar avaliação específica; não desenvolver um algoritmo
complexo nem suspender todo o pavimento por uma exceção.

## Etapa 8 — Diagnóstico e apresentação

Produzir como entrega principal os PDFs gráficos de comparação resistência ×
solicitação definidos em [reporting](reporting.md), por prancha/conjunto de regiões
e, quando necessário, por direção/face. Usar a prancha original, delimitações e IDs,
configurações de aço, resistência, os dois indicadores, n de linhas, relações
compatíveis, legenda e quadro lateral com resultados e pendências.

Não restringir a seleção às regiões com resistência publicada: incluir as
pendentes no mapa ou quadro específico e reconciliar os IDs com o inventário.
Se o segundo indicador não puder ser obtido, manter o primeiro válido e indicar
o motivo, sem inventar média de três linhas. Identificar o indicador que governa
cada camada visual; nenhuma comparação favorável equivale a aprovação estrutural.

Conferir legibilidade da prancha e dos rótulos por renderização, ampliando detalhes.
Dividir PDFs/páginas quando necessário, preferindo gráficos vetoriais. Usar o
formato S07 como referência visual, sem transferir parâmetros do caso e sem
importar seus geradores com efeitos globais. Não existe gerador integrado no 1A.

O relatório consolidado complementar reúne apontamentos, limitações e cobertura
e remete aos PDFs; não os substitui. Em falta de dados ou ferramenta compatível,
registrar precisamente quais PDFs/comparações estão pendentes, mantendo as entregas
parciais. Submeter seleção e redação definitiva dos apontamentos ao engenheiro;
não publicar todos os FAIL automaticamente.

## Pendências, decisões e correções

1. Identificar dado, objeto e controles afetados, separando tarefa não realizada
   de informação efetivamente ausente no projeto.
2. Procurar em chamada, tabela, forma, corte, detalhe genérico, viga referenciada
   e documentos de revisão disponíveis.
3. Se continuar ambíguo, formular pedido localizado ao engenheiro com alternativas,
   evidências e consequência; prosseguir nos controles independentes.
4. Registrar resposta e origem com CONFIRM/CORRECT/PROVIDE, autor, data com fuso,
   justificativa e escopo físico/documental; não fabricar confirmação em seu nome.
5. Atualizar explicitamente as entidades consumidoras e a disponibilidade dos
   dados; dado liberado não implica controle aprovado.
6. Reavaliar os controles dependentes antes de utilizar seus resultados como
   vigentes. Preservar o resultado anterior e o motivo da substituição no
   histórico do projeto, fora de atributos inexistentes do contrato 1A.
7. Reemitir tabelas, mapas e apontamentos afetados; uma aceitação anterior não
   se transfere automaticamente para o resultado corrigido.

Não há propagação/invalidação automática no código. Manter relação simples
dado/evidência → controles/entregas afetados. Se o impacto ainda for desconhecido,
delimitar o subconjunto afetado para revisão; controles comprovadamente
independentes conservam validade. Usar os estados existentes, sem inventar
um novo enum de “obsoleto”: a versão antiga fica arquivada e explicitamente
fora da seleção vigente até reavaliação.
