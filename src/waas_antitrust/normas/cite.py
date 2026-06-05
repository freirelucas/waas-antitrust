"""Citação verbatim — `citar(urn, dispositivo)` recupera trecho do corpus.

Atende ao invariante CLAUDE.md: **toda citação deve ser verificável**.
O helper devolve o trecho literal do corpus local com a marca de
estado (verbatim vs. redação consolidada de teste) deixada a cargo do
chamador, que pode inspecionar o cabeçalho do arquivo via
`carregar_norma`.
"""

from __future__ import annotations

from waas_antitrust.normas.articulacao import (
    buscar_dispositivo,
    parse_articulacao,
)
from waas_antitrust.normas.corpus import carregar_norma
from waas_antitrust.normas.urn import URNLex


def citar(urn: URNLex | str, dispositivo: str) -> str:
    """Devolve o texto verbatim de um dispositivo de uma norma indexada.

    Exemplos:
        citar(URN_LEI_12529, "Art. 85")
        citar(URN_LEI_12529, "Art. 86")
        citar(URN_LEI_13608, "Art. 4º-A")
        citar(URN_RESOLUCAO_CADE_21_2018, "Art. 12")

    Levanta `KeyError` se a URN não estiver no corpus; `LookupError`
    se o dispositivo não for encontrado dentro da norma.
    """
    texto = carregar_norma(urn)
    raizes = parse_articulacao(texto)
    disp = buscar_dispositivo(raizes, dispositivo)
    if disp is None:
        raise LookupError(f"Dispositivo {dispositivo!r} não encontrado em {urn}.")
    return disp.texto


def citar_com_subitens(urn: URNLex | str, dispositivo: str) -> str:
    """Como `citar`, mas concatena o caput com todos os subitens (§/inciso/alínea).

    Útil para citar artigo completo no paper. Subitens são rotulados
    no início de cada bloco (rótulo + texto).
    """
    texto = carregar_norma(urn)
    raizes = parse_articulacao(texto)
    disp = buscar_dispositivo(raizes, dispositivo)
    if disp is None:
        raise LookupError(f"Dispositivo {dispositivo!r} não encontrado em {urn}.")
    partes = [disp.texto]
    for filho in disp.filhos:
        partes.append(f"{filho.rotulo}. {filho.texto}")
        for neto in filho.filhos:
            partes.append(f"  {neto.rotulo} — {neto.texto}")
    return "\n".join(partes)
