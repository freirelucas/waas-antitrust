#!/usr/bin/env python3
"""Driver de fumaça do waas-antitrust.

Exercita, num passe só, as quatro camadas que os PRs deste repositório costumam
tocar — e produz um artefato visual (as figuras), que é o equivalente do
"screenshot" para um projeto científico sem GUI:

  1. modelo      (model.py / agents.py) — 3 regimes; dissuasão (R01) e bem-estar (R05);
  2. sobol       (sobol/)               — varredura replicada + índices mediados;
  3. jogo_global (jogo_global.py)       — limiar de switching único, convergência τ→0 (R02);
  4. viz         (viz/)                 — gera as 2 figuras implementadas em PNG.

Rode dentro do venv de desenvolvimento (Python 3.12, `pip install -e ".[dev]"`):

    /home/user/.venv-waas/bin/python \
        .claude/skills/run-waas-antitrust/driver.py --out /tmp/waas-driver

Sai com código 0 se tudo rodar; imprime um resumo legível e o caminho das figuras.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def secao(titulo: str) -> None:
    print(f"\n=== {titulo} ===")


def smoke_modelo() -> None:
    """Camada de modelo: roda os 3 regimes via API pública e imprime métricas."""
    from waas_antitrust.model import WaaSModel, WaaSParametros
    from waas_antitrust.sobol.execucao import calcular_bem_estar

    secao("modelo · 3 regimes (execução direta)")
    for regime in ("A", "B", "C"):
        p = WaaSParametros(
            n_empresas=20, tam_medio_empresa=200, n_tiques=40, regime=regime, seed=42
        )
        df = WaaSModel(p).executar()
        vp = int(df["verdadeiros_positivos_acum"].max())
        fp = int(df["falsos_positivos_acum"].max())
        fn = int(df["falsos_negativos_acum"].max())
        dano = int(df["dano_acumulado"].max())
        custo = float(df["custo_recompensa_acum"].max())
        bem_estar = calcular_bem_estar(dano, fp, custo, p.w_a_base)
        print(
            f"  regime {regime}: VP={vp:4d} FP={fp:3d} FN={fn:3d} "
            f"dano={dano:5d} bem_estar={bem_estar:9.1f}"
        )


def smoke_sobol() -> None:
    """Camada de sensibilidade: varredura replicada + índices de Sobol mediados."""
    from waas_antitrust.sobol import PROBLEMA_SOBOL_8D, executar_varredura
    from waas_antitrust.sobol.analise import calcular_indices_replicado

    secao("sobol · varredura replicada + índices mediados")
    df = executar_varredura(n_base=8, regime="B", n_jobs=1, n_empresas=4, n_tiques=6, n_replicas=2)
    print(f"  amostras={len(df)}  réplicas={sorted(int(r) for r in df['replica'].unique())}")
    resumo = calcular_indices_replicado(df, PROBLEMA_SOBOL_8D, metrica="bem_estar")
    print("  ST (ordem total) — 4 parâmetros mais sensíveis:")
    for _, linha in resumo.head(4).iterrows():
        print(f"    {linha['parâmetro']:<16} ST={linha['ST']:+.3f}")


def smoke_jogo_global() -> None:
    """Camada R02: limiar de switching único e convergência quando τ→0."""
    from waas_antitrust.jogo_global import limiar_switching, trilha_convergencia

    secao("jogo_global · limiar de switching único (R02, estilizado)")
    b, c, k = 1.5, 0.15, 0.05
    limite = limiar_switching(b, c, k, tau=0.0)
    erros = [abs(x - limite) for x in trilha_convergencia(b, c, k, [0.5, 0.1, 0.01])]
    print(f"  x*(τ→0)={limite:+.4f}  erros decrescentes p/ τ↓: {[f'{e:.3f}' for e in erros]}")
    assert erros == sorted(erros, reverse=True), "convergência não-monotônica em τ"


def smoke_figuras(out: Path) -> list[Path]:
    """Camada de visualização: gera as figuras implementadas (inversão e fase)."""
    import matplotlib

    matplotlib.use("Agg")  # backend headless; sem display/xvfb

    from waas_antitrust.viz import aplicar_estilo, fase, inversao

    secao("viz · geração de figuras (Agg, headless)")
    aplicar_estilo()
    out.mkdir(parents=True, exist_ok=True)
    gerados: list[Path] = []
    figuras = {"01_inversao": inversao.gerar_figura, "02_fase": fase.gerar_figura}
    for nome, fn in figuras.items():
        fig, _ = fn()
        caminho = out / f"{nome}.png"
        fig.savefig(caminho, dpi=120, bbox_inches="tight")
        print(f"  gerada: {caminho}")
        gerados.append(caminho)
    return gerados


def main() -> int:
    parser = argparse.ArgumentParser(description="Driver de fumaça do waas-antitrust.")
    parser.add_argument("--out", type=Path, default=Path("/tmp/waas-driver"))
    args = parser.parse_args()

    smoke_modelo()
    smoke_sobol()
    smoke_jogo_global()
    figs = smoke_figuras(args.out)

    secao("OK")
    print(f"  figuras em {args.out}: {', '.join(f.name for f in figs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
