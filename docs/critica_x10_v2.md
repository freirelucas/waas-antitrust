# Crítica x10 v2 — pós-reframe "massa crítica como bem quase-público"

Segunda rodada de revisão crítica, motivada pelo reframe central do projeto:
o autor desloca a centralidade narrativa de **"empresa paga pela delação"**
(IC-F\*) para **"criação de massa crítica de cooperação interna como bem
quase-público"** (Olson 1965; Ostrom 1990). Sob o novo framing, o WaaS é
**um instrumento entre vários** de internalização desse bem público — ao
lado de vesting Hirschman (R07), crédito tributário (R22, novo) e leniência
criminal individual (R23, novo).

A x10 v1 teve 8 personas (2 Mat, 2 Eco, 2 Adv, 1 Designer, 1 PM). A v2
mantém todas as 8 e acrescenta duas estreias para validar o reframe:

- **Sociólogo da coordenação coletiva** (Olson, Ostrom, Coleman, Elster, Chwe)
- **Cientista político da regulação** (Stigler, Wilson, McCubbins-Schwartz, Carpenter-Moss)

Cada especialista entregou diagnóstico + 3-5 melhorias concretas. As
críticas integrais estão arquivadas no histórico da sessão; aqui ficam os
achados sintéticos.

---

## Convergências principais

Pontos em que **dois ou mais especialistas** chegaram à mesma conclusão
independentemente — os achados mais robustos da rodada.

### A. A categoria conceitual está errada — Coleman > Samuelson (Sociólogo, Adv A, Eco A)

A maior surpresa da rodada. O Sociólogo demonstra que "bem quase-público"
(Samuelson 1954, sobre mercadorias com rivalidade/excluibilidade variáveis)
**não é a categoria certa** para massa crítica de cooperação interna. A
categoria correta é **capital social** (Coleman 1990, *Foundations of Social
Theory*, cap. 12) — *bem coletivo produzido como subproduto de relações de
obrigação*. A diferença é material: Coleman prevê *destruição do capital
social pelo próprio uso instrumental*. Recompensar denúncia pode **erodir a
confiabilidade horizontal** que produz o bem. O Adv A complementa pelo lado
jurídico: "bem público de detecção" não tem precedente no direito sancionador
BR; "**interesse público em detecção e cessação**" (Lei 9.784/99) é a
formulação dogmática disponível. O Eco A toca em paralelo: WaaS é "tecnologia
de governança de bem comum", linguagem Ostrom — mas Ostrom requer 8 *design
principles*, dos quais o WaaS satisfaz apenas 3 (P1 fronteiras, P4
monitoramento, P5 sanções graduadas), com 5 ausentes/silenciosos.

**Implicação**: o nome do reframe precisa mudar. "Massa crítica como capital
social com risco de erosão endógena" é a formulação mais defensável
teoricamente; "interesse público em detecção e cessação" é a formulação
jurídica complementar.

### B. Falta de modelagem de uso adversarial / oportunista (Cientista Político, Mat B, Sociólogo)

Convergência inesperada. O Cientista Político lista quatro vetores:
(i) insider acionista vendendo a descoberto antes de plantar denúncia;
(ii) concorrente financiando ex-empregado para denúncia oportunista;
(iii) chantagem intra-firma como ameaça pré-rescisão para extrair severance;
(iv) hedge fund ativista combinando short + WaaS payout. Dyck-Morse-Zingales
documentam ~17% de motivação financeira direta em denúncias SEC — não
desprezível. O Mat B menciona o desertor estratégico de Granovetter (1978):
o imitativo sinaliza quando `phi ≥ 0,30` mas nunca *desiste* porque os
outros já vão sinalizar. O Sociólogo evoca anti-commons (Heller 1998) como
mecanismo de sobre-denúncia frívola. **Solução proposta por todos os três**:
arquétipo `denunciante_oportunista` (utilidade puramente extrativa) +
reporter `densidade_denuncia_frivola`.

### C. R10 (IC-F\* completa) precisa virar matriz condicional ao instrumento e à posição (Eco A, Mat A)

