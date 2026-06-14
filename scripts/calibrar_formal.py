#!/usr/bin/env python
r"""Calibração formal R03 sobre o problema reduzido.

A análise de identificabilidade (`scripts/identificabilidade_r03.py`,
commit `f62a690`) decompôs o "conflito de 3 alvos" em:

- 1 alvo operacional: TCC/ano reescalonado por (n_modelo / N_universo).
- 2 parâmetros dominantes: `fracao_violadoras`, `taxa_capacidade`.
- 1 parâmetro a descartar: `rho` (Δ mediana = 0 sobre alvos de volume).
- 1 alvo a descartar: DMZ 19% (não-identificável com canal único).

Este script faz a calibração formal sobre o problema reduzido usando
`scipy.optimize.minimize(method="Nelder-Mead")` — derivative-free,
adequado para função objetivo ruidosa (multi-seed). Honestidade:

- A função objetivo é *expressamente normalizada* — alvo em TCC/ano por
  20 firmas (não 47/ano do universo CADE inteiro). O N\* implícito é
  reportado ao final como predição falsificável.
- Multi-seed averaging (média sobre seeds), não bootstrap CI no loop
  interno — bootstrap externo no ponto ótimo dá o IC honesto.
- O ponto ótimo é registrado em `results/calibracao_formal_r03.json`
  com tudo: ponto, valor objetivo, alvo, N\* implícito, seeds, número
  de iterações, configuração.

Saídas:
- `results/calibracao_formal_r03.json` (ponto + diagnóstico).
- Stdout: trace de convergência + relatório final com IC bootstrap.

Uso:
    python scripts/calibrar_formal.py
    python scripts/calibrar_formal.py --seeds 11 23 37 41 53 59
    python scripts/calibrar_formal.py --n-universo 1500  # alvo escalado
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.robustez import bootstrap_ci

#: Universo CADE inteiro — alvo "47 TCC/ano". A normalização por
#: (n_modelo / N_universo) é a essência do achado de identificabilidade.
ALVO_TCC_ANUAL_UNIVERSO = 47.0


@dataclass
class PontoOtimo:
    """Resultado da calibração formal."""

    fracao_violadoras: float
    taxa_capacidade: float
    tcc_anual_simulado: float
    tcc_anual_alvo: float
    erro_relativo: float
    n_iteracoes: int
    n_universo_assumido: float
    n_estrela_implicito: float
    ic_inf_tcc: float
    ic_sup_tcc: float
    seeds: list[int]
    n_empresas_modelo: int
    n_tiques: int


def _tcc_anual_medio(
    fracao_violadoras: float,
    taxa_capacidade: float,
    seeds: list[int],
    n_empresas: int,
    n_tiques: int,
) -> tuple[float, list[float]]:
    """Roda o modelo para cada seed e devolve (média TCC/ano, lista por seed)."""
    valores: list[float] = []
    for seed in seeds:
        params = WaaSParametros(
            n_empresas=n_empresas,
            tam_medio_empresa=200,
            n_tiques=n_tiques,
            regime="B",
            seed=seed,
            fracao_violadoras=float(np.clip(fracao_violadoras, 0.01, 0.99)),
            taxa_capacidade=float(np.clip(taxa_capacidade, 0.05, 0.99)),
        )
        df = WaaSModel(params).executar()
        n_anos = n_tiques / 4.0
        valores.append(float(df["n_tcc_assinados"].iloc[-1]) / n_anos)
    return float(np.mean(valores)), valores


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--seeds", type=int, nargs="+", default=[11, 23, 37, 41, 53])
    ap.add_argument("--tiques", type=int, default=40)
    ap.add_argument("--n-empresas", type=int, default=20)
    ap.add_argument(
        "--n-universo",
        type=float,
        default=1567.0,
        help=(
            "Universo CADE assumido para reescalonar o alvo de volume. "
            "Default 1.567 vem da identificabilidade — predição falsificável "
            "contra o número real (pendência empírica)."
        ),
    )
    ap.add_argument("--out", type=str, default="results/calibracao_formal_r03.json")
    ap.add_argument("--x0", type=float, nargs=2, default=[0.30, 0.50])
    args = ap.parse_args()

    alvo_modelo = ALVO_TCC_ANUAL_UNIVERSO * args.n_empresas / args.n_universo
    print(
        f"Problema reduzido: minimizar |tcc/ano − {alvo_modelo:.3f}|² "
        f"em (fracao_violadoras, taxa_capacidade)."
    )
    print(f"Alvo normalizado: {alvo_modelo:.3f} TCC/ano (modelo de {args.n_empresas} firmas).")
    print(
        f"Hipótese de universo CADE: {args.n_universo:.0f} firmas "
        f"(predição falsificável; pendência empírica)."
    )
    print(f"Seeds: {args.seeds}; horizonte: {args.tiques} tiques.\n")

    n_aval = [0]

    def objetivo(x: np.ndarray) -> float:
        fv, tc = float(x[0]), float(x[1])
        media, _ = _tcc_anual_medio(fv, tc, args.seeds, args.n_empresas, args.tiques)
        n_aval[0] += 1
        erro = (media - alvo_modelo) ** 2
        print(
            f"  iter {n_aval[0]:>3}: fv={fv:.3f} tc={tc:.3f} → "
            f"tcc/ano={media:.3f}  erro²={erro:.4e}"
        )
        return erro

    t0 = time.time()
    resultado = minimize(
        objetivo,
        x0=np.asarray(args.x0),
        method="Nelder-Mead",
        options={"xatol": 0.01, "fatol": 1e-4, "maxiter": 40, "disp": False},
    )
    dt = time.time() - t0

    fv_otimo, tc_otimo = float(resultado.x[0]), float(resultado.x[1])
    # IC bootstrap no ponto ótimo (re-roda com seeds + IC sobre a lista).
    _, lista_tcc = _tcc_anual_medio(fv_otimo, tc_otimo, args.seeds, args.n_empresas, args.tiques)
    ic = bootstrap_ci(lista_tcc, n_bootstrap=2000, seed=0)
    media_otima = float(np.mean(lista_tcc))

    # N_estrela implícito: que universo CADE tornaria o modelo consistente?
    n_estrela = (
        ALVO_TCC_ANUAL_UNIVERSO * args.n_empresas / max(1e-9, media_otima)
        if media_otima > 0
        else float("inf")
    )
    erro_rel = abs(media_otima - alvo_modelo) / max(1e-9, alvo_modelo)

    ponto = PontoOtimo(
        fracao_violadoras=fv_otimo,
        taxa_capacidade=tc_otimo,
        tcc_anual_simulado=media_otima,
        tcc_anual_alvo=alvo_modelo,
        erro_relativo=erro_rel,
        n_iteracoes=int(resultado.nit),
        n_universo_assumido=float(args.n_universo),
        n_estrela_implicito=float(n_estrela),
        ic_inf_tcc=float(ic.inferior),
        ic_sup_tcc=float(ic.superior),
        seeds=list(args.seeds),
        n_empresas_modelo=int(args.n_empresas),
        n_tiques=int(args.tiques),
    )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(asdict(ponto), indent=2, ensure_ascii=False))

    print("\n" + "=" * 70)
    print("RESULTADO DA CALIBRAÇÃO FORMAL R03 (PROBLEMA REDUZIDO)")
    print("=" * 70)
    print(f"  fracao_violadoras*  = {fv_otimo:.3f}")
    print(f"  taxa_capacidade*    = {tc_otimo:.3f}")
    print(
        f"  TCC/ano simulado    = {media_otima:.3f}  (IC 95%: [{ic.inferior:.3f}, {ic.superior:.3f}])"
    )
    print(f"  TCC/ano alvo (normalizado) = {alvo_modelo:.3f}")
    print(f"  erro relativo            = {erro_rel:.2%}")
    print(
        f"  N★ implícito             = {n_estrela:.0f} firmas (vs N_assumido = {args.n_universo:.0f})"
    )
    print(f"  iterações Nelder-Mead    = {resultado.nit}  (avaliações: {n_aval[0]})")
    print(f"  tempo                    = {dt:.1f}s")
    print(f"\nGravado: {out}")


if __name__ == "__main__":
    main()
