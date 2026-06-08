# Changelog

Todas as mudanças notáveis deste projeto são registradas aqui.

O formato segue, de forma adaptada, o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
as mensagens de commit seguem *Conventional Commits* em português. O versionamento
semântico será adotado a partir da primeira release (Zenodo).

## [Não lançado]

Trabalho desde a importação inicial do projeto (`563588c`, "Add files via upload"),
agrupado por tema. O hash de cada commit aparece entre parênteses.

### Reframe v2 — Mat A (limiar Saito por posição) + arquétipo oportunista

Terceiro commit do Sprint A do plano v2 pós-x10 v2. Primeiro código que
materializa críticas convergentes da rodada — duas categorias do plano v2.

**Categoria v2.G — Mat A: oferta escalonada do bem coletivo (jogo global)**

- `src/waas_antitrust/jogo_global.py` ganha `limiar_switching_por_posicao(b, c,
  k_rel, posicao_trabalhador, tau, perfil)` e `familia_limiares_por_posicao`.
  Sob LCMC, o ganho marginal vira `b_k = decaimento_W(k) · b` — cada posição
  na fila intra-firma tem seu próprio limiar Morris-Shin. A "oferta do bem
  coletivo" é escalonada por posição, não monolítica.
- Docstring do módulo ganha § "Extensão LCMC (Mat A v2 — R20)" com a
  fórmula `x*_k(τ)` derivada e caveat formal Frankel-Morris-Pauzner 2003 /
  Angeletos-Hellwig-Pavan 2007: a unicidade Morris-Shin clássica não se
  estende automaticamente; sob LCMC com fila inter-firma correlacionada
  (sinal público), a Proposição 2 reformulada vira conjectura aberta.
- 6 novos testes em `tests/test_jogo_global.py`: posição 1 = limiar base;
  monotonicidade `x*_1 < x*_2 < x*_3`; n* finito explícito; piso Tribunal
  posições ≥ 9; validação de input.

**Categoria v2.B.1 — Arquétipo `denunciante_oportunista` (R24)**

- `TrabalhadorAgent.ARQUETIPOS` agora tem 6 tipos: + "oportunista".
  Convergência tripla na x10 v2 — Cient. Político (uso adversarial: insider
  acionista, concorrente, chantagem, hedge fund); Sociólogo (anti-commons
  Heller 1998); Mat B (desertor estratégico Granovetter).
- `decidir_sinal` ganha branch `oportunista` ANTES do guard `observou`.
  Utilidade puramente extrativa: `u = W_efetivo - prob_falso · sancao_calunia`.
  `prob_falso = 0.7` se não observou (planta denúncia); `0.3` se observou
  (qualidade da prova maior). Sanção de calúnia (Art. 340 CP) calibrada em
  `0.5 · w_a`. **NÃO consulta** represália nem `phi_vizinhos` —
  comportamento extrativo isolado, ortogonal à pressão social.
- Novo preset `DISTRIBUICAO_COM_OPORTUNISTAS` em `cenarios.py` (20% de
  oportunistas, limite superior do reportado por Dyck-Morse-Zingales 2010
  ~17% de motivação financeira direta em denúncias SEC).
- Default `distribuicao_arquetipos=None` mantém oportunista em 0% —
  preserva backward compat estrita.
- 9 novos testes em `tests/test_oportunista.py`: catálogo; ativação por
  preset; sinaliza com W alto sem observar; não sinaliza com W baixo;
  prob_falso menor se observou; modelo end-to-end roda; preset soma 1.0;
  comportamento independente de phi_vizinhos.

**Atualizações de catálogo de testes**:
- `tests/test_agents.py::test_arquetipos_validos` — 5 → 6 arquétipos.
- `tests/test_fairminded_cenarios.py::test_fairminded_esta_no_catalogo` — 5 → 6.

Verificação: pytest 249 passed (234 + 15 novos); ruff check; black --check;
mkdocs build --strict.

Postura epistêmica: o oportunista é arquétipo de teste de robustez do
mecanismo, não recomendação. Sob `DISTRIBUICAO_COM_OPORTUNISTAS`, simula-se
o que aconteceria se o WaaS fosse adotado em uma população com fração
adversarial calibrada. Falsificador F7 candidato: se sob 20% de
oportunistas o mecanismo degrada acima de tolerância, há necessidade de
salvaguardas (anonimato, recompensa coletiva, janela curta).

### Reframe v2 — Capital social com risco de erosão endógena (Coleman > Samuelson)

Segundo commit do plano v2 pós-crítica x10 v2. Categoria v2.A: reposicionamento
conceitual sem mudança de código. Anchora o reframe na categoria certa,
sustentado por sociologia (Coleman, Olson, Ostrom, Heller, Elster, Chwe) e
literatura de motivation crowding (Titmuss 1970, Frey-Jegen 2001,
Bénabou-Tirole 2003).

**Novos arquivos:**
- `docs/bem_publico.md` — anexo conceitual; abre com leitura Samuelson e
  desloca para Coleman (capital social com risco de erosão endógena);
  apresenta os quatro instrumentos de internalização com reservas
  constitucionais distintas (Art. 22 I; Art. 146 LC; Art. 5º XXXIX); fecha
  com diagnóstico Ostrom dos 5 design principles ausentes.
- `docs/viabilidade_regime_c.md` — atende à crítica do Cientista Político
  v2; PL 2768/2022 parado desde 2023, agenda Câmara concentrada, Regime C
  provavelmente infactível 2024-2027 sem crise reputacional grande.

