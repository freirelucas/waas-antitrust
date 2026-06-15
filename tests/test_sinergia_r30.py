"""Testes da sinergia entre autoridades internacionais (R30, LCMC global).

Duas alavancas independentes:

1. **Grupos econômicos consolidados** (`usar_escrow_consolidado_grupo`):
   firmas no mesmo grupo (jurisdições diferentes da mesma multinacional)
   pool de depósitos para o gatilho de massa crítica. Paralelo: MoU
   bilateral CADE-DOJ-ATR 2019 ou cooperação ICN.

2. **Coordenação internacional** (`coordenacao_internacional ∈ [0, 1]`):
   amplifica o sinal Schelling erga omnes — cada abertura eleva `p_perc`
   em TODAS as outras firmas, modelando o efeito notícia ICN/OECD.

Compat estrita: ambos defaults preservam comportamento bit-a-bit.
"""

from __future__ import annotations

import pytest

from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Backward compat estrita
# ----------------------------------------------------------------------


def test_defaults_compat_estrita():
    """Default `grupos_economicos=None` ⇒ cada firma seu grupo;
    `usar_escrow_consolidado_grupo=False`, `coordenacao_internacional=0`."""
    p = WaaSParametros(n_empresas=3, tam_medio_empresa=20, n_tiques=2, seed=11)
    assert p.grupos_economicos is None
    assert p.usar_escrow_consolidado_grupo is False
    assert p.coordenacao_internacional == 0.0
    m = WaaSModel(p)
    assert m.grupos_economicos == (0, 1, 2)
    assert m.usar_escrow_consolidado_grupo is False
    assert m.coordenacao_internacional == 0.0


def test_reporters_zero_sob_default():
    """Sob default, reporters R30 nunca saem de 0."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=5,
            tam_medio_empresa=40,
            n_tiques=10,
            seed=11,
            regime="B",
            usar_escrow_explicito=True,
        )
    )
    df = m.executar()
    assert "n_aberturas_consolidadas_grupo_acum" in df.columns
    assert "n_boosts_coordenacao_intl_acum" in df.columns
    assert df["n_aberturas_consolidadas_grupo_acum"].max() == 0
    assert df["n_boosts_coordenacao_intl_acum"].max() == 0


def test_grupos_economicos_tamanho_invalido_levanta():
    """`grupos_economicos` deve ter tamanho `n_empresas`."""
    with pytest.raises(ValueError, match="tamanho n_empresas"):
        WaaSModel(
            WaaSParametros(
                n_empresas=3,
                tam_medio_empresa=10,
                n_tiques=2,
                seed=13,
                grupos_economicos=(0, 0),  # tamanho 2 ≠ 3
            )
        )


# ----------------------------------------------------------------------
# Grupos econômicos: consolidação cross-jurisdicional
# ----------------------------------------------------------------------


def test_grupo_unitario_no_op():
    """Grupos com 1 firma só não acionam o gatilho consolidado."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=20,
            n_tiques=8,
            seed=17,
            regime="B",
            usar_escrow_explicito=True,
            usar_escrow_consolidado_grupo=True,
            grupos_economicos=(0, 1, 2),  # cada firma um grupo
        )
    )
    df = m.executar()
    assert df["n_aberturas_consolidadas_grupo_acum"].max() == 0


