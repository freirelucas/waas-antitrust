"""Calibração da capacidade institucional do CADE (R06).

**Status: calibrado contra os Relatórios Integrados de Gestão (RIG)
2022, 2023 e 2024 — fonte primária verificada (TCU exige publicação
anual de toda autarquia federal).**

URLs dos RIGs (verificadas, HTTP 200):

- RIG 2022 (Lei 14.303/2022):
  https://cdn.cade.gov.br/Portal/acesso-a-informacao/Transpar%C3%AAncia%20e%20Presta%C3%A7%C3%A3o%20de%20Contas/2022/RIG_2022_Cade.pdf
- RIG 2023 (Lei 14.535/2023):
  https://cdn.cade.gov.br/Portal/acesso-a-informacao/Transpar%C3%AAncia%20e%20Presta%C3%A7%C3%A3o%20de%20Contas/2023/RIG-2023.pdf
- RIG 2024 (publicado em 25/06/2025; Lei 14.822/2024):
  https://cdn.cade.gov.br/Portal/acesso-a-informacao/Transpar%C3%AAncia%20e%20Presta%C3%A7%C3%A3o%20de%20Contas/2025/RIG%202024%20COMPLETO%202025.06.25.pdf

Página índice:
  https://www.gov.br/cade/pt-br/acesso-a-informacao/transparencia-e-prestacao-de-contas/relatorios-de-gestao

Referências secundárias que confirmam números (verificadas em rodada
anterior):
- CADE — notícia recorde de 2024 (14/01/2025).
- ConJur — Cordeiro, balanço de 2023 (30/12/2023).
- Mattos Filho — *Anticompetitive conduct enforcement 2024.*

Limitações importantes (caveats marcados como [?] no código):

- **Decomposição SG/DEE/Tribunal de servidores**: os RIGs reportam
  força de trabalho consolidada. Apenas o RIG 2024 (p. 110) declara
  "180 servidores na área-fim" — agregado que cobre SG/CADE + parte
  do DEE; usar como proxy de SG com caveat documentado.
- **Tabelas gráficas**: pdftotext não extrai gráficos. Para
  decomposição mais fina (e.g., por unidade administrativa interna),
  pedir planilha bruta via LAI ao Fala.BR / Cgesp/DAP do CADE.
- **Discrepâncias menores entre fontes**: ACs 2023 = 594 (RIG, fonte
  primária) vs. 579 (ConJur). Usamos RIG. Leniências históricas: 113
  (RIG 2024) vs. 109 (comunicado CADE 2023).
- **Mudança metodológica em 2021**: contagem de ACs antes/depois
  não comparável diretamente (RIG 2024, p. 74).
"""

from __future__ import annotations

# ---------------------------------------------------------------------
# Força de trabalho — RIG 2022-2024
# ---------------------------------------------------------------------

#: Servidores em exercício no CADE — verbatim do RIG.
#: 2022: NT CADE/2022 e RIG 2022 (p. 89); 2024: RIG (p. 109-110).
N_SERVIDORES_EM_EXERCICIO_POR_ANO: dict[int, int] = {
    2022: 287,
    2023: 311,
    2024: 326,
}

#: Total de pessoas (servidores + colaboradores externos) — RIG.
N_PESSOAS_TOTAL_POR_ANO: dict[int, int] = {
    2022: 524,
    2023: 545,
    2024: 569,
}

#: Fração de servidores provenientes de outras instituições (cedidos),
#: indicando alta dependência de pessoal não-próprio — RIG.
FRACAO_SERVIDORES_DE_OUTRAS_INSTITUICOES: dict[int, float] = {
    2022: 0.75,
    2023: 0.77,
    2024: 0.82,
}

#: Compat: número total mais recente verificado (RIG 2024).
N_SERVIDORES_TOTAL: int | None = 326

#: Servidores próprios do PGPE (Plano Geral de Cargos do Poder Executivo)
#: — quadro permanente do órgão. RIG 2024, p. 112.
N_SERVIDORES_PGPE_QUADRO_PROPRIO: int | None = 35

#: **Servidores na área-fim** (RIG 2024, p. 110): agregado de SG/CADE +
#: parte do DEE. Usamos como **proxy de SG** com caveat — a SG estrita
#: tem menos servidores; o DEE tem 5 unidades técnicas com algumas
#: dezenas. Sem decomposição mais fina nos RIGs publicados.
N_SERVIDORES_AREA_FIM: int | None = 180

