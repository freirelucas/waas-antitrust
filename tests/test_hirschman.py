"""Testes da camada Hirschman exit-with-equity (R07, exploratório)."""

import pytest

from waas_antitrust.hirschman import (
    custo_exodo_esperado,
    custo_substituicao,
    deve_pagar_com_hirschman,
    g_i_efetivo,
    valor_liquido_pos_tributos,
    valor_vesting_acelerado,
)


def test_sem_clausula_custo_exodo_zero():
    """Sem cláusula contratual de aceleração, não há gatilho legal → custo nulo."""
    assert custo_exodo_esperado(n_disparados=20, w_a_medio=180_000, tem_clausula=False) == 0.0


def test_com_clausula_custo_exodo_positivo_e_cresce_com_n():
    """Com cláusula, o custo é positivo e linear no número de funcionários."""
    c5 = custo_exodo_esperado(5, 180_000, tem_clausula=True)
    c10 = custo_exodo_esperado(10, 180_000, tem_clausula=True)
    assert c5 > 0
    assert c10 == pytest.approx(2 * c5)


def test_componentes_yc_padrao():
    """Padrões YC: substituição = 50% salário; equity = 50% salário × 50% non-vested."""
    # 1 funcionário com salário 180k
    sub = custo_substituicao(1, 180_000)
    vest = valor_vesting_acelerado(1, 180_000)
    assert sub == 90_000.0  # 50% de 180k
    assert vest == 45_000.0  # 50% × 50% de 180k


def test_g_i_efetivo_desconta_so_com_clausula():
    """O desconto preventivo só se aplica a firmas com cláusula."""
    sem = g_i_efetivo(g_i=0.2, tem_clausula=False, p_perc=0.5)
    com = g_i_efetivo(g_i=0.2, tem_clausula=True, p_perc=0.5)
    assert sem == 0.2
    assert com < 0.2  # descontou
    # Com peso_hirschman padrão 0.3: g_efetivo = 0.2 - 0.5*0.3 = 0.05
    assert com == pytest.approx(0.05)


def test_ic_f_ampliada_pode_forcar_pagamento():
    """Quando IC-F* sozinha rejeitaria pagar (W>D), o exit-threat pode reverter."""
    # Caso 1: sem exit-threat, IC-F* clássica rejeita
    W_total = 100.0
    D_val = 50.0
    assert deve_pagar_com_hirschman(W_total, D_val, custo_exodo=0.0) is False
    # Caso 2: exit-threat alto reverte
    assert deve_pagar_com_hirschman(W_total, D_val, custo_exodo=100.0) is True
    # Caso de fronteira: D + exodo = W (não paga, é estritamente maior)
    assert deve_pagar_com_hirschman(W_total, D_val, custo_exodo=50.0) is False


def test_argumentos_invalidos_levantam():
    """Salvaguardas de domínio."""
    with pytest.raises(ValueError):
        custo_substituicao(-1, 180_000)
    with pytest.raises(ValueError):
        valor_vesting_acelerado(10, 180_000, fracao_nao_vested=1.5)


def test_valor_liquido_pos_tributos_aplica_haircut():
    """Categoria 4 (Adv B): IRPF + INSS derrete o valor bruto do vesting."""
    # Default 40% → líquido = 60% do bruto.
    assert valor_liquido_pos_tributos(100_000.0) == pytest.approx(60_000.0)
    # Aliquota 0 ⇒ líquido = bruto (compat com versão antiga).
    assert valor_liquido_pos_tributos(100_000.0, aliquota_efetiva=0.0) == 100_000.0
    # Aliquota 0.5 (caracterização salarial estrita).
    assert valor_liquido_pos_tributos(100_000.0, aliquota_efetiva=0.5) == 50_000.0


def test_valor_liquido_rejeita_argumentos_invalidos():
    with pytest.raises(ValueError):
        valor_liquido_pos_tributos(-1.0)
    with pytest.raises(ValueError):
        valor_liquido_pos_tributos(100.0, aliquota_efetiva=1.0)
    with pytest.raises(ValueError):
        valor_liquido_pos_tributos(100.0, aliquota_efetiva=-0.1)


