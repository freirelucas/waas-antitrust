"""Testes de R19 — choques exógenos discretos.

Cobertura:
- Validação de Choque (tipo, tique, magnitude);
- Aplicação de cada tipo (layoff, caso_paradigmatico, campanha_cade,
  choque_juridico);
- Catálogos canônicos (tech_2022_2024 etc.);
- Integração em WaaSModel.step() — choque do tique X efetivamente atua;
- Ex-funcionário tem r efetivo reduzido (hipótese layoffs);
- Reporters de diagnóstico.
"""

from __future__ import annotations

import pytest

from waas_antitrust.choques import (
    CHOQUES_CAMPANHA_CADE_DIGITAL,
    CHOQUES_CASO_PARADIGMATICO_IFOOD_2023,
    CHOQUES_JURIDICO_ADVERSO,
    CHOQUES_TECH_2022_2024,
    Choque,
    aplicar_choque,
    listar_catalogos,
)
from waas_antitrust.model import WaaSModel, WaaSParametros

# ----------------------------------------------------------------------
# Validação da dataclass Choque
# ----------------------------------------------------------------------


def test_choque_valido_constroi():
    c = Choque(tique=4, tipo="layoff", magnitude=0.06, descricao="onda jan/23")
    assert c.tique == 4
    assert c.tipo == "layoff"


def test_choque_tipo_invalido_levanta():
    with pytest.raises(ValueError, match="tipo de choque desconhecido"):
        Choque(tique=1, tipo="alien_event", magnitude=0.1)


def test_choque_tique_zero_levanta():
    with pytest.raises(ValueError, match="tique deve ser >= 1"):
        Choque(tique=0, tipo="layoff", magnitude=0.1)


def test_choque_magnitude_fora_intervalo_levanta():
    with pytest.raises(ValueError, match="magnitude"):
        Choque(tique=1, tipo="layoff", magnitude=1.5)
    with pytest.raises(ValueError, match="magnitude"):
        Choque(tique=1, tipo="layoff", magnitude=-0.1)


# ----------------------------------------------------------------------
# Catálogos canônicos
# ----------------------------------------------------------------------


def test_catalogo_tech_2022_2024_tem_dois_choques():
    assert len(CHOQUES_TECH_2022_2024) == 2
    assert all(c.tipo == "layoff" for c in CHOQUES_TECH_2022_2024)


def test_listar_catalogos_devolve_quatro_chaves():
    catalogos = listar_catalogos()
    assert set(catalogos.keys()) == {
        "tech_2022_2024",
        "campanha_cade_digital",
        "caso_paradigmatico_ifood_2023",
        "juridico_adverso",
    }


# ----------------------------------------------------------------------
# Aplicação direta dos choques
# ----------------------------------------------------------------------


def test_aplicar_layoff_converte_fracao_dos_trabalhadores():
    m = WaaSModel(WaaSParametros(n_empresas=4, tam_medio_empresa=100, n_tiques=1, seed=11))
    aplicar_choque(m, Choque(tique=1, tipo="layoff", magnitude=0.10))
    total = sum(len(ws) for ws in m.trabalhadores_por_empresa.values())
    n_ex = sum(
        sum(1 for t in ws if t.status == "ex_funcionario")
        for ws in m.trabalhadores_por_empresa.values()
    )
    # ~10% (com arredondamento por firma).
    assert n_ex > 0
    assert n_ex < total
    fracao = n_ex / total
    assert abs(fracao - 0.10) < 0.05  # margem para arredondamento por firma


def test_aplicar_caso_paradigmatico_eleva_p_perc():
    m = WaaSModel(WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=1, seed=13))
    p_inicial = m.p_perc
    aplicar_choque(m, Choque(tique=1, tipo="caso_paradigmatico", magnitude=0.40))
    assert m.p_perc >= 0.40
    assert m.p_perc >= p_inicial


def test_aplicar_campanha_cade_eleva_rho_autoridade():
    m = WaaSModel(WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=1, seed=17))
    rho_inicial = m.autoridade.rho
    aplicar_choque(m, Choque(tique=1, tipo="campanha_cade", magnitude=0.15))
    assert m.autoridade.rho > rho_inicial
    assert m.autoridade.rho <= 0.99


def test_aplicar_choque_juridico_eleva_p_anulacao():
    m = WaaSModel(
        WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=1, seed=19, p_anulacao_tcc=0.0)
    )
    aplicar_choque(m, Choque(tique=1, tipo="choque_juridico", magnitude=0.30))
    assert m.p_anulacao_tcc == pytest.approx(0.30)


