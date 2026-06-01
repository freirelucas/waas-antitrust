# Changelog

Todas as mudanças notáveis deste projeto são registradas aqui.

O formato segue, de forma adaptada, o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
as mensagens de commit seguem *Conventional Commits* em português. O versionamento
semântico será adotado a partir da primeira release (Zenodo).

## [Não lançado]

Trabalho desde a importação inicial do projeto (`563588c`, "Add files via upload"),
agrupado por tema. O hash de cada commit aparece entre parênteses.

### Estrutura e empacotamento
- Descompacta o projeto do tarball para a raiz do repositório e passa a versionar os
  arquivos (`src/`, `tests/`, `docs/`, `paper/`, …) em vez do `.tar.gz` (`04eb127`).

### Integridade científica e correção de método
- **Fase 1** — corrige defeitos que invalidavam as alegações: contaminação de seed na
  varredura de Sobol (estimador de Saltelli), separação de métricas de fluxo × estoque,
  remoção de código morto, substituição do teste tautológico da Proposição 1, RNG único
  (Mesa 3.5) e alinhamento das alegações infladas (`9c146b9`).
- Sincroniza o CLI `waas-sobol` com a replicação (`--n-replicas`) e adiciona ajuda a
  todos os argumentos (`50c9705`).
- Corrige `scripts/run_sobol_full.py`, quebrado após o conserto do Sobol
  (`n_seeds` → `n_replicas`; índices replicados); README com instruções de instalação
  (`d318613`).

### Modelo e mecanismo (pesquisa)
- **Fase 2** — bem-estar com significado, autoridade com acurácia sensível à qualidade
  da prova e capacidade da autoridade ancorada na vazão do CADE (`fdf9ba5`).
- **R04** — canal de falso reporte: não-violadoras podem ser reportadas, então os falsos
  positivos deixam de ser identicamente nulos (`be911b3`).
- **R01** — dissuasão endógena (à la Harrington–Chang): a firma viola enquanto sua
  atratividade `g_i` supera a detecção percebida; expõe `dano_acumulado` (`c2dc8b5`).
- **R05** — bem-estar redefinido como o negativo do custo social (dano + falsos
  positivos), creditando a prevenção em vez de premiar a detecção (`233797e`).
- **R02** — jogo global estilizado: limiar de switching único derivado em forma fechada,
  com convergência verificada quando τ → 0 (exploratório) (`2d0102c`).
- **R07** — Hirschman exit-with-equity: novo módulo `hirschman.py` (puro, testado) +
  integração em P0 (camada preventiva: firmas com cláusula contratual de vesting
  acelerado têm `g_i` efetivo menor) e P3 (IC-F* ampliada: `D + custo_exodo > W`,
  parametrizada por padrões YC — vesting 4y/1y cliff, substituição ~50% w_a, equity
  ~50% w_a, ~50% non-vested). Novos reporters `n_firmas_sob_ameaca_exodo` e
  `custo_exodo_acum`. Teste de integração confirma direcionalmente: dissuasão
  preventiva reduz o dano social com cláusulas ativas.
- **R08** — Heterogeneidade conduta × ator crítico: novo módulo `condutas.py` com
  catálogo de 7 condutas canônicas digitais (self_preferencing, tying, predatory
  pricing, killer acquisitions, dark patterns, acesso API/dados, MFN), cada uma
  com atores primários (eng/produto/design/growth/comercial/juridico/corpdev).
  `TrabalhadorAgent` ganha `papel`, `EmpresaAgent` ganha `conduta_potencial`, e a
  observabilidade em P0 passa a depender do par (papel, conduta). Teste
  end-to-end confirma direcionalmente que engenheiros observam mais
  self_preferencing que designers. Glossário ganha 10 termos.
