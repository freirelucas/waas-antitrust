"""§5 — Diagrama de fluxo (Sankey) da corrida LCMC.

R20 Fase 6: visualiza o fluxo agregado de denúncias do sistema sob a
LCMC com canal de depósito condicional explícito. As 5 etapas:

1. **Sinais**: trabalhadores que decidiram sinalizar (P1/P2).
2. **Depósitos**: sinais que viraram depósito condicional no escrow
   do CADE (sob `usar_escrow_explicito=True`).
3. **Massa crítica**: firmas que atingiram o gatilho intra-firma
   $q_{\\min}\\cdot n$ no horizonte.
4. **Aberturas simultâneas**: depósitos que se abriram quando massa
   crítica foi atingida (all-or-nothing à la Kickstarter).
5. **TCCs assinados**: casos em que a firma optou pelo TCC com
   ressarcimento WaaS (IC-F* ativada).

A figura mostra também os ramos perdidos: depósitos que **permanecem**
em escrow ao fim do horizonte e depósitos que **expiraram** sob
`janela_escrow_tiques > 0` (R27-ii).

Implementação minimalista com `matplotlib.patches` (Rectangle + Polygon
para os fluxos). Sem dependência nova além do conjunto técnico definido
em CLAUDE.md.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Polygon, Rectangle

from waas_antitrust.cenarios import aplicar_cenario
from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def _executar_cenario_demo(seed: int = 2026) -> dict[str, int]:
    """Executa cenário canônico LCMC com escrow explícito e devolve fluxos."""
    params = aplicar_cenario(
        WaaSParametros(
            n_empresas=10,
            tam_medio_empresa=120,
            n_tiques=15,
            seed=seed,
            fracao_violadoras=0.6,
            taxa_observacao=0.45,
            usar_escrow_explicito=True,
        ),
        "cenario_corrida_leniencia",
    )
    df = WaaSModel(params).executar()
    final = df.iloc[-1]
    return {
        "sinais": int(final["n_sinais"]),
        "depositos": int(final["n_aberturas_simultaneas_acum"])
        + int(final["n_denuncias_em_escrow"])
        + int(final["n_depositos_expirados_acum"]),
        "firmas_mc": int(final["n_firmas_atingiram_massa_critica_interna"]),
        "aberturas": int(final["n_aberturas_simultaneas_acum"]),
        "tccs": int(final["n_tcc_assinados"]),
        "em_escrow": int(final["n_denuncias_em_escrow"]),
        "expirados": int(final["n_depositos_expirados_acum"]),
    }


def gerar_figura(
    fluxos: dict[str, int] | None = None,
    seed: int = 2026,
) -> tuple[Figure, Axes]:
    """Diagrama de fluxo (Sankey simplificado) da corrida LCMC.

    Parameters
    ----------
    fluxos : dict, opcional
        Dicionário com os fluxos agregados ({"sinais", "depositos",
        "aberturas", "tccs", "em_escrow", "expirados"}). Se omitido,
        executa o cenário canônico `cenario_corrida_leniencia`.
    seed : int
        Semente do cenário canônico (ignorado se `fluxos` for passado).

    Returns
    -------
    (Figure, Axes)
    """
    aplicar_estilo()
    if fluxos is None:
        fluxos = _executar_cenario_demo(seed=seed)

    sinais = max(1, fluxos["sinais"])
    depositos = max(
        1,
        fluxos.get(
            "depositos",
            fluxos["aberturas"] + fluxos.get("em_escrow", 0) + fluxos.get("expirados", 0),
        ),
    )
    aberturas = fluxos["aberturas"]
    tccs = fluxos["tccs"]
    em_escrow = fluxos.get("em_escrow", 0)
    expirados = fluxos.get("expirados", 0)
    nao_tcc = max(0, aberturas - tccs)

    # Layout: 4 colunas (x = 0, 3, 6, 9), barras verticais
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, sinais * 1.1)
    ax.axis("off")

    # Helper: desenhar uma caixa
    def caixa(x: float, y: float, h: float, label: str, valor: int, cor: str) -> None:
        rect = Rectangle(
            (x, y), 0.8, h, facecolor=cor, edgecolor="black", linewidth=0.6, alpha=0.85
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.4, y + h / 2, str(valor), ha="center", va="center", fontsize=10, fontweight="bold"
        )
        ax.text(x + 0.4, y + h + sinais * 0.025, label, ha="center", va="bottom", fontsize=9)

    # Helper: desenhar fluxo (polígono trapezoidal entre duas alturas)
    def fluxo(
        x1: float,
        y1a: float,
        y1b: float,
        x2: float,
        y2a: float,
        y2b: float,
        cor: str,
        alpha: float = 0.35,
    ) -> None:
        pts = np.array(
            [
                [x1, y1a],
                [x2, y2a],
                [x2, y2b],
                [x1, y1b],
            ]
        )
        poly = Polygon(pts, facecolor=cor, edgecolor="none", alpha=alpha)
        ax.add_patch(poly)

    # Coluna 1: Sinais
    caixa(0, 0, sinais, "Sinais\n(P1/P2)", sinais, PALETA["cade"])

    # Coluna 2: Depósitos (todos os sinais que viraram depósito condicional)
    # Por construção do modelo sob usar_escrow_explicito=True, sinais ⊇ depósitos
    nao_dep = max(0, sinais - depositos)
    caixa(3, 0, depositos, "Depósitos\n(escrow CADE)", depositos, PALETA["B"])
    fluxo(0.8, 0, depositos, 3.0, 0, depositos, PALETA["B"])
    if nao_dep > 0:
        # ramo de sinais que não viraram depósito (rejeitados pelo arquétipo, sob caminho histórico)
        fluxo(
            0.8, depositos, sinais, 3.0, depositos, depositos + nao_dep * 0.05, "grey", alpha=0.15
        )

    # Coluna 3: 3 destinos do depósito (abertura, permanece, expira)
    y_cursor = 0.0
    caixa(6, y_cursor, aberturas, "Aberturas\nsimultâneas", aberturas, PALETA["C"])
    fluxo(3.8, 0, aberturas, 6.0, 0, aberturas, PALETA["C"])
    y_cursor += aberturas + sinais * 0.03

    if em_escrow > 0:
        caixa(
            6,
            y_cursor,
            em_escrow,
            "Em escrow\n(massa crítica não atingida)",
            em_escrow,
            "lightgrey",
        )
        fluxo(
            3.8,
            aberturas,
            aberturas + em_escrow,
            6.0,
            y_cursor,
            y_cursor + em_escrow,
            "lightgrey",
            alpha=0.5,
        )
        y_cursor += em_escrow + sinais * 0.03

    if expirados > 0:
        caixa(6, y_cursor, expirados, "Expirados\n(janela)", expirados, "salmon")
        fluxo(
            3.8,
            aberturas + em_escrow,
            aberturas + em_escrow + expirados,
            6.0,
            y_cursor,
            y_cursor + expirados,
            "salmon",
            alpha=0.5,
        )

    # Coluna 4: 2 destinos das aberturas (TCC assinado, caso sem TCC)
    caixa(9, 0, tccs, "TCCs\nassinados", tccs, PALETA["adv"])
    fluxo(6.8, 0, tccs, 9.0, 0, tccs, PALETA["adv"])
    if nao_tcc > 0:
        caixa(9, tccs + sinais * 0.03, nao_tcc, "Casos sem TCC", nao_tcc, "lightgrey")
        fluxo(
            6.8,
            tccs,
            aberturas,
            9.0,
            tccs + sinais * 0.03,
            tccs + sinais * 0.03 + nao_tcc,
            "lightgrey",
            alpha=0.4,
        )

    ax.set_title(
        f"Fluxo agregado da corrida LCMC — {sinais} sinais → "
        f"{depositos} depósitos → {aberturas} aberturas → {tccs} TCCs",
        fontsize=10,
    )
    fig.tight_layout()
    return fig, ax


if __name__ == "__main__":
    from pathlib import Path

    fig, _ = gerar_figura()
    out = Path("docs/img/11_sankey_corrida_lcmc.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
