"""Onze visualizações modulares.

Cada submódulo expõe uma função `gerar_figura(...)` que retorna uma tupla
`(fig, ax)` ou `(fig, axes)` do matplotlib.
"""

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

__all__ = ["PALETA", "aplicar_estilo"]
