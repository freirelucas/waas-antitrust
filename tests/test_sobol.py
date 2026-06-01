"""Testes da varredura Sobol (modo rápido)."""

import pandas as pd
import pytest

from waas_antitrust.sobol import PROBLEMA_SOBOL_8D, executar_para_sobol


def test_problema_sobol_8d_estrutura():
    """O problema de Sobol tem 8 dimensões nomeadas com limites finitos."""
    assert PROBLEMA_SOBOL_8D["num_vars"] == 8
    assert len(PROBLEMA_SOBOL_8D["names"]) == 8
    assert len(PROBLEMA_SOBOL_8D["bounds"]) == 8
    for nome, (low, high) in zip(
        PROBLEMA_SOBOL_8D["names"], PROBLEMA_SOBOL_8D["bounds"], strict=True
    ):
        assert low < high, f"Limites inválidos para {nome}"


def test_executar_para_sobol_retorna_dict():
    """Cada execução individual produz um dicionário com chaves esperadas."""
    linha_central = [1.5, 0.05, 0.30, 0.7, 0.15, 1.0, 0.10, 0.20]
    resultado = executar_para_sobol(
        linha_central,
        regime="B",
        seed=42,
        n_empresas=4,
        n_tiques=4,
    )
    assert "VP" in resultado
    assert "FP" in resultado
    assert "bem_estar" in resultado
    assert "precisao" in resultado


def test_executar_para_sobol_determinismo():
    """Mesma linha e seed ⇒ resultado idêntico (pareamento de Saltelli preservável)."""
    linha = [1.5, 0.05, 0.30, 0.7, 0.15, 1.0, 0.10, 0.20]
    r1 = executar_para_sobol(linha, regime="B", seed=42, n_empresas=4, n_tiques=4)
    r2 = executar_para_sobol(linha, regime="B", seed=42, n_empresas=4, n_tiques=4)
    assert (r1["VP"], r1["FP"], r1["bem_estar"]) == (r2["VP"], r2["FP"], r2["bem_estar"])


def test_calcular_bem_estar_social():
    """bem_estar social = −(dano + β·FP + γ·custo/w_a); padrão γ=0 ⇒ −(dano + FP)."""
    from waas_antitrust.sobol.execucao import calcular_bem_estar

    assert calcular_bem_estar(dano=100, fp=5, custo_recompensa=1e6, w_a_base=180_000) == -105.0
    pesos = {"beta_fp": 1.0, "gamma_recompensa": 1.0}
    # custo/w_a = 360000/180000 = 2  ⇒  −(100 + 5 + 2) = −107
    assert calcular_bem_estar(100, 5, 360_000, 180_000, pesos) == -107.0


def test_calcular_bem_estar_inclui_exodo_e_multa():
    """Categoria 3 (Eco B): custo_exodo soma como custo social;
    multa_arrecadada credita (entra com sinal +)."""
    from waas_antitrust.sobol.execucao import calcular_bem_estar

    pesos = {
        "beta_fp": 1.0,
        "gamma_recompensa": 0.0,
        "delta_exodo": 0.5,
        "delta_multa": 1.0,
    }
    # exodo = 360000 → exodo/w_a = 2 → contrib = +0,5·2 = 1
    # multa = 360000 → multa/w_a = 2 → contrib = −1·2 = −2 (credita o bem-estar)
    # −(100 + 5 + 0 + 1 − 2) = −104
    bem_estar = calcular_bem_estar(
        100, 5, 0.0, 180_000, pesos=pesos, custo_exodo=360_000, multa_arrecadada=360_000
    )
    assert bem_estar == -104.0


def test_calcular_bem_estar_argumentos_novos_preservam_default_antigo():
    """Sem custo_exodo/multa, a fórmula nova bate com a antiga: backward-compat."""
    from waas_antitrust.sobol.execucao import calcular_bem_estar

    # Pesos default: delta_exodo=0.5, delta_multa=1.0, mas como custo_exodo e
    # multa são 0 (default), os termos não disparam.
    assert calcular_bem_estar(dano=100, fp=5, custo_recompensa=1e6, w_a_base=180_000) == -105.0


def test_calcular_indices_matriz_unica():
    """calcular_indices roda sobre uma matriz única e retorna S1/ST por parâmetro."""
    import numpy as np
    from SALib.sample import sobol as amostragem

    from waas_antitrust.sobol.analise import calcular_indices

    amostras = amostragem.sample(PROBLEMA_SOBOL_8D, 8, calc_second_order=False)
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"bem_estar": rng.normal(size=len(amostras))})
    res = calcular_indices(df, PROBLEMA_SOBOL_8D, "bem_estar")
    assert len(res) == PROBLEMA_SOBOL_8D["num_vars"]
    assert {"parâmetro", "S1", "ST"}.issubset(res.columns)


def test_identificar_regiao_robusta():
    """Marca como robusta quem tem bem-estar positivo e precisão acima do limiar."""
    from waas_antitrust.sobol.analise import identificar_regiao_robusta

    df = pd.DataFrame({"bem_estar": [5, -1, 3], "precisao": [0.9, 0.95, 0.5]})
    out = identificar_regiao_robusta(df, limiar_precisao=0.85)
    assert out["robusta"].tolist() == [True, False, False]


@pytest.mark.slow
def test_varredura_replicada_e_indices():
    """Varredura replicada gera coluna `replica` e índices de Sobol mediados."""
    from waas_antitrust.sobol import executar_varredura
    from waas_antitrust.sobol.analise import calcular_indices_replicado

    df = executar_varredura(n_base=8, regime="B", n_jobs=1, n_empresas=3, n_tiques=4, n_replicas=2)
    assert isinstance(df, pd.DataFrame)
    assert "bem_estar" in df.columns
    assert df["replica"].nunique() == 2

    resumo = calcular_indices_replicado(df, PROBLEMA_SOBOL_8D, metrica="bem_estar")
    assert len(resumo) == PROBLEMA_SOBOL_8D["num_vars"]
    assert {"parâmetro", "S1", "ST", "S1_dp", "ST_dp"}.issubset(resumo.columns)
