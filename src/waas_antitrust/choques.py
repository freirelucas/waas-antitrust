"""Choques exógenos discretos sobre o modelo (R19, exploratório).

Atende à crítica do autor — "como o modelo lida com choques?" — e à
hipótese substantiva — "os layoffs podem ser oportunidade?". O modelo
deixa de ser estacionário-estocástico e ganha um mecanismo de **eventos
discretos** no tempo, inspirado na tradição Eurace@Unibi (Dawid et al.)
de choques exógenos em ABM macro.

Quatro tipos canônicos (v0, simplificação documentada — efeitos
**instantâneos** que se propagam pela dinâmica adaptativa do modelo;
duração explícita fica para v1):

- **layoff**: converte `magnitude` × trabalhadores a `status="ex_funcionario"`.
  Ex-funcionários têm `r_represalia` efetivo reduzido (fator <1) e
  preservam capacidade de sinalizar via `historico_observou > 0`.
- **caso_paradigmatico**: pulso em `p_perc` global. Eleva detecção
  percebida ao `max(p_perc, magnitude)` — captura efeito Schelling de
  um TCC público de alto perfil (Meta-Instagram 2012, iFood 2023).
- **campanha_cade**: pulso em `rho_acuracia` da autoridade. Captura
  alocação extraordinária de capacidade investigativa a casos digitais.
- **choque_juridico**: pulso em `p_anulacao_tcc`. Captura decisão
  jurisprudencial adversa que eleva risco F6 permanentemente.

Cinco catálogos canônicos:

- `CHOQUES_TECH_2022_2024` — ondas de layoff jan/2023 e jan/2024
  (calibração frouxa contra layoffs.fyi para o setor tech BR;
  magnitudes ainda em ordem de grandeza). Causalidade CÍCLICA
  (overhiring pandêmico + aperto monetário).
- `CHOQUES_TECH_2024_2025_AI_RESTRUCTURING` — ondas Q4/2024 e 2025-26
  com causalidade ESTRUTURAL (IA-eficiência + pivot estratégico).
  Pesquisa de fundo 2026: 40% das vagas eliminadas não são reabertas
  (AlixPartners 2025). Salesforce, SAP, Intel, Cisco, Meta Reality Labs.
- `CHOQUES_CAMPANHA_CADE_DIGITAL` — pulso de prioridade digital no
  CADE-DEE pós DT-003/2022.
- `CHOQUES_CASO_PARADIGMATICO_IFOOD_2023` — TCC iFood publicado.

Calibração formal pendente em R03 — em particular, as magnitudes dos
choques precisam ser ancoradas em fontes primárias:
- layoffs.fyi para `layoff` (fração mensal/anual em tech BR);
- DEE/CADE DTs para `campanha_cade`;
- Casos paradigmáticos com cobertura de imprensa de massa para
  `caso_paradigmatico`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from waas_antitrust.model import WaaSModel


#: Tipos válidos de choque — validar contra este conjunto antes de aplicar.
TIPOS_VALIDOS: frozenset[str] = frozenset(
    {"layoff", "campanha_cade", "caso_paradigmatico", "choque_juridico"}
)


@dataclass(frozen=True)
class Choque:
    """Evento exógeno discreto.

    `tique` é o passo de tempo (1-indexado, igual à variável `self.tique`
    em `WaaSModel`). `magnitude` tem semântica dependente de `tipo`:

    - `layoff`: fração de trabalhadores demitidos em cada firma (∈ [0, 1]).
    - `caso_paradigmatico`: novo piso de `p_perc` (∈ [0, 1]).
    - `campanha_cade`: aumento em `rho_acuracia` (somado, clipado a 0,99).
    - `choque_juridico`: aumento em `p_anulacao_tcc` (somado, clipado a 1).

    `descricao` é texto livre para diagnóstico (referência empírica,
    contexto institucional, fonte primária).
    """

    tique: int
    tipo: str
    magnitude: float
    descricao: str = ""
    # Pesquisa de fundo 2026 (autor): a causalidade declarada dos layoffs
    # tech mudou de cíclica ("overhiring pandêmico"; 2022-2023) para
    # estrutural ("AI efficiency restructuring"; 2024-2025). Distinguir
    # facilita análise heterogênea de magnitude e padrão de propagação.
    # Valores aceitos (não-validados): "overhiring_pandemico", "aperto_monetario",
    # "ai_efficiency", "pivot_estrategico", "campanha_regulatoria",
    # "decisao_judicial". Default "" preserva compat.
    causa_declarada: str = ""

    def __post_init__(self) -> None:
        if self.tipo not in TIPOS_VALIDOS:
            raise ValueError(
                f"tipo de choque desconhecido: {self.tipo!r}. " f"Válidos: {sorted(TIPOS_VALIDOS)}."
            )
        if self.tique < 1:
            raise ValueError(f"tique deve ser >= 1, recebeu {self.tique}.")
        if not 0.0 <= self.magnitude <= 1.0:
            raise ValueError(f"magnitude deve estar em [0, 1], recebeu {self.magnitude}.")


def aplicar_choque(modelo: WaaSModel, choque: Choque) -> None:
    """Aplica `choque` ao `modelo` in-place no tique corrente.

    Idempotente em um único tique — chamar duas vezes com o mesmo choque
    no mesmo tique produzirá o efeito acumulado (e.g., dois layoffs de
    6% = ~11,6% de demitidos).
    """
    if choque.tipo == "layoff":
        for ws in modelo.trabalhadores_por_empresa.values():
            ativos = [t for t in ws if t.status == "ativo"]
            n_ex = int(choque.magnitude * len(ativos))
            if n_ex <= 0:
                continue
            indices = modelo.rng.choice(len(ativos), size=n_ex, replace=False)
            for i in indices:
                ativos[int(i)].status = "ex_funcionario"
        modelo.n_choques_layoff_aplicados += 1
        return
    if choque.tipo == "caso_paradigmatico":
        modelo.p_perc = max(modelo.p_perc, float(choque.magnitude))
        modelo.n_choques_paradigmaticos_aplicados += 1
        return
    if choque.tipo == "campanha_cade":
        rho_novo = min(0.99, modelo.autoridade.rho + float(choque.magnitude))
        modelo.autoridade.rho = rho_novo
        modelo.n_choques_campanha_aplicados += 1
        return
    if choque.tipo == "choque_juridico":
        modelo.p_anulacao_tcc = min(1.0, modelo.p_anulacao_tcc + float(choque.magnitude))
        modelo.n_choques_juridicos_aplicados += 1
        return


# ---------------------------------------------------------------------
# Catálogos canônicos — calibração ainda frouxa (R03)
# ---------------------------------------------------------------------

#: Duas ondas grandes de layoff em tech 2022-2024 (causalidade CÍCLICA).
#: Magnitudes em ordem de grandeza de layoffs.fyi para o setor; calibrar
#: contra a série específica de BR em R03.
#:
#: **Pesquisa de fundo 2026**: 2022-2024 totalizou ~579 mil demissões
#: globais (165 mi 2022 + 262 mi 2023 + 152 mi 2024); ondas dominadas por
#: Meta nov/2022 (11k, 13%), Twitter nov/2022 (3,7k, 50%), Amazon nov/2022
#: (10k), Google jan/2023 (12k, 6%), Microsoft jan/2023 (10k, 5%).
#: Brasscom 2024 indica EXPANSÃO LÍQUIDA do setor TIC BR (+4,5% formal),
#: mas com cortes específicos em iFood, PicPay, Loft, Neon, C6, PagSeguro.
CHOQUES_TECH_2022_2024: tuple[Choque, ...] = (
    Choque(
        tique=4,
        tipo="layoff",
        magnitude=0.06,
        descricao=(
            "Onda jan/2023 (Meta, Google, Amazon, Microsoft globais; " "subsidiárias BR atingidas)."
        ),
        causa_declarada="overhiring_pandemico",
    ),
    Choque(
        tique=8,
        tipo="layoff",
        magnitude=0.04,
        descricao=(
            "Onda jan/2024 (continuação da contração global; ajuste "
            "pós-bolha de contratação 2021)."
        ),
        causa_declarada="aperto_monetario",
    ),
)

#: Onda de demissões 2024-2026 com causalidade ESTRUTURAL (AI restructuring).
#: Pesquisa de fundo 2026 confirma mudança qualitativa: 40% das vagas
#: eliminadas NÃO são reabertas (AlixPartners 2025), apontando substituição
#: por automação/IA. Empresas declararam explicitamente "AI efficiency":
#: Salesforce 8k (Q4/2024), SAP até 8k + €2bi/ano em IA, Intel 15k (~15%),
#: Cisco 4k (~5%), Meta Reality Labs 1k (10% RL) + 3,6k geral 2025-26.
#: Hipótese: o trabalhador demitido por "IA-eficiência" tem mais conhecimento
#: técnico de algoritmos e dados → qualidade de prova potencialmente maior.
CHOQUES_TECH_2024_2025_AI_RESTRUCTURING: tuple[Choque, ...] = (
    Choque(
        tique=12,
        tipo="layoff",
        magnitude=0.05,
        descricao=(
            "Onda Q4/2024 — primeiras demissões EXPLICITAMENTE atribuídas a "
            "IA-eficiência: Salesforce, SAP, Intel, Cisco. ~40% das vagas "
            "não são reabertas (AlixPartners 2025)."
        ),
        causa_declarada="ai_efficiency",
    ),
    Choque(
        tique=16,
        tipo="layoff",
        magnitude=0.04,
        descricao=(
            "Onda 2025-26 — pivot estratégico Meta Reality Labs → IA "
            "hardware; reestruturação por capacidade de modelo. Atinge "
            "engenharia de pesquisa e produto sênior."
        ),
        causa_declarada="pivot_estrategico",
    ),
)

#: Pulso de prioridade digital no CADE pós DEE DT-003/2022.
CHOQUES_CAMPANHA_CADE_DIGITAL: tuple[Choque, ...] = (
    Choque(
        tique=6,
        tipo="campanha_cade",
        magnitude=0.15,
        descricao=(
            "Inflexão DEE/CADE DT-003/2022 (aprendizado de máquina e "
            "antitruste) + ramp de prioridade digital pós-2024."
        ),
    ),
)

#: TCC paradigmático iFood 2023 — efeito Schelling sobre p_perc.
CHOQUES_CASO_PARADIGMATICO_IFOOD_2023: tuple[Choque, ...] = (
    Choque(
        tique=5,
        tipo="caso_paradigmatico",
        magnitude=0.35,
        descricao=(
            "TCC iFood 2023 com exclusividade — cobertura ampla na imprensa "
            "elevou a percepção de risco no setor de marketplaces BR."
        ),
    ),
)

#: Choque jurisprudencial adverso hipotético — STJ anula TCC-WaaS.
CHOQUES_JURIDICO_ADVERSO: tuple[Choque, ...] = (
    Choque(
        tique=10,
        tipo="choque_juridico",
        magnitude=0.30,
        descricao=(
            "Decisão hipotética do STJ desautorizando a re-caracterização "
            "da recompensa como ressarcimento (falsificador F6 ativado)."
        ),
    ),
)


def listar_catalogos() -> dict[str, tuple[Choque, ...]]:
    """Nomes dos catálogos canônicos disponíveis."""
    return {
        "tech_2022_2024": CHOQUES_TECH_2022_2024,
        "tech_2024_2025_ai_restructuring": CHOQUES_TECH_2024_2025_AI_RESTRUCTURING,
        "campanha_cade_digital": CHOQUES_CAMPANHA_CADE_DIGITAL,
        "caso_paradigmatico_ifood_2023": CHOQUES_CASO_PARADIGMATICO_IFOOD_2023,
        "juridico_adverso": CHOQUES_JURIDICO_ADVERSO,
    }
