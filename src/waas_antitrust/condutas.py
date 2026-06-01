"""Catálogo de condutas anticompetitivas em mercados digitais × atores internos.

EXPLORATÓRIO (R08). Cada conduta canônica tem **atores primários** — papéis
dentro da firma que mais frequentemente executam/sabem da conduta e que, sob o
WaaS, teriam incentivo material a denunciá-la.

Catalogo inicial baseado em decisões/processos paradigmáticos do CADE, DOJ/FTC,
UE-DMA, KFTC e UK CMA. Refinar com pesquisa específica do mercado brasileiro
(ver `docs/DECISIONS.md`, R08).

A função `observabilidade` é o "lookup" que o `model.step` usa para modular a
taxa de observação de cada trabalhador: um designer "observa" um dark pattern
muito melhor que um corp dev observa uma killer acquisition, e vice-versa.
"""

from __future__ import annotations

from dataclasses import dataclass

#: Papéis padronizados. "outro" cobre RH/financeiro/operações etc. com
#: observabilidade baixa em todas as condutas digitais.
PAPEIS_PADRAO: tuple[str, ...] = (
    "eng",
    "produto",
    "design",
    "growth",
    "comercial",
    "juridico",
    "corpdev",
    "outro",
)

#: Distribuição padrão (aproxima big tech madura; calibrar em R03).
DISTRIBUICAO_PAPEIS_PADRAO: dict[str, float] = {
    "eng": 0.30,
    "produto": 0.15,
    "design": 0.10,
    "growth": 0.10,
    "comercial": 0.10,
    "juridico": 0.05,
    "corpdev": 0.05,
    "outro": 0.15,
}


@dataclass(frozen=True)
class Conduta:
    """Tipo de conduta anticompetitiva digital com seu executor típico."""

    nome: str
    descricao: str
    atores_primarios: tuple[str, ...]
    severidade_base: float
    casos_referencia: tuple[str, ...] = ()


#: Catálogo canônico (7 condutas). Ordem não importa.
CATALOGO: tuple[Conduta, ...] = (
    Conduta(
        nome="self_preferencing",
        descricao="Autopreferenciamento de produto próprio em marketplace/busca.",
        atores_primarios=("eng", "produto"),
        severidade_base=0.7,
        casos_referencia=("Google Shopping (UE 2017)", "Amazon Buy Box (UE 2022)"),
    ),
    Conduta(
        nome="tying_bundling",
        descricao="Vinculação de produtos para forçar compra conjunta.",
        atores_primarios=("produto", "comercial"),
        severidade_base=0.6,
        casos_referencia=("Microsoft Windows-Media Player", "Apple App Store"),
    ),
    Conduta(
        nome="predatory_pricing",
        descricao="Preços abaixo do custo para excluir concorrentes em adjacência.",
        atores_primarios=("growth", "eng"),
        severidade_base=0.8,
        casos_referencia=("Uber 2014-2019", "iFood vs concorrentes"),
    ),
    Conduta(
        nome="killer_acquisitions",
        descricao="Aquisição de concorrente nascente para neutralizar competição.",
        atores_primarios=("corpdev", "juridico"),
        severidade_base=0.9,
        casos_referencia=("Meta-Instagram (2012)", "Meta-WhatsApp (2014)"),
    ),
    Conduta(
        nome="dark_patterns",
        descricao="Design de interface que dificulta saída ou induz consentimento.",
        atores_primarios=("design", "produto"),
        severidade_base=0.5,
        casos_referencia=("Amazon Prime cancelamento (FTC 2023)", "Facebook ad opt-out"),
    ),
    Conduta(
        nome="acesso_api_dados",
        descricao="Discriminação no acesso a API ou dados prejudicando concorrentes.",
        atores_primarios=("eng", "produto"),
        severidade_base=0.7,
        casos_referencia=("Twitter API 2023", "Google Maps embargos"),
    ),
    Conduta(
        nome="mfn_paridade",
        descricao="Paridade obrigando vendedor a não cobrar menos em outros canais.",
        atores_primarios=("comercial", "juridico"),
        severidade_base=0.6,
        casos_referencia=("Booking.com (UE 2015)", "Amazon Marketplace"),
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
    peso_outro: float = 0.2,
) -> float:
    """Quanto um funcionário do `papel` consegue observar a `conduta`.

    Padrão: atores primários ⇒ peso 1.0; demais ⇒ peso 0.2. Provisional;
    calibrar em R03 com survey/literatura.
    """
    if papel in conduta.atores_primarios:
        return peso_primario
    return peso_outro
