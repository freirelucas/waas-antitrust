"""Fixtures compartilhadas dos testes."""

import pytest

from waas_antitrust.model import WaaSModel, WaaSParametros


@pytest.fixture
def params_pequeno():
    """Parâmetros calibrados para testes rápidos."""
    return WaaSParametros(
        n_empresas=5,
        tam_medio_empresa=50,
        n_tiques=4,
        regime="B",
        seed=42,
    )


@pytest.fixture
def modelo_pequeno(params_pequeno):
    """Instância pronta para uso, ainda não executada."""
    return WaaSModel(params_pequeno)


@pytest.fixture
def regimes():
    """Os três regimes institucionais."""
    return ["A", "B", "C"]