def test_custo_exodo_haircut_so_no_vesting_nao_na_substituicao():
    """O haircut tributário atinge só o equity (rendimento do trabalhador),
    não o custo de substituição (despesa operacional da firma)."""
    # Sem haircut (default 0): bruto.
    c_bruto = custo_exodo_esperado(10, 180_000, tem_clausula=True)
    # Com haircut 0,4: vesting cai 40%, substituição inalterada.
    c_liq = custo_exodo_esperado(10, 180_000, tem_clausula=True, aliquota_tributaria=0.4)
    sub = custo_substituicao(10, 180_000)  # 50% × 10 × 180k = 900k
    vest = valor_vesting_acelerado(10, 180_000)  # 50% × 50% × 10 × 180k = 450k
    assert c_bruto == pytest.approx(sub + vest)
    assert c_liq == pytest.approx(sub + vest * 0.6)
    # A queda no custo total = 40% do vesting (não do total).
    assert (c_bruto - c_liq) == pytest.approx(vest * 0.4)


def test_gating_juridico_regime_b_forca_fracao_zero_e_emite_warning():
    """Categoria 4.1 (Adv B): Resolução do CADE (Regime B) não pode impor
    cláusula contratual padrão (reserva de lei). Sob A/B, o modelo força
    `fracao_contratos_acelerados=0` e emite UserWarning."""
    from waas_antitrust.model import WaaSModel, WaaSParametros

    for regime_proibido in ("A", "B"):
        with pytest.warns(UserWarning, match="reserva de lei"):
            modelo = WaaSModel(
                WaaSParametros(
                    n_empresas=4,
                    tam_medio_empresa=30,
                    n_tiques=2,
                    regime=regime_proibido,
                    fracao_contratos_acelerados=0.5,
                )
            )
        assert modelo.fracao_contratos_acelerados == 0.0


def test_gating_juridico_regime_c_preserva_fracao():
    """Categoria 4.1 (Adv B): Regime C (via lei) pode impor a cláusula."""
    from waas_antitrust.model import WaaSModel, WaaSParametros

    modelo = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=30,
            n_tiques=2,
            regime="C",
            fracao_contratos_acelerados=0.5,
        )
    )
    assert modelo.fracao_contratos_acelerados == pytest.approx(0.5)


def test_modelo_integrado_aumenta_pagamento_com_clausula():
    """End-to-end: fração maior de cláusulas → mais firmas pagam denunciantes
    (a ameaça preventiva e a IC ampliada se reforçam).

    Roda sob Regime C (via lei): após Categoria 4 (Adv B), só o Regime C
    pode impor a cláusula contratual padrão (reserva de lei, Art. 22, I, CF);
    A e B forçam `fracao_contratos_acelerados=0` independentemente do input.
    """
    from waas_antitrust.model import WaaSModel, WaaSParametros

    base = {
        "n_empresas": 30,
        "tam_medio_empresa": 150,
        "n_tiques": 30,
        "regime": "C",
        "seed": 7,
        "fracao_violadoras": 0.4,
        "taxa_observacao": 0.4,
    }
    sem = WaaSModel(WaaSParametros(**base, fracao_contratos_acelerados=0.0)).executar()
    com = WaaSModel(WaaSParametros(**base, fracao_contratos_acelerados=1.0)).executar()

    # Direcional: cláusulas devem reduzir o dano social (canal preventivo via
    # g_i_efetivo OU canal reativo via IC-F* ampliada). Menos TCC pode resultar
    # de menos violação — o que é precisamente o sucesso esperado.
    dano_sem = int(sem["dano_acumulado"].max())
    dano_com = int(com["dano_acumulado"].max())
    assert dano_com < dano_sem, (
        f"esperado redução de dano com cláusulas (dissuasão preventiva): "
        f"dano sem={dano_sem}, com={dano_com}"
    )
