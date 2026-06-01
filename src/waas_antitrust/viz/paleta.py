"""Paleta cromática unificada e estilo padrão.

Categoria 6 (Designer, crítica x10):

- Mapas de cor de figuras conceituais migrados de `RdYlGn` (pior caso para
  daltonismo vermelho-verde) para `cividis`/`viridis` (cego-amigáveis e com
  ordenação perceptual estável).
- Marcadores por regime (`MARCADORES`) e padrões de hachura (`HACHURAS`)
  para reforçar a distinção de séries além da cor — atende o princípio de
  redundância sensorial (Wong 2011, *Nat Methods*).
"""

import matplotlib.pyplot as plt
import seaborn as sns

PALETA = {
    "A": "#5D6D7E",  # cinza-azulado · Regime A (situação atual)
    "B": "#27AE60",  # verde · Regime B (Resolução)
    "C": "#8E44AD",  # roxo · Regime C (Lei)
    "adv": "#C0392B",  # vermelho · cenários adversariais
    "cade": "#D68910",  # âmbar · série histórica CADE
    "neutro_escuro": "#2C3E50",
    "neutro_claro": "#ECF0F1",
    "destaque": "#16A085",
}

#: Marcadores por regime — redundância sensorial além da cor.
MARCADORES: dict[str, str] = {
    "A": "o",  # círculo
    "B": "s",  # quadrado
    "C": "^",  # triângulo
}

#: Padrões de hachura por regime para áreas/barras preenchidas.
HACHURAS: dict[str, str] = {
    "A": "",
    "B": "//",
    "C": "..",
}

#: Mapa de cor padrão para figuras conceituais (cego-amigável).
CMAP_CONCEITUAL: str = "cividis"


def aplicar_estilo() -> None:
    """Aplica o estilo padrão das figuras do artigo."""
    sns.set_theme(style="white", context="paper", font_scale=1.0)
    plt.rcParams["figure.dpi"] = 110
    plt.rcParams["savefig.dpi"] = 150
    plt.rcParams["font.family"] = "DejaVu Sans"
