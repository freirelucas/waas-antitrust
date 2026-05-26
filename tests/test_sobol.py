"""Testes da varredura Sobol (modo rápido)."""

import pandas as pd
import pytest

from waas_antitrust.sobol import PROBLEMA_SOBOL_8D, executar_para_sobol


def test_problema_sobol_8d_estrutura():
    """O problema de Sobol tem 8 dimensões nomeadas com limites finitos."""
    assert PROBLEMA_SOBOL_8D["num_vars"] == 8
    assert len(PROBLEMA_SOBOL_8D["names"]) == 8
    assert len(PROBLEMA_SOBOL_8D["bounds"]) == 8
    for nome, (low, high) in zip(PROBLEMA_SOBOL_8D["names"], PROBLEMA_SOBOL_8D["bounds"]):
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


@pytest.mark.slow
def test_varredura_curta_completa():
    """Varredura curta executa e retorna DataFrame válido."""
    from waas_antitrust.sobol import executar_varredura

    df = executar_varredura(n_base=4, regime="B", n_jobs=1, n_empresas=3, n_tiques=4)
    assert isinstance(df, pd.DataFrame)
    assert "bem_estar" in df.columns
    assert len(df) > 0
