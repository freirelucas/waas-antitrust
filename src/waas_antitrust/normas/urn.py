"""URN-LEX: identificadores persistentes do LexML Brasil.

Formato canônico (RFC 5141 + perfil LexML):

    urn:lex:<jurisdicao>:<autoridade>:<tipo>:<data>;<numero>

Exemplo:

    urn:lex:br:federal:lei:2011-11-30;12529

Resolutor público (devolve HTML/PDF, NÃO XML estruturado — usar apenas
como link de citação):

    https://www.lexml.gov.br/urn/urn:lex:br:federal:lei:2011-11-30;12529

Referência: projeto.lexml.gov.br (Modelo de Referência + Parte 2: URN).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_REGEX_URN_LEX = re.compile(
    r"^urn:lex:"
    r"(?P<jurisdicao>[a-z][a-z\-]*):"
    r"(?P<autoridade>[a-z][a-z\.\-]*):"
    r"(?P<tipo>[a-z][a-z\.\-]*):"
    r"(?P<data>\d{4}-\d{2}-\d{2});"
    r"(?P<numero>[\d\.]+)"
    r"$"
)


@dataclass(frozen=True)
class URNLex:
    """Identificador URN-LEX (padrão LexML Brasil).

    Campos seguem o perfil oficial: jurisdição (`br`, `br;sp`...);
    autoridade (`federal`, `cade`, `tjsp`...); tipo (`lei`,
    `decreto`, `resolucao`...); data ISO (YYYY-MM-DD); número.
    """

    jurisdicao: str
    autoridade: str
    tipo: str
    data: str  # YYYY-MM-DD
    numero: str

    def __str__(self) -> str:
        return (
            f"urn:lex:{self.jurisdicao}:{self.autoridade}:" f"{self.tipo}:{self.data};{self.numero}"
        )

    @property
    def url_resolutor(self) -> str:
        """URL do resolutor público LexML — devolve HTML/PDF, não XML."""
        return f"https://www.lexml.gov.br/urn/{self}"


def parse_urn(urn: str) -> URNLex:
    """Decompõe uma string URN-LEX em `URNLex`.

    Levanta `ValueError` se o formato não bate com o perfil LexML.
    """
    m = _REGEX_URN_LEX.match(urn.strip())
    if m is None:
        raise ValueError(f"URN inválida (não bate com perfil LexML): {urn!r}")
    return URNLex(**m.groupdict())


# ----- URNs canônicas das normas centrais do WaaS --------------------

URN_LEI_12529 = URNLex(
    jurisdicao="br",
    autoridade="federal",
    tipo="lei",
    data="2011-11-30",
    numero="12529",
)

URN_LEI_13608 = URNLex(
    jurisdicao="br",
    autoridade="federal",
    tipo="lei",
    data="2018-01-10",
    numero="13608",
)

URN_LEI_13964 = URNLex(
    jurisdicao="br",
    autoridade="federal",
    tipo="lei",
    data="2019-12-24",
    numero="13964",
)

URN_RESOLUCAO_CADE_21_2018 = URNLex(
    jurisdicao="br",
    autoridade="cade",
    tipo="resolucao",
    data="2018-06-13",
    numero="21",
)
