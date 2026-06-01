#!/usr/bin/env python
"""Gera `docs/img/03_dissuasao_bem_estar.png` — saída real do modelo.

Categoria 6.4 (Designer, crítica x10): regenera com rótulos A/B nos painéis,
anotações numéricas, painel direito em escala adequada, marcadores por regime
e paleta cego-amigável.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.sobol.execucao import calcular_bem_estar
from waas_antitrust.viz import aplicar_estilo
from waas_antitrust.viz.paleta import HACHURAS, MARCADORES, PALETA


def _executar_regime(regime: str, seed: int = 11) -> dict:
    p = WaaSParametros(
        n_empresas=20,
        tam_medio_empresa=200,
        n_tiques=40,
        regime=regime,
        seed=seed,
        fracao_violadoras=0.5,
        taxa_observacao=0.4,
    )
    m = WaaSModel(p)
    df = m.executar()
    bem = calcular_bem_estar(
        dano=int(df["dano_acumulado"].max()),
        fp=int(df["falsos_positivos_acum"].max()),
        custo_recompensa=float(df["custo_recompensa_acum"].max()),
        w_a_base=p.w_a_base,
        custo_exodo=float(df["custo_exodo_acum"].max()),
        multa_arrecadada=float(df["multa_arrecadada_acum"].max()),
    )
    return {
        "df": df,
        "bem_estar": bem,
        "viol_serie": df["n_violadoras_ativas"].to_numpy(),
        "tiques": df["tique"].to_numpy(),
    }


def gerar(destino: Path, dpi: int = 150) -> None:
    aplicar_estilo()
    res = {r: _executar_regime(r) for r in ("A", "B", "C")}

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.0), gridspec_kw={"width_ratios": [1.3, 1.0]})

    # --- Painel A: número de violadoras ativas por tique ---
    axA = axes[0]
    for regime in ("A", "B", "C"):
        axA.plot(
            res[regime]["tiques"],
            res[regime]["viol_serie"],
            marker=MARCADORES[regime],
            markersize=5,
            markevery=4,
            linewidth=2,
            color=PALETA[regime],
            label=f"Regime {regime}",
        )
    axA.set_xlabel("tique (trimestre)")
    axA.set_ylabel("violadoras ativas")
    axA.set_title("Dissuasão endógena ao longo do tempo", fontweight="bold")
    axA.text(
        0.02, 0.94, "(A)", transform=axA.transAxes, fontsize=14, fontweight="bold", color="#333"
    )
    axA.grid(alpha=0.25)
    axA.legend(loc="upper right", framealpha=0.95)

    # Anotação: queda B/C em ~5 tiques
    viol_b = res["B"]["viol_serie"]
    if viol_b[0] > 0:
        ticks_to_zero = next((i for i, v in enumerate(viol_b) if v == 0), int(len(viol_b) * 0.3))
        axA.annotate(
            f"violadoras → 0\nem ~{ticks_to_zero} tiques",
            xy=(ticks_to_zero, 0),
            xytext=(ticks_to_zero + 7, max(viol_b) * 0.45),
            fontsize=10,
            color=PALETA["B"],
            arrowprops=dict(arrowstyle="->", color=PALETA["B"], lw=1.5),
        )

    # --- Painel B: bem-estar por regime (barras + hachuras) ---
    axB = axes[1]
    nomes = ["A", "B", "C"]
    bem_estares = [res[r]["bem_estar"] for r in nomes]
    cores = [PALETA[r] for r in nomes]
    bars = axB.bar(nomes, bem_estares, color=cores, edgecolor="black", linewidth=1.2, alpha=0.85)
    for bar, regime in zip(bars, nomes, strict=True):
        bar.set_hatch(HACHURAS[regime])
        altura = bar.get_height()
        rotulo_y = altura + (max(bem_estares) - min(bem_estares)) * 0.02
        axB.text(
            bar.get_x() + bar.get_width() / 2,
            rotulo_y,
            f"{altura:.0f}",
            ha="center",
            fontsize=10,
            fontweight="bold",
        )
    # Anotação Δ B vs A
    bem_a, bem_b = res["A"]["bem_estar"], res["B"]["bem_estar"]
    if bem_a < 0:
        delta_pct = 100.0 * (bem_b - bem_a) / abs(bem_a)
        axB.text(
            0.5,
            -0.15,
            f"ΔW (B sobre A) = {delta_pct:+.0f}%   ·   ΔW (C sobre A) = "
            f"{100.0 * (res['C']['bem_estar'] - bem_a) / abs(bem_a):+.0f}%",
            transform=axB.transAxes,
            fontsize=10,
            ha="center",
            color="#555",
        )

    axB.set_ylabel("bem-estar (menos negativo é melhor)")
    axB.set_title("Bem-estar social por regime", fontweight="bold")
    axB.text(
        0.02, 0.94, "(B)", transform=axB.transAxes, fontsize=14, fontweight="bold", color="#333"
    )
    axB.grid(alpha=0.25, axis="y")
    axB.axhline(0, color="black", lw=0.6, alpha=0.6)

    fig.suptitle(
        "Dissuasão endógena e bem-estar social — saída real do modelo (20 firmas, 40 tiques)",
        fontsize=12,
        fontweight="bold",
        y=1.02,
    )
    fig.tight_layout()
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, dpi=dpi, bbox_inches="tight")
    print(f"  gerada: {destino}")


def principal() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("docs/img/03_dissuasao_bem_estar.png"),
    )
    parser.add_argument("--dpi", type=int, default=150)
    args = parser.parse_args()
    gerar(args.out, args.dpi)


if __name__ == "__main__":
    principal()
