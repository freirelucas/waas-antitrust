"""§11 — Comparação 3 jurisdições (BR × EUA-DOJ-ATR × UE-DMA).

Materializa o R28: as três jurisdições como variantes paramétricas do
mesmo agente-modelo, comparadas em multi-seed. Cenários (`cenarios.py`):

- **BR (status quo)**: `status_quo` — Regime A, sem canal de incentivo.
- **EUA**: `eua_doj_atr_rewards_2025` — Regime C + `prob_pagamento_perc=0.225`
  (média da faixa 15-30% do DOJ-ATR) + LCMC ativa.
- **UE**: `ue_dma_whistleblower_tool_2024` — Regime A + proteção horizontal
  (Diretiva 2019/1937) sem recompensa.

Painel 1×2: (A) trajetória mediana de `dano_acumulado` por jurisdição
(banda = IC bootstrap 95% por tique); (B) barras do dano final.

Caveat herdado de `docs/internacional.md`: `taxa_capacidade` NÃO está
calibrada contra DOJ-ATR/DG-COMP — comparações são DIRECIONAIS, não de
volume absoluto.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.cenarios import aplicar_cenario
from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.robustez import bootstrap_ci
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

DEFAULT_SEEDS: tuple[int, ...] = (11, 23, 37, 41, 53, 59, 71, 83)

#: Jurisdições comparadas: (rótulo, nome do cenário, cor da paleta).
JURISDICOES: tuple[tuple[str, str, str], ...] = (
    ("BR status quo", "status_quo", "A"),
    ("EUA DOJ-ATR 2025", "eua_doj_atr_rewards_2025", "C"),
    ("UE DMA Tool 2024", "ue_dma_whistleblower_tool_2024", "B"),
)


def gerar_figura(
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    n_tiques: int = 24,
) -> tuple[Figure, list[Axes]]:
    """Painel 1×2 da comparação 3 jurisdições, multi-seed.

    Parameters
    ----------
    seeds : tuple[int, ...]
        Sementes para o multi-seed (default 8).
    n_tiques : int
        Horizonte (default 24 — 6 anos em trimestres).

    Returns
    -------
    (Figure, [Axes, Axes])
    """
    aplicar_estilo()
    base = WaaSParametros(
        n_empresas=15,
        tam_medio_empresa=150,
        n_tiques=n_tiques,
        fracao_violadoras=0.5,
        taxa_observacao=0.4,
    )

    trajetorias: dict[str, np.ndarray] = {}
    finais: dict[str, list[float]] = {}
    for rotulo, cenario, _ in JURISDICOES:
        curvas = []
        for seed in seeds:
            from dataclasses import replace

            params = aplicar_cenario(replace(base, seed=seed), cenario)
            df = WaaSModel(params).executar()
            curvas.append(df["dano_acumulado"].to_numpy(dtype=float))
        matriz = np.vstack(curvas)  # (n_seeds, n_tiques)
        trajetorias[rotulo] = matriz
        finais[rotulo] = matriz[:, -1].tolist()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ax_a, ax_b = axes[0], axes[1]

    # Painel A: trajetórias medianas com banda interquartílica
    tempo = np.arange(1, n_tiques + 1)
    for rotulo, _, cor_key in JURISDICOES:
        matriz = trajetorias[rotulo]
        mediana = np.median(matriz, axis=0)
        q25 = np.quantile(matriz, 0.25, axis=0)
        q75 = np.quantile(matriz, 0.75, axis=0)
        ax_a.plot(tempo, mediana, label=rotulo, color=PALETA[cor_key])
        ax_a.fill_between(tempo, q25, q75, color=PALETA[cor_key], alpha=0.15)
    ax_a.set_xlabel("Tique (trimestre)")
    ax_a.set_ylabel("Dano acumulado")
    ax_a.set_title("(A) Trajetória mediana (banda interquartílica)")
    ax_a.legend(fontsize=8)
    ax_a.grid(True, alpha=0.3)

    # Painel B: dano final com IC bootstrap
    posicoes = range(len(JURISDICOES))
    medianas = []
    erros_inf = []
    erros_sup = []
    cores = []
    rotulos = []
    for i, (rotulo, _, cor_key) in enumerate(JURISDICOES):
        ic = bootstrap_ci(finais[rotulo], n_bootstrap=2000, seed=i)
        medianas.append(ic.mediana)
        erros_inf.append(ic.mediana - ic.inferior)
        erros_sup.append(ic.superior - ic.mediana)
        cores.append(PALETA[cor_key])
        rotulos.append(rotulo.replace(" ", "\n", 1))
    ax_b.bar(
        posicoes,
        medianas,
        yerr=[erros_inf, erros_sup],
        color=cores,
        alpha=0.85,
        capsize=6,
        edgecolor="black",
        linewidth=0.5,
    )
    ax_b.set_xticks(list(posicoes))
    ax_b.set_xticklabels(rotulos, fontsize=8)
    ax_b.set_ylabel("Dano acumulado (final)")
    ax_b.set_title("(B) Dano final + IC bootstrap 95%")
    ax_b.grid(True, axis="y", alpha=0.3)

    fig.suptitle(
        f"Comparação direcional 3 jurisdições — {len(seeds)} seeds × {n_tiques} tiques "
        "(capacidade institucional NÃO calibrada; ver caveats em internacional.md)",
        fontsize=9,
    )
    fig.tight_layout()
    return fig, [ax_a, ax_b]


if __name__ == "__main__":
    from pathlib import Path

    fig, _ = gerar_figura()
    out = Path("docs/img/13_internacional_3jurisdicoes.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
