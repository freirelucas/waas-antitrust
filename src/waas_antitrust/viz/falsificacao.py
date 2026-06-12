"""§8 — Mapa de falsificabilidade: os 5 vetores de quebra executados.

Cada limitação declarada do mecanismo tem um **vetor de quebra**
parametrizável e um **reporter que o detecta** (tabela em
`resultados.md` § "Os vetores de quebra"). Esta figura EXECUTA os
5 vetores contra o baseline (Regime B, defaults adversariais
moderados) e mostra o reporter respectivo disparando:

- **Vetor A** (R15): `D_disc_base_tcc = D_disc` — o TCC clássico já dá
  todo o desconto → `n_firmas_optaram_tcc_classico` sobe.
- **Vetor B** (R15/F6): `p_anulacao_tcc = 1` — Judiciário anula todo
  TCC-WaaS → `n_tcc_anulados` sobe.
- **Vetor C** (R15): `custo_legal_uw` alto — o denunciante racional
  desiste → `n_sinais` cai.
- **Vetor D** (R20/LCMC): `q_min` inalcançável — nenhuma firma atinge
  massa crítica → `n_firmas_atingiram_massa_critica_interna` zera.
- **Vetor E** (R26 Coleman): `alpha_erosao` alto — substrato cooperativo
  seca → `capital_social_residual` colapsa.

Grid 1×5: cada mini-eixo compara baseline × vetor no reporter próprio
(mediana sobre seeds). A honestidade estruturada do Ato 4 em uma figura:
cada fragilidade é um botão que QUEBRA o mecanismo de forma mensurável.
"""

from __future__ import annotations

from dataclasses import replace

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

DEFAULT_SEEDS: tuple[int, ...] = (11, 23, 37)


def _mediana_reporter(
    params: WaaSParametros,
    reporter: str,
    seeds: tuple[int, ...],
    agregacao: str = "final",
) -> float:
    """Mediana de `reporter` sobre as seeds.

    `agregacao="final"` lê o último tique (correto para contadores
    monotônicos `_acum` e estados); `"soma"` soma a série inteira
    (correto para fluxos por tique como `n_sinais` — espelha o critério
    de `tests/test_vetores_quebra.py`).
    """
    valores = []
    for seed in seeds:
        df = WaaSModel(replace(params, seed=seed)).executar()
        serie = df[reporter]
        valores.append(float(serie.sum() if agregacao == "soma" else serie.iloc[-1]))
    return float(np.median(valores))


def gerar_figura(
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    n_tiques: int = 10,
) -> tuple[Figure, list[Axes]]:
    """Grid 1×5: cada vetor de quebra disparando o seu reporter.

    Parameters
    ----------
    seeds : tuple[int, ...]
        Sementes do multi-seed (default 3; mediana).
    n_tiques : int
        Horizonte de cada execução (default 10).

    Returns
    -------
    (Figure, list[Axes])  # 5 eixos
    """
    aplicar_estilo()
    base = WaaSParametros(
        n_empresas=10,
        tam_medio_empresa=100,
        n_tiques=n_tiques,
        regime="B",
        fracao_violadoras=0.6,
        taxa_observacao=0.45,
        D_disc=0.30,
    )
    base_corrida = replace(base, modo_corrida=True, q_min_cooperacao_interna=0.10)

    #: (rótulo, params_baseline, params_vetor, reporter, anotação, agregação)
    vetores = (
        (
            "Vetor A\nD_base = D_total",
            base,
            replace(base, D_disc_base_tcc=0.30),
            "n_firmas_optaram_tcc_classico",
            "firmas no TCC clássico",
            "final",
        ),
        (
            "Vetor B (F6)\np_anulação = 1",
            base,
            replace(base, p_anulacao_tcc=1.0),
            "n_tcc_anulados",
            "TCCs anulados",
            "final",
        ),
        (
            # Critério do teste de regressão: custo 5·w_a derrota qualquer W
            # razoável no racional; sinais somados sobre a série inteira.
            "Vetor C\ncusto legal = 5·w_a",
            base,
            replace(base, custo_legal_uw=5.0),
            "n_sinais",
            "Σ sinais (cai)",
            "soma",
        ),
        (
            "Vetor D (LCMC)\nq_min inalcançável",
            base_corrida,
            replace(base_corrida, q_min_cooperacao_interna=0.90),
            "n_firmas_atingiram_massa_critica_interna",
            "firmas c/ massa crítica",
            "final",
        ),
        (
            "Vetor E (Coleman)\nalpha_erosão = 0,9",
            base,
            replace(base, alpha_erosao=0.9),
            "capital_social_residual",
            "capital social residual",
            "final",
        ),
    )

    fig, axes = plt.subplots(1, 5, figsize=(13, 3.4))
    for ax, (rotulo, p_base, p_vetor, reporter, anotacao, agregacao) in zip(
        axes, vetores, strict=True
    ):
        v_base = _mediana_reporter(p_base, reporter, seeds, agregacao)
        v_vetor = _mediana_reporter(p_vetor, reporter, seeds, agregacao)
        ax.bar(
            [0, 1],
            [v_base, v_vetor],
            color=[PALETA["B"], PALETA["adv"]],
            edgecolor="black",
            linewidth=0.5,
            alpha=0.85,
        )
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["base", "vetor"], fontsize=8)
        ax.set_title(rotulo, fontsize=8)
        ax.set_ylabel(anotacao, fontsize=7)
        ax.tick_params(axis="y", labelsize=7)
        ax.grid(True, axis="y", alpha=0.3)

    fig.suptitle(
        f"Mapa de falsificabilidade — cada vetor de quebra dispara o seu reporter "
        f"(mediana de {len(seeds)} seeds × {n_tiques} tiques, Regime B)",
        fontsize=10,
    )
    fig.tight_layout()
    return fig, list(axes)


if __name__ == "__main__":
    from pathlib import Path

    fig, _ = gerar_figura()
    out = Path("docs/img/16_falsificacao_vetores.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
