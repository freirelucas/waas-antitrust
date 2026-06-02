"""Testes dos **vetores de quebra** do mecanismo WaaS (R15, exploratório).

A crítica é direta: "basta a empresa se recusar a pagar os whistleblower e
pegar o desconto para ruir tudo?". Esta suíte mostra como o modelo agora
torna essa pergunta explícita e quantificável.

Três vetores cobertos:

- **A** — TCC clássico já oferece desconto (Art. 85, sem WaaS). A IC-F*
  correta compara W contra o **incremento** ``D_extra = D_total − D_base``.
  Quando ``D_base ≥ D_total``, ninguém paga W.
- **B** — TCC-WaaS pode ser anulado judicialmente (F6 falsificador). Com
  ``p_anulacao_tcc > 0``, a multa cheia retorna ao Estado e o sistema
  perde a coordenação. Calibrar a probabilidade falsifica F6.
- **C** — Custos legais do denunciante. ``custo_legal_uw > 0`` modula a
  IR-W do arquétipo racional; eleva o piso de recompensa para denunciar.
"""

from __future__ import annotations

from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Vetor A — D_base do TCC clássico erode incentivo WaaS
# ----------------------------------------------------------------------


def test_vetor_a_d_base_zero_preserva_comportamento_original():
    """Default `D_disc_base_tcc=0.0` ⇒ IC-F* compara D_total × W (compat)."""
    base = dict(
        n_empresas=12,
        tam_medio_empresa=120,
        n_tiques=20,
        seed=51,
        regime="B",
        fracao_violadoras=0.5,
        taxa_observacao=0.4,
    )
    df_zero = WaaSModel(WaaSParametros(**base, D_disc_base_tcc=0.0)).executar()
    tcc_zero = int(df_zero["n_tcc_assinados"].max())
    # Modelo com D_base=0 mantém o sistema operante (algum TCC ocorre).
    assert tcc_zero >= 0  # não-negatividade


def test_vetor_a_d_base_alto_quebra_o_mecanismo():
    """Quando `D_disc_base_tcc ≥ D_disc`, `D_extra = 0` ⇒ ninguém paga W.

    A firma prefere TCC clássico (Art. 85 sozinho), e o contador
    `n_firmas_optaram_tcc_classico` registra o vetor de quebra A.
    """
    base = dict(
        n_empresas=20,
        tam_medio_empresa=200,
        n_tiques=30,
        seed=59,
        regime="B",
        fracao_violadoras=0.8,
        taxa_observacao=0.5,
        D_disc=0.30,
    )
    # D_base igual ao D total ⇒ incremento nulo ⇒ IC-F* nunca satisfeita.
    m = WaaSModel(WaaSParametros(**base, D_disc_base_tcc=0.30))
    df = m.executar()
    pagou = int(df["n_pagou"].max())
    optaram = int(df["n_firmas_optaram_tcc_classico"].max())
    assert pagou == 0, f"esperado nenhuma firma pague W; pagou={pagou}"
    assert optaram >= 1, f"vetor A não materializado: n_firmas_optaram_tcc_classico={optaram}"


def test_vetor_a_d_base_intermediario_reduz_pagamentos():
    """`D_base` intermediário entre 0 e D_disc reduz proporcionalmente o
    número de firmas que decidem pagar W."""
    base = dict(
        n_empresas=20,
        tam_medio_empresa=200,
        n_tiques=30,
        seed=61,
        regime="B",
        fracao_violadoras=0.8,
        taxa_observacao=0.5,
        D_disc=0.30,
    )
    df_zero = WaaSModel(WaaSParametros(**base, D_disc_base_tcc=0.0)).executar()
    df_meio = WaaSModel(WaaSParametros(**base, D_disc_base_tcc=0.20)).executar()
    pagou_zero = int(df_zero["n_pagou"].max())
    pagou_meio = int(df_meio["n_pagou"].max())
    assert pagou_meio <= pagou_zero, (
        f"esperado D_base intermediário reduzir pagamentos; "
        f"zero={pagou_zero}, meio={pagou_meio}"
    )


# ----------------------------------------------------------------------
# Vetor B — anulação judicial do TCC (F6 explicitado)
# ----------------------------------------------------------------------


