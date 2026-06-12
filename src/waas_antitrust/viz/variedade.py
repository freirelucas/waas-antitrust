"""§6 — Amplificação de variedade ashbiana por distribuição de papéis.

Lê a tese cibernética do mecanismo (Ashby 1956; Conant-Ashby 1970): o
regulador clássico tem variedade insuficiente para os estados internos
da firma digital; o WaaS **amplifica variedade** recrutando os sensores
internos — os trabalhadores, cuja observabilidade depende do papel
(gradiente 3-níveis Near & Miceli em `condutas.py`).

A figura varre os dois presets de distribuição de papéis e mede a
consequência observável da variedade: sinais e detecção em multi-seed.

- **`BIGTECH_MADURA`** (default): engenharia-pesada (30% eng).
- **`MARKETPLACE_BR`** (E05): operações-pesada (25% operações, 15%
  comercial) — perfil iFood/Mercado Livre.

Painel 1×2: (A) Σ sinais por preset (mediana + IQR); (B) verdadeiros
positivos acumulados. Se a distribuição de papéis importa para a
variedade efetiva, os dois presets divergem — e a divergência é a
justificativa empírica do item E05 (calibrar distribuição contra
organogramas reais).
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.condutas import BIGTECH_MADURA, MARKETPLACE_BR
from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

DEFAULT_SEEDS: tuple[int, ...] = (11, 23, 37, 41, 53)

PRESETS: tuple[tuple[str, dict[str, float] | None, str], ...] = (
    ("BIGTECH_MADURA\n(30% eng)", BIGTECH_MADURA, "B"),
    ("MARKETPLACE_BR\n(25% operações)", MARKETPLACE_BR, "C"),
)


def gerar_figura(
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    n_tiques: int = 12,
) -> tuple[Figure, list[Axes]]:
    """Painel 1×2 da variedade efetiva por preset de distribuição de papéis.

    Parameters
    ----------
    seeds : tuple[int, ...]
        Sementes do multi-seed (default 5).
    n_tiques : int
        Horizonte de cada execução (default 12).

    Returns
    -------
    (Figure, [Axes, Axes])
    """
    aplicar_estilo()

    sinais: dict[str, list[float]] = {}
    vps: dict[str, list[float]] = {}
    for rotulo, preset, _ in PRESETS:
        s_list: list[float] = []
        v_list: list[float] = []
        for seed in seeds:
            params = WaaSParametros(
                n_empresas=10,
                tam_medio_empresa=120,
                n_tiques=n_tiques,
                seed=seed,
                regime="B",
                fracao_violadoras=0.6,
                taxa_observacao=0.45,
                distribuicao_papeis=preset,
            )
            df = WaaSModel(params).executar()
            s_list.append(float(df["n_sinais"].sum()))
            v_list.append(float(df["verdadeiros_positivos_acum"].iloc[-1]))
        sinais[rotulo] = s_list
        vps[rotulo] = v_list

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.0))
    ax_a, ax_b = axes[0], axes[1]

    for ax, dados, titulo, ylabel in (
        (ax_a, sinais, "(A) Σ sinais no horizonte", "Σ sinais"),
        (ax_b, vps, "(B) Verdadeiros positivos acumulados", "VP acumulados (final)"),
    ):
        posicoes = range(len(PRESETS))
        medianas = []
        erros_inf = []
        erros_sup = []
        cores = []
        rotulos = []
        for rotulo, _, cor_key in PRESETS:
            arr = np.asarray(dados[rotulo])
            med = float(np.median(arr))
            medianas.append(med)
            erros_inf.append(med - float(np.quantile(arr, 0.25)))
            erros_sup.append(float(np.quantile(arr, 0.75)) - med)
            cores.append(PALETA[cor_key])
            rotulos.append(rotulo)
        ax.bar(
            posicoes,
            medianas,
            yerr=[erros_inf, erros_sup],
            color=cores,
            alpha=0.85,
            capsize=6,
            edgecolor="black",
            linewidth=0.5,
        )
        ax.set_xticks(list(posicoes))
        ax.set_xticklabels(rotulos, fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(titulo)
        ax.grid(True, axis="y", alpha=0.3)

    fig.suptitle(
        f"Variedade efetiva por distribuição de papéis (Ashby/Near-Miceli) — "
        f"mediana + IQR, {len(seeds)} seeds × {n_tiques} tiques, Regime B",
        fontsize=10,
    )
    fig.tight_layout()
    return fig, [ax_a, ax_b]


if __name__ == "__main__":
    from pathlib import Path

    fig, _ = gerar_figura()
    out = Path("docs/img/17_variedade_papeis.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