# ----------------------------------------------------------------------
# Integração — choque é aplicado pelo step
# ----------------------------------------------------------------------


def test_choque_layoff_pelo_step_no_tique_correto():
    """Choque com tique=3 deve ser aplicado quando o modelo chegar ao tique 3."""
    choques = (Choque(tique=3, tipo="layoff", magnitude=0.05),)
    m = WaaSModel(
        WaaSParametros(
            n_empresas=6,
            tam_medio_empresa=120,
            n_tiques=5,
            seed=23,
            choques=choques,
        )
    )
    df = m.executar()
    # Antes do tique 3 não há ex-funcionários; depois há.
    n_ex_t2 = int(df.loc[df["tique"] == 2, "n_ex_funcionarios"].iloc[0])
    n_ex_t3 = int(df.loc[df["tique"] == 3, "n_ex_funcionarios"].iloc[0])
    assert n_ex_t2 == 0
    assert n_ex_t3 > 0
    assert int(df["n_choques_layoff_aplicados"].max()) == 1


def test_modelo_sem_choques_preserva_comportamento_compat():
    """`choques=()` (default) ⇒ nenhum ex-funcionário, nenhum choque aplicado."""
    df = WaaSModel(
        WaaSParametros(n_empresas=4, tam_medio_empresa=40, n_tiques=4, seed=29)
    ).executar()
    assert int(df["n_ex_funcionarios"].max()) == 0
    assert int(df["n_choques_layoff_aplicados"].max()) == 0


# ----------------------------------------------------------------------
# Hipótese substantiva: ex-funcionário tem r efetivo menor
# ----------------------------------------------------------------------


def test_ex_funcionario_tem_represalia_efetiva_menor():
    """`fator_represalia_ex_funcionario=0.2` ⇒ r efetivo = 0.2·r.

    Sob layoff massivo, a sinalização do arquétipo racional deve subir
    (mais agentes acima do limiar IR-W).
    """
    base = dict(
        n_empresas=15,
        tam_medio_empresa=200,
        n_tiques=10,
        seed=31,
        regime="B",
        fracao_violadoras=0.7,
        taxa_observacao=0.5,
        W_mult=1.5,
        r_represalia=0.30,  # alto, para que o efeito do fator seja visível
    )
    # Sem choque — baseline.
    df_sem = WaaSModel(WaaSParametros(**base, choques=())).executar()
    # Com layoff massivo no tique 2.
    choques_pesados = (Choque(tique=2, tipo="layoff", magnitude=0.50),)
    df_com = WaaSModel(
        WaaSParametros(**base, choques=choques_pesados, fator_represalia_ex_funcionario=0.1)
    ).executar()
    # Hipótese: com 50% de ex-funcionários e r efetivo 10×menor,
    # o nº de sinais NÃO É menor que o baseline.
    sinais_sem = int(df_sem["n_sinais"].sum())
    sinais_com = int(df_com["n_sinais"].sum())
    assert sinais_com >= sinais_sem, (
        f"layoff massivo + r ex-funcionário baixo deveria aumentar (ou manter) "
        f"sinais; sem={sinais_sem}, com={sinais_com}"
    )


def test_catalogo_tech_2022_2024_executa_end_to_end():
    """O catálogo canônico roda sem erro em horizonte 10 tiques."""
    m = WaaSModel(
        WaaSParametros(
            n_empresas=10,
            tam_medio_empresa=150,
            n_tiques=10,
            seed=37,
            regime="B",
            choques=CHOQUES_TECH_2022_2024,
        )
    )
    df = m.executar()
    assert int(df["n_choques_layoff_aplicados"].max()) == 2  # 2 ondas
    assert int(df["n_ex_funcionarios"].max()) > 0


def test_catalogos_paradigmatico_campanha_e_juridico_executam():
    for catalogo in (
        CHOQUES_CASO_PARADIGMATICO_IFOOD_2023,
        CHOQUES_CAMPANHA_CADE_DIGITAL,
        CHOQUES_JURIDICO_ADVERSO,
    ):
        m = WaaSModel(
            WaaSParametros(
                n_empresas=6,
                tam_medio_empresa=80,
                n_tiques=12,
                seed=41,
                regime="B",
                choques=catalogo,
            )
        )
        df = m.executar()
        assert len(df) == 12  # sanity
