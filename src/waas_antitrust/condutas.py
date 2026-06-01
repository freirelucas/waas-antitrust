"""Catálogo de condutas anticompetitivas em mercados digitais × atores internos.

EXPLORATÓRIO (R08). Cada conduta canônica tem **atores primários** — papéis
dentro da firma que mais frequentemente executam/sabem da conduta e que, sob o
WaaS, teriam incentivo material a denunciá-la — e **atores adjacentes**, com
observabilidade intermediária (Categoria 5 da crítica x10, PM: gradiente
3-níveis em vez de binário).

Catálogo baseado em decisões/processos paradigmáticos do CADE (incluindo
casos específicos do mercado brasileiro: iFood TCC 2023, Apple Brasil
anti-steering 2025), DOJ/FTC, UE-DMA, KFTC e UK CMA. Refinar com pesquisa
adicional do mercado brasileiro (ver `docs/DECISIONS.md`, R08, E05).

A função `observabilidade` é o "lookup" que o `model.step` usa para modular a
taxa de observação de cada trabalhador. Padrão de pesos (gradiente Near &
Miceli sobre whistleblowing organizacional):
- ator primário: 1.0 (executa a conduta diretamente)
- ator adjacente: 0.5 (vê o efeito imediato — métricas, decisões, P&L)
- demais: 0.1 (não há vetor estável de observação)
"""

from __future__ import annotations

from dataclasses import dataclass, field

#: Papéis padronizados. "outro" cobre RH/jurídico-tributário/regulação setorial
#: com observabilidade baixa em todas as condutas digitais.
PAPEIS_PADRAO: tuple[str, ...] = (
    "eng",
    "produto",
    "design",
    "growth",
    "comercial",
    "juridico",
    "corpdev",
    "operacoes",
    "financeiro",
    "outro",
)

#: Distribuição BIGTECH_MADURA (Google/Meta/Apple-like): eng-heavy, baixa
#: operações, sem grande financeiro operacional.
BIGTECH_MADURA: dict[str, float] = {
    "eng": 0.30,
    "produto": 0.15,
    "design": 0.10,
    "growth": 0.10,
    "comercial": 0.08,
    "juridico": 0.05,
    "corpdev": 0.05,
    "operacoes": 0.05,
    "financeiro": 0.02,
    "outro": 0.10,
}

#: Distribuição MARKETPLACE_BR (iFood/Mercado Livre-like): operations-heavy,
#: grande gestão comercial de sellers, financeiro com FP&A significativo.
#: Reflete a observação da Categoria 5 (PM): marketplaces brasileiros têm
#: shape organizacional distinto da big tech madura — calibrar formalmente
#: contra organogramas/LinkedIn em E05.
MARKETPLACE_BR: dict[str, float] = {
    "eng": 0.18,
    "produto": 0.08,
    "design": 0.05,
    "growth": 0.08,
    "comercial": 0.15,
    "juridico": 0.04,
    "corpdev": 0.02,
    "operacoes": 0.25,
    "financeiro": 0.05,
    "outro": 0.10,
}

#: Distribuição padrão usada pelo `WaaSModel` quando `params.distribuicao_papeis`
#: é None. Mantida como BIGTECH_MADURA para preservar a calibração existente do
#: catálogo (a maior parte dos casos canônicos é de big tech) — `MARKETPLACE_BR`
#: deve ser passada explicitamente para cenários de marketplace BR.
DISTRIBUICAO_PAPEIS_PADRAO: dict[str, float] = BIGTECH_MADURA


@dataclass(frozen=True)
class Conduta:
    """Tipo de conduta anticompetitiva digital com seu executor típico.

    `atores_primarios`: papéis que executam diretamente (observabilidade 1.0).
    `atores_adjacentes`: papéis que veem efeito imediato — métricas,
    decisões, P&L — sem executar (observabilidade 0.5). Papéis fora dos dois
    conjuntos têm observabilidade distal (0.1, default).
    """

    nome: str
    descricao: str
    atores_primarios: tuple[str, ...]
    severidade_base: float
    atores_adjacentes: tuple[str, ...] = field(default_factory=tuple)
    casos_referencia: tuple[str, ...] = ()


