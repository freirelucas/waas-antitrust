#!/usr/bin/env python
"""Análise de identificabilidade dos 3 alvos de calibração (R03, terceira ponta).

A segunda rodada de calibração (`results/calibracao_r03_first_pass.parquet`)
encontrou sinais opostos: o modelo sub-conta volume (0,84 TCC/ano vs alvo 47)
e super-detecta internamente (88% vs alvo 19%). Esta análise decompõe o
diagnóstico em três perguntas:

1. **Sensibilidade 1D**: qual parâmetro move qual alvo? Varre 7 parâmetros
   um de cada vez (resto no default, Regime B), 5 valores × 5 seeds, e mede
   a amplitude de resposta de cada um dos 3 alvos.

2. **Fator de escala implícito (alvo de volume)**: o alvo de 47 TCC/ano é do
   universo INTEIRO do CADE; o modelo simula `n_empresas=20`. O alvo
   reescalonado é `47 × (n_modelo / N_universo)`. Invertendo: qual N_universo
   tornaria o modelo consistente? `N* = 47 × n_modelo / tcc_anual_simulado`.
   N* é uma PREDIÇÃO FALSIFICÁVEL — comparar com o número real de firmas
   sob jurisdição ativa do CADE (pendência E-nova; não inventar o número).

3. **Alvo de composição inaplicável (fração interna)**: o alvo DMZ de 19%
   é a fração de fraudes detectadas POR EMPREGADOS dentre TODOS os canais
   (auditoria, mídia, concorrentes, reguladores). O modelo tem UM canal de
   detecção (o trabalhador) — a fração interna é ~100% por construção, menos
   o ruído de falso reporte. O alvo 3 é não-identificável sem modelar canais
   exógenos de detecção.

Saídas:
- `results/identificabilidade_r03.parquet`: long DataFrame da varredura 1D.
- Stdout: matriz parâmetro × alvo (amplitude de resposta) + N* + diagnóstico.

Uso:
    python scripts/identificabilidade_r03.py
    python scripts/identificabilidade_r03.py --seeds 11 23 37 41 53 59
"""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from waas_antitrust.model import WaaSModel, WaaSParametros

# Alvos do ODD (mesmos do scripts/calibrar.py — fontes primárias lá citadas).
ALVO_TCC_ANUAL = 47.0  # Saito 2021, média 2012-2019, universo CADE inteiro
ALVO_FRACAO_VP_INTERNAS = 0.19  # Dyck-Morse-Zingales 2010, composição de canais

#: Grades 1D por parâmetro — 5 valores cobrindo o intervalo plausível de cada um.
GRADES_1D: dict[str, list[float]] = {
    "taxa_observacao": [0.05, 0.15, 0.25, 0.40, 0.60],
    "taxa_falso_reporte": [0.0, 0.01, 0.02, 0.05, 0.10],
    "rho": [0.40, 0.55, 0.70, 0.85, 0.95],
    "taxa_capacidade": [0.05, 0.15, 0.30, 0.50, 0.90],
    "fracao_violadoras": [0.10, 0.30, 0.50, 0.70, 0.90],
    "k_rel": [0.01, 0.03, 0.05, 0.10, 0.20],
    "W_mult": [0.5, 1.0, 1.5, 2.5, 4.0],
}