- **Crítica x10 sintetizada**: 8 especialistas em paralelo (2 mat / 2 eco / 2 adv
  / 1 designer / 1 PM) entregaram diagnóstico + 3–5 melhorias concretas cada.
  Síntese em `docs/critica_x10.md` (convergências + críticas únicas + sinal mais
  forte: descompasso de competência do Regime B). Roteiro de execução em
  `docs/plano_melhorias.md`, com 7 categorias filtradas por "piloto automático"
  (sem decisão normativa do autor, ≤2 h, gate verde, reduz overclaim) e 1
  categoria de pendências normativas (R09–R13 a abrir).
- **REFERENCES expandida com pesquisa de fundo** (ABM aplicado a economia
  industrial e a mercados digitais). Subagente em paralelo retornou ~26
  referências verificadas (com DOI/arXiv/URL estável) cobrindo: ABM
  fundacional (Tesfatsion-Judd, Farmer-Foley, LeBaron, Wilensky-Rand,
  Dawid-Eurace); leniência clássica (Spagnolo, Motta-Polo,
  Harrington-Chang 2009/2015, Aubert-Rey-Kovacic, Bigoni et al.,
  Apesteguia-Dufwenberg-Selten); denúncia interna empírica
  (Dyck-Morse-Zingales, Call et al., Stubben-Welch, Wiedman-Zhu sobre
  Dodd-Frank §922); mercados digitais (Rochet-Tirole, Calvano et al.
  2020/2021 sobre Q-learning colusivo, Klein, Ezrachi-Stucke,
  Cunningham-Ederer-Ma sobre killer acquisitions, Caffarra-Crawford-Valletti
  sobre *reverse* killer, Crémer-Montjoye-Schweitzer, Mathur et al. sobre
  dark patterns); contexto brasileiro (Roquete/CADE, DEE/CADE DOCs
  003/2022 e 001/2024, IPEA CTS sobre PL 2768/2022). **Marcações [?]
  explícitas** em 3 referências não confirmadas (Roquete autoria JOTA;
  Castro-Mundim-Resende DEE; Anderson Caputo Silva — este removido por
  não-existência). Síntese pós-pesquisa em REFERENCES §4 identifica 5
  contribuições distintivas do WaaS vs. corpus existente (objeto =
  abuso unilateral; acoplamento triplo IC-T/IR/IC-F*; Hirschman como
  microfundamento original de IC-F*; calibração institucional brasileira
  granular; catálogo conduta × papel com gradiente 3-níveis).
- **Pivô de UX e curadoria fina do texto** (decorrente da crítica continuada
  "a experiência do leitor continua péssima"): home reescrita com **H1
  pergunta-tese** (`E se a empresa pagasse para ser delatada?`),
  bloco-hero acima da dobra trazendo a figura empírica imediatamente,
  navegação por **personas em grid cards Material** (Curioso · Formulador
  ou jurista · Pesquisador · Cético saudável) substituindo o admonition
  monolítico, badges movidas ao rodapé. CSS estendido em
  `docs/stylesheets/extra.css` com classe `.hero` (verde institucional +
  gradiente sutil), refinamento dos cards (hover, sombra, cabeçalho em
  destaque) e suporte explícito a modo escuro. `mkdocs.yml` ganha
  `md_in_html`, `tables`, `pymdownx.details` e `pymdownx.tabbed`.
  `docs/resultados.md` curada com numeração ordinal (§1/§2/§3), painéis
  rotulados explicitamente. `docs/limitacoes.md` reescrita: lista
  expandida do que **já** está implementado (incluindo bootstrap
  multi-seed, gating R07, catálogo BR de 9 condutas) e tabela atualizada
  de pendências com R09–R14. `README.md` alinhado ao H1 do site para
  coerência cross-canal. Sem regressão de testes (80 verdes).
