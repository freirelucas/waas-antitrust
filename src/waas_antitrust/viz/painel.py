"""§12 — Painel consolidado: a tese em seis células (figura-síntese).

Última figura do backlog T01. Compõe, em grid 2×3, as seis evidências
que estruturam o argumento — alvo: figura única para abstract/divulgação:

- **(A)** Dano acumulado por regime A/B/C (trajetória mediana multi-seed)
  — a ordenação de regimes da Proposição 3.
- **(B)** Detecção percebida `p_perc` por regime — a dissuasão endógena
  (R01) que explica a ordenação.
- **(C)** Fração de firmas com massa crítica interna por tique sob LCMC
  (`modo_corrida`) — a coordenação acontecendo.
- **(D)** Depósitos em escrow e aberturas simultâneas acumuladas por
  tique (`usar_escrow_explicito`) — o canal v3 operando.
- **(E)** Capital social residual com e sem erosão Coleman
  (`alpha_erosao` 0 × 0,5) — a forma fraca da Proposição 5.
- **(F)** Dano final nas 5 variantes institucionais (A, B, C, EUA, UE)
  — a generalidade R28 em uma barra.

Todas as células usam a MESMA população de execuções (config compacta,
multi-seed) — o painel é uma leitura agregada, não um experimento novo.
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

_COR_REGIME = {"A": "A", "B": "B", "C": "C", "EUA": "C", "UE": "A"}


def _executar(params: WaaSParametros, seeds: tuple[int, ...]) -> list:
    """Executa o modelo para cada seed; devolve lista de DataFrames."""
    return [WaaSModel(replace(params, seed=s)).executar() for s in seeds]


def gerar_figura(
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    n_tiques: int = 16,
) -> tuple[Figure, list[Axes]]:
    """Painel-síntese 2×3 da tese completa.

    Parameters
    ----------
    seeds : tuple[int, ...]
        Sementes do multi-seed (default 3; mediana/IQR).
    n_tiques : int
        Horizonte de cada execução (default 16 — 4 anos em trimestres).

    Returns
    -------
    (Figure, list[Axes])  # 6 eixos
    """
    aplicar_estilo()
    base = WaaSParametros(
        n_empresas=10,
        tam_medio_empresa=100,
        n_tiques=n_tiques,
        fracao_violadoras=0.6,
        taxa_observacao=0.45,
    )

    # População de execuções compartilhada entre células.
    dfs_por_regime = {r: _executar(replace(base, regime=r), seeds) for r in ("A", "B", "C")}
    dfs_eua = _executar(replace(base, regime="EUA"), seeds)
    dfs_ue = _executar(replace(base, regime="UE"), seeds)
    dfs_corrida = _executar(
        replace(base, regime="B", modo_corrida=True, usar_escrow_explicito=True), seeds
    )
    dfs_erosao = _executar(replace(base, regime="B", alpha_erosao=0.5), seeds)

    tempo = np.arange(1, n_tiques + 1)
    fig, eixos = plt.subplots(2, 3, figsize=(13.5, 7.2))
    ax_a, ax_b, ax_c = eixos[0]
    ax_d, ax_e, ax_f = eixos[1]

    def _mediana_serie(dfs: list, coluna: str) -> np.ndarray:
        return np.median(np.vstack([d[coluna].to_numpy(dtype=float) for d in dfs]), axis=0)

    # (A) Dano acumulado por regime
    for r in ("A", "B", "C"):
        ax_a.plot(
            tempo,
            _mediana_serie(dfs_por_regime[r], "dano_acumulado"),
            label=f"Regime {r}",
            color=PALETA[r],
        )
    ax_a.set_title("(A) Dano acumulado por regime")
    ax_a.set_ylabel("Dano acumulado")
    ax_a.legend(fontsize=7)
    ax_a.grid(True, alpha=0.3)

    # (B) Violadoras ativas — a consequência observável da dissuasão (R01)
    for r in ("A", "B", "C"):
        ax_b.plot(
            tempo,
            _mediana_serie(dfs_por_regime[r], "n_violadoras_ativas"),
            label=f"Regime {r}",
            color=PALETA[r],
        )
    ax_b.set_title("(B) Violadoras ativas (dissuasão R01)")
    ax_b.set_ylabel("violadoras ativas")
    ax_b.legend(fontsize=7)
    ax_b.grid(True, alpha=0.3)

    # (C) Massa crítica interna sob LCMC
    serie_mc = _mediana_serie(dfs_corrida, "n_firmas_atingiram_massa_critica_interna")
    ax_c.plot(tempo, serie_mc / base.n_empresas, color=PALETA["cade"])
    ax_c.set_title("(C) Fração de firmas c/ massa crítica (LCMC)")
    ax_c.set_ylabel("fração de firmas")
    ax_c.set_ylim(0, 1.05)
    ax_c.grid(True, alpha=0.3)

    # (D) Canal v3: escrow e aberturas
    ax_d.plot(
        tempo,
        _mediana_serie(dfs_corrida, "n_denuncias_em_escrow"),
        label="em escrow",
        color=PALETA["B"],
    )
    ax_d.plot(
        tempo,
        _mediana_serie(dfs_corrida, "n_aberturas_simultaneas_acum"),
        label="aberturas acum.",
        color=PALETA["C"],
    )
    ax_d.set_title("(D) Canal de depósito condicional (R27)")
    ax_d.set_ylabel("denúncias")
    ax_d.set_xlabel("Tique")
    ax_d.legend(fontsize=7)
    ax_d.grid(True, alpha=0.3)

    # (E) Erosão Coleman: capital social com e sem alpha
    ax_e.plot(
        tempo,
        _mediana_serie(dfs_por_regime["B"], "capital_social_residual"),
        label=r"$\alpha = 0$",
        color=PALETA["B"],
    )
    ax_e.plot(
        tempo,
        _mediana_serie(dfs_erosao, "capital_social_residual"),
        label=r"$\alpha = 0{,}5$",
        color=PALETA["adv"],
    )
    ax_e.set_title("(E) Erosão Coleman — forma fraca (R26)")
    ax_e.set_ylabel("capital social residual")
    ax_e.set_xlabel("Tique")
    ax_e.set_ylim(-0.05, 1.1)
    ax_e.legend(fontsize=7)
    ax_e.grid(True, alpha=0.3)

    # (F) Dano final nas 5 variantes institucionais
    variantes = (
        ("A", dfs_por_regime["A"]),
        ("B", dfs_por_regime["B"]),
        ("C", dfs_por_regime["C"]),
        ("EUA", dfs_eua),
        ("UE", dfs_ue),
    )
    medianas = [
        float(np.median([d["dano_acumulado"].iloc[-1] for d in dfs])) for _, dfs in variantes
    ]
    cores = [PALETA[_COR_REGIME[r]] for r, _ in variantes]
    ax_f.bar(
        range(len(variantes)), medianas, color=cores, edgecolor="black", linewidth=0.5, alpha=0.85
    )
    ax_f.set_xticks(range(len(variantes)))
    ax_f.set_xticklabels([r for r, _ in variantes], fontsize=8)
    ax_f.set_title("(F) Dano final — 5 variantes (R28)")
    ax_f.set_ylabel("Dano acumulado (final)")
    ax_f.set_xlabel("Variante institucional")
    ax_f.grid(True, axis="y", alpha=0.3)

    fig.suptitle(
        f"A tese em seis células — mediana de {len(seeds)} seeds × {n_tiques} tiques",
        fontsize=11,
    )
    fig.tight_layout()
    return fig, [ax_a, ax_b, ax_c, ax_d, ax_e, ax_f]


if __name__ == "__main__":
    from pathlib import Path

    fig, _ = gerar_figura()
    out = Path("docs/img/18_painel_sintese.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Gravado: {out}")