def _medir(params: WaaSParametros) -> dict[str, float]:
    """Roda o modelo e devolve os 3 alvos medidos (normalizados a anuais)."""
    df = WaaSModel(params).executar()
    n_anos = params.n_tiques / 4.0
    tcc_anual = float(df["n_tcc_assinados"].iloc[-1]) / n_anos
    vp = int(df["verdadeiros_positivos_acum"].iloc[-1])
    fn = int(df["falsos_negativos_acum"].iloc[-1])
    fracao_vp_internas = vp / max(1, vp + fn)
    return {"tcc_anual": tcc_anual, "fracao_vp_internas": fracao_vp_internas}


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--seeds", type=int, nargs="+", default=[11, 23, 37, 41, 53])
    ap.add_argument("--tiques", type=int, default=40)
    ap.add_argument("--out", type=str, default="results/identificabilidade_r03.parquet")
    args = ap.parse_args()

    base = WaaSParametros(
        n_empresas=20,
        tam_medio_empresa=200,
        n_tiques=args.tiques,
        regime="B",
    )

    n_rodadas = sum(len(v) for v in GRADES_1D.values()) * len(args.seeds)
    print(
        f"Varredura 1D: {len(GRADES_1D)} parâmetros × ~5 valores × "
        f"{len(args.seeds)} seeds = {n_rodadas} rodadas ({args.tiques} tiques cada)\n"
    )

    registros: list[dict[str, object]] = []
    for nome_param, grade in GRADES_1D.items():
        for valor in grade:
            for seed in args.seeds:
                params = replace(base, seed=seed, **{nome_param: valor})
                medidas = _medir(params)
                registros.append(
                    {
                        "parametro": nome_param,
                        "valor": valor,
                        "seed": seed,
                        **medidas,
                    }
                )

    df = pd.DataFrame(registros)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    print(f"Gravado: {out} ({len(df)} linhas)\n")

    # ------------------------------------------------------------------
    # 1. Matriz de sensibilidade: amplitude da mediana por parâmetro × alvo
    # ------------------------------------------------------------------
    print("=" * 72)
    print("1. SENSIBILIDADE 1D — amplitude da resposta mediana (max − min sobre a grade)")
    print("=" * 72)
    print(f"{'parâmetro':<22} {'Δ tcc_anual':>14} {'Δ fração_interna':>18}")
    medianas_por_pv = df.groupby(["parametro", "valor"]).median(numeric_only=True).reset_index()
    for nome_param in GRADES_1D:
        sub = medianas_por_pv[medianas_por_pv["parametro"] == nome_param]
        amp_tcc = float(sub["tcc_anual"].max() - sub["tcc_anual"].min())
        amp_fr = float(sub["fracao_vp_internas"].max() - sub["fracao_vp_internas"].min())
        print(f"{nome_param:<22} {amp_tcc:>14.3f} {amp_fr:>18.3f}")

    # ------------------------------------------------------------------
    # 2. Fator de escala implícito do alvo de volume
    # ------------------------------------------------------------------
    print()
    print("=" * 72)
    print("2. FATOR DE ESCALA IMPLÍCITO (alvo de volume: 47 TCC/ano no universo CADE)")
    print("=" * 72)
    base_medidas = [_medir(replace(base, seed=s)) for s in args.seeds]
    tcc_anual_base = float(np.median([m["tcc_anual"] for m in base_medidas]))
    n_estrela = ALVO_TCC_ANUAL * base.n_empresas / max(1e-9, tcc_anual_base)
    print(
        f"Modelo (defaults, Regime B, {base.n_empresas} firmas): "
        f"{tcc_anual_base:.2f} TCC/ano simulado."
    )
    print(
        f"N* (universo que tornaria o modelo consistente com 47 TCC/ano): "
        f"~{n_estrela:.0f} firmas."
    )
    print(
        "Leitura: o 'gap de escala' das rodadas anteriores não é defeito do\n"
        "modelo — é falta de normalização do alvo. O alvo de volume só é\n"
        "comparável após reescalonar por (n_modelo / N_universo). N* acima é\n"
        "uma predição falsificável: verificar contra o número real de firmas\n"
        "sob jurisdição ativa do CADE (pendência empírica — não inventar)."
    )

    # ------------------------------------------------------------------
    # 3. Alvo de composição inaplicável
    # ------------------------------------------------------------------
    print()
    print("=" * 72)
    print("3. ALVO DE COMPOSIÇÃO (19% DMZ) — não-identificável por construção")
    print("=" * 72)
    fr_base = float(np.median([m["fracao_vp_internas"] for m in base_medidas]))
    print(f"Fração interna simulada (defaults): {fr_base:.1%} (alvo DMZ: 19%).")
    print(
        "O modelo tem UM canal de detecção (o trabalhador). A fração de 19%\n"
        "de DMZ é a participação dos empregados ENTRE TODOS os canais\n"
        "(auditoria externa, mídia, concorrentes, reguladores). Sem modelar\n"
        "canais exógenos de detecção, a fração interna do modelo é ~100% por\n"
        "construção — o alvo 3 não restringe nenhum parâmetro atual.\n"
        "Recomendação: remover o alvo 3 da função objetivo de calibração até\n"
        "que canais exógenos sejam modelados (novo item de backlog), ou\n"
        "reinterpretá-lo como alvo do parâmetro de um canal exógeno futuro."
    )


if __name__ == "__main__":
    main()
