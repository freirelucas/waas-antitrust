"""Visualizações modulares.

Implementadas (15 módulos): `inversao`, `fase`, `cascata`, `erosao`,
`painel_macro`, `painel_micro`, `proposicao_5`, `multiplicidade_unicidade`,
`alpha_erosao_limiar`, `sankey`, `bootstrap`, `internacional`, `cade`,
`adversarial`, e o suporte cromático `paleta`. Cada submódulo implementado
expõe uma função `gerar_figura(...)` que retorna `(fig, ax)` ou
`(fig, axes)` do matplotlib.

Em backlog T01 (`docs/DECISIONS.md`; ver `docs/roadmap_figuras.md` para
o status visual público): `painel`, `falsificacao`, `variedade` — esses
3 módulos hoje contêm apenas o stub que levanta `NotImplementedError`;
a implementação canônica vive no caderno `notebooks/WaaS_caderno_v2.ipynb`.
"""

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

__all__ = ["PALETA", "aplicar_estilo"]
