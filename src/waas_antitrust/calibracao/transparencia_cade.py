"""Calibração da capacidade institucional do CADE (R06).

**Status: preenchido parcialmente, com marcações `[?]` explícitas.**

Fontes primárias verificadas (URLs reais):

- **CADE — notícia institucional 14/01/2025** (recorde 2024 em ACs):
  https://www.gov.br/cade/pt-br/assuntos/noticias/cade-bate-recorde-de-notificacao-de-atos-de-concentracao-em-2024
- **CADE — Tribunal Administrativo** (composição estatutária 7 membros,
  Lei 12.529/2011 art. 6º): https://www.gov.br/cade/pt-br/composicao/tribunal-administrativo/membros
- **CADE — Departamento de Estudos Econômicos**:
  https://www.gov.br/cade/pt-br/acesso-a-informacao/institucional/competencias/departamento-de-estudos-economicos
- **ConJur — Alexandre Cordeiro, balanço CADE 2023** (30/12/2023):
  https://www.conjur.com.br/2023-dez-30/balanco-da-atuacao-do-cade-e-novas-perspectivas-para-2024/
- **Nota Técnica CADE 24/05/2022 e 2023** (reproduzidas em
  Direção Concursos — texto integral citado verbatim na publicação):
  https://www.direcaoconcursos.com.br/noticias/concurso-cade-solicitado-2023
  https://www.direcaoconcursos.com.br/noticias/concurso-eppgg-cade-solicitado-2023/

Fontes-alvo **não acessíveis via WebFetch** (retornaram 405/403 ou
interface dinâmica): Portal da Transparência por órgão (`30211`),
SIOP, Painel Estatístico de Pessoal MGISP, PDF da Carta de Serviços
2023. Para preenchimento futuro destas fontes, recomenda-se:

1. **Relatórios Integrados de Gestão** (TCU exige publicação anual) —
   PDF disponível em `cdn.cade.gov.br`; baixar e usar `pdftotext`.
2. **SIOP via download Excel** (interface não-fetchable, mas exportação
   tabular é pública para UO 30211).
3. **Painel de Receita Federal** (abr-2026) para o universo regulado
   por faixa de faturamento.

**Decomposição SG/DEE/Tribunal não está publicada** em fonte indexada —
o organograma é qualitativo (SG: 1 superintendente + 2 adjuntos + 9
CGAAs; DEE: 5 unidades; Tribunal: 7 conselheiros). Headcount por
unidade fica como `None` até verificação direta.

**Distinção crítica entre ACs e PAs** (não confundir):

- **Atos de Concentração (AC)**: análise prévia de fusões/aquisições
  com faturamento acima do limiar (Lei 12.529 art. 88: R$ 750 mi / R$
  75 mi). 712 notificados em 2024 (recorde). Procedimento de triagem,
  não investigação de conduta.
- **Processos Administrativos (PA) de conduta**: investigação de
  infração à ordem econômica. **Apenas 14 instaurados em 2023**. Esta
  é a categoria que o WaaS endereça. Em 2024 H1: 6 PAs + 5 preparatórios
  + 4 inquéritos administrativos.
"""

from __future__ import annotations

# ---------------------------------------------------------------------
# Servidores — verificados onde possível, [?] caso contrário
# ---------------------------------------------------------------------

#: Total de servidores em exercício no CADE.
#: Fonte: Nota Técnica CADE 24/05/2022, reportada em Direção Concursos.
#: Caveat: dado de 2022-2023; concurso CNU 2024 (30 vagas EPPGG) só
#: começa a impactar a lotação em 2024-2025.
N_SERVIDORES_TOTAL: int | None = 292

#: Servidores efetivos próprios (excluindo cedidos/comissionados externos).
#: Fonte: mesma Nota Técnica CADE de 2022.
N_SERVIDORES_EFETIVOS_PROPRIOS: int | None = 34

