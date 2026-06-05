"""Testes do módulo `calibracao/saito.py` — Carolina Saito (2021).

Após o "go saito": o módulo deixou de ser placeholder e ganhou dados reais
verificados no PDF primário (Saito, C., *TCC na Lei nº 12.529/11*,
CADE/PNUD, 24/02/2021, 349 TCCs CADE 2012-2019). Estes testes garantem
que as constantes refletem a fonte primária e que o helper de fallback
mantém invariantes esperadas pelos cenários (`waas_antitrust.cenarios`).
"""

from __future__ import annotations

import pytest

from waas_antitrust.calibracao import saito

# ----------------------------------------------------------------------
# Metadados bibliográficos (verbatim)
# ----------------------------------------------------------------------


def test_autoria_saito_verbatim():
    assert saito.AUTORIA_SAITO == "Carolina Saito"
    assert saito.DATA_PUBLICACAO_SAITO == "2021-02-24"


def test_n_tcc_eh_verbatim():
    """349 TCCs (verbatim do título da dissertação)."""
    assert saito.N_TCC_SAITO_2012_2019 == 349


def test_periodo_saito():
    """Período coberto: 04/07/2012 a 11/12/2019."""
    assert saito.PERIODO_SAITO == ("2012-07-04", "2019-12-11")


# ----------------------------------------------------------------------
# Estatísticas extraídas (Saito 2021, Imagens 23 e 25)
# ----------------------------------------------------------------------


def test_medias_por_posicao_sg_cade():
    """Imagem 23, p. 38: médias decrescentes do 1º ao 9º compromissário."""
    medias = saito.MEDIA_DESCONTO_SG_POR_POSICAO
    assert medias[1] == pytest.approx(0.4343)
    assert medias[2] == pytest.approx(0.3451)
    assert medias[3] == pytest.approx(0.2022)
    # Monotonia decrescente até a 3ª posição.
    assert medias[1] > medias[2] > medias[3]
    # Conveniences batem com o dict.
    assert medias[1] == saito.MEDIA_DESCONTO_SG_1A_POSICAO
    assert medias[2] == saito.MEDIA_DESCONTO_SG_2A_POSICAO
    assert medias[3] == saito.MEDIA_DESCONTO_SG_3A_POSICAO


def test_media_tribunal_1a_posicao_eh_15_por_cento():
    """Imagem 25, p. 39: 15,00% para 1ª posição no Tribunal/CADE."""
    assert pytest.approx(0.15) == saito.MEDIA_DESCONTO_TRIBUNAL_1A_POSICAO


def test_faixas_guia_cade_codificadas():
    """Guia CADE de TCC (11/09/2017): faixas codificadas para cartel."""
    assert saito.FAIXAS_DESCONTO_SG_GUIA_CADE[1] == (0.30, 0.50)
    assert saito.FAIXAS_DESCONTO_SG_GUIA_CADE[2] == (0.25, 0.40)
    assert saito.FAIXAS_DESCONTO_TRIBUNAL == (0.0, 0.15)


# ----------------------------------------------------------------------
# Marcações [?] — o que Saito NÃO reporta
# ----------------------------------------------------------------------


def test_mediana_eh_nao_reportada():
    """Saito (2021) reporta médias, não mediana. Constante deve ser None."""
    assert saito.MEDIANA_DESCONTO_TCC_2012_2019 is None
    assert saito.Q1_DESCONTO_TCC_2012_2019 is None
    assert saito.Q3_DESCONTO_TCC_2012_2019 is None


def test_decomposicao_por_conduta_nao_reportada():
    """A Imagem 21 traz alíquota de multa, não desconto — não inferir."""
    assert all(v is None for v in saito.MEDIANA_DESCONTO_POR_TIPO.values())


def test_disponivel_reflete_mediana_nao_reportada():
    """`disponivel()` indica False enquanto mediana for None."""
    assert saito.disponivel() is False


# ----------------------------------------------------------------------
# Helper de fallback — usado por `cenarios.py`
# ----------------------------------------------------------------------


def test_helper_devolve_media_tribunal_quando_mediana_indisponivel():
    """Política de seleção: fallback = média Tribunal/1ª posição (15%)."""
    assert saito.d_base_tcc_calibrado() == pytest.approx(0.15)


def test_helper_ignora_default_quando_tribunal_disponivel():
    """O default só é usado em situação patológica (Tribunal também None)."""
    assert saito.d_base_tcc_calibrado(default=0.99) == pytest.approx(0.15)


def test_helper_retorna_mediana_quando_preenchida(monkeypatch):
    """Quando mediana for fornecida via fonte alternativa, ela tem precedência."""
    monkeypatch.setattr(saito, "MEDIANA_DESCONTO_TCC_2012_2019", 0.22)
    assert saito.d_base_tcc_calibrado() == pytest.approx(0.22)
    assert saito.d_base_tcc_calibrado(default=0.99) == pytest.approx(0.22)


# ----------------------------------------------------------------------
# Resumo textual
# ----------------------------------------------------------------------


def test_resumo_inclui_autoria_e_n_e_medias():
    texto = saito.resumo()
    assert "Carolina Saito" in texto
    assert "349" in texto
    assert "43.43%" in texto or "0.4343" in texto or "43,43%" in texto
    assert "NÃO REPORTADA" in texto
