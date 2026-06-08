"""Testes dos agentes."""

from waas_antitrust.agents import TrabalhadorAgent
from waas_antitrust.model import WaaSModel, WaaSParametros


def test_arquetipos_validos():
    """Seis arquétipos canônicos: Hokamp-Pickhardt 2010 (quatro) +
    fairminded (Torsell 2026, R16) + oportunista (R24, x10 v2 — Cient.
    Político + Sociólogo). FM e oportunista têm default 0% para preservar
    a calibração histórica; cenários em `waas_antitrust.cenarios` ativam."""
    assert TrabalhadorAgent.ARQUETIPOS == (
        "ético",
        "imitativo",
        "racional",
        "aleatório",
        "fairminded",
        "oportunista",
    )


def test_trabalhador_nao_observa_nao_sinaliza():
    """Trabalhador que não observou violação nunca sinaliza."""
    params = WaaSParametros(n_empresas=2, tam_medio_empresa=50, n_tiques=1, seed=1)
    modelo = WaaSModel(params)
    for ws in modelo.trabalhadores_por_empresa.values():
        for t in ws:
            t.observou = False
            assert (
                t.decidir_sinal(s_i=0.9, phi_vizinhos=1.0, W_esperado=1e6, r=0.0, F_falso=0.0) == 0
            )


def test_empresa_sancao_aumenta_com_severidade():
    """Sanção esperada cresce com severidade σ."""
    params = WaaSParametros(seed=42)
    modelo = WaaSModel(params)
    empresa = modelo.empresas[0]
    sancao_base = empresa.sancao_esperada()
    empresa.sigma = empresa.sigma + 0.5
    sancao_alta = empresa.sancao_esperada()
    assert sancao_alta > sancao_base


def test_autoridade_respeita_capacidade():
    """Autoridade descarta casos acima da capacidade κ."""
    params = WaaSParametros(n_empresas=5, tam_medio_empresa=20, n_tiques=1, seed=1)
    modelo = WaaSModel(params)
    autoridade = modelo.autoridade
    # injeta mais casos que a capacidade
    for _ in range(autoridade.capacidade * 3):
        autoridade.receber_caso(
            modelo.empresas[0], qualidade_prova=0.5, identidades_protegidas=True
        )
    resultados = autoridade.processar_casos()
    assert len(resultados) == autoridade.capacidade


def test_autoridade_prova_perfeita_classifica_corretamente():
    """Com qualidade de prova = 1, a classificação é sempre correta (ρ + (1−ρ)·1 = 1)."""
    params = WaaSParametros(
        n_empresas=5, tam_medio_empresa=20, n_tiques=1, seed=1, rho=0.5, taxa_capacidade=1.0
    )
    modelo = WaaSModel(params)
    autoridade = modelo.autoridade
    for empresa in modelo.empresas:
        autoridade.receber_caso(empresa, qualidade_prova=1.0, identidades_protegidas=True)
    for resultado in autoridade.processar_casos():
        assert resultado["classificada_violadora"] == resultado["eh_violadora_real"]
