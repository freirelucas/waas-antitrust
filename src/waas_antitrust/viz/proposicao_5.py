"""§v2.B.4 + balanço 360° item #7 — Validar Proposição 5 candidata visualmente.

Painel 1×2 dedicado à Proposição 5 candidata (R26 Coleman): existe
`alpha_erosao*` tal que para `alpha_erosao > *`, Regime B colapsa em
A após N tiques. A figura compara, para 4 valores de `alpha_erosao` em
multi-seed:

- **(A)** Trajetórias de `capital_social_residual` ao longo do tempo.
- **(B)** Dano acumulado relativo ao baseline (alpha=0).

A leitura: se Coleman estiver certo, o painel B mostra o dano
acumulado crescendo monotônicamente com alpha — confirmando que
"premiar denúncia destrói o substrato que produz a cooperação".

Sob o reframe v3 (canal de depósito condicional), R26 é diagnóstico
secundário (não mecanismo central). Esta visualização confirma ou
falsifica o diagnóstico empiricamente.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def gerar_figura(
    n_tiques: int = 40,
    seeds: tuple[int, ...] = (11, 23, 37, 41, 59),
    alphas: tuple[float, ...] = (0.0, 0.1, 0.3, 0.7),
) -> tuple[Figure, list[Axes]]:
    """Painel 1×2 da Proposição 5 candidata, multi-seed.

    Parameters
    ----------
    n_tiques : int
        Horizonte temporal (default 40).
    seeds : tuple[int, ...]
        Sementes para multi-seed averaging (default 5 seeds).
    alphas : tuple[float, ...]
        Valores de `alpha_erosao` a comparar (default 4 valores).

    Returns
    -------
    (Figure, [Axes, Axes])
        Painel 1×2 (capital social residual; dano relativo).
    """
    aplicar_estilo()
    fig, (ax_cs, ax_dano) = plt.subplots(1, 2, figsize=(11, 4.5))

    cores = [PALETA["A"], PALETA["B"], PALETA["destaque"], PALETA["adv"]]
    rotulos = [f"$\\alpha$ = {a:.1f}" for a in alphas]

    # Coleta multi-seed para cada alpha
    capital_por_alpha: dict[float, np.ndarray] = {}
    dano_por_alpha: dict[float, np.ndarray] = {}
    for alpha in alphas:
        capital_seeds = []
        dano_seeds = []
        for seed in seeds:
            m = WaaSModel(
                WaaSParametros(
                    n_empresas=15,
                    tam_medio_empresa=150,
                    n_tiques=n_tiques,
                    seed=seed,
                    regime="B",
                    fracao_violadoras=0.7,
                    taxa_observacao=0.6,
                    alpha_erosao=alpha,
                )
            )
            df = m.executar()
            capital_seeds.append(df["capital_social_residual"].to_numpy())
            dano_seeds.append(df["dano_acumulado"].to_numpy())
        capital_por_alpha[alpha] = np.array(capital_seeds)  # (n_seeds, n_tiques)
        dano_por_alpha[alpha] = np.array(dano_seeds)

    # Painel A: capital social residual (média + envelope ±1 std)
    for alpha, cor, rotulo in zip(alphas, cores, rotulos, strict=False):
        serie = capital_por_alpha[alpha]
        media = serie.mean(axis=0)
        std = serie.std(axis=0)
        tiques = np.arange(len(media))
        ax_cs.plot(tiques, media, color=cor, lw=2.0, label=rotulo)
        ax_cs.fill_between(tiques, media - std, media + std, color=cor, alpha=0.15)

    ax_cs.axhline(
        0.5,
        color=PALETA["neutro_escuro"],
        ls=":",
        lw=0.9,
        alpha=0.5,
        label="patamar crítico (R03)",
    )
    ax_cs.set_xlim(0, n_tiques - 1)
    ax_cs.set_ylim(0.0, 1.05)
    ax_cs.set_xlabel("Tique (trimestre)")
    ax_cs.set_ylabel("Capital social residual (média ± 1 std)")
    ax_cs.set_title(
        "(A) Capital social residual ao longo do tempo",
        fontsize=10.5,
        loc="left",
    )
    ax_cs.legend(loc="lower left", fontsize=8.5, framealpha=0.9)
    ax_cs.grid(True, alpha=0.25, linestyle=":")

    # Painel B: dano acumulado relativo ao baseline alpha=0
    dano_baseline = dano_por_alpha[alphas[0]].mean(axis=0)
    for alpha, cor, rotulo in zip(alphas, cores, rotulos, strict=False):
        media = dano_por_alpha[alpha].mean(axis=0)
        # Ratio em relação ao baseline para evidenciar quanto "extra de dano"
        # alpha alto produz. Baseline (alpha=0) = 1.0 em todos os tiques.
        # Adiciona pequeno epsilon para evitar divisão por zero nos primeiros tiques.
        ratio = (media + 1) / (dano_baseline + 1)
        tiques = np.arange(len(media))
        ax_dano.plot(tiques, ratio, color=cor, lw=2.0, label=rotulo)

    ax_dano.axhline(
        1.0,
        color=PALETA["neutro_escuro"],
        ls="--",
        lw=0.9,
        alpha=0.5,
        label="baseline ($\\alpha=0$)",
    )
    ax_dano.set_xlim(0, n_tiques - 1)
    ax_dano.set_xlabel("Tique (trimestre)")
    ax_dano.set_ylabel("Dano acumulado / baseline")
    ax_dano.set_title(
        "(B) Dano acumulado relativo (mostra Proposição 5)",
        fontsize=10.5,
        loc="left",
    )
    ax_dano.legend(loc="upper left", fontsize=8.5, framealpha=0.9)
    ax_dano.grid(True, alpha=0.25, linestyle=":")

    fig.suptitle(
        f"Proposição 5 candidata — multi-seed ({len(seeds)} seeds, horizonte {n_tiques} tiques)",
        fontsize=11,
        y=0.99,
    )
    fig.tight_layout()
    return fig, [ax_cs, ax_dano]
