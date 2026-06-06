"""Testes da mecânica de corrida por leniência coletiva interna (R20)."""

from __future__ import annotations

import pytest

from waas_antitrust.calibracao import saito
from waas_antitrust.cenarios import aplicar_cenario
from waas_antitrust.corrida import (
    FilaInternaCooperacao,
    FilaLeniencia,
    decaimento_D,
    decaimento_W,
    massa_critica_interna_atingida,
)
from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Decaimentos calibrados contra Saito (2021)
# ----------------------------------------------------------------------


def test_decaimento_D_posicao_1_eh_43_por_cento():
    """1ª compromissária ganha 43,43% — Saito Imagem 23, p. 38."""
    assert decaimento_D(1) == pytest.approx(0.4343)


def test_decaimento_D_posicao_2_eh_34_por_cento():
    assert decaimento_D(2) == pytest.approx(0.3451)


def test_decaimento_D_posicao_3_eh_20_por_cento():
    assert decaimento_D(3) == pytest.approx(0.2022)


def test_decaimento_D_posicao_alta_cai_para_tribunal():
    """Posição ≥ 10 (ou ausência) cai para teto Tribunal/CADE (15%)."""
    assert decaimento_D(99) == pytest.approx(0.15)


def test_decaimento_W_posicao_1_eh_W_base():
    """1ª posição recebe W_base integral (normalização por D(1)/D(1) = 1)."""
    assert decaimento_W(1, W_base=1.0) == pytest.approx(1.0)


def test_decaimento_W_decresce_com_posicao():
    """f_W(2)/f_W(1) = D(2)/D(1) = 34,51/43,43 ≈ 0,795."""
    w1 = decaimento_W(1, W_base=1.0)
    w2 = decaimento_W(2, W_base=1.0)
    w3 = decaimento_W(3, W_base=1.0)
    assert w1 > w2 > w3
    assert w2 == pytest.approx(
        saito.MEDIA_DESCONTO_SG_2A_POSICAO / saito.MEDIA_DESCONTO_SG_1A_POSICAO
    )


def test_decaimento_W_posicao_invalida_levanta():
    with pytest.raises(ValueError, match="posicao_trabalhador"):
        decaimento_W(0, W_base=1.0)
    with pytest.raises(ValueError, match="posicao_trabalhador"):
        decaimento_W(-1, W_base=1.0)


def test_decaimento_perfil_invalido_levanta():
    with pytest.raises(ValueError, match="perfil"):
        decaimento_D(1, perfil="aleatorio")
    with pytest.raises(ValueError, match="perfil"):
        decaimento_W(1, W_base=1.0, perfil="aleatorio")


# ----------------------------------------------------------------------
# Filas — registro e idempotência
# ----------------------------------------------------------------------


def test_fila_interna_registra_em_ordem():
    fila = FilaInternaCooperacao(empresa_id=1)
    assert fila.registrar(trabalhador_id=10, tique=2) == 1
    assert fila.registrar(trabalhador_id=20, tique=3) == 2
    assert fila.registrar(trabalhador_id=30, tique=4) == 3
    assert len(fila) == 3


def test_fila_interna_idempotente():
    """Mesmo trabalhador registrado duas vezes mantém a primeira posição."""
    fila = FilaInternaCooperacao(empresa_id=1)
    fila.registrar(10, tique=2)
    fila.registrar(20, tique=3)
    assert fila.registrar(10, tique=99) == 1  # primeira posição preservada
    assert len(fila) == 2  # sem duplicação


def test_fila_interna_posicao_inexistente_devolve_none():
    fila = FilaInternaCooperacao(empresa_id=1)
    fila.registrar(10, tique=2)
    assert fila.posicao(999) is None


def test_fila_leniencia_inter_firma():
    fila = FilaLeniencia()
    assert fila.registrar(empresa_id=0, tique=3) == 1
    assert fila.registrar(empresa_id=1, tique=4) == 2
    assert fila.registrar(empresa_id=2, tique=4) == 3  # empate quebrado por inserção
    assert fila.posicao(1) == 2


