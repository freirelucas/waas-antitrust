"""Testes das visualizações."""

import importlib

import matplotlib
import pytest

matplotlib.use("Agg")  # backend não-interativo
import matplotlib.pyplot as plt

from waas_antitrust.viz import PALETA, aplicar_estilo, fase, inversao


def test_paleta_tem_chaves_esperadas():
    """A paleta contém as cores canônicas dos regimes."""
    for chave in ["A", "B", "C", "adv", "cade"]:
        assert chave in PALETA
        assert PALETA[chave].startswith("#")


def test_inversao_gera_figura():
    aplicar_estilo()
    fig, axes = inversao.gerar_figura()
    assert fig is not None
    assert len(axes) == 2
    plt.close(fig)


def test_fase_gera_figura():
    aplicar_estilo()
    fig, ax = fase.gerar_figura()
    assert fig is not None
    plt.close(fig)


@pytest.mark.parametrize(
    "modulo",
    [
        "adversarial",
        "bootstrap",
        "cade",
        "cascata",
        "falsificacao",
        "internacional",
        "painel",
        "sankey",
        "variedade",
    ],
)
def test_viz_stubs_levantam_not_implemented(modulo):
    """Os 9 stubs de viz (ainda no caderno) levantam NotImplementedError."""
    mod = importlib.import_module(f"waas_antitrust.viz.{modulo}")
    with pytest.raises(NotImplementedError):
        mod.gerar_figura()