# Compat com versão anterior (NT CADE 2022).
N_SERVIDORES_EFETIVOS_PROPRIOS: int | None = 34  # NT CADE 2022

#: Decomposição por categoria funcional.
N_SERVIDORES_POR_CATEGORIA: dict[str, int | None] = {
    # EPPGG: 200 cargos criados por Lei 12.529/2011; 65 lotados em 2023
    # (Nota Técnica CADE 2023 — déficit de ~67%).
    "eppgg": 65,
    # Procurador federal (PFE/CADE): contagem específica não publicada
    # nos RIGs (apenas estrutura qualitativa).
    "procurador_federal": None,  # [?]
    # Técnico administrativo: parte dos 326; sem decomposição direta.
    "tecnico_administrativo": None,  # [?]
    # Tribunal Administrativo: 7 membros estatutários (Lei 12.529 art. 6º).
    "conselheiro": 7,
    # Cargos comissionados (DAS/FCPE): sem decomposição nos RIGs.
    "cargo_comissionado": None,  # [?]
}

#: Distribuição por unidade operacional. **Caveat**: os RIGs não
#: publicam decomposição SG/DEE separada. Usamos "área-fim = 180"
#: como proxy de SG; DEE permanece `None`.
N_SERVIDORES_POR_UNIDADE: dict[str, int | None] = {
    # Proxy: agregado área-fim (RIG 2024). Para a SG estrita, ofício
    # LAI à Cgesp/DAP é o caminho.
    "superintendencia_geral": 180,
    "departamento_estudos_economicos": None,  # [?]
    "tribunal_administrativo": 7,
}

# ---------------------------------------------------------------------
# Orçamento — Ação 2807 (Promoção e Defesa da Concorrência)
# ---------------------------------------------------------------------

#: LOA total do CADE por ano, em reais. RIG 2022/2023/2024.
ORCAMENTO_LOA_TOTAL_BRL_POR_ANO: dict[int, float | None] = {
    2022: 42_769_864.00,  # Lei 14.303/2022
    2023: 42_769_864.00,  # Lei 14.535/2023 — sem aumento nominal vs 2022
    2024: 49_521_635.00,  # Lei 14.822/2024 (discricionário)
}

#: LOA específica da Ação 2807 (Promoção e Defesa da Concorrência) —
#: dotação inicial. Distinta do total (que inclui pessoal).
ORCAMENTO_LOA_ACAO_2807_INICIAL_POR_ANO: dict[int, float | None] = {
    2022: 41_815_432.00,
    2023: None,  # [?] — RIG 2023 reporta dotação atualizada (44.632.872)
    2024: None,  # [?] — RIG 2024 reporta atualizada (40.784.391)
}

#: LOA atualizada (com suplementações) e execução. RIG.
ORCAMENTO_LOA_ACAO_2807_ATUALIZADA_POR_ANO: dict[int, float | None] = {
    2022: 42_030_777.00,
    2023: 44_632_872.00,
    2024: 40_784_391.00,
}
EXECUCAO_ACAO_2807_POR_ANO: dict[int, float | None] = {
    2022: 41_863_484.11,  # 99,60% (RIG 2022 p. 101)
    2023: 44_364_137.35,  # 99,40% empenhado (RIG 2023 p. 104)
    2024: 40_702_990.67,  # 99,80% (RIG 2024 p. 120)
}

#: Compat com schema anterior (LOA total).
ORCAMENTO_LOA_POR_ANO: dict[int, float | None] = ORCAMENTO_LOA_TOTAL_BRL_POR_ANO

#: Execução orçamentária total (compat).
EXECUCAO_ORCAMENTARIA_POR_ANO: dict[int, float | None] = EXECUCAO_ACAO_2807_POR_ANO

#: TIC dentro da Ação 2807, em reais. RIG.
GASTO_TIC_ACAO_2807_BRL_POR_ANO: dict[int, float | None] = {
    2022: 6_777_439.94,
    2023: None,  # [?]
    2024: 9_163_362.97,
}

# ---------------------------------------------------------------------
# Fluxo de processos — RIG (fonte primária)
# ---------------------------------------------------------------------

