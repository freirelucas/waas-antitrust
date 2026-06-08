"""§v2.B.4 — Erosão endógena do capital social (R26, Coleman 1990).

Visualização da Proposição 5 candidata: existe `alpha_erosao*` tal que para
`alpha_erosao > *`, Regime B colapsa em A após N tiques. A figura compara
três trajetórias de `capital_social_residual` ao longo do tempo: sem
erosão (alpha=0), erosão leve (alpha=0.2), erosão moderada (alpha=0.5).

A leitura sob reframe: o WaaS não opera sobre um substrato infinito —
opera sobre capital social organizacional finito, que pode ser consumido
pelo próprio uso instrumental (Coleman 1990, Foundations cap. 12).
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def gerar_figura(
    n_tiques: int = 20,
    seed: int = 41,
    alphas: tuple[float, ...] = (0.0, 0.2, 0.5),
) -> tuple[Figure, Axes]:
    """Trajetórias de `capital_social_residual` para múltiplos `alpha_erosao`.

    Parameters
    ----------
    n_tiques : int
        Horizonte temporal (default 20).
    seed : int
        Semente para reprodutibilidade.
    alphas : tuple[float, ...]
        Valores de `alpha_erosao` a comparar (default: 0, 0.2, 0.5).

    Returns
    -------
    (Figure, Axes)
    """
    aplicar_estilo()
    fig, ax = plt.subplots(figsize=(8, 4.5))

    cores = [PALETA["A"], PALETA["B"], PALETA["adv"]]
    rotulos_alpha = [f"$\\alpha_{{erosão}}$ = {a:.1f}" for a in alphas]

    for alpha, cor, rotulo in zip(alphas, cores, rotulos_alpha, strict=False):
        m = WaaSModel(
            WaaSParametros(
                n_empresas=10,
                tam_medio_empresa=120,
                n_tiques=n_tiques,
                seed=seed,
                regime="B",
                fracao_violadoras=0.7,
                taxa_observacao=0.6,
                alpha_erosao=alpha,
            )
        )
        df = m.executar()
        ax.plot(
            df.index,
            df["capital_social_residual"],
            color=cor,
            lw=2.0,
            label=rotulo,
        )

    ax.axhline(
        0.5,
        color=PALETA["neutro_escuro"],
        ls=":",
        lw=0.9,
        alpha=0.5,
        label="patamar crítico (calibrar em R03)",
    )

    ax.set_xlim(0, n_tiques - 1)
    ax.set_ylim(0.0, 1.05)
    ax.set_xlabel("Tique (trimestre)")
    ax.set_ylabel("Capital social residual")
    ax.set_title(
        "Coleman: erosão endógena do capital social por uso instrumental",
        fontsize=11,
        loc="left",
    )
    ax.legend(loc="lower left", fontsize=8.5, framealpha=0.9)
    ax.grid(True, alpha=0.25, linestyle=":")

    fig.tight_layout()
    return fig, ax
