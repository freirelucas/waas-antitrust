"""Execução da varredura paramétrica de Sobol.

Suporta execução síncrona e assíncrona (via joblib). Para a versão definitiva
do artigo, recomenda-se `n_base = 1024` com paralelismo total.
"""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
from joblib import Parallel, delayed
from SALib.sample import sobol as sobol_amostragem

from waas_antitrust.model import WaaSModel, WaaSParametros
from waas_antitrust.sobol.problema import PROBLEMA_SOBOL_8D

# Pesos do bem-estar SOCIAL. NORMATIVOS e provisórios — calibrar em R03
# (ver docs/DECISIONS.md, R05). O bem-estar é o NEGATIVO do custo social total:
# dano (Σ violadoras·tique, R01) + custo de erro (falsos positivos) + custo da
# recompensa + custo de êxodo (Hirschman, R07) − multa arrecadada pelo Estado
# (transferência ao erário, Categoria 3 da crítica x10).
# `gamma_recompensa`=0 por ser, a rigor, transferência privada (empresa →
# denunciantes); eleve para penalizar distorções. `delta_exodo` e `delta_multa`
# entram pela Categoria 3 (Eco B) — calibrar em R03.
PESOS_BEM_ESTAR: dict[str, float] = {
    "beta_fp": 1.0,  # custo de um falso positivo (em violador-tiques equivalentes)
    "gamma_recompensa": 0.0,  # peso do custo de recompensa (normalizado por w_a)
    "delta_exodo": 0.5,  # peso do custo de êxodo materializado (normalizado por w_a)
    "delta_multa": 1.0,  # peso da multa arrecadada pelo Estado (normalizado por w_a)
    # v2.D.1 (Eco B v2): externalidade erga omnes do bem coletivo.
    # Default 0 preserva compatibilidade; ativar com epsilon > 0 sob reframe.
    "epsilon_dissuasao_difusa": 0.0,
}


def calcular_bem_estar(
    dano: float,
    fp: int,
    custo_recompensa: float,
    w_a_base: float,
    pesos: dict[str, float] | None = None,
    custo_exodo: float = 0.0,
    multa_arrecadada: float = 0.0,
    dissuasao_difusa: float = 0.0,
) -> float:
    """Bem-estar social com termo de externalidade erga omnes (v2.D).

    Fórmula:
        bem_estar = −(dano + β·FP + γ·custo + δ_ex·exodo
                      − δ_mu·multa − ε·dissuasao_difusa) / w_a

    `dano` = Σ violadoras ativas por tique (R01) ou `dano_economico_acum`
    (ponderado por fatia de mercado, Categoria 3); ambos creditam a PREVENÇÃO.
    `custo_exodo` (Hirschman, R07) é custo social de perda de capital humano
    transitória; `multa_arrecadada` é receita do erário (entra com sinal +).

    **v2.D.1 (Eco B v2, R21):** `dissuasao_difusa` é a externalidade
    positiva erga omnes do bem coletivo de massa crítica — calibrada como
    `Σ (p_perc_t − p_perc_0) · n_empresas_não_notificadas · overcharge`.
    Conta a dissuasão difusa que o WaaS gera sobre firmas que CADE/MPF
    jamais investigaria. Default 0 (compat); ativar via `pesos`.

    Mitigação de double-counting: o termo `dano` já desconta violadoras
    ativas, então `dissuasao_difusa` deve usar apenas firmas que **jamais**
    foram notificadas — não as que viraram VP no estoque.

    Pesos normativos provisórios (calibrar em R03 contra Connor-Lande
    overcharge mediano 17-19%).
    """
    pesos = pesos or PESOS_BEM_ESTAR
    custo_norm = custo_recompensa / w_a_base if w_a_base else 0.0
    exodo_norm = custo_exodo / w_a_base if w_a_base else 0.0
    multa_norm = multa_arrecadada / w_a_base if w_a_base else 0.0
    dissuasao_norm = dissuasao_difusa / w_a_base if w_a_base else 0.0
    return -(
        dano
        + pesos["beta_fp"] * fp
        + pesos["gamma_recompensa"] * custo_norm
        + pesos.get("delta_exodo", 0.0) * exodo_norm
        - pesos.get("delta_multa", 0.0) * multa_norm
        - pesos.get("epsilon_dissuasao_difusa", 0.0) * dissuasao_norm
    )


