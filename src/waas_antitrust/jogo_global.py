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
