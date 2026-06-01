"""Classe principal do modelo WaaS e contêiner de parâmetros."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import networkx as nx
from mesa import Model
from mesa.datacollection import DataCollector

from waas_antitrust import condutas as condutas_mod
from waas_antitrust import hirschman
from waas_antitrust.agents import AutoridadeAgent, EmpresaAgent, TrabalhadorAgent
from waas_antitrust.calibracao.cade import INVESTIGACOES_ANUAIS_CADE
from waas_antitrust.robustez import beta_binomial_smoothing

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
    p_deteccao_prior: float = 0.15  # detecção percebida inicial (dissuasão, R01)
    lambda_expectativa: float = 0.3  # peso da expectativa adaptativa de detecção (R01)
    taxa_observacao: float = 0.20
    taxa_falso_reporte: float = (
        0.02  # prob. de reporte errôneo/malicioso por não-violadora/tique (R04)
    )
    tau_ruido: float = 0.10
    sigma_etico: float = 0.5
    eta_aleatorio: float = 0.05
    delta_leniencia: float = 0.5
    w_a_base: float = 180_000.0  # salário anual (R$, Brasscom 2024)
    R_por_trabalhador: float = 1_500_000.0

    # Hirschman exit-with-equity (R07): cláusulas contratuais de vesting
    # acelerado por gatilho de ação coletiva. Pesos provisionais (calibrar R03).
    fracao_contratos_acelerados: float = 0.0  # fração das firmas com cláusula
    peso_hirschman: float = 0.3  # peso do exit-threat no g_i preventivo
    valor_equity_por_funcionario_uw: float = 0.5  # em unidades de w_a (YC ref)
    fator_substituicao_uw: float = 0.5  # custo recrutamento/onboarding em w_a
    fracao_nao_vested: float = 0.5  # vesting 4y/1y cliff: ~50% non-vested

    # Heterogeneidade conduta × ator (R08): distribuição de papéis nos
    # trabalhadores; o catálogo de condutas vem de waas_antitrust.condutas.
    distribuicao_papeis: dict[str, float] | None = None  # None ⇒ padrão big tech

    # Suavização Beta-Binomial em p_perc (Categoria 2 da crítica x10, Mat A):
    # estimador `(vp + α) / (n_viol + α + β)` remove singularidade em
    # n_viol = 0 e estabiliza a variância em n pequeno. α=1, β=5 ⇒ prior
    # centrado em ~16,7%, próximo do default `p_deteccao_prior = 0.15`.
    alpha_beta_binomial: float = 1.0
    beta_beta_binomial: float = 5.0

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
        self.taxa_falso_reporte = params.taxa_falso_reporte
        self.p_deteccao_prior = params.p_deteccao_prior
        self.lambda_expectativa = params.lambda_expectativa
        self.tau_ruido = params.tau_ruido
        self.sigma_etico = params.sigma_etico
        self.eta_aleatorio = params.eta_aleatorio
        self.delta_leniencia = params.delta_leniencia
        self.w_a_base = params.w_a_base
        self.R_por_trabalhador = params.R_por_trabalhador
        # Hirschman exit-with-equity (R07)
        self.fracao_contratos_acelerados = params.fracao_contratos_acelerados
        self.peso_hirschman = params.peso_hirschman
        self.valor_equity_por_funcionario_uw = params.valor_equity_por_funcionario_uw
        self.fator_substituicao_uw = params.fator_substituicao_uw
        self.fracao_nao_vested = params.fracao_nao_vested
        # Heterogeneidade conduta × ator (R08): distribuição de papéis.
        self.distribuicao_papeis = (
            params.distribuicao_papeis
            if params.distribuicao_papeis is not None
            else condutas_mod.DISTRIBUICAO_PAPEIS_PADRAO
        )
        # Suavização Beta-Binomial (Categoria 2, Mat A): pseudo-contagens do prior.
        self.alpha_beta_binomial = params.alpha_beta_binomial
        self.beta_beta_binomial = params.beta_beta_binomial

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
        # Dissuasão endógena (R01): detecção percebida e contagem de violadoras ativas.
        self._g_max = params.p_deteccao_prior / max(1e-6, 1.0 - params.fracao_violadoras)
        self.p_perc: float = params.p_deteccao_prior
        self.n_violadoras_ativas: int = 0
        self.dano_acumulado: int = 0  # Σ violadoras ativas por tique (proxy de dano social)
        # Hirschman (R07): firmas sob ameaça materializada de êxodo e custo agregado.
        self.n_firmas_sob_ameaca_exodo: int = 0
        self.custo_exodo_acum: float = 0.0

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
                "n_violadoras_ativas": "n_violadoras_ativas",
                "dano_acumulado": "dano_acumulado",
                "vp_tique": "vp_tique",
                "fp_tique": "fp_tique",
                "fn_tique": "fn_tique",
                "n_firmas_sob_ameaca_exodo": "n_firmas_sob_ameaca_exodo",
                # Estoques (acumulados até o tique)
                "n_tcc_assinados": self._contar_tcc,
                "n_pagou": self._contar_pagou,
                "custo_recompensa_acum": "custo_recompensa_acum",
                "custo_exodo_acum": "custo_exodo_acum",
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
            # Atratividade de violar g_i = ganho ilícito / sanção esperada (R01).
            # A firma viola enquanto g_i > detecção percebida; _g_max calibra a
            # fração inicial de violadoras dado o prior de detecção.
            g_violacao = float(self.rng.uniform(0.0, self._g_max))
            sigma_potencial = float(self.rng.uniform(0.3, 0.9))
            eh_v = g_violacao > self.p_deteccao_prior
            sigma = sigma_potencial if eh_v else 0.0
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
            empresa.g_violacao = g_violacao
            empresa.sigma_potencial = sigma_potencial
            # Hirschman (R07): firma tem cláusula contratual de vesting acelerado
            # por gatilho de ação coletiva? Sorteio Bernoulli na população.
            empresa.tem_clausula_acelerada = bool(
                self.rng.random() < self.fracao_contratos_acelerados
            )
            # Conduta-tipo da firma (R08): qual abuso ela cometeria se violasse.
            empresa.conduta_potencial = str(
                self.rng.choice([c.nome for c in condutas_mod.CATALOGO])
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
            papeis_keys = list(self.distribuicao_papeis.keys())
            papeis_probs = list(self.distribuicao_papeis.values())
            papeis = self.rng.choice(papeis_keys, size=tam, p=papeis_probs)
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
                    papel=str(papeis[j]),
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

        # P0 · dissuasão endógena (R01): a detecção percebida é atualizada por
        # expectativa adaptativa sobre a detecção realizada no tique anterior;
        # cada firma re-decide violar enquanto sua atratividade g_i superar p_perc.
        # Categoria 2 (Mat A): estimador frequencista vp/n_viol substituído por
        # Beta-Binomial MAP `(vp + α) / (n_viol + α + β)` — sempre definido
        # (mesmo em n_viol = 0, retorna a média do prior) e estável em n pequeno.
        if self.tique > 1:
            p_realizado = beta_binomial_smoothing(
                self.vp_tique,
                self.n_violadoras_ativas,
                alpha=self.alpha_beta_binomial,
                beta=self.beta_beta_binomial,
            )
            self.p_perc = (
                1.0 - self.lambda_expectativa
            ) * self.p_perc + self.lambda_expectativa * p_realizado
        # Reset contadores de fluxo Hirschman (P3 abaixo os preenche).
        self.n_firmas_sob_ameaca_exodo = 0
        for empresa in self.empresas:
            # Hirschman preventivo (R07): firmas com cláusula têm g_i efetivo menor.
            g_ef = hirschman.g_i_efetivo(
                empresa.g_violacao,
                empresa.tem_clausula_acelerada,
                self.p_perc,
                self.peso_hirschman,
            )
            empresa.eh_violadora = g_ef > self.p_perc
            empresa.sigma = empresa.sigma_potencial if empresa.eh_violadora else 0.0
        self.n_violadoras_ativas = sum(1 for e in self.empresas if e.eh_violadora)
        self.dano_acumulado += self.n_violadoras_ativas
        for fid, ws in self.trabalhadores_por_empresa.items():
            empresa = self.empresas[fid]
            violando = empresa.eh_violadora
            # R08: observabilidade depende do par (papel × conduta). Sem conduta
            # potencial registrada, cai no taxa_observacao homogêneo (compat).
            conduta = (
                condutas_mod.lookup_conduta(empresa.conduta_potencial)
                if violando and empresa.conduta_potencial is not None
                else None
            )
            for t in ws:
                if not violando:
                    t.observou = False
                    continue
                fator = (
                    condutas_mod.observabilidade(t.papel, conduta) if conduta is not None else 1.0
                )
                t.observou = self.rng.random() < (self.taxa_observacao * fator)

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

        # P3 · decisão de pagamento (IC-F* ampliada por Hirschman, R07)
        for empresa in self.empresas:
            if not empresa.notificada_no_periodo:
                continue
            disparados = [t for t in empresa.trabalhadores if t.sinaliza_agora]
            W_total = sum(self._W_esperado(t.w_a) for t in disparados)
            S_esp = empresa.sancao_esperada()
            D_val = self.D_disc * S_esp if D_ativo else 0.0
            # Custo do êxodo se a firma não pagar (zero sem cláusula).
            w_a_medio = (
                sum(t.w_a for t in disparados) / len(disparados) if disparados else self.w_a_base
            )
            c_exodo = hirschman.custo_exodo_esperado(
                len(disparados),
                w_a_medio,
                empresa.tem_clausula_acelerada,
                fator_substituicao=self.fator_substituicao_uw,
                valor_equity_por_funcionario=self.valor_equity_por_funcionario_uw,
                fracao_nao_vested=self.fracao_nao_vested,
            )
            empresa.pagou_denunciantes = D_ativo and hirschman.deve_pagar_com_hirschman(
                W_total, D_val, c_exodo
            )
            if empresa.pagou_denunciantes:
                empresa.tcc_assinado = True
                self.custo_recompensa_acum += W_total
            elif c_exodo > 0.0:
                # Firma com cláusula que não pagou ⇒ êxodo materializa.
                self.n_firmas_sob_ameaca_exodo += 1
                self.custo_exodo_acum += c_exodo

        # P4 · intervenção da autoridade
        for empresa in self.empresas:
            if not empresa.notificada_no_periodo:
                # canal residual independente (auto-detecção)
                if empresa.eh_violadora and self.rng.random() < 0.012:
                    self.autoridade.receber_caso(empresa, 0.4, identidades_protegidas=True)
                # canal de falso reporte (R04): reporte errôneo/malicioso contra
                # não-violadora, com prova fraca — fonte de falsos positivos.
                elif (
                    not empresa.eh_violadora
                    and W_ativo
                    and self.rng.random() < self.taxa_falso_reporte
                ):
                    self.autoridade.receber_caso(empresa, 0.15, identidades_protegidas=True)
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
