"""Testes do módulo `calibracao/transparencia_cade.py` — RIG CADE 2022-2024.

Após a extração do Relatório Integrado de Gestão (RIG) do CADE em três
exercícios (PDFs primários baixados e parseados via pdftotext), o módulo
contém uma série temporal verbatim de força de trabalho, orçamento e
fluxo de processos. Estes testes validam constantes verificadas + as
marcações `[?]` explícitas para o que segue não publicado nos RIGs.
"""

from __future__ import annotations

from waas_antitrust.calibracao import transparencia_cade as tcade

# ----------------------------------------------------------------------
# Força de trabalho — série RIG 2022-2024
# ----------------------------------------------------------------------


def test_servidores_em_exercicio_serie_2022_2024():
    """RIG 2022 (287), 2023 (311), 2024 (326) — verbatim das p. 89, 96, 109-110."""
    assert tcade.N_SERVIDORES_EM_EXERCICIO_POR_ANO[2022] == 287
    assert tcade.N_SERVIDORES_EM_EXERCICIO_POR_ANO[2023] == 311
    assert tcade.N_SERVIDORES_EM_EXERCICIO_POR_ANO[2024] == 326


def test_pessoas_total_serie_2022_2024():
    """Servidores + colaboradores: 524, 545, 569 (RIG)."""
    assert tcade.N_PESSOAS_TOTAL_POR_ANO[2022] == 524
    assert tcade.N_PESSOAS_TOTAL_POR_ANO[2023] == 545
    assert tcade.N_PESSOAS_TOTAL_POR_ANO[2024] == 569


def test_n_servidores_total_eh_326_RIG_2024():
    """Atualização: 326 substitui 292 da NT CADE 2022."""
    assert tcade.N_SERVIDORES_TOTAL == 326


def test_dependencia_de_cedidos_cresceu_2022_2024():
    """A fração de cedidos passou de 75% (2022) a 82% (2024) — RIG."""
    fracoes = tcade.FRACAO_SERVIDORES_DE_OUTRAS_INSTITUICOES
    assert fracoes[2022] == 0.75
    assert fracoes[2024] == 0.82
    assert fracoes[2022] < fracoes[2024]


def test_pgpe_quadro_proprio_eh_35():
    """Quadro permanente PGPE: apenas 35 (RIG 2024, p. 112)."""
    assert tcade.N_SERVIDORES_PGPE_QUADRO_PROPRIO == 35


def test_area_fim_eh_180_proxy_sg():
    """Área-fim total = 180 servidores (RIG 2024, p. 110)."""
    assert tcade.N_SERVIDORES_AREA_FIM == 180


def test_sg_usa_area_fim_como_proxy():
    """`N_SERVIDORES_POR_UNIDADE['superintendencia_geral'] = 180` (proxy)."""
    assert tcade.N_SERVIDORES_POR_UNIDADE["superintendencia_geral"] == 180


def test_dee_permanece_marcado_indisponivel():
    """RIGs não decompõem DEE separadamente — segue `None` [?]."""
    assert tcade.N_SERVIDORES_POR_UNIDADE["departamento_estudos_economicos"] is None


def test_tribunal_eh_7_estatutario():
    """Lei 12.529/2011 art. 6º — 7 membros."""
    assert tcade.N_SERVIDORES_POR_UNIDADE["tribunal_administrativo"] == 7
    assert tcade.N_SERVIDORES_POR_CATEGORIA["conselheiro"] == 7


# ----------------------------------------------------------------------
# Orçamento — Ação 2807 (Promoção e Defesa da Concorrência)
# ----------------------------------------------------------------------


def test_loa_total_2022_2024():
    """RIG: R$ 42,77 mi em 2022/2023; R$ 49,52 mi em 2024 (Lei 14.822/2024)."""
    loa = tcade.ORCAMENTO_LOA_TOTAL_BRL_POR_ANO
    assert loa[2022] == 42_769_864.00
    assert loa[2023] == 42_769_864.00  # sem aumento nominal
    assert loa[2024] == 49_521_635.00


