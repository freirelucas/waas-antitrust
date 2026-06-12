"""§7 — Cenários adversariais: uso oportunista do canal (R24).

Varre a fração de trabalhadores com arquétipo `oportunista` (utilidade
extrativa: insider acionista, concorrente plantando informante, chantagem
pré-rescisão, hedge fund ativista) e mede o custo sistêmico em multi-seed:

- **(A)** Falsos positivos acumulados por fração de oportunistas
  (mediana + banda interquartílica) — o canal vira vetor de assédio?
- **(B)** Dano acumulado — o ruído adversarial compromete a dissuasão?

Calibração da fração: Dyck-Morse-Zingales (2010) reportam ~17% de
motivação financeira direta em denúncias à SEC; a varredura cobre
0% a 30% (o cenário canônico `uso_adversarial_oportunista` usa 20%
como limite superior).

A distribuição de arquétipos é renormalizada a cada ponto: a fração
oportunista cresce comprimindo proporcionalmente os demais arquétipos
do preset `DISTRIBUICAO_COM_OPORTUNISTAS`.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

DEFAULT_SEEDS: tuple[int, ...] = (11, 23, 37, 41, 53)
DEFAULT_FRACOES: tuple[float, ...] = (0.0, 0.05, 0.10, 0.20, 0.30)

#: Núcleo de arquétipos não-oportunistas (proporções relativas entre si);
#: renormalizado para (1 − fração_oportunista) em cada ponto da varredura.
_NUCLEO_SEM_OPORTUNISTA: dict[str, float] = {
    "ético": 0.10,
    "imitativo": 0.30,
    "racional": 0.30,
    "fairminded": 0.10,
    "aleatório": 0.20,
}


def _distribuicao_com(fracao_oportunista: float) -> dict[str, float]:
    """Distribuição de arquétipos com a fração oportunista pedida."""
    resto = 1.0 - fracao_oportunista
    dist = {k: v * resto for k, v in _NUCLEO_SEM_OPORTUNISTA.items()}
    dist["oportunista"] = fracao_oportunista
    return dist


def gerar_figura(
    fracoes: tuple[float, ...] = DEFAULT_FRACOES,
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    n_tiques: int = 12,
) -> tuple[Figure, list[Axes]]:
    """Painel 1×2 do custo sistêmico do uso adversarial, multi-seed.

    Parameters
    ----------
    fracoes : tuple[float, ...]
        Frações de oportunistas a varrer (default 0% a 30%).
    seeds : tuple[int, ...]
        Sementes do multi-seed (default 5).
    n_tiques : int
        Horizonte de cada execução (default 12 — 3 anos em trimestres).

    Returns
    -------
    (Figure, [Axes, Axes])
    """
    aplicar_estilo()

    fp_por_fracao: list[np.ndarray] = []
    dano_por_fracao: list[np.ndarray] = []
    for fr in fracoes:
        fps = []
        danos = []
        for seed in seeds:
            params = WaaSParametros(
                n_empresas=10,
                tam_medio_empresa=100,
                n_tiques=n_tiques,
                seed=seed,
                regime="B",
                fracao_violadoras=0.5,
                taxa_observacao=0.4,
                taxa_falso_reporte=0.05,
                distribuicao_arquetipos=_distribuicao_com(fr) if fr > 0 else None,
            )
            df = WaaSModel(params).executar()
            fps.append(float(df["falsos_positivos_acum"].iloc[-1]))
            danos.append(float(df["dano_acumulado"].iloc[-1]))
        fp_por_fracao.append(np.asarray(fps))
        dano_por_fracao.append(np.asarray(danos))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    ax_a, ax_b = axes[0], axes[1]

    xs = [f * 100 for f in fracoes]
    for ax, dados, titulo, ylabel, cor in (
        (
            ax_a,
            fp_por_fracao,
            "(A) Falsos positivos acumulados",
            "FP acumulados (final)",
            PALETA["adv"],
        ),
        (ax_b, dano_por_fracao, "(B) Dano acumulado", "Dano acumulado (final)", PALETA["B"]),
    ):
        medianas = [float(np.median(d)) for d in dados]
        q25 = [float(np.quantile(d, 0.25)) for d in dados]
        q75 = [float(np.quantile(d, 0.75)) for d in dados]
        ax.fill_between(xs, q25, q75, color=cor, alpha=0.18)
        ax.plot(xs, medianas, marker="o", color=cor)
        ax.axvline(17, color="grey", linestyle=":", alpha=0.7)
        ax.annotate("DMZ 2010\n(~17% SEC)", (17, max(q75) * 0.92), fontsize=7, ha="left")
        ax.set_xlabel("Fração de oportunistas (%)")
        ax.set_ylabel(ylabel)
        ax.set_title(titulo)
        ax.grid(True, alpha=0.3)

    fig.suptitle(
        f"Uso adversarial do canal (R24) — mediana e banda interquartílica, "
        f"{len(seeds)} seeds × {n_tiques} tiques, Regime B",
        fontsize=10,
    )
    fig.tight_layout()
    return fig, [ax_a, ax_b]


if __name__ == "__main__":
    from pathlib import Path

    fig, _ = gerar_figura()
    out = Path("docs/img/15_adversarial_oportunistas.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
