"""Calibração contra Saito (2021) — "TCC na Lei nº 12.529/11".

Fonte primária verificada (PDF baixado e seção 3.7.7 conferida):
    Saito, Carolina (24/02/2021). *TCC na Lei nº 12.529/11.* Gabinete da
    Presidência do CADE, resultado da Consultoria PNUD/Brasil no projeto
    "Melhores práticas e procedimentos de negociação de TCC" (2019-2020).
    Universo: **349 TCCs firmados entre 04/07/2012 e 11/12/2019**.
    URL: https://cdn.cade.gov.br/Portal/centrais-de-conteudo/publicacoes/TCC%20na%20Lei%20n%C2%BA%2012.52911/TCC%20na%20Lei%20n%C2%BA%2012.529-11.pdf

Notas de extração (relevantes para a calibração de `D_disc_base_tcc`):

1. **Saito (2021) NÃO reporta mediana** do desconto, nem quartis ou
   desvio-padrão. Reporta **médias por posição na fila** de
   compromissários (Imagens 23 e 25, p. 38-39). Logo, qualquer "mediana"
   abaixo seria construção interpretativa — e este módulo evita.

2. **A decomposição por tipo de conduta NÃO está disponível para o
   desconto**. A Imagem 21 (p. 37) traz "alíquota média por conduta", que
   é a **taxa da multa**, não o desconto. Não confundir. Os números aqui
   são, portanto, derivados majoritariamente de TCCs de cartel — a
   transposição para conduta unilateral (alvo do WaaS) requer cuidado.

3. **Caveat de cobertura**: em 25,88% dos Requerimentos os documentos do
   CADE não abordam expressamente o desconto aplicado (p. 37).

O helper `d_base_tcc_calibrado` retorna por padrão a média mais
**conservadora** (Tribunal, qualquer compromissário = 15%), porque o
WaaS opera num contexto adversarial em que a firma frequentemente não é
a primeira a colaborar. Para análise específica de cartel-em-SG/CADE,
usar `MEDIA_DESCONTO_SG_1A_POSICAO` (43,43%) etc. explicitamente.
"""

from __future__ import annotations

# --- Bibliográficos -------------------------------------------------------

#: Número de TCCs analisados — verbatim do título da dissertação.
N_TCC_SAITO_2012_2019: int = 349

#: Período coberto.
PERIODO_SAITO: tuple[str, str] = ("2012-07-04", "2019-12-11")

#: Autoria e data de publicação.
AUTORIA_SAITO: str = "Carolina Saito"
DATA_PUBLICACAO_SAITO: str = "2021-02-24"

# --- Médias por posição na fila (SG/CADE), Imagem 23 p. 38 ----------------

#: Desconto médio na contribuição pecuniária do TCC, segundo a posição
#: do compromissário na fila e a fase processual SG/CADE (PA principal).
#: Fonte: Saito (2021), Imagem 23, p. 38.
MEDIA_DESCONTO_SG_POR_POSICAO: dict[int, float] = {
    1: 0.4343,  # 43,43%
    2: 0.3451,  # 34,51%
    3: 0.2022,  # 20,22%
    4: 0.1799,  # 17,99%
    5: 0.1677,  # 16,77%
    6: 0.1600,  # 16,00%
    7: 0.1500,  # 15,00%
    8: 0.1533,  # 15,33%
    9: 0.1500,  # 15,00%
}

# Convenções de uso individual.
MEDIA_DESCONTO_SG_1A_POSICAO: float = 0.4343
MEDIA_DESCONTO_SG_2A_POSICAO: float = 0.3451
MEDIA_DESCONTO_SG_3A_POSICAO: float = 0.2022

# --- Tribunal/CADE — qualquer compromissário, Imagem 25 p. 39 -------------

#: Desconto médio no Tribunal/CADE (segundo estágio processual), 1ª posição.
#: Por jurisprudência codificada, máximo de 15% para qualquer compromissário
#: nesta fase. Saito reporta média = 15% para 1ª posição.
MEDIA_DESCONTO_TRIBUNAL_1A_POSICAO: float = 0.1500

