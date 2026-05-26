#!/usr/bin/env python
"""Gera todas as figuras do artigo nas pastas indicadas."""

from __future__ import annotations

import argparse
from pathlib import Path

from waas_antitrust.viz import aplicar_estilo, fase, inversao


def principal():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("figuras/"))
    parser.add_argument("--formato", choices=["png", "svg", "ambos"], default="ambos")
    parser.add_argument("--dpi", type=int, default=150)
    args = parser.parse_args()

    aplicar_estilo()
    args.out.mkdir(parents=True, exist_ok=True)

    geradoras = {
        "01_inversao_utilidade": inversao.gerar_figura,
        "02_fase_jogo_global": fase.gerar_figura,
        # 03-11 ainda no caderno; ver docs/DECISIONS.md
    }

    formatos = ["png", "svg"] if args.formato == "ambos" else [args.formato]

    for nome, fn in geradoras.items():
        try:
            fig, _ = fn()
            for fmt in formatos:
                caminho = args.out / f"{nome}.{fmt}"
                fig.savefig(caminho, dpi=args.dpi, bbox_inches="tight")
                print(f"  gerada: {caminho}")
        except NotImplementedError as e:
            print(f"  pulada {nome}: {e}")


if __name__ == "__main__":
    principal()
