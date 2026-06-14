"""Visualizações modulares.

20 módulos implementados (T01 fechado em jun/2026 + 2 figuras de
auditoria adicionadas para refletir conteúdo do código no site):
`inversao`, `fase`, `cascata`, `erosao`, `painel_macro`, `painel_micro`,
`proposicao_5`, `multiplicidade_unicidade`, `alpha_erosao_limiar`,
`sankey`, `bootstrap`, `internacional`, `cade`, `adversarial`,
`falsificacao`, `variedade`, `painel` (figura-síntese 2×3), `choques`
(R19 — 5 catálogos canônicos), `identificabilidade` (R03 — 175 rodadas
1D que dissolveram o "conflito de 3 alvos"), e o suporte cromático
`paleta`. Cada submódulo expõe uma função `gerar_figura(...)` que
retorna `(fig, ax)` ou `(fig, axes)` do matplotlib. Mapa figura →
página em `docs/roadmap_figuras.md`.
"""

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

__all__ = ["PALETA", "aplicar_estilo"]
