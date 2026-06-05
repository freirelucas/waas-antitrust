"""Calibração contra dados externos primários.

Submódulos:
    cade               — série histórica do CADE (comunicados + DEE)
    brasscom           — parâmetros do mercado de trabalho TIC (Brasscom 2024)
    saito              — Saito (Carolina, 2021): desconto em TCCs 2012-2019
    transparencia_cade — capacidade institucional do CADE via Portal da
                         Transparência e MGISP (placeholder R06)
"""

from waas_antitrust.calibracao.brasscom import PARAMS_BRASSCOM_2024
from waas_antitrust.calibracao.cade import SERIE_LENIENCIAS_CADE_2003_2023
from waas_antitrust.calibracao.saito import (
    MEDIANA_DESCONTO_TCC_2012_2019,
    N_TCC_SAITO_2012_2019,
)
from waas_antitrust.calibracao.transparencia_cade import (
    N_SERVIDORES_TOTAL,
)

__all__ = [
    "MEDIANA_DESCONTO_TCC_2012_2019",
    "N_SERVIDORES_TOTAL",
    "N_TCC_SAITO_2012_2019",
    "PARAMS_BRASSCOM_2024",
    "SERIE_LENIENCIAS_CADE_2003_2023",
]
