# Decisões em aberto e backlog

Decisões rastreadas que afetam o desenho do mecanismo ou a arquitetura do código.

## Conceituais

| # | Decisão | Status | Observação |
|---|---|---|---|
| D01 | Caminho via Resolução vs. via Lei | aberta | Preferência inicial: Resolução. Reverificar com falsificador F6. |
| D02 | Modelar a Assessoria jurídica como agente estratégico? | aberta | Hoje colapsada em intermediário transparente. |
| D03 | Calibrar topologia de redes intra-firma via instrumento empírico | aberta | Requer survey ou aproximação via LinkedIn (aprovação ética). |
| D04 | Co-autoria com Felipe Roquete | aberta | Hipótese original surgiu em conversa de 06/09/2022. |
| D05 | Versão completa da IC-F* (não simplificada) | aberta | Hoje usa D > W. A Fase 2 ligou a acurácia da autoridade à qualidade da prova, mas a dissuasão (p_detecção endógeno) segue aberta — ver R01. |
| D06 | Análise dogmática "vítima-empregado" no Art. 12 da Res. 21/2018 | aberta | Adv A/B convergiram que "vítima" é categoria coletiva e o empregado-denunciante é testemunha qualificada (ou partícipe → colisão com Art. 86). Necessária análise dogmática própria e seção no paper (esboço já em `docs/INSTITUTIONAL.md` § "Quem é vítima?"). Charneira do falsificador F6. |

## Técnicas

| # | Decisão | Status | Observação |
|---|---|---|---|
| T01 | Migrar viz 3 a 11 do caderno para módulos | aberta | Hoje só inversão e fase têm módulo. |
| T02 | Adotar Mesa 3.x space classes para a rede intra-firma | aberta | Hoje uso direto de NetworkX. |
| T03 | Integração contínua com Zenodo | aberta | Workflow `.github/workflows/release.yml` pronto; falta vincular conta. |
| T04 | Adicionar DVC para versionamento de dados brutos | aberta | Pasta `data/raw/` reservada. |
| T05 | Cobertura de testes acima de 80% | fechada | Cobertura 93% (modo rápido): modelo, agentes, sobol (execução + análise) e viz (figuras + stubs). |

## Empíricas

| # | Decisão | Status | Observação |
|---|---|---|---|
| E01 | Triangular número de empregados em subsidiárias Big Tech BR | aberta | RAIS/CAGED via MTE. |
| E02 | Construir série temporal completa de TCCs do CADE | aberta | Saito 2021 cobre 2012-2019; estender até 2024. |
| E03 | Levantar série de represálias trabalhistas em casos relevantes | aberta | TST + CGU + MPT. |
| E04 | Verificar texto integral da Resolução 21/2018, Art. 12 | aberta | Conferir contra publicação no Diário Oficial. Pendência explicitada também no `paper/main.tex` (rodapé TODO em §Mecanismo); enquanto não fechada, o paper cita o Art. 12 de memória — risco rastreado. |
| E05 | Calibrar distribuição de papéis em marketplace BR (R08) | aberta | `DISTRIBUICAO_PAPEIS_PADRAO` foi parametrizada para perfil tipo big tech madura; PM apontou que marketplaces brasileiros (iFood, Mercado Livre) são operations-heavy. Necessário survey/levantamento de organogramas ou aproximação via LinkedIn. Liga-se a presets `MARKETPLACE_BR` × `BIGTECH_MADURA` na Categoria 5 do plano de melhorias. |

## Backlog pós-crítica (Fase 3 — pesquisa)

Itens levantados na crítica de 2026-05-26. As alegações infladas correspondentes
já foram neutralizadas nas Fases 1–2 (texto e código); estes itens são o trabalho
de pesquisa necessário para *sustentar* — não apenas alegar — cada ponto.

