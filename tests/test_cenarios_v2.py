"""Testes dos cenários novos do reframe v2 (instrumentos de internalização +
robustez do mecanismo)."""

from __future__ import annotations

from waas_antitrust.cenarios import (
    CATALOGO_CENARIOS,
    aplicar_cenario,
    lookup_cenario,
)
from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Cenários v2 — instrumentos de internalização
# ----------------------------------------------------------------------


def test_apenas_massa_critica_observavel_e_regime_a():
    """Cenário v2.A: testa massa crítica sem instrumento (D_disc=0).
    Falsificador F7 — o sinal Schelling sobrevive à invisibilidade do instrumento?"""
    p = aplicar_cenario(WaaSParametros(), "apenas_massa_critica_observavel")
    assert p.regime == "A"
    assert p.D_disc == 0.0


def test_dois_instrumentos_acoplados_ativa_modo_corrida_e_hirschman():
    """Cenário v2.C: WaaS + Hirschman simultâneos sob LCMC."""
    p = aplicar_cenario(WaaSParametros(), "dois_instrumentos_acoplados")
    assert p.regime == "C"
    assert p.modo_corrida is True
    assert p.fracao_contratos_acelerados == 1.0
    assert p.aliquota_tributaria_vesting == 0.40


def test_credito_tributario_puro_stub_executa():
    """R22 stub: aplica via Hirschman como proxy. Validação smoke."""
    p_base = WaaSParametros(n_empresas=4, tam_medio_empresa=30, n_tiques=2)
    p = aplicar_cenario(p_base, "credito_tributario_puro")
    assert p.regime == "C"
    assert p.aliquota_tributaria_vesting == 0.10
    df = WaaSModel(p).executar()
    assert len(df) >= 1


def test_leniencia_criminal_individual_stub_executa():
    """R23 stub: custo_legal_uw ~0 simula 'Estado defende'."""
    p_base = WaaSParametros(n_empresas=4, tam_medio_empresa=30, n_tiques=2)
    p = aplicar_cenario(p_base, "leniencia_criminal_individual")
    assert p.regime == "C"
    assert p.custo_legal_uw <= 0.05
    assert p.p_anulacao_tcc == 0.0
    df = WaaSModel(p).executar()
    assert len(df) >= 1


# ----------------------------------------------------------------------
# Cenários v2 — robustez do mecanismo
# ----------------------------------------------------------------------


def test_captura_processamento_cade_reduz_capacidade():
    """Cenário Cient. Político v2: capacidade estrangulada (gargalo CADE 180 servidores)."""
    p = aplicar_cenario(WaaSParametros(), "captura_processamento_cade")
    assert p.regime == "B"
    assert p.taxa_capacidade == 0.10


def test_uso_adversarial_oportunista_usa_distribuicao_correta():
    """R24: cenário com 20% de oportunistas + falso reporte elevado."""
    p = aplicar_cenario(WaaSParametros(), "uso_adversarial_oportunista")
    assert p.regime == "B"
    assert "oportunista" in p.distribuicao_arquetipos
    assert p.distribuicao_arquetipos["oportunista"] >= 0.10
    assert p.taxa_falso_reporte >= 0.10


def test_uso_adversarial_executa_e_sorteia_oportunistas():
    """Smoke + sanity: cenário roda end-to-end e produz oportunistas no modelo."""
    p_base = WaaSParametros(n_empresas=6, tam_medio_empresa=120, n_tiques=5, seed=53)
    p = aplicar_cenario(p_base, "uso_adversarial_oportunista")
    m = WaaSModel(p)
    arqs = {t.arquetipo for ws in m.trabalhadores_por_empresa.values() for t in ws}
    assert "oportunista" in arqs, "esperado oportunistas sorteados"
    df = m.executar()
    assert len(df) == 5


def test_todos_seis_cenarios_v2_no_catalogo():
    """Validação de catálogo: 6 cenários novos do reframe v2 estão presentes."""
    nomes_v2 = {
        "apenas_massa_critica_observavel",
        "dois_instrumentos_acoplados",
        "credito_tributario_puro",
        "leniencia_criminal_individual",
        "captura_processamento_cade",
        "uso_adversarial_oportunista",
    }
    nomes_catalogo = {c.nome for c in CATALOGO_CENARIOS}
    assert nomes_v2.issubset(nomes_catalogo), f"faltam cenários v2: {nomes_v2 - nomes_catalogo}"


