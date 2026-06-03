#!/usr/bin/env python
"""Calibração ingênua de R03 — primeira ponta.

Varre grid sobre `taxa_observacao`, `taxa_falso_reporte` e `rho` para
minimizar erro relativo contra três alvos do ODD:

- **Alvo 1**: ~5 leniências/ano (comunicado CADE 06/10/2023).
- **Alvo 2**: ~47 TCCs/ano (Saito 2021, média 2012-2019).
- **Alvo 3**: 19% das fraudes corporativas descobertas por funcionários
  (Dyck-Morse-Zingales 2010).

A função objetiva é o erro quadrático relativo médio. Esta é uma
calibração **ingênua**: não há identificação formal, intervalos de
confiança nem teste de overfitting. Serve como ponto de partida para
R03; a calibração definitiva exigirá:

- Bootstrap sobre seeds (já temos `robustez.bootstrap_ci`);
- Identificação de quais parâmetros são identificáveis pelos alvos;
- Substituição da grid por SALib/scipy.optimize.

Uso:
    python scripts/calibrar.py                        # grid pequena
    python scripts/calibrar.py --grid 5               # grid mais fina
    python scripts/calibrar.py --seeds 1 7 13         # multi-seed

Saída: imprime ranking dos top-5 conjuntos de parâmetros + score.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import asdict, dataclass

import numpy as np

from waas_antitrust.model import WaaSModel, WaaSParametros

# Alvos do ODD (verbatim das fontes primárias).
ALVO_LENIENCIAS_ANUAIS = 5.0  # comunicado CADE 06/10/2023
ALVO_TCC_ANUAL = 47.0  # Saito 2021
ALVO_FRACAO_VP_INTERNAS = 0.19  # Dyck-Morse-Zingales 2010


@dataclass(frozen=True)
class CombinacaoParam:
    taxa_observacao: float
    taxa_falso_reporte: float
    rho: float


@dataclass(frozen=True)
class ResultadoCalibracao:
    parametros: CombinacaoParam
    score: float
    leniencias_anuais: float
    tcc_anual: float
    fracao_vp_internas: float


def _executar_ponto(p: CombinacaoParam, seed: int) -> ResultadoCalibracao:
    params = WaaSParametros(
        n_empresas=20,
        tam_medio_empresa=200,
        n_tiques=40,  # 10 anos em trimestres
        regime="B",
        seed=seed,
        taxa_observacao=p.taxa_observacao,
        taxa_falso_reporte=p.taxa_falso_reporte,
        rho=p.rho,
    )
    modelo = WaaSModel(params)
    df = modelo.executar()
    # 40 tiques = 10 anos; normalizar para anuais.
    n_anos = params.n_tiques / 4.0
    leniencias_anuais = float(df["n_tcc_assinados"].iloc[-1]) / n_anos
    tcc_anual = float(df["n_tcc_assinados"].iloc[-1]) / n_anos
    vp_total = int(df["verdadeiros_positivos_acum"].iloc[-1])
    fn_total = int(df["falsos_negativos_acum"].iloc[-1])
    fracao_vp_internas = vp_total / max(1, vp_total + fn_total)
    score = (
        ((leniencias_anuais - ALVO_LENIENCIAS_ANUAIS) / ALVO_LENIENCIAS_ANUAIS) ** 2
        + ((tcc_anual - ALVO_TCC_ANUAL) / ALVO_TCC_ANUAL) ** 2
        + ((fracao_vp_internas - ALVO_FRACAO_VP_INTERNAS) / ALVO_FRACAO_VP_INTERNAS) ** 2
    )
    return ResultadoCalibracao(
        parametros=p,
        score=float(score),
        leniencias_anuais=leniencias_anuais,
        tcc_anual=tcc_anual,
        fracao_vp_internas=fracao_vp_internas,
    )


def calibrar(grid_size: int, seeds: list[int]) -> list[ResultadoCalibracao]:
    """Varre a grid e retorna os top-5 pontos pelo erro médio (sobre seeds)."""
    grid_taxa_obs = np.linspace(0.10, 0.50, grid_size).tolist()
    grid_falso = np.linspace(0.005, 0.05, grid_size).tolist()
    grid_rho = np.linspace(0.55, 0.85, grid_size).tolist()
    candidatos: list[ResultadoCalibracao] = []
    for to, fr, rh in itertools.product(grid_taxa_obs, grid_falso, grid_rho):
        p = CombinacaoParam(taxa_observacao=to, taxa_falso_reporte=fr, rho=rh)
        resultados = [_executar_ponto(p, s) for s in seeds]
        score_medio = float(np.mean([r.score for r in resultados]))
        media = ResultadoCalibracao(
            parametros=p,
            score=score_medio,
            leniencias_anuais=float(np.mean([r.leniencias_anuais for r in resultados])),
            tcc_anual=float(np.mean([r.tcc_anual for r in resultados])),
            fracao_vp_internas=float(np.mean([r.fracao_vp_internas for r in resultados])),
        )
        candidatos.append(media)
    candidatos.sort(key=lambda r: r.score)
    return candidatos[:5]


def principal() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid", type=int, default=3, help="pontos por eixo")
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[11, 23, 37],
        help="seeds para multi-seed averaging",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="imprime resultado em JSON (top-5)",
    )
    args = parser.parse_args()

    print(
        f"Calibração ingênua (R03 — primeira ponta). "
        f"Grid {args.grid}³ = {args.grid**3} pontos × {len(args.seeds)} seeds.\n"
        f"Alvos: leniências={ALVO_LENIENCIAS_ANUAIS:.0f}/ano, "
        f"TCC={ALVO_TCC_ANUAL:.0f}/ano, fração VP internas={ALVO_FRACAO_VP_INTERNAS:.0%}.\n"
    )
    top5 = calibrar(grid_size=args.grid, seeds=args.seeds)

    if args.json:
        print(json.dumps([asdict(r) for r in top5], indent=2, ensure_ascii=False))
        return

    print(
        f"{'rank':<5}{'score':>10}{'taxa_obs':>10}{'falso':>10}{'rho':>8}"
        f"{'len/ano':>10}{'tcc/ano':>10}{'frac_int':>10}"
    )
    for i, r in enumerate(top5, start=1):
        print(
            f"{i:<5}{r.score:>10.4f}"
            f"{r.parametros.taxa_observacao:>10.3f}"
            f"{r.parametros.taxa_falso_reporte:>10.4f}"
            f"{r.parametros.rho:>8.3f}"
            f"{r.leniencias_anuais:>10.2f}"
            f"{r.tcc_anual:>10.2f}"
            f"{r.fracao_vp_internas:>10.2%}"
        )


if __name__ == "__main__":
    principal()
