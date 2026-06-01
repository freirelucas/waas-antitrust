"""Testes da camada Hirschman exit-with-equity (R07, exploratório)."""

import pytest

from waas_antitrust.hirschman import (
    custo_exodo_esperado,
    custo_substituicao,
    deve_pagar_com_hirschman,
    g_i_efetivo,
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


def test_modelo_integrado_aumenta_pagamento_com_clausula():
    """End-to-end: fração maior de cláusulas → mais firmas pagam denunciantes
    (a ameaça preventiva e a IC ampliada se reforçam)."""
    from waas_antitrust.model import WaaSModel, WaaSParametros

    base = {
        "n_empresas": 30,
        "tam_medio_empresa": 150,
        "n_tiques": 30,
        "regime": "B",
        "seed": 7,
        "fracao_violadoras": 0.4,
        "taxa_observacao": 0.4,
    }
    sem = WaaSModel(WaaSParametros(**base, fracao_contratos_acelerados=0.0)).executar()
    com = WaaSModel(WaaSParametros(**base, fracao_contratos_acelerados=1.0)).executar()

    # Direcional: com cláusula em todas as firmas, mais TCCs assinados
    # OU menos dano (ou ambos: pagamento direto OU dissuasão preventiva).
    n_tcc_sem = int(sem["n_tcc_assinados"].max())
    n_tcc_com = int(com["n_tcc_assinados"].max())
    dano_sem = int(sem["dano_acumulado"].max())
    dano_com = int(com["dano_acumulado"].max())

    melhora = (n_tcc_com >= n_tcc_sem) and (dano_com <= dano_sem)
    assert melhora, (
        f"esperado mais cooperação ou menos dano com cláusulas: "
        f"TCC {n_tcc_sem}→{n_tcc_com}, dano {dano_sem}→{dano_com}"
    )
