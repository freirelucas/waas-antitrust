"""Testes do canal de depósito condicional explícito (R27, balanço 360° item #1).

Atende ao maior débito semântico do reframe v3: sob a versão corrigida,
o `AutoridadeAgent` deve ser explicitamente o portador do escrow de
denúncias condicionais (Ayres-Unkovic 2012; análogo Callisto). Sob
`usar_escrow_explicito=True`, o `WaaSModel.step()`:

- P2 deposita cada sinal em `autoridade.escrow_denuncias` (não notifica a
  firma imediatamente).
- P2.5b chama `abrir_escrow_se_massa_critica` que decide se a massa
  crítica intra-firma foi atingida; se sim, **todas as denúncias se abrem
  simultaneamente** e viram `casos_neste_tique` no CADE.
- P4 processa os casos normalmente.

Sob default `usar_escrow_explicito=False`, comportamento histórico
idêntico ao anterior (escrow implícito em P2).
"""

from __future__ import annotations

from waas_antitrust.agents import AutoridadeAgent
from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Backward compat estrita
# ----------------------------------------------------------------------


def test_default_usar_escrow_explicito_e_false():
    """Backward compat: default preserva comportamento histórico."""
    m = WaaSModel(WaaSParametros(n_empresas=3, tam_medio_empresa=30, n_tiques=2, seed=7))
    assert m.usar_escrow_explicito is False


def test_reporter_n_denuncias_em_escrow_zero_sob_default():
    """Sob `usar_escrow_explicito=False`, escrow nunca recebe depósitos."""
    m = WaaSModel(
        WaaSParametros(n_empresas=5, tam_medio_empresa=50, n_tiques=3, seed=11, regime="B")
    )
    df = m.executar()
    assert df["n_denuncias_em_escrow"].max() == 0
    assert df["n_aberturas_simultaneas_acum"].max() == 0


def test_decisoes_de_trabalhadores_e_firmas_identicas_em_P0_P1_P2():
    """**Escopo do refator semântico R27**: o escrow muda APENAS o caminho
    pelo qual sinais viram casos no CADE (em P2/P2.5/P4). NÃO muda a
    decisão dos trabalhadores em P1 nem o gatilho de massa crítica em P2.

    Verificação: `n_sinais` (decidido em P1) é idêntico em ambos os modos
    no PRIMEIRO tique antes que a divergência semântica se propague.
    """
    base_args = dict(
        n_empresas=8,
        tam_medio_empresa=60,
        n_tiques=1,  # 1 tique: testa só P0/P1/P2 antes que a divergência
        seed=23,  # de P4 (escrow vs receber_caso) propague para P0 do
        regime="B",  # próximo tique via p_perc
        fracao_violadoras=0.6,
    )
    sem = WaaSModel(WaaSParametros(**base_args, usar_escrow_explicito=False)).executar()
    com = WaaSModel(WaaSParametros(**base_args, usar_escrow_explicito=True)).executar()
    # n_sinais é decidido em P1, antes da divergência em P2 — deve ser idêntico.
    assert sem["n_sinais"].iloc[0] == com["n_sinais"].iloc[0]
    # n_violadoras_ativas é decidido em P0 — também idêntico no t=0.
    assert sem["n_violadoras_ativas"].iloc[0] == com["n_violadoras_ativas"].iloc[0]


# ----------------------------------------------------------------------
# API do canal de depósito condicional
# ----------------------------------------------------------------------


def test_autoridade_inicia_com_escrow_vazio():
    """`AutoridadeAgent` ganha atributos `escrow_denuncias` e contadores."""
    m = WaaSModel(WaaSParametros(n_empresas=2, tam_medio_empresa=20, n_tiques=1, seed=3))
    assert isinstance(m.autoridade.escrow_denuncias, dict)
    assert len(m.autoridade.escrow_denuncias) == 0
    assert m.autoridade.n_denuncias_em_escrow == 0
    assert m.autoridade.n_aberturas_simultaneas_acum == 0


def test_depositar_condicional_adiciona_ao_escrow():
    """`depositar_condicional` armazena denúncia e incrementa contador."""
    m = WaaSModel(WaaSParametros(n_empresas=2, tam_medio_empresa=20, n_tiques=1, seed=3))
    m.autoridade.depositar_condicional(
        id_empresa=0, id_trabalhador=42, qualidade_prova=0.7, tique=0
    )
    assert 0 in m.autoridade.escrow_denuncias
    assert len(m.autoridade.escrow_denuncias[0]) == 1
    assert m.autoridade.n_denuncias_em_escrow == 1
    deposito = m.autoridade.escrow_denuncias[0][0]
    assert deposito["id_trabalhador"] == 42
    assert deposito["qualidade_prova"] == 0.7


def test_abrir_escrow_nao_atinge_massa_critica_devolve_false():
    """Com 1 depósito em firma de 100 trabalhadores e q_min=0.10,
    1/100 = 0.01 < 0.10 ⇒ escrow não abre."""
    m = WaaSModel(WaaSParametros(n_empresas=2, tam_medio_empresa=100, n_tiques=1, seed=3))
    m.autoridade.depositar_condicional(id_empresa=0, id_trabalhador=1, qualidade_prova=0.5, tique=0)
    abriu = m.autoridade.abrir_escrow_se_massa_critica(
        id_empresa=0, q_min=0.10, n_trabalhadores_firma=100
    )
    assert abriu is False
    assert m.autoridade.n_aberturas_simultaneas_acum == 0
    # Depósito permanece no escrow.
    assert len(m.autoridade.escrow_denuncias[0]) == 1


