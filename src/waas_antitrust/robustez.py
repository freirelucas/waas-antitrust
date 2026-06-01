"""Funções de robustez estatística para o modelo WaaS.

Categoria 2 do plano de melhorias pós-crítica x10 (Mat A, Mat B):

1. **Suavização Beta-Binomial** (`beta_binomial_smoothing`): substitui o
   estimador frequencista `vp/n_violadoras`, que tem variância explosiva
   quando `n_violadoras` é pequeno e singularidade em `n_violadoras = 0`.
   Com prior Beta(α, β) — pseudo-contagens — a posterior é
   `Beta(α + vp, β + n_violadoras − vp)`, cuja média
   `(vp + α) / (n_violadoras + α + β)` está sempre bem definida e
   converge para o estimador frequencista quando `n_violadoras → ∞`.

2. **Bootstrap multi-seed** (`bootstrap_ci`, `varredura_multi_seed`):
   helpers para promover testes de uma seed única a comparações com
   intervalo de confiança via reamostragem percentílica. Reduz o risco
   de overclaim na cauda de seeds (Mat A: a variância pontual de
   `vp/n_violadoras` é alta; Mat B: o ranking entre regimes pode
   cruzar zero em algumas seeds).

Ambos são funções puras e testáveis em isolamento.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


def beta_binomial_smoothing(
    sucessos: int,
    tentativas: int,
    alpha: float = 1.0,
    beta: float = 5.0,
) -> float:
    """Estimador MAP de probabilidade Beta-Binomial com pseudo-contagens.

    Resolve duas patologias do estimador frequencista `sucessos / tentativas`:

    1. **Singularidade** em `tentativas = 0` (divisão por zero).
    2. **Variância explosiva** em `tentativas` pequenas (estimador instável
       quando o denominador é pequeno; sensível a cauda de seeds).

    Com prior Beta(α, β), a posterior conjugada é
    `Beta(α + sucessos, β + tentativas − sucessos)`, cuja média
    `(sucessos + α) / (tentativas + α + β)` está sempre bem definida.
    Em `tentativas = 0` retorna a média do prior `α / (α + β)`. À medida
    que `tentativas → ∞`, converge para o estimador frequencista.

    Padrão `α = 1, β = 5` corresponde a prior fraco centrado em ~16,7%
    (próximo do `p_deteccao_prior = 0.15` do modelo); ajustar formalmente
    em R03.
    """
    if sucessos < 0 or tentativas < 0:
        raise ValueError("sucessos e tentativas devem ser não-negativos")
    if sucessos > tentativas:
        raise ValueError("sucessos não pode exceder tentativas")
    if alpha <= 0 or beta <= 0:
        raise ValueError("hiperparâmetros do prior devem ser positivos")
    return (sucessos + alpha) / (tentativas + alpha + beta)


@dataclass
class IntervaloConfianca:
    """Estatística pontual + intervalo via percentil bootstrap.

    `mediana` é a mediana observada na amostra; `inferior` e `superior` são
    os quantis (α/2) e (1 − α/2) da distribuição bootstrap das medianas
    reamostradas. `n` registra o tamanho da amostra original.
    """

    mediana: float
    inferior: float
    superior: float
    n: int


def bootstrap_ci(
    valores: list[float] | np.ndarray,
    n_bootstrap: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> IntervaloConfianca:
    """Intervalo de confiança via reamostragem bootstrap percentílica.

    Para uma amostra de N execuções (cada uma com seed distinto), retorna
    a mediana observada e o intervalo `(1 − α)` aproximado pelos quantis
    da distribuição bootstrap das medianas reamostradas (com reposição).

    `seed` controla o gerador interno do bootstrap (independente das seeds
    das execuções do modelo).
    """
    arr = np.asarray(valores, dtype=float)
    if arr.size == 0:
        raise ValueError("valores vazio")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha deve estar em (0, 1)")
    rng = np.random.default_rng(seed)
    medianas = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        amostra = rng.choice(arr, size=arr.size, replace=True)
        medianas[i] = float(np.median(amostra))
    inferior = float(np.quantile(medianas, alpha / 2))
    superior = float(np.quantile(medianas, 1.0 - alpha / 2))
    return IntervaloConfianca(
        mediana=float(np.median(arr)),
        inferior=inferior,
        superior=superior,
        n=int(arr.size),
    )


def varredura_multi_seed(
    fabrica: Callable[[int], float],
    seeds: list[int],
) -> list[float]:
    """Executa `fabrica(seed)` para cada seed e coleta as métricas escalares.

    Helper para testes multi-seed: o chamador descreve a métrica como uma
    função pura `seed → escalar` (e.g., "dano final do regime B com este
    seed"). Útil em conjunto com `bootstrap_ci` para construir intervalos
    de confiança a partir de N replicas.
    """
    return [float(fabrica(s)) for s in seeds]
