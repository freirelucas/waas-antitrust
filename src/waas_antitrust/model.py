"""Classe principal do modelo WaaS e contêiner de parâmetros."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import networkx as nx
from mesa import Model
from mesa.datacollection import DataCollector

from waas_antitrust.agents import AutoridadeAgent, EmpresaAgent, TrabalhadorAgent
from waas_antitrust.calibracao.cade import INVESTIGACOES_ANUAIS_CADE

if TYPE_CHECKING:
    import pandas as pd


@dataclass
class WaaSParametros:
    """Contêiner de parâmetros do modelo.

    Valores-padrão inspirados em ordens de grandeza de Brasscom 2024 e da
    série do CADE (ver `waas_antitrust.calibracao`). Não há ajuste/calibração
    formal contra esses alvos — ver `docs/DECISIONS.md`.
    """

    # Tamanho do sistema
    n_empresas: int = 20
    tam_medio_empresa: int = 500

    # Parâmetros do mecanismo
    W_mult: float = 1.5  # recompensa em múltiplos do salário anual
    k_rel: float = 0.05  # massa crítica como fração de n_trabalhadores
    D_disc: float = 0.30  # desconto sobre contribuição pecuniária
    rho: float = 0.7  # acurácia-base da autoridade
    taxa_capacidade: float = 0.5  # fração de empresas processáveis por tique (limitada pelo CADE)
    r_represalia: float = 0.15  # probabilidade de represália
    F_falso: float = 1.0  # penalidade por falso reporte (múltiplos de w_a)
    densidade: float = 0.10  # reescrita Watts-Strogatz

    # Regime institucional
    regime: str = "B"  # "A", "B" ou "C"

    # Calibração
    fracao_violadoras: float = 0.30
    taxa_observacao: float = 0.20
    tau_ruido: float = 0.10
    sigma_etico: float = 0.5
    eta_aleatorio: float = 0.05
    delta_leniencia: float = 0.5
    w_a_base: float = 180_000.0  # salário anual (R$, Brasscom 2024)
    R_por_trabalhador: float = 1_500_000.0

    # Execução
    n_tiques: int = 40  # horizonte (10 anos em trimestres)
    seed: int = 42


class WaaSModel(Model):
    """Modelo Whistleblower-as-a-Service com três populações.

    Implementa as cinco fases do protocolo ODD (Grimm et al., JASSS 2020):
        P1 — fase de sinalização (sinal privado ruidoso; inspirada em jogo global)
        P2 — disparo de massa crítica
        P3 — decisão de pagamento da empresa (IC-F*)
        P4 — intervenção da autoridade (com restrição de capacidade)
        P5 — coleta de estado
    """

    def __init__(self, params: WaaSParametros) -> None:
        # Mesa 3.5 fornece self.rng (numpy Generator) a partir de `rng`.
        super().__init__(rng=params.seed)
        self.params = params

        self.regime = params.regime
        self.W_mult = params.W_mult
        self.k_rel = params.k_rel
        self.D_disc = params.D_disc
        self.rho = params.rho
        self.r_represalia = params.r_represalia
        self.F_falso = params.F_falso
        self.densidade = params.densidade
        self.fracao_violadoras = params.fracao_violadoras
        self.taxa_observacao = params.taxa_observacao
        self.tau_ruido = params.tau_ruido
        self.sigma_etico = params.sigma_etico
        self.eta_aleatorio = params.eta_aleatorio
        self.delta_leniencia = params.delta_leniencia
        self.w_a_base = params.w_a_base
        self.R_por_trabalhador = params.R_por_trabalhador

        self.tique: int = 0
        self.empresas: list[EmpresaAgent] = []
        self.trabalhadores_por_empresa: dict[int, list[TrabalhadorAgent]] = {}
        self.historia_sinais_por_empresa: dict[int, list[set[int]]] = {}

        # Contadores de fluxo (por tique), redefinidos a cada step.
        self.vp_tique: int = 0
        self.fp_tique: int = 0
        self.fn_tique: int = 0
        # Custo total de recompensas pagas (R$, acumulado no horizonte).
        self.custo_recompensa_acum: float = 0.0

        # Capacidade da autoridade por tique: fração das empresas do sistema,
        # limitada pela vazão trimestral do CADE (INVESTIGACOES_ANUAIS_CADE / 4).
        # O reescalonamento exato para o universo do CADE é decisão em aberto
        # (ver docs/DECISIONS.md, E01).
        capacidade_cade_trimestral = max(1, INVESTIGACOES_ANUAIS_CADE // 4)
        capacidade_por_fracao = max(1, int(params.taxa_capacidade * params.n_empresas))
        capacidade_tique = min(capacidade_por_fracao, capacidade_cade_trimestral)
        self.autoridade = AutoridadeAgent(
            self, capacidade=capacidade_tique, rho_acuracia=params.rho
        )

        self._criar_empresas(params.n_empresas, params.tam_medio_empresa)

        self.coletor = DataCollector(
            model_reporters={
                "tique": "tique",
                # Fluxos (por tique)
                "n_sinais": self._contar_sinais,
                "n_empresas_notif": self._contar_notificadas,
                "vp_tique": "vp_tique",
                "fp_tique": "fp_tique",
                "fn_tique": "fn_tique",
                # Estoques (acumulados até o tique)
                "n_tcc_assinados": self._contar_tcc,
                "n_pagou": self._contar_pagou,
                "custo_recompensa_acum": "custo_recompensa_acum",
                "verdadeiros_positivos_acum": self._contar_vp,
                "falsos_positivos_acum": self._contar_fp,
                "falsos_negativos_acum": self._contar_fn,
                "regime": "regime",
            }
        )

    # ---- coletor de métricas ----
    def _contar_sinais(self) -> int:
        return sum(
            sum(t.sinaliza_agora for t in ws) for ws in self.trabalhadores_por_empresa.values()
        )

    def _contar_notificadas(self) -> int:
        return sum(1 for e in self.empresas if e.notificada_no_periodo)

    def _contar_tcc(self) -> int:
        return sum(1 for e in self.empresas if e.tcc_assinado)

    def _contar_pagou(self) -> int:
        return sum(1 for e in self.empresas if e.pagou_denunciantes)

    def _contar_vp(self) -> int:
        return sum(
            1
            for c in self.autoridade.historico_casos
            if c["eh_violadora_real"] and c["classificada_violadora"]
        )

    def _contar_fp(self) -> int:
        return sum(
            1
            for c in self.autoridade.historico_casos
            if not c["eh_violadora_real"] and c["classificada_violadora"]
        )

    def _contar_fn(self) -> int:
        return sum(
            1
            for c in self.autoridade.historico_casos
            if c["eh_violadora_real"] and not c["classificada_violadora"]
        )

    # ---- criação ----
    def _criar_empresas(self, n_empresas: int, tam_medio: int) -> None:
        for fid in range(n_empresas):
            tam = max(50, int(self.rng.normal(tam_medio, tam_medio * 0.3)))
            eh_v = self.rng.random() < self.fracao_violadoras
            sigma = self.rng.uniform(0.3, 0.9) if eh_v else 0.0
            R = tam * self.R_por_trabalhador

            empresa = EmpresaAgent(
                self,
                id_empresa=fid,
                sigma=sigma,
                eh_violadora=eh_v,
                n_trabalhadores=tam,
                fatia_mercado=1.0 / n_empresas,
                R_receita=R,
            )
            self.empresas.append(empresa)

            k_viz = max(4, int(tam * 0.02))
            if k_viz >= tam:
                k_viz = tam - 1
            if k_viz % 2 == 1:
                k_viz += 1
            grafo_seed = int(self.rng.integers(0, 2**31 - 1))
            try:
                g = nx.watts_strogatz_graph(tam, k_viz, self.densidade, seed=grafo_seed)
            except (nx.NetworkXError, ValueError):
                g = nx.erdos_renyi_graph(tam, 0.02, seed=grafo_seed)
            empresa.grafo_interno = g

            arquetipos = self.rng.choice(
                TrabalhadorAgent.ARQUETIPOS,
                size=tam,
                p=[0.15, 0.35, 0.40, 0.10],
            )
            ws = []
            for j in range(tam):
                w_a = max(60_000, self.rng.normal(self.w_a_base, self.w_a_base * 0.25))
                k_p = max(1, int(self.k_rel * tam + self.rng.normal(0, 1)))
                t = TrabalhadorAgent(
                    self,
                    id_empresa=fid,
                    arquetipo=str(arquetipos[j]),
                    w_a=w_a,
                    k_pessoal=k_p,
                )
                t.observou = eh_v and (self.rng.random() < self.taxa_observacao)
                ws.append(t)
            empresa.trabalhadores = ws
            self.trabalhadores_por_empresa[fid] = ws
            self.historia_sinais_por_empresa[fid] = []

    def _W_esperado(self, w_a: float) -> float:
        return self.W_mult * w_a

    # ---- step ----
    def step(self) -> None:  # noqa: C901 — orquestra as 5 fases do protocolo ODD
        self.tique += 1
        W_ativo = self.regime in ("B", "C")
        D_ativo = self.regime in ("B", "C")

        # P1 · fase de sinalização
        for fid, ws in self.trabalhadores_por_empresa.items():
            empresa = self.empresas[fid]
            sinais_anteriores = (
                self.historia_sinais_por_empresa[fid][-1]
                if self.historia_sinais_por_empresa[fid]
                else set()
            )
            for idx, t in enumerate(ws):
                s_i = t.receber_sinal(empresa.sigma, self.tau_ruido) if W_ativo else None
                if empresa.grafo_interno is not None and idx in empresa.grafo_interno.nodes:
                    viz = list(empresa.grafo_interno.neighbors(idx))
                    phi = sum(1 for n in viz if n in sinais_anteriores) / max(1, len(viz))
                else:
                    phi = 0.0
                W_esp = self._W_esperado(t.w_a) if W_ativo else 0.0
                t.sinaliza_agora = (
                    bool(t.decidir_sinal(s_i, phi, W_esp, self.r_represalia, self.F_falso))
                    if W_ativo
                    else False
                )
            atuais = {i for i, t in enumerate(ws) if t.sinaliza_agora}
            self.historia_sinais_por_empresa[fid].append(atuais)

        # P2 · massa crítica
        for fid, ws in self.trabalhadores_por_empresa.items():
            empresa = self.empresas[fid]
            empresa.notificada_no_periodo = False
            n_sig = sum(1 for t in ws if t.sinaliza_agora)
            k_req = max(1, int(self.k_rel * empresa.n_trabalhadores))
            if W_ativo and n_sig >= k_req:
                empresa.notificada_no_periodo = True

        # P3 · decisão de pagamento
        for empresa in self.empresas:
            if not empresa.notificada_no_periodo:
                continue
            disparados = [t for t in empresa.trabalhadores if t.sinaliza_agora]
            W_total = sum(self._W_esperado(t.w_a) for t in disparados)
            S_esp = empresa.sancao_esperada()
            D_val = self.D_disc * S_esp if D_ativo else 0.0
            empresa.pagou_denunciantes = D_ativo and empresa.satisfaz_ic_f_estrela(W_total, D_val)
            if empresa.pagou_denunciantes:
                empresa.tcc_assinado = True
                self.custo_recompensa_acum += W_total

        # P4 · intervenção da autoridade
        for empresa in self.empresas:
            if not empresa.notificada_no_periodo:
                # canal residual independente (auto-detecção)
                if empresa.eh_violadora and self.rng.random() < 0.012:
                    self.autoridade.receber_caso(empresa, 0.4, identidades_protegidas=True)
                continue
            qualidade = 0.9 if empresa.pagou_denunciantes else 0.6
            id_prot = not empresa.pagou_denunciantes
            self.autoridade.receber_caso(empresa, qualidade, id_prot)

        resultados_tique = self.autoridade.processar_casos()
        self.vp_tique = sum(
            1 for c in resultados_tique if c["eh_violadora_real"] and c["classificada_violadora"]
        )
        self.fp_tique = sum(
            1
            for c in resultados_tique
            if not c["eh_violadora_real"] and c["classificada_violadora"]
        )
        self.fn_tique = sum(
            1
            for c in resultados_tique
            if c["eh_violadora_real"] and not c["classificada_violadora"]
        )
        self.coletor.collect(self)

    def executar(self, n_tiques: int | None = None) -> pd.DataFrame:
        """Executa o modelo por n_tiques (ou pelos parâmetros configurados)."""
        n = n_tiques if n_tiques is not None else self.params.n_tiques
        for _ in range(n):
            self.step()
        return self.coletor.get_model_vars_dataframe()
