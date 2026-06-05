"""Parser de texto articulado conforme LC 95/1998.

A Lei Complementar 95/1998 (técnica de elaboração legislativa)
codifica a hierarquia de dispositivos:

    Artigo  →  Parágrafos (numerados ou parágrafo único)
            →  Incisos (I, II, III, ...)
            →  Alíneas (a), b), c), ...)
            →  Itens (1, 2, 3, ...)

Este módulo provê um parser **regex disciplinado** que decompõe texto
articulado em uma árvore de `Dispositivo` — auditável, finito,
suficiente para as três normas-base do WaaS (Lei 12.529, Lei 13.608,
Resolução CADE 21/2018).

Casos patológicos NÃO cobertos (documentados; rejeitam-se com
mensagem clara em vez de falhar silenciosamente):

- Notas marginais ou subseções entre dispositivos.
- Citações longas que ultrapassem múltiplos dispositivos.
- Numeração não-padrão (e.g., "Art. 4º-A" — coberta; mas "Art. 4-bis" não).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ----- Regex de início de dispositivo --------------------------------

# Artigo: "Art. 1º", "Art. 12", "Art. 4º-A", "Art. 86, § 7º" (este último
# fica fora — capturamos só a abertura).
_ART = re.compile(
    r"^\s*Art\.\s*(?P<numero>\d+(?:º)?(?:-[A-Z])?)\s*[.\-º]?\s*",
)

# Parágrafo: "§ 1º", "§ 2º", "Parágrafo único".
_PAR_NUM = re.compile(r"^\s*§\s*(?P<numero>\d+)\s*[º°]?\s*[.\-]?\s*")
_PAR_UNICO = re.compile(r"^\s*Parágrafo\s+único\s*[.\-]?\s*", re.IGNORECASE)

# Inciso: "I -", "II -", "I –", "I.".
_INCISO = re.compile(
    r"^\s*(?P<numero>[IVXLCDM]+)\s*[\-–.]\s*",
)

# Alínea: "a)", "b)", ...
_ALINEA = re.compile(r"^\s*(?P<letra>[a-z])\)\s*")

# Item (raro): "1.", "2.", ..., distintos de inciso.
_ITEM = re.compile(r"^\s*(?P<numero>\d+)\.\s*")


@dataclass
class Dispositivo:
    """Unidade hierárquica de uma norma articulada."""

    tipo: str  # "artigo" | "paragrafo" | "inciso" | "alinea" | "item" | "preambulo"
    rotulo: str  # "Art. 12", "§ 1º", "Parágrafo único", "I", "a"
    texto: str
    filhos: list[Dispositivo] = field(default_factory=list)

    def caminho(self) -> str:
        """Identificador concatenado, ex.: 'Art. 86 § 7º' (sem filhos)."""
        return self.rotulo


def _classificar_linha(linha: str) -> tuple[str, str, str] | None:
    """Devolve (tipo, rotulo, resto_da_linha) se a linha inicia dispositivo."""
    m = _ART.match(linha)
    if m:
        n = m.group("numero")
        rotulo = f"Art. {n}"
        return ("artigo", rotulo, linha[m.end() :])
    m = _PAR_UNICO.match(linha)
    if m:
        return ("paragrafo", "Parágrafo único", linha[m.end() :])
    m = _PAR_NUM.match(linha)
    if m:
        rotulo = f"§ {m.group('numero')}º"
        return ("paragrafo", rotulo, linha[m.end() :])
    m = _INCISO.match(linha)
    if m:
        return ("inciso", m.group("numero"), linha[m.end() :])
    m = _ALINEA.match(linha)
    if m:
        return ("alinea", m.group("letra"), linha[m.end() :])
    m = _ITEM.match(linha)
    if m:
        return ("item", m.group("numero"), linha[m.end() :])
    return None


def parse_articulacao(texto: str) -> list[Dispositivo]:
    """Decompõe `texto` articulado numa lista de `Dispositivo` (raízes).

    Cada raiz é tipicamente um artigo (`Art. N`). Parágrafos, incisos
    e alíneas viram filhos por encaixe hierárquico.

    O parser opera linha a linha (texto pré-quebrado em `\n`) e mantém
    uma pilha de níveis. Linhas que não iniciam dispositivo são
    anexadas ao texto do dispositivo corrente (continuação).
    """
    raizes: list[Dispositivo] = []
    pilha: list[Dispositivo] = []
    # Hierarquia: artigo > paragrafo > inciso > alinea > item.
    nivel = {"artigo": 0, "paragrafo": 1, "inciso": 2, "alinea": 3, "item": 4}

    for linha_bruta in texto.splitlines():
        linha = linha_bruta.strip()
        if not linha:
            continue
        c = _classificar_linha(linha)
        if c is None:
            if pilha:
                pilha[-1].texto = (pilha[-1].texto + " " + linha).strip()
            continue
        tipo, rotulo, resto = c
        novo = Dispositivo(tipo=tipo, rotulo=rotulo, texto=resto.strip())
        n_novo = nivel[tipo]
        # Desempilha enquanto o topo for de nível >= novo.
        while pilha and nivel[pilha[-1].tipo] >= n_novo:
            pilha.pop()
        if pilha:
            pilha[-1].filhos.append(novo)
        else:
            raizes.append(novo)
        pilha.append(novo)

    return raizes


def buscar_dispositivo(raizes: list[Dispositivo], caminho: str) -> Dispositivo | None:
    """Localiza um dispositivo pelo seu rótulo no nível superior.

    Suporta busca direta por rótulo de artigo (e.g., `"Art. 85"`) ou
    composto (e.g., `"Art. 86 § 7º"`).
    """
    partes = [p.strip() for p in caminho.split("§")]
    rotulo_art = partes[0].strip()
    artigo = next((r for r in raizes if r.tipo == "artigo" and r.rotulo == rotulo_art), None)
    if artigo is None or len(partes) == 1:
        return artigo
    # Buscar parágrafo no artigo.
    rotulo_par = "§ " + partes[1].strip()
    return next(
        (f for f in artigo.filhos if f.tipo == "paragrafo" and f.rotulo == rotulo_par),
        None,
    )
