"""Painel macro — telas de simulação agregadas (v2.H, Designer + PM).

Atende ao pedido recorrente do autor por **telas de simulação de parâmetros
e crenças a respeito do micro e do macro comportamento das classes de
agentes**. Esta peça é o lado *macro*: trajetórias agregadas que mostram
o comportamento de sistema ao longo do tempo.

Estrutura: painel 2×2 matplotlib que combina:
  (a) detecção percebida `p_perc` global — sinal Schelling
  (b) firmas atingiram massa crítica interna (LCMC, R20)
  (c) bem-estar substantivo cumulativo
  (d) capital social residual (R26 Coleman) — sob risco de erosão

A função `gerar_figura(df)` aceita um DataFrame de modelo já executado
para evitar acoplamento ao seed específico — pode ser chamada com
qualquer execução.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def gerar_figura(df: pd.DataFrame | None = None) -> tuple[Figure, list[Axes]]:
    """Painel macro 2×2 a partir de um DataFrame de execução do `WaaSModel`.

    Parameters
    ----------
    df : pd.DataFrame | None
        DataFrame retornado por `WaaSModel.executar()`. Se None, executa
        um cenário canônico (Regime B + R20 modo_corrida + alpha_erosao=0.2).

    Returns
    -------
    (Figure, list[Axes])
        Painel 2×2 (4 axes na ordem: detecção, massa crítica, bem-estar,
        capital social).
    """
    aplicar_estilo()

    if df is None:
        # Cenário canônico para demonstração da tela macro.
        from waas_antitrust.model import WaaSModel, WaaSParametros

        m = WaaSModel(
            WaaSParametros(
                n_empresas=10,
                tam_medio_empresa=150,
                n_tiques=20,
                seed=37,
                regime="B",
                fracao_violadoras=0.7,
                taxa_observacao=0.5,
                alpha_erosao=0.2,
                modo_corrida=True,
            )
        )
        df = m.executar()

    fig, axes = plt.subplots(2, 2, figsize=(10, 6.5))
    ax_p, ax_mc, ax_bs, ax_cs = axes.flatten()

    tiques = df.index.to_numpy()

    # (a) Detecção percebida global (sinal Schelling).
    if "p_perc" in df.columns:
        ax_p.plot(tiques, df["p_perc"], color=PALETA["B"], lw=2.0)
    else:
        # Reporter `p_perc` não foi exposto historicamente; usa proxy.
        ax_p.text(0.5, 0.5, "p_perc não disponível", ha="center", va="center")
    ax_p.set_title("(a) Detecção percebida global", fontsize=10, loc="left")
    ax_p.set_xlabel("Tique")
    ax_p.set_ylabel("$p_{perc}$")
    ax_p.set_ylim(0, 1.0)
    ax_p.grid(True, alpha=0.25, linestyle=":")

    # (b) Firmas que atingiram massa crítica interna (LCMC R20).
    col_mc = "n_firmas_atingiram_massa_critica_interna"
    if col_mc in df.columns:
        ax_mc.plot(tiques, df[col_mc], color=PALETA["C"], lw=2.0, drawstyle="steps-post")
    else:
        ax_mc.plot(tiques, df.get("n_empresas_notif", [0] * len(tiques)), color=PALETA["C"])
    ax_mc.set_title("(b) Firmas com massa crítica interna", fontsize=10, loc="left")
    ax_mc.set_xlabel("Tique")
    ax_mc.set_ylabel("contagem cumulativa")
    ax_mc.grid(True, alpha=0.25, linestyle=":")

    # (c) Bem-estar substantivo cumulativo (negativo do custo social).
    if "bem_estar" in df.columns:
        ax_bs.plot(tiques, df["bem_estar"], color=PALETA["destaque"], lw=2.0)
        ax_bs.axhline(0, color=PALETA["neutro_escuro"], ls=":", lw=0.7, alpha=0.5)
    else:
        ax_bs.text(0.5, 0.5, "bem_estar não disponível", ha="center", va="center")
    ax_bs.set_title("(c) Bem-estar substantivo", fontsize=10, loc="left")
    ax_bs.set_xlabel("Tique")
    ax_bs.set_ylabel("bem-estar (unidades de $w_a$)")
    ax_bs.grid(True, alpha=0.25, linestyle=":")

    # (d) Capital social residual (R26 Coleman).
    if "capital_social_residual" in df.columns:
        ax_cs.plot(tiques, df["capital_social_residual"], color=PALETA["adv"], lw=2.0)
        ax_cs.axhline(0.5, color=PALETA["neutro_escuro"], ls=":", lw=0.9, alpha=0.5)
        ax_cs.set_ylim(0, 1.05)
    else:
        ax_cs.text(0.5, 0.5, "capital_social_residual\nnão disponível", ha="center", va="center")
    ax_cs.set_title("(d) Capital social residual (Coleman)", fontsize=10, loc="left")
    ax_cs.set_xlabel("Tique")
    ax_cs.set_ylabel("capital social [0, 1]")
    ax_cs.grid(True, alpha=0.25, linestyle=":")

    fig.suptitle(
        "Painel macro — comportamento do sistema sob reframe v2",
        fontsize=12,
        y=0.995,
    )
    fig.tight_layout()
    return fig, [ax_p, ax_mc, ax_bs, ax_cs]
