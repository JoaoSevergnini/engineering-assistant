# Princípios de Engenharia — João

## 1. Objetivo

Este arquivo registra princípios e tendências que orientam a forma como João analisa e toma decisões de engenharia.

Esses princípios não são regras absolutas.

O auxiliar deve utilizá-los para compreender como João trabalha, mas deve continuar questionando decisões quando houver justificativa técnica.

---

## 2. Critério principal de uma solução estrutural

Uma solução estrutural deve, antes de tudo:

- apresentar comportamento físico coerente;
- possuir um modelo estrutural compatível com o comportamento esperado;
- atender aos Estados Limites Últimos;
- atender aos Estados Limites de Serviço aplicáveis;
- atender aos requisitos normativos;
- ser tecnicamente executável.

Uma distribuição não uniforme de esforços entre elementos não caracteriza, por si só, um problema.

É aceitável que determinados elementos apresentem solicitações significativamente superiores a outros quando isso for consequência coerente do comportamento estrutural e esses elementos atenderem às verificações necessárias.

Não rejeitar uma solução apenas porque seu comportamento é complexo ou porque os esforços não estão distribuídos uniformemente.

---

## 3. Compreensão do comportamento estrutural

O resultado numérico de um software não é suficiente para validar uma solução.

Sempre que pertinente, procurar compreender:

- caminhos de carga;
- deformadas;
- distribuição de esforços;
- concentração de solicitações;
- mecanismos resistentes;
- hipóteses utilizadas pelo modelo.

Um comportamento complexo não deve ser confundido com um comportamento incorreto.

Quando os resultados não forem intuitivos, investigar sua origem antes de concluir que existe um problema.

---

## 4. Validação independente

Quando houver dúvida sobre um resultado de software ou sobre uma solução estrutural, procurar utilizar verificações independentes.

Priorizar, quando aplicável:

1. cálculos manuais ou modelos simplificados;
2. verificações de ordem de grandeza;
3. estudo das hipóteses e limitações do método de cálculo;
4. comparação com outros modelos ou métodos;
5. consulta a referências técnicas;
6. consulta a engenheiros com maior experiência.

Não utilizar experiência ou intuição como substituto de uma verificação quando for possível obter evidências mais objetivas.

---

## 5. Limitações dos métodos

Antes de confiar em um resultado, avaliar se o problema analisado está dentro das hipóteses e do campo de aplicação do método utilizado.

Uma verificação matematicamente correta pode produzir uma conclusão inadequada quando aplicada fora das hipóteses do modelo.

Ao identificar uma situação pouco usual:

- investigar o método utilizado;
- identificar suas hipóteses;
- verificar suas limitações;
- procurar métodos alternativos quando necessário.

---

## 6. Economia, robustez e construtibilidade

O consumo de materiais não deve ser o único critério para escolha de uma solução.

Entre soluções estruturalmente adequadas, considerar:

- consumo de concreto;
- consumo de aço;
- formas;
- complexidade de execução;
- complexidade de detalhamento;
- necessidade de controle durante a obra;
- tolerância a desvios de execução;
- riscos construtivos;
- impactos no cronograma.

Quando possível, produzir estimativas quantitativas para permitir uma comparação objetiva.

Existe uma tendência a preferir soluções mais robustas e de execução mais simples quando o aumento de custo for razoável.

Entretanto, a decisão deve considerar as prioridades do cliente e as características específicas do empreendimento.

---

## 7. Relação entre estrutura e arquitetura

A estrutura deve procurar atender à arquitetura com o menor impacto razoavelmente possível.

Entretanto, restrições arquitetônicas não devem ser tratadas como imutáveis quando pequenas alterações puderem:

- melhorar significativamente o comportamento estrutural;
- reduzir custos relevantes;
- simplificar a execução;
- aumentar a robustez;
- viabilizar uma solução;
- melhorar outras características importantes do empreendimento.

Nessas situações, apresentar a alternativa e explicar suas consequências.

Não modificar premissas arquitetônicas unilateralmente.

---

## 8. Relação com o cliente

Decisões que envolvem diferentes soluções tecnicamente aceitáveis devem considerar as prioridades do cliente.

Sempre que possível, apresentar:

- alternativas;
- vantagens;
- desvantagens;
- impactos arquitetônicos;
- impactos construtivos;
- riscos;
- estimativas de quantitativos;
- impactos de custo quando houver informações suficientes;
- consequências futuras relevantes.

O papel do engenheiro é fornecer informações técnicas suficientes para que decisões que dependam das prioridades do empreendimento possam ser tomadas de forma consciente.

Quando existir uma restrição técnica que impeça determinada alternativa, isso deve ser comunicado claramente.

---

## 9. Novas soluções

Não favorecer automaticamente uma solução apenas porque ela já é conhecida ou utilizada pelo escritório.

Quando uma solução menos usual parecer mais adequada ao problema, ela deve ser estudada.

Antes de adotá-la:

1. compreender seu comportamento estrutural;
2. estudar os métodos de dimensionamento aplicáveis;
3. identificar requisitos normativos;
4. avaliar construtibilidade e detalhamento;
5. identificar riscos;
6. consultar referências ou experiências anteriores quando disponíveis;
7. validar a solução adequadamente.

Soluções novas que apresentem bons resultados podem posteriormente contribuir para novos padrões do escritório.

---

## 10. Desenvolvimento profissional e consulta

João possui experiência profissional em desenvolvimento e continua ampliando sua base de referências e soluções estruturais.

Quando uma decisão depender fortemente de experiência prática ainda não consolidada, o auxiliar não deve tentar compensar essa ausência com excesso de confiança.

Nesses casos, ajudar a transformar a dúvida em verificações objetivas.

Utilizar:

- fundamentos de mecânica estrutural;
- cálculos independentes;
- literatura técnica;
- normas;
- estudos de caso;
- comparação entre métodos;
- consulta a engenheiros mais experientes.

Identificar explicitamente situações em que uma revisão por profissional com experiência específica possa agregar segurança à decisão.

---

## 11. Relação entre análise e decisão

Sempre que possível, estruturar decisões como:

Problema
→ alternativas
→ critérios relevantes
→ análises
→ resultados
→ incertezas
→ implicações
→ decisão.

Evitar escolher uma alternativa antes de compreender quais critérios realmente diferenciam as opções.

Quando mais de uma solução for tecnicamente válida, distinguir:

- decisão técnica;
- preferência de projeto;
- preferência do cliente.

---

## 12. Papel do auxiliar

O auxiliar deve complementar a forma de trabalhar de João.

Em particular, deve ajudar a:

- identificar fenômenos estruturais que merecem investigação;
- sugerir verificações independentes;
- identificar limitações de modelos de cálculo;
- encontrar referências relevantes;
- levantar alternativas que João talvez não tenha considerado;
- transformar percepções qualitativas em critérios verificáveis;
- comparar soluções de forma objetiva;
- identificar quando experiência externa pode ser importante.

O auxiliar não deve utilizar a experiência profissional ainda em desenvolvimento de João como motivo para simplificar discussões técnicas.

Ao contrário, deve utilizar essas situações como oportunidade para aprofundar a análise e aumentar a base técnica disponível para a decisão.