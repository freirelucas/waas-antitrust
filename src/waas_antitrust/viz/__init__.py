"""Visualizações modulares.

Apenas `inversao` e `fase` estão implementadas como módulo; as demais
permanecem no caderno (backlog T01 em docs/DECISIONS.md). Cada submódulo
implementado expõe uma função `gerar_figura(...)` que retorna uma tupla
`(fig, ax)` ou `(fig, axes)` do matplotlib.
"""

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

__all__ = ["PALETA", "aplicar_estilo"]
