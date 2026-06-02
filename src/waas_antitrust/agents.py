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

    Heterogeneidade adicional (R14, exploratório):
        anos_carreira              — tempo na firma (distrib. exponencial em P0)
        fracao_vested_individual   — derivado: 0 se < 1 ano (cliff); min(1, anos/4)
        tolerancia_represalia      — multiplicador individual do custo esperado
                                     de represália (heterogeneidade ~ N(1, 0,15))
        historico_observou         — memória: nº de tiques em que observou
    """

    ARQUETIPOS = ("ético", "imitativo", "racional", "aleatório")

    def __init__(
        self,
        modelo: Model,
        id_empresa: int,
        arquetipo: str,
        w_a: float,
        k_pessoal: int,
        papel: str = "outro",
        anos_carreira: float = 2.0,
        tolerancia_represalia: float = 1.0,
    ) -> None:
        super().__init__(modelo)
        self.id_empresa = id_empresa
        self.arquetipo = arquetipo
        self.w_a = w_a
        self.k_pessoal = k_pessoal
        self.papel = papel  # R08: time funcional na firma (afeta observabilidade)
        # R14: heterogeneidade individual (carreira, vesting, tolerância).
        self.anos_carreira = anos_carreira
        self.tolerancia_represalia = tolerancia_represalia
        self.observou: bool = False
        self.sinaliza_agora: bool = False
        self.historico_observou: int = 0

    @property
    def fracao_vested_individual(self) -> float:
        """Fração vested do equity, dada `anos_carreira` (4y vesting, 1y cliff).

        Antes do cliff (anos < 1): 0. Depois: linear até 1 em 4 anos.
        """
        if self.anos_carreira < 1.0:
            return 0.0
        return min(1.0, self.anos_carreira / 4.0)

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
        """Retorna 1 se sinaliza nesta rodada, 0 caso contrário.

        O custo esperado de represália é modulado por `tolerancia_represalia`
        (R14): trabalhadores mais tolerantes ao risco têm custo efetivo menor.
        """
        if not self.observou:
            return 0

        if self.arquetipo == "ético":
            return 1 if (s_i is not None and s_i > self.model.sigma_etico) else 0

        if self.arquetipo == "imitativo":
            return 1 if phi_vizinhos >= 0.30 else 0

        if self.arquetipo == "racional":
            if s_i is None:
                return 0
            # IR-W: W ≥ r · tol · 2·w_a (R14: tolerância individual a represália)
            custo_esperado = r * self.tolerancia_represalia * 2.0 * self.w_a
            # **Vetor de quebra C** (R15): custo legal individual do denunciante.
            # Advogado para reivindicar a recompensa, defesa em ação trabalhista
            # se houver represália, e potencial responsabilização criminal se
            # caracterizado partícipe (Art. 86 — Lei 12.529/2011, colisão com
            # leniência clássica). `custo_legal_uw` em unidades de w_a.
            custo_legal = getattr(self.model, "custo_legal_uw", 0.0) * self.w_a
            # IC-T: penalidade esperada por falso reporte
            prob_verdadeiro = 1.0 / (1.0 + np.exp(-5.0 * (s_i - 0.5)))
            penalidade_esperada = (1.0 - prob_verdadeiro) * 0.5 * F_falso * self.w_a
            ganho_liquido = W_esperado - custo_esperado - custo_legal - penalidade_esperada
            return 1 if ganho_liquido > 0 else 0

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

    Heterogeneidade adicional (R14, exploratório):
        cultura_compliance — ∈ [0, 1]; modula a severidade efetiva da conduta
                             ``sigma_efetiva = sigma_potencial · (1 − ω·cultura)``.
                             Captura programa de integridade, conselho de ética,
                             treinamento — sem alterar a Proposição 3 (canal
                             ortogonal ao WaaS).
        poder_retaliacao   — proporcional a `fatia_mercado`; modula o custo
                             efetivo de represália percebido pelo trabalhador.
        n_denuncias_acum   — memória: nº de denúncias internas já sofridas
                             (proxy de pressão reputacional).
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
        cultura_compliance: float = 0.0,
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
        self.g_violacao: float = 0.0  # atratividade de violar = ganho/sanção (R01)
        self.sigma_potencial: float = sigma  # severidade quando ativa a violação
        self.tem_clausula_acelerada: bool = False  # vesting acelerado em ação coletiva (R07)
        self.conduta_potencial: str | None = None  # tipo de conduta se eh_violadora (R08)
        # R14: heterogeneidade institucional / poder relativo.
        self.cultura_compliance = cultura_compliance
        self.poder_retaliacao: float = fatia_mercado  # proxy: posição dominante
        self.n_denuncias_acum: int = 0

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

    Heterogeneidade adicional (R14, exploratório):
        prioridade_digital — ∈ [0, 1]; modula a acurácia em condutas digitais
                             ``rho_efetivo = rho + (1 − rho)·prioridade``.
                             Captura especialização institucional (CGAA/CADE
                             Departamento de Estudos Econômicos sobre digital).
                             Default 0 preserva o comportamento original.
    """

    def __init__(
        self,
        modelo: Model,
        capacidade: int,
        rho_acuracia: float,
        prioridade_digital: float = 0.0,
    ) -> None:
        super().__init__(modelo)
        self.capacidade = capacidade
        self.rho = rho_acuracia
        self.prioridade_digital = prioridade_digital
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
        # R14: acurácia base é elevada por `prioridade_digital` (especialização
        # institucional da autoridade em mercados digitais). Default 0 preserva
        # o comportamento original (rho_efetivo == rho).
        rho_efetivo = self.rho + (1.0 - self.rho) * self.prioridade_digital
        for caso in aceitos:
            # A acurácia cresce com a qualidade da prova: p_correto = ρ + (1−ρ)·q.
            # Provas melhores (canal WaaS) ⇒ classificação mais confiável.
            p_correto = min(1.0, rho_efetivo + (1.0 - rho_efetivo) * caso["qualidade_prova"])
            acerta = self.model.rng.random() < p_correto
            classificada_violadora = (
                caso["eh_violadora_real"] if acerta else not caso["eh_violadora_real"]
            )
            resultados.append({**caso, "classificada_violadora": classificada_violadora})
        self.historico_casos.extend(resultados)
        self.casos_neste_tique = []
        return resultados

    def step(self) -> None:
        return None
