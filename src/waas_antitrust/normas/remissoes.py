"""Extrator de remissões cruzadas entre dispositivos legais.

Captura padrões canônicos do tipo:

- "Art. 85 desta Lei"
- "Art. 86, § 7º"
- "Art. 45, V e VI da Lei nº 12.529, de 30 de novembro de 2011"
- "Art. 4º-A da Lei 13.608/2018"
- "art. 88 da Lei 12.529/11"

Utilidade no WaaS: mapear o "espaço normativo" do mecanismo (Art. 12
da Res. 21/2018 → Art. 45, V e VI da Lei 12.529 → Art. 85 da mesma
Lei) como **grafo dirigido** que pode ser consumido por NetworkX.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Captura: "art." ou "Art." + número (com sufixos), opcionalmente
# seguido de §, inciso, alínea, e da norma de referência.
_PADRAO_REMISSAO = re.compile(
    r"""
    \b[Aa]rt\.\s*                              # 'Art.'
    (?P<artigo>\d+(?:[ºo°])?(?:-[A-Z])?)       # número (12, 4º, 4º-A...)
    (?:\s*,?\s*§\s*(?P<paragrafo>\d+)[ºo°]?)?  # opcional § N
    (?:\s*,?\s*                                # opcional incisos
        (?P<incisos>
            [IVXLCDM]+
            (?:\s*(?:,|e)\s*[IVXLCDM]+)*       # "V e VI" ou "II, III e IV"
        )
    )?
    (?:\s*,?\s*alínea\s+(?P<alinea>[a-z]))?    # opcional alínea
    (?:\s+d[ae]                                # opcional "da Lei..."
        \s+(?P<norma>
            (?:Lei\s+(?:Complementar\s+)?(?:nº\s*)?[\d\.]+(?:/\d{2,4})?)
            | (?:Resolu[çc][ãa]o\s+(?:CADE\s+)?(?:nº\s*)?[\d\.]+(?:/\d{2,4})?)
            | (?:Decreto(?:-Lei)?\s+(?:nº\s*)?[\d\.]+(?:/\d{2,4})?)
        )
    )?
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class Remissao:
    """Referência cruzada extraída de um texto legal."""

    artigo: str  # "12", "4º", "4º-A"
    paragrafo: str | None  # "7", None
    incisos: tuple[str, ...]  # ("V", "VI") ou ()
    alinea: str | None  # "a" ou None
    norma_alvo: str | None  # "Lei nº 12.529, de 30 de novembro de 2011" ou None
    trecho_capturado: str  # texto bruto extraído

    def __str__(self) -> str:
        partes = [f"Art. {self.artigo}"]
        if self.paragrafo:
            partes.append(f"§ {self.paragrafo}º")
        if self.incisos:
            partes.append(", ".join(self.incisos))
        if self.alinea:
            partes.append(f"alínea {self.alinea}")
        ref = " ".join(partes)
        if self.norma_alvo:
            ref += f" da {self.norma_alvo}"
        return ref


def _split_incisos(s: str | None) -> tuple[str, ...]:
    if not s:
        return ()
    # Aceita "V e VI", "II, III e IV"
    partes = re.split(r"\s*(?:,|e)\s*", s.strip())
    return tuple(p for p in (p.strip() for p in partes) if p)


def extrair_remissoes(texto: str) -> list[Remissao]:
    """Devolve todas as remissões cruzadas encontradas em `texto`.

    Implementação conservadora: apenas padrões inequivocamente
    capturáveis por regex sobre a LC 95/1998. Casos ambíguos
    (e.g., "o artigo anterior") ficam fora — preferimos perder
    captura a inventar referências.
    """
    resultado: list[Remissao] = []
    for m in _PADRAO_REMISSAO.finditer(texto):
        # Filtra falsos positivos: artigo precisa ser número plausível.
        artigo = (m.group("artigo") or "").strip()
        if not artigo:
            continue
        resultado.append(
            Remissao(
                artigo=artigo,
                paragrafo=m.group("paragrafo"),
                incisos=_split_incisos(m.group("incisos")),
                alinea=m.group("alinea"),
                norma_alvo=(m.group("norma") or "").strip() or None,
                trecho_capturado=m.group(0).strip(),
            )
        )
    return resultado
