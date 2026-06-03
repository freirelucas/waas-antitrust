"""Testes da distribuição de fatia de mercado (R13a) e do reporter HHI.

Motivação (Eco B + PM da crítica x10): em mercados digitais o dano segue
**cauda longa**, não uniforme — uma firma de 40% market share que viola
causa muito mais dano que uma de 2%. O modelo agora oferece três modos
explícitos: uniforme (default, compat), Pareto e lognormal.
"""

from __future__ import annotations

import pytest

from waas_antitrust.cenarios import aplicar_cenario
from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Distribuição uniforme (default, compat)
# ----------------------------------------------------------------------


def test_uniforme_default_produz_fatias_iguais():
    """Default `distribuicao_fatia_mercado='uniforme'` ⇒ todas as fatias = 1/n."""
    n = 20
    m = WaaSModel(
        WaaSParametros(
            n_empresas=n,
            tam_medio_empresa=80,
            n_tiques=1,
            seed=3,
        )
    )
    fatias = [e.fatia_mercado for e in m.empresas]
    esperado = 1.0 / n
    assert all(abs(f - esperado) < 1e-12 for f in fatias)
    # Soma exatamente 1 (módulo erro numérico).
    assert abs(sum(fatias) - 1.0) < 1e-9


def test_hhi_uniforme_eh_um_sobre_n():
    """Para n firmas uniformes: HHI = n · (1/n)² = 1/n."""
    n = 25
    m = WaaSModel(WaaSParametros(n_empresas=n, tam_medio_empresa=40, n_tiques=1, seed=5))
    df = m.executar()
    hhi = float(df["hhi"].iloc[-1])
    assert abs(hhi - 1.0 / n) < 1e-9


# ----------------------------------------------------------------------
# Pareto — cauda longa típica de mercados digitais
# ----------------------------------------------------------------------


def test_pareto_produz_cauda_longa_e_normaliza():
    """Pareto: top firma >> média uniforme; HHI > 1/n; soma exata 1."""
    n = 30
    m = WaaSModel(
        WaaSParametros(
            n_empresas=n,
            tam_medio_empresa=100,
            n_tiques=1,
            seed=11,
            distribuicao_fatia_mercado="pareto",
            alpha_pareto=1.16,
        )
    )
    fatias = sorted((e.fatia_mercado for e in m.empresas), reverse=True)
    assert abs(sum(fatias) - 1.0) < 1e-9
    # Top firma significativamente maior que a média uniforme.
    assert fatias[0] > 2.0 * (1.0 / n)
    # HHI maior que sob uniforme (concentração elevada).
    df = m.executar()
    hhi_pareto = float(df["hhi"].iloc[-1])
    assert hhi_pareto > 1.0 / n


def test_pareto_alpha_menor_intensifica_cauda():
    """α menor ⇒ cauda mais pesada ⇒ HHI maior em expectativa."""
    base = dict(
        n_empresas=40,
        tam_medio_empresa=80,
        n_tiques=1,
        seed=17,
        distribuicao_fatia_mercado="pareto",
    )
    df_pesado = WaaSModel(WaaSParametros(**base, alpha_pareto=0.8)).executar()
    df_leve = WaaSModel(WaaSParametros(**base, alpha_pareto=2.5)).executar()
    hhi_pesado = float(df_pesado["hhi"].iloc[-1])
    hhi_leve = float(df_leve["hhi"].iloc[-1])
    assert hhi_pesado > hhi_leve, (
        f"α=0.8 deveria produzir HHI maior que α=2.5; "
        f"pesado={hhi_pesado:.3f}, leve={hhi_leve:.3f}"
    )


# ----------------------------------------------------------------------
# Lognormal
# ----------------------------------------------------------------------


def test_lognormal_produz_heterogeneidade_e_normaliza():
    n = 25
    m = WaaSModel(
        WaaSParametros(
            n_empresas=n,
            tam_medio_empresa=80,
            n_tiques=1,
            seed=23,
            distribuicao_fatia_mercado="lognormal",
            sigma_lognormal=1.0,
        )
    )
    fatias = [e.fatia_mercado for e in m.empresas]
    assert abs(sum(fatias) - 1.0) < 1e-9
    # Heterogeneidade efetiva: pelo menos 5 valores distintos.
    assert len({round(f, 5) for f in fatias}) >= 5


# ----------------------------------------------------------------------
# Validação de entrada
# ----------------------------------------------------------------------


def test_distribuicao_invalida_levanta_value_error():
    with pytest.raises(ValueError, match="distribuicao_fatia_mercado"):
        WaaSModel(
            WaaSParametros(
                n_empresas=4,
                tam_medio_empresa=40,
                n_tiques=1,
                distribuicao_fatia_mercado="exponencial_arbitraria",
            )
        )


# ----------------------------------------------------------------------
# Integração com cenários (R17)
# ----------------------------------------------------------------------


def test_cenario_mercado_digital_br_pareto_ativa_pareto():
    """O novo cenário `mercado_digital_br_pareto` deve produzir HHI alto."""
    p_base = WaaSParametros(n_empresas=25, tam_medio_empresa=120, n_tiques=2, seed=37)
    p_pareto = aplicar_cenario(p_base, "mercado_digital_br_pareto")
    assert p_pareto.distribuicao_fatia_mercado == "pareto"
    assert p_pareto.regime == "C"
    df = WaaSModel(p_pareto).executar()
    hhi = float(df["hhi"].iloc[-1])
    # Pareto deve concentrar fatias bem acima do nível uniforme (1/25 = 0.04).
    assert hhi > 1.0 / 25