**Atualizações de documentação:**
- `docs/index.md` — sublinha cinza em itálico abaixo da H1 ("punchline
  jornalística + reframe acadêmico empilhados tipograficamente" per
  Designer v2).
- `docs/INSTITUTIONAL.md` — Regime C decomposto em Cₜ (trabalhista, Art.
  22 I), Cᵩ (tributária-LC, Art. 146 + LRF) e Cₚ (penal, Art. 5º XXXIX);
  nova seção "Art. 12 como reconhecimento de interesse público em
  detecção" (Lei 9.784/99) + **Lei 12.846/2013 LAC Art. 7º VII-VIII** como
  precedente dogmático que faltava; analogia ao IRS Whistleblower
  rejeitada.
- `docs/ODD.md` §2.1 — subseção "Diagnóstico Ostrom" cruzando os 8 design
  principles de governança de commons com reporters/parâmetros do modelo:
  3 atendidos (P1 fronteiras, P4 monitoramento, P5 sanções graduadas), 1
  silencioso (P8), 4 ausentes (P2, P3, P6, P7).
- `docs/limitacoes.md` — nova seção "Fragilidades do bem coletivo" com 3
  fragilidades pós-reframe (free-riding/sub-iniciação Olson; anti-commons
  Heller; erosão endógena Coleman); nova seção "Viabilidade política do
  Regime C".
- `docs/REFERENCES.md` — 4 novos blocos: "Coordenação coletiva, capital
  social e bens coletivos" (Olson, Ostrom, Coleman, Hardin, Heller,
  Elster, Samuelson); "Erosão de motivação por uso instrumental" (Titmuss,
  Frey-Jegen, Bénabou-Tirole, Mussler-Macy); "Jogos globais dinâmicos"
  (Frankel-Morris-Pauzner 2003, Angeletos-Hellwig-Pavan 2007, Chwe 2000);
  "Ciência política da regulação" (Stigler, Wilson, McCubbins-Schwartz,
  Carpenter-Moss, Levi, Mattli-Woods).
- `docs/DECISIONS.md` — R21-R26 abertos: R21 operacionalizar bem
  coletivo; R22 crédito tributário (com mapa de reservas); R23 leniência
  criminal individual; R24 free-riding e tragédia reversa; R25 jurisdição
  concorrente; **R26 erosão endógena por uso instrumental** (Proposição 5
  candidata, mais ambiciosa do plano v2).
- `docs/stylesheets/extra.css` — classes `.sublinha-tese` (sublinha cinza
  com borda lateral) e `.chip-instrumento` (componente reutilizável para
  os 4 instrumentos, com variante `.waas` em cor primária).
- `mkdocs.yml` — `bem_publico.md` e `viabilidade_regime_c.md`
  registrados em Anexos.

**Verificação**: pytest 234 passed; ruff check; black --check; mkdocs
build --strict.

### R20 — Leniência Condicionada à Massa Crítica (LCMC): macroconceito unificador

A LCMC é o **macroconceito** sob o qual o WaaS passa a ser entendido. Sob a
tese do moat — mercados digitais geram condutas unilaterais, sem cúmplice
externo para uma leniência clássica de Spagnolo (2004) ou Motta-Polo (2003)
— a única corrida possível é **intra-firma**. A LCMC institucionaliza isso
e a acopla a uma corrida **inter-firma**, ambas calibradas pelo gradiente
empírico do CADE (Saito 2021: 1ª=43,43%; 2ª=34,51%; 3ª=20,22%).

- **Fases 1-2** (núcleo + calibração Saito): novo módulo
  `src/waas_antitrust/corrida.py` com `decaimento_D` (fila inter-firma) e
  `decaimento_W` (fila intra-firma) consumindo
  `saito.MEDIA_DESCONTO_SG_POR_POSICAO`; dataclasses
  `FilaInternaCooperacao` e `FilaLeniencia`; função
  `massa_critica_interna_atingida`. Novos `WaaSParametros`:
  `modo_corrida: bool = False` (opt-in, preserva backward compat),
  `q_min_cooperacao_interna`, `janela_temporal_tiques`, `perfil_decaimento`.
  Phase P2.5 em `model.step()`. Atributos novos em `TrabalhadorAgent`
  (`posicao_corrida_interna`, `tique_cooperou`) e `EmpresaAgent`
  (`posicao_fila_leniencia`, `massa_critica_interna_satisfeita`). Cenário
  canônico `cenario_corrida_leniencia` em `cenarios.py` (Regime C plena).
  21 testes em `tests/test_corrida.py`.
- **Fase 7** (catálogo expandido de condutas digitais): `condutas.py` de 9
  → 28 condutas cobrindo 12 famílias (auto-preferência, restrições de
  plataforma, vinculação, predação algorítmica, acesso/dados/self-dealing,
  killer + reverse killer, discriminação algorítmica, captura de
  aprendizagem, manipulação de relevância, tying IA, lock-in via
  credentials, switching costs). Casos de referência verificados: CJUE
  Google Shopping (09/2024), US v. Google Search Mehta (08/2024), FTC v.
  Amazon (2023), Apple Brasil CADE (2025), DMA UE (2022), CMA UK SMS
  (2025), Khan (2017), Crémer-Montjoye-Schweitzer (2019), Cunningham-
  Ederer-Ma JPE (2021). Casos não consolidados marcados `[?]` no
  docstring. Novo dict `N_ATORES_PRIMARIOS_NECESSARIOS` calibra
  `q_min_cooperacao_interna` por conduta (nenhuma exige > 3 papéis
  primários — confirma tese do moat). 11 → 14 testes em
  `tests/test_condutas.py`.
