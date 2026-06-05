"""Testes do módulo `calibracao/transparencia_cade.py` (R06).

Após a primeira rodada de extração: o módulo deixa de ser placeholder
puro e ganha dados verificados de fontes primárias (CADE 2025; ConJur
2023; Notas Técnicas CADE 2022/2023). Constantes não verificáveis em
fonte primária seguem marcadas como `None` com docstring explicativo.
"""

from __future__ import annotations

from waas_antitrust.calibracao import transparencia_cade as tcade

# ----------------------------------------------------------------------
# Constantes verificadas (fontes primárias)
# ----------------------------------------------------------------------


def test_total_servidores_eh_292():
    """Nota Técnica CADE 24/05/2022 (verificada via Direção Concursos)."""
    assert tcade.N_SERVIDORES_TOTAL == 292


def test_servidores_efetivos_proprios_eh_34():
    """Mesma Nota Técnica CADE 2022."""
    assert tcade.N_SERVIDORES_EFETIVOS_PROPRIOS == 34


def test_eppgg_lotados_eh_65():
    """Nota Técnica CADE 2023 — 65 EPPGGs lotados de 200 cargos criados."""
    assert tcade.N_SERVIDORES_POR_CATEGORIA["eppgg"] == 65


def test_tribunal_administrativo_eh_7_estatutario():
    """Lei 12.529/2011 art. 6º — 7 membros (1 presidente + 6 conselheiros)."""
    assert tcade.N_SERVIDORES_POR_CATEGORIA["conselheiro"] == 7
    assert tcade.N_SERVIDORES_POR_UNIDADE["tribunal_administrativo"] == 7


# ----------------------------------------------------------------------
# Marcações [?] — constantes não verificáveis em fonte primária
# ----------------------------------------------------------------------


def test_procuradores_e_tecnicos_nao_publicados():
    """PFE/CADE e técnicos não têm contagem em fonte indexada."""
    assert tcade.N_SERVIDORES_POR_CATEGORIA["procurador_federal"] is None
    assert tcade.N_SERVIDORES_POR_CATEGORIA["tecnico_administrativo"] is None
    assert tcade.N_SERVIDORES_POR_CATEGORIA["cargo_comissionado"] is None


def test_decomposicao_sg_dee_nao_publicada():
    """Apenas Tribunal (7) tem headcount conhecido; SG/DEE pendentes."""
    assert tcade.N_SERVIDORES_POR_UNIDADE["superintendencia_geral"] is None
    assert tcade.N_SERVIDORES_POR_UNIDADE["departamento_estudos_economicos"] is None


def test_orcamento_pendente():
    """Portal da Transparência (UO 30211) bloqueia WebFetch — LOA pendente."""
    assert all(v is None for v in tcade.ORCAMENTO_LOA_POR_ANO.values())
    assert all(v is None for v in tcade.EXECUCAO_ORCAMENTARIA_POR_ANO.values())


# ----------------------------------------------------------------------
# Fluxo de processos — verificados
# ----------------------------------------------------------------------


def test_atos_concentracao_2024_eh_712_recorde():
    """CADE notícia 14/01/2025 — 712 ACs em 2024 (recorde histórico)."""
    assert tcade.ATOS_CONCENTRACAO_NOTIFICADOS_POR_ANO[2024] == 712
    # 2023: 579 (também verificado em ConJur)
    assert tcade.ATOS_CONCENTRACAO_NOTIFICADOS_POR_ANO[2023] == 579


def test_pas_de_conduta_2023_eh_14_NAO_eh_712():
    """Distinção crítica: 712 = ACs (fusões); 14 = PAs de conduta.
    Esta é a categoria relevante para o WaaS."""
    assert tcade.PROCESSOS_ADMINISTRATIVOS_CONDUTA_POR_ANO[2023] == 14
    # 2024: H1 publicado (6); anualização pendente.
    assert tcade.PROCESSOS_ADMINISTRATIVOS_CONDUTA_POR_ANO[2024] is None


def test_leniencias_assinadas_2022_2023_2024():
    """Mattos Filho — 2024 retrospective + ConJur 2023."""
    assert tcade.LENIENCIAS_ASSINADAS_POR_ANO[2022] == 1
    assert tcade.LENIENCIAS_ASSINADAS_POR_ANO[2023] == 2
    assert tcade.LENIENCIAS_ASSINADAS_POR_ANO[2024] == 4