#: Atos de Concentração notificados ao CADE.
#: NÃO confundir com investigação de conduta (PAs).
ATOS_CONCENTRACAO_NOTIFICADOS_POR_ANO: dict[int, int | None] = {
    2022: 660,
    2023: 594,  # RIG 2023 (594) — primária; ConJur reportou 579
    2024: 712,  # recorde histórico
}

#: Valor agregado das operações notificadas, em reais (RIG).
VALOR_OPERACOES_ACS_BRL_POR_ANO: dict[int, float | None] = {
    2022: 1_560_000_000_000.0,  # R$ 1,56 trilhões
    2023: 905_600_000_000.0,
    2024: 1_070_000_000_000.0,
}

#: **Investigações instauradas pela SG** — categoria ampla que cobre
#: PAs de conduta + procedimentos preparatórios + inquéritos
#: administrativos. Esta é a categoria de capacidade relevante para
#: o WaaS (RIG, série 2022-2024).
INVESTIGACOES_INSTAURADAS_SG_POR_ANO: dict[int, int | None] = {
    2022: 103,
    2023: 63,
    2024: 73,
}

#: Investigações concluídas pela SG (RIG).
INVESTIGACOES_CONCLUIDAS_SG_POR_ANO: dict[int, int | None] = {
    2022: 111,
    2023: 106,
    2024: 89,
}

#: Estoque de investigações em curso no final do ano (RIG).
ESTOQUE_INVESTIGACOES_SG_POR_ANO: dict[int, int | None] = {
    2022: 247,
    2023: 177,
    2024: 185,
}

#: PAs de conduta especificamente instaurados — categoria mais
#: restrita (ConJur balanço 2023). RIGs reportam o agregado
#: (investigações), não decomposição.
PROCESSOS_ADMINISTRATIVOS_CONDUTA_POR_ANO: dict[int, int | None] = {
    2023: 14,  # ConJur (14 PAs + 5 TCC)
    2024: None,  # [?] não decomposto no RIG
}

#: Acordos de leniência assinados (RIG).
LENIENCIAS_ASSINADAS_POR_ANO: dict[int, int | None] = {
    2022: 1,  # + 1 Leniência Plus
    2023: 2,
    2024: 4,
}

#: Total cumulativo de leniências assinadas (RIG 2024, p. 85).
TOTAL_LENIENCIAS_HISTORICAS: int = 113

#: Operações de busca e apreensão executadas (RIG).
OPERACOES_BUSCA_APREENSAO_POR_ANO: dict[int, int | None] = {
    2022: 2,
    2023: 2,
    2024: 3,  # 16 mandados em 3 operações
}

#: Denúncias recebidas via Clique Denúncia (canal CADE de denúncia
#: anônima). RIG 2024, p. 85.
DENUNCIAS_CLIQUE_DENUNCIA_POR_ANO: dict[int, int | None] = {
    2022: None,  # apenas "121% acima de 2021" (RIG 2022)
    2023: None,  # [?]
    2024: 3_725,
}

#: Valor agregado de multas com trânsito em julgado em 2024 (RIG).
MULTAS_TRANSITO_JULGADO_2024_BRL: dict[str, float] = {
    "nominal": 158_180_000.0,
    "atualizado": 161_940_000.0,
    "arrecadado": 29_170_000.0,
}

#: Compat com versão anterior — multas aplicadas anuais (ConJur).
MULTAS_APLICADAS_BRL_POR_ANO: dict[int, float | None] = {
    2023: 114_500_000.0,  # ConJur balanço 2023
    2024: 158_180_000.0,  # RIG 2024 — nominal com trânsito em julgado
}

#: Tempo médio de análise de Ato de Concentração (RIG).
TEMPO_MEDIO_AC_SUMARIO_DIAS_POR_ANO: dict[int, float | None] = {
    2022: 21.4,
    2023: 12.6,
    2024: 15.1,
}
TEMPO_MEDIO_AC_ORDINARIO_DIAS_POR_ANO: dict[int, float | None] = {
    2022: 125.6,
    2023: 116.7,
    2024: 92.1,  # RIG 2024 (notícia 14/01/2025 reportou 93,9; RIG é primária)
}

#: Compat com schema anterior (ordinário).
TEMPO_MEDIO_ANALISE_AC_DIAS_POR_ANO: dict[int, float | None] = TEMPO_MEDIO_AC_ORDINARIO_DIAS_POR_ANO

# ---------------------------------------------------------------------
# Universo regulado — Lei 12.529/2011 art. 88
# ---------------------------------------------------------------------

