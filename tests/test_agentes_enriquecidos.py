"""Testes do enriquecimento heterogêneo dos agentes (R14, exploratório).

Cada teste verifica um canal ortogonal ao R01 (dissuasão por detecção
endógena), sem violar as Proposições 1–3.
"""

from __future__ import annotations

import pytest

from waas_antitrust.agents import TrabalhadorAgent
from waas_antitrust.model import WaaSModel, WaaSParametros

# ---- TrabalhadorAgent: vesting individual derivado de anos_carreira ----


def test_fracao_vested_individual_respeita_cliff_e_acelera_em_4y():
    """Antes do cliff (anos < 1) ⇒ 0; depois linear até 1 em 4 anos."""

    class _ModeloMock:
        rng = None  # placeholder; não usado nas asserções abaixo

    # Construímos sem chamar __init__ completo para testar só a property.
    t = TrabalhadorAgent.__new__(TrabalhadorAgent)
    t.anos_carreira = 0.5
    assert t.fracao_vested_individual == 0.0  # cliff
    t.anos_carreira = 1.0
    assert t.fracao_vested_individual == pytest.approx(0.25)
    t.anos_carreira = 2.0
    assert t.fracao_vested_individual == pytest.approx(0.5)
    t.anos_carreira = 4.0
    assert t.fracao_vested_individual == pytest.approx(1.0)
    t.anos_carreira = 6.0
    assert t.fracao_vested_individual == pytest.approx(1.0)  # clip em 1


# ---- TrabalhadorAgent: tolerância à represália heterogênea ----


def test_heterogeneidade_tolerancia_quando_sigma_zero_eh_homogenea():
    """sigma_tolerancia_represalia=0 (default) ⇒ todos tol=1 (compat)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=40,
            n_tiques=1,
            seed=5,
            regime="B",
            sigma_tolerancia_represalia=0.0,
        )
    )
    tols = [t.tolerancia_represalia for ws in m.trabalhadores_por_empresa.values() for t in ws]
    assert all(tol == 1.0 for tol in tols)


def test_heterogeneidade_tolerancia_quando_sigma_positivo_dispersa():
    """sigma_tolerancia_represalia=0.3 ⇒ distribuição dispersa em torno de 1."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=200,
            n_tiques=1,
            seed=5,
            regime="B",
            sigma_tolerancia_represalia=0.3,
        )
    )
    tols = [t.tolerancia_represalia for ws in m.trabalhadores_por_empresa.values() for t in ws]
    assert len(set(round(x, 3) for x in tols)) > 1  # heterogeneidade efetiva
    # Todos clipados em [0.2, 2.0]
    assert all(0.2 <= tol <= 2.0 for tol in tols)
    # Média próxima de 1
    media = sum(tols) / len(tols)
    assert abs(media - 1.0) < 0.1


# ---- EmpresaAgent: cultura de compliance atenua severidade ----


def test_cultura_compliance_reduz_dano_quando_peso_positivo():
    """ω positivo + cultura ∈ [0,1] sorteada por firma ⇒ menos dano que com ω=0.

    Canal ortogonal ao R01: a firma ainda decide violar pela atratividade g_i,
    mas a severidade efetiva σ cai (programa de integridade interno).
    Por consequência, sanção esperada e dano marginal por tique diminuem.
    """
    base = dict(
        n_empresas=20,
        tam_medio_empresa=120,
        n_tiques=40,
        seed=19,
        regime="B",
        fracao_violadoras=0.5,
        taxa_observacao=0.4,
    )
    df_sem = WaaSModel(WaaSParametros(**base, peso_cultura_compliance=0.0)).executar()
    df_com = WaaSModel(WaaSParametros(**base, peso_cultura_compliance=0.5)).executar()
    # σ menor ⇒ sancao_esperada menor ⇒ multa arrecadada acumulada cai.
    multa_sem = float(df_sem["multa_arrecadada_acum"].max())
    multa_com = float(df_com["multa_arrecadada_acum"].max())
    assert multa_com < multa_sem, (
        f"esperado multa_com<multa_sem com cultura ativa; "
        f"sem={multa_sem:.0f}, com={multa_com:.0f}"
    )


# ---- AutoridadeAgent: prioridade digital eleva acurácia ----


def test_prioridade_digital_eleva_acuracia_efetiva():
    """`prioridade_digital_autoridade > 0` ⇒ ρ_efetivo > ρ ⇒ mais VP, menos FN."""
    base = dict(
        n_empresas=20,
        tam_medio_empresa=150,
        n_tiques=30,
        seed=29,
        regime="B",
        fracao_violadoras=0.5,
        taxa_observacao=0.4,
    )
    df_sem = WaaSModel(WaaSParametros(**base, prioridade_digital_autoridade=0.0)).executar()
    df_com = WaaSModel(WaaSParametros(**base, prioridade_digital_autoridade=0.9)).executar()
    vp_sem = int(df_sem["verdadeiros_positivos_acum"].max())
    vp_com = int(df_com["verdadeiros_positivos_acum"].max())
    assert vp_com >= vp_sem, f"esperado VP_com>=VP_sem; sem={vp_sem}, com={vp_com}"


# ---- Memória dos agentes ----


def test_historico_observou_acumula_em_violadoras():
    """`historico_observou` cresce monotonamente em trabalhadores de violadoras."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=200,
            n_tiques=10,
            seed=37,
            regime="B",
            fracao_violadoras=0.8,
            taxa_observacao=0.6,
        )
    )
    m.executar()
    historicos = [t.historico_observou for ws in m.trabalhadores_por_empresa.values() for t in ws]
    # Não-negatividade
    assert all(h >= 0 for h in historicos)
    # Alguma observação ocorreu
    assert sum(historicos) > 0


def test_n_denuncias_acum_cresce_quando_massa_critica_dispara():
    """A firma registra cada disparo de massa crítica em `n_denuncias_acum`."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=10,
            tam_medio_empresa=200,
            n_tiques=20,
            seed=43,
            regime="B",
            fracao_violadoras=0.7,
            taxa_observacao=0.5,
        )
    )
    m.executar()
    total = sum(e.n_denuncias_acum for e in m.empresas)
    # Pelo menos uma denúncia interna disparou ao longo de 20 tiques.
    assert total >= 1