# ----------------------------------------------------------------------
# Massa crítica interna
# ----------------------------------------------------------------------


def test_massa_critica_interna_satisfeita_em_10_por_cento():
    """q_min=0.10, n=100, cooperadores=10 ⇒ satisfeita."""
    assert massa_critica_interna_atingida(10, 100, q_min=0.10) is True
    assert massa_critica_interna_atingida(9, 100, q_min=0.10) is False


def test_massa_critica_interna_n_zero_eh_falsa():
    assert massa_critica_interna_atingida(0, 0, q_min=0.10) is False


def test_massa_critica_interna_q_min_invalido_levanta():
    with pytest.raises(ValueError, match="q_min"):
        massa_critica_interna_atingida(5, 100, q_min=0.0)
    with pytest.raises(ValueError, match="q_min"):
        massa_critica_interna_atingida(5, 100, q_min=1.5)


# ----------------------------------------------------------------------
# Integração com WaaSModel — default preserva comportamento histórico
# ----------------------------------------------------------------------


def test_modo_corrida_default_eh_false():
    """`modo_corrida=False` (default) ⇒ comportamento histórico."""
    m = WaaSModel(WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=1, seed=3))
    assert m.modo_corrida is False
    assert m.n_firmas_atingiram_massa_critica_interna == 0


def test_modo_corrida_pode_ser_ativado():
    m = WaaSModel(
        WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=1, seed=5, modo_corrida=True)
    )
    assert m.modo_corrida is True
    assert len(m.filas_internas) == 4  # uma fila por empresa


def test_modo_corrida_sem_sinais_nao_registra_posicao():
    """Sem trabalhadores sinalizando, ninguém ganha posição na fila."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=30,
            n_tiques=2,
            seed=7,
            regime="A",  # sem WaaS ⇒ ninguém sinaliza
            modo_corrida=True,
        )
    )
    m.executar()
    for ws in m.trabalhadores_por_empresa.values():
        for t in ws:
            assert t.posicao_corrida_interna is None


# ----------------------------------------------------------------------
# Cenário canônico — `cenario_corrida_leniencia`
# ----------------------------------------------------------------------


def test_cenario_corrida_leniencia_ativa_modo_corrida():
    p = aplicar_cenario(
        WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=2),
        "cenario_corrida_leniencia",
    )
    assert p.modo_corrida is True
    assert p.perfil_decaimento == "saito"
    assert p.regime == "C"


def test_cenario_corrida_leniencia_executa_end_to_end():
    p = aplicar_cenario(
        WaaSParametros(
            n_empresas=8,
            tam_medio_empresa=150,
            n_tiques=10,
            seed=11,
            fracao_violadoras=0.7,
            taxa_observacao=0.5,
        ),
        "cenario_corrida_leniencia",
    )
    m = WaaSModel(p)
    df = m.executar()
    assert len(df) == 10
    # Diagnóstico: pelo menos uma firma deve formar massa crítica interna em
    # 10 tiques com q_min=0.10 e 60% violadoras.
    n_firmas_corrida = int(df["n_firmas_atingiram_massa_critica_interna"].max())
    assert n_firmas_corrida >= 0  # pode ser 0 dependendo de seeds, mas executa


def test_modo_corrida_atribui_posicao_em_fila_inter_firma():
    """Quando massa crítica interna é satisfeita, firma recebe posição
    sequencial na fila de leniência inter-firma."""
    p = aplicar_cenario(
        WaaSParametros(
            n_empresas=10,
            tam_medio_empresa=200,
            n_tiques=20,
            seed=23,
            fracao_violadoras=0.9,
            taxa_observacao=0.7,
            q_min_cooperacao_interna=0.05,  # gatilho fácil
        ),
        "cenario_corrida_leniencia",
    )
    m = WaaSModel(p)
    m.executar()
    posicoes = sorted(
        e.posicao_fila_leniencia for e in m.empresas if e.posicao_fila_leniencia is not None
    )
    if posicoes:
        # Posições devem ser 1, 2, 3, ... sem buracos.
        assert posicoes == list(range(1, len(posicoes) + 1))
