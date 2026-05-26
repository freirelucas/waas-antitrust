"""Execução da varredura paramétrica de Sobol.

Suporta execução síncrona e assíncrona (via joblib). Para a versão definitiva
do artigo, recomenda-se `n_base = 1024` com paralelismo total.
"""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
from joblib import Parallel, delayed
from SALib.sample import sobol as sobol_amostragem

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.sobol.problema import PROBLEMA_SOBOL_8D

# Pesos do bem-estar social. NORMATIVOS e provisórios — marcados para calibração
# (ver docs/DECISIONS.md). Padrão: contagem líquida de acertos penalizando erros
# (VP − FP − FN). O custo de recompensa entra com peso nulo por ser, a rigor, uma
# transferência privada (empresa → denunciantes); eleve `gamma_recompensa` para
# penalizar distorções/custos administrativos da recompensa.
PESOS_BEM_ESTAR: dict[str, float] = {
    "alpha_vp": 1.0,
    "beta_fp": 1.0,
    "delta_fn": 1.0,
    "gamma_recompensa": 0.0,
}


def calcular_bem_estar(
    vp: int,
    fp: int,
    fn: int,
    custo_recompensa: float,
    w_a_base: float,
    pesos: dict[str, float] | None = None,
) -> float:
    """Bem-estar social agregado (métrica normativa; pesos em PESOS_BEM_ESTAR).

    `custo_recompensa` (R$) é normalizado por `w_a_base` (salário anual) antes de
    entrar com peso `gamma_recompensa`.
    """
    pesos = pesos or PESOS_BEM_ESTAR
    custo_norm = custo_recompensa / w_a_base if w_a_base else 0.0
    return (
        pesos["alpha_vp"] * vp
        - pesos["beta_fp"] * fp
        - pesos["delta_fn"] * fn
        - pesos["gamma_recompensa"] * custo_norm
    )


def executar_para_sobol(
    linha: Sequence[float],
    *,
    regime: str = "B",
    seed: int = 42,
    n_empresas: int = 15,
    tam_medio_empresa: int = 300,
    n_tiques: int = 24,
    replica: int = 0,
) -> dict:
    """Executa uma única configuração paramétrica.

    `VP`/`FP`/`bem_estar` são os totais acumulados ao fim do horizonte.
    """
    W_mult, k_rel, D_disc, rho, r_repres, F_falso, densidade, taxa_obs = linha
    params = WaaSParametros(
        n_empresas=n_empresas,
        tam_medio_empresa=tam_medio_empresa,
        regime=regime,
        seed=seed,
        W_mult=W_mult,
        k_rel=k_rel,
        D_disc=D_disc,
        rho=rho,
        r_represalia=r_repres,
        F_falso=F_falso,
        densidade=densidade,
        taxa_observacao=taxa_obs,
        n_tiques=n_tiques,
    )
    modelo = WaaSModel(params)
    df = modelo.executar()
    vp = int(df["verdadeiros_positivos_acum"].max())
    fp = int(df["falsos_positivos_acum"].max())
    fn = int(df["falsos_negativos_acum"].max())
    custo_recompensa = float(df["custo_recompensa_acum"].max())
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    return {
        **dict(zip(PROBLEMA_SOBOL_8D["names"], linha, strict=True)),
        "regime": regime,
        "seed": seed,
        "replica": replica,
        "VP": vp,
        "FP": fp,
        "FN": fn,
        "custo_recompensa": custo_recompensa,
        "precisao": precisao,
        "bem_estar": calcular_bem_estar(vp, fp, fn, custo_recompensa, params.w_a_base),
    }


def executar_varredura(
    n_base: int = 128,
    regime: str = "B",
    n_jobs: int = -1,
    n_empresas: int = 15,
    n_tiques: int = 24,
    seed_base: int = 42,
    n_replicas: int = 5,
    problema: dict | None = None,
) -> pd.DataFrame:
    """Executa a varredura de Sobol com replicação correta sobre seeds.

    A matriz de Saltelli é gerada uma vez. Para cada réplica ``r`` em
    ``range(n_replicas)``, a matriz **inteira** é avaliada com uma seed fixa
    (``seed_base + r``), preservando o pareamento A/B/AB_i exigido pelo
    estimador de Sobol. As linhas de cada réplica ficam na ordem original da
    matriz; os índices são calculados por réplica e mediados em
    ``analise.calcular_indices_replicado``.

    NB: alternar a seed *dentro* de uma única matriz (como em versões
    anteriores) contamina o estimador e é incorreto.

    Parameters
    ----------
    n_base : int
        Número-base N. A matriz tem N·(d+2) linhas (calc_second_order=False).
    n_replicas : int
        Número de réplicas (seeds distintas) da matriz inteira.

    Returns
    -------
    DataFrame com N·(d+2)·n_replicas linhas; colunas: parâmetros + regime +
    seed + replica + VP + FP + precisão + bem_estar.
    """
    problema = problema or PROBLEMA_SOBOL_8D
    amostras = sobol_amostragem.sample(problema, n_base, calc_second_order=False)

    tarefas = [(r, linha) for r in range(n_replicas) for linha in amostras]
    resultados = Parallel(n_jobs=n_jobs, verbose=10)(
        delayed(executar_para_sobol)(
            linha,
            regime=regime,
            seed=seed_base + r,
            n_empresas=n_empresas,
            n_tiques=n_tiques,
            replica=r,
        )
        for r, linha in tarefas
    )
    return pd.DataFrame(resultados)