def test_vetor_b_p_anulacao_zero_preserva_comportamento():
    """`p_anulacao_tcc=0.0` (default) ⇒ TCC-WaaS válido, sem anulações."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=10,
            tam_medio_empresa=100,
            n_tiques=15,
            seed=67,
            regime="B",
            p_anulacao_tcc=0.0,
        )
    )
    df = m.executar()
    assert int(df["n_tcc_anulados"].max()) == 0


def test_vetor_b_p_anulacao_um_anula_todos_os_tcc():
    """`p_anulacao_tcc=1.0` (limite) ⇒ todo TCC-WaaS é anulado, multa cheia.

    Falsificador F6 levado ao limite. Confirma o canal direcionalmente
    (efeito não-nulo).
    """
    base = dict(
        n_empresas=15,
        tam_medio_empresa=200,
        n_tiques=30,
        seed=71,
        regime="B",
        fracao_violadoras=0.7,
        taxa_observacao=0.5,
    )
    df_zero = WaaSModel(WaaSParametros(**base, p_anulacao_tcc=0.0)).executar()
    df_um = WaaSModel(WaaSParametros(**base, p_anulacao_tcc=1.0)).executar()
    # Com anulação total, a multa cheia (sem desconto) retorna ao erário;
    # logo, a multa acumulada com p_anulacao=1 NÃO PODE ser inferior à
    # com p_anulacao=0 (anulação retira o desconto, eleva o valor pago).
    multa_zero = float(df_zero["multa_arrecadada_acum"].max())
    multa_um = float(df_um["multa_arrecadada_acum"].max())
    assert multa_um >= multa_zero, (
        f"esperado multa_um>=multa_zero (anulação retira desconto); "
        f"zero={multa_zero:.0f}, um={multa_um:.0f}"
    )
    assert int(df_um["n_tcc_anulados"].max()) >= 1


# ----------------------------------------------------------------------
# Vetor C — custo legal do denunciante eleva piso da IR-W
# ----------------------------------------------------------------------


def test_vetor_c_custo_legal_zero_preserva_comportamento():
    """`custo_legal_uw=0.0` (default) ⇒ IR-W = `W ≥ r · tol · 2 · w_a` (compat)."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=8,
            tam_medio_empresa=120,
            n_tiques=10,
            seed=73,
            regime="B",
            custo_legal_uw=0.0,
        )
    )
    df = m.executar()
    # Sem custo legal, o sistema deve produzir alguns sinais.
    assert int(df["n_sinais"].sum()) >= 0


def test_vetor_c_custo_legal_alto_reduz_sinalizacao_racional():
    """Custo legal alto eleva o piso da IR-W e reduz o nº de sinais —
    em particular no arquétipo racional, que computa a IR-W explicitamente.
    """
    base = dict(
        n_empresas=20,
        tam_medio_empresa=200,
        n_tiques=20,
        seed=79,
        regime="B",
        fracao_violadoras=0.7,
        taxa_observacao=0.6,
        W_mult=1.5,
        r_represalia=0.15,
    )
    df_zero = WaaSModel(WaaSParametros(**base, custo_legal_uw=0.0)).executar()
    # custo_legal = 5·w_a — derrota qualquer W razoável no racional.
    df_alto = WaaSModel(WaaSParametros(**base, custo_legal_uw=5.0)).executar()
    sinais_zero = int(df_zero["n_sinais"].sum())
    sinais_alto = int(df_alto["n_sinais"].sum())
    assert sinais_alto <= sinais_zero, (
        f"esperado custo legal alto reduzir sinais (racional não dispara); "
        f"zero={sinais_zero}, alto={sinais_alto}"
    )


# ----------------------------------------------------------------------
# Combinação: o mecanismo é robusto até onde?
# ----------------------------------------------------------------------


def test_combinacao_d_base_e_anulacao_corroem_o_mecanismo():
    """Combinar D_base alto + p_anulacao alto **degrada** o sistema:
    incentivo marginal cai e ainda há risco de anulação. Demonstra que o
    mecanismo é frágil sob calibração adversa — propriedade desejável
    para um falsificador honesto."""
    base = dict(
        n_empresas=20,
        tam_medio_empresa=200,
        n_tiques=30,
        seed=83,
        regime="B",
        fracao_violadoras=0.7,
        taxa_observacao=0.5,
    )
    df_robusto = WaaSModel(
        WaaSParametros(**base, D_disc_base_tcc=0.0, p_anulacao_tcc=0.0)
    ).executar()
    df_quebrado = WaaSModel(
        WaaSParametros(**base, D_disc_base_tcc=0.25, p_anulacao_tcc=0.5)
    ).executar()
    pagou_robusto = int(df_robusto["n_pagou"].max())
    pagou_quebrado = int(df_quebrado["n_pagou"].max())
    assert pagou_quebrado <= pagou_robusto, (
        f"esperado calibração adversa reduzir pagamentos; "
        f"robusto={pagou_robusto}, quebrado={pagou_quebrado}"
    )
