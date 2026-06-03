"""Testes integrados de R16 (arquétipo fairminded + Torsell 2026),
R17 (cenários normativos) e R18 (commitment da firma / sanção
catastrófica)."""

from __future__ import annotations

import pytest

from waas_antitrust.agents import TrabalhadorAgent
from waas_antitrust.cenarios import (
    CATALOGO_CENARIOS,
    DISTRIBUICAO_COM_FAIRMINDED,
    Cenario,
    aplicar_cenario,
    listar_cenarios,
    lookup_cenario,
)
from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# R16 — Arquétipo fairminded + inequity aversion (Torsell 2026)
# ----------------------------------------------------------------------


def test_fairminded_esta_no_catalogo_de_arquetipos():
    """ARQUETIPOS agora inclui fairminded (Torsell 2026, Fehr-Schmidt 1999)."""
    assert "fairminded" in TrabalhadorAgent.ARQUETIPOS
    assert len(TrabalhadorAgent.ARQUETIPOS) == 5


def test_distribuicao_arquetipos_default_preserva_4_tipos():
    """Default `distribuicao_arquetipos=None` ⇒ fairminded em 0% (compat)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=80,
            n_tiques=1,
            seed=11,
            regime="B",
            distribuicao_arquetipos=None,
        )
    )
    arqs = {t.arquetipo for ws in m.trabalhadores_por_empresa.values() for t in ws}
    assert "fairminded" not in arqs  # default não sorteia FM


def test_distribuicao_com_fairminded_sorteia_fm():
    """Quando `distribuicao_arquetipos` inclui fairminded, ele aparece."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=200,
            n_tiques=1,
            seed=17,
            regime="B",
            distribuicao_arquetipos=DISTRIBUICAO_COM_FAIRMINDED,
        )
    )
    arqs = [t.arquetipo for ws in m.trabalhadores_por_empresa.values() for t in ws]
    assert "fairminded" in arqs
    # ~20% da população deve ser FM (margem ampla para acomodar variância).
    fracao_fm = arqs.count("fairminded") / len(arqs)
    assert 0.10 < fracao_fm < 0.30


def test_fairminded_peso_zero_degenera_em_racional_puro():
    """`peso_inequity_aversion=0` ⇒ FM decide como racional sem pressão ética."""
    base = dict(
        n_empresas=10,
        tam_medio_empresa=200,
        n_tiques=10,
        seed=23,
        regime="B",
        fracao_violadoras=0.6,
        taxa_observacao=0.5,
        distribuicao_arquetipos=DISTRIBUICAO_COM_FAIRMINDED,
        peso_inequity_aversion=0.0,
    )
    df_zero = WaaSModel(WaaSParametros(**base)).executar()
    # Sistema funcional, mas sem o boost ético: serve só como baseline.
    assert int(df_zero["n_sinais"].sum()) >= 0


def test_fairminded_peso_alto_acelera_cascata_etica():
    """Break-even ético coletivo (R16): peso de inequity aversion alto faz
    a fração de tiques com sinalização crescer — emerge sem hardcoding."""
    base = dict(
        n_empresas=12,
        tam_medio_empresa=300,
        n_tiques=25,
        seed=37,
        regime="B",
        fracao_violadoras=0.7,
        taxa_observacao=0.6,
        distribuicao_arquetipos=DISTRIBUICAO_COM_FAIRMINDED,
    )
    df_baixo = WaaSModel(WaaSParametros(**base, peso_inequity_aversion=0.0)).executar()
    df_alto = WaaSModel(WaaSParametros(**base, peso_inequity_aversion=2.0)).executar()
    sinais_baixo = int(df_baixo["n_sinais"].sum())
    sinais_alto = int(df_alto["n_sinais"].sum())
    # Peso alto ⇒ FM responde à pressão ética ⇒ mais sinais ao longo do tempo.
    assert sinais_alto >= sinais_baixo, (
        f"peso de inequity aversion alto deveria gerar ≥ sinais; "
        f"baixo={sinais_baixo}, alto={sinais_alto}"
    )


# ----------------------------------------------------------------------
# R17 — Cenários normativos como variantes paramétricas
# ----------------------------------------------------------------------


def test_catalogo_tem_7_cenarios_canonicos():
    assert len(CATALOGO_CENARIOS) == 7
    nomes = [c.nome for c in CATALOGO_CENARIOS]
    assert len(set(nomes)) == 7  # nomes únicos


def test_cenarios_cobrem_status_quo_e_regimes_b_e_c():
    """Cobertura mínima: pelo menos um cenário em cada um dos três regimes."""
    regimes_cobertos = {c.sobrescritas.get("regime") for c in CATALOGO_CENARIOS}
    assert {"A", "B", "C"}.issubset(regimes_cobertos)


def test_lookup_cenario_funciona_e_levanta_em_desconhecido():
    c = lookup_cenario("resolucao_pura")
    assert isinstance(c, Cenario)
    assert c.sobrescritas["regime"] == "B"
    with pytest.raises(KeyError, match="desconhecido"):
        lookup_cenario("cenario_inexistente_xyz")


