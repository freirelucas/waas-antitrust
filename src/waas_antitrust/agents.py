"""Três classes de agentes do modelo WaaS.

Trabalhador
    Funcionário de uma grande empresa de tecnologia, com arquétipo
    heterogêneo (Hokamp & Pickhardt, Int. Economic Journal 24(4), 2010).

Empresa
    Grande empresa de tecnologia, com tipo {violadora, não-violadora} e
    decisão de pagamento da recompensa segundo a condição IC-F*.

Autoridade
    Entidade do tipo CADE, com restrição de capacidade κ no espírito de
    Harrington & Chang (Journal of Law and Economics 58(2), 2015) e
    acurácia ρ.
"""

from __future__ import annotations

import networkx as nx
import numpy as np
from mesa import Agent, Model


class TrabalhadorAgent(Agent):
    """Funcionário de uma grande empresa de tecnologia.

    Arquétipos (Hokamp & Pickhardt, 2010):
        ético     — sinaliza se severidade percebida supera limiar pessoal
        imitativo — sinaliza se fração de vizinhos sinalizadores ≥ 30%
        racional  — ponderação custo-benefício explícita (IR-W e IC-T)
        aleatório — ruído uniforme com probabilidade eta
    """

    ARQUETIPOS = ("ético", "imitativo", "racional", "aleatório")

    def __init__(
        self,
        modelo: Model,
        id_empresa: int,
        arquetipo: str,
        w_a: float,
        k_pessoal: int,
    ) -> None:
        super().__init__(modelo)
        self.id_empresa = id_empresa
        self.arquetipo = arquetipo
        self.w_a = w_a
        self.k_pessoal = k_pessoal
        self.observou: bool = False
        self.sinaliza_agora: bool = False

    def receber_sinal(self, sigma: float, tau: float) -> float | None:
        """Sinal privado σ + ε, ε ~ N(0, τ²) (inspirado em jogo global; sem cálculo de equilíbrio)."""
        if not self.observou:
            return None
        return sigma + self.model.rng.normal(0, tau)

    def decidir_sinal(
        self,
        s_i: float | None,
        phi_vizinhos: float,
        W_esperado: float,
        r: float,
        F_falso: float,
    ) -> int:
        """Retorna 1 se sinaliza nesta rodada, 0 caso contrário."""
        if not self.observou:
            return 0

        if self.arquetipo == "ético":
            return 1 if (s_i is not None and s_i > self.model.sigma_etico) else 0

        if self.arquetipo == "imitativo":
            return 1 if phi_vizinhos >= 0.30 else 0

        if self.arquetipo == "racional":
            if s_i is None:
                return 0
            # IR-W: W ≥ r · 2·w_a (custo esperado de represália)
            custo_esperado = r * 2.0 * self.w_a
            # IC-T: penalidade esperada por falso reporte
            prob_verdadeiro = 1.0 / (1.0 + np.exp(-5.0 * (s_i - 0.5)))
            penalidade_esperada = (1.0 - prob_verdadeiro) * 0.5 * F_falso * self.w_a
            return 1 if (W_esperado - custo_esperado - penalidade_esperada > 0) else 0

        if self.arquetipo == "aleatório":
            return 1 if self.model.rng.random() < self.model.eta_aleatorio else 0

        return 0

    def step(self) -> None:
        """Os passos do trabalhador são orquestrados pelo modelo (fases P1–P5)."""
        return


class EmpresaAgent(Agent):
    """Grande empresa de tecnologia.

    Tipo θ ∈ {V, V̄} (violadora ou não). Decisão de pagamento (IC-F*):
    paga se D > W (e o regime permite).
    """

    def __init__(
        self,
        modelo: Model,
        id_empresa: int,
        sigma: float,
        eh_violadora: bool,
        n_trabalhadores: int,
        fatia_mercado: float,
        R_receita: float,
    ) -> None:
        super().__init__(modelo)
        self.id_empresa = id_empresa
        self.sigma = sigma
        self.eh_violadora = eh_violadora
        self.n_trabalhadores = n_trabalhadores
        self.fatia_mercado = fatia_mercado
        self.R = R_receita
        self.notificada_no_periodo: bool = False
        self.pagou_denunciantes: bool = False
        self.tcc_assinado: bool = False
        self.trabalhadores: list[TrabalhadorAgent] = []
        self.grafo_interno: nx.Graph | None = None

    def sancao_esperada(self) -> float:
        """E[S] escalada por σ. Faixa CADE: 0,1% a 20% da receita afetada."""
        base = 0.05 * self.R
        return base * (1.0 + self.sigma)

    def satisfaz_ic_f_estrela(self, W_total: float, D_val: float) -> bool:
        """IC-F*: a firma paga as recompensas se o desconto no TCC supera o custo (D > W)."""
        return D_val > W_total

    def step(self) -> None:
        return None


class AutoridadeAgent(Agent):
    """Autoridade do tipo CADE.

    Capacidade κ (casos por tique) e acurácia ρ. Casos não-aceitos por
    restrição de capacidade são descartados (Harrington-Chang 2015).
    """

    def __init__(self, modelo: Model, capacidade: int, rho_acuracia: float) -> None:
        super().__init__(modelo)
        self.capacidade = capacidade
        self.rho = rho_acuracia
        self.casos_neste_tique: list[dict] = []
        self.historico_casos: list[dict] = []

    def receber_caso(
        self,
        empresa: EmpresaAgent,
        qualidade_prova: float,
        identidades_protegidas: bool,
    ) -> None:
        self.casos_neste_tique.append(
            {
                "id_empresa": empresa.id_empresa,
                "eh_violadora_real": empresa.eh_violadora,
                "qualidade_prova": qualidade_prova,
                "id_protegidas": identidades_protegidas,
                "tique": self.model.tique,
            }
        )

    def processar_casos(self) -> list[dict]:
        aceitos = self.casos_neste_tique[: self.capacidade]
        resultados = []
        for caso in aceitos:
            classificada_violadora = (
                caso["eh_violadora_real"]
                if self.model.rng.random() < self.rho
                else not caso["eh_violadora_real"]
            )
            resultados.append({**caso, "classificada_violadora": classificada_violadora})
        self.historico_casos.extend(resultados)
        self.casos_neste_tique = []
        return resultados

    def step(self) -> None:
        return None
