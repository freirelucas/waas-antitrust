# Tela para brincar com o modelo

Painel interativo. Mude sliders e *checkboxes*, aperte **Rodar simulação**,
veja o efeito em quatro gráficos. Cada rodada é uma execução completa do
`WaaSModel` — não animação pré-renderizada — e demora menos de 30 segundos
em ambiente normal.

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_brincar.ipynb)

## O que você pode mexer

| Controle | O que muda no modelo | Faixa | Sugestão para começar |
|---|---|---|---|
| **Regime** | Configuração institucional: A status quo · B Resolução CADE · C lei nova · EUA DOJ-ATR · UE DMA Tool | A, B, C, EUA, UE | Comece em B vs A |
| **Número de empresas** | Tamanho do sistema simulado | 4–40 | 10 |
| **Trabalhadores por empresa** | Tamanho de cada firma | 30–400 | 120 |
| **Horizonte** | Quantos trimestres simular | 8–60 | 20 |
| **Fração violadoras** | Quantas empresas começam violando | 10%–90% | 50% |
| **Taxa de observação** | Probabilidade do trabalhador ver a conduta | 5%–80% | 45% |
| **W_mult** | Recompensa em múltiplos do salário anual | 0–4 | 1,5 |
| **k_rel** | Fração mínima de cooperadores para massa crítica | 1%–25% | 5% |
| **alpha_erosão** | Risco de erosão Coleman do substrato cooperativo | 0–0,9 | 0 (sem erosão) |
| **usar_escrow_explicito** | Liga o canal R27 (`AutoridadeAgent.escrow_denuncias`) | on/off | off para começar |
| **janela_escrow_tiques** | Δt antes do depósito expirar (0 = eterno) | 0–12 | 0 |
| **Seed** | Semente do gerador aleatório | 1–999 | 11 |

## O que sai

Painel 2×2 com a comparação **Regime escolhido vs Regime A** (referência) na
mesma seed:

- **(A) Dano acumulado** — quanto dano social acumulado ao longo do horizonte.
- **(B) Violadoras ativas** — quantas empresas ainda violam por tique
  (dissuasão R01).
- **(C) Sinais por tique** — quantos trabalhadores sinalizam em cada
  trimestre.
- **(D) Capital social residual** — substrato cooperativo (R26 Coleman).

Abaixo, um resumo numérico do último tique (dano total, sinais somados,
TCCs assinados; se `usar_escrow_explicito = on`, também `n_denuncias_em_escrow`
e `n_aberturas_simultaneas_acum`).

## 5 experimentos sugeridos

Cada um demora menos de 30 segundos depois do setup inicial:

1. **Comparar Regime A vs B**. Deixe o slider padrão, troque o regime entre
   A e B. Dano em A cresce linear; em B achata. Esta é a Proposição 3 do
   projeto vista em uma execução.
2. **Forçar a Proposição 5 forte**. Coloque `alpha_erosão = 0.9` em
   Regime B. O dano deveria ainda ficar abaixo de A (o achado de jun/2026
   diz que sim). Se romper, o achado caiu — reabra
   [`limitacoes.md`](limitacoes.md).
3. **Ver o canal funcionando isoladamente**. Regime B, `W_mult = 0`,
   `usar_escrow_explicito = on`, `alpha = 0`. Os depósitos vêm dos
   arquétipos éticos e cascateiam por imitação — sem nenhum incentivo
   monetário. É a demonstração que LCMC é **mecanismo de coordenação,
   não de pagamento**.
4. **Comparar BR vs EUA vs UE**. Mesma seed, alterne o regime entre B, EUA,
   UE. UE replica A (sem recompensa, só proteção horizontal Diretiva
   2019/1937); EUA replica C (recompensa estatutária Dodd-Frank §922).
5. **Achar massa crítica inalcançável**. Regime B, `k_rel = 0.25`,
   `N empresas = 4`, `usar_escrow_explicito = on`. Nenhuma firma atinge
   o gatilho. Reduza `k_rel` para 0.05 e veja o sistema ganhar vida.

## Limites deste painel

Este caderno é **didático**. Os achados científicos do projeto vêm de
varreduras multi-seed (10+ sementes, bootstrap CI 95%), não de execução
única. Para reproduzir os achados oficiais sem brincar:

```bash
# Falsificação da Prop. 5 forte
python scripts/varredura_alpha_erosao.py

# Calibração formal R03
python scripts/calibrar_formal.py

# Identificabilidade dos alvos
python scripts/identificabilidade_r03.py

# Todas as 19 figuras do site
python scripts/regerar_todas_as_figuras.py
```

Cada um produz `.parquet` ou `.json` em `results/` e PNG em `docs/img/`.

## Em ambiente local

Se preferir não usar Colab, instale localmente em três comandos:

```bash
git clone https://github.com/freirelucas/waas-antitrust.git
cd waas-antitrust && pip install -e ".[dev]" && pip install ipywidgets
jupyter notebook notebooks/WaaS_brincar.ipynb
```

`ipywidgets` é dependência só do caderno brincar — não está em
`pyproject.toml` para não onerar a instalação base.
