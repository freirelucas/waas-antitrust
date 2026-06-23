# Plano de melhorias — pós crítica x10

> **Documento histórico (jun/2026).** Esta página registra o plano de melhorias produzido após a primeira [crítica x10](critica_x10.md), anterior aos reframes v2 e v3. Itens já endereçados estão documentados nas rodadas posteriores ([brainstorm de revisão](brainstorm_revisao.md), [aprendizados v3](aprendizados_v3.md), [auditoria estrutural](auditoria_estrutural.md)). Para o backlog atual, ver [Decisões e backlog](DECISIONS.md).

Esta página prioriza as melhorias propostas pelos 8 especialistas (ver
[Crítica x10](critica_x10.md)) por **filtros do piloto automático**:

- **(a) sem necessidade de decisão normativa do autor**;
- **(b) implementação ≤ 2 h**;
- **(c) gate verde garantido** (testes, lint, mkdocs, sync `main`);
- **(d) reduz overclaim ou sobe rigor**.

## Categoria 1 — Honestidade documental (S, doc-only)

Pode ser feito agora; só altera texto e não muda comportamento do modelo.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| 1.1 | Adv B | Corrigir docstring "padrões YC" → "construção normativa proposta" | `src/waas_antitrust/hirschman.py` |
| 1.2 | Adv B | Caveat: Lei 13.608 não cobre antitruste no eixo recompensa | `docs/DECISIONS.md` (R07) |
| 1.3 | Adv B | Caveat: tributação derrete 40–50% do `valor_vesting_acelerado` | `docs/DECISIONS.md` (R07) |
| 1.4 | Mat B | Particionar R02 em R02a/R02b/R02c (limiar integrado / contraste mult.×unic. / heterogeneidade) | `docs/DECISIONS.md` |
| 1.5 | Adv A | Tom: "é, assim, re-caracterizada" → "pode ser re-caracterizada, sujeita à controvérsia" | `paper/main.tex` |
| 1.6 | Adv A | Linha "L-Jur1: fragilidade jurídica do Regime B" | `docs/limitacoes.md` |
| 1.7 | Adv B | Subseção "Limites do Regime B" (reserva de lei) | `docs/INSTITUTIONAL.md` |
| 1.8 | Adv A | Subseção "Quem é vítima?" com tipologia × Art. 86/Art. 12 | `docs/INSTITUTIONAL.md` |
| 1.9 | Adv A | Abrir D06 "análise dogmática vítima-empregado"; fechar E04 (ou explicitar pendência) | `docs/DECISIONS.md` |
| 1.10 | PM | Abrir E05 "calibrar distribuição de papéis em marketplace BR" | `docs/DECISIONS.md` |
| 1.11 | Mat B | Pressuposto de homogeneidade de Morris-Shin no ODD; marcar Prop. 2 conjectura aberta sob heterogeneidade | `docs/ODD.md` |

## Categoria 2 — Infra de robustez (S, código)

Adiciona/reescreve mecanismos sem mudar a *direção* do modelo. Reduz risco
de overclaim na cauda de seeds.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| 2.1 | Mat A | Suavização Beta-Binomial em `p_perc`: `(vp + α) / (n_viol + α + β)` com pseudo-contagens; remove singularidade em `n_viol=0` | `src/waas_antitrust/model.py` (P0); novo módulo/função pura testável |
| 2.2 | Mat A, Mat B | Helper de bootstrap multi-seed para headline-metrics; promover `test_dissuasao_endogena_*` a multi-seed com CI 95% | novo módulo `src/waas_antitrust/robustez.py`; `tests/test_model.py` |

## Categoria 3 — Bem-estar substantivo (S, código)

