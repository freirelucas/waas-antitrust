"""Testes do subjogo global (R02, exploratório/estilizado)."""

import pytest

from waas_antitrust.jogo_global import limiar_switching, trilha_convergencia


def test_limite_tau_zero_formula():
    """No limite τ→0, x* = c·k / (b·(1−k))."""
    b, c, k = 2.0, 1.0, 0.2
    esperado = (c * k) / (b * (1.0 - k))
    assert abs(limiar_switching(b, c, k) - esperado) < 1e-12


def test_converge_quando_tau_para_zero():
    """O erro vs. o limite decresce monotonicamente com τ → 0 (seleção de equilíbrio único)."""
    b, c, k = 2.0, 1.0, 0.2
    limite = limiar_switching(b, c, k, tau=0.0)
    taus = [0.5, 0.1, 0.01, 0.001]
    erros = [abs(x - limite) for x in trilha_convergencia(b, c, k, taus)]
    assert erros == sorted(erros, reverse=True)
    assert erros[-1] < 1e-3


def test_monotonia_economica():
    """Mais represália ⇒ limiar maior (mais cauteloso); mais recompensa ⇒ limiar menor."""
    assert limiar_switching(2.0, 2.0, 0.2) > limiar_switching(2.0, 1.0, 0.2)
    assert limiar_switching(4.0, 1.0, 0.2) < limiar_switching(2.0, 1.0, 0.2)


def test_parametros_invalidos():
    with pytest.raises(ValueError):
        limiar_switching(2.0, 1.0, 1.5)
    with pytest.raises(ValueError):
        limiar_switching(0.0, 1.0, 0.2)