- **Harmonização documental** (Ato 1, Ato 2, ODD, DECISIONS, REFERENCES):
  `docs/index.md` ganha seção "O macroconceito LCMC" + regime "C+LCMC"
  na tabela; `docs/mecanismo.md` ganha seção "O macroconceito" no topo
  e "A corrida que faltava (R20)" detalhando as duas corridas; `docs/ODD.md`
  ganha Phase P2.5 e reformulação das Proposições 1, 2, 3 sob LCMC como
  "conjectura aberta"; `docs/DECISIONS.md` registra R20 + atualiza R08
  (28 condutas) + reformula R09-R11 como mais acionáveis sob LCMC;
  `docs/REFERENCES.md` ganha bloco "Fontes regulatórias e jurisprudenciais
  do antitruste digital" + atualiza §4 (síntese) com a LCMC como peça
  distintiva.

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
- **T07 — Módulo `normas/` para parsing programático** (resposta à
  pergunta "pesquise metodologia adequada para parsear e manipular
  norma"). Agente de pesquisa retornou diagnóstico claro: **não há
  parser PT-BR maduro em Python para texto consolidado de leis em
  vigor**. Caminho adotado conforme recomendação: módulo ad-hoc
  disciplinado por LC 95/1998 + corpus local versionado em Git.
  - **Novo `src/waas_antitrust/normas/`**:
    * `urn.py` — dataclass `URNLex` (padrão URN-LEX do LexML Brasil)
      + `parse_urn` + 4 URNs canônicas pré-definidas (Leis 12.529,
      13.608, 13.964; Resolução CADE 21/2018). Resolutor LexML
      devolve HTML/PDF — usar apenas como link de citação.
    * `articulacao.py` — parser regex disciplinado por LC 95/1998.
      Decompõe texto articulado em árvore `Dispositivo` (artigo →
      parágrafo → inciso → alínea → item). Suporta `Parágrafo único`,
      `Art. 4º-A`, incisos romanos e alíneas. Casos patológicos
      (notas marginais, "Art. 4-bis") declarados fora de escopo.
    * `remissoes.py` — extrator de remissões cruzadas como dataclass
      `Remissao(artigo, paragrafo, incisos, alinea, norma_alvo,
      trecho_capturado)`. Padrão único: "Art. 45, V e VI da Lei nº
      12.529, de 30 de novembro de 2011" e variantes. Postura
      conservadora: prefere perder captura ambígua a inventar.
    * `corpus.py` — `NORMAS_INDEXADAS` mapeia URN → arquivo em
      `data/normas/`. `carregar_norma(urn)` aceita objeto ou string.
      Sem fetch em tempo de execução — integridade vem do Git.
    * `cite.py` — `citar(urn, dispositivo)` e `citar_com_subitens`
      recuperam trecho do corpus local (atende invariante CLAUDE.md
      de citações verificáveis).
  - **Novo `data/normas/`** com 3 textos:
    * Lei 12.529/2011 — Arts. 85-87 (Art. 85 caput **verbatim**
      verificado contra `INSTITUTIONAL.md`; demais marcados como
      "redação consolidada para teste interno do parser, aguardando
      verificação DOU" via E04).
    * Lei 13.608/2018 — Arts. 4º-A a 4º-C (paráfrases consistentes
      com `INSTITUTIONAL.md`; status declarado em cada arquivo).
    * Resolução CADE 21/2018 — Art. 12 (redação consolidada; **E04
      segue ABERTO** — verificação verbatim contra DOU é
      pré-requisito para citação no paper).
  - **Honestidade documental**: cada arquivo em `data/normas/` tem
    cabeçalho `# STATUS DE VERIFICAÇÃO` declarando o que é verbatim
    e o que é redação consolidada para teste — preserva o invariante
    CLAUDE.md "não inventar referências".
  - **24 testes** em `tests/test_normas.py`: URN bijeção, parser
    decompõe Arts. 85-87 com seus parágrafos e incisos numerados
    (I/II/III), Parágrafo único do Art. 87, Arts. 4º-A/B/C da Lei
    13.608, remissões `art. 45, V e VI da Lei 12.529`, busca de
    dispositivo composto (`Art. 85 § 1º`), `citar` recupera trecho
    verbatim do caput do Art. 85.
  - **REFERENCES.md** ganha seção "Parsing programático de normas
    (T07)" com 6 entradas verificadas (LexML BR, Akoma Ntoso, LC
    95/1998, laws.africa/cobalt + bluebell, ulysses-segmenter,
    lexml-parser-projeto-lei).
  - **DECISIONS T07** aberto com "Implementado", lista pendências
    futuras (gerador inverso XML LexML, comparador de versões
    consolidadas, grafo NetworkX de remissões).
  - Total: 187 → 211 testes; ruff/black/mkdocs --strict limpos.
- **R06 — Relatórios Integrados de Gestão (RIG) 2022-2024 calibrados**.
  Agente em background baixou os três PDFs primários (URLs HTTP 200
  em `cdn.cade.gov.br`, dezenas de MB cada), parseou com `pdftotext`
  e extraiu série temporal completa com **número de página verbatim**
  para cada constante. Mudanças substantivas:
  - **N_SERVIDORES_TOTAL: 292 → 326** (RIG 2024 substitui NT 2022).
  - Série completa de servidores em exercício
    `{2022: 287, 2023: 311, 2024: 326}` + fração de cedidos
    `{2022: 0,75; 2023: 0,77; 2024: 0,82}` — alta dependência
    crescente de pessoal cedido de outras instituições.
  - `N_SERVIDORES_PGPE_QUADRO_PROPRIO = 35` (apenas 35 do quadro
    permanente; ~291 são cedidos ou comissionados).
  - **`N_SERVIDORES_AREA_FIM = 180`** (RIG 2024, p. 110) — usado como
    proxy de SG/CADE em `N_SERVIDORES_POR_UNIDADE["superintendencia_geral"]`.
    Caveat documentado: agregado SG + parte do DEE; para SG estrita,
    ofício LAI ao Fala.BR/Cgesp/DAP.
  - **Orçamento Ação 2807 série 2022-2024**: LOA total e atualizada,
    execução próxima de 100% (99,4-99,8%) — **gargalo do CADE NÃO é
    orçamentário**. TIC dentro de 2807: R$ 9,2 mi (22%) em 2024.
  - **Fluxo de processos verbatim**: ACs `{660, 594, 712}`; valor
    `{1,56; 0,91; 1,07} trilhões`; investigações SG instauradas
    `{103, 63, 73}` (categoria ampla); concluídas `{111, 106, 89}`;
    estoque `{247, 177, 185}`; leniências `{1, 2, 4}`; total
    histórico **113** (substitui 109 anterior); B&A `{2, 2, 3}`;
    16 mandados em 2024; Clique Denúncia 2024 = **3.725**; multas
    trânsito julgado 2024 = R$ 158,18 mi nominal × R$ 29,17 mi
    arrecadado (**gap de cobrança >80%**); tempo médio AC ordinário
    `{125,6; 116,7; 92,1}` dias — tendência decrescente forte.
  - Helper `servidores_sg_calibrado()` atualizado: default 50 → 180
    (RIG); helper `capacidade_efetiva_por_tique()` agora retorna
    **90 casos/tique** (180 × 2 / 4) — compare com estoque médio
    observado (~200), saturação parcial consistente.
  - Novo helper `execucao_orcamentaria_relativa(ano)` para
    diagnóstico (relação executado / LOA atualizada).
  - Resolvida discrepância ACs 2023: RIG = 594 é primária; ConJur =
    579 é secundária. Usamos RIG.
  - REFERENCES.md ganha entrada "Relatórios Integrados de Gestão"
    com 3 PDFs verificados + página índice.
  - Testes ampliados de 24 → 38 cobrindo série temporal completa,
    decomposições, marcações [?] persistentes (DEE estrito,
    procuradores, comissionados), e helpers atualizados.
  - DECISIONS R06: movido de "Parcialmente calibrado" para
    "Calibrado contra RIG".
- **R02a — `jogo_global.x*` integrado ao arquétipo racional (opt-in)**.
  Fecha pendência de Mat B na crítica x10. O arquétipo "racional" pode
  agora decidir via `s_i ≥ x*` (limiar de switching de Morris-Shin)
  em vez da comparação direta IR-W ↔ ganho líquido. Implementação:
  - Novo `WaaSParametros.usar_x_estrela_no_racional: bool = False`
    (default preserva caminho histórico — zero regressão).
  - Em `agents.decidir_sinal`, ramo "racional" consulta a flag e, se
    ativada, chama `jogo_global.limiar_switching(b, c, k, τ)` com:
    `b = W_esperado/w_a`, `c = r·tol·2`, `k = model.k_rel`,
    `τ = model.tau_ruido`. Decisão final: `s_i ≥ x*`.
  - Lida com casos de borda: `W=0` (regime A) retorna 0;
    `observou=False` retorna 0 (mesmo com flag ativa).
  - 9 testes em `tests/test_jogo_global_no_racional.py`: default
    preserva histórico; flag pode ser ativada; limiar determinístico
    (mesmos inputs → mesma saída); limite Morris-Shin τ→0 é
    `c·k/(b·(1−k))` exato; sinaliza acima do limiar, cala abaixo;
    cala em `W=0` ou `observou=False`; modelo completo executa em
    ambos os modos.
  - DECISIONS R02a movido de "Aberto" para "Implementado (opt-in)".
  - **Integra a Prop. 2 ao ABM**: o modelo de coordenação intra-firma
    deixa de ser apenas heurística e passa a usar a derivação
    analítica fechada do jogo global (R02).
- **R06 — Portal da Transparência preenchido com dados verificados**.
  Segundo passo do padrão "go saito": após a infraestrutura, o agente
  de pesquisa em background extraiu números de fontes primárias
  indexadas (15 buscas em ~3 min). Constantes preenchidas em
  `calibracao/transparencia_cade.py`:
  - **N_SERVIDORES_TOTAL = 292** (Nota Técnica CADE 24/05/2022, via
    Direção Concursos);
  - **N_SERVIDORES_EFETIVOS_PROPRIOS = 34**;
  - **EPPGG lotados = 65** de 200 cargos criados por Lei 12.529/2011
    (déficit ≈ 67%, helper `deficit_eppgg()`);
  - **Tribunal = 7 conselheiros** (Lei 12.529/2011 art. 6º);
  - **ACs notificados 2024 = 712** (recorde; CADE 14/01/2025);
  - **PAs de conduta 2023 = 14 + 5 TCC** (ConJur balanço 2023) —
    **distinção crítica**: 712 (ACs/fusões) ≠ 14 (conduta), e é a
    segunda categoria que o WaaS endereça;
  - Leniências assinadas: 1 (2022), 2 (2023), 4 (2024) — Mattos Filho;
  - Multas 2023 = R$ 114,5 mi; tempo médio AC ordinário 117d → 93,9d
    (2023 → 2024); limiares Lei 12.529 art. 88: R$ 75 mi / R$ 750 mi.
  - **Pendências marcadas [?]** explicitamente em campo dedicado:
    decomposição SG/DEE (não publicada — pendente Relatório Integrado
    de Gestão), orçamento LOA (Portal da Transparência bloqueado via
    WebFetch, HTTP 405), contagem exata de procuradores e técnicos.
  - **REFERENCES.md** ganha 7 fontes verificadas para R06 + a
    pendência do Portal da Transparência marcada como `[?]`.
  - Testes expandidos para 24 (cobrindo cada constante verificada,
    cada marcação `[?]`, helpers de fallback, e estrutura estável).
  - **Recomendação substantiva preservada do agente**: tratar
    `UNIVERSO_FIRMAS_REGULADAS_ESTIMATIVA = (5.000, 20.000)` como
    variável de varredura Sobol — universo de firmas com receita ≥
    R$ 75 mi sob jurisdição da Lei 12.529 não tem corte primário
    publicado.
  - Total: 152 → 164 testes; gates limpos; main sincronizada.
- **R06 — Infraestrutura de calibração do Portal da Transparência**.
  Atende ao próximo movimento do balanço (capacidade do CADE) e à
  sugestão do autor de usar o Portal da Transparência como fonte.
  - Novo módulo `src/waas_antitrust/calibracao/transparencia_cade.py`
    com estrutura formal placeholder: `N_SERVIDORES_TOTAL`,
    `N_SERVIDORES_POR_CATEGORIA` (EPPGG/procuradores/técnicos/
    conselheiros/cargos comissionados), `N_SERVIDORES_POR_UNIDADE`
    (SG/CADE/DEE/Tribunal Administrativo), `ORCAMENTO_LOA_POR_ANO` e
    `EXECUCAO_ORCAMENTARIA_POR_ANO` cobrindo 2022-2024. Tudo em `None`
    até a extração ser concluída — marcação honesta.
  - Helpers: `servidores_sg_calibrado(default)` (devolve SG/CADE
    real quando preenchido; fallback no default em placeholder);
    `capacidade_efetiva_por_tique(trimestres_por_ano,
    casos_por_servidor_ano)` (estimativa empírica que retorna `None`
    em placeholder, sinalizando ao chamador para usar
    `INVESTIGACOES_ANUAIS_CADE/4`); `disponivel()` e `resumo()` para
    diagnóstico.
  - Padrão "go saito" replicado: agente de pesquisa em background
    explorando Portal da Transparência, Painel Estatístico de
    Pessoal MGISP, SIOP e fontes correlatas para preencher as
    constantes. Quando o agente retornar, segundo commit fechará a
    calibração com dados verificados.
  - DECISIONS R06 atualizado refletindo a infraestrutura pronta.
  - 12 testes em `tests/test_transparencia_cade_placeholder.py`
    cobrem estado placeholder, fallback dos helpers, monkeypatch da
    constante (precedência sobre default), piso de capacidade
    (nunca cai a zero), e estabilidade da estrutura (categorias e
    unidades canônicas). Total: 140 → 152 testes; gates limpos.
- **R03a — Saito (2021) extraído da fonte primária + cenários atualizados**.
  Sequência "go saito" entregue em dois movimentos coesos:
  1. **Infraestrutura**: `calibracao/saito.py` ganha helper
     `d_base_tcc_calibrado()` consultado por **todos os 7 cenários
     relevantes** via constante `_D_BASE_TCC` em `cenarios.py` — ponto
     único de consulta substituindo as 7 ocorrências hardcoded de
     `D_disc_base_tcc: 0.10`.
  2. **Extração**: agente de pesquisa baixou o PDF primário
     (Saito, Carolina, *TCC na Lei nº 12.529/11*, CADE/PNUD, 24/02/2021,
     349 TCCs 2012-2019, URL verificada em REFERENCES) e a §3.7.7 foi
     conferida diretamente. Achados:
     - **Autoria corrigida**: é **Carolina Saito** (não Pedro Saito).
     - **Mediana NÃO REPORTADA** pela autora — Saito reporta médias
       por posição na fila, não momento central.
     - Constantes nomeadas reais extraídas (Imagens 23 e 25,
       p. 38-39): 1ª SG/CADE = **43,43%**, 2ª = **34,51%**,
       3ª = **20,22%**, Tribunal/1ª = **15,00%**.
     - Faixas codificadas do Guia CADE de TCC (11/09/2017) adicionadas
       como fonte secundária.
     - Marcações explícitas para o que Saito **não** reporta (mediana,
       Q1/Q3, decomposição por tipo de conduta — a Imagem 21 traz
       alíquota da multa, NÃO desconto: caveat documentado).
  3. **Helper agora retorna 0,15 (média Tribunal — estimativa
     conservadora consistente com Saito e com o teto codificado pelo
     Guia CADE)** em vez do default histórico 0,10. Todos os 7
     cenários afetados herdaram o novo valor automaticamente via
     `_D_BASE_TCC` — **zero alterações em `cenarios.py`** além da
     refatoração inicial.
  4. **REFERENCES.md** atualizada com autoria correta + URL do PDF;
     `calibracao/cade.py` também corrigido. 13 testes em
     `test_saito_placeholder.py` cobrem: metadados verbatim, médias
     por posição (Imagens 23/25), faixas Guia CADE, marcações [?],
     helper retorna média Tribunal por default, monkeypatch da
     mediana tem precedência. Total: 127 → 140 testes; gates limpos.
- **R19 — Choques exógenos discretos (Eurace@Unibi)**. Preparação
  do "go saito": `calibracao/saito.py` ganha helper
  `d_base_tcc_calibrado(default=0.10)` que devolve `MEDIANA_DESCONTO_TCC_2012_2019`
  quando preenchido, fallback no default quando placeholder.
  `cenarios.py` consulta o helper via constante `_D_BASE_TCC` no topo do
  módulo — **ponto único de consulta** substituindo as 7 ocorrências
  hardcoded de `D_disc_base_tcc: 0.10`. Resultado: quando a extração
  manual da tabela principal de Saito (349 TCCs CADE 2012-2019) for
  concluída e a constante for preenchida, todos os 7 cenários
  (`resolucao_pura`, `resolucao_mais_portaria_mte`, `lei_waas_pura`,
  `lei_waas_com_fundo_honorarios`, `lei_waas_com_vesting_padrao`,
  `mercado_digital_br_pareto`, `cenario_sancao_dura`) herdam o valor real
  **sem mudança no `cenarios.py`** — basta o diff de uma linha em
  `saito.py`. Cinco testes novos em `tests/test_saito_placeholder.py`
  cobrem: placeholder detectado por `disponivel()`, helper retorna
  default quando placeholder, helper retorna Saito quando preenchido
  (via `monkeypatch`), `resumo()` descreve o estado, e
  `N_TCC_SAITO_2012_2019 = 349` verbatim. Teste impactado
  `test_aplicar_cenario_nao_muta_params_original` reescrito para
  comparar contra `d_base_tcc_calibrado()` em vez do literal 0,10 —
  invariante semântica preservada. Total: 127 → 132 testes; gates
  verdes; HEAD sincronizada com main + origin.
- **R19 — Choques exógenos discretos (Eurace@Unibi)**. Atende a "como
  o modelo lida com choques?" + à hipótese substantiva "os layoffs
  podem ser oportunidade?". O modelo deixa de ser estacionário-
  estocástico e ganha um mecanismo de **eventos discretos** no tempo.
  - **Módulo novo** `src/waas_antitrust/choques.py` com dataclass
    `Choque(tique, tipo, magnitude, descricao)` validada e função
    `aplicar_choque(modelo, choque)`. Quatro tipos canônicos: `layoff`
    (converte fração de trabalhadores a `ex_funcionario`),
    `caso_paradigmatico` (pulso em `p_perc`, efeito Schelling),
    `campanha_cade` (eleva `rho_acuracia` da autoridade) e
    `choque_juridico` (eleva `p_anulacao_tcc`).
  - **`TrabalhadorAgent.status`** ∈ {`"ativo"`, `"ex_funcionario"`}.
    Ex-funcionário tem `r` efetivo multiplicado por
    `fator_represalia_ex_funcionario` (default 0,2 — "o demitido já
    perdeu o emprego") e preserva capacidade de sinalizar via
    `historico_observou > 0`. Aplica-se aos arquétipos `racional` e
    `fairminded` em `agents.decidir_sinal`.
  - **Quatro catálogos canônicos**: `CHOQUES_TECH_2022_2024` (ondas
    jan/2023 e jan/2024, magnitudes 6% e 4% — calibração frouxa contra
    layoffs.fyi); `CHOQUES_CAMPANHA_CADE_DIGITAL` (pulso DT-003/2022);
    `CHOQUES_CASO_PARADIGMATICO_IFOOD_2023` (TCC iFood);
    `CHOQUES_JURIDICO_ADVERSO` (decisão hipotética STJ ativando F6).
  - **Choques aplicados no início de `step()`**, antes de P0. Reporters
    novos: `n_ex_funcionarios`, `n_choques_layoff_aplicados`,
    `n_choques_paradigmaticos_aplicados`.
  - **15 testes** em `tests/test_choques.py`: validação de Choque
    (tipo/tique/magnitude), aplicação direta de cada tipo, integração
    pelo `step` no tique correto, modelo sem choques preserva
    comportamento (compat), ex-funcionário tem represália efetiva
    menor (validação direcional da hipótese substantiva), catálogos
    executam end-to-end.
  - **v0 simplificação documentada**: efeitos instantâneos que se
    propagam pela dinâmica adaptativa; duração explícita fica para
    v1. Calibração formal de magnitudes pendente em R03.
  - **Frameworks estabelecidos referenciados**: Eurace@Unibi (Dawid et
    al.) para choques em ABM macro; resposta à pergunta do autor
    sobre adesão a frameworks consolidados.
  - Total: 112 → 127 testes; ruff/black/mkdocs --strict limpos.
- **R13a + R03 (primeira ponta) + Saito placeholder** — três itens
  inter-relacionados da Frente A do roadmap (impacto/custo alto, sem
  decisão normativa):
  - **R13a** — `WaaSParametros.distribuicao_fatia_mercado` aceita
    `"uniforme"` (default), `"pareto"` (α=1,16 regra 80/20) ou
    `"lognormal"` (σ=1,0). Novo método `WaaSModel._sortear_fatias_mercado`
    sorteia e normaliza. Reporter **HHI** (índice Herfindahl-Hirschman)
    exposto pelo DataCollector. Novo cenário `mercado_digital_br_pareto`
    em `cenarios.py` (8 cenários no catálogo agora — Regime C + Pareto).
    7 testes em `tests/test_fatia_pareto.py`. Fecha o item (ii) de R13
    (endgame do paper, Eco B).
  - **R03 (primeira ponta)** — novo `scripts/calibrar.py`: varredura em
    grade sobre (`taxa_observacao`, `taxa_falso_reporte`, `rho`)
    minimizando erro quadrático relativo médio contra os 3 alvos do ODD
    (5 leniências/ano, 47 TCC/ano, 19% DMZ) com multi-seed averaging.
    `--grid N` e `--seeds ...`; saída tabular ou JSON. **Achado direto
    da primeira rodada:** parâmetros default produzem ~1 TCC/ano contra
    alvo 47 — o **gap de escala** revela dependência forte de R06
    (reescalonar capacidade ao universo do CADE), agora documentado.
  - **Saito placeholder** — novo módulo `src/waas_antitrust/calibracao/saito.py`
    com docstring rigoroso, constantes a preencher
    (`MEDIANA_DESCONTO_TCC_2012_2019`, `Q1`, `Q3`, decomposição por
    tipo) e procedimento de extração manual da tabela principal da
    dissertação. Função `disponivel()` + `resumo()` para diagnóstico.
    Quando preenchido, fecha `D_disc_base_tcc` em `cenarios.py`. R03 e
    R13 atualizados em DECISIONS refletindo o estado.
  - Total: 105 → 112 testes; gates verdes (ruff/black/mkdocs --strict).
- **R16, R17, R18 — pressupostos teóricos mais robustos** (resposta à
  crítica do autor + PDF Torsell 2026 enviado por anexo).
  - **R16 — Arquétipo fairminded + inequity aversion (Torsell 2026,
    Fehr-Schmidt 1999)**: `TrabalhadorAgent.ARQUETIPOS` ganha o quinto
    arquétipo `"fairminded"`. Em `decidir_sinal`, FM computa payoff
    racional base + prêmio ético `α · φ_vizinhos · w_a`. Parâmetros
    novos: `peso_inequity_aversion` (default 0 ⇒ FM degenera em racional)
    e `distribuicao_arquetipos` (default None ⇒ Hokamp-Pickhardt
    clássico, sem FM — preserva calibração). Preset `DISTRIBUICAO_COM_FAIRMINDED`
    em `cenarios.py`. **Resultado central de Torsell 2026** (FM domina HE
    sob fictitious play) motiva o modelo do **break-even ético coletivo**:
    o ponto de virada onde calar passa a ser desigualdade moral mais
    custosa do que falar, emergente sem hardcoding.
  - **R17 — Cenários normativos como variantes paramétricas**: novo
    módulo `src/waas_antitrust/cenarios.py` com 7 cenários canônicos
    (`status_quo`, `resolucao_pura`, `resolucao_mais_portaria_mte`,
    `lei_waas_pura`, `lei_waas_com_fundo_honorarios`,
    `lei_waas_com_vesting_padrao`, `cenario_sancao_dura`). Dataclass
    `Cenario` com `nome`/`descricao`/`sobrescritas`. Função
    `aplicar_cenario(params, cenario)` retorna novo `WaaSParametros` via
    `dataclasses.replace`. Cobertura mínima: pelo menos um cenário em
    cada regime A/B/C; vesting padrão respeita gating jurídico R07 (só
    em C). Trata alterações regulatórias como **cenários comparáveis e
    reprodutíveis**, não notas textuais.
  - **R18 — Commitment da firma + sanção catastrófica** ("se não paga,
    perdem tudo"): dois canais simétricos de commitment. (i)
    `prob_pagamento_perc ∈ [0,1]` — trabalhadores racionais e FM
    descontam W esperado por essa probabilidade (commitment problem
    clássico). (ii) `p_descumprimento_tcc` + `multa_descumprimento_tcc`
    — firma que assina e descumpre sofre multa adicional em múltiplos da
    sanção base. Reporters novos: `n_firmas_quebraram_tcc`,
    `multa_descumprimento_acum`.
  - **17 testes novos** em `tests/test_fairminded_cenarios.py`. Total:
    88 → 105 testes. Gates verdes (ruff/black/mkdocs --strict limpos).
  - **REFERENCES expandida** com nova seção "Inequity aversion e evolução
    de preferências (base de R16)": Fehr-Schmidt (1999), Bolton-Ockenfels
    (2000), Güth-Yaari (1992), Skyrms (1996), Huck-Oechssler (1999),
    Nowak-Page-Sigmund (2000), Henrich et al. (2001), **Torsell (2026,
    *Theory and Decision*)** com DOI verificado, Fudenberg-Levine (1998),
    Camerer-Ho (1999).
  - **`docs/mecanismo.md` (Ato 2)** ganha duas seções novas:
    "O break-even ético coletivo (R16)" — derivação narrativa do canal
    fairminded; e "Cenários normativos como variantes paramétricas
    (R17)" — tabela dos 7 cenários e exemplo de uso programático.
- **Pivotagem estética e argumentativa radical** (decorrente da crítica
  continuada do autor "tá muito cru ainda; falta corpo; pivotagem
  radical; conte uma história concatenada no UX"). O site foi
  reescrito como **arco narrativo em 5 atos**:
  - **Ato 1 · O problema** (`index.md`): diagnóstico — leniência clássica
    bate num muro em mercados digitais (abuso unilateral, sem cúmplice);
    Art. 12 da Res. 21/2018 como oportunidade institucional já existente;
    tabela dos 3 regimes; navegação por persona em grid cards;
    callouts numéricos e `pull-quote` flanqueada; hook para Ato 2.
  - **Ato 2 · O mecanismo** (`mecanismo.md`): IC-F* em prosa antes da
    fórmula; exemplo numérico desenvolvido (R$ 1B receita ⇒ S = R$ 75M,
    D_total = R$ 22,5M, D_base = R$ 7,5M, D_extra = R$ 15M, W = R$ 2,7M,
    margem R$ 12,3M) com dois callouts dramáticos; três vetores de
    quebra A/B/C com nome empírico no modelo; tabela IR-W/IC-T/IC-F*;
    hook para Ato 3.
  - **Ato 3 · Resultados** (`resultados.md`): a simulação como
    *testemunho* (20 firmas, 40 trimestres); painéis (A) e (B)
    explicados como evidência; multi-seed bootstrap CI 95% que não
    cruza zero apresentado como segurança contra cherry-picking de
    seed; regimes adversariais como falsificadores quantitativos;
    como reproduzir (Colab + Sobol); hook para Ato 4.
  - **Ato 4 · Limitações** (`limitacoes.md`): fragilidade jurídica do
    Regime B em três frentes (re-caracterização do Art. 12, reserva
    de lei para R07, colisão com Art. 86); calibração faltando (R03
    contra Saito 2021, DEE/CADE 2022/2024, Wiedman-Zhu 2023); pesos
    do bem-estar provisórios (R05); Proposições 1-3 com status
    explícito; 5 decisões normativas R09-R13; o que **já** está
    sustentado (simetria); hook para Ato 5.
  - **Ato 5 · Colaborar** (`colaborar.md`, página nova): reproduzir e
    derrubar (comandos prontos); contribuir com calibração externa
    contra três bancos de dados específicos; discordar do desenho
    (R09-R13 abertas); história institucional (Felipe Roquete, IPEA
    independente); citação, licença, contato.
  - **CSS expandido** (`docs/stylesheets/extra.css`): classes `.lead`
    (parágrafo introdutório maior), `.numero-callout` (valor central
    em peso 600 com legenda em 38em), `.pull-quote` (citação flanqueada
    com borda esquerda turquesa), `.ato-fim` (bloco de conclusão verde
    com link para próximo ato), `.ato-chip` ("Ato N de 5" em letter-spacing
    alargado). Tipografia editorial: H1/H2 com letter-spacing negativo,
    H2 com 2,6em de respiro superior. Modo escuro tratado em todos.
  - **Nav reorganizada** (`mkdocs.yml`): "Ato 1 · O problema", "Ato 2 ·
    O mecanismo", etc., como itens de primeiro nível; "Anexos" agrupa
    Como usar, Glossário, ODD, Institutional, References, API;
    "Desenvolvimento" mantém crítica x10, plano de melhorias,
    decisões.
  - `README.md` ajustado: cita "5 atos" e usa D_extra na linha do
    incremento.
  - Sem regressão de testes (88 verdes; ruff/black/mkdocs --strict
    limpos).
- **R15 — Vetores de quebra do mecanismo (resposta à crítica direta do
  autor)**. Três perguntas céticas materializadas no modelo e em uma página
  narrativa expandida (`docs/mecanismo.md`):
  - **Vetor A — TCC clássico já dá desconto**: novo parâmetro
    `D_disc_base_tcc` em `WaaSParametros`. A IC-F* correta compara `W`
    contra o **incremento** `D_extra = D_disc − D_disc_base_tcc`, NÃO
    contra o desconto total. Default 0 preserva comportamento; com
    `D_base ≥ D_total` ninguém paga W. Contador
    `n_firmas_optaram_tcc_classico` registra materialização.
  - **Vetor B — anulação judicial do TCC** (falsificador F6 explicitado):
    novo parâmetro `p_anulacao_tcc`. Em P4, TCC válido sorteia anulação
    com essa probabilidade; quando anulado, a multa cheia retorna ao
    erário. Contador `n_tcc_anulados`. Calibrar `p_anulacao` falsifica F6
    quantitativamente.
  - **Vetor C — custos legais do denunciante** (advogado, defesa
    trabalhista, eventual partícipe sob Art. 86): novo parâmetro
    `custo_legal_uw` em unidades de `w_a` (0,1–0,5 realista no Brasil).
    Entra na IR-W do arquétipo racional via `agents.decidir_sinal`.
  - Nova página `docs/mecanismo.md` ("Como o mecanismo se sustenta") com
    aritmética da IC-F* em exemplo numérico (R$ 1B receita, σ=0,5 ⇒
    `D_extra` = R$ 15M vs. `W` = R$ 2,7M), três cenários institucionais
    para quem cobre o custo legal (denunciante, empresa via TCC, Estado
    via fundo) e §"Onde isto ainda pode ruir" listando gaps abertos
    (R03/R09/R10/R13). Inserida cedo na navegação (entre Início e
    Resultados). `docs/index.md` ganha card "Cético — e se a empresa não
    pagar?" apontando direto para a página, e a "tese técnica" foi
    reescrita usando `D_extra` em vez de `D` total.
  - 8 testes em `tests/test_vetores_quebra.py` (vetores A/B/C
    individualmente + combinação adversa). Total: 80 → 88.
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
