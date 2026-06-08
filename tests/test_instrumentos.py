"""Testes do módulo declarativo `instrumentos.py` (R21 + Eco A + Adv B v2)."""

from __future__ import annotations

import pytest

from waas_antitrust.instrumentos import (
    INSTRUMENTOS,
    Instrumento,
    instrumentos_por_regime,
    lookup_instrumento,
)


def test_catalogo_tem_4_instrumentos_canonicos():
    """Quatro instrumentos: WaaS, Hirschman, Tributário, Criminal."""
    assert len(INSTRUMENTOS) == 4
    nomes = {i.nome for i in INSTRUMENTOS}
    esperados = {
        "recompensa_tcc_waas",
        "vesting_acelerado_hirschman",
        "credito_tributario_denunciante",
        "leniencia_criminal_individual",
    }
    assert nomes == esperados


def test_instrumento_e_dataclass_frozen():
    """`Instrumento` é dataclass imutável (frozen=True)."""
    from dataclasses import FrozenInstanceError

    waas = INSTRUMENTOS[0]
    assert isinstance(waas, Instrumento)
    with pytest.raises(FrozenInstanceError):
        waas.nome = "outro"  # type: ignore[misc]


def test_status_canonicos():
    """Cada instrumento declara status implementado/stub/conceitual."""
    statuses_validos = {"implementado", "stub", "conceitual"}
    for inst in INSTRUMENTOS:
        assert inst.status in statuses_validos, f"{inst.nome}: status {inst.status!r} inválido"


def test_waas_e_hirschman_implementados():
    """Os 2 primeiros instrumentos têm implementação real no projeto."""
    waas = lookup_instrumento("recompensa_tcc_waas")
    hirsch = lookup_instrumento("vesting_acelerado_hirschman")
    assert waas.status == "implementado"
    assert hirsch.status == "implementado"


def test_tributario_e_criminal_sao_stub():
    """Os 2 últimos instrumentos são stubs declarativos (R22, R23)."""
    trib = lookup_instrumento("credito_tributario_denunciante")
    crim = lookup_instrumento("leniencia_criminal_individual")
    assert trib.status == "stub"
    assert crim.status == "stub"


def test_reservas_constitucionais_corretas():
    """Adv B v2: três reservas constitucionais hierárquicas."""
    waas = lookup_instrumento("recompensa_tcc_waas")
    hirsch = lookup_instrumento("vesting_acelerado_hirschman")
    trib = lookup_instrumento("credito_tributario_denunciante")
    crim = lookup_instrumento("leniencia_criminal_individual")
    assert "Art. 22" in waas.reserva_constitucional
    assert "Art. 22" in hirsch.reserva_constitucional
    assert "Art. 146" in trib.reserva_constitucional  # LC tributária
    assert "Art. 5º XXXIX" in crim.reserva_constitucional  # penal estrita


def test_lookup_instrumento_levanta_em_desconhecido():
    with pytest.raises(KeyError, match="desconhecido"):
        lookup_instrumento("instrumento_inexistente")


def test_instrumentos_por_regime_a_vazio():
    """Regime A: nenhum instrumento."""
    assert instrumentos_por_regime("A") == []


def test_instrumentos_por_regime_b_so_waas():
    """Regime B: apenas o instrumento WaaS (reserva ordinária)."""
    lista = instrumentos_por_regime("B")
    assert len(lista) == 1
    assert lista[0].nome == "recompensa_tcc_waas"


def test_instrumentos_por_regime_c_inclui_hirschman():
    """Regime C/Cₜ: WaaS + Hirschman."""
    lista = instrumentos_por_regime("C")
    nomes = {i.nome for i in lista}
    assert nomes == {"recompensa_tcc_waas", "vesting_acelerado_hirschman"}


def test_instrumentos_por_regime_subregime_invalido():
    with pytest.raises(ValueError, match="regime desconhecido"):
        instrumentos_por_regime("X")


def test_fontes_primarias_documentam_lac():
    """Adv A v2: WaaS deve citar LAC Art. 7º como precedente dogmático."""
    waas = lookup_instrumento("recompensa_tcc_waas")
    assert "LAC" in waas.fonte_primaria or "12.846" in waas.fonte_primaria
