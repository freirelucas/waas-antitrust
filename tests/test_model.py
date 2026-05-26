"""Testes do modelo principal."""

import pytest

from waas_antitrust.agents import EmpresaAgent
from waas_antitrust.model import WaaSModel, WaaSParametros


@pytest.mark.parametrize("regime", ["A", "B", "C"])
def test_modelo_executa_em_todos_regimes(regime):
    """O modelo executa sem erro nos três regimes."""
    params = WaaSParametros(
        n_empresas=3,
        tam_medio_empresa=30,
        n_tiques=4,
        regime=regime,
        seed=42,
    )
    modelo = WaaSModel(params)
    df = modelo.executar()
    assert df is not None
    assert len(df) == 4
    assert "verdadeiros_positivos_acum" in df.columns


def test_regime_a_produz_silencio_em_horizonte_curto():
    """No Regime A não há canal de denúncia; sinais devem ser zero."""
    params = WaaSParametros(
        n_empresas=3,
        tam_medio_empresa=30,
        n_tiques=4,
        regime="A",
        seed=42,
    )
    df = WaaSModel(params).executar()
    assert df["n_sinais"].sum() == 0


def test_regime_b_produz_sinais():
    """No Regime B, o canal WaaS está ativo; deve haver sinais."""
    params = WaaSParametros(
        n_empresas=8,
        tam_medio_empresa=200,
        n_tiques=8,
        regime="B",
        seed=42,
    )
    df = WaaSModel(params).executar()
    assert df["n_sinais"].sum() > 0


def test_modelo_eh_reprodutivel_dado_seed():
    """Mesma seed deve produzir o mesmo resultado."""
    p = WaaSParametros(n_empresas=5, tam_medio_empresa=100, n_tiques=6, regime="B", seed=7)
    df1 = WaaSModel(p).executar()
    df2 = WaaSModel(p).executar()
    assert df1["n_sinais"].equals(df2["n_sinais"])
    assert df1["verdadeiros_positivos_acum"].equals(df2["verdadeiros_positivos_acum"])


def test_proposicao_1_ic_f_estrela_satisfazivel_no_ponto_alvo():
    """Proposição 1: no ponto-alvo (W=1,5·w_a, D=0,30·S) existe firma com D > W."""
    p = WaaSParametros(seed=42, W_mult=1.5, D_disc=0.30)
    modelo = WaaSModel(p)
    empresa = EmpresaAgent(
        modelo,
        id_empresa=999,
        sigma=0.6,
        eh_violadora=True,
        n_trabalhadores=500,
        fatia_mercado=0.05,
        R_receita=500 * p.R_por_trabalhador,
    )
    D_val = p.D_disc * empresa.sancao_esperada()
    W_total = 20 * modelo._W_esperado(p.w_a_base)  # 20 denunciantes a 1,5·w_a
    assert D_val > W_total
    assert empresa.satisfaz_ic_f_estrela(W_total, D_val) is True


def test_ic_f_estrela_viola_com_recompensa_excessiva():
    """Caso espelho: desconto baixo e recompensa total enorme ⇒ IC-F* viola."""
    p = WaaSParametros(seed=42)
    modelo = WaaSModel(p)
    empresa = EmpresaAgent(
        modelo,
        id_empresa=999,
        sigma=0.3,
        eh_violadora=True,
        n_trabalhadores=60,
        fatia_mercado=0.05,
        R_receita=60 * p.R_por_trabalhador,
    )
    D_val = 0.10 * empresa.sancao_esperada()
    W_total = 500 * modelo._W_esperado(p.w_a_base)
    assert W_total > D_val
    assert empresa.satisfaz_ic_f_estrela(W_total, D_val) is False


def test_canal_falso_reporte_gera_falsos_positivos():
    """R04: o canal de falso reporte é a fonte de falsos positivos (sem ele, FP≡0)."""
    base = dict(
        n_empresas=20,
        tam_medio_empresa=120,
        n_tiques=40,
        regime="B",
        seed=3,
        fracao_violadoras=0.2,
        rho=0.6,
    )
    sem = WaaSModel(WaaSParametros(**base, taxa_falso_reporte=0.0)).executar()
    com = WaaSModel(WaaSParametros(**base, taxa_falso_reporte=0.6)).executar()
    assert sem["falsos_positivos_acum"].max() == 0
    assert com["falsos_positivos_acum"].max() > 0


def test_dissuasao_endogena_reduz_violadoras_no_regime_b():
    """R01: o canal WaaS (B) eleva a detecção percebida e DETER a violação vs. Regime A."""
    base = dict(
        n_empresas=30,
        tam_medio_empresa=150,
        n_tiques=40,
        seed=11,
        fracao_violadoras=0.5,
        taxa_observacao=0.4,
    )
    df_a = WaaSModel(WaaSParametros(**base, regime="A")).executar()
    df_b = WaaSModel(WaaSParametros(**base, regime="B")).executar()
    viol_a = df_a["n_violadoras_ativas"].tail(10).mean()
    viol_b = df_b["n_violadoras_ativas"].tail(10).mean()
    # canal de dissuasão da Prop. 3: B reduz as violadoras ativas; A não deter
    assert viol_b < viol_a
    assert viol_a >= df_a["n_violadoras_ativas"].iloc[0]
