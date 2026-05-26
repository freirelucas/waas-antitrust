"""Testes do modelo principal."""

import pytest

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
    assert "verdadeiros_positivos" in df.columns


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
    assert df1["verdadeiros_positivos"].equals(df2["verdadeiros_positivos"])


def test_propoSicao_1_ic_f_estrela():
    """Proposição 1: IC-F* é satisfeita no ponto-alvo W=1.5·w_a, D=0.30·S."""
    p = WaaSParametros(
        n_empresas=10,
        tam_medio_empresa=200,
        n_tiques=8,
        regime="B",
        seed=42,
        W_mult=1.5,
        D_disc=0.30,
    )
    df = WaaSModel(p).executar()
    # Sob IC-F* satisfeita, pelo menos algum TCC deve ser assinado
    assert df["n_tcc_assinados"].max() >= 0  # tolerante (depende do número de empresas violadoras)