- **R14 — Enriquecimento heterogêneo dos agentes (exploratório)**:
  três canais ortogonais ao R01, sem violar Proposições, todos opt-in
  por defaults para preservar compatibilidade.
  - **TrabalhadorAgent**: `anos_carreira` (Exponencial), property
    derivada `fracao_vested_individual` (cliff 1y + linear até 4y),
    `tolerancia_represalia` heterogênea (multiplicador individual no
    custo esperado de represália; ativa com
    `sigma_tolerancia_represalia > 0`), e memória `historico_observou`.
  - **EmpresaAgent**: `cultura_compliance ∈ [0,1]` modula a severidade
    efetiva σ via `peso_cultura_compliance · cultura` — programa de
    integridade como canal ortogonal ao R01. Atributo `poder_retaliacao`
    (proxy = `fatia_mercado`; ainda não acionado). Memória
    `n_denuncias_acum` em P2.
  - **AutoridadeAgent**: `prioridade_digital ∈ [0,1]` eleva ρ na P4
    (`ρ_ef = ρ + (1−ρ)·prioridade`). Default 0 preserva ρ_ef = ρ.
  - Sete testes direcionais novos em `tests/test_agentes_enriquecidos.py`
    (vesting + cliff, homogeneidade vs heterogeneidade, cultura reduz
    multa, prioridade eleva VP, memória acumula). Total: 73 → 80.
- **Categoria 7 (pendências normativas)** — abrir **R09** (endogeneizar
  `g_i(t) = π·R/(p·S)` — altera Prop. 3), **R10** (IC-F* completa
  `W + p_pago·(S−D) < p_npago·S` — altera Prop. 1), **R11** (Hirschman
  como elevação de `W_esperado` em vez de subtração de `g_i` — altera
  microfundamento de R07), **R12** (substituir arquétipo "racional" por
  `s_i ≥ x*` do `jogo_global` — fecha R02a) e **R13** (endgame do paper:
  `p_anulacao_tcc`, fatia Pareto/lognormal, sankey real, 3 condutas-piloto
  com fixtures). Estes itens **alteram material e Proposições** e
  permanecem no backlog `docs/DECISIONS.md` para conversa explícita —
  fora do piloto automático por design.
- **Categoria 6 (UX visual + acessibilidade)** — Designer. (6.1) Mapas de
  cor das figuras conceituais migrados de `RdYlGn` (pior caso para
  daltonismo vermelho-verde) para `cividis` (`viz/inversao.py`,
  `viz/fase.py`). (6.2) Novas constantes em `viz/paleta.py`: `MARCADORES`
  (A=`o`, B=`s`, C=`^`), `HACHURAS` (regime-específicas para barras) e
  `CMAP_CONCEITUAL`. (6.3) Novo `docs/stylesheets/extra.css` com classes
  `.figura-conceitual` (borda cinza tracejada + chip "Ilustrativo") e
  `.figura-empirica` (borda verde + chip "Resultado da simulação"); modo
  escuro tratado. `mkdocs.yml` ganha `extra_css`. (6.4) Novo script
  `scripts/gerar_figura_dissuasao.py` que regenera
  `docs/img/03_dissuasao_bem_estar.png` com rótulos `(A)`/`(B)` nos
  painéis, anotações numéricas (tiques até zero violadoras, ΔW% B/C vs
  A), marcadores por regime e hachuras nas barras. (6.5) Markdown
  (`index.md`, `resultados.md`) ganha attribute lists
  `{ .figura-conceitual }` (figs 1 e 2) e `{ .figura-empirica }` (fig 3).
- **Categoria 5 (catálogo BR + papéis)** — PM. (5.1) Nova conduta
  `exclusividade_retaliacao_marketplace` (iFood TCC 2023 + indícios contra
  Mercado Livre 2024-2025); primários: comercial/operações. (5.2) Nova
  conduta `anti_steering_iap` (Apple Brasil CADE dez/2025; Epic v. Apple
  EUA 2021); primários: produto/eng. (5.3) `PAPEIS_PADRAO` ganha
  **`operacoes`** (marketplaces BR são operations-heavy) e **`financeiro`**
  (FP&A em predatory pricing). (5.4) Dois presets de distribuição:
  `BIGTECH_MADURA` (eng-heavy; default) e `MARKETPLACE_BR`
  (operations-heavy). (5.5) Cada `Conduta` ganha `atores_adjacentes`;
  `observabilidade` agora é gradiente 3-níveis (primário=1.0,
  **adjacente=0.5**, distal=0.1 — Near & Miceli sobre whistleblowing
  organizacional), substituindo o binário 1.0/0.2. Glossário ganha 5
  termos (Exclusividade/retaliação marketplace, anti-steering/IAP, ator
  adjacente, MARKETPLACE_BR/BIGTECH_MADURA). Total: 70 → 73 testes;
  calibração formal de papéis BR pendente em E05.
