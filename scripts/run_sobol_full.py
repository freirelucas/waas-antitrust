#!/usr/bin/env python
"""Executa a varredura completa de Sobol em modo assíncrono.

Para a versão definitiva do artigo, use:
    python scripts/run_sobol_full.py --n-base 1024 --jobs -1 --out results/sobol_full.parquet

Tempo previsto: 2 a 8 horas dependendo do número de núcleos.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from waas_antitrust.sobol import executar_varredura
from waas_antitrust.sobol.analise import calcular_indices_replicado, identificar_regiao_robusta
from waas_antitrust.sobol.problema import PROBLEMA_SOBOL_8D


def principal():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-base", type=int, default=128)
    parser.add_argument("--regime", choices=["A", "B", "C"], default="B")
    parser.add_argument("--jobs", type=int, default=-1)
    parser.add_argument("--n-empresas", type=int, default=15)
    parser.add_argument("--n-tiques", type=int, default=24)
    parser.add_argument("--n-replicas", type=int, default=5)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    print("=== Varredura Sobol ===")
    print(f"  n_base    : {args.n_base}")
    print(f"  n_replicas: {args.n_replicas}")
    print(f"  regime    : {args.regime}")
    print(f"  núcleos   : {args.jobs}")
    print(f"  n_empresas: {args.n_empresas}")
    print(f"  n_tiques  : {args.n_tiques}")
    print(f"  saída     : {args.out}")
    print()

    inicio = time.time()
    df = executar_varredura(
        n_base=args.n_base,
        regime=args.regime,
        n_jobs=args.jobs,
        n_empresas=args.n_empresas,
        n_tiques=args.n_tiques,
        n_replicas=args.n_replicas,
    )
    elapsed = time.time() - inicio
    print(f"\nVarredura concluída em {elapsed/60:.1f} minutos · {len(df)} amostras")

    # Persiste resultados brutos
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(args.out)
    print(f"Resultados brutos: {args.out}")

    # Calcula índices Sobol e região robusta (tolerante a resultados constantes)
    try:
        indices = calcular_indices_replicado(df, PROBLEMA_SOBOL_8D)
        indices.to_csv(args.out.with_suffix(".indices.csv"), index=False)
        print(f"Índices Sobol: {args.out.with_suffix('.indices.csv')}")
        print()
        print(indices.to_string(index=False, float_format=lambda x: f"{x:7.3f}"))
    except (ValueError, RuntimeError) as e:
        print(
            f"AVISO: cálculo de índices Sobol falhou (provavelmente n_base muito "
            f"pequeno produziu resultados constantes): {e}"
        )
        print("Eleve --n-base para >= 32 e tente novamente.")

    regiao = identificar_regiao_robusta(df)
    fracao = regiao["robusta"].mean()
    print(f"\nFração robusta: {fracao*100:.1f}% ({regiao['robusta'].sum()}/{len(regiao)})")
    regiao.to_parquet(args.out.with_suffix(".regiao.parquet"))


if __name__ == "__main__":
    principal()
