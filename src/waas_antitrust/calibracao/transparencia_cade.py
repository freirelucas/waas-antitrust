"""Calibração contra o Portal da Transparência e fontes correlatas (R06).

**Status: placeholder estruturado.** Aguardando extração de dados de
capacidade institucional do CADE — número de servidores, decomposição
por cargo, orçamento autorizado vs. executado. Quando preenchido,
calibra dois parâmetros estruturais do modelo:

- **`INVESTIGACOES_ANUAIS_CADE`** (hoje 92, calibrado contra balanço
  2024): triangula com nº de procuradores e técnicos da SG/CADE.
- **`taxa_capacidade`** em `WaaSParametros` (hoje 0,5 arbitrário): fração
  do sistema simulado que pode ser processada por tique. A relação
  empírica é
  `taxa_capacidade ≈ servidores_SG / casos_potenciais_por_trimestre`.

Fontes primárias-alvo (verificar antes de citar verbatim):

- **Portal da Transparência** (`portaldatransparencia.gov.br`) — lotação
  e orçamento por órgão.
- **Painel Estatístico de Pessoal** (MGISP, `paineldepessoal.economia.gov.br`)
  — séries históricas de servidores ativos por órgão.
- **CADE — Acesso à Informação** (`gov.br/cade/acesso-a-informacao`) —
  organograma, lotação, orçamento publicado.
- **SIOP** (`siop.planejamento.gov.br`) — LOA e execução orçamentária
  por unidade.

Caveats antecipados:

- A capacidade do CADE é heterogênea entre as três unidades (SG,
  DEE, Tribunal). Sem decomposição interna, calibrar apenas o
  agregado.
- Variação interanual: 2022-2024 podem diferir por contratações,
  vacâncias, transferências. Usar séries históricas para média
  móvel de 3 anos quando possível.
- A relação `servidores → casos por tique` depende de produtividade
  individual e da complexidade do caso (digital tende a ser mais
  intensivo em técnicos do que conduta cartelizada clássica).
"""

from __future__ import annotations

# ---------------------------------------------------------------------
# Constantes a preencher — placeholders explícitos
# ---------------------------------------------------------------------

#: Número total de servidores ativos do CADE (lotação mais recente).
#: Fonte preferida: Painel Estatístico de Pessoal MGISP ou Portal da
#: Transparência. Marcar [?] se não verificável.
N_SERVIDORES_TOTAL: int | None = None

#: Decomposição por categoria funcional.
N_SERVIDORES_POR_CATEGORIA: dict[str, int | None] = {
    "eppgg": None,  # Especialistas em Política Pública e Gestão Governamental
    "procurador_federal": None,  # PFE/CADE
    "tecnico_administrativo": None,
    "conselheiro": None,  # Tribunal Administrativo (7 membros estatutários)
    "cargo_comissionado": None,  # DAS/FCPE
}

#: Distribuição interna entre as três unidades operacionais.
N_SERVIDORES_POR_UNIDADE: dict[str, int | None] = {
    "superintendencia_geral": None,  # SG/CADE — instrução e leniência
    "departamento_estudos_economicos": None,  # DEE
    "tribunal_administrativo": None,
}

#: Orçamento autorizado (Lei Orçamentária Anual — LOA) e execução
#: efetiva (Tesouro Gerencial / SIAFI), em reais.
ORCAMENTO_LOA_POR_ANO: dict[int, float | None] = {
    2022: None,
    2023: None,
    2024: None,
}
EXECUCAO_ORCAMENTARIA_POR_ANO: dict[int, float | None] = {
    2022: None,
    2023: None,
    2024: None,
}


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def disponivel() -> bool:
    """Indica se o conjunto principal de constantes foi preenchido."""
    return N_SERVIDORES_TOTAL is not None


def servidores_sg_calibrado(default: int = 50) -> int:
    """Número de servidores da SG/CADE — instrução e leniência.

    A Superintendência-Geral é o gargalo operacional do enforcement: é
    onde os PAs são instruídos, leniências negociadas e TCCs propostos.
    Para calibrar `taxa_capacidade` empiricamente, esta é a contagem
    relevante.

    Se a constante específica `N_SERVIDORES_POR_UNIDADE['superintendencia_geral']`
    estiver preenchida, retorna-a. Caso contrário, devolve o `default`
    (estimativa documentada de ordem de grandeza).
    """
    sg = N_SERVIDORES_POR_UNIDADE.get("superintendencia_geral")
    if sg is not None:
        return int(sg)
    return int(default)


def capacidade_efetiva_por_tique(
    trimestres_por_ano: int = 4,
    casos_por_servidor_ano: float = 2.0,
) -> int | None:
    """Estimativa empírica de quantos casos a SG/CADE pode processar por tique.

    A fórmula é simples — e essa simplicidade é deliberada porque
    qualquer modelo mais sofisticado dependeria de dados que não temos
    (heterogeneidade de complexidade, sazonalidade, vacâncias):

        capacidade_anual ≈ servidores_SG × casos_por_servidor_ano
        capacidade_tique  ≈ capacidade_anual / trimestres_por_ano

    Retorna `None` quando a contagem de servidores ainda não foi
    preenchida — sinaliza ao chamador que deve cair em fallback.

    `casos_por_servidor_ano` é estimativa documentada: ~2 instruções
    completas por ano por procurador/técnico sênior em casos complexos
    é a ordem de grandeza encontrada na literatura comparada
    (FTC/DOJ EUA). Calibrar com dados específicos do CADE em R03.
    """
    sg = N_SERVIDORES_POR_UNIDADE.get("superintendencia_geral")
    if sg is None:
        return None
    capacidade_anual = sg * casos_por_servidor_ano
    return max(1, int(capacidade_anual / trimestres_por_ano))


def resumo() -> str:
    """Resumo textual do estado de calibração."""
    if disponivel():
        return (
            f"Portal da Transparência calibrado: {N_SERVIDORES_TOTAL} servidores "
            f"totais; SG/CADE={N_SERVIDORES_POR_UNIDADE['superintendencia_geral']}; "
            f"capacidade ≈ {capacidade_efetiva_por_tique()} casos/tique."
        )
    return (
        "Portal da Transparência ainda em placeholder. Constantes-alvo: "
        "N_SERVIDORES_TOTAL, N_SERVIDORES_POR_UNIDADE['superintendencia_geral'], "
        "ORCAMENTO_LOA_POR_ANO. Ver docstring do módulo para procedimento."
    )
