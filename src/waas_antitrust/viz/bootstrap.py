"""§10 — Intervalos de confiança multi-seed por regime (bootstrap).

Fecha o loop entre a infraestrutura de robustez (`robustez.bootstrap_ci` +
`varredura_multi_seed`) e a apresentação: painel 1×2 com mediana + IC 95%
(reamostragem bootstrap) de duas métricas finais por regime A/B/C:

- **(A)** `dano_acumulado` — quanto dano social cada regime permite.
- **(B)** `bem_estar` — computado por `sobol.execucao.calcular_bem_estar`
  a partir dos reporters acumulados (dano, FP, custo de recompensa,
  custo de êxodo, multa arrecadada).

Cada barra usa N seeds (default 12); o erro é o IC bootstrap percentílico
da mediana — a mesma técnica dos testes de robustez multi-seed.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.robustez import bootstrap_ci
from waas_antitrust.sobol.execucao import calcular_bem_estar
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

DEFAULT_SEEDS: tuple[int, ...] = (11, 23, 37, 41, 53, 59, 71, 83, 97, 101, 113, 127)


def _metricas_finais(regime: str, seed: int, n_tiques: int) -> tuple[float, float]:
    """Roda o modelo e devolve (dano_acumulado, bem_estar) finais."""
    params = WaaSParametros(
        n_empresas=15,
        tam_medio_empresa=150,
        n_tiques=n_tiques,
        seed=seed,
        regime=regime,
        fracao_violadoras=0.5,
        taxa_observacao=0.4,
    )
    df = WaaSModel(params).executar()
    ultima = df.iloc[-1]
    dano = float(ultima["dano_acumulado"])
    bem_estar = calcular_bem_estar(
        dano=dano,
        fp=int(ultima["falsos_positivos_acum"]),
        custo_recompensa=float(ultima["custo_recompensa_acum"]),
        w_a_base=params.w_a_base,
        custo_exodo=float(ultima["custo_exodo_acum"]),
        multa_arrecadada=float(ultima["multa_arrecadada_acum"]),
    )
    return dano, bem_estar


def gerar_figura(
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    n_tiques: int = 20,
) -> tuple[Figure, list[Axes]]:
    """Painel 1×2: dano acumulado e bem-estar por regime, com IC bootstrap 95%.

    Parameters
    ----------
    seeds : tuple[int, ...]
        Sementes para o multi-seed (default 12 seeds).
    n_tiques : int
        Horizonte de cada execução (default 20 — 5 anos em trimestres).

    Returns
    -------
    (Figure, [Axes, Axes])
    """
    aplicar_estilo()
    regimes = ("A", "B", "C")

    danos: dict[str, list[float]] = {r: [] for r in regimes}
    bens: dict[str, list[float]] = {r: [] for r in regimes}
    for regime in regimes:
        for seed in seeds:
            dano, bem = _metricas_finais(regime, seed, n_tiques)
            danos[regime].append(dano)
            bens[regime].append(bem)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    ax_a, ax_b = axes[0], axes[1]

    for ax, dados, titulo, ylabel in (
        (ax_a, danos, "(A) Dano acumulado", "Dano acumulado (final)"),
        (ax_b, bens, "(B) Bem-estar social", "Bem-estar (unidades de $w_a$)"),
    ):
        posicoes = range(len(regimes))
        medianas = []
        erros_inf = []
        erros_sup = []
        cores = []
        for regime in regimes:
            ic = bootstrap_ci(dados[regime], n_bootstrap=2000, seed=hash(regime) % 1000)
            medianas.append(ic.mediana)
            erros_inf.append(ic.mediana - ic.inferior)
            erros_sup.append(ic.superior - ic.mediana)
            cores.append(PALETA[regime])
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
        ax.set_xticklabels([f"Regime {r}" for r in regimes])
        ax.set_ylabel(ylabel)
        ax.set_title(titulo)
        ax.grid(True, axis="y", alpha=0.3)

    fig.suptitle(
        f"Mediana + IC bootstrap 95% sobre {len(seeds)} seeds × {n_tiques} tiques",
        fontsize=10,
    )
    fig.tight_layout()
    return fig, [ax_a, ax_b]


if __name__ == "__main__":
    from pathlib import Path

    fig, _ = gerar_figura()
    out = Path("docs/img/12_bootstrap_regimes.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
