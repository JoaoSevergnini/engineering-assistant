# Revisão negativa de apoios extremos — implementação

## Arquitetura e leitura

Foram consultados AGENTS.md, reinforcement-review/SKILL.md, referências negativas e de términos/intermediários, support_geometry, support_anchorage, longitudinal_review, negative_detailing, reprodutor e goldens V516/V517, API pública atual de flexão/ancoragem do Concretopy e primitiva existente de espaçamento mínimo. A política geométrica existente de igualdade não possui tolerância geral de engenharia; não foi criada uma.

A camada semântica nova é `negative_end_support_review`: `review_negative_end_support` confirma END/COLUMN e descobre marcas que realmente chegam à face; `check_negative_end_support` verifica cada peça. `prepare_reinforcement`, `composition_capacity`, regra terminal S1/S13, lb básico e nó negativo existente foram reutilizados. A pequena extração `negative_end_vertical_bend_limits` evita duplicar a expressão geométrica já presente; saídas legadas permanecem exatas. Não há novo motor de flexão/ancoragem nem mudanças em Concretopy.

## Regras e fontes

`engineer_confirmed_negative_end_support_vertical_bend_v1`: perna mínima=min(h_total−c−φ_estribo,2lb_básico), cm. Altura total, bitola própria, POOR confirmado; sem α=0,7 ou horizontal+vertical equivalente. `bend_documents` associa marca/lado/orientação vertical/comprimento/fonte; alternativamente end_bend por lado explicitamente documentado. Na prancha V516/V517, N4 tem 40 cm e N7 45 cm de perna escrita, com provenance na página 1. Não estimar dobra inexistente.

Resistência terminal usa S1 LEFT/S13 RIGHT diretamente, pelo `engineer_confirmed_negative_support_terminal_section_demand_v1`; geometria vem de SupportGeometry, nunca da seção TQS. Capacidade e necessidade são controles independentes da dobra. Comparação sem a marca demonstra necessidade terminal, preservando seus demais usos físicos. Não concluir redução de N7: peça participa junto a P1.

`engineer_confirmed_negative_reinforcement_vibrator_clearance_v1`: pelo menos um vão livre ≥4 cm. Não são 4 cm entre eixos nem em todos os pares. Centros reais de cada barra são necessários; verificar todos os demais mínimos com Concretopy.normas.espacamento_min_arm_long_viga, sem duplicar equação. Default agregado 16 mm é explicitamente registrado como contrato atual; agregado real e todas as prescrições normativas não são certificados.

`engineer_confirmed_column_interference_effective_cover_v1`: quando a dimensão perpendicular documentada do pilar equivale à largura da viga, sobrepor apenas no controle transversal c_eff=c_real+2,5 cm. Registrar b_useful=b−2c_eff e largura dentro do estribo real. Não alterar seção, d, MRd, lb ou posições físicas; não redistribuir barras automaticamente. Sem dimensão/fonte, INCONCLUSIVE. Default igualdade exata; qualquer tolerância fornecida exige provenance explícita do chamador. Dimensão não equivalente torna somente essa hipótese NOT_APPLICABLE.

## Golden e resultados

V516 P5/N4: 3Ø16; S1 Msk=−31,165533700 kNm; MRd=118,167324258 kNm; Mk=84,405231613 kNm; d=47,9 cm; flexão PASS. V517: S1 Msk=−32,832664200 kNm; mesma capacidade, PASS. lb próprio=62,939073262 cm; 2lb=125,878146523 cm. Espaço reto=21,5 cm, insuficiente. Perna mínima=48,7 cm; escrita=40 cm; margem=−8,7 cm; geometria FAIL.

V516 P6/N7: 2Ø20; S13 Msk=−17,063571000 kNm; MRd=122,221132129 kNm; Mk=87,300808664 kNm; d=47,7 cm; flexão PASS. V517: S13 Msk=−20,456671900 kNm; mesma capacidade, PASS. lb próprio=78,673841577 cm; 2lb=157,347683154 cm. Espaço reto=21,5 cm, insuficiente. Perna mínima=48,7 cm; escrita=45 cm; margem=−3,7 cm; geometria FAIL.

Os controles transversais reais permanecem INCONCLUSIVE: não há centros horizontais cotados no modelo nem dimensão perpendicular documentada de P5/P6. Os 24 cm da tabela de apoios são longitudinais e não foram reutilizados como dimensão perpendicular. Resistência da ancoragem curva permanece separada e não verificada. Relatório completo: V516_V517_negative_reinforcement_review.md, seção 14.

## Testes e regressões

40 testes novos do módulo: LEFT/RIGHT, PASS/equality/FAIL, governância geométrica/2lb, altura total, fonte/ausência/valor inválido da dobra, ausência de equivalente reto/gancho reduzido, S1/S13, independência entre flexão/dobra/dados faltantes, ancoragem reta, descoberta automática de marcas, identidade global, corredor maior/igual/menor que 4 cm, somente um corredor suficiente, mínimos restantes, coberturas transversais, dimensão perpendicular/tolerância com provenance, inputs invariantes e otimização null. Mais 4 regressões reais cobrem P5/N4, P6/N7, flexão independente e pendências geométricas.

Engineering-assistant: **663 aprovados**, 39+30+34+560. Concretopy: **405 aprovados**. quick_validate válido; git diff --check limpo. SHA-256 de 174 arquivos protegidos intactos; todos os dados/resultados anteriores V516/V517 e nós legados comparados exatamente. Os goldens positivos, SCALING, eventos coincidentes, ANCHORAGE_BEYOND_INTERMEDIATE_SUPPORT, S1/S13, sinal e políticas de gaps/extrapolação foram preservados.

## Limitações e conclusão

A falha geométrica da perna não é falha de flexão. Ancoragem curva, pino/raio, confinamento, interferências completas do nó/pilar, agregado real, alinhamento de corredores entre camadas e fabricação não são aprovados. Mínimos/corredor reais precisam de coordenadas transversais; interferência precisa de dimensão perpendicular. Faltas não bloqueiam controles independentes.

Insuficiência junto a P1 e N8/LEFT permanecem; N8/N9 RIGHT continuam aprovadas desde a face de P1, sem alterações. Aprovação global fora de escopo. A preferência futura por menor bitola em uma camada foi apenas documentada com suas condições globais. Não se propôs correção, redução, economia, nova armadura ou redesenho. selected_solution=null; detailing_optimization=null.

## Arquivos criados/alterados

- `tools/reinforcement_checks/negative_end_support_review.py`
- `tools/reinforcement_checks/negative_detailing.py`
- `tools/reinforcement_checks/test_negative_end_support_review.py`
- `tools/reinforcement_checks/test_v516_v517_negative.py`
- `analises/pranchas/validar_v516_v517_negativo.py`
- `analises/pranchas/V516_negative_reinforcement_review.json`
- `analises/pranchas/V517_negative_reinforcement_review.json`
- `analises/pranchas/V516_V517_negative_review_validation.json`
- `.agents/skills/reinforcement-review/SKILL.md`
- `.agents/skills/reinforcement-review/references/negative-end-support.md`
- `.agents/skills/reinforcement-review/references/negative-longitudinal-review.md`
- `tools/reinforcement_checks/README.md`
- `tools/reinforcement_checks/longitudinal_review.md`
- `.codex/analises/V516_V517_negative_reinforcement_review.md`
- `.codex/analises/negative_end_support_review_implementation.md`
