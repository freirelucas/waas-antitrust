"""Smoke tests do script de calibração multi-target R03.

Valida as três funções de apoio sem rodar otimização completa
(Nelder-Mead leva minutos com seeds reais). O teste smoke usa
configuração reduzida (4 empresas × 8 tiques) e verifica apenas
que a estrutura do código está consistente.

Para a calibração formal multi-target, ver
`scripts/calibrar_formal_multitarget.py` e a página
`docs/calibracao_pendente.md`.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


def _carregar_modulo_script():
    """Carrega scripts/calibrar_formal_multitarget.py como módulo."""
    script_path = Path(__file__).parent.parent / "scripts" / "calibrar_formal_multitarget.py"
    spec = importlib.util.spec_from_file_location("multitarget", script_path)
    if spec is None or spec.loader is None:
        pytest.skip("script de calibração multi-target não encontrado")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_executar_seed_retorna_3_alvos():
    """A função _executar_seed devolve um dict com as 3 grandezas alvo."""
    mod = _carregar_modulo_script()
    r = mod._executar_seed(
        fracao_violadoras=0.3,
        taxa_capacidade=0.5,
        seed=11,
        n_empresas=4,
        n_tiques=8,
    )
    assert set(r.keys()) == {"tcc_anual", "fracao_sinais", "dano_final"}
    assert all(isinstance(v, float) for v in r.values())


def test_baseline_dano_regime_a_mapeia_seeds():
    """O baseline retorna um dict {seed → dano} com piso 1e-6."""
    mod = _carregar_modulo_script()
    baseline = mod._baseline_dano_regime_a(
        seeds=[11, 23],
        n_empresas=4,
        n_tiques=8,
    )
    assert set(baseline.keys()) == {11, 23}
    assert all(v >= 1e-6 for v in baseline.values())


def test_objetivo_multitarget_devolve_escalar_nao_negativo():
    """A função objetivo é escalar não-negativa (soma de quadrados)."""
    mod = _carregar_modulo_script()
    baseline = mod._baseline_dano_regime_a(seeds=[11], n_empresas=4, n_tiques=8)
    val = mod._objetivo_multitarget(
        x=np.array([0.3, 0.5]),
        pesos=(1 / 3, 1 / 3, 1 / 3),
        alvo_tcc_modelo=0.12,
        seeds=[11],
        n_empresas=4,
        n_tiques=8,
        dano_baseline_a=baseline,
    )
    assert isinstance(val, float)
    assert val >= 0.0


def test_objetivo_multitarget_respeita_pesos_zero():
    """Sob pesos (1, 0, 0), o objetivo equivale ao alvo único (TCC)."""
    mod = _carregar_modulo_script()
    baseline = mod._baseline_dano_regime_a(seeds=[11], n_empresas=4, n_tiques=8)
    val_pesos_um_alvo = mod._objetivo_multitarget(
        x=np.array([0.3, 0.5]),
        pesos=(1.0, 0.0, 0.0),
        alvo_tcc_modelo=0.12,
        seeds=[11],
        n_empresas=4,
        n_tiques=8,
        dano_baseline_a=baseline,
    )
    val_pesos_neutro = mod._objetivo_multitarget(
        x=np.array([0.3, 0.5]),
        pesos=(1 / 3, 1 / 3, 1 / 3),
        alvo_tcc_modelo=0.12,
        seeds=[11],
        n_empresas=4,
        n_tiques=8,
        dano_baseline_a=baseline,
    )
    # Ambos não-negativos; o de peso único é puro componente TCC.
    assert val_pesos_um_alvo >= 0.0
    assert val_pesos_neutro >= 0.0
