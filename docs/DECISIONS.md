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
| E04 | Verificar texto integral da Resolução 21/2018, Art. 12 | aberta | Conferir contra publicação no Diário Oficial. |

## Backlog pós-crítica (Fase 3 — pesquisa)

Itens levantados na crítica de 2026-05-26. As alegações infladas correspondentes
já foram neutralizadas nas Fases 1–2 (texto e código); estes itens são o trabalho
de pesquisa necessário para *sustentar* — não apenas alegar — cada ponto.

| # | Item | Abordagem recomendada |
|---|---|---|
| R01 | Dissuasão endógena (Prop. 3) | **Implementado:** a firma viola enquanto g_i = ganho/sanção > detecção percebida (expectativa adaptativa, λ). B/C deter; A não. `dano_acumulado` exposto; teste de regressão em `tests/test_model.py`. *Caveat:* p_percebida = vp/violadoras é ruidosa com poucas violadoras (pode super-deter em n pequeno) — suavizar/Bayes fica para R03. Resta calibrar prior/λ (R03). |
| R02 | Jogo global de fato (Prop. 2) | **Exploratório:** `jogo_global.py` deriva o limiar único x*(b,c,k,τ) do subgame estilizado e verifica a convergência quando τ→0 (teste). Resta: contrastar com a multiplicidade sob conhecimento comum, generalizar (ganho/massa crítica) e integrar à dinâmica de arquétipos do ABM. |
| R03 | Calibração + validação reais | Rotina que ajusta parâmetros aos alvos do ODD (109 leniências; 47 TCC/ano; 19% Dyck-Morse-Zingales) e reporta aderência. Hoje os alvos não restringem o modelo; a "calibração" é documental. |
| R04 | Canal de falso reporte | **Parcial (implementado):** `taxa_falso_reporte` gera reportes errôneos/maliciosos contra não-violadoras (prova fraca q=0,15) ⇒ FP>0 e precisão deixa de ser trivial; teste de regressão em `tests/test_model.py`. Falta: represália a falsos reportes e calibração da taxa. |
| R05 | Bem-estar coerente / pesos | **Implementado (parcial):** `bem_estar` redefinido como −(dano + β·FP + γ·custo) — credita a dissuasão (R01) em vez de premiar detecção. Resta calibrar os pesos β/γ contra estimativas de dano ao consumidor e custo de erro (R03). |
| R06 | Reescalonar capacidade ao universo do CADE | Hoje `capacidade_tique` é fração do sistema simulado limitada por INVESTIGACOES_ANUAIS_CADE/4; o reescalonamento para o universo nacional é aproximação (liga-se a E01). |
| R07 | Ameaça crível de êxodo coletivo (Hirschman exit-with-equity) | **Implementado (exploratório):** módulo `hirschman.py` (puro, testado) + integração em P0 (camada preventiva via `g_i_efetivo`) e P3 (IC-F* ampliada `D + custo_exodo > W`). Parâmetros YC-padrão (vesting 4y/1y cliff; custo de substituição ~50% w_a; equity ~50% w_a; ~50% non-vested). Novos reporters: `n_firmas_sob_ameaca_exodo`, `custo_exodo_acum`. Resta: calibrar `peso_hirschman`, `valor_equity`, `fator_substituicao` contra dados YC reais (R03), e modelar a opção "corrigir conduta sem pagar" como terceira via (hoje a firma sem cláusula apenas escolhe pagar/não-pagar). |

Itens correlatos já rastreados: migração das 9 viz do caderno (T01) e adoção das
classes de espaço do Mesa para a rede intra-firma (T02).

## Histórico de decisões fechadas

| # | Decisão | Resolução | Data |
|---|---|---|---|
| F01 | Linguagem: anglicismos? | Sem anglicismos quando houver termo português. Siglas mantidas. | 2026-05-26 |
| F02 | Licença | CC-BY-SA 4.0 | 2026-05-26 |
| F03 | Estrutura do pacote | src/ layout, Python 3.12+ (mesa≥3.5 exige 3.12) | 2026-05-26 |
