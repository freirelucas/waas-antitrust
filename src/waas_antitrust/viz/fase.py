"""§3 — Diagrama de fase · jogo global Morris-Shin."""

import matplotlib.pyplot as plt
import numpy as np

from waas_antitrust.viz.paleta import PALETA


def gerar_figura():
    fig, ax = plt.subplots(figsize=(9, 6.5))
    sigma_grid = np.linspace(0, 1, 80)
    k_grid = np.linspace(0.01, 0.30, 80)
    Sig, K = np.meshgrid(sigma_grid, k_grid)
    q = 0.05 + 0.6 * Sig
    p_sinaliza = 1.0 / (1.0 + np.exp(-7 * (Sig - 0.4)))
    P_cascata = 1.0 / (1.0 + np.exp(-30 * (q * p_sinaliza - K)))

    cs = ax.contourf(Sig, K, P_cascata, levels=20, cmap="RdYlGn", alpha=0.92)
    plt.colorbar(cs, ax=ax, shrink=0.85, label=r"$P(\mathrm{cascata}) = P(\sum a_i \geq k)$")
    ax.contour(Sig, K, P_cascata, levels=[0.5], colors="black", linewidths=2.5)

    ax.text(
        0.15,
        0.05,
        r"silêncio" + "\n" + r"$P\to 0$",
        fontsize=12,
        color="darkred",
        ha="center",
        fontweight="bold",
        alpha=0.85,
    )
    ax.text(
        0.80,
        0.06,
        r"cascata garantida" + "\n" + r"$P\to 1$",
        fontsize=12,
        color="darkgreen",
        ha="center",
        fontweight="bold",
    )
    ax.scatter(
        [0.6],
        [0.05],
        s=180,
        marker="*",
        color=PALETA["B"],
        edgecolors="white",
        linewidths=2,
        zorder=10,
        label="Regime B · alvo",
    )
    ax.scatter(
        [0.7],
        [0.10],
        s=180,
        marker="*",
        color=PALETA["C"],
        edgecolors="white",
        linewidths=2,
        zorder=10,
        label="Regime C · alvo",
    )
    ax.set_xlabel(r"Severidade da violação  $\sigma$")
    ax.set_ylabel(r"Massa crítica relativa  $k / n$")
    ax.set_title("Coordenação como jogo global · seleção Morris-Shin (1998)", fontweight="bold")
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.01, 0.30)
    plt.tight_layout()
    return fig, ax
