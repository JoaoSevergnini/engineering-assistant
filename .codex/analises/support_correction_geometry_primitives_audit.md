# Auditoria prévia — primitivas de cabimento

06/10/2026, antes da implementação de correção orientada pelo detalhamento.

Encontradas `concretopy.normas.espacamento_min_arm_long_viga` (cm) e `concretopy.detalhamento.arranjos.numero_barras_maximo_camada`. A primeira retorna max(phi/10,2,1,2×agregado/10); o parâmetro padrão de agregado=16 mm resulta em 1,92 cm, não governante, reproduzindo exatamente max(2 cm,phi_cm) para a série considerada. A rotina reutilizará essa primitiva e registrará o parâmetro de compatibilidade; não afirma que 16 mm seja o agregado do projeto nem confere prescrição de agregado neste workflow. O parâmetro TQS auditado é 15 mm, igualmente não governante. Não foi encontrado conflito para o critério confirmado ou essas bitolas.

A capacidade uniforme por camada também será reutilizada. Para reportar largura disponível/necessária, usa-se geometria explícita, sem nova fórmula de número máximo. Camadas com bitolas distintas podem ter sua largura composta explicitamente, com folgas de cada par pela maior exigência individual; não se cria bitola média. Concretopy não suporta mistura de bitolas dentro da mesma camada resistente, que continuará bloqueada para cálculo de flexão.

A validação de flexão existente no Concretopy verifica apenas diâmetros ocupados na largura, sem todas as folgas; não se altera esse controle. O novo filtro de detailing pertence ao assistant. Não há duplicação de resistência, ancoragem, al, posicionamento vertical ou interpolação.

`calcular_alturas_uteis_camadas` já é API pública e será reutilizada para novas posições, com explícitos preservados em prolongamentos. As primitivas de espaçamento/capacidade são acessíveis pelos submódulos, mas não fazem parte da fachada API congelada; o adaptador registrará interface/hash, e testes de contrato protegerão essa dependência sem modificar o Concretopy.
