# Brincar com o modelo (simulador in-browser)

Esta página é um **simulador interativo do modelo LCMC** que roda inteiramente
no seu navegador, sem servidor, sem download. Ajuste os parâmetros nos sliders
abaixo; a simulação re-roda em <300 ms e os quatro gráficos atualizam ao vivo.
A comparação é sempre **Regime A (status quo) vs o regime escolhido** na mesma
*seed* — para o leitor enxergar a diferença causal.

> **O que este simulador é.** Uma versão JavaScript reduzida das fases P1–P4 do
> `WaaSModel` Python, fiel à mecânica do canal (R27), à janela de adesão R29 e
> ao gatilho de massa crítica. Roda em <1 s mesmo em 40 firmas × 200 trabalhadores.
>
> **O que ele não é.** O modelo cheio. A produção dos achados científicos —
> bootstrap multi-seed, calibração formal R03, varredura Sobol — só sai do
> Python. Para isso, clone o repositório e use os scripts (instruções abaixo).

<div id="sim-controles" class="sim-painel">

<div class="sim-grid">

<div class="sim-grupo">
<strong>Configuração institucional</strong>
<label>Regime
<select id="sim-regime">
<option value="A">A — status quo</option>
<option value="B" selected>B — Resolução CADE (de lege lata)</option>
<option value="C">C — Lei ordinária federal (de lege ferenda)</option>
<option value="EUA">EUA — DOJ-ATR Rewards 2025</option>
<option value="UE">UE — DMA Whistleblower Tool 2024</option>
</select></label>
<label>Canal LCMC explícito (R27)
<input type="checkbox" id="sim-escrow" checked></label>
</div>

<div class="sim-grupo">
<strong>Tamanho do sistema</strong>
<label>Número de firmas: <span id="sim-n-empresas-val">10</span>
<input id="sim-n-empresas" type="range" min="4" max="40" step="1" value="10"></label>
<label>Trabalhadores por firma: <span id="sim-tam-empresa-val">80</span>
<input id="sim-tam-empresa" type="range" min="20" max="240" step="10" value="80"></label>
<label>Horizonte (tiques): <span id="sim-n-tiques-val">24</span>
<input id="sim-n-tiques" type="range" min="8" max="60" step="1" value="24"></label>
</div>

<div class="sim-grupo">
<strong>Composição micro</strong>
<label>Fração violadoras: <span id="sim-fracao-violadoras-val">0.5</span>
<input id="sim-fracao-violadoras" type="range" min="0.05" max="0.9" step="0.05" value="0.5"></label>
<label>Taxa de observação: <span id="sim-taxa-observacao-val">0.45</span>
<input id="sim-taxa-observacao" type="range" min="0.05" max="0.8" step="0.05" value="0.45"></label>
<label>Custo de represália r: <span id="sim-r-represalia-val">0.5</span>
<input id="sim-r-represalia" type="range" min="0" max="1" step="0.05" value="0.5"></label>
</div>

<div class="sim-grupo">
<strong>Instrumento WaaS (R20/R29)</strong>
<label>Recompensa W_mult: <span id="sim-w-mult-val">1.5</span>
<input id="sim-w-mult" type="range" min="0" max="4" step="0.1" value="1.5"></label>
<label>k_rel (massa crítica clássica): <span id="sim-k-rel-val">0.05</span>
<input id="sim-k-rel" type="range" min="0.01" max="0.25" step="0.01" value="0.05"></label>
<label>q_min (massa crítica do canal): <span id="sim-q-min-val">0.1</span>
<input id="sim-q-min" type="range" min="0.01" max="0.3" step="0.01" value="0.1"></label>
</div>

<div class="sim-grupo">
<strong>Janelas (Δt)</strong>
<label>Janela de expiração escrow (R27-ii): <span id="sim-janela-escrow-val">0</span>
<input id="sim-janela-escrow" type="range" min="0" max="12" step="1" value="0"></label>
<label>Janela de adesão pós-abertura (R29): <span id="sim-janela-adesao-val">10</span>
<input id="sim-janela-adesao" type="range" min="0" max="20" step="1" value="10"></label>
</div>

<div class="sim-grupo">
<strong>Adversariais</strong>
<label>Erosão Coleman alpha (R26): <span id="sim-alpha-erosao-val">0</span>
<input id="sim-alpha-erosao" type="range" min="0" max="0.9" step="0.05" value="0"></label>
<label>Semente RNG: <span id="sim-seed-val">11</span>
<input id="sim-seed" type="range" min="1" max="999" step="1" value="11"></label>
</div>

</div>

<div class="sim-acoes">
<button id="sim-rodar" type="button">▶ Rodar comparativo (A vs regime escolhido)</button>
<span id="sim-tempo">aguardando…</span>
</div>

<div class="sim-graficos">
<canvas id="sim-canvas-dano" width="600" height="260"></canvas>
<canvas id="sim-canvas-violadoras" width="600" height="260"></canvas>
<canvas id="sim-canvas-canal" width="600" height="260"></canvas>
<canvas id="sim-canvas-capital" width="600" height="260"></canvas>
</div>

