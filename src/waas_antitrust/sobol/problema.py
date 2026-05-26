"""Definição do problema de Sobol para análise de sensibilidade global."""

PROBLEMA_SOBOL_8D: dict = {
    "num_vars": 8,
    "names": [
        "W_mult",  # recompensa / salário anual
        "k_rel",  # massa crítica como fração de n
        "D_disc",  # desconto sobre TCC
        "rho",  # acurácia da autoridade
        "r_represalia",  # probabilidade de represália
        "F_falso",  # penalidade por falso reporte
        "densidade",  # reescrita Watts-Strogatz
        "taxa_observacao",  # fração de trabalhadores que observa
    ],
    "bounds": [
        [0.5, 3.0],
        [0.01, 0.25],
        [0.10, 0.50],
        [0.30, 0.95],
        [0.05, 0.35],
        [0.0, 5.0],
        [0.01, 0.30],
        [0.10, 0.40],
    ],
}