def test_abrir_escrow_atinge_massa_critica_devolve_true_e_esvazia():
    """Com 12 depósitos em firma de 100 e q_min=0.10, 12/100 = 0.12 ≥ 0.10
    ⇒ escrow abre simultaneamente: os 12 depósitos colapsam em UM caso
    (massa crítica é prova qualificada DA FIRMA, não N casos independentes).
    O caso aberto registra n_cooperadores=12 para auditoria."""
    m = WaaSModel(WaaSParametros(n_empresas=2, tam_medio_empresa=100, n_tiques=1, seed=3))
    for i in range(12):
        m.autoridade.depositar_condicional(
            id_empresa=0, id_trabalhador=i, qualidade_prova=0.5, tique=0
        )
    n_casos_antes = len(m.autoridade.casos_neste_tique)
    abriu = m.autoridade.abrir_escrow_se_massa_critica(
        id_empresa=0, q_min=0.10, n_trabalhadores_firma=100
    )
    assert abriu is True
    assert m.autoridade.n_aberturas_simultaneas_acum == 1
    assert m.autoridade.n_denuncias_em_escrow == 0  # esvaziado
    assert len(m.autoridade.escrow_denuncias[0]) == 0
    # Um caso colapsado para a firma — não 12.
    assert len(m.autoridade.casos_neste_tique) == n_casos_antes + 1
    caso = m.autoridade.casos_neste_tique[-1]
    assert caso["via_escrow"] is True
    assert caso["id_protegidas"] is True
    assert caso["n_cooperadores"] == 12


def test_abertura_simultanea_media_qualidade_de_prova():
    """Cada depósito carrega sua `qualidade_prova` própria; ao abrir, o
    caso colapsado tem qualidade = média ponderada (mais cooperadores ⇒
    mais confiança média)."""
    m = WaaSModel(WaaSParametros(n_empresas=2, tam_medio_empresa=10, n_tiques=1, seed=3))
    qualidades = [0.3, 0.6, 0.9]
    for i, q in enumerate(qualidades):
        m.autoridade.depositar_condicional(
            id_empresa=0, id_trabalhador=i, qualidade_prova=q, tique=0
        )
    m.autoridade.abrir_escrow_se_massa_critica(id_empresa=0, q_min=0.10, n_trabalhadores_firma=10)
    caso = m.autoridade.casos_neste_tique[-1]
    media_esperada = sum(qualidades) / len(qualidades)
    assert abs(caso["qualidade_prova"] - media_esperada) < 1e-9


# ----------------------------------------------------------------------
# Integração com WaaSModel
# ----------------------------------------------------------------------


def test_modelo_com_escrow_explicito_executa_sem_erro():
    """Modelo end-to-end com `usar_escrow_explicito=True` roda completo."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=60,
            n_tiques=10,
            seed=29,
            regime="B",
            fracao_violadoras=0.7,
            taxa_observacao=0.5,
            usar_escrow_explicito=True,
        )
    )
    df = m.executar()
    assert len(df) == 10
    # Reporters do escrow estão no DataFrame.
    assert "n_denuncias_em_escrow" in df.columns
    assert "n_aberturas_simultaneas_acum" in df.columns


def test_escrow_explicito_produz_aberturas_quando_massa_critica():
    """Cenário em que massa crítica é atingida: deve haver aberturas simultâneas."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=80,
            n_tiques=15,
            seed=41,
            regime="B",
            fracao_violadoras=0.9,
            taxa_observacao=0.7,
            q_min_cooperacao_interna=0.05,
            usar_escrow_explicito=True,
        )
    )
    df = m.executar()
    # Em ao menos um tique deve haver depósito em escrow ou abertura simultânea.
    teve_atividade = (
        df["n_denuncias_em_escrow"].max() > 0 or df["n_aberturas_simultaneas_acum"].max() > 0
    )
    assert teve_atividade, (
        f"esperado atividade no escrow; "
        f"max_em_escrow={df['n_denuncias_em_escrow'].max()}, "
        f"max_aberturas={df['n_aberturas_simultaneas_acum'].max()}"
    )


def test_escrow_idempotente_para_firma_vazia():
    """Tentar abrir escrow de uma firma sem depósitos é no-op."""
    m = WaaSModel(WaaSParametros(n_empresas=2, tam_medio_empresa=50, n_tiques=1, seed=3))
    abriu = m.autoridade.abrir_escrow_se_massa_critica(
        id_empresa=99, q_min=0.10, n_trabalhadores_firma=50
    )
    assert abriu is False
    assert m.autoridade.n_aberturas_simultaneas_acum == 0


def test_n_trabalhadores_zero_devolve_false():
    """Edge case: firma com 0 trabalhadores não dispara escrow."""
    m = WaaSModel(WaaSParametros(n_empresas=2, tam_medio_empresa=20, n_tiques=1, seed=3))
    m.autoridade.depositar_condicional(id_empresa=0, id_trabalhador=1, qualidade_prova=0.5, tique=0)
    abriu = m.autoridade.abrir_escrow_se_massa_critica(
        id_empresa=0, q_min=0.10, n_trabalhadores_firma=0
    )
    assert abriu is False


def test_isinstance_autoridade_agent():
    """Sanidade: `m.autoridade` é `AutoridadeAgent`."""
    m = WaaSModel(WaaSParametros(n_empresas=2, tam_medio_empresa=20, n_tiques=1, seed=3))
    assert isinstance(m.autoridade, AutoridadeAgent)
