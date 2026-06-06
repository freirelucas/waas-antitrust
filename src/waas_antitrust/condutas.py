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
    # ----- 19 condutas adicionadas via R20 (pesquisa pós-LCMC) -----
    Conduta(
        nome="ranking_demotion_rivais",
        descricao="Degradação algorítmica do ranking de rivais em busca ou feed.",
        atores_primarios=("eng", "produto"),
        atores_adjacentes=("growth",),
        severidade_base=0.65,
        casos_referencia=(
            "Google Shopping (CJUE 10/09/2024)",
            "FTC v. Amazon §VI (EUA 2023)",
        ),
    ),
    Conduta(
        nome="tying_ia_generativa",
        descricao=(
            "Embutir assistente de IA do operador do SO/busca/produtividade "
            "sem opção neutra de escolha."
        ),
        atores_primarios=("produto", "eng"),
        atores_adjacentes=("comercial", "juridico"),
        severidade_base=0.65,
        casos_referencia=(
            "Microsoft Copilot/Bing (EC RFI 2024) [?]",
            "Google Gemini default em Android [?]",
        ),
    ),
    Conduta(
        nome="subsidio_cruzado_ecossistema",
        descricao=(
            "Subsídio de produto em mercado adjacente financiado pelo monopólio "
            "principal do ecossistema."
        ),
        atores_primarios=("financeiro", "growth"),
        atores_adjacentes=("produto", "corpdev"),
        severidade_base=0.7,
        casos_referencia=(
            "Khan 2017 (Amazon)",
            "CADE Caderno Plataformas Digitais 2023",
        ),
    ),
    Conduta(
        nome="reverse_killer_shelving",
        descricao=(
            "Adquirir e engavetar produto que competiria com linha existente " "do adquirente."
        ),
        atores_primarios=("corpdev", "produto"),
        atores_adjacentes=("eng", "financeiro"),
        severidade_base=0.75,
        casos_referencia=(
            "Cunningham-Ederer-Ma JPE 2021 (mecanismo)",
            "Crémer-Montjoye-Schweitzer EC 2019 [?]",
        ),
    ),
    Conduta(
        nome="uso_dados_concorrentes",
        descricao=(
            "Plataforma usa dados de sellers do próprio marketplace para "
            "informar o desenvolvimento de produto próprio."
        ),
        atores_primarios=("eng", "produto"),
        atores_adjacentes=("corpdev", "comercial"),
        severidade_base=0.75,
        casos_referencia=(
            "Amazon Marketplace use of seller data (UE 2022 commitments)",
            "FTC v. Amazon §V (EUA 2023)",
        ),
    ),
    Conduta(
        nome="mfn_inverso_algorithmic",
        descricao=(
            "Algoritmo que detecta paridade alheia e penaliza seller via "
            "remoção de Buy Box ou similar."
        ),
        atores_primarios=("eng", "comercial"),
        atores_adjacentes=("produto", "growth"),
        severidade_base=0.7,
        casos_referencia=("FTC v. Amazon §IV — Project Nessie (EUA 2023) [?]",),
    ),
    Conduta(
        nome="sideloading_block",
        descricao=(
            "Bloquear instalação direta de apps fora da loja oficial do "
            "operador do sistema operacional."
        ),
        atores_primarios=("produto", "eng"),
        atores_adjacentes=("juridico", "design"),
        severidade_base=0.7,
        casos_referencia=(
            "Apple Brasil TCC CADE 2025",
            "DMA UE Art. 6(4) (2022)",
            "CMA SMS Apple mobile (UK 10/2025)",
        ),
    ),
    Conduta(
        nome="multihoming_friction",
        descricao=(
            "Atrito técnico ou de UX que torna custoso usar serviços rivais "
            "em paralelo ao serviço dominante."
        ),
        atores_primarios=("design", "eng"),
        atores_adjacentes=("produto", "growth"),
        severidade_base=0.55,
        casos_referencia=(
            "DMA UE Art. 6(7) interoperabilidade (2022)",
            "CMA SMS Mobile Roadmap (UK 2025) [?]",
        ),
    ),
    Conduta(
        nome="degradacao_api_seletiva",
        descricao=(
            "Degradar performance ou SLA de API só para integradores que "
            "competem em adjacência com a plataforma."
        ),
        atores_primarios=("eng", "operacoes"),
        atores_adjacentes=("produto", "juridico"),
        severidade_base=0.65,
        casos_referencia=(
            "Cornell JLPP — Pulling Up the Drawbridge (2025)",
            "FTC v. Meta — WhitePages política descontinuada [?]",
        ),
    ),
    Conduta(
        nome="lock_in_credenciais",
        descricao=(
            "Forçar login do ecossistema (Apple ID, Google Account) como "
            "pré-requisito para funcionalidades básicas."
        ),
        atores_primarios=("produto", "eng"),
        atores_adjacentes=("design", "growth"),
        severidade_base=0.55,
        casos_referencia=(
            "DMA UE Art. 5(7) (2022)",
            "Crémer-Montjoye-Schweitzer EC 2019 (capítulo SSO) [?]",
        ),
    ),
    Conduta(
        nome="switching_costs_design",
        descricao=(
            "Exportação proprietária, fricção de migração, ausência de "
            "portabilidade real entre serviços."
        ),
        atores_primarios=("eng", "produto"),
        atores_adjacentes=("design", "juridico"),
        severidade_base=0.55,
        casos_referencia=(
            "DMA UE Art. 6(9) portabilidade (2022)",
            "GDPR Art. 20",
            "CADE Caderno Plataformas Digitais 2023 §6",
        ),
    ),
    Conduta(
        nome="treino_ia_com_dados_concorrentes",
        descricao=(
            "Plataforma treina modelo de IA com dados ou conteúdo de business "
            "users rivais sem autorização ou contrapartida."
        ),
        atores_primarios=("eng", "produto"),
        atores_adjacentes=("corpdev", "juridico"),
        severidade_base=0.75,
        casos_referencia=(
            "Caso emergente sem condenação antitruste consolidada [?]",
            "NYT v. OpenAI (direito autoral, 2023)",
        ),
    ),
    Conduta(
        nome="discriminacao_algoritmica_preco",
        descricao=(
            "Preço personalizado ou dinâmico baseado em reputação de compra "
            "ou vulnerabilidade do usuário."
        ),
        atores_primarios=("eng", "produto"),
        atores_adjacentes=("growth", "comercial"),
        severidade_base=0.6,
        casos_referencia=(
            "RealPage litigation (EUA em curso)",
            "CMA Ticketmaster algorithmic pricing (UK 2024)",
            "NY Algorithmic Pricing Disclosure Act (2025)",
        ),
    ),
    Conduta(
        nome="surge_predatorio",
        descricao=(
            "Surge pricing usado em momentos de cativação (chuva, fila, etc.) "
            "sem alternativa real ao consumidor."
        ),
        atores_primarios=("eng", "operacoes"),
        atores_adjacentes=("financeiro", "produto"),
        severidade_base=0.5,
        casos_referencia=(
            "Sem condenação formal consolidada [?]",
            "Literatura de economia digital",
        ),
    ),
    Conduta(
        nome="manipulacao_relevancia_moderacao",
        descricao=(
            "Shadow-banning ou deboost seletivo de concorrente ou conteúdo "
            "crítico via moderação algorítmica."
        ),
        atores_primarios=("eng", "produto"),
        atores_adjacentes=("operacoes", "juridico"),
        severidade_base=0.6,
        casos_referencia=("Sem condenação antitruste consolidada — preocupação regulatória [?]",),
    ),
    Conduta(
        nome="exclusao_app_store_seletiva",
        descricao=("Remoção ou atraso de aprovação de app concorrente da loja oficial."),
        atores_primarios=("produto", "operacoes"),
        atores_adjacentes=("juridico", "eng"),
        severidade_base=0.7,
        casos_referencia=(
            "Epic v. Apple Fortnite ban 2020 (EUA)",
            "Apple Brasil TCC CADE 2025 (critérios não-discriminatórios)",
        ),
    ),
    Conduta(
        nome="default_distribution_exclusivo",
        descricao=(
            "Pagamento por default de busca ou IA em SO/browser excluindo "
            "concorrentes do canal principal de distribuição."
        ),
        atores_primarios=("comercial", "corpdev"),
        atores_adjacentes=("juridico", "produto"),
        severidade_base=0.75,
        casos_referencia=(
            "US v. Google Search — Mehta 05/08/2024 (Sherman §2)",
            "CMA SMS Google Search (UK 10/10/2025)",
        ),
    ),
    Conduta(
        nome="aquisicao_assets_chave",
        descricao=(
            "Aquisição de patentes, talento ou dataset estratégico para travar "
            "a entrada de rivais em mercado adjacente."
        ),
        atores_primarios=("corpdev", "juridico"),
        atores_adjacentes=("eng", "financeiro"),
        severidade_base=0.7,
        casos_referencia=(
            "Microsoft-OpenAI investment (EC RFI 2024)",
            "Google-Waze 2013 (citado em Dream Big v. Google) [?]",
        ),
    ),
    Conduta(
        nome="auto_deteccao_atrasada",
        descricao=(
            "Compliance interna detecta a conduta mas atrasa correção até "
            "intimação externa — torna a auto-correção uma estratégia adiada."
        ),
        atores_primarios=("juridico", "operacoes"),
        atores_adjacentes=("produto", "eng"),
        severidade_base=0.65,
        casos_referencia=("FTC v. Amazon — Project Nessie liga/desliga sob escrutínio",),
    ),
)


# ----- R20: q_min de cooperação interna por conduta -----
#
# Quantos papéis primários são minimamente necessários para que a
# conduta seja executada e mantida internamente. Calibra
# `q_min_cooperacao_interna` no `WaaSModel` quando o cenário declara
# uma conduta específica.
#
# Interpretação: nenhuma conduta digital unilateral aqui catalogada
# exige mais que 2-3 papéis primários — o que reforça a tese do
# moat. A corrida intra-firma do WaaS visa o primeiro denunciante
# entre 2-3 pessoas em papéis distintos, NÃO entre 10-15 cúmplices
# externos como no cartel clássico.
#
# Valores são **número absoluto de atores primários** (não fração).
# A fração `q_min` final é derivada pelo `model.py` dividindo pelo
# tamanho médio da firma.
N_ATORES_PRIMARIOS_NECESSARIOS: dict[str, int] = {
    c.nome: max(2, len(c.atores_primarios)) for c in CATALOGO
}


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