| # | Item | Abordagem recomendada |
|---|---|---|
| R01 | Dissuasão endógena (Prop. 3) | **Implementado:** a firma viola enquanto g_i = ganho/sanção > detecção percebida (expectativa adaptativa, λ). B/C deter; A não. `dano_acumulado` exposto; teste de regressão em `tests/test_model.py`. *Suavização Beta-Binomial (Categoria 2, Mat A):* `p_realizado` agora é o MAP `(vp + α)/(n_viol + α + β)`, removendo a singularidade em `n_viol = 0` e estabilizando a variância em n pequeno (`α=1, β=5` ⇒ prior centrado em ~16,7%; calibrar em R03). Resta calibrar λ e os hiperparâmetros (α, β) (R03). |
| R02a | Integração do `x*` no ABM (decisão dos arquétipos) | **Aberto:** `jogo_global.x*(b,c,k,τ)` está derivado em forma fechada (e testado), mas `agents.py::decidir_sinal` ainda usa heurísticas hardcoded (limiar 0,30 no "imitativo"). Substituir o gatilho do arquétipo "racional" por `s_i ≥ x*` é a integração mínima. Item normativo na Categoria 7 do plano. |
| R02b | Contraste multiplicidade × unicidade (Morris-Shin) | **Aberto:** a Prop. 2 invoca Morris-Shin 1998 sem demonstrar numericamente a multiplicidade sob conhecimento comum (a contrapartida que torna a seleção de equilíbrio único de fato informativa). Falta um experimento que exiba os dois ramos. |
| R02c | Unicidade do equilíbrio sob heterogeneidade | **Conjectura aberta:** Morris-Shin supõe homogeneidade. Com arquétipos (R01) + papéis (R08), não há resultado fechado conhecido para o mix. Marcar como conjectura no `ODD.md` (feito) e deixar como pesquisa futura. |
| R02 | (legado) Jogo global de fato (Prop. 2) | **Particionado em R02a / R02b / R02c** após a crítica x10 (Mat B). Os subitens preservam o conteúdo original com granularidade suficiente para rastrear a integração ABM, o contraste numérico de multiplicidade e a unicidade sob heterogeneidade separadamente. |
| R03 | Calibração + validação reais | Rotina que ajusta parâmetros aos alvos do ODD (109 leniências; 47 TCC/ano; 19% Dyck-Morse-Zingales) e reporta aderência. Hoje os alvos não restringem o modelo; a "calibração" é documental. |
| R04 | Canal de falso reporte | **Parcial (implementado):** `taxa_falso_reporte` gera reportes errôneos/maliciosos contra não-violadoras (prova fraca q=0,15) ⇒ FP>0 e precisão deixa de ser trivial; teste de regressão em `tests/test_model.py`. Falta: represália a falsos reportes e calibração da taxa. |
| R05 | Bem-estar coerente / pesos | **Implementado (Categoria 3 da crítica x10):** `bem_estar` agora é `−(dano + β·FP + γ·custo_recompensa + δ_exodo·custo_exodo − δ_multa·multa_arrecadada)/w_a` — credita a prevenção (R01), agrega o custo de êxodo de Hirschman (R07), e credita a multa arrecadada pelo erário (transferência ao Estado). Reporters novos: `dano_economico_acum` (ponderado por fatia de mercado — colapsa em `dano_acumulado/n_empresas` sob fatias uniformes, mas vira métrica significativa quando a heterogeneidade Pareto/lognormal for introduzida) e `multa_arrecadada_acum` (VP sem TCC ⇒ multa cheia; VP com TCC ⇒ residual). Pesos provisórios (β=1, γ=0, δ_exodo=0.5, δ_multa=1.0); calibrar contra Connor-Lande (overcharge mediano 15–25%) e Polinsky-Shavell (custo FP ≈ 1–2× sanção) em R03. |
| R06 | Reescalonar capacidade ao universo do CADE | Hoje `capacidade_tique` é fração do sistema simulado limitada por INVESTIGACOES_ANUAIS_CADE/4; o reescalonamento para o universo nacional é aproximação (liga-se a E01). |
| R07 | Ameaça crível de êxodo coletivo (Hirschman exit-with-equity) | **Implementado (exploratório, com caveats jurídicos e tributários abaixo):** módulo `hirschman.py` (puro, testado) + integração em P0 (camada preventiva via `g_i_efetivo`) e P3 (IC-F* ampliada `D + custo_exodo > W`). Parâmetros provisionais (vesting 4y/1y cliff; custo de substituição ~50% w_a; equity ~50% w_a; ~50% non-vested). Novos reporters: `n_firmas_sob_ameaca_exodo`, `custo_exodo_acum`. **Gating jurídico (Categoria 4 implementada):** sob Regime A ou B, `fracao_contratos_acelerados > 0` é incoerente (Resolução do CADE não pode impor cláusula contratual padrão — reserva de lei, Art. 22, I, CF); o `WaaSModel.__init__` agora **força** `fracao_contratos_acelerados = 0` nesses regimes e emite `UserWarning`. Apenas o **Regime C** (via lei) preserva o parâmetro. Teste em `tests/test_hirschman.py`. **Caveat de escopo (Adv B):** a Lei 13.608/2018 (Art. 4º-C, §3º) **não cobre antitruste no eixo recompensa** — restringe a "crimes contra a administração pública"; extensão analógica anti-represália é hipótese, não jurisprudência consolidada. **Caveat tributário implementado:** função `valor_liquido_pos_tributos(valor_bruto, aliquota_efetiva=0.4)` aplica haircut IRPF + INSS sobre o vesting (substituição NÃO sofre haircut — é despesa operacional da firma). Parâmetro `aliquota_tributaria_vesting` em `WaaSParametros` (default 0.0 para compat; ~0.4 para realismo). Resta: calibrar `peso_hirschman`, `valor_equity`, `fator_substituicao`, `aliquota_tributaria` (R03), e modelar a opção "corrigir conduta sem pagar" como terceira via. |
| R14 | Enriquecimento heterogêneo dos agentes | **Implementado (exploratório).** TrabalhadorAgent ganha `anos_carreira` (Exponencial), `fracao_vested_individual` (cliff 1y + linear até 4y), `tolerancia_represalia` (heterogeneidade individual, padrão homogêneo 1.0; ativar com `sigma_tolerancia_represalia>0`), e memória `historico_observou`. EmpresaAgent ganha `cultura_compliance ∈ [0,1]` (sorteio U[0,1]; modula σ efetiva via `peso_cultura_compliance·cultura`), `poder_retaliacao` (proxy = `fatia_mercado`, ainda não acionado), e memória `n_denuncias_acum`. AutoridadeAgent ganha `prioridade_digital ∈ [0,1]` (eleva ρ na P4; default 0 preserva comportamento original). Tudo opt-in por defaults; canais ortogonais ao R01 (não violam Proposições). Testes direcionais em `tests/test_agentes_enriquecidos.py` (7 casos). Resta: usar `fracao_vested_individual` por trabalhador em `custo_exodo_esperado` (refinar R07), e implementar canal de `poder_retaliacao` (modula `r_represalia` localmente). |
| R08 | Heterogeneidade conduta × ator crítico | **Implementado (exploratório; Categoria 5 da crítica x10):** módulo `condutas.py` com catálogo de **9 condutas** (7 canônicas digitais + 2 específicas BR: `exclusividade_retaliacao_marketplace` — iFood TCC 2023 + indícios Mercado Livre 2024-2025; `anti_steering_iap` — Apple Brasil CADE dez/2025, Epic v. Apple EUA 2021). `PAPEIS_PADRAO` ganha **`operacoes`** (marketplaces BR são operations-heavy) e **`financeiro`** (FP&A em predatory pricing). Trabalhadores ganham `papel`; firmas ganham `conduta_potencial`. **Gradiente 3-níveis** (Near & Miceli): primário=1.0, **adjacente=0.5**, distal=0.1 — substituiu o binário 1.0/0.2. Cada conduta ganha `atores_adjacentes`. Dois presets de distribuição de papéis: `BIGTECH_MADURA` (eng-heavy, default) e `MARKETPLACE_BR` (operations-heavy). Teste end-to-end confirma direcionalmente que engenheiros observam mais self_preferencing que designers; testes específicos cobrem o gradiente 3-níveis, os presets e as condutas BR. Resta: calibrar distribuição de papéis em marketplace BR contra organogramas/LinkedIn (E05), e calibrar pesos de observabilidade contra survey/literatura (R03). |

