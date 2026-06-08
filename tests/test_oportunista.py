"""Testes do arquétipo `denunciante_oportunista` (R24, x10 v2).

Atende à convergência tripla Cient. Político v2 + Sociólogo v2 + Mat B v2:
o WaaS pode ser usado adversarialmente. Vetores de uso:
- insider acionista vendendo a descoberto antes de plantar denúncia;
- concorrente financiando ex-empregado para denúncia oportunista;
- chantagem intra-firma como ameaça pré-rescisão para extrair severance;
- hedge fund ativista combinando short + WaaS payout.

Dyck-Morse-Zingales (2010) reportam ~17% de motivação financeira direta em
denúncias SEC. A modelagem aqui captura o limite superior 20%.
"""

from __future__ import annotations

from waas_antitrust.agents import TrabalhadorAgent
from waas_antitrust.cenarios import DISTRIBUICAO_COM_OPORTUNISTAS
from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Catálogo de arquétipos: oportunista presente
# ----------------------------------------------------------------------


def test_oportunista_esta_no_catalogo_de_arquetipos():
    """ARQUETIPOS agora inclui oportunista (R24, x10 v2)."""
    assert "oportunista" in TrabalhadorAgent.ARQUETIPOS
    assert len(TrabalhadorAgent.ARQUETIPOS) == 6


def test_distribuicao_default_nao_sorteia_oportunista():
    """Default `distribuicao_arquetipos=None` ⇒ oportunista em 0% (compat)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=80,
            n_tiques=1,
            seed=11,
            regime="B",
            distribuicao_arquetipos=None,
        )
    )
    arqs = {t.arquetipo for ws in m.trabalhadores_por_empresa.values() for t in ws}
    assert "oportunista" not in arqs


def test_distribuicao_com_oportunistas_sorteia_oportunistas():
    """Quando `distribuicao_arquetipos=DISTRIBUICAO_COM_OPORTUNISTAS`, eles aparecem."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=200,
            n_tiques=1,
            seed=17,
            regime="B",
            distribuicao_arquetipos=DISTRIBUICAO_COM_OPORTUNISTAS,
        )
    )
    arqs = [t.arquetipo for ws in m.trabalhadores_por_empresa.values() for t in ws]
    assert "oportunista" in arqs
    fracao_op = arqs.count("oportunista") / len(arqs)
    # ~20% da população deve ser oportunista (margem ampla para variância).
    assert 0.10 < fracao_op < 0.30


# ----------------------------------------------------------------------
# Comportamento: utilidade puramente extrativa
# ----------------------------------------------------------------------


def test_oportunista_sinaliza_quando_recompensa_compensa_calunia():
    """Oportunista sinaliza se ganho extrativo > 0, sem precisar observar."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=50,
            n_tiques=1,
            seed=23,
            regime="B",
            W_mult=5.0,  # recompensa generosa compensa sanção de calúnia
            distribuicao_arquetipos=DISTRIBUICAO_COM_OPORTUNISTAS,
        )
    )
    op = next(
        t for ws in m.trabalhadores_por_empresa.values() for t in ws if t.arquetipo == "oportunista"
    )
    # W_esperado alto, prob_falso=0.7 (não observou) ⇒ ganho extrativo positivo
    # se W_efetivo > 0.7 · 0.5 · w_a = 0.35 · w_a
    op.observou = False
    decisao = op.decidir_sinal(
        s_i=None,  # oportunista ignora observação
        phi_vizinhos=0.0,
        W_esperado=5.0 * op.w_a,
        r=0.15,
        F_falso=0.5,
    )
    assert decisao == 1, "oportunista com W alto deve sinalizar mesmo sem observar"


def test_oportunista_nao_sinaliza_quando_calunia_supera_recompensa():
    """Oportunista racional desiste quando sanção esperada de calúnia > W."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=50,
            n_tiques=1,
            seed=29,
            regime="B",
            W_mult=0.1,  # recompensa baixíssima
            distribuicao_arquetipos=DISTRIBUICAO_COM_OPORTUNISTAS,
        )
    )
    op = next(
        t for ws in m.trabalhadores_por_empresa.values() for t in ws if t.arquetipo == "oportunista"
    )
    op.observou = False
    decisao = op.decidir_sinal(
        s_i=None,
        phi_vizinhos=0.0,
        W_esperado=0.05 * op.w_a,  # 0.05·w_a < 0.7 · 0.5 · w_a = 0.35·w_a
        r=0.15,
        F_falso=0.5,
    )
    assert decisao == 0, "oportunista com W baixo NÃO deve sinalizar"