<div class="sim-kpis">
<div class="sim-kpi"><strong>Dano acum. (A)</strong><span id="sim-kpi-dano-A">—</span></div>
<div class="sim-kpi"><strong>Dano acum. (tratamento)</strong><span id="sim-kpi-dano-T">—</span></div>
<div class="sim-kpi"><strong>ΔW (redução de dano)</strong><span id="sim-kpi-delta">—</span></div>
<div class="sim-kpi"><strong>Aderentes R29</strong><span id="sim-kpi-aderentes">—</span></div>
<div class="sim-kpi"><strong>Blocos abertos</strong><span id="sim-kpi-blocos">—</span></div>
<div class="sim-kpi"><strong>TCCs assinados</strong><span id="sim-kpi-tccs">—</span></div>
</div>

</div>

## O que cada controle muda

| Controle | Efeito mecânico | Onde no código Python |
|---|---|---|
| **Regime** | Liga (B/C/EUA) ou desliga (A) a recompensa W e o canal. Tag em `params.regime`. | `WaaSParametros.regime` |
| **Canal LCMC (R27)** | Liga `AutoridadeAgent.escrow_denuncias` explícito; depósitos não-abertos ficam selados até massa crítica. | `usar_escrow_explicito` |
| **Janela de adesão R29** | Habilita a cascata pós-abertura: trabalhadores da firma aberta aderem por ordem para desconto decrescente (100/70/50/30/10%). | `janela_adesao_pos_abertura` |
| **Janela de expiração escrow (R27-ii)** | Tempo máximo (em tiques) que um depósito individual fica selado antes de expirar. 0 = escrow eterno (Callisto). | `janela_escrow_tiques` |
| **q_min** | Fração mínima de depositantes na firma para o gatilho de abertura simultânea. | `q_min_cooperacao_interna` |
| **alpha_erosao (R26)** | Cada notificação corrói o substrato cooperativo (Coleman 1990; Titmuss 1970). | `alpha_erosao` |

## Cinco experimentos sugeridos

Cada um exige um único ajuste em relação ao default e fica pronto em <1 s no
seu navegador.

1. **Compare Regime A vs B com canal explícito.** Default já basta — alterne
   a opção *Regime* entre A e B. O dano acumulado em A cresce linearmente; em
   B achata depois que o canal abre o primeiro bloco. É a Proposição 3 do
   projeto vista em uma execução.
2. **Force a cascata R29.** Suba *Janela de adesão pós-abertura* para 20 e
   *Recompensa W_mult* para 3,0. Após a primeira abertura, o painel (C) mostra
   a curva *Aderentes* subir em degraus — cada degrau é um tique novo onde
   trabalhadores da firma aberta vão entrando na fila de desconto.
3. **Falsifique a Prop. 5 forte.** Mantenha Regime B, suba *alpha_erosao* para
   0,9. O capital social residual no painel (D) cai vertiginosamente, mas o
   dano em B ainda fica abaixo de A — é o achado de jun/2026: a forma forte
   foi **refutada empiricamente** (a forma fraca sobrevive).
4. **Canal sem dinheiro.** Regime B, *W_mult=0*, *Erosão=0*, *Janela de adesão
   R29=10*. Os depósitos vêm exclusivamente dos arquétipos éticos e
   cascateiam por imitação — sem nenhum incentivo monetário. É a demonstração
   visual de que LCMC é **mecanismo de coordenação, não de pagamento**.
5. **Compare BR vs EUA vs UE.** Mesma seed, alterne o *Regime* entre B, EUA e
   UE. UE replica A no comportamento agregado (proteção horizontal Diretiva
   2019/1937 sem recompensa); EUA aproxima C (Dodd-Frank §922 reproduzido por
   ato administrativo DOJ-ATR em 2025).

## Quero o modelo cheio

Este simulador é uma **lupa didática**. Os achados científicos do projeto
vêm do modelo Python completo com bootstrap multi-seed. Para reproduzir:

```bash
git clone https://github.com/freirelucas/waas-antitrust.git
cd waas-antitrust && pip install -e ".[dev]"

# Falsificação da Prop. 5 forte (10 sementes × 8 alphas)
python scripts/varredura_alpha_erosao.py

# Calibração formal R03 (Nelder-Mead, 5 sementes)
python scripts/calibrar_formal.py

# Todas as 23 figuras do site
python scripts/regerar_todas_as_figuras.py
```

Cada um produz `.parquet` ou `.json` em `results/` e PNG em `docs/img/`. O
`pytest` cobre 354 casos verdes em ~38 s; o `ruff`/`black` rodam em <2 s
cada.

[**▶ Mecanismo →**](mecanismo.md) · [**▶ Resultados →**](resultados.md) ·
[**▶ Limitações →**](limitacoes.md)
