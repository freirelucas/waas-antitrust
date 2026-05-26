"""§2 — Figura central · inversão da função-utilidade."""

import matplotlib.pyplot as plt
import numpy as np

from waas_antitrust.viz.paleta import PALETA


def gerar_figura():
    """Retorna (fig, axes) com painel duplo: utilidade clássica vs. WaaS."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))

    ax = axes[0]
    p = np.linspace(0.01, 0.5, 100)
    for compliance in [10, 20, 40, 80]:
        ax.plot(p, compliance / p, alpha=0.4, color="gray", linewidth=1)
    ax.scatter([0.05], [100], s=180, color=PALETA["A"], zorder=5, edgecolors="white", linewidth=2)
    ax.annotate(
        "Conformidade ótima:\nbaixa detecção, baixo gasto",
        xy=(0.05, 100),
        xytext=(0.20, 130),
        fontsize=10,
        ha="left",
        arrowprops=dict(arrowstyle="->", color=PALETA["A"], lw=1.5),
    )
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 250)
    ax.set_xlabel(r"Probabilidade de detecção  $p$")
    ax.set_ylabel(r"Custo esperado da sanção  $p \cdot S$")
    ax.set_title(
        "Regime A · função-utilidade clássica\nA empresa minimiza  "
        r"$\mathbb{E}[\mathrm{sanção}]$",
        fontweight="bold",
        color=PALETA["A"],
    )
    ax.fill_between([0, 0.5], 0, 50, color=PALETA["A"], alpha=0.06)
    ax.text(0.02, 25, "zona de\nimpunidade", fontsize=9, color=PALETA["A"], alpha=0.7)

    ax = axes[1]
    W = np.linspace(0, 3, 100)
    D_pct = np.linspace(0.1, 0.5, 100)
    Wg, Dg = np.meshgrid(W, D_pct)
    margem = Dg * 8 - Wg
    cs = ax.contourf(Wg, Dg, margem, levels=15, cmap="RdYlGn", alpha=0.85)
    ax.contour(Wg, Dg, margem, levels=[0], colors="black", linewidths=2, linestyles="--")
    cbar = plt.colorbar(cs, ax=ax, shrink=0.85)
    cbar.set_label(r"Margem da empresa  $D - W$  (proporcional ao bem-estar)", fontsize=9)
    ax.scatter([1.5], [0.30], s=180, color="black", zorder=5, edgecolors="white", linewidth=2)
    ax.annotate(
        "Ponto-alvo do artigo:\n$W=1{,}5\\,w_a$,  $D=30\\%\\,S$",
        xy=(1.5, 0.30),
        xytext=(0.4, 0.43),
        fontsize=10,
        ha="left",
        color="black",
        arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
    )
    ax.text(
        2.6,
        0.15,
        "IC-F*\nviolada",
        fontsize=10,
        color="darkred",
        ha="center",
        fontweight="bold",
        alpha=0.7,
    )
    ax.set_xlabel(r"Recompensa ao denunciante  $W$  ($\times\,w_a$)")
    ax.set_ylabel(r"Desconto sobre TCC  $D$  (fração de $S$)")
    ax.set_title(
        r"Regime B/C · inversão sob WaaS"
        + "\nA empresa maximiza  "
        + r"$D - W \Leftrightarrow$ casos reportados",
        fontweight="bold",
        color=PALETA["B"],
    )

    plt.suptitle(
        "Tese central · inversão da função-utilidade da conformidade",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    return fig, axes