#: Decomposição por categoria funcional.
N_SERVIDORES_POR_CATEGORIA: dict[str, int | None] = {
    # EPPGG (Especialista em Política Pública e Gestão Governamental):
    # 200 cargos criados por lei (Lei 12.529/2011), apenas 65 lotados em
    # 2023 (déficit 59,5-67%). Contagem alternativa: 81 em exercício se
    # incluir 25 em DAS/FCPE.
    "eppgg": 65,
    # Procurador federal (PFE/CADE): estrutura tem 2 coordenações (CGEP +
    # CGCJ); contagem exata não publicada em fonte indexada.
    "procurador_federal": None,  # [?]
    # Técnico administrativo: parte do total 292; sem decomposição.
    "tecnico_administrativo": None,  # [?]
    # Tribunal Administrativo: 7 membros estatutários (Lei 12.529/2011
    # art. 6º — 1 presidente + 6 conselheiros).
    "conselheiro": 7,
    # Cargos comissionados (DAS/FCPE): parte dos 292, sem decomposição.
    "cargo_comissionado": None,  # [?]
}

#: Distribuição interna entre as três unidades operacionais.
#: NÃO PUBLICADA em fonte indexada — qualitativo apenas:
#:   - SG/CADE: 1 superintendente + 2 adjuntos + 9 CGAAs
#:   - DEE: 5 unidades técnicas
#:   - Tribunal: 7 conselheiros estatutários
#: Para preencher: usar Relatório Integrado de Gestão (PDF do TCU).
N_SERVIDORES_POR_UNIDADE: dict[str, int | None] = {
    "superintendencia_geral": None,  # [?]
    "departamento_estudos_economicos": None,  # [?]
    "tribunal_administrativo": 7,  # estatutário
}

# ---------------------------------------------------------------------
# Orçamento — Portal da Transparência inacessível via WebFetch
# ---------------------------------------------------------------------

#: Orçamento autorizado (Lei Orçamentária Anual — LOA), em reais.
#: Fontes: SIOP UO 30211 / Tesouro Gerencial — acesso direto necessário.
#: Referência secundária (não verificada): faixa R$ 120-150 mi/ano [?].
ORCAMENTO_LOA_POR_ANO: dict[int, float | None] = {
    2022: None,  # [?]
    2023: None,  # [?]
    2024: None,  # [?]
}

#: Execução orçamentária (SIAFI), em reais. Idem.
EXECUCAO_ORCAMENTARIA_POR_ANO: dict[int, float | None] = {
    2022: None,  # [?]
    2023: None,  # [?]
    2024: None,  # [?]
}

# ---------------------------------------------------------------------
# Fluxo de processos — fontes verificadas
# ---------------------------------------------------------------------

#: Atos de Concentração notificados ao CADE por ano (NÃO confundir com
#: investigações de conduta — são análise prévia de fusões/aquisições).
#: Fontes: CADE notícia 14/01/2025 (2024); ConJur balanço 2023.
ATOS_CONCENTRACAO_NOTIFICADOS_POR_ANO: dict[int, int | None] = {
    2023: 579,
    2024: 712,  # recorde histórico
}

#: Processos Administrativos de conduta INSTAURADOS por ano. Esta é a
#: categoria relevante para o WaaS — investigação de infração à ordem
#: econômica.
#: Fonte: ConJur balanço 2023 (14 PAs + 5 TCC); Madrona 2024 H1
#: (6 PAs + 5 preparatórios + 4 inquéritos).
PROCESSOS_ADMINISTRATIVOS_CONDUTA_POR_ANO: dict[int, int | None] = {
    2023: 14,
    2024: None,  # [?] — só primeiro semestre publicado (6); anualização
}

#: Acordos de leniência ASSINADOS por ano.
#: Fonte: Mattos Filho — 2024 retrospective; ConJur 2023.
LENIENCIAS_ASSINADAS_POR_ANO: dict[int, int | None] = {
    2022: 1,
    2023: 2,
    2024: 4,
}

#: Valor agregado de multas aplicadas pelo CADE, em reais.
#: Fonte: ConJur balanço 2023 (R$ 114,5 mi); Mattos Filho 2024
#: ("quase triplicaram", sem valor auditado).
MULTAS_APLICADAS_BRL_POR_ANO: dict[int, float | None] = {
    2023: 114_500_000.0,
    2024: None,  # [?] — "quase triplicaram"
}

