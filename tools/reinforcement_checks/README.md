# Flexão positiva: golden e regiões geométricas

Camada pequena de orquestração, separada de beam_mapping. Consome modelos
existentes e usa exclusivamente a API pública do Concretopy para áreas, alturas
úteis, equilíbrio, resistência e diagnósticos. Nenhuma equação resistente local.

```powershell
python -B tools/reinforcement_checks/v501_positive_flexure.py --concretopy-root ../concretopy --output analises/pranchas/V501_positive_flexure_check.json
python -B -m unittest discover -s tools/reinforcement_checks -p "test_*.py" -v
```

Concretopy não está instalado no Python atual; a CLI recebe explicitamente a raiz
do repositório local, sem instalar/copiar/alterar a biblioteca. O teste de integração
usa o repositório irmão `../concretopy`. API: `check_case(detail,tqs,positioned,
mapping,raw,api)`.

A origem da série é auditada no raw existente: VGESFS, registro M MX., vão,
valores normalizados, envelope max, stage model_input, kN.m. A natureza Msk é
declarada pelo engenheiro no pedido deste golden case. Não basta nome max. Valores
negativos são excluídos da governança; não há interpolação ou valor absoluto.

N5 precisa conservar sua composição documental e cobrir as 13 seções. Isso não
comprova desenvolvimento/ancoragem. A seção resistente usa o estribo documental
da região do ponto governante; não afirma capacidade uniforme nas outras regiões.
Fck é selecionado somente entre campos com unidade original MPa. RELDTVeT é
excluído. Cobrimento inferior TQS é identificado como dado do modelo, não como
confirmação de execução. Gamma_f é obtido explicitamente dos registros autorizados;
gamma_c/gamma_s e Es usam defaults públicos registrados do Concretopy.

`materials.py` interpreta CA50/CA-50/CA-50A como CA-50, fyk=500 MPa, pela regra
confirmada `engineer_confirmed_ca50_fyk_500_v1`. Independente de beam id,
preserva texto original, classe normalizada, fyk, regra e proveniência de cada
observação. A equivalência CA-50A é limitada à resistência característica neste
fluxo. Qualquer designação operacional desconhecida, mesmo junto de uma conhecida,
ou ausência de classe bloqueia a verificação, sem usar Aco.fyk default.
RELDTVeT continua excluído, com observações preservadas separadamente.
Conflitos textuais históricos não são apagados do consolidado; não geram conflito
do fyk derivado. Não existe tabela de outras classes. O antigo override
`--fyk-resolution` foi removido para impedir bypass de classe desconhecida.

Resultado mantém a dataclass completa do Concretopy e converte exclusivamente
kN.cm para kN.m (divisão por 100). Utilização usa Mk equivalente recebido, nunca
MRd diretamente. Ductilidade, hipóteses resistentes, mínimo e ancoragem são campos
independentes. Mínimo não é solicitado nesta etapa.

CLI audita hashes do mapping e raw, registra hashes dos inputs e da implementação
Concretopy e interpretador de materiais. Não altera modelos/fontes ou Concretopy.
O golden real usa o aço derivado dos artefatos pela regra confirmada, executa
a API real com d omitido e verifica capacidade, utilização e diagnósticos.
Os testes de materiais cobrem aliases equivalentes, origem preservada, ausente,
desconhecido, exclusão de RELDTVeT e imutabilidade.

## Diagrama linear de Msk (regra confirmada em 04/10/2026)

`moment_diagram.MomentDiagram(points, provenance)` recebe qualquer sequência
estritamente crescente com pelo menos dois pontos. `diagram_from_tqs` reutiliza
a auditoria M MX. e as positions existentes. Métodos: `moment_at_x(x)`,
`find_crossings(M_limit)`, `positive_maximum()` e `as_dict()`.
Sem extrapolação, sem gaps conectados, com endpoints documentais exatos.
Usa Decimal com precisão explícita 50; resultados derivados conservam strings
decimais operacionais e números float compatíveis com os modelos existentes.
Cruzamentos são analíticos, ordenados e deduplicados por coordenada exata;
segmentos coincidentes retornam intervalos. Gaps tornam a busca incompleta.