#: Limiares de notificação obrigatória de Ato de Concentração ao CADE
#: (Lei 12.529 art. 88; Portaria Interministerial 994/2012), em reais.
LIMIARES_NOTIFICACAO_AC_BRL: tuple[float, float] = (75_000_000.0, 750_000_000.0)

#: Universo estimado de firmas reguladas (sem corte primário publicado).
UNIVERSO_FIRMAS_REGULADAS_ESTIMATIVA: tuple[int, int] = (5_000, 20_000)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def disponivel() -> bool:
    """Indica se o conjunto principal de constantes foi preenchido."""
    return N_SERVIDORES_TOTAL is not None


def servidores_sg_calibrado(default: int = 180) -> int:
    """Servidores da SG/CADE — gargalo operacional do enforcement.

    Retorna `N_SERVIDORES_POR_UNIDADE["superintendencia_geral"]` (que
    hoje é o proxy "área-fim = 180" do RIG 2024). Default elevado a
    180 (de 50 anterior) refletindo o dado primário.

    Para a SG estrita (sem DEE e sem áreas-fim auxiliares), ofício
    LAI ao Fala.BR é o caminho documentado.
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

    Com SG=180 (RIG 2024, proxy área-fim) e 2 casos/ano por servidor:
        capacidade_anual ≈ 180 × 2 = 360 casos/ano
        capacidade_tique ≈ 90 casos/trimestre

    Compare com o ESTOQUE médio observado (~200 investigações em curso
    em qualquer momento) — a saturação é parcial, consistente com a
    capacidade nominal aqui calculada.

    `casos_por_servidor_ano = 2.0` é estimativa documentada (ordem de
    grandeza FTC/DOJ); calibrar com dados específicos do CADE em R03.
    """
    sg = N_SERVIDORES_POR_UNIDADE.get("superintendencia_geral")
    if sg is None:
        return None
    capacidade_anual = sg * casos_por_servidor_ano
    return max(1, int(capacidade_anual / trimestres_por_ano))


def deficit_eppgg() -> float:
    """Déficit de EPPGGs vs. 200 cargos criados (Nota Técnica CADE 2023)."""
    cargos_criados = 200
    lotados = N_SERVIDORES_POR_CATEGORIA["eppgg"]
    if lotados is None:
        return 0.0
    return (cargos_criados - lotados) / cargos_criados


def execucao_orcamentaria_relativa(ano: int) -> float | None:
    """Razão executado / LOA atualizada (Ação 2807) para o ano.

    RIGs mostram execução próxima de 100% (99,4-99,8%) em 2022-2024
    — o gargalo do CADE não é orçamentário, é de pessoal e
    procedimental.
    """
    loa = ORCAMENTO_LOA_ACAO_2807_ATUALIZADA_POR_ANO.get(ano)
    exec_ = EXECUCAO_ACAO_2807_POR_ANO.get(ano)
    if loa is None or exec_ is None or loa <= 0:
        return None
    return exec_ / loa


def resumo() -> str:
    """Resumo textual do estado de calibração — útil para diagnóstico."""
    if not disponivel():
        return "Portal da Transparência / RIG ainda em placeholder."
    return (
        f"RIG CADE 2024: {N_SERVIDORES_TOTAL} servidores em exercício "
        f"(82% cedidos); área-fim = {N_SERVIDORES_AREA_FIM} (proxy SG); "
        f"Tribunal = 7; EPPGG = "
        f"{N_SERVIDORES_POR_CATEGORIA['eppgg']}/200 (déficit "
        f"{deficit_eppgg():.0%}). "
        f"LOA total = R$ {ORCAMENTO_LOA_TOTAL_BRL_POR_ANO[2024] / 1e6:.1f} mi; "
        f"execução Ação 2807 = {execucao_orcamentaria_relativa(2024):.1%}. "
        f"ACs 2024 = {ATOS_CONCENTRACAO_NOTIFICADOS_POR_ANO[2024]} (recorde); "
        f"investigações instauradas SG 2024 = "
        f"{INVESTIGACOES_INSTAURADAS_SG_POR_ANO[2024]}; "
        f"leniências 2024 = {LENIENCIAS_ASSINADAS_POR_ANO[2024]}; "
        f"capacidade ≈ {capacidade_efetiva_por_tique()} casos/tique."
    )