O Eco A formula explicitamente: `p_pago = f(instrumento_ativo,
posicao_fila_inter, n_cooperadores_intra)`. Com 4+ instrumentos coexistindo,
isso é **matriz** de probabilidades, não escalar. O Mat A complementa
mostrando que sob decaimento Saito $f_W(k)$, existe **conjunto de limiares
heterogêneos por posição** $x^\star_k$, não um único $x^\star(t)$. R10
deixa de ser opcional sob reframe — sem ela, comparações entre instrumentos
colapsam em "qual é mais barato no margem", perdendo o efeito sistêmico.

### D. Topologia e grafo inter-firma como variáveis de política (Mat B, Eco B, Cientista Político)

Convergência tripla. O Mat B propõe que `topologia_intra ∈ {watts_strogatz,
caverna, estrela, regular, random}` vire instrumento — sem `p_rewiring > 0`,
o pequeno-mundo colapsa em caverna e a cascata morre. O Eco B aciona
Sah-Stiglitz 1986 (*spillover*): massa crítica em firma X eleva `p_perc`
percebida em outras firmas — externalidade inter-firma endógena.
O Cientista Político adiciona que mercados digitais têm aprendizado
inter-firma via **redes específicas** (ex-funcionários migrando, conselheiros
compartilhados, escritórios de advocacia). O `p_perc` escalar atual é
**campo de Schelling médio** insuficiente — substituir por `nx.Graph`
inter-firma com `p_perc_i = média de vizinhos no grafo`.

### E. Hierarquia de reservas constitucionais não foi entendida (Adv B, Adv A)

Adv B aponta erro hierárquico fundamental: instrumentos R22 (tributário) e
R23 (criminal) **não exigem apenas "lei"** — exigem reservas distintas:
- R22 (crédito tributário): **lei complementar** Art. 146 CF (IRPJ/CSLL) +
  lei ordinária específica Art. 150 §6º (benefício fiscal) + LRF Art. 14
  (estimativa trienal de impacto). Resolução CADE + Portaria RFB **não suprem**.
- R23 (leniência criminal individual): reserva penal estrita Art. 5º XXXIX —
  Art. 86 da Lei 12.529 protege empresa+colaboradores-do-acordo, não
  empregado-terceiro. Extensão analógica é vedada (*in malam partem*).

Adv A confirma pelo direito sancionador administrativo: tipicidade fechada
das circunstâncias atenuantes (Art. 45 Lei 12.529; Lei 9.784/99) **não
admite criação dogmática constitutiva** de atenuante "por bem público".
O precedente ausente é **Lei 12.846/2013 (LAC) Art. 7º VII-VIII** — programa
de integridade como atenuante em dosimetria. Ambos convergem: Regime C
precisa **decompor** em sub-regimes (`Cₜ` trabalhista, `Cᵩ` tributária-LC,
`Cₚ` penal).

### F. Bem-estar atual não conta externalidade erga omnes (Eco B, Eco A, Sociólogo)

`calcular_bem_estar` hoje é contabilidade de custos sociais privatizados
(dano + FP + recompensa + êxodo − multa). **Não conta o bem público**.
Convergência tripla:
- Eco B propõe `valor_dissuasao_difusa_acum = (p_perc_t − p_perc_0) ·
  n_empresas_nao_violadoras · overcharge_evitavel`, calibrado em Connor-Lande
  17-19%.
- Eco A propõe a mesma família de termos como reporter por instrumento.
- Sociólogo propõe `capital_social_residual_firma` (densidade de laços
  fortes pré/pós denúncia) para testar Coleman: uso instrumental erode
  produção.

Risco de double-counting: mitigação por usar somente firmas que *jamais*
foram notificadas no termo externalidade.

### G. Capacidade institucional CADE é gargalo (Cientista Político, PM)

O Cientista Político é categórico: WaaS pulveriza o *gatilho* (cada
empregado-denunciante é um *fire alarm*, McCubbins-Schwartz 1984) mas
**concentra captura no processamento**. Os 326 servidores (82% cedidos) do
RIG 2024 — 180 área-fim — são gargalo. Sem expansão de quadro, WaaS entrega
*seleção discricionária de notificações a investigar* — exatamente o vetor de
captura mais barato (Carpenter-Moss 2014). O PM confirma do ângulo
institucional: o reframe precisa atravessar "conselheiro CADE mediano" cuja
leitura de "bem público" é direito difuso constitucional (Art. 129 III CF),
não falha-de-Samuelson.

