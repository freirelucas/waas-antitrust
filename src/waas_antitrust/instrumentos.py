"""Instrumentos de internalização do capital social (R21 + Eco A + Adv B v2).

Módulo **declarativo**: define a taxonomia do **canal base** + **4 instrumentos**
sob a correção radical v3. Não introduz lógica nova de modelo — referencia as
implementações existentes (`agents.py`/`model.py` P2/P2.5b para o canal,
`model.py` P3 para WaaS, `hirschman.py` para Hirschman) ou marca como stub
(crédito tributário, leniência criminal individual).

Sob a correção v3 (Ayres-Unkovic 2012; análogo Callisto), o **canal de
depósito condicional operado pelo CADE** é o mecanismo BASE — não paga, não
puni, apenas armazena denúncias condicionais até massa crítica intra-firma.
Os 4 instrumentos monetários são **acoplamentos opcionais** ao canal.

Atende à convergência forte da x10 v2:

- **Eco A v2** — sem `Protocol Instrumento` ortogonal, "múltiplos
  instrumentos" é decoração: o modelo continua tratando tudo como variante
  do WaaS monetário, e o reframe de bem coletivo fica preso na narrativa.

- **Adv B v2** — gating estrutural em ponto único: cada instrumento tem
  reserva constitucional distinta (ordinária, complementar tributária,
  penal estrita). Tratar "exigir lei" como categoria homogênea é erro
  hierárquico de fontes.

A taxonomia aqui permite a `cenarios.py` referenciar cada instrumento por
nome e a futuras viz (`viz/instrumentos.py`) compararem `dano_evitavel ÷
custo_público` lado a lado.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrumento:
    """Metadados estruturais de um instrumento de internalização.

    Atributos:
        nome: identificador canônico em snake_case
        descricao: o que internaliza, em uma frase
        reserva_constitucional: artigo/tipo (Art. 22 I, Art. 146 LC, etc.)
        regime_minimo: sub-regime mínimo capaz de hospedar (A, B, Cₜ, Cᵩ, Cₚ)
        fonte_primaria: precedente dogmático ou literatura calibradora
        modulo_implementacao: arquivo .py onde a lógica está (ou stub)
        status: "implementado" | "stub" | "conceitual"
    """

    nome: str
    descricao: str
    reserva_constitucional: str
    regime_minimo: str
    fonte_primaria: str
    modulo_implementacao: str
    status: str


#: Catálogo declarativo: canal base (v3) + 4 instrumentos canônicos do reframe v2.
INSTRUMENTOS: tuple[Instrumento, ...] = (
    Instrumento(
        nome="canal_deposito_condicional",
        descricao=(
            "**Mecanismo BASE da LCMC v3**: canal procedimental do CADE que "
            "recebe denúncias condicionais (depósitos em escrow) e só as abre "
            "quando massa crítica intra-firma é atingida (q_min · n co-depósitos). "
            "Não paga, não pune — é a infraestrutura de coordenação sem a qual "
            "qualquer instrumento monetário acoplado opera no vácuo. Análogo "
            "operacional: Callisto (callisto.org), em uso desde 2015 em "
            "universidades americanas para assédio sexual. Os 4 instrumentos "
            "abaixo são **acoplamentos opcionais** ao canal."
        ),
        reserva_constitucional=(
            "Sem reserva específica — base autônoma em Art. 4º II/III da Lei "
            "12.529/2011 (atribuição do CADE: instaurar processo, propor TCC) "
            "c/c Lei 9.784/99 (procedimento administrativo federal)"
        ),
        regime_minimo="B",
        fonte_primaria=(
            "Ayres & Unkovic 2012 *Michigan L. Rev.* 111:145 (information escrow); "
            "análogo Callisto (callisto.org); Lei 12.529/2011 Art. 4º + Lei 9.784/99"
        ),
        modulo_implementacao=(
            "agents.py (AutoridadeAgent.escrow_denuncias, R27) + "
            "model.py (P2 deposita, P2.5b expira e abre)"
        ),
        status="implementado",
    ),
    Instrumento(
        nome="recompensa_tcc_waas",
        descricao=(
            "Firma paga o trabalhador denunciante; o pagamento é re-caracterizado "
            "como ressarcimento extrajudicial sob Art. 12 da Res. 21/2018 e/ou "
            "como reconhecimento de interesse público em detecção e cessação "
            "(Lei 9.784/99). Precedente dogmático brasileiro: Lei 12.846/2013 "
            "(LAC) Art. 7º VII-VIII (programa de integridade como atenuante)."
        ),
        reserva_constitucional="Art. 22 I CF (lei ordinária comum)",
        regime_minimo="B",
        fonte_primaria="Lei 12.529/2011 Art. 85 + Res. 21/2018 Art. 12 + LAC Art. 7º",
        modulo_implementacao="model.py (P3) + corrida.py (LCMC)",
        status="implementado",
    ),
    Instrumento(
        nome="vesting_acelerado_hirschman",
        descricao=(
            "Cláusula contratual padrão que acelera vesting de equity em "
            "gatilho de ação coletiva. Cria ameaça crível de êxodo coletivo "
            "que reduz `g_i` preventivamente (P0) e amplia a IC-F* da firma "
            "(P3: `D_extra + custo_exodo > W`). NÃO destrói valor; transfere "
            "equity aos funcionários que saem."
        ),
        reserva_constitucional="Art. 22 I CF (matéria contratual padrão exige lei ordinária federal)",
        regime_minimo="Cₜ trabalhista",
        fonte_primaria="Hirschman 1970 *Exit, Voice, and Loyalty*; padrões YC/NVCA",
        modulo_implementacao="hirschman.py",
        status="implementado",
    ),
    Instrumento(
        nome="credito_tributario_denunciante",
        descricao=(
            "Estado financia o trabalhador denunciante por renúncia fiscal "
            "(crédito ou abatimento sobre IRPF). Análogo limitado ao IRS "
            "Whistleblower Office (26 U.S.C. §7623), MAS a analogia americana "
            "É INAPLICÁVEL — IRS opera sob federal taxing power exclusivo, "
            "sem reserva penal. No Brasil, exige LC + LRF Art. 14."
        ),
        reserva_constitucional=(
            "Art. 146 III CF (LC para IRPJ/CSLL) + Art. 150 §6º (benefício "
            "fiscal específico) + LRF Art. 14 (estimativa trienal de impacto)"
        ),
        regime_minimo="Cᵩ tributária-LC",
        fonte_primaria=(
            "Crémer-Montjoye-Schweitzer (EC 2019); IRS Whistleblower Office "
            "(precedente análogo, NÃO transponível); pendência R22"
        ),
        modulo_implementacao="cenarios.py (stub: credito_tributario_puro)",
        status="stub",
    ),
    Instrumento(
        nome="leniencia_criminal_individual",
        descricao=(
            "Estado oferece imunidade ou redução de pena ao empregado-partícipe "
            "que coopera com a investigação antitruste. NÃO confundir com Art. "
            "86 da Lei 12.529/2011, que protege EMPRESA+colaboradores-do-acordo, "
            "não empregado-terceiro. Lei 13.608 Art. 4º-C §3º restringe a "
            "'crimes contra a administração pública' — cartel é Lei 8.137 Art. "
            "4º, categoria distinta. Extensão analógica é vedada in malam partem."
        ),
        reserva_constitucional="Art. 5º XXXIX CF (reserva penal estrita)",
        regime_minimo="Cₚ penal",
        fonte_primaria=(
            "Lei 12.529/2011 Art. 86 (limite); Lei 13.608/2018 Art. 4º-C §3º "
            "(restrição); pendência R23 + análise dogmática D-cap (autor)"
        ),
        modulo_implementacao="cenarios.py (stub: leniencia_criminal_individual)",
        status="stub",
    ),
)


def lookup_instrumento(nome: str) -> Instrumento:
    """Localiza um instrumento por nome canônico; KeyError se desconhecido."""
    for inst in INSTRUMENTOS:
        if inst.nome == nome:
            return inst
    nomes_validos = ", ".join(i.nome for i in INSTRUMENTOS)
    raise KeyError(f"instrumento desconhecido: {nome!r}. Válidos: {nomes_validos}")


#: Hierarquia de regimes — chave para resolver hospedagem por `regime_minimo`.
_NIVEL_REGIME: dict[str, int] = {
    "A": 0,
    "B": 1,
    "C": 2,
    "Cₜ": 2,
    "Ct": 2,
    "Cᵩ": 3,
    "Cf": 3,
    "Cₚ": 4,
    "Cp": 4,
}


def instrumentos_por_regime(regime: str) -> list[Instrumento]:
    """Lista entradas hospitáveis em um dado regime (canal + instrumentos),
    derivando o nível de cada entrada do campo `regime_minimo`.

    Hierarquia:
    - Regime A: nenhum (canal exige base infralegal mínima — Regime B)
    - Regime B: canal_deposito_condicional + recompensa_tcc_waas
    - Regime C / Cₜ: + vesting_acelerado_hirschman
    - Regime Cᵩ: + credito_tributario_denunciante
    - Regime Cₚ: + leniencia_criminal_individual
    """
    if regime not in _NIVEL_REGIME:
        raise ValueError(f"regime desconhecido: {regime!r}. Use A, B, C, Cₜ, Cᵩ, Cₚ.")
    nivel = _NIVEL_REGIME[regime]
    return [i for i in INSTRUMENTOS if _NIVEL_REGIME[i.regime_minimo.split()[0]] <= nivel]
