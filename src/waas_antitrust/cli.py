"""Interface de linha de comando do projeto."""

from __future__ import annotations

import argparse
from pathlib import Path


def sobol() -> None:
    """Entry point: waas-sobol."""
    parser = argparse.ArgumentParser(
        description="Varredura de Sobol para análise de sensibilidade global do WaaS.",
    )
    parser.add_argument(
        "--n-base",
        type=int,
        default=128,
        help="Número-base de amostras Sobol (128 rápido, 1024 paper-grade).",
    )
    parser.add_argument("--regime", choices=["A", "B", "C"], default="B")
    parser.add_argument("--jobs", type=int, default=-1, help="Núcleos paralelos.")
    parser.add_argument("--n-empresas", type=int, default=15)
    parser.add_argument("--n-tiques", type=int, default=24)
    parser.add_argument("--out", type=Path, default=Path("results/sobol.parquet"))
    args = parser.parse_args()

    from waas_antitrust.sobol import executar_varredura

    print(f"Executando varredura Sobol · regime={args.regime} · n_base={args.n_base}")
    df = executar_varredura(
        n_base=args.n_base,
        regime=args.regime,
        n_jobs=args.jobs,
        n_empresas=args.n_empresas,
        n_tiques=args.n_tiques,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(args.out)
    print(f"Resultados gravados em {args.out} · {len(df)} amostras")


def figuras() -> None:
    """Entry point: waas-figuras."""
    parser = argparse.ArgumentParser(
        description="Gera todas as figuras do artigo para a pasta indicada.",
    )
    parser.add_argument("--out", type=Path, default=Path("figuras/"))
    parser.add_argument("--formato", choices=["png", "svg", "ambos"], default="ambos")
    args = parser.parse_args()

    from waas_antitrust.viz import aplicar_estilo, fase, inversao

    aplicar_estilo()
    args.out.mkdir(parents=True, exist_ok=True)

    figuras_disponiveis = {
        "01_inversao": inversao.gerar_figura,
        "02_fase": fase.gerar_figura,
        # outras viz ainda no caderno; ver docs/DECISIONS.md
    }

    for nome, fn in figuras_disponiveis.items():
        try:
            fig, _ = fn()
            for ext in (["png", "svg"] if args.formato == "ambos" else [args.formato]):
                caminho = args.out / f"{nome}.{ext}"
                fig.savefig(caminho, dpi=150, bbox_inches="tight")
                print(f"  gerada: {caminho}")
        except NotImplementedError as e:
            print(f"  pulada {nome}: {e}")


if __name__ == "__main__":
    import sys

    if sys.argv[1:2] == ["sobol"]:
        sys.argv.pop(1)
        sobol()
    elif sys.argv[1:2] == ["figuras"]:
        sys.argv.pop(1)
        figuras()
    else:
        print("Uso: python -m waas_antitrust.cli [sobol|figuras] ...")
