"""Painel micro — tela de simulação para UMA firma específica (v2.H).

Complementa `painel_macro.py`: enquanto o macro agrega sistema-todo, o
micro mostra **o que acontece dentro de uma firma**. Útil para:
- Entender por que/quando uma firma forma massa crítica enquanto outras não.
- Inspecionar a distribuição de arquétipos e papéis numa firma.
- Validar a corrida intra-firma (R20) sob `modo_corrida=True`.

Estrutura: painel 2×2 matplotlib que combina:
  (a) trabalhadores que sinalizaram, por arquétipo
  (b) trabalhadores que sinalizaram, por papel
  (c) trajetória da firma — eh_violadora ao longo dos tiques (binário)
  (d) posições de cooperação interna na fila (LCMC), se modo_corrida
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from waas_antitrust.viz.paleta import PALETA, aplicar_estilo

if TYPE_CHECKING:
    from waas_antitrust.model import WaaSModel


def gerar_figura(modelo: WaaSModel, fid: int = 0) -> tuple[Figure, list[Axes]]:
    """Painel micro 2×2 para a firma `fid` num `WaaSModel` já executado.

    Parameters
    ----------
    modelo : WaaSModel
        Instância já com `.executar()` chamado.
    fid : int
        Índice da firma a inspecionar (default 0).

    Returns
    -------
    (Figure, list[Axes])
    """
    aplicar_estilo()

    if fid not in modelo.trabalhadores_por_empresa:
        raise ValueError(
            f"firma {fid} não existe em modelo; firmas disponíveis: "
            f"{list(modelo.trabalhadores_por_empresa.keys())[:5]}..."
        )

    trabalhadores = modelo.trabalhadores_por_empresa[fid]
    empresa = modelo.empresas[fid]

    fig, axes = plt.subplots(2, 2, figsize=(10, 6.5))
    ax_arq, ax_pap, ax_viol, ax_fila = axes.flatten()

    # (a) Sinalizadores por arquétipo (snapshot do último tique).
    arq_counter: dict[str, int] = {}
    arq_sinaliza: dict[str, int] = {}
    for t in trabalhadores:
        arq_counter[t.arquetipo] = arq_counter.get(t.arquetipo, 0) + 1
        if t.sinaliza_agora:
            arq_sinaliza[t.arquetipo] = arq_sinaliza.get(t.arquetipo, 0) + 1
    arqs = sorted(arq_counter.keys())
    total = [arq_counter[a] for a in arqs]
    sinaliza = [arq_sinaliza.get(a, 0) for a in arqs]
    x_pos = range(len(arqs))
    ax_arq.bar(x_pos, total, color=PALETA["neutro_claro"], label="população")
    ax_arq.bar(x_pos, sinaliza, color=PALETA["B"], label="sinalizou")
    ax_arq.set_xticks(list(x_pos))
    ax_arq.set_xticklabels(arqs, rotation=30, ha="right", fontsize=8)
    ax_arq.set_title("(a) Sinalizadores por arquétipo", fontsize=10, loc="left")
    ax_arq.set_ylabel("trabalhadores")
    ax_arq.legend(fontsize=8)

    # (b) Sinalizadores por papel (R08).
    pap_counter: dict[str, int] = {}
    pap_sinaliza: dict[str, int] = {}
    for t in trabalhadores:
        pap_counter[t.papel] = pap_counter.get(t.papel, 0) + 1
        if t.sinaliza_agora:
            pap_sinaliza[t.papel] = pap_sinaliza.get(t.papel, 0) + 1
    paps = sorted(pap_counter.keys())
    total_p = [pap_counter[p] for p in paps]
    sinaliza_p = [pap_sinaliza.get(p, 0) for p in paps]
    x_pos_p = range(len(paps))
    ax_pap.bar(x_pos_p, total_p, color=PALETA["neutro_claro"], label="população")
    ax_pap.bar(x_pos_p, sinaliza_p, color=PALETA["C"], label="sinalizou")
    ax_pap.set_xticks(list(x_pos_p))
    ax_pap.set_xticklabels(paps, rotation=30, ha="right", fontsize=8)
    ax_pap.set_title(
        f"(b) Sinalizadores por papel — conduta: {empresa.conduta_potencial or 'n/a'}",
        fontsize=10,
        loc="left",
    )
    ax_pap.set_ylabel("trabalhadores")
    ax_pap.legend(fontsize=8)

    # (c) Estado da firma — eh_violadora hoje + notificada.
    estados = [
        ("violadora?", empresa.eh_violadora),
        ("notificada?", empresa.notificada_no_periodo),
        (
            "massa crítica\ninterna?",
            getattr(empresa, "massa_critica_interna_satisfeita", False),
        ),
        ("TCC assinado?", empresa.tcc_assinado),
    ]
    rotulos = [e[0] for e in estados]
    valores = [int(e[1]) for e in estados]
    ax_viol.barh(
        rotulos,
        valores,
        color=[PALETA["adv"] if v else PALETA["neutro_claro"] for v in valores],
    )
    ax_viol.set_xlim(0, 1)
    ax_viol.set_xticks([0, 1])
    ax_viol.set_xticklabels(["Não", "Sim"])
    ax_viol.set_title(f"(c) Estado da firma {fid}", fontsize=10, loc="left")

    # (d) Fila intra-firma (LCMC R20).
    if (
        getattr(modelo, "modo_corrida", False)
        and hasattr(modelo, "filas_internas")
        and fid in modelo.filas_internas
    ):
        fila = modelo.filas_internas[fid]
        if hasattr(fila, "cooperadores") and fila.cooperadores:
            posicoes = list(range(1, len(fila.cooperadores) + 1))
            tiques_coop = [t for _, t in fila.cooperadores]
            ax_fila.scatter(
                posicoes,
                tiques_coop,
                color=PALETA["destaque"],
                s=80,
                zorder=3,
            )
            ax_fila.set_xlabel("Posição na fila intra-firma")
            ax_fila.set_ylabel("Tique de cooperação")
            ax_fila.set_title(
                f"(d) Fila intra-firma (LCMC) — {len(posicoes)} cooperadores",
                fontsize=10,
                loc="left",
            )
            ax_fila.grid(True, alpha=0.25, linestyle=":")
        else:
            ax_fila.text(
                0.5,
                0.5,
                "Nenhum cooperador interno\n(massa crítica não atingida)",
                ha="center",
                va="center",
                fontsize=10,
            )
            ax_fila.set_title("(d) Fila intra-firma (LCMC) — vazia", fontsize=10, loc="left")
    else:
        ax_fila.text(
            0.5,
            0.5,
            "modo_corrida=False\n(usar LCMC para popular esta tela)",
            ha="center",
            va="center",
            fontsize=10,
        )
        ax_fila.set_title("(d) Fila intra-firma (LCMC) — inativa", fontsize=10, loc="left")

    fig.suptitle(
        f"Painel micro — comportamento intra-firma (firma {fid})",
        fontsize=12,
        y=0.995,
    )
    fig.tight_layout()
    return fig, [ax_arq, ax_pap, ax_viol, ax_fila]
