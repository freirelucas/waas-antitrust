"""Jogo global (Morris-Shin 1998) do subjogo de coordenação dos denunciantes.

EXPLORATÓRIO / ESTILIZADO (R02). Deriva o **limiar de switching único** da decisão
de sinalizar sob informação privada e mostra que ele converge a um limite bem
definido quando o ruído do sinal τ → 0 — a seleção de equilíbrio único que motiva a
Proposição 2. **Não** está integrado à dinâmica de arquétipos do ABM principal
(`agents.py`); serve como verificação analítica da estrutura teórica.

Modelo estilizado
-----------------
Fundamental θ (severidade) com prior difuso; cada trabalhador recebe sinal privado
``x_i = θ + τ·ε_i``, ``ε_i ~ N(0, 1)``, e sinaliza se ``x_i ≥ x*``. A cascata (massa
crítica) é bem-sucedida se a fração de sinalizadores ≥ ``k``. O ganho de uma denúncia
bem-sucedida cresce com a severidade (``b·θ``, com ``b ∝ W``); o custo de uma denúncia
frustrada é ``c`` (``∝`` represália ``r``). A indiferença do trabalhador marginal
(crença laplaciana) dá o limiar **único**

    x*(τ) = [c·k − b·τ·φ(Φ⁻¹(k))] / [b·(1−k)],     x*(0) = c·k / [b·(1−k)],

com φ e Φ a densidade e a CDF normais padrão. O limiar é único (linear em ``x*``), em
contraste com a multiplicidade de equilíbrios do jogo de coordenação sob conhecimento
comum — exatamente o ponto de Morris-Shin.

Limitações (ver docs/DECISIONS.md, R02): ganho linear na severidade e massa crítica
constante são simplificações; o contraste formal com a multiplicidade e a integração
ao ABM seguem em aberto.

Extensão LCMC (Mat A v2 — R20)
------------------------------
Sob `modo_corrida=True`, o ganho marginal do trabalhador deixa de ser ``b`` uniforme e
passa a depender da posição esperada ``k`` na fila intra-firma:

    b_k = f_W(k) · b,      f_W(k) = D_Saito(k) / D_Saito(1)

(``decaimento_W`` em ``corrida.py``). O **limiar por posição** vira

    x*_k(τ) = [c·k_rel − b_k·τ·φ(Φ⁻¹(k_rel))] / [b_k·(1−k_rel)]

onde ``k_rel`` é a massa crítica relativa (não confundir com a posição ``k`` na fila).
Logo, sob LCMC, **não há um único limiar** — há uma **família de limiares** indexada
por posição esperada, e a "oferta do bem coletivo" tem escala decrescente conforme
posições se afastam da 1ª.

**Caveat formal de unicidade** (Mat A v2, Frankel-Morris-Pauzner 2003;
Angeletos-Hellwig-Pavan 2007): a unicidade Morris-Shin clássica supõe jogo estático.
Sob LCMC a fila inter-firma é sinal público correlacionado — Angeletos-Hellwig-Pavan
mostraram que isso pode restaurar multiplicidade. A Proposição 2 reformulada
"sequência {x*(t)}_t decrescente é única em cada instante" requer condições adicionais
(independência inter-firma; ausência de sinal público sobre fila) que não são
satisfeitas no caso geral. Tratamos como **conjectura aberta** (ver ODD §Prop 2).
"""

from __future__ import annotations

from scipy.stats import norm


def limiar_switching(b: float, c: float, k: float, tau: float = 0.0) -> float:
    """Limiar de switching ``x*`` do jogo global (``tau=0`` dá o limite de Morris-Shin).

    Parameters
    ----------
    b : float
        Ganho marginal de uma denúncia bem-sucedida por unidade de severidade (``∝ W``).
    c : float
        Custo de uma denúncia frustrada (``∝`` represália ``r``).
    k : float
        Massa crítica como fração, em ``(0, 1)``.
    tau : float
        Desvio-padrão do ruído do sinal privado (``≥ 0``). ``0`` devolve o limite ``τ→0``.

    Returns
    -------
    float
        O limiar único ``x*``: o trabalhador sinaliza sse seu sinal privado ``x_i ≥ x*``.
    """
    if not 0.0 < k < 1.0:
        raise ValueError("k deve estar em (0, 1)")
    if b <= 0.0:
        raise ValueError("b deve ser positivo")
    if tau < 0.0:
        raise ValueError("tau deve ser não-negativo")
    z = float(norm.ppf(k))
    return (c * k - b * tau * float(norm.pdf(z))) / (b * (1.0 - k))


def trilha_convergencia(b: float, c: float, k: float, taus: list[float]) -> list[float]:
    """Limiares para uma sequência de ``τ``, evidenciando a convergência ao limite ``τ→0``."""
    return [limiar_switching(b, c, k, tau) for tau in taus]


def limiar_switching_por_posicao(
    b: float,
    c: float,
    k_rel: float,
    posicao_trabalhador: int,
    tau: float = 0.0,
    perfil: str = "saito",
) -> float:
    """Limiar de switching ``x*_k`` para o trabalhador na ``posicao_trabalhador`` na fila
    intra-firma sob LCMC (``modo_corrida=True``).

    Sob o decaimento Saito, o ganho marginal vira ``b_k = f_W(k) · b`` com
    ``f_W(k) = D_Saito(k) / D_Saito(1)``. A consequência é que **cada posição** tem
    seu próprio limiar; o "bem coletivo" tem oferta escalonada por posição.

    Atende a M1 da crítica Mat A v2 (x10 v2): explicita que o limiar Morris-Shin
    sob LCMC não é monolítico.

    Parameters
    ----------
    b : float
        Ganho marginal base (posição 1) por unidade de severidade.
    c : float
        Custo de denúncia frustrada.
    k_rel : float
        Massa crítica relativa em ``(0, 1)`` (não confundir com posição na fila).
    posicao_trabalhador : int
        Posição esperada na fila intra-firma (1-indexada).
    tau : float
        Desvio-padrão do ruído.
    perfil : str
        Perfil de decaimento; só ``"saito"`` está calibrado (consome Saito 2021).

    Returns
    -------
    float
        Limiar ``x*_k`` para a posição dada. Quanto maior a posição, **maior** o
        limiar (recompensa esperada cai com posição ⇒ trabalhador mais cauteloso).
    """
    from waas_antitrust.corrida import decaimento_W

    if posicao_trabalhador < 1:
        raise ValueError(f"posicao_trabalhador deve ser ≥ 1; recebeu {posicao_trabalhador}")
    b_k = decaimento_W(posicao_trabalhador, b, perfil=perfil)
    return limiar_switching(b_k, c, k_rel, tau)


def familia_limiares_por_posicao(
    b: float,
    c: float,
    k_rel: float,
    posicoes: list[int] | tuple[int, ...] = (1, 2, 3, 4, 5),
    tau: float = 0.0,
    perfil: str = "saito",
) -> list[float]:
    """Família de limiares ``{x*_k}`` para uma sequência de posições na fila intra-firma.

    Útil para visualizar o "bem coletivo escalonado" — Proposição 1 reformulada sob LCMC
    afirma que existe número finito ``n*`` de posições para as quais ``x*_k`` está
    abaixo de algum limite tolerável; posições além de ``n*`` enfrentam limiar
    proibitivo e desistem de cooperar.
    """
    return [limiar_switching_por_posicao(b, c, k_rel, k, tau=tau, perfil=perfil) for k in posicoes]