Fechar gaps do R05 que ficaram pendentes.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| 3.1 | Eco B | Incorporar `custo_exodo_acum` em `calcular_bem_estar` com peso `delta_exodo` (default ~0,5) | `src/waas_antitrust/sobol/execucao.py` |
| 3.2 | Eco B | Reporter `multa_arrecadada_acum` (VP sem TCC ⇒ multa cheia; com TCC ⇒ parte residual) + termo no bem-estar | `src/waas_antitrust/model.py`; `sobol/execucao.py` |
| 3.3 | Eco A, Eco B, PM | Ponderar `dano_acumulado` por `fatia_mercado` da firma violadora; expor `dano_economico_acum` | `src/waas_antitrust/model.py` (P0) |

## Categoria 4 — Gating jurídico de R07 (M, código + doc)

Este é o item **estrutural** que Adv B aponta — o modelo não pode oferecer
no Regime B uma cláusula contratual que só Regime C pode entregar.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| 4.1 | Adv B | Gating: `fracao_contratos_acelerados > 0` apenas em Regime C; em A/B força 0 com warning | `src/waas_antitrust/model.py` (`__init__`) |
| 4.2 | Adv B | Função `valor_liquido_pos_tributos` com haircut IRPF/INSS (default ~40%) antes de `custo_exodo_esperado` | `src/waas_antitrust/hirschman.py` |
| 4.3 | Adv B | Atualizar testes para refletir o gating | `tests/test_hirschman.py` |

## Categoria 5 — Catálogo BR + papéis (M, código + doc)

Expande R08 com cobertura empírica brasileira.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| 5.1 | PM | Adicionar `exclusividade_retaliacao_marketplace` ao catálogo | `src/waas_antitrust/condutas.py` |
| 5.2 | PM | Adicionar `anti_steering_iap` ao catálogo | `src/waas_antitrust/condutas.py` |
| 5.3 | PM | Acrescentar `operacoes` e `financeiro` aos `PAPEIS_PADRAO` | `src/waas_antitrust/condutas.py` |
| 5.4 | PM | Preset `MARKETPLACE_BR` em distribuições; manter `BIGTECH_MADURA` como padrão | `src/waas_antitrust/condutas.py` |
| 5.5 | PM | Gradiente 3-níveis (primário=1.0, adjacente=0.5, distal=0.1); campo `atores_adjacentes` em `Conduta` | `src/waas_antitrust/condutas.py` |

## Categoria 6 — UX visual + acessibilidade (S, viz + CSS)

Designer apontou risco real: jornalista cita figura conceitual como
resultado.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| 6.1 | Designer | Trocar `RdYlGn` por `cividis` em figuras conceituais | `src/waas_antitrust/viz/inversao.py`, `viz/fase.py` |
| 6.2 | Designer | Adicionar marcadores A=`o`, B=`s`, C=`^` e hachuras nas séries por regime | `src/waas_antitrust/viz/paleta.py` (constantes); chamadas em viz |
| 6.3 | Designer | CSS custom `.figura-conceitual` (borda cinza tracejada + chip "Ilustrativo") e `.figura-empirica` (borda verde + chip "Resultado da simulação") | `docs/stylesheets/extra.css`; `mkdocs.yml` |
| 6.4 | Designer | Regenerar `03_dissuasao_bem_estar.png` com rótulos "A"/"B" nos painéis, anotações numéricas, painel direito em escala adequada | `docs/img/03_dissuasao_bem_estar.png` (regen via script) |
| 6.5 | Designer | Aplicar classes `{ .figura-conceitual }` / `{ .figura-empirica }` em `docs/index.md` e `docs/resultados.md` | `docs/index.md`, `docs/resultados.md` |

## Categoria 7 — Decisões normativas suas (FORA do piloto automático)

Estes itens **alteram material e Proposições centrais** — entram no
backlog (DECISIONS) para conversa explícita:

- **Eco A**: endogeneizar `g_i(t) = π·R / (p·S)` como função do estado, não constante (altera Prop. 3 e R01).
- **Eco A**: implementar IC-F* completa `W + p_pago·(S−D) < p_npago·S` (altera Prop. 1).
- **Eco A**: Hirschman como elevação de `W_esperado` em vez de subtração de `g_i` (alterar microfundamento de R07).
- **Mat B**: substituir arquétipo "racional" por estratégia-limiar `s_i ≥ x*` do `jogo_global` (integra Prop. 2).
- **Mat B**: contraste numérico multiplicidade × unicidade no espírito Morris-Shin.
- **Adv A**: parâmetro `p_anulacao_tcc` na simulação (transforma F6 em falsificador).
- **Eco B**: distribuição Pareto/lognormal de `fatia_mercado` (R03 dependência empírica).
- **Designer**: promover `sankey.py` de stub a fluxograma real do mecanismo.
- **PM**: 3 condutas-piloto para o paper (marketplace_exclusividade, anti_steering, killer_acq_ia) com fixtures e testes de regressão.

Estes itens vão para `DECISIONS.md` como R09–R13 com descrição clara da
decisão pendente.

---

## Ordem de execução (piloto automático)

Cada bloco é **um commit + sync `main`**, com gates verdes (pytest, ruff,
black, mkdocs --strict, nbval do demo).

1. **Síntese**: este arquivo + `critica_x10.md` (commitado **antes** das
   melhorias para preservar a rastreabilidade).
2. **Categoria 1** (honestidade documental) — único commit.
3. **Categoria 2** (Beta-Binomial + multi-seed CI).
4. **Categoria 3** (bem-estar substantivo).
5. **Categoria 4** (gating jurídico do R07).
6. **Categoria 5** (catálogo BR + papéis).
7. **Categoria 6** (UX visual + acessibilidade).
8. Final: regenerar a figura 3 com as melhorias visuais; verificação final.

Ao final, `DECISIONS.md` ganha R09–R13 da Categoria 7 (pendências
normativas suas).

---

# v2 pós-reframe

Esta seção sintetiza as melhorias propostas pelos **10 especialistas** da
[Crítica x10 v2](critica_x10_v2.md) — 8 originais + sociólogo da coordenação
coletiva + cientista político da regulação. O reframe central deixa de ser
"empresa paga pela delação" e passa a ser **"massa crítica de cooperação
interna como bem coletivo cuja internalização é instrumental"**.

**Recategorização sob filtros adaptados ao reframe:**

- **(a') reduz overclaim conceitual** (corrige nome do reframe, decompõe
  Regime C, ata reservas constitucionais)