- **Categoria 4 (gating jurídico do R07)** — Adv B (sinal mais forte da
  crítica x10: descompasso de competência do Regime B). (4.1)
  `WaaSModel.__init__` agora rejeita `fracao_contratos_acelerados > 0` sob
  Regime A ou B: emite `UserWarning` citando reserva de lei (Art. 22, I,
  CF — Resolução do CADE não pode impor cláusula contratual padrão) e
  força o valor para 0.0. Apenas Regime C preserva o parâmetro. (4.2)
  Nova função `valor_liquido_pos_tributos(valor_bruto, aliquota=0.4)` em
  `hirschman.py`: aplica haircut IRPF+INSS (40% default) sobre o vesting
  acelerado; **substituição não sofre haircut** — é despesa operacional
  da firma, não rendimento do trabalhador. `custo_exodo_esperado` ganha
  arg `aliquota_tributaria=0.0` (default preserva versão bruta histórica);
  `WaaSParametros.aliquota_tributaria_vesting` propaga para o modelo.
  (4.3) Testes novos: gating sob A/B com `pytest.warns`, preservação sob
  C, haircut só no vesting (não na substituição), defaults antigos. O
  teste integrado de R07 migrou de regime B → C (coerência institucional).
  Total: 65 → 70 testes.
- **Categoria 3 (bem-estar substantivo)** — Eco B. (3.1) `custo_exodo_acum`
  entra em `calcular_bem_estar` com peso `delta_exodo=0.5` (custo social de
  perda transitória de capital humano). (3.2) Novo reporter
  `multa_arrecadada_acum` em `model.py`: a cada tique, VPs que assinaram TCC
  pagam apenas o residual `sancao · (1 − D_disc)`, VPs sem TCC pagam a multa
  cheia; integrado no `bem_estar` com peso `delta_multa=1.0` (credita o
  erário). (3.3) Novo reporter `dano_economico_acum = Σ fatia_mercado ·
  eh_violadora`: sob fatias uniformes colapsa em `dano_acumulado/n_empresas`,
  mas torna-se métrica significativa quando heterogeneidade Pareto/lognormal
  for introduzida (R03/E05). `calcular_bem_estar` ganha argumentos
  `custo_exodo` e `multa_arrecadada` com defaults 0 (backward-compat). Testes
  novos: `test_calcular_bem_estar_inclui_exodo_e_multa` e
  `test_calcular_bem_estar_argumentos_novos_preservam_default_antigo`.
  Pesos provisórios; calibrar em R03.
- **Categoria 2 (infra de robustez)** — Mat A + Mat B. Novo módulo
  `src/waas_antitrust/robustez.py` com (2.1) **suavização Beta-Binomial**
  `beta_binomial_smoothing(sucessos, tentativas, α, β)` — estimador MAP
  `(sucessos + α) / (tentativas + α + β)` que remove a singularidade do
  estimador frequencista em `tentativas = 0` e estabiliza a variância em
  n pequeno; integrada em P0 (`model.py`) substituindo `vp/n_violadoras`,
  parametrizada por `alpha_beta_binomial=1.0` e `beta_beta_binomial=5.0`
  (prior centrado em ~16,7%, próximo do `p_deteccao_prior` default). (2.2)
  Helper de **bootstrap multi-seed** `bootstrap_ci(valores, n_bootstrap,
  α, seed)` + `varredura_multi_seed(fabrica, seeds)` para promover
  comparações pontuais a comparações com intervalo de confiança
  percentílico. Teste novo `test_dissuasao_endogena_robusta_a_multi_seed`
  confirma que a mediana de `B − A` em 12 seeds é negativa e o CI 95% não
  cruza zero — direção da Prop. 3 robusta a reamostragem. 10 testes novos
  (53 → 63); gates seguem verdes.
