"""Falsificação numérica da Proposição 5 candidata (R26 Coleman).

Lê `results/alpha_erosao_grade.parquet` (gerado por
`scripts/varredura_alpha_erosao.py`) e produz painel 1×2 que mostra,
contra o baseline do Regime A:

- **(A)** Mediana de `dano_acumulado` por `alpha_erosao` no Regime B,
  com banda IC bootstrap 95%; linha tracejada com o piso A.
- **(B)** Mediana de `capital_social_residual` final por `alpha_erosao`
  no Regime B — efeito direto do parâmetro sobre o substrato.

A leitura: a Proposição 5 candidata previa que existe `alpha*` tal que o
dano em B atravessa o piso em A. Na grade inicial (10 seeds × 8 alphas ×
40 tiques), **o cruzamento não ocorre** até alpha=0.9 — o efeito
Schelling (`p_perc` subindo via dissuasão endógena R01) domina a erosão
no nível agregado, mesmo quando o substrato cooperativo se aproxima de 0.

Esta figura **falsifica numericamente a Proposição 5 candidata** na sua
forma forte ("colapso em A"). A forma fraca (erosão do substrato) é
confirmada pelo painel B. Documentação: docs/limitacoes.md e DECISIONS R26.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.robustez import bootstrap_ci
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def gerar_figura(
    parquet_path: str | Path = "results/alpha_erosao_grade.parquet",
) -> tuple[Figure, list[Axes]]:
    """Painel 1×2 da falsificação numérica da Proposição 5 candidata."""
    aplicar_estilo()
    df = pd.read_parquet(parquet_path)
    alphas = sorted(df[df["regime"] == "B"]["alpha_erosao"].unique())

    medianas_b: list[float] = []
    ci_inf_b: list[float] = []
    ci_sup_b: list[float] = []
    capital_med: list[float] = []
    capital_inf: list[float] = []
    capital_sup: list[float] = []
    for alpha in alphas:
        sub = df[(df["regime"] == "B") & (df["alpha_erosao"] == alpha)]
        ic_dano = bootstrap_ci(sub["dano_acumulado"].to_list(), n_bootstrap=1000, seed=int(alpha * 1000))
        medianas_b.append(ic_dano.mediana)
        ci_inf_b.append(ic_dano.inferior)
        ci_sup_b.append(ic_dano.superior)
        ic_cap = bootstrap_ci(
            sub["capital_social_residual"].to_list(), n_bootstrap=1000, seed=int(alpha * 1000) + 1
        )
        capital_med.append(ic_cap.mediana)
        capital_inf.append(ic_cap.inferior)
        capital_sup.append(ic_cap.superior)

    sub_a = df[df["regime"] == "A"]["dano_acumulado"].to_list()
    ic_a = bootstrap_ci(sub_a, n_bootstrap=1000, seed=0)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ax_a, ax_b = axes[0], axes[1]

    # Painel A: dano por alpha vs piso A
    ax_a.fill_between(alphas, ci_inf_b, ci_sup_b, color=PALETA["B"], alpha=0.18)
    ax_a.plot(alphas, medianas_b, marker="o", color=PALETA["B"], label="Regime B (mediana, IC 95%)")
    ax_a.axhline(ic_a.mediana, color=PALETA["A"], linestyle="--", label=f"Regime A (piso, mediana = {ic_a.mediana:.0f})")
    ax_a.set_xlabel(r"$\alpha_{\mathrm{erosão}}$")
    ax_a.set_ylabel("Dano acumulado (final)")
    ax_a.set_title("(A) Prop. 5 forte: B não atravessa A")
    ax_a.legend(loc="center right", fontsize=8)
    ax_a.grid(True, alpha=0.3)

    # Painel B: substrato cooperativo erodido
    ax_b.fill_between(alphas, capital_inf, capital_sup, color=PALETA["cade"], alpha=0.18)
    ax_b.plot(alphas, capital_med, marker="s", color=PALETA["cade"], label="Capital social residual final")
    ax_b.axhline(1.0, color="grey", linestyle=":", alpha=0.5, label="Baseline alpha=0")
    ax_b.set_xlabel(r"$\alpha_{\mathrm{erosão}}$")
    ax_b.set_ylabel("Capital social residual")
    ax_b.set_title("(B) Prop. 5 fraca: substrato sim erodido")
    ax_b.set_ylim(-0.05, 1.10)
    ax_b.legend(loc="upper right", fontsize=8)
    ax_b.grid(True, alpha=0.3)

    fig.suptitle(
        "Falsificação numérica da Proposição 5 candidata (R26 Coleman)",
        fontsize=11,
    )
    fig.tight_layout()
    return fig, [ax_a, ax_b]


if __name__ == "__main__":
    fig, _ = gerar_figura()
    out = Path("docs/img/10_alpha_erosao_limiar.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