Golden independente: `python -B tools/reinforcement_checks/v1001_moment_interpolation.py
--concretopy-root ../concretopy --output analises/pranchas/V1001_moment_linear_interpolation.json`.
Consulta o término documental de N3 e chama Concretopy para N5 isolada na
configuração auditada à esquerda do evento. Não altera o algoritmo discreto
anterior das regiões, nem escolhe corte normativo ou avalia ancoragem.

## Verificação genérica por regiões de um vão mapeado


```powershell
python -B tools/reinforcement_checks/positive_flexure.py --detail analises/pranchas/V501_V503_beam_model.json --tqs analises/pranchas/V501_tqs.json --positioned analises/pranchas/V501_tqs_positions.json --mapping analises/pranchas/V501_beam_mapping.json --raw analises/pranchas/V501_tqs_raw.json --concretopy-root ../concretopy --output analises/pranchas/V501_positive_flexure_regions.json
```

`flexure_regions.decompose_regions(bars, domain, transverse_regions=None)` é
função geométrica pura: eventos de início/fim, domínio físico explícito e mudanças
transversais. `positive_flexure.check_positive_flexure(...)` orquestra cada região.
`tqs_moments.audited_moment_series` é compartilhada com o golden; campos materiais
documentais são compartilhados em materials.py. O script V501 permanece fixture
de integração/regressão, sem ser arquitetura definitiva da função genérica.

Domínio padrão: eixo esquerdo até eixo direito do único vão físico mapeado,
incluindo as seções TQS internas aos apoios. Não se extrapola estribo para os apoios.
Regiões sem operandos transversais conhecidos permanecem não resolvidas.

### Limites e camadas

Intervalos documentais de barras continuam fechados. Os interiores entre eventos
são inicialmente abertos. Cada limite é incluído na região direita se a configuração
fechada coincide; senão na esquerda se coincide; senão cria região pontual fechada.
`include_start/include_end` são explícitos. Cada seção pertence a uma única região,
sem epsilon. No encontro fim/início de marcas, o ponto pode conter ambas. No
encontro de estribos diferentes, a geometria do ponto fica não resolvida.

O índice 1-based do vetor layers do beam_model representa a camada a partir da
mesma face inferior. Somam-se quantidades apenas com essa identidade documental,
face lower e mesma bitola. Camadas sem posição/face conhecida não são fundidas.
Bitolas diferentes na mesma camada e lacunas de camadas são preservadas e bloqueadas:
Concretopy admite uma bitola por camada e não se pode colapsar índices físicos
para gerar d automático. Não há área/bitola equivalente.

Por padrão, limites dos estribos do mapping subdividem a configuração transversal,
com seção retangular e cobrimento documentado ou inferior TQS. A API aceita também
regiões transversais explicitamente fornecidas com proveniência, para dados de
seção/cobrimento por trecho; não infere variações de cortes sem abscissa.
Intervalos desconhecidos não viram ausência. Função longitudinal não classificada
permanece candidata não resolvida, impedindo composição falsa.

### Resultado

Conserva composição por camada/marca, geometria, pontos (inclusive negativos),
governança positiva, chamada e dataclass Concretopy completa, MRd/Mk e utilização,
diagnósticos separados e proveniência. Referências compartilhadas evitam repetir
arquivos-fontes. `demand_not_sampled` preserva região sem ponto; `no_positive_demand`
preserva negativos sem fabricar solicitação. Dados ausentes/arranjos não suportados
impedem somente chamadas dependentes. Não há cálculo resistente/interpolação local.

Resumo enumera verificadas, não resolvidas, sem pontos, sem positivos e não
verificadas. `all_checked_regions_capacity_sufficient` refere-se somente às
chamadas concluídas; é null se nenhuma foi concluída, e nunca significa vão aprovado.
`incomplete` e diagnósticos de cada região expõem todas as lacunas.
