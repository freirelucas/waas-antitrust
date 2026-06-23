"""Testes da janela de adesão pós-abertura com desconto progressivo (R29).

A regra modelada: quando uma firma atinge massa crítica intra-firma e seu
escrow é aberto, abre-se uma janela de `janela_adesao_pos_abertura` tiques
durante a qual trabalhadores da MESMA firma que não cooperaram ainda podem
aderir à "classe dos lenientes" e receber desconto progressivo por ordem de
chegada (`descontos_faixas_adesao`).

Espelha a fila clássica de leniência (Spagnolo 2004; Lei 12.529/2011 Art. 86)
operada DENTRO da firma já aberta — incentivo de cascata pós-coordenação.

Compat estrita: `janela_adesao_pos_abertura = 0` desliga o mecanismo.
"""

from __future__ import annotations

from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Backward compat estrita
# ----------------------------------------------------------------------


def test_janela_adesao_pos_abertura_default_zero_compat():
    """Default 0 preserva caminho histórico (mecanismo desligado)."""
    p = WaaSParametros(n_empresas=3, tam_medio_empresa=30, n_tiques=2, seed=11)
    assert p.janela_adesao_pos_abertura == 0
    m = WaaSModel(p)
    assert m.janela_adesao_pos_abertura == 0


def test_reporter_aderentes_zero_sob_default():
    """Sob default, reporter de aderentes pós-abertura permanece em 0."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=5,
            tam_medio_empresa=40,
            n_tiques=15,
            seed=11,
            regime="B",
            usar_escrow_explicito=True,
        )
    )
    df = m.executar()
    assert "n_aderentes_pos_abertura_acum" in df.columns
    assert "n_blocos_em_janela_adesao_acum" in df.columns
    assert df["n_aderentes_pos_abertura_acum"].max() == 0
    assert df["n_blocos_em_janela_adesao_acum"].max() == 0


# ----------------------------------------------------------------------
# Mecanismo desligado sob escrow implícito
# ----------------------------------------------------------------------


def test_janela_no_op_sob_escrow_implicito():
    """Mesmo com janela > 0, se escrow é implícito o mecanismo é no-op."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=5,
            tam_medio_empresa=40,
            n_tiques=15,
            seed=11,
            regime="B",
            usar_escrow_explicito=False,
            janela_adesao_pos_abertura=10,
        )
    )
    df = m.executar()
    assert df["n_aderentes_pos_abertura_acum"].max() == 0
    assert df["n_blocos_em_janela_adesao_acum"].max() == 0


# ----------------------------------------------------------------------
# API direta do AutoridadeAgent
# ----------------------------------------------------------------------


def test_registrar_bloco_em_adesao_inicializa_registro():
    """Após `registrar_bloco_em_adesao`, o registro contém tique e listas
    vazias/preenchidas conforme a abertura anterior."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=4,
            tam_medio_empresa=30,
            n_tiques=2,
            seed=13,
            regime="B",
            usar_escrow_explicito=True,
            janela_adesao_pos_abertura=10,
        )
    )
    autoridade = m.autoridade
    # Simula uma abertura: depósito + abre + registra.
    autoridade.depositar_condicional(id_empresa=0, id_trabalhador=42, qualidade_prova=0.5, tique=1)
    autoridade.depositar_condicional(id_empresa=0, id_trabalhador=43, qualidade_prova=0.6, tique=1)
    autoridade.abrir_escrow_se_massa_critica(id_empresa=0, q_min=0.01, n_trabalhadores_firma=10)
    autoridade.registrar_bloco_em_adesao(id_empresa=0, tique_abertura=1)
    reg = autoridade.blocos_em_janela_adesao[0]
    assert reg["tique_abertura"] == 1
    assert len(reg["depositantes_originais"]) == 2
    assert reg["aderentes_pos_abertura"] == []
    assert autoridade.n_blocos_em_janela_adesao_acum == 1


def test_processar_adesao_no_op_sob_janela_zero():
    """`janela <= 0` ⇒ no-op sem inspeção de candidatos."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=20,
            n_tiques=2,
            seed=17,
            regime="B",
            usar_escrow_explicito=True,
            janela_adesao_pos_abertura=10,
        )
    )
    autoridade = m.autoridade
    n = autoridade.processar_adesao_pos_abertura(
        tique_atual=5,
        janela=0,
        descontos=(1.0, 0.7, 0.5),
        trabalhadores_por_empresa=m.trabalhadores_por_empresa,
        W_max=10.0,
        custo_represalia=1.0,
    )
    assert n == 0
    assert autoridade.n_aderentes_pos_abertura_acum == 0


