"""waas-antitrust · modelo baseado em agentes para o mecanismo
Whistleblower-as-a-Service em enforcement antitruste de mercados digitais.

Núcleo computacional do artigo "Rescaling Leniency Programs for Digital Markets:
A Whistleblower-as-a-Service Mechanism".

Módulos principais:
    agents     — três classes de agentes (Trabalhador, Empresa, Autoridade)
    model      — classe WaaSModel e contêiner WaaSParametros
    viz        — onze visualizações modulares para o artigo
    sobol      — varredura de Sobol e identificação da região robusta
    calibracao — parâmetros calibrados (CADE histórico, Brasscom 2024)
"""

from waas_antitrust.agents import AutoridadeAgent, EmpresaAgent, TrabalhadorAgent
from waas_antitrust.model import WaaSModel, WaaSParametros

__version__ = "0.1.0"
__all__ = [
    "TrabalhadorAgent",
    "EmpresaAgent",
    "AutoridadeAgent",
    "WaaSModel",
    "WaaSParametros",
    "__version__",
]
