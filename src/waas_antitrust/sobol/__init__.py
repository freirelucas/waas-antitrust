"""Varredura de Sobol e análise de sensibilidade global."""

from waas_antitrust.sobol.execucao import executar_para_sobol, executar_varredura
from waas_antitrust.sobol.problema import PROBLEMA_SOBOL_8D

__all__ = ["PROBLEMA_SOBOL_8D", "executar_para_sobol", "executar_varredura"]
