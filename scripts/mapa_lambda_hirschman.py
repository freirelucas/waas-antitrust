#!/usr/bin/env python
"""Mapa de regime em (λ, peso_hirschman) — resposta ao Mat A (v1).

A crítica do Mat A apontou possíveis bifurcações não-diagramadas no
acoplamento entre dois ganhos de retroalimentação:

- **λ** (`lambda_expectativa`, R01): peso da expectativa adaptativa da
  detecção percebida — o ganho do laço dissuasório.
- **peso_hirschman** (R07): desconto preventivo sobre `g_i` pela ameaça
  de êxodo coletivo — o ganho do laço contratual.

Este script NÃO faz análise formal de bifurcação (autovalores do
jacobiano ficam para trabalho futuro); produz o **mapa empírico de
regime**: heatmap de `dano_acumulado` final (mediana multi-seed) sobre
a grade (λ × peso_hirschman) em Regime C com Hirschman universal
(`fracao_contratos_acelerados=1`). Leitura: transições abruptas de cor
na grade são candidatas a fronteiras de bifurcação; gradientes suaves
indicam resposta monotônica sem mudança qualitativa de regime.

Saídas:
- `results/mapa_lambda_hirschman.parquet` (long: λ, peso, seed, dano).
- `docs/img/19_mapa_lambda_hirschman.png` (heatmap da mediana).

Uso:
    python scripts/mapa_lambda_hirschman.py
    python scripts/mapa_lambda_hirschman.py --grade 7 --seeds 11 23 37 41 53
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.viz.paleta import aplicar_estilo


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--grade", type=int, default=5, help="pontos por eixo")
    ap.add_argument("--seeds", type=int, nargs="+", default=[11, 23, 37])
    ap.add_argument("--tiques", type=int, default=20)
    ap.add_argument("--out", type=str, default="results/mapa_lambda_hirschman.parquet")
    ap.add_argument("--fig", type=str, default="docs/img/19_mapa_lambda_hirschman.png")
    args = ap.parse_args()

    lambdas = np.linspace(0.05, 0.95, args.grade)
    pesos = np.linspace(0.0, 1.0, args.grade)
    print(
        f"Mapa (λ × peso_hirschman): {args.grade}×{args.grade} × "
        f"{len(args.seeds)} seeds × {args.tiques} tiques = "
        f"{args.grade**2 * len(args.seeds)} rodadas"
    )

    registros: list[dict[str, float]] = []
    for lam in lambdas:
        for peso in pesos:
            for seed in args.seeds:
                params = WaaSParametros(
                    n_empresas=10,
                    tam_medio_empresa=100,
                    n_tiques=args.tiques,
                    seed=seed,
                    regime="C",  # Hirschman exige C (gating Art. 22 I CF)
                    fracao_contratos_acelerados=1.0,
                    fracao_violadoras=0.6,
                    taxa_observacao=0.45,
                    lambda_expectativa=float(lam),
                    peso_hirschman=float(peso),
                )
                df = WaaSModel(params).executar()
                registros.append(
                    {
                        "lambda_expectativa": float(lam),
                        "peso_hirschman": float(peso),
                        "seed": seed,
                        "dano_acumulado": float(df["dano_acumulado"].iloc[-1]),
                    }
                )

    long_df = pd.DataFrame(registros)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    long_df.to_parquet(out, index=False)
    print(f"Gravado: {out} ({len(long_df)} linhas)")

    # Heatmap da mediana
    medianas = (
        long_df.groupby(["lambda_expectativa", "peso_hirschman"])["dano_acumulado"]
        .median()
        .unstack()  # linhas = λ, colunas = peso
    )
    aplicar_estilo()
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    im = ax.imshow(
        medianas.to_numpy(),
        origin="lower",
        aspect="auto",
        cmap="cividis",
        extent=(float(pesos[0]), float(pesos[-1]), float(lambdas[0]), float(lambdas[-1])),
    )
    fig.colorbar(im, ax=ax, label="Dano acumulado (mediana, final)")
    ax.set_xlabel("peso_hirschman (ganho do laço contratual, R07)")
    ax.set_ylabel(r"$\lambda$ (ganho do laço dissuasório, R01)")
    ax.set_title(
        f"Mapa de regime em (λ × peso_hirschman) — Regime C, Hirschman universal\n"
        f"mediana de {len(args.seeds)} seeds × {args.tiques} tiques",
        fontsize=10,
    )
    fig.tight_layout()
    fig_path = Path(args.fig)
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_path, dpi=150, bbox_inches="tight")
    print(f"Gravado: {fig_path}")

    # Diagnóstico textual: amplitude e gradiente máximo entre células vizinhas
    matriz = medianas.to_numpy()
    amplitude = float(np.nanmax(matriz) - np.nanmin(matriz))
    grad_v = np.abs(np.diff(matriz, axis=0)).max() if matriz.shape[0] > 1 else 0.0
    grad_h = np.abs(np.diff(matriz, axis=1)).max() if matriz.shape[1] > 1 else 0.0
    print(
        f"\nDiagnóstico: amplitude total = {amplitude:.1f}; "
        f"salto máximo entre células vizinhas = {max(grad_v, grad_h):.1f}."
    )
    if amplitude > 0 and max(grad_v, grad_h) > 0.5 * amplitude:
        print(
            "Salto vizinho > 50% da amplitude — há transição abrupta na grade: "
            "candidata a fronteira de bifurcação; refinar a grade em torno do salto."
        )
    else:
        print(
            "Resposta predominantemente suave na grade — sem evidência de "
            "transição qualitativa abrupta nesta resolução (Mat A: o mapa "
            "empírico não acusa bifurcação; análise formal segue futura)."
        )


if __name__ == "__main__":
    main()
