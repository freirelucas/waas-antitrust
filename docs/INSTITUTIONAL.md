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

### Regime C — WaaS via Lei (decomposto em Cₜ / Cᵩ / Cₚ)

Extensão da Lei 13.608/2018 para alcançar infrações à ordem econômica, com percentual explícito de recompensa. Maior robustez jurídica, custo político mais alto.

**Decomposição em sub-regimes** (atendendo à crítica do Adv B na x10 v2): "exigir lei" não é categoria homogênea no direito constitucional brasileiro. Cada instrumento de internalização sob o reframe tem **reserva constitucional distinta**, e o Regime C precisa decompor:

| Sub-regime | Instrumento que hospeda | Reserva constitucional aplicável | Tramitação |
|---|---|---|---|
| **Cₜ trabalhista** | Vesting Hirschman (R07): cláusula contratual padrão de vesting acelerado por gatilho de ação coletiva | Art. 22 I CF — reserva ordinária comum | Lei ordinária |
| **Cᵩ tributária-LC** | Crédito tributário ao denunciante (R22, novo): renúncia fiscal | Art. 146 III CF (IRPJ/CSLL) + Art. 150 §6º (benefício fiscal) + LRF Art. 14 (estimativa trienal) | **Lei complementar** + lei ordinária específica + plano fiscal |
| **Cₚ penal** | Leniência criminal individual (R23, novo): não-persecução do empregado-partícipe | Art. 5º XXXIX CF — reserva penal estrita | Lei ordinária + análise dogmática de colisão com Art. 86 da Lei 12.529 e Lei 8.137 |

A analogia ao **IRS Whistleblower Office** (26 U.S.C. §7623) é **inaplicável** ao WaaS antitruste brasileiro. O IRS opera sob *federal taxing power* (US Const. Art. I §8) — competência tributária federal exclusiva, sem reserva penal. No Brasil, o WaaS atravessa três competências (concorrencial, tributária, penal-econômica), cada uma com sua reserva. A "analogia" só funciona se o instrumento for puramente tributário (recompensa = restituição de imposto sonegado pelo cartel) — não é o caso de antitruste, onde o dano é privado (sobrepreço a consumidores), não fiscal.

A viabilidade política dos sub-regimes Cᵩ e Cₚ no horizonte 2024-2027 está documentada em [Viabilidade política do Regime C](viabilidade_regime_c.md). Cₜ tem janela aberta (vesting toca discurso de "proteção do trabalhador"); Cᵩ e Cₚ enfrentam barreiras dogmáticas e fiscais que tornam tramitação improvável sem crise reputacional grande.

## Limites do Regime B (reserva de lei)

Mesmo aceitando a re-caracterização da recompensa como ressarcimento, há uma
restrição estrutural que o Regime B **não pode** ultrapassar por via resolutiva:
matéria de **direito do trabalho** e **direito contratual** padrão é
competência privativa da União por **lei** (Art. 22, I, da Constituição
Federal). Em consequência:

- Resolução do CADE **não** pode impor cláusula contratual padrão de *vesting
  acelerado por gatilho de ação coletiva* nos contratos de trabalho — esse é
  exatamente o instrumento que a mecânica Hirschman exit-with-equity (R07,
  módulo `hirschman.py`) supõe.
- Resolução do CADE **não** pode criar tipo penal nem proteção trabalhista
  contra represália que vá além das já existentes em lei (a Lei 13.608/2018,
  Art. 4º-A a 4º-C, restringe a recompensa a crimes contra a administração
  pública).
- Resolução do CADE **pode**, sim, regulamentar o cálculo da contribuição
  pecuniária do TCC (Art. 85 da Lei 12.529/2011) e o reconhecimento de
  atenuantes — esse é o terreno onde o Regime B se sustenta.

Em termos do modelo: o parâmetro `fracao_contratos_acelerados > 0` é
juridicamente coerente apenas sob **Regime C** (via lei). Hoje o código aceita
o parâmetro em qualquer regime; o gating estrutural está rastreado em
`docs/plano_melhorias.md`, Categoria 4.

## Quem é "vítima" no Art. 12?

O Art. 12 da Resolução 21/2018 remete a "ressarcimento (extra)judicial das
vítimas" e cita o Art. 45, V e VI, da Lei 12.529/2011 — circunstâncias
agravantes/atenuantes. Na práxis do CADE, **vítima** em infração à ordem
econômica é categoria *coletiva*: consumidores afetados por sobrepreço,
concorrentes excluídos por conduta exclusionária, eventualmente o erário.

O **denunciante interno** do WaaS é tipicamente **funcionário ou
ex-funcionário** da empresa que cometeu a infração. Há tensão dogmática em
duas frentes:

1. **Categoria errada de vítima**: o empregado-denunciante não é a
   coletividade lesada — é, no melhor caso, **testemunha qualificada**. Tratar
   o pagamento ao empregado como "ressarcimento das vítimas" do Art. 12 é
   re-caracterização *finalística* (pelo papel funcional na produção da
   prova), não dogmática (pelo nexo de causalidade com o dano coletivo).
2. **Conflito com Art. 86 (leniência)**: se o empregado-denunciante for
   **partícipe** da conduta (engenheiro que codificou o algoritmo de
   self-preferencing; comercial que operou exclusividade; growth que
   instrumentou dark patterns — ver `condutas.py`, R08), o caminho
   institucionalmente adequado é a **leniência clássica**, não o WaaS. O
   Regime B pode criar arbitragem regulatória entre os dois canais.

Esse risco dogmático é a charneira do falsificador **F6** (re-caracterização
sujeita a validação judicial) e da decisão **D06** (análise dogmática
detalhada da figura "vítima-empregado", ver `DECISIONS.md`).

## Art. 12 como reconhecimento de interesse público em detecção (reframe v2)

A crítica do Adv A na x10 v2 trouxe correção dogmática material. A
re-caracterização atual ("recompensa = ressarcimento das vítimas") apoia-se
em construção *finalística* sobre o Art. 12 da Resolução 21/2018 — argumento
defensável mas sujeito a F6 (anulação judicial). O reframe original — que
falava em "atenuante por contribuição a bem público de detecção" — **agravava**
o problema ao criar categoria *constitutiva* sem ancoragem expressa.

A formulação dogmática disponível no direito sancionador administrativo
brasileiro é mais discreta:

> **Interesse público em detecção e cessação** (Lei 9.784/99, Art. 2º,
> parágrafo único, IV — "atuação segundo padrões éticos de probidade,
> decoro e boa-fé"; e XIII — "interpretação da norma administrativa da
> forma que melhor garanta o atendimento do fim público a que se dirige").

Não cria categoria nova; usa princípio existente como base de
fundamentação para a atenuante já prevista no Art. 12. O reframe
**não substitui** a leitura "ressarcimento finalístico" — a complementa
com um princípio de direito administrativo que sustenta a discricionariedade
do CADE em reconhecer cooperação interna como bem juridicamente relevante.

### O precedente que faltava: Lei 12.846/2013 (LAC) Art. 7º VII-VIII

O **precedente brasileiro mais relevante** para o reframe — ausente das
versões anteriores deste documento — é a Lei Anticorrupção (Lei
12.846/2013), Art. 7º, VII e VIII:

> Art. 7º Serão levados em consideração na aplicação das sanções: (...)
> VII — a cooperação da pessoa jurídica para a apuração das infrações;
> VIII — a existência de mecanismos e procedimentos internos de
> integridade, auditoria e incentivo à denúncia de irregularidades e a
> aplicação efetiva de códigos de ética e de conduta no âmbito da pessoa
> jurídica.

A LAC **já trata mecanismos de detecção interna como bem juridicamente
relevante para dosimetria**. Esse é exatamente o tipo de reconhecimento
institucional que o WaaS antitruste busca. A construção do reframe é
defensável como **extensão analógica do princípio da LAC ao enforcement
antitruste**, com vantagens dogmáticas claras:

- LAC é lei ordinária federal (já passou pelo Congresso), removendo a
  fragilidade de "criar categoria por resolução".
- O Decreto 11.129/2022 (regulamenta a LAC) detalha os critérios de
  *programa de integridade* — vocabulário que cabe à cooperação interna
  WaaS sem forçar a barra.
- O CGU/AGU já desenvolveram metodologia de avaliação de programas de
  integridade que pode ser adaptada à avaliação de "massa crítica
  qualificada" no antitruste.

Essa âncora dogmática mitiga **parcialmente** o F6 mas não o elimina — a
analogia LAC → antitruste é defensável, não pacífica. A pendência
**E04** (verbatim do Art. 12 da Resolução 21/2018 contra o Diário Oficial)
permanece obrigatória; o reframe não a resolve, apenas reposiciona o
argumento.

## Decisão de design não-trivial

O método `satisfaz_ic_f_estrela` da `EmpresaAgent` implementa o teste IC-F* na forma D > W. Isso é uma escolha deliberada: assume-se que, dado o sinal já recebido, o caminho "não paga" é dominado pela detecção quase certa (a notificação chega à autoridade de qualquer forma). A forma completa (custo_waas ≤ custo_não_paga, com p_detecção endógeno) fica como exercício para variantes do modelo — ver R01 no backlog.

## Articulação com o IPEA

Este repositório é mantido por L. (IPEA/DIEST/COGIT) independentemente do Instituto. As posições aqui defendidas não vinculam o IPEA. A intenção é submeter o artigo a revista internacional indexada (Journal of Competition Law & Economics ou similar) com aprovação prévia da chefia institucional.
