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

# Paleta acadêmica sóbria (jun/2026). Substitui o verde/roxo/âmbar
# saturados por tons de baixa saturação em escala grafite-azul, no
# registro de figura de periódico. Mantém distinção daltonismo-amigável
# (luminâncias separadas) reforçada por MARCADORES e HACHURAS.
PALETA = {
    "A": "#9aa5b1",  # cinza-azulado claro · Regime A (situação atual)
    "B": "#1f4e5f",  # azul-petróleo escuro · Regime B (Resolução)
    "C": "#4b3f6b",  # roxo-grafite · Regime C (Lei)
    "adv": "#8c3b3b",  # vermelho-tijolo sóbrio · cenários adversariais
    "cade": "#8a6d3b",  # mostarda escura · série histórica CADE
    "neutro_escuro": "#2d3748",
    "neutro_claro": "#edf0f3",
    "destaque": "#2c5f6f",
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