#: Catálogo canônico. Ordem não importa.
CATALOGO: tuple[Conduta, ...] = (
    Conduta(
        nome="self_preferencing",
        descricao="Autopreferenciamento de produto próprio em marketplace/busca.",
        atores_primarios=("eng", "produto"),
        atores_adjacentes=("growth", "comercial"),
        severidade_base=0.7,
        casos_referencia=("Google Shopping (UE 2017)", "Amazon Buy Box (UE 2022)"),
    ),
    Conduta(
        nome="tying_bundling",
        descricao="Vinculação de produtos para forçar compra conjunta.",
        atores_primarios=("produto", "comercial"),
        atores_adjacentes=("juridico", "eng"),
        severidade_base=0.6,
        casos_referencia=("Microsoft Windows-Media Player", "Apple App Store"),
    ),
    Conduta(
        nome="predatory_pricing",
        descricao="Preços abaixo do custo para excluir concorrentes em adjacência.",
        atores_primarios=("growth", "eng"),
        atores_adjacentes=("financeiro", "comercial"),
        severidade_base=0.8,
        casos_referencia=("Uber 2014-2019", "iFood vs concorrentes"),
    ),
    Conduta(
        nome="killer_acquisitions",
        descricao="Aquisição de concorrente nascente para neutralizar competição.",
        atores_primarios=("corpdev", "juridico"),
        atores_adjacentes=("produto", "financeiro"),
        severidade_base=0.9,
        casos_referencia=("Meta-Instagram (2012)", "Meta-WhatsApp (2014)"),
    ),
    Conduta(
        nome="dark_patterns",
        descricao="Design de interface que dificulta saída ou induz consentimento.",
        atores_primarios=("design", "produto"),
        atores_adjacentes=("growth", "eng"),
        severidade_base=0.5,
        casos_referencia=("Amazon Prime cancelamento (FTC 2023)", "Facebook ad opt-out"),
    ),
    Conduta(
        nome="acesso_api_dados",
        descricao="Discriminação no acesso a API ou dados prejudicando concorrentes.",
        atores_primarios=("eng", "produto"),
        atores_adjacentes=("juridico", "comercial"),
        severidade_base=0.7,
        casos_referencia=("Twitter API 2023", "Google Maps embargos"),
    ),
    Conduta(
        nome="mfn_paridade",
        descricao="Paridade obrigando vendedor a não cobrar menos em outros canais.",
        atores_primarios=("comercial", "juridico"),
        atores_adjacentes=("produto", "financeiro"),
        severidade_base=0.6,
        casos_referencia=("Booking.com (UE 2015)", "Amazon Marketplace"),
    ),
    Conduta(
        nome="exclusividade_retaliacao_marketplace",
        descricao=(
            "Exclusividade contratual ou retaliação contra sellers que listam em "
            "concorrentes em marketplace de duas pontas."
        ),
        atores_primarios=("comercial", "operacoes"),
        atores_adjacentes=("juridico", "produto"),
        severidade_base=0.75,
        casos_referencia=(
            "iFood TCC 2023 (exclusividade com restaurantes)",
            "Mercado Livre vs sellers (indícios 2024-2025)",
        ),
    ),
    Conduta(
        nome="anti_steering_iap",
        descricao=(
            "Bloqueio de informação ou redirecionamento de pagamento fora do "
            "in-app purchase do operador de plataforma móvel."
        ),
        atores_primarios=("produto", "eng"),
        atores_adjacentes=("juridico", "comercial"),
        severidade_base=0.7,
        casos_referencia=(
            "Apple Brasil — CADE dez/2025",
            "Epic Games v. Apple (EUA 2021)",
        ),
    ),
)


def lookup_conduta(nome: str) -> Conduta:
    """Localiza uma conduta por nome; levanta KeyError se desconhecida."""
    for c in CATALOGO:
        if c.nome == nome:
            return c
    raise KeyError(f"conduta desconhecida: {nome}")


def observabilidade(
    papel: str,
    conduta: Conduta,
    peso_primario: float = 1.0,
    peso_adjacente: float = 0.5,
    peso_distal: float = 0.1,
) -> float:
    """Quanto um funcionário do `papel` consegue observar a `conduta`.

    Gradiente 3-níveis (Categoria 5 da crítica x10, PM, inspirado em Near &
    Miceli sobre whistleblowing organizacional):

    - ator primário (executa a conduta): peso 1.0
    - ator adjacente (vê efeito imediato): peso 0.5
    - demais (sem vetor de observação): peso 0.1

    Pesos provisionais; calibrar em R03 com survey/literatura específica.
    """
    if papel in conduta.atores_primarios:
        return peso_primario
    if papel in conduta.atores_adjacentes:
        return peso_adjacente
    return peso_distal
