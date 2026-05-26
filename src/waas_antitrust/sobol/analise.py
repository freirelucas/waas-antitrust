"""Análise dos resultados da varredura Sobol."""

from __future__ import annotations

import pandas as pd
from SALib.analyze import sobol as sobol_analise


def calcular_indices(
    df_resultados: pd.DataFrame,
    problema: dict,
    metrica: str = "bem_estar",
) -> pd.DataFrame:
    """Índices de Sobol (S1 e ST) para uma **matriz única** (uma réplica).

    Para resultados de `executar_varredura` (com coluna ``replica``), use
    ``calcular_indices_replicado``, que medeia os índices entre réplicas.
    """
    Y = df_resultados[metrica].to_numpy()
    Si = sobol_analise.analyze(problema, Y, calc_second_order=False, print_to_console=False)
    return pd.DataFrame(
        {
            "parâmetro": problema["names"],
            "S1": Si["S1"],
            "S1_ic": Si["S1_conf"],
            "ST": Si["ST"],
            "ST_ic": Si["ST_conf"],
        }
    ).sort_values("ST", ascending=False)


def calcular_indices_replicado(
    df_resultados: pd.DataFrame,
    problema: dict,
    metrica: str = "bem_estar",
) -> pd.DataFrame:
    """Índices de Sobol mediados sobre réplicas.

    Espera ``df_resultados`` com coluna ``replica`` (ver
    ``execucao.executar_varredura``). Cada bloco de réplica deve estar na ordem
    da matriz de Saltelli. Calcula S1/ST por réplica e devolve média e
    desvio-padrão entre réplicas — esta é a forma correta de obter índices com
    incerteza estocástica, em vez de alternar seeds dentro de uma só matriz.
    """
    if "replica" not in df_resultados.columns:
        raise ValueError(
            "df_resultados não tem coluna 'replica'; use executar_varredura "
            "ou calcular_indices para uma matriz única."
        )
    por_replica = []
    for replica, grupo in df_resultados.groupby("replica", sort=True):
        Y = grupo[metrica].to_numpy()
        Si = sobol_analise.analyze(problema, Y, calc_second_order=False, print_to_console=False)
        por_replica.append(
            pd.DataFrame(
                {
                    "parâmetro": problema["names"],
                    "replica": replica,
                    "S1": Si["S1"],
                    "ST": Si["ST"],
                }
            )
        )
    todos = pd.concat(por_replica, ignore_index=True)
    return (
        todos.groupby("parâmetro", sort=False)
        .agg(S1=("S1", "mean"), S1_dp=("S1", "std"), ST=("ST", "mean"), ST_dp=("ST", "std"))
        .reset_index()
        .sort_values("ST", ascending=False)
    )


def identificar_regiao_robusta(
    df_resultados: pd.DataFrame,
    *,
    limiar_bem_estar: float = 0.0,
    limiar_precisao: float = 0.85,
) -> pd.DataFrame:
    """Marca amostras na região robusta de política.

    Região robusta: bem-estar estritamente positivo E precisão acima do limiar.
    """
    df = df_resultados.copy()
    df["robusta"] = (df["bem_estar"] > limiar_bem_estar) & (df["precisao"] > limiar_precisao)
    return df
