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

# Pesos do bem-estar SOCIAL. NORMATIVOS e provisórios — calibrar em R03
# (ver docs/DECISIONS.md, R05). O bem-estar é o NEGATIVO do custo social total:
# dano (Σ violadoras·tique, R01) + custo de erro (falsos positivos) + custo da
# recompensa. `gamma_recompensa`=0 por ser, a rigor, transferência privada
# (empresa → denunciantes); eleve para penalizar distorções.
PESOS_BEM_ESTAR: dict[str, float] = {
    "beta_fp": 1.0,  # custo de um falso positivo (em violador-tiques equivalentes)
    "gamma_recompensa": 0.0,  # peso do custo de recompensa (normalizado por w_a)
}


def calcular_bem_estar(
    dano: int,
    fp: int,
    custo_recompensa: float,
    w_a_base: float,
    pesos: dict[str, float] | None = None,
) -> float:
    """Bem-estar social = − custo social total = −(dano + β·FP + γ·custo/w_a).

    `dano` = Σ violadoras ativas por tique (proxy de dano social). Como a dissuasão
    (R01) reduz o dano, esta métrica credita a PREVENÇÃO — ao contrário da antiga
    contagem por detecção (VP−FP−FN), que ranqueava mal regimes que deterem.
    Pesos normativos provisórios (calibrar em R03).
    """
    pesos = pesos or PESOS_BEM_ESTAR
    custo_norm = custo_recompensa / w_a_base if w_a_base else 0.0
    return -(dano + pesos["beta_fp"] * fp + pesos["gamma_recompensa"] * custo_norm)


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
    dano = int(df["dano_acumulado"].max())
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    return {
        **dict(zip(PROBLEMA_SOBOL_8D["names"], linha, strict=True)),
        "regime": regime,
        "seed": seed,
        "replica": replica,
        "VP": vp,
        "FP": fp,
        "FN": fn,
        "dano_acumulado": dano,
        "custo_recompensa": custo_recompensa,
        "precisao": precisao,
        "bem_estar": calcular_bem_estar(dano, fp, custo_recompensa, params.w_a_base),
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
