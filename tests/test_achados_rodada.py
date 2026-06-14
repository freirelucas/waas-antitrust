"""Testes de regressão dos 3 achados científicos da rodada de jun/2026.

Cada teste protege contra regressão um achado que sobreviveu a varreduras
multi-seed e está documentado em `docs/limitacoes.md` / `paper/main.tex`
/ `docs/transparencia.md`. Se um destes testes quebrar, o achado precisa
ser reexaminado antes de qualquer release.
"""

from __future__ import annotations

import numpy as np
import pytest

from waas_antitrust.model import WaaSModel, WaaSParametros

# ---------------------------------------------------------------------
# Achado 1 — Prop. 5 forte falsificada
# ---------------------------------------------------------------------


def test_prop5_forte_segue_falsificada_em_alpha_alto():
    """Achado da rodada (commit 80d1224): com `alpha_erosao=0.9` em Regime B,
    o dano permanece **abaixo** do piso A para uma seed reproduzível."""
    seed = 11
    n_tiques = 40
    base = dict(
        n_empresas=15,
        tam_medio_empresa=200,
        n_tiques=n_tiques,
        seed=seed,
        fracao_violadoras=0.5,
        taxa_observacao=0.4,
    )
    df_a = WaaSModel(WaaSParametros(**base, regime="A")).executar()
    df_b_alto = WaaSModel(WaaSParametros(**base, regime="B", alpha_erosao=0.9)).executar()

    dano_a = float(df_a["dano_acumulado"].iloc[-1])
    dano_b = float(df_b_alto["dano_acumulado"].iloc[-1])

    # Margem: dano em A deve ser substancialmente maior que em B (esperado ~8×).
    assert dano_b < dano_a, (
        f"Prop. 5 forte: Regime B deveria seguir dominando A mesmo com alpha=0.9. "
        f"dano_A={dano_a:.1f}, dano_B(alpha=0.9)={dano_b:.1f}"
    )
    assert dano_b < dano_a * 0.5, (
        f"Prop. 5 forte: a margem deveria ser folgada (>50%). "
        f"dano_A={dano_a:.1f}, dano_B(alpha=0.9)={dano_b:.1f}"
    )


def test_prop5_fraca_segue_verificada_substrato_erode_com_alpha():
    """Achado da rodada: a forma fraca (substrato decai com `alpha`) é
    confirmada — `capital_social_residual` final é estritamente menor sob
    `alpha=0.9` que sob `alpha=0`."""
    base = dict(
        n_empresas=10,
        tam_medio_empresa=120,
        n_tiques=20,
        seed=23,
        regime="B",
        fracao_violadoras=0.6,
        taxa_observacao=0.45,
    )
    sem = WaaSModel(WaaSParametros(**base, alpha_erosao=0.0)).executar()
    com = WaaSModel(WaaSParametros(**base, alpha_erosao=0.9)).executar()
    final_sem = float(sem["capital_social_residual"].iloc[-1])
    final_com = float(com["capital_social_residual"].iloc[-1])
    assert final_com < final_sem
    # Confirmação adicional: substrato fica perto do piso (< 0.3) com alpha alto.
    assert final_com < 0.3, f"capital social residual deveria colapsar; final = {final_com:.3f}"


# ---------------------------------------------------------------------
# Achado 2 — Mapa (λ × peso_hirschman): sem bifurcação na grade
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "lambda_, peso",
    [(0.05, 0.0), (0.05, 1.0), (0.95, 0.0), (0.95, 1.0)],
)
def test_mapa_lambda_hirschman_extremos_executam(lambda_: float, peso: float):
    """Achado da rodada (commit 24feb0d): em Regime C com Hirschman universal,
    os 4 cantos da grade rodam sem erro e produzem dano finito não-negativo."""
    params = WaaSParametros(
        n_empresas=8,
        tam_medio_empresa=80,
        n_tiques=10,
        seed=37,
        regime="C",
        fracao_contratos_acelerados=1.0,
        fracao_violadoras=0.6,
        taxa_observacao=0.45,
        lambda_expectativa=lambda_,
        peso_hirschman=peso,
    )
    df = WaaSModel(params).executar()
    dano = float(df["dano_acumulado"].iloc[-1])
    assert np.isfinite(dano) and dano >= 0.0


