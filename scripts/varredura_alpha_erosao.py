#!/usr/bin/env python
"""Varredura de `alpha_erosao` para estimar o limiar `alpha*` da Proposição 5.

A Proposição 5 candidata (R26 Coleman): existe `alpha_erosao* > 0` tal que,
para `alpha_erosao > alpha*`, o Regime B colapsa em A após N tiques —
"premiar denúncia destrói o substrato cooperativo".

Esta varredura mede, em grade × multi-seed × bootstrap, o **dano relativo**
do Regime B contra o baseline B sem erosão (alpha=0):

    dano_rel(alpha) = dano_acum_B(alpha) / dano_acum_B(0)

Hipótese: dano_rel é monotônica crescente em alpha; o "colapso em A" se
materializa quando dano_rel(alpha) ≈ dano_acum_A / dano_acum_B(0).

Saídas:
- `results/alpha_erosao_grade.parquet`: long DataFrame com (alpha, seed,
  dano_acum, capital_social_residual_final, n_tcc_assinados, regime).
- Stdout: tabela com IC bootstrap por alpha + estimativa de alpha* (cruzamento
  com Regime A).

Calibração mantida frouxa: 10 seeds × 8 alphas × 40 tiques é um trade-off
entre tempo de execução (~3 min em laptop) e estabilidade do bootstrap.
Para a versão paper-grade, elevar `--seeds 30 --tiques 60`.

Uso:
    python scripts/varredura_alpha_erosao.py                  # default
    python scripts/varredura_alpha_erosao.py --seeds 20       # multi-seed maior
    python scripts/varredura_alpha_erosao.py --out custom.parquet
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.robustez import bootstrap_ci

# Defaults justificados:
# - alphas: 0 (baseline) + 7 valores cobrindo o intervalo viz/proposicao_5.py
#   já documentado (0.0, 0.1, 0.3, 0.7) e estendendo para 0.05/0.2/0.5/0.9.
DEFAULT_ALPHAS = (0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9)
DEFAULT_SEEDS = (11, 23, 37, 41, 53, 59, 71, 83, 97, 101)


def executar_uma(
    alpha: float,
    seed: int,
    regime: str,
    n_tiques: int,
    n_empresas: int,
    tam_medio: int,
    fracao_violadoras: float,
    taxa_observacao: float,
) -> dict[str, float]:
    """Executa uma rodada (alpha, seed, regime) e devolve métricas finais."""
    params = WaaSParametros(
        n_empresas=n_empresas,
        tam_medio_empresa=tam_medio,
        n_tiques=n_tiques,
        seed=seed,
        regime=regime,
        fracao_violadoras=fracao_violadoras,
        taxa_observacao=taxa_observacao,
        alpha_erosao=alpha if regime != "A" else 0.0,
    )
    df = WaaSModel(params).executar()
    ultima = df.iloc[-1]
    return {
        "alpha_erosao": alpha,
        "seed": seed,
        "regime": regime,
        "dano_acumulado": float(ultima["dano_acumulado"]),
        "capital_social_residual": float(ultima["capital_social_residual"]),
        "n_tcc_assinados": int(ultima.get("n_tcc_assinados", 0)),
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--alphas", type=float, nargs="+", default=list(DEFAULT_ALPHAS))
    ap.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    ap.add_argument("--tiques", type=int, default=40)
    ap.add_argument("--n-empresas", type=int, default=15)
    ap.add_argument("--tam-medio", type=int, default=200)
    ap.add_argument("--fracao-violadoras", type=float, default=0.5)
    ap.add_argument("--taxa-observacao", type=float, default=0.4)
    ap.add_argument("--out", type=str, default="results/alpha_erosao_grade.parquet")
    args = ap.parse_args()

    print(
        f"Varredura: {len(args.alphas)} alphas × {len(args.seeds)} seeds × "
        f"2 regimes (A baseline + B varrendo) × {args.tiques} tiques"
    )

    registros: list[dict[str, float]] = []
    # Regime A baseline (alpha não aplica) — uma curva por seed para piso de referência.
    for seed in args.seeds:
        registros.append(
            executar_uma(
                alpha=0.0,
                seed=seed,
                regime="A",
                n_tiques=args.tiques,
                n_empresas=args.n_empresas,
                tam_medio=args.tam_medio,
                fracao_violadoras=args.fracao_violadoras,
                taxa_observacao=args.taxa_observacao,
            )
        )
    # Regime B varrendo alpha.
    for alpha in args.alphas:
        for seed in args.seeds:
            registros.append(
                executar_uma(
                    alpha=alpha,
                    seed=seed,
                    regime="B",
                    n_tiques=args.tiques,
                    n_empresas=args.n_empresas,
                    tam_medio=args.tam_medio,
                    fracao_violadoras=args.fracao_violadoras,
                    taxa_observacao=args.taxa_observacao,
                )
            )

    df = pd.DataFrame(registros)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    print(f"Gravado: {out} ({len(df)} linhas)")

    # Sumário com bootstrap CI 95%.
    print("\nSumário: dano_acumulado por (regime, alpha) com IC bootstrap 95%")
    print(f"{'regime':<8} {'alpha':>6} {'mediana':>12} {'IC inf':>12} {'IC sup':>12}")
    danos_a = df[df["regime"] == "A"]["dano_acumulado"].to_list()
    ic_a = bootstrap_ci(danos_a, n_bootstrap=1000, seed=0)
    print(f"{'A':<8} {'-':>6} {ic_a.mediana:>12.2f} {ic_a.inferior:>12.2f} {ic_a.superior:>12.2f}")
    medianas_b: dict[float, float] = {}
    for alpha in args.alphas:
        danos = df[(df["regime"] == "B") & (df["alpha_erosao"] == alpha)][
            "dano_acumulado"
        ].to_list()
        ic = bootstrap_ci(danos, n_bootstrap=1000, seed=int(alpha * 1000))
        medianas_b[alpha] = ic.mediana
        print(
            f"{'B':<8} {alpha:>6.2f} {ic.mediana:>12.2f} {ic.inferior:>12.2f} {ic.superior:>12.2f}"
        )

    # Estimativa frouxa de alpha*: maior alpha em que mediana_B(alpha) < mediana_A.
    baseline_a = ic_a.mediana
    alphas_ordenados = sorted(medianas_b.keys())
    alpha_estrela = None
    for alpha in alphas_ordenados:
        if medianas_b[alpha] >= baseline_a:
            alpha_estrela = alpha
            break
    if alpha_estrela is None:
        print(
            f"\nLimiar alpha* não atravessado na grade — Regime B segue dominante "
            f"até alpha={alphas_ordenados[-1]} (dano_B = {medianas_b[alphas_ordenados[-1]]:.2f} "
            f"vs dano_A = {baseline_a:.2f})."
        )
    else:
        print(
            f"\nEstimativa frouxa de alpha*: ~{alpha_estrela:.2f} "
            f"(mediana_B({alpha_estrela}) = {medianas_b[alpha_estrela]:.2f} ≥ mediana_A = {baseline_a:.2f}). "
            f"Calibração rigorosa exige grade mais fina em torno deste ponto."
        )


if __name__ == "__main__":
    main()
