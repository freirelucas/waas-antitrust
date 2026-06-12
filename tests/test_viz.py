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


def test_painel_micro_gera_figura():
    """`painel_micro.gerar_figura(modelo, fid)` retorna painel 2×2 da firma."""
    from waas_antitrust.model import WaaSModel, WaaSParametros
    from waas_antitrust.viz import painel_micro

    aplicar_estilo()
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=50,
            n_tiques=3,
            seed=11,
            regime="B",
            modo_corrida=True,
        )
    )
    m.executar()
    fig, axes = painel_micro.gerar_figura(m, fid=0)
    assert fig is not None
    assert len(axes) == 4
    plt.close(fig)


def test_painel_micro_firma_invalida_levanta():
    """`gerar_figura` levanta ValueError se firma não existe."""
    import pytest

    from waas_antitrust.model import WaaSModel, WaaSParametros
    from waas_antitrust.viz import painel_micro

    m = WaaSModel(WaaSParametros(n_empresas=2, tam_medio_empresa=30, n_tiques=1, seed=7))
    m.executar()
    with pytest.raises(ValueError, match="firma 999"):
        painel_micro.gerar_figura(m, fid=999)


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


def test_proposicao_5_gera_figura():
    """`proposicao_5.gerar_figura` retorna (Figure, [Axes, Axes]) com painel
    1×2 multi-seed: capital social residual + dano relativo ao baseline.
    Implementada no item #7 do Tier MÉDIA do balanço 360°."""
    from waas_antitrust.viz import proposicao_5

    aplicar_estilo()
    # Configuração reduzida para teste rápido (~ 2s)
    fig, axes = proposicao_5.gerar_figura(n_tiques=10, seeds=(11, 23), alphas=(0.0, 0.5))
    assert fig is not None
    assert len(axes) == 2
    # Painel A é capital social, painel B é dano relativo
    assert "Capital social" in axes[0].get_ylabel()
    assert "Dano" in axes[1].get_ylabel() or "dano" in axes[1].get_ylabel().lower()
    plt.close(fig)


def test_alpha_erosao_limiar_gera_figura(tmp_path):
    """`alpha_erosao_limiar.gerar_figura` lê parquet e produz painel 1×2 da
    falsificação numérica da Proposição 5 candidata."""
    import pandas as pd

    from waas_antitrust.viz import alpha_erosao_limiar

    # Mini-parquet sintético: 2 alphas × 3 seeds × 2 regimes
    registros = []
    for seed in (1, 2, 3):
        registros.append(
            {
                "alpha_erosao": 0.0,
                "seed": seed,
                "regime": "A",
                "dano_acumulado": 100.0 + seed,
                "capital_social_residual": 1.0,
                "n_tcc_assinados": 0,
            }
        )
    for alpha in (0.0, 0.5):
        for seed in (1, 2, 3):
            registros.append(
                {
                    "alpha_erosao": alpha,
                    "seed": seed,
                    "regime": "B",
                    "dano_acumulado": 30.0 + seed + alpha * 5,
                    "capital_social_residual": max(0.1, 1.0 - alpha),
                    "n_tcc_assinados": 1,
                }
            )
    df = pd.DataFrame(registros)
    parquet = tmp_path / "alpha_erosao_grade_mini.parquet"
    df.to_parquet(parquet, index=False)

    aplicar_estilo()
    fig, axes = alpha_erosao_limiar.gerar_figura(parquet_path=parquet)
    assert fig is not None
    assert len(axes) == 2
    plt.close(fig)


def test_multiplicidade_unicidade_gera_figura():
    """`multiplicidade_unicidade.gerar_figura` retorna (Figure, [Axes, Axes])
    com painel 1×2 do contraste Morris-Shin: múltiplos equilíbrios sob
    conhecimento comum × equilíbrio único sob informação privada.
    Atende R02b do balanço 360° (item #5)."""
    from waas_antitrust.viz import multiplicidade_unicidade

    aplicar_estilo()
    fig, axes = multiplicidade_unicidade.gerar_figura(
        b=2.0, c=1.0, k=0.2, taus=(0.0, 0.1, 0.3, 0.5)
    )
    assert fig is not None
    assert len(axes) == 2
    plt.close(fig)
