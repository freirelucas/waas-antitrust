"""§R30 — Sinergia entre autoridades internacionais (LCMC global).

Compara ΔW (redução de dano agregado) sob três regimes:

1. **Sem LCMC global** (Regime A — status quo internacional)
2. **LCMC descoordenada** (cada autoridade roda LCMC localmente, sem MoU
   bilateral nem ICN coordenação)
3. **LCMC coordenada** (grupos econômicos consolidam depósitos + sinal
   Schelling amplificado erga omnes)

A figura é a evidência visual da hipótese central da R30: a sinergia
entre autoridades produz **dissuasão superlinear** comparada à soma das
adoções isoladas.

Estrutura em dois painéis:

(A) Trajetória de violadoras ativas ao longo dos tiques — 3 curvas que
    mostram o gap qualitativo entre coordenação vs descoordenação.

(B) Bem-estar agregado acumulado — barras finais ΔW(A→D→C) mostrando o
    "ganho da coordenação" como segundo degrau além do ganho da LCMC
    local.

Sob padrões internacionais reais (ICN MoU 2001; CADE-DOJ-ATR 2019;
DG-COMP comunicado conjunto 2024 sobre DMA), o efeito esperado é
positivo mas dependente de q_min e topologia de grupos.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.cenarios import aplicar_cenario
from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def _rodar(cenario: str | None, seed: int, n_tiques: int) -> tuple[list[int], list[float]]:
    """Executa um cenário e devolve séries (violadoras_ativas, dano_acumulado)."""
    base = WaaSParametros(
        n_empresas=6,
        tam_medio_empresa=60,
        n_tiques=n_tiques,
        seed=seed,
    )
    if cenario:
        base = aplicar_cenario(base, cenario)
    m = WaaSModel(base)
    df = m.executar()
    return (
        df["n_violadoras_ativas"].tolist(),
        df["dano_acumulado"].tolist(),
    )


def gerar_figura(
    seed: int = 2026,
    n_tiques: int = 30,
) -> tuple[Figure, tuple[Axes, Axes]]:
    """Sinergia entre autoridades internacionais — figura em 2 painéis.

    Parameters
    ----------
    seed : int
        Semente comum às três trajetórias (comparação na mesma realização).
    n_tiques : int
        Horizonte temporal.

    Returns
    -------
    (Figure, (Axes_A, Axes_B))
        Padrão `gerar_figura()` para inclusão no paper/site.
    """
    aplicar_estilo()
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13, 5))

    # Status quo (sem LCMC)
    viol_sq, dano_sq = _rodar(None, seed, n_tiques)
    # LCMC descoordenada
    viol_desc, dano_desc = _rodar("lcmc_global_descoordenada", seed, n_tiques)
    # LCMC coordenada
    viol_coord, dano_coord = _rodar("lcmc_global_coordenada", seed, n_tiques)

    tiques = np.arange(len(viol_sq))

    # -------- (A) Violadoras ativas --------
    ax_a.plot(
        tiques,
        viol_sq,
        color=PALETA["A"],
        lw=2.0,
        marker="o",
        markevery=max(1, len(tiques) // 8),
        markersize=5,
        label="Status quo (sem LCMC)",
    )
    ax_a.plot(
        tiques,
        viol_desc,
        color=PALETA["cade"],
        lw=2.0,
        marker="s",
        markevery=max(1, len(tiques) // 8),
        markersize=5,
        label="LCMC descoordenada",
    )
    ax_a.plot(
        tiques,
        viol_coord,
        color=PALETA["B"],
        lw=2.6,
        marker="^",
        markevery=max(1, len(tiques) // 8),
        markersize=6,
        label="LCMC global coordenada",
    )
    ax_a.set_xlabel("Tique (trimestres)")
    ax_a.set_ylabel("Firmas violadoras ativas")
    ax_a.set_title(
        "(A) Trajetória de violadoras ativas\n"
        "6 firmas em 2 grupos multinacionais (3+3 jurisdições)",
        fontsize=11,
        loc="left",
    )
    ax_a.legend(loc="upper right", frameon=False, fontsize=9)
    ax_a.spines[["top", "right"]].set_visible(False)
    ax_a.grid(alpha=0.3, linestyle=":")

    # -------- (B) ΔW acumulado (dano evitado) --------
    final_sq = dano_sq[-1]
    final_desc = dano_desc[-1]
    final_coord = dano_coord[-1]
    delta_desc = max(0, final_sq - final_desc)
    delta_coord = max(0, final_sq - final_coord)
    sinergia = delta_coord - delta_desc

    barras_x = [0, 1, 2]
    barras_h = [0, delta_desc, delta_coord]
    cores = [PALETA["A"], PALETA["cade"], PALETA["B"]]
    rotulos = ["Status quo", "LCMC desc.", "LCMC coord."]
    ax_b.bar(
        barras_x,
        barras_h,
        color=cores,
        edgecolor=PALETA["neutro_escuro"],
        linewidth=0.8,
    )
    for x, h in zip(barras_x, barras_h, strict=True):
        if h > 0:
            ax_b.text(
                x,
                h + max(barras_h) * 0.02,
                f"{h:.1f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

    # Marca a "altura da sinergia" como segmento sobre a barra coordenada.
    if delta_coord > delta_desc:
        ax_b.annotate(
            "",
            xy=(2.32, delta_coord),
            xytext=(2.32, delta_desc),
            arrowprops=dict(arrowstyle="<->", color="#C0392B", lw=2),
        )
        ax_b.text(
            2.4,
            (delta_coord + delta_desc) / 2,
            f"sinergia\nΔ = {sinergia:.1f}",
            fontsize=10,
            color="#C0392B",
            va="center",
            ha="left",
            fontweight="bold",
        )
    ax_b.set_xticks(barras_x)
    ax_b.set_xticklabels(rotulos)
    ax_b.set_ylabel("Dano evitado vs status quo (acum.)")
    ax_b.set_title(
        "(B) Ganho da coordenação como segundo degrau\n"
        "ΔW(coord) − ΔW(desc) mede o efeito sinergia",
        fontsize=11,
        loc="left",
    )
    ax_b.set_xlim(-0.5, 3.0)
    if max(barras_h) > 0:
        ax_b.set_ylim(0, max(barras_h) * 1.25)
    ax_b.spines[["top", "right"]].set_visible(False)
    ax_b.grid(axis="y", alpha=0.3, linestyle=":")

    fig.suptitle(
        "R30 — Sinergia entre autoridades internacionais sob LCMC global",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    fig.tight_layout()
    return fig, (ax_a, ax_b)
