"""Visualizações modulares.

22 módulos implementados (T01 fechado em jun/2026 + R29 e R30 em
jun/2026): `inversao`, `fase`, `cascata`, `erosao`, `painel_macro`,
`painel_micro`, `proposicao_5`, `multiplicidade_unicidade`,
`alpha_erosao_limiar`, `sankey`, `bootstrap`, `internacional`, `cade`,
`adversarial`, `falsificacao`, `variedade`, `painel` (figura-síntese
2×3), `choques` (R19 — 5 catálogos canônicos), `identificabilidade`
(R03 — 175 rodadas 1D que dissolveram o "conflito de 3 alvos"),
`cascata_adesao` (R29 — janela de adesão pós-abertura com desconto
progressivo), `sinergia_internacional` (R30 — adoção coordenada LCMC
por múltiplas autoridades), e o suporte cromático `paleta`. Cada
submódulo expõe uma função `gerar_figura(...)` que retorna
`(fig, ax)` ou `(fig, axes)` do matplotlib. Mapa figura → página em
`docs/roadmap_figuras.md`.
"""

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

__all__ = ["PALETA", "aplicar_estilo"]
