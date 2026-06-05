"""Testes do módulo `normas` — URN-LEX, parser de articulação,
remissões cruzadas e citação verbatim a partir do corpus local."""

from __future__ import annotations

import pytest

from waas_antitrust.normas import (
    NORMAS_INDEXADAS,
    carregar_norma,
    citar,
    extrair_remissoes,
    parse_articulacao,
    parse_urn,
)
from waas_antitrust.normas.articulacao import buscar_dispositivo
from waas_antitrust.normas.cite import citar_com_subitens
from waas_antitrust.normas.urn import (
    URN_LEI_12529,
    URN_LEI_13608,
    URN_RESOLUCAO_CADE_21_2018,
)

# ----------------------------------------------------------------------
# URN-LEX
# ----------------------------------------------------------------------


def test_urn_str_canonica():
    urn = URN_LEI_12529
    assert str(urn) == "urn:lex:br:federal:lei:2011-11-30;12529"


def test_url_resolutor_lexml():
    urn = URN_LEI_12529
    assert urn.url_resolutor.endswith("/urn/urn:lex:br:federal:lei:2011-11-30;12529")


def test_parse_urn_redondo():
    """parse(str(urn)) ≡ urn — bijeção sob `__str__`."""
    for urn in (URN_LEI_12529, URN_LEI_13608, URN_RESOLUCAO_CADE_21_2018):
        assert parse_urn(str(urn)) == urn


def test_parse_urn_aceita_lei_complementar_e_resolucao():
    """Cobertura de tipos: lei, resolucao (com autoridade cade)."""
    p = parse_urn("urn:lex:br:cade:resolucao:2018-06-13;21")
    assert p.autoridade == "cade"
    assert p.tipo == "resolucao"


def test_parse_urn_invalida_levanta():
    with pytest.raises(ValueError, match="URN inválida"):
        parse_urn("xpto:lei:12.529")


# ----------------------------------------------------------------------
# Parser de articulação — LC 95/1998
# ----------------------------------------------------------------------


def test_articulacao_decompoe_artigos_e_paragrafos():
    """Art. 85 caput + 4 parágrafos numerados."""
    raizes = parse_articulacao(carregar_norma(URN_LEI_12529))
    arts = {r.rotulo: r for r in raizes if r.tipo == "artigo"}
    assert "Art. 85" in arts
    art85 = arts["Art. 85"]
    # Parágrafos do Art. 85 (1º, 2º, 3º, 4º).
    paragrafos = [f for f in art85.filhos if f.tipo == "paragrafo"]
    rotulos = {p.rotulo for p in paragrafos}
    assert "§ 1º" in rotulos
    assert "§ 2º" in rotulos
    assert "§ 3º" in rotulos
    assert "§ 4º" in rotulos


def test_articulacao_extrai_incisos_no_paragrafo_1():
    """§ 1º do Art. 85 tem 3 incisos (I, II, III)."""
    raizes = parse_articulacao(carregar_norma(URN_LEI_12529))
    art85 = next(r for r in raizes if r.tipo == "artigo" and r.rotulo == "Art. 85")
    par1 = next(p for p in art85.filhos if p.rotulo == "§ 1º")
    incisos = [i.rotulo for i in par1.filhos if i.tipo == "inciso"]
    assert incisos == ["I", "II", "III"]


def test_articulacao_paragrafo_unico():
    """Art. 87 tem `Parágrafo único`."""
    raizes = parse_articulacao(carregar_norma(URN_LEI_12529))
    art87 = next(r for r in raizes if r.tipo == "artigo" and r.rotulo == "Art. 87")
    rotulos = {f.rotulo for f in art87.filhos}
    assert "Parágrafo único" in rotulos


def test_articulacao_artigos_4a_a_4c_da_lei_13608():
    """Lei 13.608 tem Arts. 4º-A, 4º-B, 4º-C."""
    raizes = parse_articulacao(carregar_norma(URN_LEI_13608))
    rotulos = {r.rotulo for r in raizes if r.tipo == "artigo"}
    assert "Art. 4º-A" in rotulos
    assert "Art. 4º-B" in rotulos
    assert "Art. 4º-C" in rotulos


def test_articulacao_lida_com_linhas_em_branco():
    """Linhas em branco entre dispositivos não devem confundir o parser."""
    texto = "Art. 1º Caput um.\n\n\n§ 1º Algo.\n\nArt. 2º Caput dois."
    raizes = parse_articulacao(texto)
    # `º` é preservado no rótulo quando presente no número original.
    assert [r.rotulo for r in raizes if r.tipo == "artigo"] == ["Art. 1º", "Art. 2º"]