### H. Empilhar reframe sobre R09-R11 abertos é frágil (PM, Adv A, Adv B)

O PM diz explicitamente: "feche 1 decisão normativa pendente antes de abrir
nova camada interpretativa, ou o leitor cético lerá o reframe como manobra
retórica para contornar fragilidade jurídica não resolvida". O Adv A
confirma: o reframe **não resolve** E04 (verbatim Art. 12) — apenas
reposiciona o argumento sobre o mesmo texto. O Adv B mostra que múltiplas
reservas constitucionais agravam o quadro, não aliviam.

### I. Cenários precisam de Protocol Instrumento ortogonal (Eco A, Adv B)

Convergência forte de duas frentes distintas. O Eco A propõe `Protocol
Instrumento` com assinatura `aplicar(firma, fila, t) -> EfeitoIC` e refator
de WaaS/Hirschman como implementações. O Adv B propõe `Instrumento(nome,
reserva_constitucional, regime_minimo, fontes_primarias)` — gating estrutural
em ponto único. Os dois convergem em criar `src/waas_antitrust/instrumentos.py`
(não apenas `bem_publico.py`). **Risco a falsificar**: substituição perversa
(*crowding out* de Frey-Jegen) — firma adota o instrumento mais barato e
mata os outros, perdendo a sinalização pública.

### J. Punchline + reframe acadêmico devem coexistir tipograficamente (Designer, PM)

Designer: "Não troque a punchline jornalística pelo reframe acadêmico —
empilhe-os tipograficamente: H1 atrai, sublinha promete, exemplo numérico
ancora, bem_publico.md generaliza." PM confirma: "bem público" funciona
com IPEA, falha com CADE mediano e OAB. Manter `# E se a empresa pagasse
para ser delatada?` como H1 + sublinha cinza em itálico contendo o reframe
é solução de compromisso. Move `bem_publico.md` para depois do Ato 2
(exemplo numérico R$ 1B / R$ 15M precede salto conceitual).

---

## Críticas únicas (não-convergentes, mas relevantes)

### Mat A — Angeletos-Hellwig-Pavan
A reformulação da Prop. 2 sob LCMC propõe "sequência $\{x^\star(t)\}$
decrescente" — sedutora mas formalmente perigosa. Morris-Shin garante
unicidade num jogo *estático* via crença laplaciana. Sob `modo_corrida`, a
fila inter-firma cria correlação que **não herda gratuitamente a unicidade**
— precisa do arcabouço de Frankel-Morris-Pauzner (2003) ou Angeletos-Hellwig-
Pavan (2007) para jogos globais dinâmicos com aprendizado público. **Sinal**:
o reframe substitui um pilar formal por conjectura mais difícil que a original.

### Mat B — `0,30` hardcoded como artefato da Prop. 1
Centola (2010 *Science*) mostra limiares de adoção 0,10-0,50 em redes reais.
O `0,30` para imitativo é **mediana arbitrária**. A Prop. 1 pode ser
artefato de 0,30 — recálculo com 0,20 ou 0,40 pode mudar o regime de cascata.
Solução: `theta_imitativo ~ Beta(α, β)` com exposição em `WaaSParametros`.

### Eco A — Instrumentos faltantes
Os 4 instrumentos do reframe omitem 3 institucionalmente disponíveis:
(i) **reputational discharge** (selo público de cooperação como ativo de
mercado de trabalho); (ii) **pré-compromisso da firma** estilo deferred
prosecution (Becker-Stigler 1974); (iii) **fundo de honorários ex-ante**
(já em `cenarios.py` mas como variante WaaS, não instrumento autônomo).
Sem esses três, "múltiplos instrumentos" são apenas variantes do mesmo
objeto monetário.

### Eco B — Não-rivalidade como teste, não definição
Hoje o modelo *assume* não-rivalidade. Teste empírico: instrumentar
`capacidade_tique` da autoridade. Se duplicar capacidade NÃO duplica dano
evitado (retornos decrescentes), há **rivalidade parcial por gargalo
institucional** — exatamente o que o Cientista Político alerta sobre o
RIG 2024. Esse é o teste falsificável.

### Adv A — LAC Art. 7º VII-VIII como precedente ausente
A Lei 12.846/2013 (LAC) trata mecanismos de detecção interna como bem
juridicamente relevante para dosimetria. **Precedente ausente do
INSTITUTIONAL.md**. Reframar como "interesse público em detecção e
cessação" (Lei 9.784/99) — terminologia dogmática existente — em vez de
criar categoria *ex novo*.