def test_execucao_acao_2807_proxima_de_100_por_cento():
    """Execução 99,4-99,8% — gargalo do CADE não é orçamentário."""
    assert abs(tcade.execucao_orcamentaria_relativa(2022) - 0.996) < 0.01
    assert abs(tcade.execucao_orcamentaria_relativa(2023) - 0.994) < 0.01
    assert abs(tcade.execucao_orcamentaria_relativa(2024) - 0.998) < 0.01


def test_tic_acao_2807_2024_R_9_2_mi():
    """RIG 2024: R$ 9.163.362,97 em TIC (22% da Ação 2807)."""
    assert tcade.GASTO_TIC_ACAO_2807_BRL_POR_ANO[2024] == 9_163_362.97


# ----------------------------------------------------------------------
# Fluxo de processos — RIG (fonte primária)
# ----------------------------------------------------------------------


def test_atos_concentracao_serie_RIG_eh_primaria():
    """RIG: 660/594/712. NB: ConJur tinha 579 em 2023; usamos RIG."""
    acs = tcade.ATOS_CONCENTRACAO_NOTIFICADOS_POR_ANO
    assert acs[2022] == 660
    assert acs[2023] == 594  # RIG, não 579
    assert acs[2024] == 712


def test_investigacoes_instauradas_sg_serie():
    """RIG: 103/63/73 — categoria ampla (PA + preparatório + inquérito)."""
    instauradas = tcade.INVESTIGACOES_INSTAURADAS_SG_POR_ANO
    assert instauradas[2022] == 103
    assert instauradas[2023] == 63
    assert instauradas[2024] == 73


def test_investigacoes_concluidas_sg_serie():
    """RIG: 111/106/89 — concluídas decrescem em 2024."""
    concluidas = tcade.INVESTIGACOES_CONCLUIDAS_SG_POR_ANO
    assert concluidas[2022] == 111
    assert concluidas[2023] == 106
    assert concluidas[2024] == 89


def test_estoque_sg_serie():
    """RIG: 247/177/185 — estoque caiu fortemente em 2023."""
    estoque = tcade.ESTOQUE_INVESTIGACOES_SG_POR_ANO
    assert estoque[2022] == 247
    assert estoque[2023] == 177
    assert estoque[2024] == 185


def test_leniencias_assinadas_serie():
    """RIG: 1/2/4 — tendência crescente em 2024."""
    assert tcade.LENIENCIAS_ASSINADAS_POR_ANO[2022] == 1
    assert tcade.LENIENCIAS_ASSINADAS_POR_ANO[2023] == 2
    assert tcade.LENIENCIAS_ASSINADAS_POR_ANO[2024] == 4


def test_total_leniencias_historicas_eh_113():
    """RIG 2024 p. 85: 113 acumuladas (substitui 109 do comunicado 2023)."""
    assert tcade.TOTAL_LENIENCIAS_HISTORICAS == 113


def test_busca_e_apreensao_serie():
    """RIG: 2/2/3 operações; 2024 com 16 mandados."""
    assert tcade.OPERACOES_BUSCA_APREENSAO_POR_ANO[2024] == 3


def test_multas_transito_julgado_2024_decomposto():
    """RIG 2024 p. 115: nominal R$ 158 mi, atualizado R$ 162 mi, arrecadado R$ 29 mi."""
    multas = tcade.MULTAS_TRANSITO_JULGADO_2024_BRL
    assert multas["nominal"] == 158_180_000.0
    assert multas["atualizado"] == 161_940_000.0
    assert multas["arrecadado"] == 29_170_000.0
    # Diferença nominal vs. arrecadado é grande — gap de cobrança.
    assert multas["arrecadado"] < multas["nominal"] * 0.20


def test_denuncias_clique_denuncia_2024_eh_3725():
    assert tcade.DENUNCIAS_CLIQUE_DENUNCIA_POR_ANO[2024] == 3_725


def test_tempo_medio_ac_sumario_serie():
    """RIG: 21,4 → 12,6 → 15,1 dias."""
    sumario = tcade.TEMPO_MEDIO_AC_SUMARIO_DIAS_POR_ANO
    assert sumario[2022] == 21.4
    assert sumario[2023] == 12.6
    assert sumario[2024] == 15.1


