"""Testes do subjogo global (R02, exploratório/estilizado).

R20 + Mat A v2 (x10 v2): testes para `limiar_switching_por_posicao` que
explicita o caráter escalonado da oferta do bem coletivo sob LCMC.
"""

import pytest

from waas_antitrust.jogo_global import (
    familia_limiares_por_posicao,
    limiar_switching,
    limiar_switching_por_posicao,
    trilha_convergencia,
)


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


# ----------------------------------------------------------------------
# R20 + Mat A v2 — limiar Saito por posição (oferta escalonada do bem coletivo)
# ----------------------------------------------------------------------


def test_limiar_posicao_1_iguala_limiar_base():
    """Posição 1 na fila intra-firma deve dar o limiar Saito sem decaimento."""
    b, c, k_rel = 2.0, 1.0, 0.2
    base = limiar_switching(b, c, k_rel)
    pos1 = limiar_switching_por_posicao(b, c, k_rel, posicao_trabalhador=1)
    assert abs(base - pos1) < 1e-9


def test_limiar_cresce_com_posicao():
    """Mat A v2: oferta escalonada do bem coletivo. Quanto mais distante o
    trabalhador da posição 1, MENOR sua recompensa esperada (decaimento Saito)
    ⇒ MAIOR seu limiar de switching (mais cauteloso)."""
    b, c, k_rel = 2.0, 1.0, 0.2
    x1 = limiar_switching_por_posicao(b, c, k_rel, posicao_trabalhador=1)
    x2 = limiar_switching_por_posicao(b, c, k_rel, posicao_trabalhador=2)
    x3 = limiar_switching_por_posicao(b, c, k_rel, posicao_trabalhador=3)
    assert x1 < x2 < x3, f"limiares devem crescer com posição; {x1} {x2} {x3}"


def test_familia_limiares_explicita_n_estrela_finito():
    """Reformulação Prop. 1 sob LCMC: existe n* finito de posições tolerável.
    A família de limiares deve ser monotonicamente crescente."""
    b, c, k_rel = 2.0, 1.0, 0.2
    familia = familia_limiares_por_posicao(b, c, k_rel, posicoes=(1, 2, 3, 4, 5))
    assert len(familia) == 5
    # Monotonicidade estrita: cada posição tem limiar > posição anterior.
    for i in range(len(familia) - 1):
        assert familia[i] < familia[i + 1], f"limiar não-monotônico em posição {i+1}→{i+2}"


def test_limiar_posicao_invalida_levanta():
    with pytest.raises(ValueError, match="posicao_trabalhador"):
        limiar_switching_por_posicao(2.0, 1.0, 0.2, posicao_trabalhador=0)


def test_limiar_posicao_9_no_piso_tribunal():
    """Posições ≥ 9 caem no piso Tribunal/CADE de 15%; o limiar é o MESMO
    para posições 9, 10, 11. Captura o teto de Saito (Imagem 25, p. 39)."""
    b, c, k_rel = 2.0, 1.0, 0.2
    x9 = limiar_switching_por_posicao(b, c, k_rel, posicao_trabalhador=9)
    x10 = limiar_switching_por_posicao(b, c, k_rel, posicao_trabalhador=10)
    x11 = limiar_switching_por_posicao(b, c, k_rel, posicao_trabalhador=11)
    assert abs(x9 - x10) < 1e-9
    assert abs(x10 - x11) < 1e-9


def test_limiar_perfil_invalido_levanta():
    with pytest.raises(ValueError, match="perfil"):
        limiar_switching_por_posicao(2.0, 1.0, 0.2, posicao_trabalhador=1, perfil="xyz")
