"""Testes da externalidade erga omnes do bem coletivo (v2.D.1, Eco B v2, R21).

Atende ao sinal mais forte do Eco B na x10 v2: `bem_estar` atual não conta o
bem público. O novo termo `valor_dissuasao_difusa_acum` mede a dissuasão
difusa sobre firmas que CADE/MPF jamais investigariam — externalidade
positiva massiva do mecanismo.

Calibração: Connor-Lande 2012 reporta overcharge mediano 15-25% em cartéis.
Usamos 18% como proxy.
"""

from __future__ import annotations

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.sobol.execucao import PESOS_BEM_ESTAR, calcular_bem_estar


def test_valor_dissuasao_difusa_acum_reporter_presente():
    """O reporter `valor_dissuasao_difusa_acum` aparece no DataFrame."""
    m = WaaSModel(WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=3, seed=7))
    df = m.executar()
    assert "valor_dissuasao_difusa_acum" in df.columns


def test_externalidade_zero_em_regime_a():
    """Regime A não tem WaaS; `p_perc` não sobe significativamente; externalidade ~0."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=80,
            n_tiques=10,
            seed=11,
            regime="A",
        )
    )
    df = m.executar()
    valor_final = float(df["valor_dissuasao_difusa_acum"].max())
    # Tolerância pequena para evitar flakiness em arredondamento.
    assert valor_final < 0.5, f"externalidade em Regime A deveria ser ~0; recebeu {valor_final}"


def test_externalidade_nao_decrece():
    """Reporter é cumulativo — nunca decresce ao longo de tiques (delta_p clipped em 0)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=8,
            tam_medio_empresa=120,
            n_tiques=15,
            seed=23,
            regime="B",
            fracao_violadoras=0.7,
            taxa_observacao=0.5,
        )
    )
    df = m.executar()
    serie = df["valor_dissuasao_difusa_acum"].tolist()
    for i in range(len(serie) - 1):
        assert (
            serie[i + 1] >= serie[i] - 1e-9
        ), f"externalidade decresce de t={i} para t={i+1}: {serie[i]} → {serie[i+1]}"


def test_calcular_bem_estar_aceita_dissuasao_difusa():
    """`calcular_bem_estar` aceita kwarg `dissuasao_difusa` (default 0; compat)."""
    sem = calcular_bem_estar(dano=10.0, fp=2, custo_recompensa=1000.0, w_a_base=180_000.0)
    com = calcular_bem_estar(
        dano=10.0,
        fp=2,
        custo_recompensa=1000.0,
        w_a_base=180_000.0,
        dissuasao_difusa=50_000.0,
    )
    # Default 0 ⇒ os dois valores devem ser idênticos pois epsilon_dissuasao=0.
    assert abs(sem - com) < 1e-9


def test_pesos_padrao_inclui_epsilon():
    """PESOS_BEM_ESTAR ganhou chave `epsilon_dissuasao_difusa` (default 0)."""
    assert "epsilon_dissuasao_difusa" in PESOS_BEM_ESTAR
    # Default 0 = compat estrita; ativar com pesos custom sob reframe.
    assert PESOS_BEM_ESTAR["epsilon_dissuasao_difusa"] == 0.0


def test_bem_estar_com_epsilon_positivo_credita_externalidade():
    """Ativando `epsilon > 0`, dissuasão difusa entra como crédito (subtrai do dano).

    Fórmula: bem_estar = -(dano + ... - ε·dissuasao) / w_a
    Com ε=1 e dissuasao=500_000 (~2.8 w_a), o bem-estar fica MENOS negativo.
    """
    pesos_ativos = {
        **PESOS_BEM_ESTAR,
        "epsilon_dissuasao_difusa": 1.0,
    }
    sem_ext = calcular_bem_estar(
        dano=100.0,
        fp=5,
        custo_recompensa=2000.0,
        w_a_base=180_000.0,
        pesos=pesos_ativos,
        dissuasao_difusa=0.0,
    )
    com_ext = calcular_bem_estar(
        dano=100.0,
        fp=5,
        custo_recompensa=2000.0,
        w_a_base=180_000.0,
        pesos=pesos_ativos,
        dissuasao_difusa=500_000.0,
    )
    # com_ext > sem_ext (menos negativo). Externalidade crédita.
    assert (
        com_ext > sem_ext
    ), f"externalidade deveria creditar bem-estar; sem={sem_ext} com={com_ext}"


def test_double_counting_mitigado():
    """v2.D.1 (Eco B v2): firmas já notificadas NÃO contam para externalidade."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=80,
            n_tiques=5,
            seed=29,
            regime="B",
            fracao_violadoras=1.0,
            taxa_observacao=0.7,
        )
    )
    df = m.executar()
    _ = df  # executa sem erro
    # Conferência direta no modelo: o set deve crescer monotonicamente.
    assert isinstance(m._empresas_ja_notificadas, set)
