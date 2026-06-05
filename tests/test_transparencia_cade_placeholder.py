"""Testes do módulo `calibracao/transparencia_cade.py` — placeholder R06.

Garantem que: (a) o estado placeholder está honestamente marcado com
`None` em todas as constantes principais; (b) os helpers
(`disponivel`, `servidores_sg_calibrado`, `capacidade_efetiva_por_tique`,
`resumo`) se comportam corretamente em ambos os estados (placeholder e
preenchido).
"""

from __future__ import annotations

from waas_antitrust.calibracao import transparencia_cade as tcade

# ----------------------------------------------------------------------
# Estado placeholder — constantes principais a `None`
# ----------------------------------------------------------------------


def test_placeholder_constantes_principais_none():
    """Enquanto não houver extração, tudo em None."""
    assert tcade.N_SERVIDORES_TOTAL is None
    assert all(v is None for v in tcade.N_SERVIDORES_POR_CATEGORIA.values())
    assert all(v is None for v in tcade.N_SERVIDORES_POR_UNIDADE.values())
    assert all(v is None for v in tcade.ORCAMENTO_LOA_POR_ANO.values())
    assert all(v is None for v in tcade.EXECUCAO_ORCAMENTARIA_POR_ANO.values())


def test_disponivel_reflete_placeholder():
    """`disponivel()` é False enquanto N_SERVIDORES_TOTAL for None."""
    if tcade.N_SERVIDORES_TOTAL is None:
        assert tcade.disponivel() is False


# ----------------------------------------------------------------------
# Helpers de fallback
# ----------------------------------------------------------------------


def test_servidores_sg_devolve_default_quando_placeholder():
    """Com unidade SG não preenchida, helper devolve `default`."""
    assert tcade.servidores_sg_calibrado(default=50) == 50
    assert tcade.servidores_sg_calibrado(default=80) == 80


def test_servidores_sg_devolve_dado_real_quando_preenchido(monkeypatch):
    """Quando SG for preenchida, helper devolve o valor real (ignora default)."""
    monkeypatch.setitem(tcade.N_SERVIDORES_POR_UNIDADE, "superintendencia_geral", 73)
    assert tcade.servidores_sg_calibrado() == 73
    assert tcade.servidores_sg_calibrado(default=999) == 73


def test_capacidade_efetiva_eh_none_em_placeholder():
    """Sem dados de SG, `capacidade_efetiva_por_tique` retorna `None`
    — sinaliza ao chamador que deve cair em fallback (e.g.,
    `INVESTIGACOES_ANUAIS_CADE/4`)."""
    if tcade.N_SERVIDORES_POR_UNIDADE["superintendencia_geral"] is None:
        assert tcade.capacidade_efetiva_por_tique() is None


def test_capacidade_efetiva_calcula_quando_preenchido(monkeypatch):
    """Com SG=80 e 2 casos/ano/servidor → 160 casos/ano → 40/trimestre."""
    monkeypatch.setitem(tcade.N_SERVIDORES_POR_UNIDADE, "superintendencia_geral", 80)
    cap = tcade.capacidade_efetiva_por_tique(trimestres_por_ano=4, casos_por_servidor_ano=2.0)
    assert cap == 40


def test_capacidade_efetiva_respeita_piso_de_1(monkeypatch):
    """Para SG pequena ou produtividade baixa, capacidade nunca cai a zero."""
    monkeypatch.setitem(tcade.N_SERVIDORES_POR_UNIDADE, "superintendencia_geral", 1)
    cap = tcade.capacidade_efetiva_por_tique(trimestres_por_ano=4, casos_por_servidor_ano=0.1)
    assert cap == 1  # piso explícito


# ----------------------------------------------------------------------
# Resumo textual
# ----------------------------------------------------------------------


def test_resumo_indica_placeholder():
    texto = tcade.resumo()
    if not tcade.disponivel():
        assert "placeholder" in texto
        assert "N_SERVIDORES_TOTAL" in texto


def test_resumo_inclui_numero_quando_preenchido(monkeypatch):
    monkeypatch.setattr(tcade, "N_SERVIDORES_TOTAL", 420)
    monkeypatch.setitem(tcade.N_SERVIDORES_POR_UNIDADE, "superintendencia_geral", 70)
    texto = tcade.resumo()
    assert "420" in texto
    assert "70" in texto


# ----------------------------------------------------------------------
# Categorias e unidades — estrutura é estável
# ----------------------------------------------------------------------


def test_categorias_funcionais_estaveis():
    """Categorias funcionais cobrem o organograma do CADE."""
    esperadas = {
        "eppgg",
        "procurador_federal",
        "tecnico_administrativo",
        "conselheiro",
        "cargo_comissionado",
    }
    assert set(tcade.N_SERVIDORES_POR_CATEGORIA.keys()) == esperadas


def test_unidades_operacionais_estaveis():
    """Três unidades canônicas: SG, DEE, Tribunal."""
    esperadas = {
        "superintendencia_geral",
        "departamento_estudos_economicos",
        "tribunal_administrativo",
    }
    assert set(tcade.N_SERVIDORES_POR_UNIDADE.keys()) == esperadas


def test_orcamento_cobre_anos_recentes():
    """LOA e execução cobrem 2022-2024."""
    assert set(tcade.ORCAMENTO_LOA_POR_ANO.keys()) == {2022, 2023, 2024}
    assert set(tcade.EXECUCAO_ORCAMENTARIA_POR_ANO.keys()) == {2022, 2023, 2024}
