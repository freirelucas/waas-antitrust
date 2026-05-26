"""Interface de linha de comando do projeto."""

from __future__ import annotations

import argparse
from pathlib import Path


def sobol() -> None:
    """Entry point: waas-sobol."""
    parser = argparse.ArgumentParser(
        description="Varredura de Sobol (replicada) para análise de sensibilidade global do WaaS.",
    )
    parser.add_argument(
        "--n-base",
        type=int,
        default=128,
        help="Número-base N. Total de execuções = N·(2d+2)·n_replicas "
        "(128 para validação; 1024 paper-grade).",
    )
    parser.add_argument(
        "--n-replicas",
        type=int,
        default=5,
        help="Réplicas da matriz inteira (seeds distintas), mediadas nos índices. Padrão: 5.",
    )
    parser.add_argument(
        "--regime", choices=["A", "B", "C"], default="B", help="Regime institucional. Padrão: B."
    )
    parser.add_argument(
        "--jobs", type=int, default=-1, help="Processos paralelos (-1 = todos os núcleos)."
    )
    parser.add_argument(
        "--n-empresas", type=int, default=15, help="Empresas por execução. Padrão: 15."
    )
    parser.add_argument(
        "--n-tiques", type=int, default=24, help="Horizonte em trimestres. Padrão: 24."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/sobol.parquet"),
        help="Arquivo Parquet de saída. Padrão: results/sobol.parquet.",
    )
    args = parser.parse_args()

    from waas_antitrust.sobol import executar_varredura

    print(
        f"Executando varredura Sobol · regime={args.regime} · "
        f"n_base={args.n_base} · n_replicas={args.n_replicas}"
    )
    df = executar_varredura(
        n_base=args.n_base,
        regime=args.regime,
        n_jobs=args.jobs,
        n_empresas=args.n_empresas,
        n_tiques=args.n_tiques,
        n_replicas=args.n_replicas,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(args.out)
    print(f"Resultados gravados em {args.out} · {len(df)} amostras")


def figuras() -> None:
    """Entry point: waas-figuras."""
    parser = argparse.ArgumentParser(
        description="Gera as figuras implementadas como módulo "
        "(inversão e fase; as demais estão no caderno).",
    )
    parser.add_argument(
        "--out", type=Path, default=Path("figuras/"), help="Pasta de saída. Padrão: figuras/."
    )
    parser.add_argument(
        "--formato",
        choices=["png", "svg", "pdf", "ambos", "todos"],
        default="ambos",
        help="Formato(s): 'ambos' = png+svg; 'todos' = png+svg+pdf. Padrão: ambos.",
    )
    args = parser.parse_args()

    from waas_antitrust.viz import aplicar_estilo, fase, inversao

    aplicar_estilo()
    args.out.mkdir(parents=True, exist_ok=True)

    figuras_disponiveis = {
        "01_inversao": inversao.gerar_figura,
        "02_fase": fase.gerar_figura,
        # outras viz ainda no caderno; ver docs/DECISIONS.md
    }

    formatos = {"ambos": ["png", "svg"], "todos": ["png", "svg", "pdf"]}.get(
        args.formato, [args.formato]
    )
    for nome, fn in figuras_disponiveis.items():
        try:
            fig, _ = fn()
            for ext in formatos:
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
