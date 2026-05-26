# Análise institucional brasileira

## Fontes primárias

1. **Lei 12.529/2011** (Lei de Defesa da Concorrência)
   - Art. 85 (TCC): "Nos procedimentos administrativos mencionados nos incisos I, II e III do art. 48 desta Lei, o Cade poderá tomar do representado compromisso de cessação da prática sob investigação ou dos seus efeitos lesivos, sempre que, em juízo de conveniência e oportunidade, devidamente fundamentado, entender que atende aos interesses protegidos por lei."
   - Art. 86 (Leniência): restringe a participantes da conduta. Imunidade total ou redução de 1 a 2/3 da penalidade.

2. **Lei 13.608/2018**, com redação dada pela **Lei 13.964/2019**, Art. 15
   - Art. 4º-A: proteção integral contra represálias.
   - Art. 4º-B: preservação de identidade.
   - Art. 4º-C, §3º: recompensa de até 5% do valor recuperado, mas restrita a crimes contra a administração pública.

3. **Resolução CADE nº 21/2018**
   - Art. 12: autoriza considerar como circunstância atenuante, no cálculo da contribuição pecuniária do TCC, o ressarcimento extrajudicial ou judicial das vítimas (art. 45, V e VI da Lei 12.529/2011). **Esta é a charneira jurídica do Regime B.**

## Os três regimes

### Regime A — situação atual

Sem canal de incentivo individual para denúncia em antitruste. Vazão histórica: ~5 leniências/ano (CADE 2003-2023) e ~47 TCCs/ano (Saito 2021).

### Regime B — WaaS via Resolução

Implementação por nova Resolução CADE complementar à 21/2018, sem necessidade de mudança legal. A recompensa paga pela empresa aos denunciantes é re-caracterizada como *ressarcimento extrajudicial* sob o Art. 12, gerando o desconto sobre a contribuição pecuniária do TCC.

**Risco principal**: validação judicial dessa re-caracterização (falsificador F6).

### Regime C — WaaS via Lei

Extensão da Lei 13.608/2018 para alcançar infrações à ordem econômica, com percentual explícito de recompensa. Maior robustez jurídica, custo político mais alto.

## Decisão de design não-trivial

O método `satisfaz_ic_f_estrela` da `EmpresaAgent` implementa o teste IC-F* na forma D > W. Isso é uma escolha deliberada: assume-se que, dado o sinal já recebido, o caminho "não paga" é dominado pela detecção quase certa (a notificação chega à autoridade de qualquer forma). A forma completa (custo_waas ≤ custo_não_paga, com p_detecção endógeno) fica como exercício para variantes do modelo — ver R01 no backlog.

## Articulação com o IPEA

Este repositório é mantido por L. (IPEA/DIEST/COGIT) independentemente do Instituto. As posições aqui defendidas não vinculam o IPEA. A intenção é submeter o artigo a revista internacional indexada (Journal of Competition Law & Economics ou similar) com aprovação prévia da chefia institucional.
