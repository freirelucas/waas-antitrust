"""§4 — Formação de massa crítica como cascata na rede intra-firma.

Implementação real (não mais stub). Sob o reframe v2, a figura mostra a
**cooperação interna como bem coletivo emergente** — uma curva sigmoidal
de cumulativa de sinalização ao longo do tempo, sobreposta às linhas de
gatilho (`q_min` e `k_rel`).

A leitura central: a massa crítica é **evento emergente**, não decidido.
Ninguém "escolhe" formar massa crítica; ela se forma quando o conjunto
de condições microscópicas (observabilidade, arquétipos, `phi_vizinhos`)
atravessa o limiar de cascata complexa (Centola-Macy 2007).

Sob LCMC, a curva também mostra a posição na fila intra-firma: o 1º
cooperador entra com o decaimento Saito completo (recompensa 100%); a
fronteira da cascata cresce com posições recebendo recompensas
decrescentes (43,43% → 34,51% → 20,22%).
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def gerar_figura(
    n_tiques: int = 40,
    q_min: float = 0.10,
    k_rel: float = 0.05,
    seed: int = 42,
) -> tuple[Figure, Axes]:
    """Formação de massa crítica como cascata sigmoidal.

    Apresenta uma trajetória estilizada (sem rodar o modelo) que ilustra
    o ponto conceitual do reframe: cooperação interna emerge por cascata,
    o pagamento via TCC apenas estabiliza.

    Parameters
    ----------
    n_tiques : int
        Horizonte temporal em tiques (default 40 = 10 anos).
    q_min : float
        Gatilho de massa crítica interna (LCMC, fração [0,1]).
    k_rel : float
        Gatilho de notificação clássico (Regime B, fração [0,1]).
    seed : int
        Semente para o jitter estilizado.

    Returns
    -------
    (Figure, Axes)
        Tupla matplotlib para inclusão no paper/site via padrão
        `gerar_figura()`.
    """
    aplicar_estilo()

    rng = np.random.default_rng(seed)
    tiques = np.arange(n_tiques)
    # Curva sigmoidal canônica de cascata (Granovetter 1978; Centola-Macy 2007).
    # Logística com centro em t* = n_tiques/3 e escala = n_tiques/12.
    t_estrela = n_tiques / 3.0
    escala = n_tiques / 12.0
    cumulativa_teorica = 1.0 / (1.0 + np.exp(-(tiques - t_estrela) / escala))

    # Jitter pequeno para simular estocasticidade discreta de seeds.
    jitter = rng.normal(scale=0.015, size=n_tiques)
    cumulativa = np.clip(cumulativa_teorica + jitter, 0.0, 1.0)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Curva de cumulativa de cooperação.
    ax.plot(
        tiques,
        cumulativa,
        color=PALETA["B"],
        lw=2.2,
        label="Fração cumulativa de cooperação interna",
        zorder=3,
    )
    ax.fill_between(
        tiques,
        0,
        cumulativa,
        color=PALETA["B"],
        alpha=0.12,
        zorder=2,
    )

    # Linhas de gatilho.
    ax.axhline(
        q_min,
        color=PALETA["C"],
        ls="--",
        lw=1.4,
        label=f"$q_{{\\min}}$ = {q_min:.0%} (gatilho LCMC, R20)",
        zorder=4,
    )
    ax.axhline(
        k_rel,
        color=PALETA["cade"],
        ls=":",
        lw=1.4,
        label=f"$k_{{\\mathrm{{rel}}}}$ = {k_rel:.0%} (gatilho notificação)",
        zorder=4,
    )

    # Anotação do break-even: onde a cumulativa cruza q_min.
    idx_break = int(np.argmax(cumulativa >= q_min))
    if cumulativa[idx_break] >= q_min:
        ax.axvline(
            idx_break,
            color=PALETA["neutro_escuro"],
            ls="-",
            lw=0.8,
            alpha=0.4,
            zorder=1,
        )
        ax.annotate(
            f"massa crítica\nformada\n(tique {idx_break})",
            xy=(idx_break, q_min),
            xytext=(idx_break + 2, q_min + 0.18),
            fontsize=8.5,
            color=PALETA["neutro_escuro"],
            arrowprops={
                "arrowstyle": "->",
                "color": PALETA["neutro_escuro"],
                "alpha": 0.6,
            },
        )

    ax.set_xlim(0, n_tiques - 1)
    ax.set_ylim(0, 1.0)
    ax.set_xlabel("Tique (trimestre)")
    ax.set_ylabel("Fração de trabalhadores cooperando")
    ax.set_title(
        "Cooperação interna como cascata emergente",
        fontsize=11,
        loc="left",
    )
    ax.legend(loc="lower right", fontsize=8.5, framealpha=0.9)
    ax.grid(True, alpha=0.25, linestyle=":")

    fig.tight_layout()
    return fig, ax