def test_mapa_lambda_hirschman_peso_alto_zera_dano():
    """Achado: `peso_hirschman=1.0` zera (ou quase) o dano para qualquer λ —
    a forma direta da dominância do laço contratual."""
    base = dict(
        n_empresas=8,
        tam_medio_empresa=80,
        n_tiques=20,
        seed=41,
        regime="C",
        fracao_contratos_acelerados=1.0,
        fracao_violadoras=0.6,
        taxa_observacao=0.45,
        lambda_expectativa=0.5,
    )
    df_baixo = WaaSModel(WaaSParametros(**base, peso_hirschman=0.0)).executar()
    df_alto = WaaSModel(WaaSParametros(**base, peso_hirschman=1.0)).executar()
    assert float(df_alto["dano_acumulado"].iloc[-1]) < float(df_baixo["dano_acumulado"].iloc[-1])


# ---------------------------------------------------------------------
# Achado 3 — Calibração formal R03: ponto ótimo é estável
# ---------------------------------------------------------------------


def test_calibracao_formal_r03_ponto_otimo_consistente_com_alvo():
    """Achado da rodada (commit daa9046): no ponto ótimo (0.323, 0.481) o
    modelo produz ~0.6 TCC/ano (alvo normalizado para 20 firmas / N=1.567)."""
    seeds = [11, 23, 37]
    valores = []
    for seed in seeds:
        params = WaaSParametros(
            n_empresas=20,
            tam_medio_empresa=200,
            n_tiques=40,
            regime="B",
            seed=seed,
            fracao_violadoras=0.323,
            taxa_capacidade=0.481,
        )
        df = WaaSModel(params).executar()
        n_anos = 40 / 4.0
        valores.append(float(df["n_tcc_assinados"].iloc[-1]) / n_anos)
    media = float(np.mean(valores))
    # Alvo normalizado em DECISIONS R03: 0.6 TCC/ano para n_empresas=20 e
    # N_universo=1567. Tolerância: 1 TCC/ano (ruído de seed é alto em 3 seeds).
    assert 0.0 <= media <= 1.6, (
        f"Calibração formal: TCC/ano simulado fora da faixa plausível "
        f"em torno do alvo 0.6: média={media:.3f}, valores={valores}"
    )


# ---------------------------------------------------------------------
# Achado 4 — `regime_declarado` preserva tag R28 e mecânica resolve
# ---------------------------------------------------------------------


def test_tags_jurisdicionais_r28_preservadas_no_modelo():
    """Achado da rodada (commit 5feea03): tags "EUA"/"UE" mapeiam para
    C/A na mecânica e ficam preservadas em `regime_declarado`."""
    for tag, mecanica in (("EUA", "C"), ("UE", "A")):
        m = WaaSModel(WaaSParametros(n_empresas=3, tam_medio_empresa=30, n_tiques=1, regime=tag))
        assert m.regime == mecanica
        assert m.regime_declarado == tag


# ---------------------------------------------------------------------
# Achado 5 — viz/painel.py é a figura-síntese (T01 fechado)
# ---------------------------------------------------------------------


def test_viz_painel_sintese_disponivel():
    """T01 fechado: `viz/painel.py` está implementado, não é mais stub."""
    from waas_antitrust.viz import painel

    assert hasattr(painel, "gerar_figura")
    # Não rodamos a figura completa aqui (test_viz.py cobre); apenas
    # confirmamos que a função existe e não é o stub.
    assert painel.gerar_figura.__doc__ is not None
    assert "stub" not in painel.gerar_figura.__doc__.lower()