Itens correlatos já rastreados: migração das 9 viz do caderno (T01) e adoção das
classes de espaço do Mesa para a rede intra-firma (T02).

## Pendências normativas — Categoria 7 da crítica x10

Itens da [Crítica x10](critica_x10.md) que alterariam material e Proposições
centrais do modelo. Ficam aqui como decisões **suas** (autor): não cabem ao
piloto automático porque mudam interpretação teórica ou de mecanismo, e exigem
conversa explícita antes da execução.

| # | Origem | Decisão pendente |
|---|---|---|
| R09 | Eco A | Endogeneizar `g_i(t) = π·R / (p·S)` como função do estado, não constante. **Altera Prop. 3** (canal de dissuasão deixaria de ser pelo gating estático de `g_i > p_perc` e passaria a refletir feedback `g_i ↘ quando p ↗`). Avaliar: o ganho de realismo justifica revisitar o esboço da Prop. 3? |
| R10 | Eco A | IC-F* completa: substituir `D > W` por `W + p_pago·(S − D) < p_npago·S`. **Altera Prop. 1**. Hoje a IC-F* assume que o caminho "não paga" é dominado por suposição estrutural — Eco A aponta que isso vicia qualquer alegação sobre economizar contribuição pecuniária. Implementação não-trivial. |
| R11 | Eco A | Hirschman como elevação de `W_esperado` em vez de subtração de `g_i`. **Altera microfundamento de R07** (cláusula vira *pagamento condicional* na IC do trabalhador, não desconto na atratividade da firma). Avaliar a equivalência analítica antes de implementar. |
| R12 | Mat B | Substituir o arquétipo "racional" por estratégia-limiar `s_i ≥ x*` do `jogo_global`. **Integra Prop. 2** ao ABM e fecha o R02a. Mais ambicioso: contraste numérico multiplicidade × unicidade no espírito Morris-Shin (R02b). |
| R13 | Adv A, Eco B, Designer, PM | Conjunto de itens "endgame" para o paper: (i) parâmetro `p_anulacao_tcc` simulado (transforma F6 em falsificador de fato, Adv A); (ii) distribuição Pareto/lognormal de `fatia_mercado` (R03 dependência empírica, Eco B); (iii) promover `sankey.py` de stub a fluxograma real do mecanismo (Designer); (iv) escolher 3 condutas-piloto para o paper (marketplace_exclusividade, anti_steering, killer_acq_ia) com fixtures e testes de regressão (PM). |

## Histórico de decisões fechadas

| # | Decisão | Resolução | Data |
|---|---|---|---|
| F01 | Linguagem: anglicismos? | Sem anglicismos quando houver termo português. Siglas mantidas. | 2026-05-26 |
| F02 | Licença | CC-BY-SA 4.0 | 2026-05-26 |
| F03 | Estrutura do pacote | src/ layout, Python 3.12+ (mesa≥3.5 exige 3.12) | 2026-05-26 |