### Adv B — Três reservas constitucionais distintas
- Reserva ordinária Art. 22 I CF: instrumentos contratuais (Hirschman, R07)
- Reserva complementar Art. 146 CF: instrumentos tributários (R22)
- Reserva penal estrita Art. 5º XXXIX CF: instrumentos criminais (R23)

Analogia ao IRS Whistleblower (US 26 §7623) é **inaplicável**: IRS opera
sob *federal taxing power* sem reserva penal; WaaS antitruste atravessa três
competências.

### Sociólogo — Anti-commons (Heller 1998)
Tragédia reversa de sobre-denúncia frívola tem nome em direito de
propriedade: **anti-commons** (Heller, *Harvard Law Review* 111:621).
Direitos de exclusão fragmentados levando à subutilização. Falta no ODD.

### Cientista Político — Regime C politicamente infactível 2024-2027
PL 2768/2022 (análogo nacional ao DMA) parado desde 2023; Câmara fragmentada;
agenda econômica centrada em reforma tributária + arcabouço fiscal.
Antitruste digital é matéria periférica. A premissa do paper de que "Regime
C é custo político mais alto, viável" **subestima o custo** — é provavelmente
*infactível* salvo crise reputacional grande (Apple TCC 2025 pode mover só
marginalmente).

### Designer — Chip-instrumento como componente reutilizável
Cada um dos 4 instrumentos precisa de um *chip visual* consistente (paleta:
WaaS em cor primária, outros em cinza-azulado). Usado em Ato 1, Ato 2 e
`bem_publico.md` — garante que o leitor reconheça "isto é um dos quatro" em
qualquer Ato. Acessibilidade: contraste AA + texto alternativo.

### PM — MVP do reframe se cortar 60%
"Sobra `bem_publico.md` (≤ 600 palavras) + parágrafo de abertura reescrito
em `mecanismo.md` + 1 figura conceitual revisada. Entrega o reposicionamento
narrativo sem tocar código nem reescrever o paper."

---

## Sinais mais fortes da sessão (top 3)

Três insights que **mudam a leitura do reframe** materialmente:

### 1. Coleman > Samuelson (Sociólogo)
**O WaaS não regula um bem quase-público no sentido de Samuelson; regula
capital social organizacional cuja produção pode ser destruída por sua
instrumentalização.** O reframe deveria ser "internalização de capital
social com risco de erosão endógena", e o ODD precisa de reporter que
**meça essa erosão** para que a Proposição 3 não confunda dissuasão com
cooperação sustentável.

### 2. Captura desloca-se do gatilho para o processamento (Cientista Político)
**WaaS reduz captura *do gatilho* mas concentra captura *no processamento* —
e o RIG 2024 (180 servidores área-fim, 82% cedidos) mostra que o CADE não
tem capacidade institucional para implementar WaaS sem que a seleção
discricionária de quais notificações investigar vire o novo ponto ótimo de
captura pela big tech regulada.**

### 3. Fechar antes de abrir (PM)
**Não empilhe reframe conceitual sobre R09-R11 abertos: feche 1 decisão
normativa pendente antes de abrir nova camada interpretativa, ou o leitor
cético (Adv B, conselheiro CADE) lerá o reframe como manobra retórica para
contornar fragilidade jurídica não resolvida.**

---

## Próximos passos

A síntese alimenta a [v2 do Plano de melhorias](plano_melhorias.md#v2-pos-reframe)
que reorganiza o backlog em três sprints com filtros adaptados ao reframe.
O ponto J (Designer + PM) garante que o site continue legível ao leigo;
o ponto A (Sociólogo) reposiciona o vocabulário do anexo conceitual;
o ponto E (Adv B + Adv A) decompõe Regime C em sub-regimes Cₜ/Cᵩ/Cₚ;
o ponto I (Eco A + Adv B) cria `src/waas_antitrust/instrumentos.py` como
módulo declarativo ortogonal.

Cinco novos R-items (R21-R25) abrem em [DECISIONS.md](DECISIONS.md), e o
[plano_melhorias.md](plano_melhorias.md) ganha categoria v2.
