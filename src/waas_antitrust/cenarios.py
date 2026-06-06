"""Cenários normativos como variantes paramétricas (R17, exploratório).

Cada cenário aqui é um **conjunto de alterações regulatórias** que altera
parâmetros do `WaaSModel`. A motivação vem da crítica do autor: tratar
alterações normativas como **cenários comparáveis**, não como notas de
rodapé textuais.

Os sete cenários cobrem o espectro de:

- **Status quo** (Regime A, sem qualquer alteração);
- **Resolução pura** (Regime B atual — Art. 12 da Res. CADE 21/2018);
- **Resolução + portaria MTE** (B com proteção trabalhista reforçada);
- **Lei WaaS pura** (Regime C — extensão da Lei 13.608/2018);
- **Lei WaaS com fundo público de honorários** (Estado paga advogado);
- **Lei WaaS com cláusula padrão de vesting acelerado** (Hirschman R07);
- **Sanção catastrófica** (qualquer regime + multa por descumprimento do TCC).

Cada cenário é um dict de **sobrescritas** de parâmetros — aplicar via
`aplicar_cenario(params, cenario_id)` produz um novo `WaaSParametros` com
as alterações em vigor.

Referências teóricas que motivam essa modularidade:
- Torsell (2026) sobre inequity aversion e evolução de preferências;
- Skyrms (1996) sobre evolução do contrato social;
- Bolton & Ockenfels (2000) sobre ERC.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from waas_antitrust.calibracao.saito import d_base_tcc_calibrado

if TYPE_CHECKING:
    from waas_antitrust.model import WaaSParametros


# Fonte única para o desconto base do TCC clássico (Lei 12.529/2011, Art. 85).
# Consulta `calibracao/saito.py`: usa Saito (2021) se preenchido, ou cai para
# o default histórico documentado (0,10). Quando a extração manual da tabela
# principal de Saito for concluída, todos os cenários abaixo herdam o valor
# real sem mudança neste módulo.
_D_BASE_TCC: float = d_base_tcc_calibrado(default=0.10)


@dataclass(frozen=True)
class Cenario:
    """Alteração normativa pré-empacotada.

    `descricao` é a interpretação institucional do cenário; `sobrescritas`
    são os campos de `WaaSParametros` que mudam ao aplicar.
    """

    nome: str
    descricao: str
    sobrescritas: dict[str, object] = field(default_factory=dict)


#: Distribuição de arquétipos calibrada para ativar fairminded sob R16.
#: Mantém Hokamp-Pickhardt como núcleo (~75% do peso) e dá 20% ao FM.
DISTRIBUICAO_COM_FAIRMINDED: dict[str, float] = {
    "ético": 0.10,
    "imitativo": 0.30,
    "racional": 0.30,
    "fairminded": 0.20,
    "aleatório": 0.10,
}


#: Sete cenários canônicos para varredura comparativa.
CATALOGO_CENARIOS: tuple[Cenario, ...] = (
    Cenario(
        nome="status_quo",
        descricao=(
            "Regime A — situação atual brasileira, sem canal de incentivo "
            "individual ao denunciante interno em antitruste."
        ),
        sobrescritas={"regime": "A"},
    ),
    Cenario(
        nome="resolucao_pura",
        descricao=(
            "Regime B — nova Resolução CADE complementar à 21/2018, sem "
            "mudar a lei. Re-caracterização da recompensa como ressarcimento "
            "extrajudicial sob Art. 12; risco F6 (anulação judicial) presente."
        ),
        sobrescritas={
            "regime": "B",
            "D_disc_base_tcc": _D_BASE_TCC,  # Saito 2021 quando disponível; senão 0,10
            "p_anulacao_tcc": 0.10,  # F6 calibrado moderadamente
        },
    ),
    Cenario(
        nome="resolucao_mais_portaria_mte",
        descricao=(
            "Regime B + portaria MTE que reforça proteção trabalhista contra "
            "represália por denúncia coletiva. Reduz tolerância à represália "
            "(trabalhador percebe ambiente mais seguro) e custo legal."
        ),
        sobrescritas={
            "regime": "B",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.10,
            "r_represalia": 0.08,  # caiu de 0.15 padrão
            "custo_legal_uw": 0.15,  # caiu por proteção trabalhista
        },
    ),
    Cenario(
        nome="lei_waas_pura",
        descricao=(
            "Regime C — extensão da Lei 13.608/2018 (com a redação da Lei "
            "13.964/2019) ao enforcement antitruste, com percentual explícito "
            "de recompensa. Robustez jurídica plena; sem risco F6."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,  # F6 eliminado: lei é robusta
            "custo_legal_uw": 0.30,  # ainda há custo, mas defesa legal facilitada
        },
    ),
    Cenario(
        nome="lei_waas_com_fundo_honorarios",
        descricao=(
            "Regime C + fundo público de honorários advocatícios (análogo ao "
            "IRS Whistleblower Office americano). Estado financia a defesa do "
            "denunciante; custo legal individual ~0. Politicamente custoso."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "custo_legal_uw": 0.05,  # quase zero — fundo cobre quase tudo
            "prob_pagamento_perc": 0.95,  # fundo aumenta credibilidade
        },
    ),
    Cenario(
        nome="lei_waas_com_vesting_padrao",
        descricao=(
            "Regime C + cláusula padrão de vesting acelerado por gatilho de "
            "ação coletiva (Hirschman exit-with-equity R07 universal). "
            "Acrescenta canal de êxodo coletivo à IC-F* da firma."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "custo_legal_uw": 0.20,
            "fracao_contratos_acelerados": 1.0,  # universal por desenho
            "aliquota_tributaria_vesting": 0.40,  # IRPF + INSS realistas
        },
    ),
    Cenario(
        nome="mercado_digital_br_pareto",
        descricao=(
            "Regime C com **fatia de mercado distribuída em Pareto** (α=1,16). "
            "Reflete a realidade de mercados digitais brasileiros: dano "
            "concentrado em uma cauda longa de plataformas dominantes "
            "(iFood, Mercado Livre, Apple/Google), não distribuído "
            "uniformemente. R13a do backlog."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "custo_legal_uw": 0.20,
            "distribuicao_fatia_mercado": "pareto",
            "alpha_pareto": 1.16,  # regra 80/20 clássica
        },
    ),
    Cenario(
        nome="cenario_sancao_dura",
        descricao=(
            "Regime C + sanção catastrófica por descumprimento do TCC: firma "
            "que assina e depois não cumpre paga multa adicional 2× a sanção "
            "base. Captura 'se a empresa não cumpre, perde tudo' e fortalece "
            "o commitment da firma (R18)."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "custo_legal_uw": 0.20,
            "multa_descumprimento_tcc": 2.0,  # 2× a sanção base como adicional
            "p_descumprimento_tcc": 0.0,  # firma não descumpre porque é severo
            "prob_pagamento_perc": 0.95,  # credibilidade alta
        },
    ),
    Cenario(
        nome="cenario_corrida_leniencia",
        descricao=(
            "Regime C + leniência coletiva interna condicionada (R20). "
            "A firma só ganha atenuante se q_min × n_trabalhadores cooperarem "
            "internamente; desconto da firma e recompensa do trabalhador decaem "
            "com a posição na fila — ambos calibrados contra Saito (2021). "
            "Cria DUAS corridas acopladas: intra-firma e inter-firma. Resposta "
            "à tese substantiva 'mercados digitais têm moat → condutas "
            "unilaterais → corrida só pode ser intra-firma'."
        ),
        sobrescritas={
            "regime": "C",
            "modo_corrida": True,
            "q_min_cooperacao_interna": 0.10,
            "janela_temporal_tiques": 4,
            "perfil_decaimento": "saito",
            "custo_legal_uw": 0.20,
            "prob_pagamento_perc": 0.95,
        },
    ),
)


def lookup_cenario(nome: str) -> Cenario:
    """Localiza um cenário por nome; KeyError se desconhecido."""
    for c in CATALOGO_CENARIOS:
        if c.nome == nome:
            return c
    nomes_validos = ", ".join(c.nome for c in CATALOGO_CENARIOS)
    raise KeyError(f"cenário desconhecido: {nome!r}. Válidos: {nomes_validos}")


def aplicar_cenario(params: WaaSParametros, cenario: str | Cenario) -> WaaSParametros:
    """Retorna um novo `WaaSParametros` com as sobrescritas do cenário.

    Aceita o objeto `Cenario` ou seu nome em string. Não muta o `params`
    original — devolve uma cópia modificada via `dataclasses.replace`.
    """
    from dataclasses import replace

    c = cenario if isinstance(cenario, Cenario) else lookup_cenario(cenario)
    return replace(params, **c.sobrescritas)


def listar_cenarios() -> list[str]:
    """Nomes dos cenários disponíveis, em ordem do catálogo."""
    return [c.nome for c in CATALOGO_CENARIOS]