def test_processar_adesao_aceita_quando_desconto_supera_represalia():
    """Aderem candidatos cujo fator * W_max > custo_represalia."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=20,
            n_tiques=2,
            seed=19,
            regime="B",
            usar_escrow_explicito=True,
            janela_adesao_pos_abertura=10,
        )
    )
    autoridade = m.autoridade
    # Faz o trabalhador real 0 da firma 0 ser o depositante original (id=999)
    # para que o teste reflita corretamente o filtro de "já dentro".
    t0 = m.trabalhadores_por_empresa[0][0]
    t0.unique_id = 999
    autoridade.depositar_condicional(id_empresa=0, id_trabalhador=999, qualidade_prova=0.5, tique=0)
    autoridade.abrir_escrow_se_massa_critica(id_empresa=0, q_min=0.001, n_trabalhadores_firma=100)
    autoridade.registrar_bloco_em_adesao(id_empresa=0, tique_abertura=0)
    # W_max alto vs represália baixa: todos os trabalhadores da firma 0 devem
    # aderir (até o limite das faixas — última faixa 0.1 ainda > represália).
    n_trab_firma0 = len(m.trabalhadores_por_empresa[0])
    n = autoridade.processar_adesao_pos_abertura(
        tique_atual=1,
        janela=10,
        descontos=(1.0, 0.7, 0.5, 0.3, 0.1),
        trabalhadores_por_empresa=m.trabalhadores_por_empresa,
        W_max=100.0,
        custo_represalia=0.5,
    )
    # 1 depositante original (o real); restantes elegíveis.
    assert n == n_trab_firma0 - 1
    reg = autoridade.blocos_em_janela_adesao[0]
    # Faixas atribuídas: primeiro novo entra na posição 0 → fator 1.0.
    assert reg["aderentes_pos_abertura"][0]["fator_desconto"] == 1.0
    # Quem entra além de N descontos cai na última faixa.
    if n >= 5:
        assert reg["aderentes_pos_abertura"][4]["fator_desconto"] == 0.1
        assert reg["aderentes_pos_abertura"][-1]["fator_desconto"] == 0.1


def test_processar_adesao_rejeita_quando_represalia_supera_desconto():
    """Ninguém adere quando todas as faixas têm fator*W_max <= represália."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=2,
            tam_medio_empresa=10,
            n_tiques=2,
            seed=23,
            regime="B",
            usar_escrow_explicito=True,
            janela_adesao_pos_abertura=10,
        )
    )
    autoridade = m.autoridade
    autoridade.depositar_condicional(id_empresa=0, id_trabalhador=1, qualidade_prova=0.5, tique=0)
    autoridade.abrir_escrow_se_massa_critica(id_empresa=0, q_min=0.001, n_trabalhadores_firma=100)
    autoridade.registrar_bloco_em_adesao(id_empresa=0, tique_abertura=0)
    n = autoridade.processar_adesao_pos_abertura(
        tique_atual=1,
        janela=10,
        descontos=(1.0, 0.5),
        trabalhadores_por_empresa=m.trabalhadores_por_empresa,
        W_max=1.0,
        custo_represalia=10.0,
    )
    assert n == 0
    assert autoridade.n_aderentes_pos_abertura_acum == 0


def test_processar_adesao_expira_bloco_fora_da_janela():
    """Bloco com idade ≥ janela é removido sem processar adesões novas."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=3,
            tam_medio_empresa=20,
            n_tiques=2,
            seed=29,
            regime="B",
            usar_escrow_explicito=True,
            janela_adesao_pos_abertura=10,
        )
    )
    autoridade = m.autoridade
    autoridade.depositar_condicional(id_empresa=0, id_trabalhador=7, qualidade_prova=0.5, tique=0)
    autoridade.abrir_escrow_se_massa_critica(id_empresa=0, q_min=0.001, n_trabalhadores_firma=100)
    autoridade.registrar_bloco_em_adesao(id_empresa=0, tique_abertura=0)
    assert 0 in autoridade.blocos_em_janela_adesao
    # tique_atual=10, janela=10 → idade==janela → expira.
    n = autoridade.processar_adesao_pos_abertura(
        tique_atual=10,
        janela=10,
        descontos=(1.0,),
        trabalhadores_por_empresa=m.trabalhadores_por_empresa,
        W_max=100.0,
        custo_represalia=0.1,
    )
    assert n == 0
    assert 0 not in autoridade.blocos_em_janela_adesao


def test_processar_adesao_nao_duplica_depositante_original():
    """Quem já estava como depositante original não pode aderir de novo
    como faixa pós-abertura (já é faixa 0 — imunidade)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=2,
            tam_medio_empresa=10,
            n_tiques=2,
            seed=31,
            regime="B",
            usar_escrow_explicito=True,
            janela_adesao_pos_abertura=10,
        )
    )
    autoridade = m.autoridade
    # Força o trabalhador real 0 da firma 0 a ter unique_id=99999 (evita
    # colisão com unique_ids autogerados pelo Mesa).
    t0 = m.trabalhadores_por_empresa[0][0]
    t0.unique_id = 99999
    autoridade.depositar_condicional(
        id_empresa=0, id_trabalhador=99999, qualidade_prova=0.5, tique=0
    )
    autoridade.abrir_escrow_se_massa_critica(id_empresa=0, q_min=0.001, n_trabalhadores_firma=100)
    autoridade.registrar_bloco_em_adesao(id_empresa=0, tique_abertura=0)
    n = autoridade.processar_adesao_pos_abertura(
        tique_atual=1,
        janela=10,
        descontos=(1.0, 0.5),
        trabalhadores_por_empresa=m.trabalhadores_por_empresa,
        W_max=100.0,
        custo_represalia=0.1,
    )
    reg = autoridade.blocos_em_janela_adesao[0]
    ids_aderentes = {a["id_trabalhador"] for a in reg["aderentes_pos_abertura"]}
    assert 99999 not in ids_aderentes
    # Demais trabalhadores da firma 0 aderiram.
    assert n == len(m.trabalhadores_por_empresa[0]) - 1