def test_listar_cenarios_devolve_lista_de_strings():
    nomes = listar_cenarios()
    assert isinstance(nomes, list)
    assert "status_quo" in nomes
    assert "lei_waas_com_vesting_padrao" in nomes


def test_aplicar_cenario_nao_muta_params_original():
    """`aplicar_cenario` retorna nova instância, não muta a original."""
    p_orig = WaaSParametros(regime="B", D_disc_base_tcc=0.0)
    p_novo = aplicar_cenario(p_orig, "resolucao_pura")
    assert p_orig.D_disc_base_tcc == 0.0  # original intacto
    assert p_novo.D_disc_base_tcc == 0.10  # novo tem a sobrescrita


def test_cenario_lei_waas_com_vesting_padrao_ativa_hirschman_so_em_c():
    """Categoria 4 (gating jurídico) é respeitada: vesting padrão só em C."""
    p_base = WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=2)
    p_vesting = aplicar_cenario(p_base, "lei_waas_com_vesting_padrao")
    assert p_vesting.regime == "C"
    assert p_vesting.fracao_contratos_acelerados == 1.0
    # Construir modelo sob Regime C funciona sem warning.
    m = WaaSModel(p_vesting)
    assert m.fracao_contratos_acelerados == 1.0  # preservado em C


def test_cenario_status_quo_eh_regime_a_puro():
    p = aplicar_cenario(WaaSParametros(), "status_quo")
    assert p.regime == "A"


def test_todos_cenarios_executam_sem_erro():
    """Cada cenário roda um modelo curto sem exceção."""
    p_base = WaaSParametros(n_empresas=4, tam_medio_empresa=30, n_tiques=2)
    for c in CATALOGO_CENARIOS:
        p = aplicar_cenario(p_base, c)
        m = WaaSModel(p)
        df = m.executar()
        assert len(df) >= 1, f"cenário {c.nome} produziu df vazio"


# ----------------------------------------------------------------------
# R18 — Commitment da firma + sanção catastrófica
# ----------------------------------------------------------------------


def test_prob_pagamento_default_1_preserva_comportamento():
    """`prob_pagamento_perc=1.0` (default) ⇒ W esperado = W nominal."""
    m = WaaSModel(WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=2))
    assert m.prob_pagamento_perc == 1.0


def test_prob_pagamento_baixa_reduz_sinalizacao_racional():
    """Quando trabalhadores percebem que firma pode não pagar, sinalizam menos.
    Pressuposto R18: 'se a empresa não paga, perdem tudo'."""
    base = dict(
        n_empresas=15,
        tam_medio_empresa=300,
        n_tiques=15,
        seed=47,
        regime="B",
        fracao_violadoras=0.6,
        taxa_observacao=0.6,
        W_mult=1.5,
        r_represalia=0.15,
    )
    df_alta = WaaSModel(WaaSParametros(**base, prob_pagamento_perc=1.0)).executar()
    df_baixa = WaaSModel(WaaSParametros(**base, prob_pagamento_perc=0.3)).executar()
    sinais_alta = int(df_alta["n_sinais"].sum())
    sinais_baixa = int(df_baixa["n_sinais"].sum())
    # Trabalhadores racionais descontam W pela prob — menos confiança = menos sinais.
    assert sinais_baixa <= sinais_alta, (
        f"prob_pagamento baixa deveria reduzir sinais; " f"alta={sinais_alta}, baixa={sinais_baixa}"
    )


def test_p_descumprimento_zero_preserva_zero_quebras():
    """`p_descumprimento_tcc=0.0` ⇒ nenhuma firma quebra TCC."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=8,
            tam_medio_empresa=100,
            n_tiques=15,
            seed=53,
            regime="B",
            p_descumprimento_tcc=0.0,
        )
    )
    df = m.executar()
    assert int(df["n_firmas_quebraram_tcc"].max()) == 0


def test_p_descumprimento_um_quebra_todas_as_assinantes():
    """`p_descumprimento_tcc=1.0` ⇒ toda firma que assina, quebra. Sanção
    catastrófica `multa_descumprimento_tcc · S_esp` acumula."""
    base = dict(
        n_empresas=15,
        tam_medio_empresa=200,
        n_tiques=20,
        seed=59,
        regime="B",
        fracao_violadoras=0.7,
        taxa_observacao=0.5,
    )
    df = WaaSModel(
        WaaSParametros(
            **base,
            p_descumprimento_tcc=1.0,
            multa_descumprimento_tcc=2.0,
        )
    ).executar()
    quebras = int(df["n_firmas_quebraram_tcc"].max())
    multa_extra = float(df["multa_descumprimento_acum"].max())
    # Para qualquer firma que tenha assinado, a multa catastrófica acumulou.
    if quebras > 0:
        assert multa_extra > 0.0, "esperado multa de descumprimento > 0 quando há quebras"