# ----------------------------------------------------------------------
# Corpus
# ----------------------------------------------------------------------


def test_corpus_indexa_tres_normas_centrais():
    assert str(URN_LEI_12529) in NORMAS_INDEXADAS
    assert str(URN_LEI_13608) in NORMAS_INDEXADAS
    assert str(URN_RESOLUCAO_CADE_21_2018) in NORMAS_INDEXADAS


def test_corpus_carregar_norma_aceita_urn_objeto_e_string():
    """API aceita URNLex e string indistintamente."""
    a = carregar_norma(URN_LEI_12529)
    b = carregar_norma(str(URN_LEI_12529))
    assert a == b


def test_corpus_norma_desconhecida_levanta():
    with pytest.raises(KeyError, match="não está indexada"):
        carregar_norma("urn:lex:br:federal:lei:1900-01-01;99999")


# ----------------------------------------------------------------------
# Cite — recupera trecho verbatim
# ----------------------------------------------------------------------


def test_citar_art_85_caput_verbatim():
    """O caput do Art. 85 deve conter o verbatim de INSTITUTIONAL.md."""
    texto = citar(URN_LEI_12529, "Art. 85")
    assert "Cade poderá tomar do representado compromisso de cessação" in texto
    assert "interesses protegidos por lei" in texto


def test_citar_art_12_resolucao_inclui_remissao_ao_45():
    """O Art. 12 da Res. 21/2018 cita `art. 45, V e VI` da Lei 12.529."""
    texto = citar(URN_RESOLUCAO_CADE_21_2018, "Art. 12")
    assert "ressarcimento" in texto.lower()
    assert "art. 45, V e VI" in texto


def test_citar_dispositivo_inexistente_levanta():
    with pytest.raises(LookupError, match="não encontrado"):
        citar(URN_LEI_12529, "Art. 999")


def test_citar_com_subitens_concatena_paragrafos():
    """`citar_com_subitens` traz caput + §§ rotulados."""
    completo = citar_com_subitens(URN_LEI_12529, "Art. 85")
    assert "§ 1º" in completo
    assert "§ 2º" in completo


# ----------------------------------------------------------------------
# Remissões cruzadas — extrator regex
# ----------------------------------------------------------------------


def test_remissoes_lei_12529_simples():
    """`Art. 48 desta Lei` é remissão interna; capturada."""
    rems = extrair_remissoes(carregar_norma(URN_LEI_12529))
    artigos = {r.artigo for r in rems}
    assert "48" in artigos  # Art. 48 é citado no Art. 85 caput
    assert "37" in artigos  # Art. 37 é citado no § 2º


def test_remissoes_resolucao_21_aponta_lei_12529():
    """Art. 12 da Res. 21/2018 remete a `art. 45, V e VI da Lei 12.529`."""
    texto = carregar_norma(URN_RESOLUCAO_CADE_21_2018)
    rems = extrair_remissoes(texto)
    rem_45 = next((r for r in rems if r.artigo == "45"), None)
    assert rem_45 is not None
    assert rem_45.incisos == ("V", "VI")
    assert "12.529" in (rem_45.norma_alvo or "")


def test_remissao_repr_legivel():
    """`str(remissao)` produz citação humana legível."""
    rems = extrair_remissoes(
        "ressarcimento das vítimas, conforme art. 45, V e VI da Lei 12.529/2011."
    )
    assert rems  # encontrou ao menos uma
    legivel = str(rems[0])
    assert "Art. 45" in legivel
    assert "V" in legivel and "VI" in legivel


def test_remissoes_devolve_lista_vazia_para_texto_sem_referencias():
    rems = extrair_remissoes("Este texto não cita nenhum dispositivo.")
    assert rems == []


# ----------------------------------------------------------------------
# Buscar dispositivo direto
# ----------------------------------------------------------------------


def test_buscar_dispositivo_devolve_none_se_nao_existe():
    raizes = parse_articulacao(carregar_norma(URN_LEI_12529))
    assert buscar_dispositivo(raizes, "Art. 999") is None


def test_buscar_dispositivo_artigo_existente():
    raizes = parse_articulacao(carregar_norma(URN_LEI_12529))
    art = buscar_dispositivo(raizes, "Art. 86")
    assert art is not None
    assert art.tipo == "artigo"


def test_buscar_dispositivo_paragrafo_composto():
    """Notação composta `Art. 85 § 1º` localiza o parágrafo."""
    raizes = parse_articulacao(carregar_norma(URN_LEI_12529))
    par = buscar_dispositivo(raizes, "Art. 85 § 1º")
    assert par is not None
    assert par.tipo == "paragrafo"
    assert par.rotulo == "§ 1º"
