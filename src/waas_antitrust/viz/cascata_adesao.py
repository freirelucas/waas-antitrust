"""§R29 — Janela de adesão pós-abertura com desconto progressivo por classe.

Quando uma firma atinge massa crítica e seu escrow é aberto, abre-se uma
janela de `janela_adesao_pos_abertura` tiques durante a qual trabalhadores
da MESMA firma podem aderir à classe dos lenientes. Quem chega primeiro
recebe desconto maior; quem não aderir até o fim da janela permanece no
escrow comum.

A figura mostra dois painéis complementares:

(A) **Gradiente de desconto por posição na fila pós-abertura**, com a
    faixa 0 (depositantes originais, imunidade total) destacada à esquerda
    e faixas 1..N (aderentes) descendo até o piso (default 10%).

(B) **Acumulação temporal de aderentes ao longo da janela de 10 tiques**:
    contraste entre uma firma com cascata forte (faixas altas atraem muitos
    aderentes nos primeiros tiques) e uma com adesão lenta (poucos
    candidatos com IR-W positiva nas faixas mais baixas).

Espelha a fila clássica do Art. 86 Lei 12.529/2011 (Spagnolo 2004),
operada DENTRO da firma já aberta — incentivo de cascata pós-coordenação.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo


def gerar_figura(
    descontos: tuple[float, ...] = (1.0, 0.7, 0.5, 0.3, 0.1),
    janela: int = 10,
    n_aderentes_cascata_forte: int = 28,
    n_aderentes_cascata_fraca: int = 6,
    seed: int = 2026,
) -> tuple[Figure, Axes]:
    """Janela de adesão progressiva — figura conceitual em dois painéis.

    Parameters
    ----------
    descontos : tuple[float, ...]
        Fatores de desconto por faixa (posição 0..N-1 na fila pós-abertura).
        Default `(1.0, 0.7, 0.5, 0.3, 0.1)` — faixa 0 = imunidade total
        (depositantes originais que dispararam a massa crítica); faixas
        1..N-1 = aderentes na janela.
    janela : int
        Tamanho da janela de adesão em tiques (default 10).
    n_aderentes_cascata_forte : int
        Total de aderentes no cenário de cascata forte (default 28).
    n_aderentes_cascata_fraca : int
        Total no cenário de cascata fraca (default 6).
    seed : int
        Semente para o jitter temporal da curva de adesão.

    Returns
    -------
    (Figure, Axes)
        Padrão `gerar_figura()` para inclusão no paper/site.
    """
    aplicar_estilo()
    rng = np.random.default_rng(seed)

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13, 5.2))

    # -------- (A) Gradiente de desconto por faixa --------
    posicoes = np.arange(len(descontos))
    rotulos_faixa = [f"Faixa {k}" for k in posicoes]
    # Cores: faixa 0 destaca (verde LCMC); faixas 1..N gradiente cividis
    # decrescente — sinaliza "quanto mais tarde aderir, menor o desconto".
    cores = [PALETA["B"]]
    cmap = plt.get_cmap("cividis_r")
    for k in range(1, len(descontos)):
        cores.append(cmap((k - 1) / max(1, len(descontos) - 2)))

    barras = ax_a.bar(
        posicoes,
        [d * 100 for d in descontos],
        color=cores,
        edgecolor=PALETA["neutro_escuro"],
        linewidth=0.8,
    )
    for k, b in enumerate(barras):
        rotulo = f"{descontos[k] * 100:.0f}%"
        ax_a.text(
            b.get_x() + b.get_width() / 2,
            b.get_height() + 2,
            rotulo,
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold" if k == 0 else "normal",
        )
    ax_a.set_xticks(posicoes)
    ax_a.set_xticklabels(rotulos_faixa)
    ax_a.set_ylim(0, 115)
    ax_a.set_ylabel("Fator de desconto sobre $W$ (%)")
    ax_a.set_xlabel("Posição na fila pós-abertura")
    ax_a.set_title(
        "(A) Gradiente de classes de leniência\n"
        "Faixa 0 = depositantes originais (imunidade); 1..N = aderentes",
        fontsize=11,
        loc="left",
    )
    # Anota a faixa 0 com a tag "imunidade"
    ax_a.annotate(
        "imunidade total\n(massa crítica disparou)",
        xy=(0, 100),
        xytext=(1.0, 95),
        fontsize=9,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", color=PALETA["neutro_escuro"], lw=0.8),
        color=PALETA["neutro_escuro"],
    )
    ax_a.spines[["top", "right"]].set_visible(False)
    ax_a.grid(axis="y", alpha=0.3, linestyle=":")

    # -------- (B) Curva temporal de adesão na janela --------
    tiques = np.arange(janela + 1)

    def curva_cumulativa(n_total: int, k_meio: float) -> np.ndarray:
        """Sigmoide cumulativa truncada em (0, n_total)."""
        x = tiques - k_meio
        sig = 1.0 / (1.0 + np.exp(-x * 0.9))
        # Normaliza para iniciar em 0 e terminar em ~n_total
        sig = (sig - sig.min()) / max(1e-9, (sig.max() - sig.min()))
        ruido = rng.normal(0, 0.5, size=tiques.shape)
        return np.clip(np.round(sig * n_total + ruido), 0, None)

    forte = curva_cumulativa(n_aderentes_cascata_forte, 2.0)
    fraca = curva_cumulativa(n_aderentes_cascata_fraca, 6.0)
    # Garante monotonicidade (curva cumulativa não decresce).
    forte = np.maximum.accumulate(forte)
    fraca = np.maximum.accumulate(fraca)

    ax_b.step(tiques, forte, where="post", color=PALETA["B"], lw=2.4, label="Cascata forte")
    ax_b.step(tiques, fraca, where="post", color=PALETA["adv"], lw=2.0, label="Cascata fraca")
    ax_b.fill_between(tiques, forte, step="post", color=PALETA["B"], alpha=0.15)
    ax_b.fill_between(tiques, fraca, step="post", color=PALETA["adv"], alpha=0.15)

    ax_b.axvline(janela, color=PALETA["neutro_escuro"], lw=1.0, ls="--", alpha=0.7)
    ax_b.text(
        janela - 0.15,
        max(forte.max(), fraca.max()) * 0.96,
        "fim da janela",
        ha="right",
        va="top",
        fontsize=9,
        color=PALETA["neutro_escuro"],
        rotation=90,
    )

    ax_b.set_xlabel(f"Tiques desde a abertura (janela = {janela})")
    ax_b.set_ylabel("Aderentes acumulados na firma")
    ax_b.set_title(
        "(B) Cascata temporal de adesão pós-abertura\n"
        "IR-W positiva nas faixas altas ⇒ adesão concentrada cedo",
        fontsize=11,
        loc="left",
    )
    ax_b.legend(loc="lower right", frameon=False)
    ax_b.spines[["top", "right"]].set_visible(False)
    ax_b.grid(alpha=0.3, linestyle=":")
    ax_b.set_xlim(0, janela + 0.5)

    fig.suptitle(
        "R29 — Janela de adesão pós-abertura com desconto progressivo por classe",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    fig.tight_layout()
    return fig, ax_a
