"""§9 — Capacidade e fluxo investigativo do CADE (calibração R06).

Visualiza as séries primárias extraídas dos Relatórios Integrados de
Gestão (RIG) 2022-2024 do CADE — fonte TCU, parseadas em
`calibracao/transparencia_cade.py` — e a série histórica de leniências
(comunicado CADE 2023, `calibracao/cade.py`).

Painel 1×2:

- **(A) Fluxo investigativo SG 2022-2024**: investigações instauradas,
  concluídas e estoque por ano (categoria ampla: PA + preparatório +
  inquérito). É a vazão real contra a qual `taxa_capacidade` precisa
  ser reescalonada (R06).
- **(B) Leniências acumuladas 2003-2023**: a série de 109 acordos em
  20 anos que ancora o alvo de calibração de volume (R03). Anotação
  marca o ponto 2023 (109 acumuladas).

Esta figura mostra DADOS EXTERNOS REAIS (não simulação) — a fonte
primária está nos docstrings dos módulos de calibração.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.calibracao.cade import SERIE_LENIENCIAS_CADE_2003_2023
from waas_antitrust.calibracao.transparencia_cade import (
    ESTOQUE_INVESTIGACOES_SG_POR_ANO,
    INVESTIGACOES_CONCLUIDAS_SG_POR_ANO,
    INVESTIGACOES_INSTAURADAS_SG_POR_ANO,
    N_SERVIDORES_AREA_FIM,
    N_SERVIDORES_EM_EXERCICIO_POR_ANO,
)
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def gerar_figura() -> tuple[Figure, list[Axes]]:
    """Painel 1×2 da capacidade investigativa real do CADE (RIG 2022-2024).

    Returns
    -------
    (Figure, [Axes, Axes])
    """
    aplicar_estilo()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ax_a, ax_b = axes[0], axes[1]

    # Painel A — fluxo investigativo SG por ano (barras agrupadas)
    anos = sorted(INVESTIGACOES_INSTAURADAS_SG_POR_ANO)
    x = np.arange(len(anos))
    largura = 0.27
    ax_a.bar(
        x - largura,
        [INVESTIGACOES_INSTAURADAS_SG_POR_ANO[a] for a in anos],
        largura,
        label="Instauradas",
        color=PALETA["B"],
        edgecolor="black",
        linewidth=0.4,
    )
    ax_a.bar(
        x,
        [INVESTIGACOES_CONCLUIDAS_SG_POR_ANO[a] for a in anos],
        largura,
        label="Concluídas",
        color=PALETA["C"],
        edgecolor="black",
        linewidth=0.4,
    )
    ax_a.bar(
        x + largura,
        [ESTOQUE_INVESTIGACOES_SG_POR_ANO[a] for a in anos],
        largura,
        label="Estoque",
        color=PALETA["adv"],
        edgecolor="black",
        linewidth=0.4,
    )
    # Anotação da força de trabalho por ano (eixo textual, sem 2º eixo y)
    for i, a in enumerate(anos):
        ax_a.annotate(
            f"{N_SERVIDORES_EM_EXERCICIO_POR_ANO[a]} serv.",
            (x[i], ESTOQUE_INVESTIGACOES_SG_POR_ANO[a] + 8),
            ha="center",
            fontsize=7,
            color="dimgrey",
        )
    ax_a.set_xticks(x)
    ax_a.set_xticklabels([str(a) for a in anos])
    ax_a.set_ylabel("Investigações SG (nº)")
    ax_a.set_title(f"(A) Fluxo investigativo SG — {N_SERVIDORES_AREA_FIM} na área-fim")
    ax_a.legend(fontsize=8)
    ax_a.grid(True, axis="y", alpha=0.3)

    # Painel B — leniências acumuladas 2003-2023
    anos_l = sorted(SERIE_LENIENCIAS_CADE_2003_2023)
    acum = [SERIE_LENIENCIAS_CADE_2003_2023[a] for a in anos_l]
    ax_b.plot(anos_l, acum, marker="o", markersize=3, color=PALETA["cade"])
    ax_b.annotate(
        f"{acum[-1]} acordos\nem 20 anos",
        (anos_l[-1], acum[-1]),
        textcoords="offset points",
        xytext=(-65, -10),
        fontsize=9,
    )
    ax_b.set_xlabel("Ano")
    ax_b.set_ylabel("Leniências acumuladas")
    ax_b.set_title("(B) Leniências CADE 2003-2023 (comunicado 2023)")
    ax_b.grid(True, alpha=0.3)

    fig.suptitle(
        "Dados primários — RIG/TCU 2022-2024 + comunicado CADE 2023 "
        "(calibracao/transparencia_cade.py, calibracao/cade.py)",
        fontsize=9,
    )
    fig.tight_layout()
    return fig, [ax_a, ax_b]


if __name__ == "__main__":
    from pathlib import Path

    fig, _ = gerar_figura()
    out = Path("docs/img/14_cade_capacidade.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
