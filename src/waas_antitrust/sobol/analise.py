"""Análise dos resultados da varredura Sobol."""

from __future__ import annotations

import pandas as pd
from SALib.analyze import sobol as sobol_analise


def calcular_indices(
    df_resultados: pd.DataFrame,
    problema: dict,
    metrica: str = "bem_estar",
) -> pd.DataFrame:
    """Calcula índices de Sobol de 1ª ordem e ordem total."""
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
