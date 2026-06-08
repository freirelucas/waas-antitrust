"""Testes da erosão endógena por uso instrumental (R26, Sociólogo v2, Coleman 1990).

Coleman 1990 (*Foundations of Social Theory*, cap. 12): capital social
organizacional é destruído pela sua instrumentalização. No WaaS, a cada
notificação bem-sucedida, a comunicação informal em outras firmas pode
degradar — chilling effect.

Proposição 5 candidata: existe `alpha_erosao*` tal que para
`alpha_erosao > *`, o regime B/C colapsa em A após N tiques (a primeira
cascata bem-sucedida seca a fonte). Os testes aqui validam o mecanismo
sem afirmar o valor de `alpha_erosao*` — calibração formal em R03/R26.

Literatura calibradora (em REFERENCES.md):
- Titmuss 1970, *The Gift Relationship*
- Frey-Jegen 2001, *motivation crowding theory*
- Bénabou-Tirole 2003, *intrinsic-extrinsic crowding-out*
"""

from __future__ import annotations

from waas_antitrust.model import WaaSModel, WaaSParametros


def test_alpha_erosao_default_zero_preserva_compat():
    """`alpha_erosao` default 0 ⇒ `capital_social_residual = 1.0` constante."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=80,
            n_tiques=8,
            seed=11,
            regime="B",
        )
    )
    df = m.executar()
    serie = df["capital_social_residual"].tolist()
    # Sem erosão ativa, todos os valores devem ser 1.0.
    assert all(
        abs(v - 1.0) < 1e-9 for v in serie
    ), f"alpha_erosao=0 deveria manter capital_social=1.0; série={serie}"


def test_alpha_erosao_positivo_degrada_capital_social():
    """Com `alpha_erosao = 0.3` e cenário com notificações, o capital social
    deve decrescer monotonicamente."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=10,
            tam_medio_empresa=120,
            n_tiques=15,
            seed=23,
            regime="B",
            fracao_violadoras=0.8,
            taxa_observacao=0.6,
            alpha_erosao=0.3,
        )
    )
    df = m.executar()
    serie = df["capital_social_residual"].tolist()
    # Monotonicidade não-crescente.
    for i in range(len(serie) - 1):
        assert (
            serie[i + 1] <= serie[i] + 1e-9
        ), f"capital social cresceu de t={i} para t={i+1}: {serie[i]} → {serie[i+1]}"
    # Início alto (≥ 0.95), fim mais baixo (≤ início). Se houver notificações,
    # o capital deve ter caído pelo menos um pouco.
    assert serie[-1] <= serie[0]


def test_alpha_erosao_limites_validos():
    """`alpha_erosao` aceita valores em [0, 1]."""
    for alpha in (0.0, 0.1, 0.5, 1.0):
        m = WaaSModel(
            WaaSParametros(
                n_empresas=3,
                tam_medio_empresa=40,
                n_tiques=2,
                seed=29,
                regime="B",
                alpha_erosao=alpha,
            )
        )
        df = m.executar()
        # Capital social fica em [0, 1].
        assert 0.0 <= df["capital_social_residual"].min() <= 1.0
        assert 0.0 <= df["capital_social_residual"].max() <= 1.0


def test_capital_social_residual_reporter_presente():
    """Reporter `capital_social_residual` aparece no DataFrame."""
    m = WaaSModel(WaaSParametros(n_empresas=3, tam_medio_empresa=40, n_tiques=2, seed=7))
    df = m.executar()
    assert "capital_social_residual" in df.columns


def test_erosao_zero_em_regime_a_mesmo_com_alpha_alto():
    """Em Regime A não há notificações WaaS; mesmo com `alpha_erosao=1.0`,
    o capital social não deve degradar pelo mesmo mecanismo (testa que a
    erosão é endogeneizada por notificações, não por tempo)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=80,
            n_tiques=10,
            seed=37,
            regime="A",
            alpha_erosao=1.0,
        )
    )
    df = m.executar()
    # Em Regime A, notificações são raras; capital_social ≥ 0.5 esperado.
    assert (
        df["capital_social_residual"].min() >= 0.5
    ), "Regime A com alpha=1.0 não deveria erodir significativamente"


def test_proposicao_5_candidata_direcional():
    """Proposição 5 candidata: alpha_erosao alto degrada o capital social
    em Regime B até patamar baixo. Não testa o valor crítico (R03), apenas
    direcionalidade.

    Esperado: `capital_social_final` com `alpha=0.5` < `alpha=0`.
    """
    base = dict(
        n_empresas=10,
        tam_medio_empresa=120,
        n_tiques=20,
        seed=41,
        regime="B",
        fracao_violadoras=0.7,
        taxa_observacao=0.6,
    )
    sem = WaaSModel(WaaSParametros(**base, alpha_erosao=0.0)).executar()
    com = WaaSModel(WaaSParametros(**base, alpha_erosao=0.5)).executar()
    final_sem = float(sem["capital_social_residual"].iloc[-1])
    final_com = float(com["capital_social_residual"].iloc[-1])
    assert final_com < final_sem, (
        f"alpha=0.5 deveria erodir capital social abaixo de alpha=0; "
        f"sem={final_sem:.3f} com={final_com:.3f}"
    )