- **Categoria 1 (honestidade documental)** — só-texto, sem mudança de comportamento.
  (1.1) `hirschman.py` corrige docstring "padrões YC" → reconhece que o
  gatilho de vesting acelerado por ação coletiva é **construção normativa
  proposta pelo projeto**, não cláusula YC/NVCA documentada, e acrescenta
  caveats de tributação (IRPF + INSS derrete 40–50% do valor bruto) e
  institucional (reserva de lei Art. 22, I, CF — só Regime C entrega).
  (1.2/1.3) `DECISIONS.md` R07: caveats de escopo (Lei 13.608/2018 não cobre
  antitruste no eixo recompensa, Art. 4º-C §3º) e tributários explicitados.
  (1.4) R02 particionada em R02a (integração do `x*` no ABM), R02b (contraste
  multiplicidade × unicidade) e R02c (unicidade sob heterogeneidade —
  conjectura). (1.5) `paper/main.tex`: "é, assim, re-caracterizada" →
  "*pode ser* re-caracterizada (controvertida, sujeita a F6)". (1.6)
  `limitacoes.md` ganha linha **L-Jur1** com a fragilidade jurídica do
  Regime B. (1.7/1.8) `INSTITUTIONAL.md` ganha subseções "Limites do Regime
  B (reserva de lei)" e "Quem é vítima? no Art. 12". (1.9) Abre **D06**
  (análise dogmática vítima-empregado) e marca **E04** como pendência
  rastreada também no paper. (1.10) Abre **E05** (calibrar
  `DISTRIBUICAO_PAPEIS_PADRAO` para marketplace BR). (1.11) `ODD.md`:
  pressuposto de homogeneidade de Morris-Shin explicitado em §2 e Prop. 2
  status atualizado para "conjectura aberta sob heterogeneidade".

### Documentação, site e paper
- **Fase 3** — registra o backlog de pesquisa (R01–R06) em `docs/DECISIONS.md`
  (`07991aa`).
- Site de documentação MkDocs Material e exportação de figuras em PDF (`1fe4f5d`).
- Paper: rascunho das seções estáveis (introdução e mecanismo), figuras reais e build
  LaTeX via Tectonic (`b171899`).
- README aponta para o site, o Colab e o paper (`8906892`).
- Site: figuras na página inicial e navegação reorganizada (`e40ed9b`).
- Adiciona e mantém este `CHANGELOG.md`, com uma entrada por commit, agrupada por tema.
- **Banho de loja de UX**: landing reescrita para o leigo (o problema → a ideia →
  resultado real → para quem), novas páginas **Resultados**, **Limitações** e
  **Glossário**, figura de resultado real do modelo (dissuasão + bem-estar) no site
  e no README, botão "editar esta página" (`edit_uri`), e README com "por quê/como"
  antes do quickstart.

### Ferramentas, Colab e testes
- Skill de execução `run-waas-antitrust` com driver de fumaça (`89bc38b`).
- Caderno instala as dependências automaticamente no Google Colab (`0f05e24`).
- Cobertura de testes ≥ 80% — análise de Sobol e stubs de visualização (`666fa13`).
- Caderno-demo limpo, baseado no pacote, como companheiro canônico para Colab/CI
  (`b4f91ce`).
- Refresh da skill `run-waas-antitrust`: driver ganha a camada `jogo_global` (R02);
  `SKILL.md` atualizado (4 camadas, demo, métricas de dano/bem-estar) e corrige a
  gotcha obsoleta "FP≡0" (o R04 introduziu falsos positivos).
