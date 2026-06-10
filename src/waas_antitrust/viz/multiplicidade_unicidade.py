"""§v2.G — Contraste numérico multiplicidade × unicidade (R02b, Mat B).

Visualização do contraste central de Morris-Shin (1998): sob **informação
comum** (`τ → ∞`), o jogo de coordenação admite **múltiplos equilíbrios**
de switching; sob **informação privada** (`τ → 0`), o equilíbrio é
**único**. A passagem entre os dois regimes seleciona equilíbrio.

A figura mostra dois painéis:

- **(A)** Curvas de melhor-resposta no espaço (θ, σ): sob conhecimento
  comum, há múltiplos pontos fixos (equilíbrios). Plotam-se até 3
  ramos: ramo "todos sinalizam", "ninguém sinaliza", ramo intermediário
  instável.
- **(B)** Trajetória `x*(τ)` quando τ varia de τ→0 (Morris-Shin) até
  τ → 0.5 (limite estilizado). Mostra a convergência ao limiar único.

Atende a R02b do balanço 360° — exibir os DOIS RAMOS conforme pedido
pelo Mat B da crítica x10 v1.

Caveat técnico (Mat A v2): sob LCMC com fila inter-firma, sinal público
correlacionado pode RESTAURAR multiplicidade (Angeletos-Hellwig-Pavan
2007). Esta figura ilustra apenas o subgame estilizado homogêneo.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.jogo_global import limiar_switching, trilha_convergencia
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def gerar_figura(
    b: float = 2.0,
    c: float = 1.0,
    k: float = 0.2,
    taus: tuple[float, ...] = (0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5),
) -> tuple[Figure, list[Axes]]:
    """Painel 1×2: multiplicidade sob conhecimento comum × unicidade Morris-Shin.

    Parameters
    ----------
    b : float
        Ganho marginal por unidade de severidade.
    c : float
        Custo de denúncia frustrada.
    k : float
        Massa crítica como fração [0, 1].
    taus : tuple[float, ...]
        Sequência de ruídos τ para trilha de convergência (default 7 pontos).

    Returns
    -------
    (Figure, [Axes, Axes])
    """
    aplicar_estilo()
    fig, (ax_mult, ax_unic) = plt.subplots(1, 2, figsize=(11, 4.5))

    # --- Painel A: múltiplos equilíbrios sob conhecimento comum ---
    # Em jogo de coordenação 2x2 com complementaridades estratégicas,
    # sob conhecimento comum há 3 equilíbrios candidatos:
    #   (1) "todos sinalizam" — equilíbrio cooperativo estável
    #   (2) "ninguém sinaliza" — equilíbrio não-cooperativo estável
    #   (3) "fração k sinaliza" — equilíbrio intermediário INSTÁVEL
    # A função de melhor-resposta tem formato S — interseções com a
    # diagonal são os equilíbrios.
    sigma = np.linspace(0, 1, 100)

    # Melhor-resposta (heurística estilizada): sigmoide centrada em k
    # com inclinação dependendo do payoff.
    slope = 20.0
    br = 1.0 / (1.0 + np.exp(-slope * (sigma - k)))

    ax_mult.plot(sigma, br, color=PALETA["B"], lw=2.0, label="Melhor-resposta BR(σ)")
    ax_mult.plot(
        sigma,
        sigma,
        color=PALETA["neutro_escuro"],
        ls="--",
        lw=1.2,
        alpha=0.6,
        label="Diagonal σ = σ",
    )

    # Marcar os 3 equilíbrios candidatos (interseções)
    equilibrios = [(0.0, 0.0), (k, k), (1.0, 1.0)]
    rotulos_eq = ["Eq. trivial\n(ninguém)", "Eq. instável\n(σ = k)", "Eq. cooperativo\n(todos)"]
    cores_eq = [PALETA["A"], PALETA["adv"], PALETA["destaque"]]
    for (x, y), rotulo, cor in zip(equilibrios, rotulos_eq, cores_eq, strict=False):
        ax_mult.plot(x, y, marker="o", markersize=10, color=cor, zorder=5)
        ax_mult.annotate(
            rotulo,
            xy=(x, y),
            xytext=(x + 0.08, y - 0.12 if x > 0.5 else y + 0.18),
            fontsize=8.5,
            color=cor,
            arrowprops={"arrowstyle": "-", "color": cor, "alpha": 0.4},
        )

    ax_mult.set_xlim(-0.05, 1.05)
    ax_mult.set_ylim(-0.05, 1.05)
    ax_mult.set_xlabel("Fração que sinaliza (σ)")
    ax_mult.set_ylabel("Fração esperada como melhor-resposta")
    ax_mult.set_title(
        "(A) Conhecimento comum: múltiplos equilíbrios",
        fontsize=10.5,
        loc="left",
    )
    ax_mult.legend(loc="lower right", fontsize=8.5, framealpha=0.9)
    ax_mult.grid(True, alpha=0.25, linestyle=":")

    # --- Painel B: convergência Morris-Shin sob informação privada ---
    # trilha_convergencia já existe em jogo_global.py
    limiares = trilha_convergencia(b, c, k, list(taus))
    limiar_zero = limiar_switching(b, c, k, tau=0.0)

    ax_unic.plot(
        taus,
        limiares,
        marker="o",
        markersize=7,
        color=PALETA["C"],
        lw=2.0,
        label="$x^\\star(\\tau)$",
    )
    ax_unic.axhline(
        limiar_zero,
        color=PALETA["neutro_escuro"],
        ls=":",
        lw=1.0,
        alpha=0.7,
        label=f"Limite Morris-Shin ($\\tau \\to 0$): $x^\\star = {limiar_zero:.3f}$",
    )

    ax_unic.set_xlim(min(taus) - 0.02, max(taus) + 0.02)
    ax_unic.set_xlabel("Ruído do sinal privado ($\\tau$)")
    ax_unic.set_ylabel("Limiar de switching $x^\\star$")
    ax_unic.set_title(
        "(B) Informação privada: equilíbrio único",
        fontsize=10.5,
        loc="left",
    )
    ax_unic.legend(loc="upper right", fontsize=8.5, framealpha=0.9)
    ax_unic.grid(True, alpha=0.25, linestyle=":")

    fig.suptitle(
        f"R02b — contraste multiplicidade × unicidade (b={b}, c={c}, k={k})",
        fontsize=11,
        y=0.99,
    )
    fig.tight_layout()
    return fig, [ax_mult, ax_unic]
