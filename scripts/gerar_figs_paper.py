#!/usr/bin/env python
"""Gera os PDFs de figuras do artigo a partir dos módulos `viz/`.

Os PDFs em `paper/figs/` são artefatos regeneráveis e NÃO são versionados
(`.gitignore`). Este script é a fonte única de regeneração — garante que
paper e site usam a MESMA figura (paleta, conteúdo, seeds).

Mapeamento figura do paper → módulo gerador:

- `01_inversao_utilidade.pdf` ← `viz/inversao.py`
- `02_fase_jogo_global.pdf`   ← `viz/fase.py`
- `03_alpha_erosao_limiar.pdf`← `viz/alpha_erosao_limiar.py`
  (requer `results/alpha_erosao_grade.parquet`; gerar antes com
  `python scripts/varredura_alpha_erosao.py`)
- `04_sankey_lcmc.pdf`        ← `viz/sankey.py` (roda cenário canônico)

Uso:
    python scripts/gerar_figs_paper.py
    # em seguida: cd paper && pdflatex main && bibtex main && pdflatex main ×2
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

FIGS = Path("paper/figs")


def main() -> None:
    FIGS.mkdir(parents=True, exist_ok=True)

    from waas_antitrust.viz import alpha_erosao_limiar, fase, inversao, sankey

    fig, _ = inversao.gerar_figura()
    fig.savefig(FIGS / "01_inversao_utilidade.pdf", bbox_inches="tight")
    print(f"Gravado: {FIGS / '01_inversao_utilidade.pdf'}")

    fig, _ = fase.gerar_figura()
    fig.savefig(FIGS / "02_fase_jogo_global.pdf", bbox_inches="tight")
    print(f"Gravado: {FIGS / '02_fase_jogo_global.pdf'}")

    parquet = Path("results/alpha_erosao_grade.parquet")
    if parquet.exists():
        fig, _ = alpha_erosao_limiar.gerar_figura(parquet_path=parquet)
        fig.savefig(FIGS / "03_alpha_erosao_limiar.pdf", bbox_inches="tight")
        print(f"Gravado: {FIGS / '03_alpha_erosao_limiar.pdf'}")
    else:
        print(
            f"AVISO: {parquet} ausente — rode `python scripts/varredura_alpha_erosao.py` "
            "antes para gerar a figura 03."
        )

    fig, _ = sankey.gerar_figura()
    fig.savefig(FIGS / "04_sankey_lcmc.pdf", bbox_inches="tight")
    print(f"Gravado: {FIGS / '04_sankey_lcmc.pdf'}")


if __name__ == "__main__":
    main()
