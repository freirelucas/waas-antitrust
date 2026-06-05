"""Parsing e manipulação programática de normas jurídicas brasileiras.

Decisão de design (após pesquisa de metodologia em 2026-06): **não há
parser PT-BR maduro em Python para texto consolidado de leis em vigor**.
O caminho adotado é ad-hoc, disciplinado pela LC 95/1998 (técnica de
elaboração legislativa) — regex auditáveis sobre um corpus local.

Submódulos:

- ``urn``         — dataclass `URNLex` para identificadores persistentes
                    no padrão URN-LEX (LexML Brasil).
- ``articulacao`` — parser regex de texto articulado (Art./§/Inciso/
                    Alínea) conforme LC 95/1998.
- ``remissoes``   — extrator de remissões cruzadas entre dispositivos.
- ``corpus``      — corpus local versionado em ``data/normas/``: Lei
                    12.529/2011, Lei 13.608/2018, Resolução CADE 21/2018.
- ``cite``        — função `citar(urn, dispositivo)` que devolve trecho
                    **verbatim** a partir do corpus local — atende ao
                    invariante CLAUDE.md de citações verificáveis.

Limitações documentadas (`docs/DECISIONS.md` T07):

1. Parser regex cobre os padrões da LC 95/1998. Casos patológicos
   (notas marginais, citações longas no meio do dispositivo,
   formatação inconsistente) ficam fora.
2. Corpus local é "snapshot" das três normas-base citadas. Versões
   consolidadas precisam de atualização manual quando a lei muda.
3. Não há fetch em tempo de execução — a confiança vem do
   versionamento Git do corpus.
4. URN-LEX é gerada como identificador, não como ID resolvível
   externamente (o resolutor `lexml.gov.br` só devolve HTML/PDF, sem
   API estruturada).
"""

from waas_antitrust.normas.articulacao import (
    Dispositivo,
    parse_articulacao,
)
from waas_antitrust.normas.cite import citar
from waas_antitrust.normas.corpus import (
    NORMAS_INDEXADAS,
    carregar_norma,
)
from waas_antitrust.normas.remissoes import Remissao, extrair_remissoes
from waas_antitrust.normas.urn import URNLex, parse_urn

__all__ = [
    "Dispositivo",
    "NORMAS_INDEXADAS",
    "Remissao",
    "URNLex",
    "carregar_norma",
    "citar",
    "extrair_remissoes",
    "parse_articulacao",
    "parse_urn",
]