def test_grupo_multinacional_aciona_consolidada():
    """Grupo de 3 firmas com depósitos somados acima de q_min
    dispara abertura em todas as firmas do grupo simultaneamente."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=30,
            n_tiques=2,
            seed=19,
            regime="B",
            usar_escrow_explicito=True,
            usar_escrow_consolidado_grupo=True,
            grupos_economicos=(0, 0, 0, 1),  # 3 firmas do grupo 0 + 1 isolada
            q_min_cooperacao_interna=0.10,
        )
    )
    autoridade = m.autoridade
    # Calcula total de trabalhadores nas firmas do grupo 0 e deposita o
    # suficiente para passar q_min=0.10 em nível consolidado.
    total_trab_grupo = sum(m.empresas[fid].n_trabalhadores for fid in (0, 1, 2))
    n_depositos = int(total_trab_grupo * 0.15) + 1  # garante > 10%
    for i in range(n_depositos):
        autoridade.depositar_condicional(
            id_empresa=i % 3,  # distribui entre as 3 firmas do grupo 0
            id_trabalhador=100 + i,
            qualidade_prova=0.5,
            tique=0,
        )
    abertas = m._abrir_escrow_consolidado_por_grupo()
    assert abertas == {0, 1, 2}
    assert m.n_aberturas_consolidadas_grupo_acum == 1
    # Cada firma aberta ⇒ caso aceito pelo CADE.
    assert len(autoridade.casos_neste_tique) == 3


def test_grupo_consolidado_nao_dispara_se_total_abaixo_q_min():
    """Quando soma de depósitos no grupo < q_min × soma de trabalhadores,
    nenhuma firma abre via gatilho consolidado."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=50,
            n_tiques=2,
            seed=23,
            regime="B",
            usar_escrow_explicito=True,
            usar_escrow_consolidado_grupo=True,
            grupos_economicos=(0, 0, 0),
            q_min_cooperacao_interna=0.20,  # alto
        )
    )
    autoridade = m.autoridade
    # Apenas 5 depósitos / 150 trabalhadores = 3% ≪ 20%.
    for i in range(5):
        autoridade.depositar_condicional(
            id_empresa=i % 3,
            id_trabalhador=200 + i,
            qualidade_prova=0.5,
            tique=0,
        )
    abertas = m._abrir_escrow_consolidado_por_grupo()
    assert abertas == set()
    assert m.n_aberturas_consolidadas_grupo_acum == 0


# ----------------------------------------------------------------------
# Coordenação internacional: amplificação do sinal Schelling
# ----------------------------------------------------------------------


def test_coordenacao_intl_no_op_sob_zero():
    """`coordenacao_internacional=0` não altera `p_perc`."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=30,
            n_tiques=2,
            seed=29,
            regime="B",
            usar_escrow_explicito=True,
            coordenacao_internacional=0.0,
        )
    )
    p_antes = m.p_perc
    m._aplicar_coordenacao_internacional(set())
    assert m.p_perc == p_antes
    assert m.n_boosts_coordenacao_intl_acum == 0


def test_coordenacao_intl_eleva_p_perc_com_abertura():
    """Quando há ao menos 1 abertura no tique e
    `coordenacao_internacional>0`, `p_perc` sobe (cap em `_g_max`)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=30,
            n_tiques=2,
            seed=31,
            regime="B",
            usar_escrow_explicito=True,
            coordenacao_internacional=0.8,
        )
    )
    # Simula 2 firmas com notificada_no_periodo=True
    m.empresas[0].notificada_no_periodo = True
    m.empresas[1].notificada_no_periodo = True
    p_antes = m.p_perc
    m._aplicar_coordenacao_internacional(set())
    assert m.p_perc > p_antes
    assert m.p_perc <= m._g_max
    assert m.n_boosts_coordenacao_intl_acum == 1


def test_coordenacao_intl_combinada_com_grupo_consolidado_end_to_end():
    """Cenário canônico: grupos + coordenação ligadas devem produzir
    pelo menos uma abertura consolidada e/ou boost em janelas razoáveis."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=80,
            n_tiques=20,
            seed=2026,
            regime="B",
            usar_escrow_explicito=True,
            usar_escrow_consolidado_grupo=True,
            coordenacao_internacional=0.5,
            grupos_economicos=(0, 0, 0, 1, 1, 1),  # 2 multinacionais
            q_min_cooperacao_interna=0.05,
            fracao_violadoras=0.6,
            taxa_observacao=0.5,
        )
    )
    df = m.executar()
    # Deve haver pelo menos um boost ou abertura consolidada na cauda da rodada.
    assert (
        df["n_aberturas_consolidadas_grupo_acum"].max() + df["n_boosts_coordenacao_intl_acum"].max()
    ) >= 1
