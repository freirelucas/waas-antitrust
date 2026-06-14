"""§13 — Trajetórias do modelo sob os 5 catálogos canônicos de choque.

R19 expandido. Cada catálogo em `choques.py` (CHOQUES_TECH_2022_2024 cíclico,
CHOQUES_TECH_2024_2025_AI_RESTRUCTURING estrutural, CHOQUES_CAMPANHA_CADE_DIGITAL,
CHOQUES_CASO_PARADIGMATICO_IFOOD_2023, CHOQUES_JURIDICO_ADVERSO) é rodado contra
o baseline sem choque. A figura mostra como cada tipo de choque institucional
desloca a trajetória de dano acumulado.

Hipótese substantiva (autor): "layoffs IA podem ser oportunidade" — o trabalhador
ex-funcionário tem represália efetiva reduzida e mantém capacidade de sinalizar
(`historico_observou > 0`). A figura permite ver se o catálogo AI restructuring
realmente reduz o dano agregado vs o baseline.
"""

from __future__ import annotations

from dataclasses import replace

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.choques import (
    CHOQUES_CAMPANHA_CADE_DIGITAL,
    CHOQUES_CASO_PARADIGMATICO_IFOOD_2023,
    CHOQUES_JURIDICO_ADVERSO,
    CHOQUES_TECH_2022_2024,
    CHOQUES_TECH_2024_2025_AI_RESTRUCTURING,
)
from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

DEFAULT_SEEDS: tuple[int, ...] = (11, 23, 37, 41, 53)

CATALOGOS: tuple[tuple[str, tuple, str], ...] = (
    ("Baseline (sem choque)", (), "B"),
    ("Tech 2022-2024 (cíclico)", CHOQUES_TECH_2022_2024, "C"),
    ("Tech 2024-2025 (IA estrutural)", CHOQUES_TECH_2024_2025_AI_RESTRUCTURING, "cade"),
    ("Campanha CADE digital", CHOQUES_CAMPANHA_CADE_DIGITAL, "adv"),
    ("Caso paradigmático iFood 2023", CHOQUES_CASO_PARADIGMATICO_IFOOD_2023, "A"),
    ("Choque jurídico adverso", CHOQUES_JURIDICO_ADVERSO, "violadoras"),
)


def gerar_figura(
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    n_tiques: int = 24,
) -> tuple[Figure, list[Axes]]:
    """Painel 2×3 do dano agregado sob os 5 catálogos de choque vs baseline."""
    aplicar_estilo()
    base = WaaSParametros(
        n_empresas=15,
        tam_medio_empresa=150,
        n_tiques=n_tiques,
        regime="B",
        fracao_violadoras=0.55,
        taxa_observacao=0.4,
    )

    tempo = np.arange(1, n_tiques + 1)
    fig, eixos_grid = plt.subplots(2, 3, figsize=(13, 7.2))
    eixos = list(eixos_grid.flatten())
    cor_base = PALETA["B"]

    medianas: dict[str, np.ndarray] = {}
    for nome, catalogo, _ in CATALOGOS:
        curvas = []
        for seed in seeds:
            params = replace(base, seed=seed, choques=catalogo)
            df = WaaSModel(params).executar()
            curvas.append(df["dano_acumulado"].to_numpy(dtype=float))
        medianas[nome] = np.median(np.vstack(curvas), axis=0)

    baseline = medianas["Baseline (sem choque)"]
    for ax, (nome, _, cor_key) in zip(eixos, CATALOGOS, strict=True):
        if nome == "Baseline (sem choque)":
            ax.plot(tempo, baseline, color=cor_base, linewidth=2.2, label="Baseline")
            ax.set_title("(0) " + nome, fontsize=10)
        else:
            ax.plot(tempo, baseline, color="grey", linewidth=1.4, linestyle="--", label="Baseline")
            cor = PALETA.get(cor_key, PALETA["C"])
            ax.plot(
                tempo, medianas[nome], color=cor, linewidth=2.2, label=nome.split("(")[0].strip()
            )
            ax.set_title(nome, fontsize=9)
        ax.set_xlabel("Tique (trimestre)", fontsize=8)
        ax.set_ylabel("Dano acumulado", fontsize=8)
        ax.legend(fontsize=7, loc="upper left")
        ax.grid(True, alpha=0.3)

    fig.suptitle(
        f"Trajetórias sob os 5 catálogos de choque (R19) — mediana de {len(seeds)} seeds × {n_tiques} tiques, Regime B",
        fontsize=11,
    )
    fig.tight_layout()
    return fig, eixos


if __name__ == "__main__":
    from pathlib import Path

    fig, _ = gerar_figura()
    out = Path("docs/img/20_choques_5_catalogos.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
