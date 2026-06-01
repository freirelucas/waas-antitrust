"""Ameaça crível de êxodo coletivo (Hirschman exit-with-equity).

EXPLORATÓRIO (R07). Quando funcionários numa firma com cláusulas de **vesting
acelerado por gatilho de ação coletiva** atingem massa crítica de denúncia, a
firma enfrenta uma ameaça crível de perder capital humano. O custo esperado
dessa perda integra o cálculo de incentivo da firma — distinto do pagamento
direto aos denunciantes.

Parâmetros padrão (YC; calibrar formalmente em R03):
- Vesting: 4 anos com cliff de 1 ano (single-trigger em ação coletiva)
- Custo de substituição: ~50% do salário anual por funcionário (recrutamento +
  onboarding + perda de produtividade na transição)
- Valor de equity por funcionário: ~50% de um salário anual (provisional)
- Em média ~50% do equity está non-vested em qualquer momento (carreira típica
  de 4 anos com cliff de 1 ano)

A integração no modelo ocorre em duas camadas:

1. **Reativa (P3)** — quando massa crítica é atingida, a firma pondera pagar
   denunciantes vs. enfrentar o êxodo. A IC-F* clássica `D > W` se amplia para
   `D + custo_exodo > W`: o exit-threat aumenta a disposição da firma a pagar.

2. **Preventiva (P0)** — antecipando a camada reativa, firmas com cláusulas
   aceleradas têm `g_i` efetivo menor: violam menos *antes* de qualquer
   denúncia ocorrer. É a dissuasão indireta pela ameaça crível.

NÃO há destruição de valor: o vesting acelerado **transfere** equity aos
funcionários que saem; o custo para a firma é a substituição + a antecipação
dessa transferência. O ecossistema de equity é preservado, em contraste com um
takeover hostil clássico.
"""

from __future__ import annotations


def custo_substituicao(
    n_funcionarios: int,
    w_a_medio: float,
    fator: float = 0.5,
) -> float:
    """Custo de substituir n funcionários (recrutamento + onboarding + transição).

    Padrão: ~50% do salário anual por funcionário (referência literatura RH/YC).
    """
    if n_funcionarios < 0 or w_a_medio < 0 or fator < 0:
        raise ValueError("argumentos não-negativos")
    return n_funcionarios * fator * w_a_medio


def valor_vesting_acelerado(
    n_funcionarios: int,
    w_a_medio: float,
    valor_equity_por_funcionario: float = 0.5,
    fracao_nao_vested: float = 0.5,
) -> float:
    """Valor do equity acelerado para n funcionários que disparam cláusula.

    `valor_equity_por_funcionario` em unidades de salário anual médio.
    `fracao_nao_vested`: em média ~50% (vesting 4y/1y cliff).
    """
    if (
        n_funcionarios < 0
        or w_a_medio < 0
        or valor_equity_por_funcionario < 0
        or not 0.0 <= fracao_nao_vested <= 1.0
    ):
        raise ValueError("argumentos inválidos")
    return n_funcionarios * valor_equity_por_funcionario * w_a_medio * fracao_nao_vested


def custo_exodo_esperado(
    n_disparados: int,
    w_a_medio: float,
    tem_clausula: bool,
    fator_substituicao: float = 0.5,
    valor_equity_por_funcionario: float = 0.5,
    fracao_nao_vested: float = 0.5,
) -> float:
    """Custo total esperado se a ameaça de êxodo se materializar.

    Sem cláusula contratual: zero (não há gatilho legal para acelerar vesting).
    """
    if not tem_clausula:
        return 0.0
    return custo_substituicao(
        n_disparados, w_a_medio, fator_substituicao
    ) + valor_vesting_acelerado(
        n_disparados, w_a_medio, valor_equity_por_funcionario, fracao_nao_vested
    )


def deve_pagar_com_hirschman(
    W_total: float,
    D_val: float,
    custo_exodo: float,
) -> bool:
    """IC-F* ampliada: a firma paga denunciantes se `D + custo_exodo > W`.

    Sem exit-threat (custo_exodo=0), reduz-se à IC-F* clássica `D > W`.
    Com exit-threat positivo, a firma pode preferir pagar mesmo quando o
    desconto sozinho não justificaria — porque evita também o custo de perder
    o capital humano.
    """
    return (D_val + custo_exodo) > W_total


def g_i_efetivo(
    g_i: float,
    tem_clausula: bool,
    p_perc: float,
    peso_hirschman: float = 0.3,
) -> float:
    """Atratividade efetiva de violar, descontada pela ameaça preventiva.

    Firmas com cláusula antecipam que, se a massa crítica for atingida, terão
    de pagar denunciantes ou enfrentar exit-threat. Essa expectativa reduz a
    atratividade de violar antes mesmo de qualquer denúncia.

    `peso_hirschman` é normativo provisional (calibrar em R03).
    """
    if not tem_clausula:
        return g_i
    return g_i - p_perc * peso_hirschman
