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
        "falsificacao",
        "internacional",
        "painel",
        "sankey",
        "variedade",
    ],
)
def test_viz_stubs_levantam_not_implemented(modulo):
    """Os 8 stubs de viz remanescentes (ainda no caderno) levantam NotImplementedError.
    `cascata` foi implementada no reframe v2 (Commit 6) e ganhou teste próprio."""
    mod = importlib.import_module(f"waas_antitrust.viz.{modulo}")
    with pytest.raises(NotImplementedError):
        mod.gerar_figura()


def test_painel_macro_gera_figura():
    """`painel_macro.gerar_figura` retorna (Figure, [4 Axes]) do painel 2×2.
    Tela de simulação macro: detecção global, massa crítica, bem-estar,
    capital social residual."""
    from waas_antitrust.viz import painel_macro

    aplicar_estilo()
    fig, axes = painel_macro.gerar_figura()
    assert fig is not None
    assert len(axes) == 4
    plt.close(fig)


def test_erosao_gera_figura():
    """`erosao.gerar_figura` retorna (Figure, Axes) com 3 trajetórias de
    `capital_social_residual` (alpha=0/0.2/0.5). Implementada no Commit 9
    do reframe v2 (R26 Coleman)."""
    from waas_antitrust.viz import erosao

    aplicar_estilo()
    fig, ax = erosao.gerar_figura(n_tiques=10, seed=7)
    assert fig is not None
    assert ax is not None
    assert "Capital social" in ax.get_ylabel()
    plt.close(fig)


def test_cascata_gera_figura():
    """`cascata.gerar_figura` retorna (Figure, Axes) com a curva sigmoidal
    de formação de massa crítica + linhas de gatilho q_min e k_rel.
    Implementada no Commit 6 do reframe v2."""
    from waas_antitrust.viz import cascata

    aplicar_estilo()
    fig, ax = cascata.gerar_figura(n_tiques=20, q_min=0.10, k_rel=0.05, seed=7)
    assert fig is not None
    assert ax is not None
    # Eixos com label e título corretos.
    assert "Tique" in ax.get_xlabel()
    assert "cooperando" in ax.get_ylabel().lower()
    plt.close(fig)
