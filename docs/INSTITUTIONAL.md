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

O texto verbatim dos dispositivos centrais acima, parseado a partir do LexML BR e disponível para consulta programática, está em [módulo `normas/` (parser LexML BR)](normas.md). Caveat: parser ainda parcial; expansão para Lei 13.608/2018 e Lei 13.964/2019 está registrada em [Brainstorm de revisão](brainstorm_revisao.md) §6.

## Doutrina brasileira relevante

A discussão sobre o desenho institucional da LCMC dialoga com três linhas doutrinárias brasileiras já estabelecidas. Esta seção registra as obras-referência, sem pretender pacificar o debate — registra apenas que o argumento do projeto não opera no vácuo doutrinário.

### Sobre os fundamentos do antitruste e a aplicação da Lei 12.529

A obra de referência é **Paula Forgioni**, *Os Fundamentos do Antitruste* (RT, sucessivas edições), que trabalha em detalhe a passagem da defesa abstrata da concorrência para o enforcement concreto sob a Lei 12.529/2011 e a relação entre instrumentos sancionatórios (multa, TCC, leniência) e os critérios dosimétricos do Art. 45. A discussão da LCMC sobre o gradiente Saito como calibração empírica do Art. 45 (ver [operacionalização](operacional.md#compatibilidade-com-a-dosimetria-do-art-45)) se insere nesse debate.

A obra de **Calixto Salomão Filho**, *Direito Concorrencial* (Malheiros, sucessivas edições), trabalha em particular o regime do abuso de posição dominante e a distinção entre conduta unilateral e coordenada. A premissa central do projeto — de que mercados digitais tornam a leniência clássica frágil porque a conduta tipicamente é unilateral — dialoga diretamente com essa linha.

### Sobre reserva de lei e limites da regulação infralegal

A questão de **se a LCMC cabe em Resolução do CADE ou exige lei nova** envolve a discussão clássica sobre reserva legal e limites da delegação normativa, na qual a obra de **Tércio Sampaio Ferraz Jr.** é referência seminal na produção brasileira — em particular o tratamento da reserva de lei como princípio estruturante e os limites do que cabe em ato infralegal sob a Constituição de 1988. A análise do falsificador F6 do desenho (ver [limitações](limitacoes.md#fragilidade-juridica-do-regime-b)) se inscreve nesse debate.

### Sobre a proteção do denunciante

A literatura brasileira específica sobre proteção do denunciante (*whistleblower*) é mais incipiente. As referências mais usadas nesta página são a literatura comparada (Vandekerckhove; Worth; Devine) e os comentários à Lei 13.608/2018 produzidos no contexto da Lei 13.964/2019. A pendência de aprofundamento doutrinário sobre este eixo está registrada em [Brainstorm de revisão](brainstorm_revisao.md) §6.

> **Caveat.** As três linhas doutrinárias acima são citadas como referência de leitura, não como autoridade que sustente este projeto. As posições do autor podem divergir das posições doutrinárias mencionadas; cada divergência substantiva fica explicitada no corpo do texto correspondente.

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

### Transposição comparada — decomposição EUA e UE (R28)

A decomposição em reservas constitucionais é específica do arranjo
brasileiro; transpor a LCMC exige refazer o exercício para cada
jurisdição. Os marcos de 2024-2025 (ver [Generalidade — EUA e
UE](internacional.md)) permitem a primeira aproximação:

| Eixo | Brasil | EUA (federal) | UE |
|---|---|---|---|
| **Canal** (depósito condicional) | Base autônoma: Art. 4º Lei 12.529 c/c Lei 9.784/99 — ato administrativo do CADE | Via administrativa demonstrada: DOJ-ATR Rewards Program instituído em jul/2025 **sem lei nova**, em parceria com o USPS | Via administrativa demonstrada: DMA Whistleblower Tool (abr/2024) operado pela Comissão sob o Reg. (UE) 2022/1925 — **sem** componente de escrow condicional |
| **Recompensa** | Regime B (re-caracterização Art. 12, sujeita a F6) ou Cᵩ (LC + LRF) | Fundo estatutário robusto: Dodd-Frank §922 (15 U.S.C. §78u-6) consolidou o template 10–30% — o DOJ-ATR opera 15–30% **sem** equivalente do risco F6 | **Inexistente**: a Diretiva (UE) 2019/1937 dá proteção horizontal anti-represália, não incentivo monetário |
| **Proteção anti-represália** | Lei 13.608/2018 (escopo restrito a "crimes contra a administração pública") | Estatutos setoriais (p.ex. Dodd-Frank para o eixo SEC) | Diretiva (UE) 2019/1937 — horizontal, transposta pelos Estados-membros |

Três leituras institucionais decorrem da tabela:

1. **A via administrativa do DOJ-ATR é o paralelo funcional do Regime B
   brasileiro** — programa de recompensa criado por ato administrativo,
   sem lei nova. A diferença material: o fundo estatutário americano
   (Dodd-Frank §922 como template já validado) elimina o equivalente do
   falsificador F6; no Brasil, a re-caracterização sob o Art. 12 ainda
   aguarda teste judicial. Por isso a tag `regime="EUA"` mapeia para a
   **mecânica C** (robustez), embora a **via** seja análoga à B.
2. **A UE demonstra o contrafactual do mecanismo**: canal + proteção,
   sem recompensa e sem massa crítica. A tag `regime="UE"` mapeia para
   a **mecânica A** porque, do ponto de vista do modelo, nenhum
   instrumento de internalização opera — o DMA Tool recebe denúncias
   individuais anônimas, não depósitos condicionais. Se a tese
   substantiva do projeto estiver certa (proteção sem incentivo é
   insuficiente para coordenação intra-firma), o desenho europeu
   sub-produzirá denúncias qualificadas em condutas unilaterais — uma
   predição comparada falsificável.
3. **A decomposição em sub-regimes não viaja**: Cₜ/Cᵩ/Cₚ respondem a
   reservas constitucionais brasileiras. Nos EUA, o eixo tributário tem
   precedente próprio (IRS Whistleblower Office sob *taxing power*) e o
   eixo penal corre pela discricionariedade de persecução do DOJ; na UE,
   a competência concorrencial é da Comissão, mas matéria penal e
   trabalhista permanece dos Estados-membros — qualquer acoplamento
   além do canal exigiria análise por Estado. Esta assimetria é o
   conteúdo institucional da afirmação "a LCMC é generalizável, os
   acoplamentos não necessariamente".

Pendência rastreada em R28: calibração de `taxa_capacidade` contra os
orçamentos DOJ-ATR (FY2025) e DG-COMP (2024) — sem ela, as comparações
de volume entre jurisdições no modelo são apenas direcionais.

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

## Canal de depósito condicional como procedimento administrativo

A LCMC **não** depende da re-caracterização do pagamento como
ressarcimento sob o Art. 12 da Resolução 21/2018. Depende apenas de
Resolução do CADE regulamentando o **procedimento de recepção
qualificada** de denúncias condicionais, com base no Art. 4º, II e III,
da Lei nº 12.529/2011 combinado com a Lei nº 9.784/1999 (Arts. 5º e
seguintes). A seção seguinte sobre o Art. 12 como reconhecimento de
interesse público trata do **instrumento WaaS** (recompensa via TCC
pós-instauração), que é um acoplamento opcional ao canal — não a base
dogmática do canal.

### O que muda na ancoragem jurídica

Sob a versão corrigida do mecanismo, a Resolução CADE proposta tem
objeto bem mais discreto:

- **Não** cria categoria sancionatória nova (atenuante por bem público).
- **Não** força re-caracterização finalística controversa de "ressarcimento".
- **Estrutura** o procedimento de recepção de denúncias: define o
  formulário, a condição de abertura (`q_min · n` co-depósitos
  compatíveis dentro de `Δt`), a custódia do escrow, a regra de
  abertura simultânea, o sigilo até abertura.

Bases legais explícitas:

- **Art. 4º, II e III, Lei 12.529/2011**: o CADE tem atribuição para
  "decidir sobre a existência de infração à ordem econômica e aplicar
  as penalidades previstas em lei" (II) e "instaurar processo
  administrativo, presidir, instruir e julgar" (III). Disso decorre,
  inferencialmente, a competência para regulamentar **como receber**
  as denúncias que disparam essa instauração.
- **Lei 9.784/99**, Art. 5º e Art. 6º: princípios de publicidade,
  motivação, eficiência e razoabilidade no procedimento administrativo
  federal. A custódia em escrow é compatível com Art. 24 (sigilo
  decorrente de interesse público).
- **Lei 13.608/2018** (com redação Lei 13.964/2019), Art. 4º-B e 4º-C:
  proteção do denunciante (anonimato), aplicável transversalmente.

O risco F6 (anulação judicial da re-caracterização) **cai materialmente**:
o que está sob controle judicial é a **regularidade do procedimento**, não
uma criação de categoria dogmática nova. Há precedente abundante de o
Judiciário deferir ao regulador discricionariedade procedimental
(Lei 9.784/99 Art. 2º, parágrafo único, IX, *desvio de finalidade* como
limite; mas não há desvio aqui — o canal serve à finalidade institucional
do CADE).

### Instrumentos monetários permanecem com suas bases próprias

Quando o canal abre e o procedimento é instaurado, os instrumentos
monetários se acoplam **com suas próprias bases legais** — não mais como
o coração do desenho, mas como acessórios:

- **WaaS (recompensa via TCC)**: re-caracterização sob Art. 12 da Res.
  21/2018. A § abaixo segue válida para este instrumento, em sua
  função acessória.
- **Hirschman**: lei ordinária federal (Cₜ), com gating do R07.
- **Crédito tributário**: lei complementar Art. 146 (Cᵩ), R22 stub.
- **Leniência criminal individual**: reserva penal estrita Art. 5º
  XXXIX (Cₚ), R23 stub.

Cada instrumento pode ser adotado isoladamente ou em conjunto. Nenhum
é necessário para o canal funcionar.

---

## Art. 12 como reconhecimento de interesse público em detecção (aplicável apenas ao instrumento WaaS)

> Esta seção trata da fundamentação dogmática do **instrumento WaaS**
> (recompensa via TCC). Sob v3, o **canal de depósito condicional**
> não depende dela — usa o Art. 4º da Lei 12.529 e a Lei 9.784/99
> como base procedimental autônoma (ver § acima). A presente seção
> sobrevive porque o instrumento WaaS, quando acoplado ao canal,
> precisa de uma base própria para a re-caracterização do pagamento
> como atenuante na contribuição pecuniária do TCC.

### Problema dogmático

A jurisprudência interna do CADE trata o Art. 12 da Resolução 21/2018
como autorização para considerar o **ressarcimento das vítimas** como
circunstância atenuante na dosimetria do TCC. O conceito de "vítima"
remete ao Art. 45, V e VI, da Lei 12.529/2011 — categoria *coletiva*
(consumidores, concorrentes, erário). Tratar a recompensa paga ao
**denunciante interno** como "ressarcimento da vítima coletiva" é
construção *finalística* (pelo papel funcional na produção da prova),
não dogmática (pelo nexo de causalidade com o dano).

Sob revisão judicial, essa re-caracterização pode ser rejeitada
(falsificador F6). Construções alternativas que substituem o
ressarcimento por "atenuante por contribuição a bem público de
detecção" **agravam** o problema, criando categoria *constitutiva* sem
ancoragem expressa na Lei nº 12.529/2011 nem em precedente brasileiro.

### Solução dogmática

A formulação disponível no direito sancionador administrativo
brasileiro é mais discreta. Em vez de criar categoria nova, usa
princípio existente como **base de fundamentação** para a discricionariedade
do CADE em reconhecer cooperação interna:

> **Interesse público em detecção e cessação** (Lei 9.784/99, Art. 2º,
> parágrafo único, IV — "atuação segundo padrões éticos de probidade,
> decoro e boa-fé"; e XIII — "interpretação da norma administrativa da
> forma que melhor garanta o atendimento do fim público a que se dirige").

Não cria atenuante novo; sustenta a discricionariedade do CADE em
*reconhecer* cooperação interna como circunstância relevante na
dosimetria já prevista no Art. 45 V/VI e na atenuante do Art. 12.

### Defesa do argumento

O argumento se defende em três flancos:

**(i) Precedente brasileiro: Lei 12.846/2013 (LAC) Art. 7º VII-VIII.**

> Art. 7º Serão levados em consideração na aplicação das sanções: (...)
> VII — a cooperação da pessoa jurídica para a apuração das infrações;
> VIII — a existência de mecanismos e procedimentos internos de
> integridade, auditoria e incentivo à denúncia de irregularidades e a
> aplicação efetiva de códigos de ética e de conduta no âmbito da pessoa
> jurídica.

A LAC **já trata mecanismos de detecção interna como bem juridicamente
relevante para dosimetria**. A construção do reframe é defensável como
**extensão analógica do princípio da LAC ao enforcement antitruste**:

- LAC é lei ordinária federal já aprovada pelo Congresso — remove a
  fragilidade de "criar categoria por resolução".
- O Decreto 11.129/2022 (regulamenta a LAC) detalha os critérios de
  *programa de integridade* — vocabulário que cabe à cooperação
  interna WaaS sem forçar a barra.
- O CGU/AGU já desenvolveram metodologia de avaliação de programas de
  integridade que pode ser adaptada à avaliação de "massa crítica
  qualificada" no antitruste.

**(ii) Ancoragem em princípios administrativos.** Lei 9.784/99 IV +
XIII (acima) sustentam a *discricionariedade* do CADE em reconhecer a
cooperação. Não há criação de tipo sancionatório; há *interpretação*
de princípio existente.

**(iii) Compatibilidade com a charneira atual.** O reframe **não
substitui** a leitura "ressarcimento finalístico" do Art. 12 — a
complementa. Se um juiz aceitar a leitura finalística, ótimo; se
rejeitar, a fundamentação alternativa via interesse público + LAC
permanece como caminho dogmático ainda defensável.

### Risco residual

A ancoragem dogmática mitiga **parcialmente** o F6 mas não o elimina —
a analogia LAC → antitruste é defensável, não pacífica. A pendência
**E04** (verbatim do Art. 12 da Resolução 21/2018 contra o Diário
Oficial) permanece obrigatória; este reframe não a resolve, apenas
reposiciona o argumento.

**Sob a tese v3**, a fragilidade F6 perde força central: o canal de
depósito condicional (mecanismo coração) não depende da
re-caracterização. Apenas o instrumento WaaS (incremento) carrega a
fragilidade — e o autor pode escolher implementar a LCMC sem WaaS,
mantendo o canal sob Resolução procedimental.

## Decisão de design não-trivial

O método `satisfaz_ic_f_estrela` da `EmpresaAgent` implementa o teste IC-F* na forma D > W. Isso é uma escolha deliberada: assume-se que, dado o sinal já recebido, o caminho "não paga" é dominado pela detecção quase certa (a notificação chega à autoridade de qualquer forma). A forma completa (custo_waas ≤ custo_não_paga, com p_detecção endógeno) fica como exercício para variantes do modelo — ver R01 no backlog.

## Articulação com o IPEA

Este repositório é mantido por L. (IPEA/DIEST/COGIT) independentemente do Instituto. As posições aqui defendidas não vinculam o IPEA. A intenção é submeter o artigo a revista internacional indexada (Journal of Competition Law & Economics ou similar) com aprovação prévia da chefia institucional.
