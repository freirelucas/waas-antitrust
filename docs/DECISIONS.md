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
| R05 | Bem-estar coerente / pesos | **Implementado (parcial):** `bem_estar` redefinido como −(dano + β·FP + γ·custo) — credita a dissuasão (R01) em vez de premiar detecção. Resta calibrar os pesos β/γ contra estimativas de dano ao consumidor e custo de erro (R03). |
| R06 | Reescalonar capacidade ao universo do CADE | Hoje `capacidade_tique` é fração do sistema simulado limitada por INVESTIGACOES_ANUAIS_CADE/4; o reescalonamento para o universo nacional é aproximação (liga-se a E01). |
| R07 | Ameaça crível de êxodo coletivo (Hirschman exit-with-equity) | **Implementado (exploratório, com caveats jurídicos e tributários abaixo):** módulo `hirschman.py` (puro, testado) + integração em P0 (camada preventiva via `g_i_efetivo`) e P3 (IC-F* ampliada `D + custo_exodo > W`). Parâmetros provisionais (vesting 4y/1y cliff; custo de substituição ~50% w_a; equity ~50% w_a; ~50% non-vested). Novos reporters: `n_firmas_sob_ameaca_exodo`, `custo_exodo_acum`. **Caveat institucional (Adv B, crítica x10):** Resolução do CADE não pode impor cláusula contratual padrão de vesting nem proteção trabalhista (reserva de lei, Art. 22, I, CF); portanto, `fracao_contratos_acelerados > 0` é coerente apenas com o **Regime C** (via lei). O modelo hoje aceita o parâmetro em qualquer regime; **gating estrutural** está rastreado na Categoria 4 do plano de melhorias. **Caveat de escopo (Adv B):** a Lei 13.608/2018 (Art. 4º-C, §3º) **não cobre antitruste no eixo recompensa** — restringe a "crimes contra a administração pública"; extensão analógica anti-represália é hipótese, não jurisprudência consolidada. **Caveat tributário (Adv B):** o valor bruto do vesting acelerado no Brasil sofre haircut de **40–50% por IRPF + INSS** (natureza salarial vs. mercantil ainda em formação na jurisprudência pós Lei 13.467/2017); o modelo opera em bruto, portanto **superestima** o exit-threat — função `valor_liquido_pos_tributos` planejada na Categoria 4. **Caveat de overclaim documental:** o docstring antigo dizia "padrões YC"; YC/NVCA cobrem aceleração apenas para *change of control*, **não** para gatilho de ação coletiva — o gatilho aqui modelado é **construção normativa proposta pelo projeto**, e o docstring foi corrigido. Resta: calibrar `peso_hirschman`, `valor_equity`, `fator_substituicao` (R03), e modelar a opção "corrigir conduta sem pagar" como terceira via. |
| R08 | Heterogeneidade conduta × ator crítico | **Implementado (exploratório):** módulo `condutas.py` com catálogo de 7 condutas canônicas digitais (self_preferencing, tying, predatory pricing, killer acquisitions, dark patterns, acesso API/dados, MFN), cada uma com seus *atores primários* (eng/produto/design/growth/comercial/juridico/corpdev). Trabalhadores ganham `papel`; firmas ganham `conduta_potencial`. A `observabilidade(papel, conduta)` modula `taxa_observacao` em P0. Teste end-to-end confirma direcionalmente que engenheiros observam mais self_preferencing que designers. Resta refinar o catálogo com pesquisa de mercado brasileiro (pesquisa de fundo em andamento) e calibrar pesos de observabilidade contra survey/literatura (R03). |

Itens correlatos já rastreados: migração das 9 viz do caderno (T01) e adoção das
classes de espaço do Mesa para a rede intra-firma (T02).

## Histórico de decisões fechadas

| # | Decisão | Resolução | Data |
|---|---|---|---|
| F01 | Linguagem: anglicismos? | Sem anglicismos quando houver termo português. Siglas mantidas. | 2026-05-26 |
| F02 | Licença | CC-BY-SA 4.0 | 2026-05-26 |
| F03 | Estrutura do pacote | src/ layout, Python 3.12+ (mesa≥3.5 exige 3.12) | 2026-05-26 |