def test_multas_2023_eh_114_5_mi():
    """ConJur balanço 2023."""
    assert tcade.MULTAS_APLICADAS_BRL_POR_ANO[2023] == 114_500_000.0
    assert tcade.MULTAS_APLICADAS_BRL_POR_ANO[2024] is None  # [?]


def test_tempo_medio_ac_caiu_de_117_para_94_dias():
    """CADE notícia 14/01/2025 — 117 → 93,9 dias."""
    assert tcade.TEMPO_MEDIO_ANALISE_AC_DIAS_POR_ANO[2023] == 117.0
    assert tcade.TEMPO_MEDIO_ANALISE_AC_DIAS_POR_ANO[2024] == 93.9


def test_limiares_notificacao_lei_12_529():
    """Lei 12.529/2011 art. 88 + Portaria Interministerial 994/2012."""
    assert tcade.LIMIARES_NOTIFICACAO_AC_BRL == (75_000_000.0, 750_000_000.0)


def test_universo_firmas_eh_estimativa_intervalar():
    """Sem dado primário; tratar como variável de varredura Sobol."""
    lo, hi = tcade.UNIVERSO_FIRMAS_REGULADAS_ESTIMATIVA
    assert lo == 5_000
    assert hi == 20_000
    assert lo < hi


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def test_disponivel_eh_true_apos_extracao_basica():
    """Com N_SERVIDORES_TOTAL preenchido (292), `disponivel()` é True."""
    assert tcade.disponivel() is True


def test_servidores_sg_devolve_default_porque_unidade_pendente():
    """SG ainda em None ⇒ helper devolve `default` (fallback documentado)."""
    assert tcade.servidores_sg_calibrado(default=50) == 50
    assert tcade.servidores_sg_calibrado(default=80) == 80


def test_servidores_sg_devolve_dado_real_quando_preenchido(monkeypatch):
    """Quando SG for preenchida (e.g. via RIG), helper devolve o valor real."""
    monkeypatch.setitem(tcade.N_SERVIDORES_POR_UNIDADE, "superintendencia_geral", 73)
    assert tcade.servidores_sg_calibrado() == 73
    assert tcade.servidores_sg_calibrado(default=999) == 73


def test_capacidade_efetiva_eh_none_enquanto_sg_pendente():
    """Sinaliza ao chamador para usar `INVESTIGACOES_ANUAIS_CADE/4`."""
    assert tcade.capacidade_efetiva_por_tique() is None


def test_capacidade_efetiva_calcula_quando_sg_preenchido(monkeypatch):
    """SG=80, 2 casos/ano/servidor → 160/ano → 40/trimestre."""
    monkeypatch.setitem(tcade.N_SERVIDORES_POR_UNIDADE, "superintendencia_geral", 80)
    cap = tcade.capacidade_efetiva_por_tique(trimestres_por_ano=4, casos_por_servidor_ano=2.0)
    assert cap == 40


def test_deficit_eppgg_eh_proximo_de_67_por_cento():
    """(200 − 65) / 200 = 0,675 — bate com a Nota Técnica CADE 2023."""
    deficit = tcade.deficit_eppgg()
    assert 0.66 < deficit < 0.69


# ----------------------------------------------------------------------
# Resumo textual
# ----------------------------------------------------------------------


def test_resumo_inclui_numeros_chave():
    texto = tcade.resumo()
    assert "292" in texto
    assert "65" in texto  # EPPGG lotados
    assert "7" in texto  # conselheiros
    assert "712" in texto  # ACs 2024
    assert "14" in texto  # PAs 2023


# ----------------------------------------------------------------------
# Estrutura estável (compat com testes anteriores)
# ----------------------------------------------------------------------


def test_categorias_funcionais_estaveis():
    esperadas = {
        "eppgg",
        "procurador_federal",
        "tecnico_administrativo",
        "conselheiro",
        "cargo_comissionado",
    }
    assert set(tcade.N_SERVIDORES_POR_CATEGORIA.keys()) == esperadas


def test_unidades_operacionais_estaveis():
    esperadas = {
        "superintendencia_geral",
        "departamento_estudos_economicos",
        "tribunal_administrativo",
    }
    assert set(tcade.N_SERVIDORES_POR_UNIDADE.keys()) == esperadas


def test_orcamento_cobre_anos_recentes():
    assert set(tcade.ORCAMENTO_LOA_POR_ANO.keys()) == {2022, 2023, 2024}
    assert set(tcade.EXECUCAO_ORCAMENTARIA_POR_ANO.keys()) == {2022, 2023, 2024}
