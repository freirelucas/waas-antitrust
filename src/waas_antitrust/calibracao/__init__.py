"""Calibração contra dados externos primários.

Submódulos:
    cade     — série histórica do CADE (Estatísticas + Saito 2021)
    brasscom — parâmetros do mercado de trabalho TIC (Brasscom 2024)
"""

from waas_antitrust.calibracao.brasscom import PARAMS_BRASSCOM_2024
from waas_antitrust.calibracao.cade import SERIE_LENIENCIAS_CADE_2003_2023

__all__ = ["PARAMS_BRASSCOM_2024", "SERIE_LENIENCIAS_CADE_2003_2023"]