def executar_para_sobol(
    linha: Sequence[float],
    *,
    regime: str = "B",
    seed: int = 42,
    n_empresas: int = 15,
    tam_medio_empresa: int = 300,
    n_tiques: int = 24,
    replica: int = 0,
) -> dict:
    """Executa uma única configuração paramétrica.

    `VP`/`FP`/`bem_estar` são os totais acumulados ao fim do horizonte.
    """
    W_mult, k_rel, D_disc, rho, r_repres, F_falso, densidade, taxa_obs = linha
    params = WaaSParametros(
        n_empresas=n_empresas,
        tam_medio_empresa=tam_medio_empresa,
        regime=regime,
        seed=seed,
        W_mult=W_mult,
        k_rel=k_rel,
        D_disc=D_disc,
        rho=rho,
        r_represalia=r_repres,
        F_falso=F_falso,
        densidade=densidade,
        taxa_observacao=taxa_obs,
        n_tiques=n_tiques,
    )
    modelo = WaaSModel(params)
    df = modelo.executar()
    vp = int(df["verdadeiros_positivos_acum"].max())
    fp = int(df["falsos_positivos_acum"].max())
    fn = int(df["falsos_negativos_acum"].max())
    custo_recompensa = float(df["custo_recompensa_acum"].max())
    dano = int(df["dano_acumulado"].max())
    dano_economico = float(df["dano_economico_acum"].max())
    custo_exodo = float(df["custo_exodo_acum"].max())
    multa_arrecadada = float(df["multa_arrecadada_acum"].max())
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    return {
        **dict(zip(PROBLEMA_SOBOL_8D["names"], linha, strict=True)),
        "regime": regime,
        "seed": seed,
        "replica": replica,
        "VP": vp,
        "FP": fp,
        "FN": fn,
        "dano_acumulado": dano,
        "dano_economico": dano_economico,
        "custo_recompensa": custo_recompensa,
        "custo_exodo": custo_exodo,
        "multa_arrecadada": multa_arrecadada,
        "precisao": precisao,
        "bem_estar": calcular_bem_estar(
            dano,
            fp,
            custo_recompensa,
            params.w_a_base,
            custo_exodo=custo_exodo,
            multa_arrecadada=multa_arrecadada,
        ),
    }


def executar_varredura(
    n_base: int = 128,
    regime: str = "B",
    n_jobs: int = -1,
    n_empresas: int = 15,
    n_tiques: int = 24,
    seed_base: int = 42,
    n_replicas: int = 5,
    problema: dict | None = None,
) -> pd.DataFrame:
    """Executa a varredura de Sobol com replicação correta sobre seeds.

    A matriz de Saltelli é gerada uma vez. Para cada réplica ``r`` em
    ``range(n_replicas)``, a matriz **inteira** é avaliada com uma seed fixa
    (``seed_base + r``), preservando o pareamento A/B/AB_i exigido pelo
    estimador de Sobol. As linhas de cada réplica ficam na ordem original da
    matriz; os índices são calculados por réplica e mediados em
    ``analise.calcular_indices_replicado``.

    NB: alternar a seed *dentro* de uma única matriz (como em versões
    anteriores) contamina o estimador e é incorreto.

    Parameters
    ----------
    n_base : int
        Número-base N. A matriz tem N·(d+2) linhas (calc_second_order=False).
    n_replicas : int
        Número de réplicas (seeds distintas) da matriz inteira.

    Returns
    -------
    DataFrame com N·(d+2)·n_replicas linhas; colunas: parâmetros + regime +
    seed + replica + VP + FP + precisão + bem_estar.
    """
    problema = problema or PROBLEMA_SOBOL_8D
    amostras = sobol_amostragem.sample(problema, n_base, calc_second_order=False)

    tarefas = [(r, linha) for r in range(n_replicas) for linha in amostras]
    resultados = Parallel(n_jobs=n_jobs, verbose=10)(
        delayed(executar_para_sobol)(
            linha,
            regime=regime,
            seed=seed_base + r,
            n_empresas=n_empresas,
            n_tiques=n_tiques,
            replica=r,
        )
        for r, linha in tarefas
    )
    return pd.DataFrame(resultados)