def test_tempo_medio_ac_ordinario_serie():
    """RIG: 125,6 → 116,7 → 92,1 dias (tendência decrescente)."""
    ordinario = tcade.TEMPO_MEDIO_AC_ORDINARIO_DIAS_POR_ANO
    assert ordinario[2022] == 125.6
    assert ordinario[2023] == 116.7
    assert ordinario[2024] == 92.1


# ----------------------------------------------------------------------
# Marcações [?] — explicitamente não publicado nos RIGs
# ----------------------------------------------------------------------


def test_decomposicao_dee_pendente():
    """DEE separado não está nos RIGs (só área-fim agregado)."""
    assert tcade.N_SERVIDORES_POR_UNIDADE["departamento_estudos_economicos"] is None


def test_procuradores_e_outros_cargos_pendentes():
    """Decomposição por cargo individual não está no RIG."""
    assert tcade.N_SERVIDORES_POR_CATEGORIA["procurador_federal"] is None
    assert tcade.N_SERVIDORES_POR_CATEGORIA["tecnico_administrativo"] is None
    assert tcade.N_SERVIDORES_POR_CATEGORIA["cargo_comissionado"] is None


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def test_disponivel_eh_true_apos_extracao():
    """Com N_SERVIDORES_TOTAL preenchido, `disponivel()` é True."""
    assert tcade.disponivel() is True


def test_servidores_sg_calibrado_devolve_180():
    """Default helper agora retorna 180 (área-fim do RIG 2024)."""
    assert tcade.servidores_sg_calibrado() == 180


def test_capacidade_efetiva_com_sg_180():
    """SG=180 × 2 casos/ano / 4 trimestres = 90 casos/tique."""
    assert tcade.capacidade_efetiva_por_tique() == 90


def test_capacidade_efetiva_respeita_overrides():
    """Variando parâmetros: SG=180 × 4 / 4 = 180."""
    assert tcade.capacidade_efetiva_por_tique(casos_por_servidor_ano=4.0) == 180


def test_deficit_eppgg_eh_proximo_67():
    """(200 − 65) / 200 = 0,675."""
    deficit = tcade.deficit_eppgg()
    assert 0.66 < deficit < 0.69


def test_execucao_orcamentaria_relativa_funciona():
    """Razão executado / LOA atualizada."""
    razao = tcade.execucao_orcamentaria_relativa(2024)
    assert razao is not None
    assert 0.99 < razao < 1.0


def test_execucao_orcamentaria_relativa_devolve_none_para_ano_invalido():
    assert tcade.execucao_orcamentaria_relativa(1999) is None


# ----------------------------------------------------------------------
# Limiares + universo regulado
# ----------------------------------------------------------------------


def test_limiares_notificacao_lei_12_529():
    assert tcade.LIMIARES_NOTIFICACAO_AC_BRL == (75_000_000.0, 750_000_000.0)


def test_universo_eh_estimativa_intervalar():
    lo, hi = tcade.UNIVERSO_FIRMAS_REGULADAS_ESTIMATIVA
    assert (lo, hi) == (5_000, 20_000)


# ----------------------------------------------------------------------
# Resumo textual
# ----------------------------------------------------------------------


def test_resumo_inclui_numeros_chave_RIG_2024():
    texto = tcade.resumo()
    assert "326" in texto  # servidores total
    assert "180" in texto  # área-fim
    assert "65" in texto  # EPPGG
    assert "712" in texto  # ACs 2024
    assert "RIG" in texto or "rig" in texto.lower()


# ----------------------------------------------------------------------
# Estrutura estável (compat)
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


def test_orcamento_cobre_2022_2024():
    assert set(tcade.ORCAMENTO_LOA_TOTAL_BRL_POR_ANO.keys()) == {2022, 2023, 2024}
    assert set(tcade.EXECUCAO_ACAO_2807_POR_ANO.keys()) == {2022, 2023, 2024}
