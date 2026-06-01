# Plano de melhorias — pós crítica x10

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