# --- Faixas codificadas pelo Guia CADE de TCC para cartel (jurisprudência) ----
#: Fonte secundária verificada (Guia CADE de TCC, 11/09/2017).
#: URL: https://cdn.cade.gov.br/Portal/centrais-de-conteudo/publicacoes/guias-do-cade/guia-tcc-atualizado-11-09-17.pdf
FAIXAS_DESCONTO_SG_GUIA_CADE: dict[int, tuple[float, float]] = {
    1: (0.30, 0.50),
    2: (0.25, 0.40),
    3: (0.0, 0.25),  # "até 25%"
}
FAIXAS_DESCONTO_TRIBUNAL: tuple[float, float] = (0.0, 0.15)  # "até 15%"

# --- Placeholders explicitamente NÃO REPORTADOS por Saito (2021) ----------

#: Mediana NÃO REPORTADA por Saito. Marcado None — não preencher sem fonte.
MEDIANA_DESCONTO_TCC_2012_2019: float | None = None

#: Quartis NÃO REPORTADOS por Saito.
Q1_DESCONTO_TCC_2012_2019: float | None = None
Q3_DESCONTO_TCC_2012_2019: float | None = None

#: Decomposição por tipo de conduta NÃO REPORTADA por Saito (a Imagem 21
#: traz alíquota de multa, não desconto). Não preencher por inferência.
MEDIANA_DESCONTO_POR_TIPO: dict[str, float | None] = {
    "cartel": None,
    "conduta_unilateral": None,
    "outras": None,
}


# --- Helpers --------------------------------------------------------------


def disponivel() -> bool:
    """Indica se a mediana (não reportada) foi eventualmente fornecida
    por extração futura ou fonte secundária.
    """
    return MEDIANA_DESCONTO_TCC_2012_2019 is not None


def d_base_tcc_calibrado(default: float = 0.10) -> float:
    """Desconto base do TCC clássico (`D_disc_base_tcc`) calibrado.

    Política de seleção (Saito 2021 já preenchido com dados reais):

    1. Se `MEDIANA_DESCONTO_TCC_2012_2019` estiver preenchido (i.e., uma
       mediana foi obtida via fonte alternativa ou recálculo), retorna-a.
    2. Caso contrário, retorna a **média do Tribunal/1ª posição** = 0,15,
       que é a estimativa mais conservadora consistente com Saito (2021)
       e com o teto codificado pelo Guia CADE de TCC (até 15% nesta
       fase, para qualquer compromissário).

    Argumento `default` é mantido por compatibilidade com chamadas
    anteriores, mas só é usado se nem a mediana nem a média Tribunal
    estiverem disponíveis (situação que não deveria ocorrer com este
    módulo preenchido). A faixa empírica útil para sensibilidade é
    `[0,15, 0,43]` (Tribunal → 1ª posição SG/CADE).
    """
    if MEDIANA_DESCONTO_TCC_2012_2019 is not None:
        return float(MEDIANA_DESCONTO_TCC_2012_2019)
    if MEDIA_DESCONTO_TRIBUNAL_1A_POSICAO is not None:
        return float(MEDIA_DESCONTO_TRIBUNAL_1A_POSICAO)
    return float(default)


def resumo() -> str:
    """Resumo textual do estado de calibração — útil para diagnóstico."""
    return (
        f"Saito ({AUTORIA_SAITO}, {DATA_PUBLICACAO_SAITO}): "
        f"{N_TCC_SAITO_2012_2019} TCCs ({PERIODO_SAITO[0]} a {PERIODO_SAITO[1]}). "
        f"Médias por posição SG/CADE: 1ª={MEDIA_DESCONTO_SG_1A_POSICAO:.2%}, "
        f"2ª={MEDIA_DESCONTO_SG_2A_POSICAO:.2%}, "
        f"3ª={MEDIA_DESCONTO_SG_3A_POSICAO:.2%}. "
        f"Tribunal/1ª posição={MEDIA_DESCONTO_TRIBUNAL_1A_POSICAO:.2%}. "
        f"Mediana NÃO REPORTADA por Saito (2021); fallback usado: Tribunal."
    )
