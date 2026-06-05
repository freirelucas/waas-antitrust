"""Calibração contra a série histórica do CADE.

Fontes primárias:
    - CADE, comunicado institucional de 06/10/2023 (109 acordos de
      leniência em 20 anos, média de cerca de 5 por ano).
    - Saito, C. (24/02/2021). *TCC na Lei nº 12.529/11.* Gabinete da
      Presidência do CADE — Consultoria PNUD/Brasil. (349 TCCs CADE
      04/07/2012 a 11/12/2019, média de cerca de 47 por ano.) Ver
      `calibracao/saito.py` para estatísticas de desconto extraídas.
    - CADE, DEE, *Documento de Trabalho 001/2024 — Benefícios de atuação
      do Cade em 2023*. (13 TCCs homologados em 2023, R$ 92,2 milhões.)
"""

# Acordos de leniência cumulativos por ano (2003–2023).
# NOTA: apenas o total (109) é verbatim do comunicado CADE de 06/10/2023; os
# valores intermediários são interpolação/composição para fechar nesse total,
# NÃO contagens ano a ano verificadas. Usar com essa ressalva.
SERIE_LENIENCIAS_CADE_2003_2023: dict[int, int] = {
    2003: 0,
    2004: 0,
    2005: 1,
    2006: 2,
    2007: 3,
    2008: 5,
    2009: 8,
    2010: 12,
    2011: 17,
    2012: 23,
    2013: 31,
    2014: 40,
    2015: 49,
    2016: 56,
    2017: 63,
    2018: 69,
    2019: 75,
    2020: 81,
    2021: 89,
    2022: 97,
    2023: 109,
}

# TCCs anuais médios (Saito 2021)
TCC_MEDIA_ANUAL_2012_2019: int = 47

# TCCs em 2023 (CADE DEE DT-001/2024)
TCC_2023: dict = {
    "homologados": 13,
    "valor_total_milhoes_brl": 92.2,
}

# Capacidade institucional (calibração de κ no modelo)
INVESTIGACOES_ANUAIS_CADE: int = 92  # CADE, balanço 2024