def test_lookup_cenario_v2_funciona():
    """`lookup_cenario` localiza os 6 cenários novos sem erro."""
    for nome in (
        "apenas_massa_critica_observavel",
        "dois_instrumentos_acoplados",
        "credito_tributario_puro",
        "leniencia_criminal_individual",
        "captura_processamento_cade",
        "uso_adversarial_oportunista",
    ):
        c = lookup_cenario(nome)
        assert c.nome == nome


def test_descricoes_cenarios_v2_citam_personas():
    """Auditável: cada cenário v2 deve citar a persona x10 v2 que o motivou."""
    citacoes_esperadas = {
        "apenas_massa_critica_observavel": "Eco A",
        "dois_instrumentos_acoplados": "Eco A",
        "credito_tributario_puro": "R22",
        "leniencia_criminal_individual": "R23",
        "captura_processamento_cade": "Cient. Político",
        "uso_adversarial_oportunista": "Dyck-Morse-Zingales",
    }
    for nome, marcador in citacoes_esperadas.items():
        c = lookup_cenario(nome)
        assert (
            marcador in c.descricao
        ), f"cenário {nome} deve citar {marcador!r}; descrição: {c.descricao[:120]}"


# ---------------------------------------------------------------------
# Cenários R28 — generalidade EUA/UE (pesquisa de fundo 2026)
# ---------------------------------------------------------------------


def test_eua_doj_atr_rewards_2025_calibra_faixa_15_30():
    """DOJ-ATR Whistleblower Rewards Program (jul/2025): 15-30% sobre multas
    ≥ US$ 1 milhão. `prob_pagamento_perc` deve refletir média 0.225."""
    p = aplicar_cenario(WaaSParametros(), "eua_doj_atr_rewards_2025")
    assert p.regime == "EUA"  # tag R28; mecânica C (Dodd-Frank §922)
    assert p.p_anulacao_tcc == 0.0  # sem F6
    assert p.prob_pagamento_perc == 0.225  # média 15-30%
    assert p.modo_corrida is True  # LCMC ativa


def test_ue_dma_whistleblower_tool_2024_sem_recompensa():
    """DMA Whistleblower Tool (30/abr/2024): proteção sem recompensa. Vetor
    empírico contra o qual o BR pode ser comparado."""
    p = aplicar_cenario(WaaSParametros(), "ue_dma_whistleblower_tool_2024")
    assert p.regime == "UE"  # tag R28; mecânica A (sem recompensa)
    assert p.D_disc == 0.0  # sem instrumento de internalização monetária
    assert p.r_represalia < 0.10  # proteção horizontal Diretiva 2019/1937


# ---------------------------------------------------------------------
# R28 — tags jurisdicionais "EUA"/"UE" no WaaSParametros.regime
# ---------------------------------------------------------------------


def test_tag_eua_mapeia_mecanica_c_e_preserva_declarado():
    """Tag "EUA" mapeia para mecânica C; `regime_declarado` preserva a tag."""
    m = WaaSModel(WaaSParametros(n_empresas=3, tam_medio_empresa=30, n_tiques=1, regime="EUA"))
    assert m.regime == "C"
    assert m.regime_declarado == "EUA"


def test_tag_ue_mapeia_mecanica_a_e_preserva_declarado():
    """Tag "UE" mapeia para mecânica A (DMA Tool: sem recompensa/LCMC)."""
    m = WaaSModel(WaaSParametros(n_empresas=3, tam_medio_empresa=30, n_tiques=1, regime="UE"))
    assert m.regime == "A"
    assert m.regime_declarado == "UE"


def test_regime_invalido_levanta_value_error():
    """Regime fora de REGIMES_VALIDOS levanta ValueError com mensagem clara."""
    import pytest

    with pytest.raises(ValueError, match="regime desconhecido"):
        WaaSModel(WaaSParametros(n_empresas=3, tam_medio_empresa=30, n_tiques=1, regime="X"))


def test_tag_eua_equivale_bit_a_bit_a_regime_c():
    """Mesma seed: regime="EUA" produz DataFrame idêntico a regime="C"
    (a tag é rótulo institucional, não mecânica nova)."""
    base = dict(n_empresas=5, tam_medio_empresa=60, n_tiques=6, seed=73)
    df_c = WaaSModel(WaaSParametros(**base, regime="C")).executar()
    df_eua = WaaSModel(WaaSParametros(**base, regime="EUA")).executar()
    assert df_c.equals(df_eua), "tag EUA deveria ser equivalente bit-a-bit à mecânica C"


