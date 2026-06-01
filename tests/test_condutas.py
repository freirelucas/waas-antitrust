"""Testes do catálogo de condutas × atores (R08, exploratório)."""

import pytest

from waas_antitrust.condutas import (
    BIGTECH_MADURA,
    CATALOGO,
    DISTRIBUICAO_PAPEIS_PADRAO,
    MARKETPLACE_BR,
    PAPEIS_PADRAO,
    Conduta,
    lookup_conduta,
    observabilidade,
)


def test_catalogo_tem_9_condutas_unicas():
    """Categoria 5 (PM): catálogo passou de 7 → 9 com adição BR (iFood, Apple)."""
    nomes = [c.nome for c in CATALOGO]
    assert len(CATALOGO) == 9
    assert len(set(nomes)) == 9  # nenhum nome duplicado


def test_catalogo_inclui_condutas_brasileiras():
    """Categoria 5.1/5.2 (PM): cobertura específica do mercado BR."""
    nomes = {c.nome for c in CATALOGO}
    assert "exclusividade_retaliacao_marketplace" in nomes
    assert "anti_steering_iap" in nomes


def test_lookup_funciona_e_levanta_em_desconhecida():
    c = lookup_conduta("self_preferencing")
    assert isinstance(c, Conduta)
    assert "eng" in c.atores_primarios
    with pytest.raises(KeyError):
        lookup_conduta("conduta_inexistente")


def test_observabilidade_gradiente_3_niveis():
    """Categoria 5.5 (PM): gradiente 3-níveis em vez de binário.
    Primário=1.0, adjacente=0.5, distal=0.1."""
    sp = lookup_conduta("self_preferencing")
    # primário (eng está em atores_primarios)
    assert observabilidade("eng", sp) == 1.0
    # adjacente (growth está em atores_adjacentes)
    assert observabilidade("growth", sp) == 0.5
    # distal (design não está em nenhum dos dois conjuntos para self_preferencing)
    assert observabilidade("design", sp) == 0.1
    # ordenação estrita
    assert (
        observabilidade("eng", sp) > observabilidade("growth", sp) > observabilidade("design", sp)
    )


def test_atores_primarios_cobrem_papeis_centrais():
    """Cada conduta canônica deve ter pelo menos 1 ator primário em PAPEIS_PADRAO."""
    for c in CATALOGO:
        for ator in c.atores_primarios:
            assert ator in PAPEIS_PADRAO, f"{c.nome}: ator '{ator}' não está em PAPEIS_PADRAO"


def test_distribuicao_papeis_soma_um():
    soma = sum(DISTRIBUICAO_PAPEIS_PADRAO.values())
    assert abs(soma - 1.0) < 1e-9, f"distribuição soma {soma}, esperado 1.0"


def test_presets_bigtech_e_marketplace_somam_um():
    """Categoria 5.4 (PM): MARKETPLACE_BR convive com BIGTECH_MADURA (default)."""
    assert abs(sum(BIGTECH_MADURA.values()) - 1.0) < 1e-9
    assert abs(sum(MARKETPLACE_BR.values()) - 1.0) < 1e-9
    # Marketplace BR é operations-heavy; bigtech é eng-heavy.
    assert MARKETPLACE_BR["operacoes"] > BIGTECH_MADURA["operacoes"]
    assert BIGTECH_MADURA["eng"] > MARKETPLACE_BR["eng"]
    # Default mantido como BIGTECH_MADURA (preserva calibração existente).
    assert DISTRIBUICAO_PAPEIS_PADRAO == BIGTECH_MADURA


def test_papeis_padrao_inclui_operacoes_e_financeiro():
    """Categoria 5.3 (PM): operações (marketplaces) e financeiro (FP&A)."""
    assert "operacoes" in PAPEIS_PADRAO
    assert "financeiro" in PAPEIS_PADRAO


def test_casos_referencia_documentados():
    """Cada conduta deve ter pelo menos 1 caso de referência verificável."""
    for c in CATALOGO:
        assert len(c.casos_referencia) >= 1, f"{c.nome}: sem caso de referência"


def test_modelo_atribui_papel_e_conduta():
    """O modelo atribui um papel a cada trabalhador e uma conduta-tipo por firma."""
    from waas_antitrust.model import WaaSModel, WaaSParametros

    m = WaaSModel(
        WaaSParametros(n_empresas=8, tam_medio_empresa=80, n_tiques=1, seed=3, regime="B")
    )
    # Cada firma com conduta_potencial registrada
    for e in m.empresas:
        assert e.conduta_potencial is not None
        assert e.conduta_potencial in {c.nome for c in CATALOGO}
    # Cada trabalhador com papel
    for ws in m.trabalhadores_por_empresa.values():
        for t in ws:
            assert t.papel in PAPEIS_PADRAO


def test_engenheiros_observam_mais_self_preferencing():
    """Direcional: numa firma cuja conduta é self_preferencing, engenheiros
    (ator primário) observam mais que designers (ator secundário)."""
    from waas_antitrust.model import WaaSModel, WaaSParametros

    # Roda só um tique para amostrar observou após P0; força violação para
    # garantir conduta ativa e usa taxa_observacao alta para reduzir ruído.
    p = WaaSParametros(
        n_empresas=15,
        tam_medio_empresa=400,
        n_tiques=1,
        seed=23,
        regime="B",
        fracao_violadoras=1.0,
        taxa_observacao=0.5,
    )
    m = WaaSModel(p)
    # Força todas as firmas a self_preferencing para o teste ser sobre o papel.
    for e in m.empresas:
        e.conduta_potencial = "self_preferencing"
    m.step()

    obs_eng, obs_des = 0, 0
    n_eng, n_des = 0, 0
    for ws in m.trabalhadores_por_empresa.values():
        for t in ws:
            if t.papel == "eng":
                n_eng += 1
                obs_eng += int(t.observou)
            elif t.papel == "design":
                n_des += 1
                obs_des += int(t.observou)
    # Razões esperadas (peso 1.0 vs 0.2 × taxa_observacao):
    # engenheiros ~50%, designers ~10%. Pode haver variabilidade mas a razão
    # tem que claramente favorecer engenheiros.
    taxa_eng = obs_eng / max(1, n_eng)
    taxa_des = obs_des / max(1, n_des)
    assert taxa_eng > taxa_des, (
        f"esperado eng > design em self_preferencing: "
        f"taxa_eng={taxa_eng:.2f} ({obs_eng}/{n_eng}), "
        f"taxa_des={taxa_des:.2f} ({obs_des}/{n_des})"
    )
