"""Paleta cromática unificada e estilo padrão."""

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


def aplicar_estilo() -> None:
    """Aplica o estilo padrão das figuras do artigo."""
    sns.set_theme(style="white", context="paper", font_scale=1.0)
    plt.rcParams["figure.dpi"] = 110
    plt.rcParams["savefig.dpi"] = 150
    plt.rcParams["font.family"] = "DejaVu Sans"
