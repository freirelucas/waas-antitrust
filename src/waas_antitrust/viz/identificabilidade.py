"""§14 — Sensibilidade 1D da identificabilidade R03 (175 rodadas).

Lê `results/identificabilidade_r03.parquet` (gerado por
`scripts/identificabilidade_r03.py`) e plota como cada parâmetro move
o alvo de volume (TCC/ano) — separando os que MOVEM (fracao_violadoras,
taxa_capacidade, k_rel) dos que NÃO MOVEM (rho — Δ mediana = 0).

Esta é a figura que **dissolve** o "conflito de 3 alvos" do R03 e
justifica reduzir o problema de calibração a 2 parâmetros dominantes.
A varredura tem 175 pontos (7 parâmetros × 5 valores × 5 seeds) mas a
síntese visual é uma tela.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

#: Ordem visual: do mais sensível ao mais ortogonal.
ORDEM_PARAMS: tuple[str, ...] = (
    "fracao_violadoras",
    "taxa_capacidade",
    "k_rel",
    "W_mult",
    "taxa_observacao",
    "taxa_falso_reporte",
    "rho",
)


def gerar_figura(
    parquet_path: str | Path = "results/identificabilidade_r03.parquet",
) -> tuple[Figure, list[Axes]]:
    """Painel 2×4 da sensibilidade 1D — TCC/ano vs valor do parâmetro."""
    aplicar_estilo()
    df = pd.read_parquet(parquet_path)

    fig, eixos_grid = plt.subplots(2, 4, figsize=(13, 6.8))
    eixos = list(eixos_grid.flatten())

    for ax, nome_param in zip(eixos[: len(ORDEM_PARAMS)], ORDEM_PARAMS, strict=False):
        sub = df[df["parametro"] == nome_param]
        if sub.empty:
            ax.axis("off")
            continue
        # mediana e IQR sobre seeds, agrupado por valor
        grupo = sub.groupby("valor")["tcc_anual"]
        valores = sorted(grupo.groups.keys())
        medianas = [grupo.get_group(v).median() for v in valores]
        q25 = [grupo.get_group(v).quantile(0.25) for v in valores]
        q75 = [grupo.get_group(v).quantile(0.75) for v in valores]

        amp = max(medianas) - min(medianas)
        dominante = amp > 0.5
        ortogonal = amp < 1e-6

        cor_principal = (
            PALETA["adv"] if ortogonal else (PALETA["B"] if dominante else PALETA["cade"])
        )

        ax.fill_between(valores, q25, q75, color=cor_principal, alpha=0.18)
        ax.plot(valores, medianas, marker="o", color=cor_principal, linewidth=2)
        ax.set_title(
            f"{nome_param}\n(Δ med = {amp:.3f})",
            fontsize=9,
            color="dimgrey" if ortogonal else "black",
        )
        ax.set_xlabel("valor do parâmetro", fontsize=8)
        ax.set_ylabel("TCC / ano simulado", fontsize=8)
        ax.tick_params(axis="both", labelsize=7)
        ax.grid(True, alpha=0.3)

        # Anotar veredicto
        if dominante:
            ax.text(
                0.97,
                0.05,
                "MOVE ALVO",
                transform=ax.transAxes,
                fontsize=7,
                fontweight="bold",
                color=cor_principal,
                ha="right",
                bbox={"facecolor": "white", "alpha": 0.7, "edgecolor": "none"},
            )
        elif ortogonal:
            ax.text(
                0.97,
                0.95,
                "ORTOGONAL — SAI",
                transform=ax.transAxes,
                fontsize=7,
                fontweight="bold",
                color=cor_principal,
                ha="right",
                va="top",
                bbox={"facecolor": "white", "alpha": 0.7, "edgecolor": "none"},
            )

    # Apagar eixo extra
    for ax in eixos[len(ORDEM_PARAMS) :]:
        ax.axis("off")

    fig.suptitle(
        "Identificabilidade R03 — sensibilidade 1D do alvo de volume (175 rodadas: 7 parâmetros × 5 valores × 5 seeds, Regime B)",
        fontsize=10,
    )
    fig.tight_layout()
    return fig, eixos


if __name__ == "__main__":
    fig, _ = gerar_figura()
    out = Path("docs/img/21_identificabilidade_r03.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
