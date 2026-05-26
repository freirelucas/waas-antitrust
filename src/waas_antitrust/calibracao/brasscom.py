"""Calibração contra dados Brasscom 2024.

Fontes primárias:
    - Brasscom, *Monitor de Empregos e Salários* (09/04/2024): 2.064.059
      trabalhadores no macrossetor de TIC em fevereiro de 2024.
    - Brasscom, *Relatório Setorial 2024* (publicado em julho de 2025):
      2.100.886 vagas formais, 3,8% do emprego formal nacional, 6,5% do PIB.
      Trabalhadores do setor de software ganham aproximadamente 3 vezes o
      salário médio nacional.
"""

PARAMS_BRASSCOM_2024: dict = {
    "trabalhadores_tic_total": 2_064_059,  # Monitor fev/2024
    "vagas_formais_tic_2024": 2_100_886,  # Relatório Setorial 2024
    "fracao_pib_tic": 0.065,  # 6,5% do PIB
    "fracao_emprego_formal_tic": 0.038,  # 3,8% do emprego formal
    "razao_salarial_tic_software_vs_nacional": 3.0,
    "salario_anual_software_medio_brl": 180_000,  # estimativa para o modelo
}

# Estimativa de funcionários em subsidiárias brasileiras das grandes empresas
# de tecnologia (Google, Meta, Microsoft, Apple, Amazon).
# Triangulação: dados públicos limitados; usar entre 30.000 e 50.000 para o modelo.
BIG_TECH_BRASIL_EMPREGADOS_ESTIMATIVA: tuple[int, int] = (30_000, 50_000)
