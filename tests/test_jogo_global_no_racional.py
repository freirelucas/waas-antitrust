"""Testes da integração `jogo_global.x*` no arquétipo racional (R02a).

Mat B na crítica x10: o subjogo de Morris-Shin (`jogo_global.py`) deriva
o limiar de switching único `x*` em forma fechada, mas não está
integrado à dinâmica de arquétipos do ABM. Estes testes verificam a
integração opt-in via `usar_x_estrela_no_racional`.
"""

from __future__ import annotations

import pytest

from waas_antitrust.agents import TrabalhadorAgent
from waas_antitrust.jogo_global import limiar_switching
from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Compatibilidade — default preserva o caminho histórico
# ----------------------------------------------------------------------


def test_default_eh_caminho_historico():
    """Default `usar_x_estrela_no_racional=False` ⇒ comportamento original."""
    m = WaaSModel(WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=1, seed=3))
    assert m.usar_x_estrela_no_racional is False


def test_flag_opcional_pode_ser_ativada():
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=40,
            n_tiques=1,
            seed=5,
            usar_x_estrela_no_racional=True,
        )
    )
    assert m.usar_x_estrela_no_racional is True


# ----------------------------------------------------------------------
# Comportamento determinístico do limiar — Morris-Shin τ→0
# ----------------------------------------------------------------------


def test_limiar_switching_eh_funcao_de_b_c_k_tau():
    """`limiar_switching` é determinístico para (b, c, k, τ)."""
    x1 = limiar_switching(b=2.0, c=1.0, k=0.1, tau=0.0)
    x2 = limiar_switching(b=2.0, c=1.0, k=0.1, tau=0.0)
    assert x1 == x2


def test_limiar_switching_no_limite_morris_shin_eh_c_k_sobre_b_1_menos_k():
    """Limite τ→0: x* = c·k / [b·(1−k)]."""
    b, c, k = 2.0, 1.0, 0.1
    esperado = c * k / (b * (1.0 - k))
    obtido = limiar_switching(b=b, c=c, k=k, tau=0.0)
    assert obtido == pytest.approx(esperado)


# ----------------------------------------------------------------------
# Integração no decidir_sinal — trabalhador comparativo
# ----------------------------------------------------------------------


def _trabalhador_construido(modelo, observou=True):
    t = TrabalhadorAgent.__new__(TrabalhadorAgent)
    # Campos mínimos para `decidir_sinal` rodar.
    t.model = modelo
    t.arquetipo = "racional"
    t.observou = observou
    t.w_a = 180_000.0
    t.tolerancia_represalia = 1.0
    t.status = "ativo"
    return t


def test_racional_com_x_estrela_compara_sinal_contra_limiar():
    """Com flag True, decisão é `s_i >= x*` em vez de IR-W direta."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=2,
            tam_medio_empresa=30,
            n_tiques=1,
            seed=11,
            usar_x_estrela_no_racional=True,
            k_rel=0.10,
            tau_ruido=0.0,
        )
    )
    t = _trabalhador_construido(m)
    # b = W_esperado / w_a = (1.5·w_a) / w_a = 1.5.
    # c = r · tol · 2 = 0.15 · 1 · 2 = 0.30 (em unidades de w_a).
    # k = 0.10; τ = 0 ⇒ x* = c·k/(b·(1−k)) = 0.30·0.10 / (1.5·0.90) = 0.0222.
    W_esperado = 1.5 * t.w_a
    x_estrela = limiar_switching(b=1.5, c=0.30, k=0.10, tau=0.0)

    # Sinal acima do limiar: sinaliza.
    sinaliza = t.decidir_sinal(
        s_i=x_estrela + 0.01, phi_vizinhos=0.0, W_esperado=W_esperado, r=0.15, F_falso=1.0
    )
    assert sinaliza == 1

    # Sinal abaixo: não sinaliza.
    nao_sinaliza = t.decidir_sinal(
        s_i=x_estrela - 0.01, phi_vizinhos=0.0, W_esperado=W_esperado, r=0.15, F_falso=1.0
    )
    assert nao_sinaliza == 0


def test_racional_sem_x_estrela_continua_usando_ir_w():
    """Sem flag, comportamento histórico é preservado (IR-W direta)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=2,
            tam_medio_empresa=30,
            n_tiques=1,
            seed=13,
            usar_x_estrela_no_racional=False,
        )
    )
    t = _trabalhador_construido(m)
    # Com W enorme e r baixo, ganho líquido positivo → sinaliza qualquer s_i.
    sinaliza = t.decidir_sinal(
        s_i=0.001, phi_vizinhos=0.0, W_esperado=100.0 * t.w_a, r=0.01, F_falso=0.1
    )
    assert sinaliza == 1


def test_racional_com_x_estrela_lida_com_W_zero():
    """Quando W=0 (regime A), o helper retorna 0 sem levantar."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=2,
            tam_medio_empresa=30,
            n_tiques=1,
            seed=17,
            usar_x_estrela_no_racional=True,
        )
    )
    t = _trabalhador_construido(m)
    decisao = t.decidir_sinal(s_i=0.5, phi_vizinhos=0.0, W_esperado=0.0, r=0.15, F_falso=1.0)
    assert decisao == 0


def test_racional_com_x_estrela_nao_observou():
    """Mesmo com flag ativada, sem observação não sinaliza."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=2,
            tam_medio_empresa=30,
            n_tiques=1,
            seed=19,
            usar_x_estrela_no_racional=True,
        )
    )
    t = _trabalhador_construido(m, observou=False)
    decisao = t.decidir_sinal(
        s_i=10.0, phi_vizinhos=0.0, W_esperado=1.5 * t.w_a, r=0.15, F_falso=1.0
    )
    assert decisao == 0


# ----------------------------------------------------------------------
# End-to-end — modelo completo roda nos dois modos
# ----------------------------------------------------------------------


def test_modelo_completo_executa_em_ambos_modos():
    """Smoke test: o modelo completo roda em ambos os modos sem erro."""
    base = dict(n_empresas=6, tam_medio_empresa=80, n_tiques=5, seed=23, regime="B")
    df_hist = WaaSModel(WaaSParametros(**base, usar_x_estrela_no_racional=False)).executar()
    df_x = WaaSModel(WaaSParametros(**base, usar_x_estrela_no_racional=True)).executar()
    assert len(df_hist) == 5
    assert len(df_x) == 5
