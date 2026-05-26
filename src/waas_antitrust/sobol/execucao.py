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


def executar_para_sobol(
    linha: Sequence[float],
    *,
    regime: str = "B",
    seed: int = 42,
    n_empresas: int = 15,
    tam_medio_empresa: int = 300,
    n_tiques: int = 24,
) -> dict:
    """Executa uma única configuração paramétrica."""
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
    vp = int(df["verdadeiros_positivos"].max())
    fp = int(df["falsos_positivos"].max())
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    return {
        **dict(zip(PROBLEMA_SOBOL_8D["names"], linha)),
        "regime": regime,
        "seed": seed,
        "VP": vp,
        "FP": fp,
        "precisao": precisao,
        "bem_estar": vp - fp,
    }


def executar_varredura(
    n_base: int = 128,
    regime: str = "B",
    n_jobs: int = -1,
    n_empresas: int = 15,
    n_tiques: int = 24,
    seed_base: int = 42,
    n_seeds: int = 5,
    problema: dict | None = None,
) -> pd.DataFrame:
    """Executa a varredura completa de Sobol.

    Parameters
    ----------
    n_base : int
        Número-base de amostras Sobol. Total de simulações é
        n_base × (2·d + 2) onde d é o número de parâmetros.
    regime : str
        "A", "B" ou "C".
    n_jobs : int
        Número de processos paralelos. -1 usa todos os núcleos.
    n_seeds : int
        Quantas sementes diferentes alternar entre as amostras.

    Returns
    -------
    DataFrame com colunas: parâmetros + regime + seed + VP + FP + precisão + bem_estar.
    """
    problema = problema or PROBLEMA_SOBOL_8D
    amostras = sobol_amostragem.sample(problema, n_base, calc_second_order=False)

    resultados = Parallel(n_jobs=n_jobs, verbose=10)(
        delayed(executar_para_sobol)(
            linha,
            regime=regime,
            seed=seed_base + (i % n_seeds),
            n_empresas=n_empresas,
            n_tiques=n_tiques,
        )
        for i, linha in enumerate(amostras)
    )
    return pd.DataFrame(resultados)