#: Tempo médio de análise de Ato de Concentração ordinário, em dias.
#: Fonte: CADE notícia 14/01/2025.
TEMPO_MEDIO_ANALISE_AC_DIAS_POR_ANO: dict[int, float | None] = {
    2023: 117.0,
    2024: 93.9,
}

# ---------------------------------------------------------------------
# Universo regulado — Lei 12.529/2011 art. 88
# ---------------------------------------------------------------------

#: Limiares de notificação obrigatória de Ato de Concentração ao CADE
#: (Lei 12.529/2011, art. 88, com atualização Portaria
#: Interministerial 994/2012). Tupla (faturamento_menor_grupo,
#: faturamento_maior_grupo) em reais.
LIMIARES_NOTIFICACAO_AC_BRL: tuple[float, float] = (75_000_000.0, 750_000_000.0)

#: Universo de empresas reguladas (CNPJs sob jurisdição da Lei 12.529).
#: NÃO PUBLICADO em corte específico nas bases verificadas. Estimativa
#: razoável: 5.000 a 20.000 firmas com receita ≥ R$ 75 mi/ano. Tratar
#: como variável de varredura Sobol.
UNIVERSO_FIRMAS_REGULADAS_ESTIMATIVA: tuple[int, int] = (5_000, 20_000)


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

    Se `N_SERVIDORES_POR_UNIDADE['superintendencia_geral']` estiver
    preenchida, retorna-a. Caso contrário, devolve o `default`
    (estimativa documentada de ordem de grandeza — não verificada em
    fonte primária).
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

    Fórmula:
        capacidade_anual ≈ servidores_SG × casos_por_servidor_ano
        capacidade_tique  ≈ capacidade_anual / trimestres_por_ano

    Retorna `None` quando a contagem de servidores da SG ainda não foi
    preenchida — sinaliza ao chamador que deve cair em fallback
    (e.g., `INVESTIGACOES_ANUAIS_CADE/4`).

    `casos_por_servidor_ano = 2.0` é estimativa documentada (ordem de
    grandeza encontrada na literatura FTC/DOJ); calibrar com dados
    específicos do CADE em R03.
    """
    sg = N_SERVIDORES_POR_UNIDADE.get("superintendencia_geral")
    if sg is None:
        return None
    capacidade_anual = sg * casos_por_servidor_ano
    return max(1, int(capacidade_anual / trimestres_por_ano))


def deficit_eppgg() -> float:
    """Déficit relativo de EPPGGs em relação aos 200 cargos criados por lei.

    Fonte: Nota Técnica CADE 2023 estima déficit de 59,5% a 67%.
    Cálculo direto: (200 − 65) / 200 = 0,675.
    """
    cargos_criados = 200
    lotados = N_SERVIDORES_POR_CATEGORIA["eppgg"]
    if lotados is None:
        return 0.0
    return (cargos_criados - lotados) / cargos_criados


def resumo() -> str:
    """Resumo textual do estado de calibração — útil para diagnóstico."""
    if disponivel():
        ac_2024 = ATOS_CONCENTRACAO_NOTIFICADOS_POR_ANO.get(2024)
        pa_2023 = PROCESSOS_ADMINISTRATIVOS_CONDUTA_POR_ANO.get(2023)
        return (
            f"Portal da Transparência: {N_SERVIDORES_TOTAL} servidores totais "
            f"(2022-2023); EPPGG lotados = "
            f"{N_SERVIDORES_POR_CATEGORIA['eppgg']}/200 (déficit "
            f"{deficit_eppgg():.0%}); Tribunal = "
            f"{N_SERVIDORES_POR_UNIDADE['tribunal_administrativo']} conselheiros. "
            f"ACs 2024 = {ac_2024} (recorde); PAs de conduta 2023 = {pa_2023}. "
            f"Decomposição SG/DEE/Tribunal e orçamento LOA pendentes "
            f"(Portal da Transparência inacessível via WebFetch)."
        )
    return "Portal da Transparência ainda em placeholder."
