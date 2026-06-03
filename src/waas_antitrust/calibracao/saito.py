"""Calibração contra Saito (2021) — placeholder formal.

**Status: placeholder.** Os campos abaixo são *espaços de calibração*
para a primeira ponta de R03; preenchê-los exige extração manual da
tabela de TCCs da dissertação de Saito (verificável via repositório
institucional CADE/PNUD). Quando preenchidos, este módulo fornece a
mediana e a dispersão do desconto observado em TCCs CADE 2012-2019,
calibrando `D_disc_base_tcc` no modelo.

Fonte primária:
    Saito, P. (2021). *Termo de Compromisso de Cessação na Lei nº
    12.529/11.* Dissertação CADE/PNUD. 349 TCCs analisados entre julho
    de 2012 e dezembro de 2019.

Procedimento para preencher (manual):
1. Localizar a dissertação no repositório CADE/PNUD ou via solicitação
   LAI ao CADE/SG.
2. Extrair, da tabela principal, o desconto percentual (sobre a
   contribuição pecuniária) negociado em cada TCC. Saito tabula isso por
   ano e por tipo de conduta.
3. Calcular mediana e quartis (Q1, Q3) — o ideal seria também por tipo
   de conduta (cartel × conduta unilateral × outras).
4. Sobrescrever `MEDIANA_DESCONTO_TCC_2012_2019` e demais constantes;
   remover o `None`.

Quando preenchido, este módulo será fonte primária para o parâmetro
`D_disc_base_tcc` em `cenarios.py` (Regimes B e C). Hoje usamos
estimativa intermediária de 10% — ver `mecanismo.md` § "Vetor de quebra A".
"""

from __future__ import annotations

# Estatística central a preencher: mediana de desconto sobre contribuição
# pecuniária nos TCCs analisados por Saito (2012-2019).
MEDIANA_DESCONTO_TCC_2012_2019: float | None = None

# Dispersão (quartis 25/75). Útil para varredura de sensibilidade.
Q1_DESCONTO_TCC_2012_2019: float | None = None
Q3_DESCONTO_TCC_2012_2019: float | None = None

# Decomposição por tipo de conduta (cartel × conduta unilateral × outras).
# Saito tabula isso; permite calibrar D_base separadamente por categoria.
MEDIANA_DESCONTO_POR_TIPO: dict[str, float | None] = {
    "cartel": None,
    "conduta_unilateral": None,
    "outras": None,
}

# Número de TCCs cobertos (verbatim do título da dissertação).
N_TCC_SAITO_2012_2019: int = 349

# Período coberto.
PERIODO_SAITO: tuple[str, str] = ("2012-07", "2019-12")


def disponivel() -> bool:
    """Indica se as constantes principais estão preenchidas (não-None)."""
    return MEDIANA_DESCONTO_TCC_2012_2019 is not None


def resumo() -> str:
    """Resumo textual do estado de calibração — útil para diagnóstico."""
    if disponivel():
        return (
            f"Saito (2021) calibrado: mediana={MEDIANA_DESCONTO_TCC_2012_2019:.2%}, "
            f"Q1={Q1_DESCONTO_TCC_2012_2019:.2%}, Q3={Q3_DESCONTO_TCC_2012_2019:.2%} "
            f"sobre {N_TCC_SAITO_2012_2019} TCCs ({PERIODO_SAITO[0]} a "
            f"{PERIODO_SAITO[1]})."
        )
    return (
        f"Saito (2021) ainda em placeholder. {N_TCC_SAITO_2012_2019} TCCs "
        f"({PERIODO_SAITO[0]} a {PERIODO_SAITO[1]}) aguardando extração manual "
        "da tabela principal. Ver docstring do módulo para procedimento."
    )