- **(b') destrava modelagem de uso adversarial e capacidade institucional**
- **(c') gate verde mantido** (testes, lint, mkdocs, sync `main`)
- **(d') compatível com Sprints A/B do PM** — não empilha sobre R09-R11

## Categoria v2.A — Reposicionamento conceitual (S, doc-only)

Correções de framing sem mudança de código. Pode ser feito antes de
qualquer commit de código.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| v2.A.1 | Sociólogo | Substituir "bem quase-público" por **"capital social com risco de erosão endógena"** como categoria conceitual primária; manter "bem público" como leitura secundária Samuelson | `docs/bem_publico.md` (renomear conceitualmente; arquivo mantém nome) + `docs/mecanismo.md` §macroconceito |
| v2.A.2 | Adv A | Substituir "atenuante por contribuição a bem público de detecção" por **"interesse público em detecção e cessação"** (Lei 9.784/99); citar Lei 12.846/2013 (LAC) Art. 7º VII-VIII como precedente dogmático | `docs/INSTITUTIONAL.md` (nova §) |
| v2.A.3 | Adv B | Decompor Regime C em sub-regimes **`Cₜ` trabalhista**, **`Cᵩ` tributária-LC**, **`Cₚ` penal** com tabela de hospedabilidade por instrumento | `docs/INSTITUTIONAL.md` "Os três regimes" → quatro |
| v2.A.4 | Sociólogo | Tabela de 8 *design principles* de Ostrom (1990) × reporters/parâmetros existentes: 3 atendidos (P1, P4, P5), 5 ausentes (P2, P3, P6, P7, P8) | `docs/ODD.md` §2 nova subseção "Diagnóstico Ostrom" |
| v2.A.5 | Cientista Político | Documentar **infactibilidade política Regime C** 2024-2027 (PL 2768/2022 parado; janela legislativa baixa); marcar como limitação no Ato 4 | `docs/limitacoes.md` + `docs/viabilidade_regime_c.md` (NOVO, ≤ 1 página) |
| v2.A.6 | Designer | Manter punchline jornalística do Ato 1 + sublinha cinza em itálico contendo reframe; mover `bem_publico.md` para depois do Ato 2 | `docs/index.md` (H1 + sublinha); `mkdocs.yml` (ordem nav) |

## Categoria v2.B — Modelagem de uso adversarial e oportunista (M, código)

Convergência forte (Cientista Político + Mat B + Sociólogo): arquétipo
`denunciante_oportunista` ausente é vácuo material.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| v2.B.1 | Cientista Político | Arquétipo `denunciante_oportunista` em `TrabalhadorAgent.ARQUETIPOS`: utilidade `u = recompensa - prob_falso_positivo·sancao_calunia`; parametriza insider acionista, concorrente, chantagem, hedge fund | `src/waas_antitrust/agents.py` + `tests/test_oportunista.py` |
| v2.B.2 | Sociólogo | Reporter `densidade_denuncia_frivola` (FP/total) por firma; teste de cenário com `fracao_oportunistas > 0.2` degrada IR financeira da firma | `src/waas_antitrust/model.py` |
| v2.B.3 | Mat B | Arquétipo `oportunista` (Olson explícito): sinaliza apenas se `phi < q_min - epsilon` (entra antes da massa); desiste se `phi ≥ k_req/n` | `src/waas_antitrust/agents.py` (variante de v2.B.1) |
| v2.B.4 | Sociólogo | Reporter `capital_social_residual_firma` = densidade de laços fortes (clustering × confiança survey-like) pré/pós denúncia; teste hipótese Coleman "uso instrumental erode produção" | `src/waas_antitrust/model.py` + `tests/test_capital_social.py` |

## Categoria v2.C — Instrumento como protocolo ortogonal (L, código)

Convergência Eco A + Adv B: criar `src/waas_antitrust/instrumentos.py` em
vez de apenas `bem_publico.py`. Substituição perversa (Frey-Jegen) só é
falsificável se cada instrumento expuser seu `EfeitoIC` separado.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| v2.C.1 | Eco A + Adv B | `Protocol Instrumento` com assinatura `aplicar(firma, fila, t) -> EfeitoIC` + metadados `(nome, reserva_constitucional, regime_minimo, fontes_primarias)`; refator WaaS/Hirschman como implementações | `src/waas_antitrust/instrumentos.py` (NOVO) + refator `model.py` P3 |
| v2.C.2 | Eco A | `p_pago_por_instrumento(instrumento, pos_fila_inter, n_coop_intra)` em `corrida.py` — matriz de p_pago condicionada (fecha R10) | `src/waas_antitrust/corrida.py` |
| v2.C.3 | Eco A | Cenário `apenas_massa_critica_observavel` em `cenarios.py`: regulador observa só `massa_critica_atingida` (sem qual instrumento); falsificador F7 — sinal Schelling sobrevive à invisibilidade do instrumento? | `src/waas_antitrust/cenarios.py` |

## Categoria v2.D — Bem-estar com externalidade explícita (M, código)

Convergência Eco A + Eco B + Sociólogo: bem-estar atual é contabilidade de
custos privatizados; falta termo de externalidade erga omnes.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| v2.D.1 | Eco B | `valor_dissuasao_difusa_acum = Σ (p_perc_t − p_perc_0) · n_empresas_não_violadoras · overcharge_evitavel` calibrado em Connor-Lande 17-19%; usar somente firmas que **jamais** foram notificadas (evita double-counting) | `src/waas_antitrust/model.py` (reporter) + `sobol/execucao.py` (peso opt-in) |
| v2.D.2 | Eco B | Renormalizar pesos β, γ por `dano_evitavel_total_potencial` (fração [0,1] em vez de R$/w_a) — permite comparação justa entre instrumentos | `sobol/execucao.py` |
| v2.D.3 | Eco B | Proposição 4 candidata: WaaS Pareto-domina TCC clássico sse `valor_dissuasao_difusa > β·FP + δ_exodo·êxodo` no equilíbrio | `docs/ODD.md` |

## Categoria v2.E — Topologia e grafo inter-firma (M, código)

Convergência Mat B + Eco B + Cientista Político: `p_perc` escalar atual é
campo Schelling-médio insuficiente; mercados digitais têm aprendizado
inter-firma estruturado.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| v2.E.1 | Mat B | Trocar `0,30` hardcoded por `theta_imitativo ~ Beta(α, β)` no `TrabalhadorAgent`; expor `theta_imitativo_media/desvio` em `WaaSParametros` | `src/waas_antitrust/agents.py` |
| v2.E.2 | Mat B | Parametrizar `topologia_intra ∈ {watts_strogatz, caverna, estrela, regular, random}`; varredura comparativa em scripts/run_sobol_full.py | `src/waas_antitrust/model.py` + `scripts/` |
| v2.E.3 | Mat B + Eco B + Cient. Pol. | Substituir `p_perc` escalar por `nx.Graph` inter-firma (rotatividade de pessoal + escritórios jurídicos); `p_perc_i = média de vizinhos no grafo` | `src/waas_antitrust/model.py` (L, opt-in) |
| v2.E.4 | Mat B | Teste de regressão: cascata morre em topologia regular (sem atalhos) e sobrevive em pequeno-mundo | `tests/test_contagio_complexo.py` (NOVO) |

## Categoria v2.F — Capacidade institucional CADE como gargalo (M, modelo)

Convergência Cientista Político + PM: WaaS pulveriza o gatilho mas concentra
captura no processamento. Sem expansão de quadro, seleção discricionária
vira ponto ótimo de captura.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| v2.F.1 | Cient. Político | Cenário `captura_processamento`: `p_inv = min(1, capacidade_servidores / (notificacoes · custo_caso))`; calibrar `capacidade_servidores = 180` (RIG 2024 área-fim) | `src/waas_antitrust/model.py` + `calibracao/cade_rig.py` |
| v2.F.2 | Eco B | Cenário-teste de **não-rivalidade** como falsificador: varrer `capacidade_tique ∈ {0.5×, 1×, 2×}`; se duplicar capacidade NÃO duplica dano evitado, há rivalidade parcial por gargalo | `tests/test_externalidade.py` (NOVO) |
| v2.F.3 | Cient. Político | Cenário `jurisdicao_concorrente` (CADE × MPF × MPT × CGU): cada autoridade com `prob_acolhida` e `custo_captura` distintos; denunciante escolhe por max utility | `src/waas_antitrust/jurisdicao.py` (NOVO) + `cenarios.py` |

## Categoria v2.G — Mat A: unicidade temporal + heterogeneidade Saito (S, doc + S, código)

Crítica isolada mas técnica e direta — não convergiu mas é fundacional para
a Proposição 2 sob reframe.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| v2.G.1 | Mat A | Generalizar `limiar_switching` para aceitar vetor `b_k = f_W(k) · b`; devolve limiar por posição $x^\star_k$ — explicita que o bem coletivo tem oferta escalonada | `src/waas_antitrust/jogo_global.py` |
| v2.G.2 | Mat A | Proposição auxiliar 2': condições suficientes (independência inter-firma; ausência de sinal público sobre fila) para que $\{x^\star(t)\}$ permaneça único em cada instante; citar Frankel-Morris-Pauzner (2003) e Angeletos-Hellwig-Pavan (2007) | `docs/ODD.md` §Prop. 2 |
| v2.G.3 | Mat A | Documentar tensão Olson vs Morris-Shin (em Olson o tamanho do grupo é hostil; em Morris-Shin o limiar é exógeno); citar Chwe 2000 *common knowledge in coordination* | `docs/ODD.md` §2 |

## Categoria v2.H — Visualização e UX (S, viz + CSS)

Designer aprofunda v1: punchline + reframe devem coexistir; chip-instrumento
reutilizável.

| # | Origem | Ação | Arquivo-alvo |
|---|---|---|---|
| v2.H.1 | Designer | Sublinha de reframe em itálico cinza (HTML `<p class="sublinha-tese">`) abaixo do H1 do Ato 1 | `docs/index.md` linhas 3-4 + `docs/stylesheets/extra.css` |
| v2.H.2 | Designer | Componente `chip-instrumento` (CSS) com paleta consistente: WaaS (cor primária), os outros 3 (cinza-azulado); contraste AA + texto alternativo | `docs/stylesheets/extra.css` |
| v2.H.3 | Designer | Sumário visual de 4 instrumentos (grid 2×2) em `bem_publico.md` topo, com cada célula linkando para onde o instrumento aparece | `docs/bem_publico.md` |
| v2.H.4 | Designer | Caption de `03_dissuasao_bem_estar.png` ganha leitura tripla: (a) eixo; (b) o reframe lê assim; (c) por que outros 3 instrumentos não aparecem | `docs/index.md` linha 13 + `docs/resultados.md` |

## Categoria v2.I — Pendências normativas que o reframe NÃO resolve (FORA do piloto)

Empilhar reframe sobre R09-R11 abertos é frágil. Itens que **alteram
material** as Proposições e exigem decisão sua antes da execução:

- **R09 (Eco A v1, reforçado pelo Eco A v2)**: endogeneizar `g_i(t) = π·R/(p·S)`; sob reframe, `p` é externalidade endógena (Sah-Stiglitz 1986 *spillover*).
- **R10 (Eco A v1, agravado pelo Eco A v2 + Mat A v2)**: IC-F\* completa não é só `W + p_pago·(S−D) < p_npago·S` — é **matriz** com `p_pago = f(instrumento, posicao_fila, n_coop)`.
- **R11 (Eco A v1)**: Hirschman como elevação de `W_esperado` em vez de subtração de `g_i` — alinhar com Protocol Instrumento (Eco A v2).

**Recomendação do PM**: fechar R09, R10 ou R11 (escolher 1) antes de
iniciar Sprint A do reframe.

## Sequenciamento sugerido (Sprints A/B do PM)

O PM v2 contesta o sequenciamento ambicioso de 8 commits em 2-3 semanas e
propõe particionar em **dois sprints**:

### Sprint A (~ 1 semana equivalente) — Reposicionamento + MVP de código

1. **Commit 1**: Crítica x10 v2 + plano_melhorias v2 (este arquivo).
2. **Commit 2**: Categoria v2.A.1-A.6 (reposicionamento conceitual; doc-only).
3. **Commit 3**: Categoria v2.G.1-G.3 + v2.B.1 (Mat A + arquétipo oportunista, código mínimo).
4. **Commit 4**: Categoria v2.H.1-H.4 (UX visual + chip-instrumento).

### Sprint B (~ 2 semanas equivalente) — Instrumentos ortogonais + Externalidade

5. **Commit 5**: Categoria v2.C.1-C.3 (Protocol Instrumento; refator P3).
6. **Commit 6**: Categoria v2.D.1-D.3 + v2.B.2-B.4 (externalidade no bem-estar; oportunismo completo).
7. **Commit 7**: Categoria v2.E.1-E.4 (topologia variável + grafo inter-firma opt-in).
8. **Commit 8**: Categoria v2.F.1-F.3 (capacidade CADE + jurisdição concorrente).

Cada commit: gates verdes + sync `main` 4-way (`HEAD = claude/branch =
origin/branch = main local = origin/main`).

**Fora deste ciclo (Fase 4)**: refator estrutural completo (FirmaIncentivoDecision class); paper main.tex (título + abstract + §5); 12 personas na x10 v3 (Behavioral ethicist + econometrista aplicado).

