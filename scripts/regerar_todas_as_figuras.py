#!/usr/bin/env python
"""Regera todas as 19 figuras publicadas no site, em sequência.

Comando único para o leitor cético reproduzir TODAS as figuras
empíricas do projeto a partir do código. Cada figura é gerada por
seu módulo `viz/` (figuras 04-09, 11-18) ou por script dedicado
(03, 10, 19).

Tempo total: ~5-10 min em laptop (figura 10 e 18 dominam o tempo).
Saídas em `docs/img/`.

Uso:
    python scripts/regerar_todas_as_figuras.py
    python scripts/regerar_todas_as_figuras.py --so 12 13   # subconjunto
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

#: Mapa figura → (gerador, descrição curta).
#: - geradores `viz/`: nome do submódulo (`gerar_figura()` salva em docs/img).
#: - geradores `script`: caminho do script a invocar.
FIGURAS: dict[str, tuple[str, str, str]] = {
    "03": ("script", "scripts/gerar_figura_dissuasao.py", "dissuasão e bem-estar"),
    "04": ("viz", "cascata", "cascata massa crítica"),
    "05": ("viz", "erosao", "erosão Coleman (3 alphas)"),
    "06": ("viz", "painel_macro", "painel macro 2×2"),
    "07": ("viz", "painel_micro", "painel micro firma 0"),
    "08": ("viz", "proposicao_5", "Proposição 5 multi-seed"),
    "09": ("viz", "multiplicidade_unicidade", "multiplicidade × unicidade"),
    "10": (
        "script",
        "scripts/varredura_alpha_erosao.py && python -m waas_antitrust.viz.alpha_erosao_limiar",
        "falsificação Prop. 5 forte",
    ),
    "11": ("viz", "sankey", "Sankey LCMC"),
    "12": ("viz", "bootstrap", "bootstrap regimes"),
    "13": ("viz", "internacional", "3 jurisdições"),
    "14": ("viz", "cade", "capacidade CADE (RIG)"),
    "15": ("viz", "adversarial", "uso adversarial R24"),
    "16": ("viz", "falsificacao", "mapa de vetores"),
    "17": ("viz", "variedade", "variedade Ashby × papéis"),
    "18": ("viz", "painel", "painel-síntese 2×3"),
    "19": ("script", "scripts/mapa_lambda_hirschman.py", "mapa λ × Hirschman"),
}

_VIZ_OUT_NUM = {
    "cascata": "04",
    "erosao": "05",
    "painel_macro": "06",
    "painel_micro": "07",
    "proposicao_5": "08",
    "multiplicidade_unicidade": "09",
    "sankey": "11",
    "bootstrap": "12",
    "internacional": "13",
    "cade": "14",
    "adversarial": "15",
    "falsificacao": "16",
    "variedade": "17",
    "painel": "18",
}


def _gerar_viz(modulo: str) -> Path:
    """Roda `viz/<modulo>.py` como módulo (salva em docs/img/)."""
    cmd = [sys.executable, "-m", f"waas_antitrust.viz.{modulo}"]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    num = _VIZ_OUT_NUM[modulo]
    candidatos = list(Path("docs/img").glob(f"{num}_*.png"))
    return candidatos[0] if candidatos else Path(f"docs/img/{num}_?.png")


def _gerar_script(rel_cmd: str) -> Path | None:
    """Roda `python <script>` ou cadeia 'cmd1 && cmd2'."""
    for partial in rel_cmd.split("&&"):
        cmd = [sys.executable] + partial.strip().split()
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    return None  # caminho do PNG variável; script imprime


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--so",
        type=str,
        nargs="+",
        default=list(FIGURAS),
        help="subconjunto de figuras (ex.: --so 12 13)",
    )
    args = ap.parse_args()

    print(f"Regerando {len(args.so)} figuras → docs/img/\n")
    t_total = time.time()
    for fig in args.so:
        if fig not in FIGURAS:
            print(f"  [pular] {fig}: não está no catálogo.")
            continue
        kind, alvo, descricao = FIGURAS[fig]
        print(f"  [{fig}] {descricao} ({kind}: {alvo})", flush=True)
        t = time.time()
        try:
            if kind == "viz":
                _gerar_viz(alvo)
            else:
                _gerar_script(alvo)
            print(f"        ✓ {time.time() - t:.1f}s")
        except subprocess.CalledProcessError as exc:
            print(f"        ✗ ERRO: {exc.stderr.strip()[:200]}")
            raise
    print(f"\nConcluído em {time.time() - t_total:.1f}s.")


if __name__ == "__main__":
    main()