# ----------------------------------------------------------------------
# End-to-end: cenário ativo produz aderentes acumulados
# ----------------------------------------------------------------------


def test_end_to_end_produz_aderentes_acumulados():
    """Sob escrow explícito + janela > 0, espera-se ≥1 aderente em alguma
    seed/configuração com massa crítica baixa e janela larga."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=8,
            tam_medio_empresa=60,
            n_tiques=25,
            seed=2026,
            regime="B",
            usar_escrow_explicito=True,
            q_min_cooperacao_interna=0.05,
            janela_adesao_pos_abertura=15,
            descontos_faixas_adesao=(1.0, 0.8, 0.6, 0.4, 0.2),
            fracao_violadoras=0.5,
            taxa_observacao=0.5,
        )
    )
    df = m.executar()
    # A janela só faz sentido se houve pelo menos UM bloco aberto.
    assert df["n_blocos_em_janela_adesao_acum"].max() >= 1
    # Em janela larga + q_min baixo + W relevante, esperamos pelo menos
    # uma adesão na cauda da simulação (cascata pós-coordenação).
    assert df["n_aderentes_pos_abertura_acum"].max() >= 1


# ----------------------------------------------------------------------
# Calibração contra gradiente Saito 2021
# ----------------------------------------------------------------------


def test_cenario_saito_calibrado_usa_gradiente_normalizado():
    """O cenário `cascata_adesao_saito_calibrada` usa as faixas derivadas
    de Saito 2021 §3.7.7 — D_Saito(k+1)/D_Saito(1) para k=1,2,3 + piso 15 %."""
    from waas_antitrust.cenarios import aplicar_cenario

    base = WaaSParametros(n_empresas=4, tam_medio_empresa=20, n_tiques=2, seed=11)
    p_saito = aplicar_cenario(base, "cascata_adesao_saito_calibrada")
    assert p_saito.descontos_faixas_adesao == (1.0, 0.795, 0.466, 0.345, 0.345)
    # E nada mais muda na topologia: comparabilidade direta com
    # `cascata_adesao_progressiva` que usa faixas arbitrárias.
    p_arb = aplicar_cenario(base, "cascata_adesao_progressiva")
    assert p_saito.janela_adesao_pos_abertura == p_arb.janela_adesao_pos_abertura
    assert p_saito.janela_escrow_tiques == p_arb.janela_escrow_tiques
    assert p_saito.q_min_cooperacao_interna == p_arb.q_min_cooperacao_interna
    assert p_saito.usar_escrow_explicito is True


def test_faixas_saito_decrescentes_monotonicamente():
    """As faixas calibradas Saito são estritamente decrescentes até o piso,
    consistentes com o gradiente do Art. 86 (Lei 12.529/2011)."""
    from waas_antitrust.cenarios import aplicar_cenario

    p = aplicar_cenario(
        WaaSParametros(n_empresas=2, tam_medio_empresa=10, n_tiques=2, seed=1),
        "cascata_adesao_saito_calibrada",
    )
    f = p.descontos_faixas_adesao
    # Faixa 0 (imunidade) é máxima
    assert f[0] == 1.0
    # Faixas 1..3 estritamente decrescentes
    assert f[1] > f[2] > f[3]
    # Faixa 4 = piso, igual à 3 (15 % normalizado pelo topo Saito)
    assert f[4] == f[3] == 0.345
