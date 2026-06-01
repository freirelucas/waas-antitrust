"""Testes da Categoria 2 (Mat A, Mat B): suavização Beta-Binomial + bootstrap multi-seed."""

from __future__ import annotations

import numpy as np
import pytest

from waas_antitrust.robustez import (
    IntervaloConfianca,
    beta_binomial_smoothing,
    bootstrap_ci,
    varredura_multi_seed,
)

# ---- Beta-Binomial smoothing ----


def test_beta_binomial_remove_singularidade_em_n_viol_zero():
    """Estimador frequencista 0/0 indefinido; Beta-Binomial retorna média do prior."""
    p_hat = beta_binomial_smoothing(0, 0, alpha=1.0, beta=5.0)
    assert p_hat == pytest.approx(1.0 / 6.0)  # prior mean


def test_beta_binomial_converge_para_frequentista_em_n_grande():
    """Para tentativas → ∞, o estimador colapsa em sucessos/tentativas."""
    p_hat = beta_binomial_smoothing(500, 1000, alpha=1.0, beta=5.0)
    assert p_hat == pytest.approx(0.5, abs=0.01)


def test_beta_binomial_encolhe_para_prior_em_n_pequeno():
    """Em n=1, o MAP fica entre o frequencista (0 ou 1) e a média do prior."""
    p_hat_zero = beta_binomial_smoothing(0, 1, alpha=1.0, beta=5.0)
    p_hat_um = beta_binomial_smoothing(1, 1, alpha=1.0, beta=5.0)
    # Frequencista seria 0.0 e 1.0; o MAP fica encolhido para a média do prior (~0.167)
    assert 0.0 < p_hat_zero < 1.0 / 6.0  # entre 0 e o prior
    assert 1.0 / 6.0 < p_hat_um < 1.0  # entre o prior e 1


def test_beta_binomial_rejeita_argumentos_invalidos():
    with pytest.raises(ValueError):
        beta_binomial_smoothing(-1, 5)
    with pytest.raises(ValueError):
        beta_binomial_smoothing(5, -1)
    with pytest.raises(ValueError):
        beta_binomial_smoothing(6, 5)  # sucessos > tentativas
    with pytest.raises(ValueError):
        beta_binomial_smoothing(1, 5, alpha=0.0)
    with pytest.raises(ValueError):
        beta_binomial_smoothing(1, 5, beta=-1.0)


# ---- bootstrap CI ----


def test_bootstrap_ci_estatistica_pontual_eh_mediana_amostral():
    valores = [1.0, 2.0, 3.0, 4.0, 5.0]
    ci = bootstrap_ci(valores, n_bootstrap=500, seed=0)
    assert ci.n == 5
    assert ci.mediana == pytest.approx(3.0)
    assert ci.inferior <= ci.mediana <= ci.superior


def test_bootstrap_ci_intervalo_estreita_com_amostra_maior():
    """CIs de uma distribuição estável encolhem com N — propriedade clássica."""
    rng = np.random.default_rng(0)
    pequena = rng.normal(0.0, 1.0, size=10).tolist()
    grande = rng.normal(0.0, 1.0, size=200).tolist()
    ci_p = bootstrap_ci(pequena, n_bootstrap=1000, seed=1)
    ci_g = bootstrap_ci(grande, n_bootstrap=1000, seed=1)
    largura_p = ci_p.superior - ci_p.inferior
    largura_g = ci_g.superior - ci_g.inferior
    assert largura_g < largura_p


def test_bootstrap_ci_rejeita_argumentos_invalidos():
    with pytest.raises(ValueError):
        bootstrap_ci([], n_bootstrap=100)
    with pytest.raises(ValueError):
        bootstrap_ci([1.0, 2.0], alpha=0.0)
    with pytest.raises(ValueError):
        bootstrap_ci([1.0, 2.0], alpha=1.0)


# ---- varredura multi-seed ----


def test_varredura_multi_seed_aplica_fabrica_em_cada_seed():
    valores = varredura_multi_seed(lambda s: float(s) ** 2, seeds=[1, 2, 3, 4])
    assert valores == [1.0, 4.0, 9.0, 16.0]


def test_varredura_multi_seed_compoe_com_bootstrap_ci():
    """Caso de uso típico: gerar amostra a partir de seeds e construir o CI."""
    valores = varredura_multi_seed(lambda s: float(s % 5), seeds=list(range(20)))
    ci = bootstrap_ci(valores, n_bootstrap=500, seed=42)
    assert isinstance(ci, IntervaloConfianca)
    assert ci.n == 20
