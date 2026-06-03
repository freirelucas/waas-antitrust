"""Calibração contra dados externos primários.

Submódulos:
    cade     — série histórica do CADE (comunicados + DEE)
    brasscom — parâmetros do mercado de trabalho TIC (Brasscom 2024)
    saito    — mediana de desconto em TCCs CADE 2012-2019 (placeholder R03)
"""

from waas_antitrust.calibracao.brasscom import PARAMS_BRASSCOM_2024
from waas_antitrust.calibracao.cade import SERIE_LENIENCIAS_CADE_2003_2023
from waas_antitrust.calibracao.saito import (
    MEDIANA_DESCONTO_TCC_2012_2019,
    N_TCC_SAITO_2012_2019,
)

__all__ = [
    "MEDIANA_DESCONTO_TCC_2012_2019",
    "N_TCC_SAITO_2012_2019",
    "PARAMS_BRASSCOM_2024",
    "SERIE_LENIENCIAS_CADE_2003_2023",
]
