#!/usr/bin/env python
r"""Calibração formal R03 multi-target (alvos 2 e 3).

Extensão do `calibrar_formal.py` para os três alvos do ODD que ficaram
em aberto sob a calibração unidimensional anterior:

- **Alvo 1** — TCCs/ano (reescalonado pelo universo CADE). Já fechado
  por Nelder-Mead 2D em `calibrar_formal.py`.
- **Alvo 2** — Sinais por tique por trabalhador (proxy de detecção
  espontânea no canal). Calibrado contra Dyck-Morse-Zingales (*J. Fin.*
  65(6), 2010) — aproximadamente 19 % das fraudes corporativas grandes
  nos EUA são descobertas por funcionários internos.
- **Alvo 3** — Dano agregado proporcional (proxy de bem-estar perdido).
  Calibrado direcionalmente — alvo absoluto não-identificável sem
  série temporal real de overcharge BR.

Função objetivo: soma ponderada de erros relativos ao quadrado por
alvo. O peso default (1/3 cada) é deliberadamente neutro; o autor
pode ajustar via flags para refletir prioridade de calibração.

Honestidade epistêmica:

- Identificabilidade fraca já documentada em
  `scripts/identificabilidade_r03.py` — os 3 alvos não são identificáveis
  conjuntamente sob o mesmo conjunto de 2 parâmetros (fração de
  violadoras, taxa de capacidade). O multi-target retorna o **melhor
  compromisso** sob o vetor de pesos escolhido, não a solução única.
- O resultado é registrado em `results/calibracao_formal_r03_multitarget.json`
  com (i) ponto, (ii) valor por alvo, (iii) erro relativo por alvo,
  (iv) pesos usados.

Uso:
    python scripts/calibrar_formal_multitarget.py
    python scripts/calibrar_formal_multitarget.py --pesos 0.6 0.3 0.1
    python scripts/calibrar_formal_multitarget.py --seeds 11 23 37
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy import optimize

from waas_antitrust.model import WaaSModel, WaaSParametros

# Universo CADE inteiro — alvo "47 TCC/ano" da Saito 2021. Reescalonado
# pelo (n_empresas_modelo / n_universo) na função objetivo.
ALVO_TCC_ANUAL_UNIVERSO = 47.0
# Alvo 2: 19 % das fraudes corporativas descobertas por funcionários
# (Dyck-Morse-Zingales 2010). Operacionalizado no modelo como fração
# de tiques em que há ≥ 1 sinal por trabalhador (proxy de \"detecção
# espontânea\").
ALVO_FRACAO_SINAIS_DMZ = 0.19
# Alvo 3: dano relativo direcional. Sob calibração ótima, o dano
# acumulado em Regime B deve ser substancialmente menor que em
# Regime A no mesmo horizonte. Default 0,3 = 70 % de redução.
ALVO_DANO_RELATIVO_B_SOBRE_A = 0.30


def _executar_seed(
    fracao_violadoras: float,
    taxa_capacidade: float,
    seed: int,
    n_empresas: int,
    n_tiques: int,
    regime: str = "B",
) -> dict[str, float]:
    """Roda 1 seed e devolve as 3 grandezas alvo."""
    params = WaaSParametros(
        n_empresas=n_empresas,
        tam_medio_empresa=200,
        n_tiques=n_tiques,
        regime=regime,
        seed=seed,
        fracao_violadoras=float(np.clip(fracao_violadoras, 0.01, 0.99)),
        taxa_capacidade=float(np.clip(taxa_capacidade, 0.05, 0.99)),
    )
    df = WaaSModel(params).executar()
    n_anos = n_tiques / 4.0
    n_trab = n_empresas * 200
    return {
        "tcc_anual": float(df["n_tcc_assinados"].iloc[-1]) / n_anos,
        "fracao_sinais": float(df["n_sinais"].mean()) / n_trab,
        "dano_final": float(df["dano_acumulado"].iloc[-1]),
    }


def _objetivo_multitarget(
    x: np.ndarray,
    pesos: tuple[float, float, float],
    alvo_tcc_modelo: float,
    seeds: list[int],
    n_empresas: int,
    n_tiques: int,
    dano_baseline_a: dict[int, float],
) -> float:
    """Erro vetorial ponderado: w1·rel²_tcc + w2·rel²_sinais + w3·rel²_dano."""
    fracao, taxa = float(x[0]), float(x[1])
    err_tcc = []
    err_sinais = []
    err_dano = []
    for seed in seeds:
        resultados = _executar_seed(fracao, taxa, seed, n_empresas, n_tiques)
        # Alvo 1 — TCCs/ano
        err_tcc.append(((resultados["tcc_anual"] - alvo_tcc_modelo) / max(alvo_tcc_modelo, 1e-6)) ** 2)
        # Alvo 2 — fração de tiques com ≥ 1 sinal por trabalhador
        err_sinais.append(
            ((resultados["fracao_sinais"] - ALVO_FRACAO_SINAIS_DMZ) / ALVO_FRACAO_SINAIS_DMZ) ** 2
        )
        # Alvo 3 — dano relativo B/A na mesma seed
        dano_a = dano_baseline_a.get(seed, 1.0)
        rel = resultados["dano_final"] / max(dano_a, 1e-6)
        err_dano.append(((rel - ALVO_DANO_RELATIVO_B_SOBRE_A) / ALVO_DANO_RELATIVO_B_SOBRE_A) ** 2)
    return float(
        pesos[0] * np.mean(err_tcc)
        + pesos[1] * np.mean(err_sinais)
        + pesos[2] * np.mean(err_dano)
    )


def _baseline_dano_regime_a(seeds: list[int], n_empresas: int, n_tiques: int) -> dict[int, float]:
    """Calcula o dano acumulado em Regime A para cada seed — referência
    do denominador no alvo 3."""
    out = {}
    for seed in seeds:
        r = _executar_seed(0.50, 0.50, seed, n_empresas, n_tiques, regime="A")
        out[seed] = max(r["dano_final"], 1e-6)
    return out


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
        help="Universo CADE assumido para reescalonar o alvo TCC/ano.",
    )
    ap.add_argument(
        "--pesos",
        type=float,
        nargs=3,
        default=[1 / 3, 1 / 3, 1 / 3],
        help="Pesos (w1, w2, w3) dos 3 alvos. Default 1/3 cada.",
    )
    ap.add_argument(
        "--out",
        type=str,
        default="results/calibracao_formal_r03_multitarget.json",
    )
    ap.add_argument("--x0", type=float, nargs=2, default=[0.30, 0.50])
    args = ap.parse_args()

    alvo_tcc_modelo = ALVO_TCC_ANUAL_UNIVERSO * args.n_empresas / args.n_universo
    pesos = tuple(args.pesos)
    print(
        f"R03 multi-target — pesos {pesos}; alvos: TCC/ano = "
        f"{alvo_tcc_modelo:.3f}, fração sinais = {ALVO_FRACAO_SINAIS_DMZ:.2f}, "
        f"dano B/A = {ALVO_DANO_RELATIVO_B_SOBRE_A:.2f}"
    )

    print("Calculando baseline dano Regime A...")
    dano_baseline_a = _baseline_dano_regime_a(args.seeds, args.n_empresas, args.tiques)

    print("Otimizando Nelder-Mead 2D sobre função objetivo vetorial...")
    t0 = time.time()
    result = optimize.minimize(
        _objetivo_multitarget,
        x0=np.array(args.x0),
        args=(pesos, alvo_tcc_modelo, args.seeds, args.n_empresas, args.tiques, dano_baseline_a),
        method="Nelder-Mead",
        options={"xatol": 1e-3, "fatol": 1e-4, "maxiter": 200, "disp": True},
    )
    dt = time.time() - t0

    fracao_otima = float(np.clip(result.x[0], 0.01, 0.99))
    taxa_otima = float(np.clip(result.x[1], 0.05, 0.99))

    # Apura erros por alvo no ponto ótimo
    relatorio_seeds = []
    for seed in args.seeds:
        r = _executar_seed(fracao_otima, taxa_otima, seed, args.n_empresas, args.tiques)
        rel_dano = r["dano_final"] / dano_baseline_a[seed]
        relatorio_seeds.append(
            {
                "seed": seed,
                "tcc_anual": r["tcc_anual"],
                "fracao_sinais": r["fracao_sinais"],
                "dano_relativo_b_sobre_a": rel_dano,
            }
        )
    tcc_medio = float(np.mean([r["tcc_anual"] for r in relatorio_seeds]))
    sinais_medio = float(np.mean([r["fracao_sinais"] for r in relatorio_seeds]))
    rel_dano_medio = float(np.mean([r["dano_relativo_b_sobre_a"] for r in relatorio_seeds]))

    erros_relativos = {
        "tcc_anual": abs(tcc_medio - alvo_tcc_modelo) / max(alvo_tcc_modelo, 1e-6),
        "fracao_sinais": abs(sinais_medio - ALVO_FRACAO_SINAIS_DMZ) / ALVO_FRACAO_SINAIS_DMZ,
        "dano_relativo": abs(rel_dano_medio - ALVO_DANO_RELATIVO_B_SOBRE_A)
        / ALVO_DANO_RELATIVO_B_SOBRE_A,
    }

    out = {
        "ponto_otimo": {"fracao_violadoras": fracao_otima, "taxa_capacidade": taxa_otima},
        "pesos": list(pesos),
        "alvos": {
            "tcc_anual_modelo": alvo_tcc_modelo,
            "fracao_sinais_DMZ": ALVO_FRACAO_SINAIS_DMZ,
            "dano_relativo_B_sobre_A": ALVO_DANO_RELATIVO_B_SOBRE_A,
        },
        "valores_medios_no_otimo": {
            "tcc_anual": tcc_medio,
            "fracao_sinais": sinais_medio,
            "dano_relativo_b_sobre_a": rel_dano_medio,
        },
        "erros_relativos": erros_relativos,
        "valor_objetivo_final": float(result.fun),
        "n_iter": int(result.nit),
        "seeds": args.seeds,
        "n_empresas": args.n_empresas,
        "n_tiques": args.n_tiques if hasattr(args, "n_tiques") else args.tiques,
        "tempo_segundos": dt,
        "metodo": "Nelder-Mead",
        "por_seed": relatorio_seeds,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nPonto ótimo: fração={fracao_otima:.4f}, taxa={taxa_otima:.4f}")
    print(
        f"Valores médios: TCC/ano={tcc_medio:.3f} (alvo {alvo_tcc_modelo:.3f}), "
        f"sinais={sinais_medio:.4f} (alvo {ALVO_FRACAO_SINAIS_DMZ:.2f}), "
        f"dano B/A={rel_dano_medio:.3f} (alvo {ALVO_DANO_RELATIVO_B_SOBRE_A:.2f})"
    )
    print(f"Erros relativos por alvo: {erros_relativos}")
    print(f"Tempo: {dt:.1f}s; resultado em {out_path}")


if __name__ == "__main__":
    main()