def test_oportunista_observou_reduz_prob_falso_subjetiva():
    """Quando `observou=True`, a probabilidade subjetiva de falso reporte cai
    (0.7 → 0.3); oportunista sinaliza com W menor que quando não observou."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=50,
            n_tiques=1,
            seed=31,
            regime="B",
            W_mult=1.0,
            distribuicao_arquetipos=DISTRIBUICAO_COM_OPORTUNISTAS,
        )
    )
    op = next(
        t for ws in m.trabalhadores_por_empresa.values() for t in ws if t.arquetipo == "oportunista"
    )
    # Com W = 0.2·w_a: sanção esperada se não observou = 0.7·0.5·w_a = 0.35·w_a
    #                  sanção esperada se observou = 0.3·0.5·w_a = 0.15·w_a
    # ⇒ observou=True deve sinalizar; observou=False não.
    W_marginal = 0.2 * op.w_a
    op.observou = False
    nao_obs = op.decidir_sinal(
        s_i=None, phi_vizinhos=0.0, W_esperado=W_marginal, r=0.15, F_falso=0.5
    )
    op.observou = True
    obs = op.decidir_sinal(s_i=None, phi_vizinhos=0.0, W_esperado=W_marginal, r=0.15, F_falso=0.5)
    assert nao_obs == 0 and obs == 1, f"esperado (0, 1); obtido ({nao_obs}, {obs})"


# ----------------------------------------------------------------------
# Robustez do mecanismo sob uso adversarial
# ----------------------------------------------------------------------


def test_oportunistas_executam_sem_erro_em_modelo_completo():
    """Modelo com 20% de oportunistas roda end-to-end sem exceção."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=120,
            n_tiques=10,
            seed=41,
            regime="B",
            distribuicao_arquetipos=DISTRIBUICAO_COM_OPORTUNISTAS,
            W_mult=2.0,
        )
    )
    df = m.executar()
    assert len(df) == 10


def test_distribuicao_com_oportunistas_soma_um():
    """Sanidade: preset soma 1.0."""
    soma = sum(DISTRIBUICAO_COM_OPORTUNISTAS.values())
    assert abs(soma - 1.0) < 1e-9, f"DISTRIBUICAO_COM_OPORTUNISTAS soma {soma}"


def test_oportunistas_independente_de_phi_vizinhos():
    """Diferente de imitativo/fairminded: oportunista NÃO depende de phi_vizinhos.
    Captura comportamento extrativo isolado (free-riding inverso)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=50,
            n_tiques=1,
            seed=43,
            regime="B",
            W_mult=2.0,
            distribuicao_arquetipos=DISTRIBUICAO_COM_OPORTUNISTAS,
        )
    )
    op = next(
        t for ws in m.trabalhadores_por_empresa.values() for t in ws if t.arquetipo == "oportunista"
    )
    op.observou = True
    # Decisão deve ser igual com phi=0 ou phi=0.9.
    dec_baixo = op.decidir_sinal(
        s_i=None, phi_vizinhos=0.0, W_esperado=2.0 * op.w_a, r=0.15, F_falso=0.5
    )
    dec_alto = op.decidir_sinal(
        s_i=None, phi_vizinhos=0.9, W_esperado=2.0 * op.w_a, r=0.15, F_falso=0.5
    )
    assert (
        dec_baixo == dec_alto
    ), "oportunista deve ignorar phi_vizinhos; pressão social não afeta extração"