def test_regimes_abc_preservam_comportamento_historico():
    """Compat: A/B/C seguem aceitos e `regime_declarado` coincide com `regime`."""
    for r in ("A", "B", "C"):
        m = WaaSModel(WaaSParametros(n_empresas=3, tam_medio_empresa=30, n_tiques=1, regime=r))
        assert m.regime == r
        assert m.regime_declarado == r


def test_instrumentos_por_regime_aceita_tags_r28():
    """`instrumentos_por_regime` resolve tags: EUA hospeda como C; UE como A."""
    from waas_antitrust.instrumentos import instrumentos_por_regime

    nomes_eua = {i.nome for i in instrumentos_por_regime("EUA")}
    assert "canal_deposito_condicional" in nomes_eua
    assert "vesting_acelerado_hirschman" in nomes_eua  # nível C
    assert instrumentos_por_regime("UE") == []  # DMA Tool não hospeda entradas LCMC


def test_cenarios_r28_executam_end_to_end():
    """Smoke: ambos os cenários R28 rodam o modelo sem erro."""
    p_base = WaaSParametros(n_empresas=4, tam_medio_empresa=30, n_tiques=3, seed=59)
    for nome in ("eua_doj_atr_rewards_2025", "ue_dma_whistleblower_tool_2024"):
        p = aplicar_cenario(p_base, nome)
        df = WaaSModel(p).executar()
        assert len(df) >= 1


def test_cenarios_r28_no_catalogo():
    """Ambos os cenários R28 estão presentes em CATALOGO_CENARIOS."""
    nomes_r28 = {"eua_doj_atr_rewards_2025", "ue_dma_whistleblower_tool_2024"}
    nomes_catalogo = {c.nome for c in CATALOGO_CENARIOS}
    assert nomes_r28.issubset(nomes_catalogo), f"faltam cenários R28: {nomes_r28 - nomes_catalogo}"


def test_descricoes_cenarios_r28_citam_marco_normativo():
    """Auditável: cada cenário R28 deve citar o marco normativo de origem."""
    marcos = {
        "eua_doj_atr_rewards_2025": "Dodd-Frank",
        "ue_dma_whistleblower_tool_2024": "2019/1937",
    }
    for nome, marco in marcos.items():
        c = lookup_cenario(nome)
        assert marco in c.descricao, f"cenário {nome} deve citar {marco!r}"


# ---------------------------------------------------------------------
# R27-i — Canal puro + R26 — Erosão Coleman (fechamento do backlog v3)
# ---------------------------------------------------------------------


def test_apenas_canal_sem_instrumento_isola_o_canal():
    """R27-i: cenário aciona `usar_escrow_explicito=True` e zera o
    instrumento monetário dos dois lados (`W_mult=0`, `D_disc=0`)."""
    p = aplicar_cenario(WaaSParametros(), "apenas_canal_sem_instrumento")
    assert p.regime == "B"
    assert p.usar_escrow_explicito is True
    assert p.W_mult == 0.0
    assert p.D_disc == 0.0
    # Rodada curta executa e expõe colunas do escrow.
    p_curto = aplicar_cenario(
        WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=3, seed=43),
        "apenas_canal_sem_instrumento",
    )
    df = WaaSModel(p_curto).executar()
    assert "n_denuncias_em_escrow" in df.columns
    assert "n_aberturas_simultaneas_acum" in df.columns


def test_erosao_coleman_adversarial_degrada_capital_social():
    """R26: cenário com `alpha_erosao=0.5` reduz `capital_social_residual`
    abaixo de 1.0 quando há notificação; baseline `resolucao_pura` permanece
    em 1.0."""
    p_base = WaaSParametros(
        n_empresas=8,
        tam_medio_empresa=120,
        n_tiques=20,
        seed=47,
        fracao_violadoras=0.7,
        taxa_observacao=0.6,
    )
    df_baseline = WaaSModel(aplicar_cenario(p_base, "resolucao_pura")).executar()
    df_erosao = WaaSModel(aplicar_cenario(p_base, "erosao_coleman_adversarial")).executar()
    cap_baseline_final = float(df_baseline["capital_social_residual"].iloc[-1])
    cap_erosao_final = float(df_erosao["capital_social_residual"].iloc[-1])
    assert cap_baseline_final == 1.0  # sem alpha_erosao, residual constante
    assert cap_erosao_final < 1.0, (
        f"esperado capital_social_residual < 1.0 sob alpha_erosao=0.5; "
        f"obtido {cap_erosao_final:.3f} (baseline {cap_baseline_final:.3f})"
    )
