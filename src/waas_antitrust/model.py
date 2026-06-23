"""Classe principal do modelo WaaS e contêiner de parâmetros."""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING

import networkx as nx
from mesa import Model
from mesa.datacollection import DataCollector

from waas_antitrust import choques as choques_mod
from waas_antitrust import condutas as condutas_mod
from waas_antitrust import hirschman
from waas_antitrust.agents import AutoridadeAgent, EmpresaAgent, TrabalhadorAgent
from waas_antitrust.calibracao.cade import INVESTIGACOES_ANUAIS_CADE
from waas_antitrust.robustez import beta_binomial_smoothing

if TYPE_CHECKING:
    import pandas as pd


#: R28 — tags jurisdicionais aceitas além de A/B/C. Cada tag mapeia para a
#: mecânica institucional equivalente; a tag original fica em
#: `WaaSModel.regime_declarado` para auditoria e relatórios.
REGIME_EQUIVALENTE: dict[str, str] = {
    "EUA": "C",  # DOJ-ATR Rewards Program 2025 sob base Dodd-Frank §922
    "UE": "A",  # DMA Whistleblower Tool: canal anônimo SEM recompensa/LCMC
}

#: Regimes aceitos por `WaaSParametros.regime`.
REGIMES_VALIDOS: frozenset[str] = frozenset({"A", "B", "C", "EUA", "UE"})


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
    D_disc: float = 0.30  # desconto TOTAL aplicável ao TCC com ressarcimento WaaS
    # **Vetor de quebra A** (D03b): o TCC clássico (Lei 12.529/2011, Art. 85)
    # **já oferece** desconto sem WaaS. Logo, o incentivo a pagar W é
    # `D_extra = D_disc − D_disc_base_tcc`, NÃO `D_disc` inteiro.
    # Default 0.0 assume que todo o desconto é WaaS-específico (compat com a
    # IC-F* simplificada). Calibrar contra Saito 2021 (média de descontos
    # observados em TCCs CADE 2012-2019).
    D_disc_base_tcc: float = 0.0
    # **Vetor de quebra B** (R13/F6): probabilidade de o TCC-WaaS ser anulado
    # judicialmente (re-caracterização da recompensa como ressarcimento
    # contestada). Default 0 preserva comportamento; ativar para falsificar F6.
    p_anulacao_tcc: float = 0.0
    rho: float = 0.7  # acurácia-base da autoridade
    taxa_capacidade: float = 0.5  # fração de empresas processáveis por tique (limitada pelo CADE)
    r_represalia: float = 0.15  # probabilidade de represália
    F_falso: float = 1.0  # penalidade por falso reporte (múltiplos de w_a)
    densidade: float = 0.10  # reescrita Watts-Strogatz

    # Regime institucional
    # "A", "B", "C" ou as tags jurisdicionais R28 "EUA"/"UE" (ver
    # REGIME_EQUIVALENTE — a tag mapeia para a mecânica equivalente e fica
    # preservada em `WaaSModel.regime_declarado`).
    regime: str = "B"

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
    # **Custo legal individual** do denunciante (em unidades de w_a). Cobre
    # honorários para reivindicar a recompensa, defesa em ação trabalhista
    # por represália e responsabilização criminal se for caracterizado
    # partícipe. Default 0 preserva compat; valor empírico realista no Brasil
    # estaria entre 0,1 e 0,5 (10–50% de um salário anual). Calibrar em R03.
    custo_legal_uw: float = 0.0

    # **R16 — Inequity aversion (Torsell 2026, Fehr-Schmidt 1999)**: peso
    # da pressão ética coletiva sobre o arquétipo "fairminded". Quando a
    # fração de vizinhos sinalizadores no tique anterior é alta, o agente
    # FM internaliza "calar é desigualdade moral" e tende a falar mais.
    # Default 0 ⇒ FM degenera em racional puro. Ativar com 0,5–2 para
    # observar o break-even ético coletivo emergente.
    peso_inequity_aversion: float = 0.0

    # **R18 — Commitment da firma (vetor de quebra D)**: probabilidade
    # PERCEBIDA pelos trabalhadores racionais e FM de a firma efetivamente
    # pagar a recompensa após a denúncia. Captura o problema clássico de
    # commitment: "se a empresa não paga, eles perdem tudo". Default 1.0
    # preserva o comportamento (W esperado = W nominal); valores realistas
    # entre 0,5 e 0,9 dependem do regime e da reputação institucional.
    prob_pagamento_perc: float = 1.0

    # **R18 — Sanção catastrófica por descumprimento do TCC**: multa adicional
    # (em múltiplos da sanção base) aplicada quando a firma assina TCC com
    # ressarcimento WaaS mas depois descumpre. Em paralelo, eleva
    # permanentemente a `p_perc` percebida pelas demais firmas (canal de
    # aprendizado coletivo). Default 0 preserva comportamento.
    multa_descumprimento_tcc: float = 0.0
    p_descumprimento_tcc: float = 0.0  # prob. de a firma descumprir após assinar

    # **R20 — Modo corrida por leniência coletiva interna** (resposta à
    # tese substantiva do autor: mercados digitais têm moat → condutas
    # unilaterais → corrida não pode ser externa, só intra-firma).
    # Sob `modo_corrida = True`, o WaaS deixa de ser incentivo isolado e
    # vira leniência coletiva interna condicionada: firma só ganha
    # atenuante se `q_min × n_trabalhadores` cooperarem na janela; o
    # desconto da firma e a recompensa do trabalhador decaem com a
    # posição na fila — ambos calibrados contra Saito (2021).
    # Default False preserva o caminho histórico integralmente.
    modo_corrida: bool = False
    q_min_cooperacao_interna: float = 0.10  # fração mínima de cooperadores
    janela_temporal_tiques: int = 4  # janela após massa crítica disparar
    perfil_decaimento: str = "saito"  # única opção implementada

    # **R26 — Erosão endógena por uso instrumental (Sociólogo v2 + Coleman 1990).**
    # Sob reframe v2, capital social organizacional é destruído pela sua
    # instrumentalização. A cada notificação em firma X, a comunicação
    # informal em outras firmas pode degradar — chilling effect. O parâmetro
    # `alpha_erosao` em [0, 1] controla a fração de degradação por notificação;
    # default 0 = sem erosão (preserva comportamento histórico). Proposição 5
    # candidata: existe `alpha_erosao*` tal que B/C colapsa em A após N tiques.
    # Literatura calibradora: Titmuss 1970, Frey-Jegen 2001, Bénabou-Tirole 2003.
    alpha_erosao: float = 0.0

    # **R27 — Canal de depósito condicional explícito** (correção radical v3,
    # balanço 360° item #1; Ayres-Unkovic 2012 *Michigan L. Rev.* 111:145).
    # Sob `usar_escrow_explicito=True`, o `AutoridadeAgent.escrow_denuncias`
    # mantém explicitamente o escrow de denúncias condicionais; quando massa
    # crítica é atingida em uma firma, **todas as denúncias se abrem
    # simultaneamente** via `abrir_escrow_se_massa_critica`. Sob default
    # `False`, o escrow é mantido implicitamente em P2.5 do WaaSModel —
    # comportamento idêntico ao histórico. Refator é SEMÂNTICO (não muda
    # resultado bit-a-bit); explicita que o CADE é o portador do escrow,
    # não a firma.
    usar_escrow_explicito: bool = False

    # **R27-ii — Janela de expiração do depósito condicional** (Δt da definição
    # LCMC v3). Quando > 0, depósitos com idade ≥ `janela_escrow_tiques` tiques
    # são removidos do escrow no início de cada P2.5b (antes da abertura). É a
    # janela do **depósito individual** — distinta de `janela_temporal_tiques`
    # (R20, janela agregada da corrida pós-massa-crítica). Default 0 preserva
    # comportamento histórico (escrow eterno, leitura Callisto).
    janela_escrow_tiques: int = 0

    # **R29 — Janela de adesão pós-abertura com desconto progressivo por classe.**
    # Quando uma firma atinge massa crítica e o escrow é aberto, abre-se uma
    # janela de `janela_adesao_pos_abertura` tiques durante a qual trabalhadores
    # da MESMA firma que NÃO depositaram ainda podem aderir à "classe dos
    # lenientes" e receber desconto progressivo por ordem de chegada. Espelha
    # a fila clássica da Lei 12.529/2011 Art. 86 (Spagnolo 2004), mas operada
    # DENTRO da firma já aberta — incentivo de cascata pós-coordenação.
    # `descontos_faixas_adesao[k]` é o fator aplicado ao W (recompensa) para
    # quem aderir na k-ésima posição da fila pós-abertura; posição ≥ N usa o
    # último elemento. Default `janela_adesao_pos_abertura=0` desliga o
    # mecanismo (compat estrita).
    janela_adesao_pos_abertura: int = 0
    descontos_faixas_adesao: tuple = (1.0, 0.7, 0.5, 0.3, 0.1)
    # R29-iii: decisão de adesão estocástica por arquétipo (opt-in).
    # Sob False (default), decisão determinística IR-W (fator * W > custo).
    # Sob True, cada arquétipo decide com probabilidade própria — captura
    # heterogeneidade comportamental clássica do modelo: ético adere
    # frequentemente (0,85), imitativo segue Granovetter (fração de
    # aderentes), racional mantém IR-W, fairminded ganha bônus 0,2 quando
    # massa atravessa 0,3 (inequity coletivo), oportunista 0,8 fixo,
    # aleatório 0,3 fixo. Detalhe em AutoridadeAgent._decidir_adesao.
    adesao_estocastica_por_arquetipo: bool = False

    # **R30 — Sinergia entre autoridades internacionais (LCMC global coordenada).**
    # Modela o cenário "e se todas as autoridades antitruste adotassem LCMC".
    # Duas alavancas independentes:
    #   (i) `grupos_economicos`: list[int] de tamanho `n_empresas` mapeando
    #       cada firma a um grupo econômico. Firmas no mesmo grupo (jurisdições
    #       diferentes da mesma multinacional) podem consolidar depósitos sob
    #       `usar_escrow_consolidado_grupo=True`: a massa crítica é avaliada
    #       no NÍVEL DO GRUPO (sum de depósitos / sum de trabalhadores), e a
    #       abertura simultânea aciona todas as firmas do grupo de uma vez —
    #       paralelo direto da cooperação inter-autoridades via MoU bilateral
    #       (CADE-DOJ-ATR 2019; DG-COMP-CADE 2009).
    #  (ii) `coordenacao_internacional ∈ [0, 1]`: fator que amplifica o sinal
    #       Schelling erga omnes (R21/v2.D.1). Cada abertura em qualquer firma
    #       eleva `p_perc` em TODAS as outras firmas por `coordenacao * delta`,
    #       capturando o efeito ICN/OECD de notícias e comunicados conjuntos.
    # Default `grupos_economicos=None` (cada firma é seu grupo);
    # `usar_escrow_consolidado_grupo=False` e `coordenacao_internacional=0.0`
    # preservam o comportamento histórico bit-a-bit.
    grupos_economicos: tuple | None = None
    usar_escrow_consolidado_grupo: bool = False
    coordenacao_internacional: float = 0.0
    # R30-ii: assimetria entre jurisdições. Mapa fid → multiplicador do
    # tamanho da firma (em torno de tam_medio_empresa). None preserva
    # comportamento histórico (firmas todas com tamanho médio). Permite
    # configurar, por exemplo, BR=0.3, US=1.5, EU=1.0 dentro de um mesmo
    # grupo multinacional, refletindo o desbalanceamento real entre
    # filiais. Aplicado em _criar_empresas.
    multiplicador_tamanho_por_firma: tuple | None = None
    # R30-iii: forum shopping. Sob True, firma notificada em uma
    # jurisdição pode tentar TCC clássico antes do gatilho global fechar
    # — captura o risco substantivo da R30 ("e se a firma corre para
    # TCC amistoso?"). Decisão em P3 quando notificada_no_periodo é True
    # e o grupo ainda não atingiu massa crítica consolidada. Modulado por
    # prob_tcc_classico_pre_consolidado ∈ [0, 1].
    forum_shopping_ativo: bool = False
    prob_tcc_classico_pre_consolidado: float = 0.5
    # **R29-iv — Recompensa coletiva (Marwell-Oliver 1993; Macy 1991)** como
    # salvaguarda anti-erosão Coleman (item #17 do brainstorm de revisão).
    # Sob True, a recompensa total W de uma abertura é dividida igualmente
    # entre depositantes originais + aderentes pós-abertura (em vez de cada
    # um receber W cheio). Desincentiva uso instrumental individual e
    # preserva o substrato cooperativo organizacional. Tensiona com R20
    # (Saito por posição), por isso default False.
    recompensa_coletiva_pos_abertura: bool = False

    # **R02a — Jogo global no arquétipo racional** (Mat B na crítica x10).
    # Quando True, o arquétipo "racional" usa o **limiar de switching x\***
    # do subgame de Morris-Shin (`jogo_global.limiar_switching`) como gatilho
    # de decisão — derivação analítica em vez de comparação IR-W direta.
    # Fecha R02a do backlog e integra a Prop. 2 ao ABM. Default False
    # preserva o caminho histórico (IR-W ↔ ganho líquido direto).
    usar_x_estrela_no_racional: bool = False

    # **R19 — Choques exógenos discretos** (Eurace@Unibi; resposta a "como o
    # modelo lida com choques?"). Lista de `Choque` (módulo `choques`)
    # aplicados in-place no início de cada step quando `choque.tique == tique`.
    # Default None preserva o modelo estacionário-estocástico.
    choques: tuple = ()  # type: ignore[assignment]
    # Multiplicador da represália percebida por ex-funcionários — sem vínculo
    # a perder, o `r` efetivo cai. Default 0,2 (perde 80% do peso).
    fator_represalia_ex_funcionario: float = 0.2

    # **R13a — Distribuição de fatia de mercado** (resposta a Eco B/PM e à
    # observação de que dano em digital é cauda longa, não uniforme).
    # "uniforme" preserva 1/n_empresas (compat com testes existentes).
    # "pareto" sorteia s_i ~ Pareto(alpha_pareto) + 1 e normaliza — α=1,16
    # reproduz a regra 80/20 clássica; valores menores intensificam a cauda.
    # "lognormal" sorteia s_i ~ LogNormal(0, sigma_lognormal) e normaliza.
    distribuicao_fatia_mercado: str = "uniforme"  # "uniforme" | "pareto" | "lognormal"
    alpha_pareto: float = 1.16  # regra 80/20; menor ⇒ cauda mais longa
    sigma_lognormal: float = 1.0

    # Hirschman exit-with-equity (R07): cláusulas contratuais de vesting
    # acelerado por gatilho de ação coletiva. Pesos provisionais (calibrar R03).
    fracao_contratos_acelerados: float = 0.0  # fração das firmas com cláusula
    peso_hirschman: float = 0.3  # peso do exit-threat no g_i preventivo
    valor_equity_por_funcionario_uw: float = 0.5  # em unidades de w_a (YC ref)
    fator_substituicao_uw: float = 0.5  # custo recrutamento/onboarding em w_a
    fracao_nao_vested: float = 0.5  # vesting 4y/1y cliff: ~50% non-vested
    # Categoria 4 (Adv B): haircut IRPF + INSS sobre vesting acelerado no BR
    # (default 0 = versão bruta histórica; ~0,4 reflete a realidade tributária).
    aliquota_tributaria_vesting: float = 0.0

    # R14: enriquecimento heterogêneo dos agentes (canais ortogonais a R01).
    # Empresa: cultura de compliance reduz σ efetivo (programa de integridade).
    peso_cultura_compliance: float = 0.0  # ω em σ_ef = σ · (1 − ω · cultura)
    # Trabalhador: dispersão da tolerância à represália em torno de 1.0.
    sigma_tolerancia_represalia: float = 0.0  # 0 ⇒ todos com tol=1 (compat); 0,2 ativa
    # Autoridade: especialização em mercados digitais (modula ρ na P4).
    prioridade_digital_autoridade: float = 0.0  # 0 ⇒ ρ_ef = ρ; 1 ⇒ ρ_ef = 1
    # Distribuição de tempo de carreira (exponencial, em anos; cliff de 1 ano).
    media_anos_carreira: float = 3.0

    # Heterogeneidade conduta × ator (R08): distribuição de papéis nos
    # trabalhadores; o catálogo de condutas vem de waas_antitrust.condutas.
    distribuicao_papeis: dict[str, float] | None = None  # None ⇒ padrão big tech

    # R16: distribuição dos arquétipos de comportamento dentro da firma.
    # None ⇒ Hokamp-Pickhardt clássico (15/35/40/10/0, sem fairminded).
    # Para ativar fairminded, passar dict com soma 1. Os cenários em
    # `waas_antitrust.cenarios` fornecem presets calibrados.
    distribuicao_arquetipos: dict[str, float] | None = None

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

        # R28: tags jurisdicionais explícitas. "EUA" e "UE" são rótulos
        # institucionais que mapeiam para a mecânica A/B/C equivalente:
        #   "EUA" → "C" (recompensa com base estatutária robusta —
        #            Dodd-Frank §922 / DOJ-ATR Rewards Program 2025);
        #   "UE"  → "A" (DMA Whistleblower Tool é canal individual anônimo
        #            SEM recompensa e SEM escrow LCMC — Diretiva 2019/1937
        #            dá proteção, não incentivo).
        # `regime_declarado` preserva a tag original para auditoria;
        # `regime` carrega a mecânica e mantém todo o downstream intacto.
        if params.regime not in REGIMES_VALIDOS:
            raise ValueError(
                f"regime desconhecido: {params.regime!r}. " f"Válidos: {sorted(REGIMES_VALIDOS)}."
            )
        self.regime_declarado = params.regime
        self.regime = REGIME_EQUIVALENTE.get(params.regime, params.regime)
        self.W_mult = params.W_mult
        self.k_rel = params.k_rel
        self.D_disc = params.D_disc
        self.D_disc_base_tcc = params.D_disc_base_tcc
        self.p_anulacao_tcc = params.p_anulacao_tcc
        self.custo_legal_uw = params.custo_legal_uw
        self.peso_inequity_aversion = params.peso_inequity_aversion
        self.prob_pagamento_perc = params.prob_pagamento_perc
        self.multa_descumprimento_tcc = params.multa_descumprimento_tcc
        self.p_descumprimento_tcc = params.p_descumprimento_tcc
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
        # Hirschman exit-with-equity (R07).
        # Categoria 4 (Adv B): gating jurídico — cláusula contratual de vesting
        # acelerado por ação coletiva só é instrumento institucionalmente
        # disponível sob Regime C (via lei). Resolução do CADE (Regime B) é
        # infralegal e, por reserva de lei (Art. 22, I, CF), não pode impor
        # cláusula trabalhista. Sob A/B, força fracao_contratos_acelerados=0.
        fc = params.fracao_contratos_acelerados
        if fc > 0.0 and self.regime in ("A", "B"):
            warnings.warn(
                f"fracao_contratos_acelerados={fc:.3f} > 0 é incoerente com Regime "
                f"{self.regime!r} (reserva de lei, Art. 22, I, CF — só Regime C pode "
                f"impor cláusula contratual padrão). Forçando para 0.0.",
                UserWarning,
                stacklevel=2,
            )
            fc = 0.0
        self.fracao_contratos_acelerados = fc
        self.peso_hirschman = params.peso_hirschman
        self.valor_equity_por_funcionario_uw = params.valor_equity_por_funcionario_uw
        self.fator_substituicao_uw = params.fator_substituicao_uw
        self.fracao_nao_vested = params.fracao_nao_vested
        self.aliquota_tributaria_vesting = params.aliquota_tributaria_vesting
        # R14: pesos da heterogeneidade adicional dos agentes.
        self.peso_cultura_compliance = params.peso_cultura_compliance
        self.sigma_tolerancia_represalia = params.sigma_tolerancia_represalia
        self.prioridade_digital_autoridade = params.prioridade_digital_autoridade
        self.media_anos_carreira = params.media_anos_carreira
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
        self.p_perc_0: float = params.p_deteccao_prior  # baseline para v2.D.1
        self.n_violadoras_ativas: int = 0
        self.dano_acumulado: int = 0  # Σ violadoras ativas por tique (proxy de dano social)
        # v2.D.1 (Eco B v2, R21): externalidade erga omnes do bem coletivo.
        # Acumula (p_perc_t - p_perc_0) × n_empresas_não_notificadas × overcharge.
        # Mede dissuasão difusa: firmas que CADE/MPF nunca investigariam mas
        # passam a ser dissuadidas pelo sinal Schelling. Calibrado contra
        # Connor-Lande 17-19% overcharge mediano.
        self.valor_dissuasao_difusa_acum: float = 0.0
        # Set de empresas já notificadas: usado para evitar double-counting
        # no termo de externalidade (firmas que viraram VP já estão em `dano`).
        self._empresas_ja_notificadas: set[int] = set()
        # v2.B.4 (Sociólogo v2, R26): capital social residual com risco de
        # erosão por uso instrumental (Coleman 1990). A previsão Coleman é que
        # após uma rodada bem-sucedida de denúncia em firma X, a comunicação
        # informal em outras firmas Y, Z muda de regime — chilling effect
        # sobre cooperação espontânea. Proxy: fração de pares (`phi_vizinhos`)
        # como capital social ativo agregado pelas firmas. Erosão é controlada
        # por `alpha_erosao` (default 0 = sem erosão; Proposição 5 candidata).
        self.capital_social_residual: float = 1.0  # baseline normalizado [0, 1]
        self.alpha_erosao: float = getattr(params, "alpha_erosao", 0.0)
        # Histórico do reporter (para auditoria + figura).
        self.capital_social_residual_hist: list[float] = []
        # Hirschman (R07): firmas sob ameaça materializada de êxodo e custo agregado.
        self.n_firmas_sob_ameaca_exodo: int = 0
        self.custo_exodo_acum: float = 0.0
        # Bem-estar substantivo (Categoria 3, Eco B): dano ponderado por
        # fatia de mercado (R$ proporcional, em vez de contagem) e multa
        # arrecadada pelo Estado (TCC ⇒ residual; sem TCC ⇒ multa cheia).
        self.dano_economico_acum: float = 0.0
        self.multa_arrecadada_acum: float = 0.0
        # Vetores de quebra (R15): contadores cumulativos
        self.n_tcc_anulados: int = 0  # F6: TCC anulado por re-caracterização rejeitada
        self.n_firmas_optaram_tcc_classico: int = 0  # firma preferiu TCC clássico vs. WaaS
        # R18: firma assinou TCC, recebeu W, e descumpriu — "perdem tudo"
        self.n_firmas_quebraram_tcc: int = 0
        self.multa_descumprimento_acum: float = 0.0
        # R19: contadores de choques aplicados (diagnóstico).
        self.n_choques_layoff_aplicados: int = 0
        self.n_choques_paradigmaticos_aplicados: int = 0
        self.n_choques_campanha_aplicados: int = 0
        self.n_choques_juridicos_aplicados: int = 0
        # R19: lista de choques a aplicar; aceita tuple (catálogo) ou list.
        self.choques: tuple = tuple(params.choques) if params.choques else ()
        self.fator_represalia_ex_funcionario = params.fator_represalia_ex_funcionario
        # R02a: integrar `jogo_global.x*` no arquétipo racional (opt-in).
        self.usar_x_estrela_no_racional = params.usar_x_estrela_no_racional
        # R27: canal de depósito condicional explícito (opt-in; default preserva
        # comportamento histórico onde o escrow é implícito em P2.5).
        self.usar_escrow_explicito = getattr(params, "usar_escrow_explicito", False)
        # R27-ii: janela de expiração do depósito individual (Δt). Default 0
        # = escrow eterno (leitura Callisto).
        self.janela_escrow_tiques = getattr(params, "janela_escrow_tiques", 0)
        # R29: janela de adesão pós-abertura com desconto progressivo. Default
        # 0 desliga o mecanismo (compat estrita).
        self.janela_adesao_pos_abertura = getattr(params, "janela_adesao_pos_abertura", 0)
        self.descontos_faixas_adesao = tuple(
            getattr(params, "descontos_faixas_adesao", (1.0, 0.7, 0.5, 0.3, 0.1))
        )
        # R29-iii: adesão estocástica por arquétipo (opt-in)
        self.adesao_estocastica_por_arquetipo = getattr(
            params, "adesao_estocastica_por_arquetipo", False
        )
        # R30: sinergia entre autoridades internacionais. Grupos econômicos
        # consolidam depósitos (proxy de MoU bilateral / cooperação ICN);
        # coordenacao_internacional amplifica o sinal Schelling erga omnes.
        # Default: cada firma em seu próprio grupo (sem consolidação) +
        # coordenação 0 (sem amplificação) ⇒ comportamento histórico.
        grupos_param = getattr(params, "grupos_economicos", None)
        if grupos_param is None:
            self.grupos_economicos = tuple(range(params.n_empresas))
        else:
            self.grupos_economicos = tuple(grupos_param)
        if len(self.grupos_economicos) != params.n_empresas:
            raise ValueError(
                "grupos_economicos deve ter tamanho n_empresas "
                f"({params.n_empresas}); recebido {len(self.grupos_economicos)}."
            )
        self.usar_escrow_consolidado_grupo = getattr(params, "usar_escrow_consolidado_grupo", False)
        self.coordenacao_internacional = float(getattr(params, "coordenacao_internacional", 0.0))
        # R30-ii: assimetria entre jurisdições — multiplicadores de tamanho.
        mult_param = getattr(params, "multiplicador_tamanho_por_firma", None)
        if mult_param is not None and len(mult_param) != params.n_empresas:
            raise ValueError(
                "multiplicador_tamanho_por_firma deve ter tamanho n_empresas "
                f"({params.n_empresas}); recebido {len(mult_param)}."
            )
        self.multiplicador_tamanho_por_firma = tuple(mult_param) if mult_param is not None else None
        # R30-iii: forum shopping ativo.
        self.forum_shopping_ativo = getattr(params, "forum_shopping_ativo", False)
        self.prob_tcc_classico_pre_consolidado = float(
            getattr(params, "prob_tcc_classico_pre_consolidado", 0.5)
        )
        # R29-iv: recompensa coletiva pós-abertura (Marwell-Oliver 1993).
        self.recompensa_coletiva_pos_abertura = getattr(
            params, "recompensa_coletiva_pos_abertura", False
        )
        # R30: contador cumulativo de aberturas consolidadas a nível de grupo.
        self.n_aberturas_consolidadas_grupo_acum: int = 0
        # R30: contador de boosts erga omnes aplicados via coordenação intl.
        self.n_boosts_coordenacao_intl_acum: int = 0
        # R30-iii: contador de firmas que fugiram via forum shopping.
        self.n_forum_shopping_acum: int = 0
        # R20 — Modo corrida + filas
        self.modo_corrida = params.modo_corrida
        self.q_min_cooperacao_interna = params.q_min_cooperacao_interna
        self.janela_temporal_tiques = params.janela_temporal_tiques
        self.perfil_decaimento = params.perfil_decaimento
        # Importação tardia para evitar circularidade.
        from waas_antitrust.corrida import FilaLeniencia

        self.fila_leniencia: FilaLeniencia = FilaLeniencia()
        # Filas internas por firma — preenchidas em _criar_empresas.
        self.filas_internas: dict[int, object] = {}
        # Contadores cumulativos para diagnóstico (R20).
        self.n_firmas_atingiram_massa_critica_interna: int = 0
        self.custo_recompensa_corrida_acum: float = 0.0

        # Capacidade da autoridade por tique: fração das empresas do sistema,
        # limitada pela vazão trimestral do CADE (INVESTIGACOES_ANUAIS_CADE / 4).
        # O reescalonamento exato para o universo do CADE é decisão em aberto
        # (ver docs/DECISIONS.md, E01).
        capacidade_cade_trimestral = max(1, INVESTIGACOES_ANUAIS_CADE // 4)
        capacidade_por_fracao = max(1, int(params.taxa_capacidade * params.n_empresas))
        capacidade_tique = min(capacidade_por_fracao, capacidade_cade_trimestral)
        self.autoridade = AutoridadeAgent(
            self,
            capacidade=capacidade_tique,
            rho_acuracia=params.rho,
            prioridade_digital=params.prioridade_digital_autoridade,
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
                "dano_economico_acum": "dano_economico_acum",
                "multa_arrecadada_acum": "multa_arrecadada_acum",
                # v2.D.1 (Eco B v2, R21): externalidade erga omnes do bem coletivo.
                "valor_dissuasao_difusa_acum": "valor_dissuasao_difusa_acum",
                # v2.B.4 (Sociólogo v2, R26): capital social residual com risco
                # de erosão por uso instrumental (Coleman 1990).
                "capital_social_residual": "capital_social_residual",
                # R27 (balanço 360° item #1): reporters do canal de depósito
                # condicional explícito. Sob `usar_escrow_explicito=False`,
                # ambos ficam em 0 (compat).
                "n_denuncias_em_escrow": self._contar_denuncias_em_escrow,
                "n_aberturas_simultaneas_acum": self._contar_aberturas_simultaneas,
                "n_depositos_expirados_acum": self._contar_depositos_expirados,
                # R29: janela de adesão pós-abertura. Sob
                # `janela_adesao_pos_abertura=0`, ambos ficam em 0 (compat).
                "n_aderentes_pos_abertura_acum": self._contar_aderentes_pos_abertura,
                "n_blocos_em_janela_adesao_acum": self._contar_blocos_em_janela_adesao,
                # R30: sinergia entre autoridades internacionais. Sob
                # `usar_escrow_consolidado_grupo=False` e
                # `coordenacao_internacional=0.0`, ambos ficam em 0 (compat).
                "n_aberturas_consolidadas_grupo_acum": ("n_aberturas_consolidadas_grupo_acum"),
                "n_boosts_coordenacao_intl_acum": "n_boosts_coordenacao_intl_acum",
                # R30-iii: firmas que fugiram via forum shopping (TCC clássico
                # antes do gatilho consolidado fechar). Sob
                # `forum_shopping_ativo=False`, sempre 0.
                "n_forum_shopping_acum": "n_forum_shopping_acum",
                "n_tcc_anulados": "n_tcc_anulados",
                "n_firmas_optaram_tcc_classico": "n_firmas_optaram_tcc_classico",
                "n_firmas_quebraram_tcc": "n_firmas_quebraram_tcc",
                "multa_descumprimento_acum": "multa_descumprimento_acum",
                "hhi": self._hhi,
                "n_ex_funcionarios": self._contar_ex_funcionarios,
                "n_choques_layoff_aplicados": "n_choques_layoff_aplicados",
                "n_choques_paradigmaticos_aplicados": "n_choques_paradigmaticos_aplicados",
                "n_firmas_atingiram_massa_critica_interna": (
                    "n_firmas_atingiram_massa_critica_interna"
                ),
                "custo_recompensa_corrida_acum": "custo_recompensa_corrida_acum",
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
        # v2.D.1: aproveita o reporter para atualizar `_empresas_ja_notificadas`
        # (set acumulado de firmas que foram notificadas em algum tique). Mantém
        # `valor_dissuasao_difusa_acum` apenas creditando firmas NUNCA notificadas.
        for e in self.empresas:
            if e.notificada_no_periodo:
                self._empresas_ja_notificadas.add(e.unique_id)
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

    def _contar_denuncias_em_escrow(self) -> int:
        """R27: total de denúncias condicionais ainda em escrow (não-abertas).

        Sob `usar_escrow_explicito=False`, sempre 0 — o escrow é implícito
        em P2.5. Sob `True`, conta `n_denuncias_em_escrow` do AutoridadeAgent.
        """
        return getattr(self.autoridade, "n_denuncias_em_escrow", 0)

    def _contar_aberturas_simultaneas(self) -> int:
        """R27: total cumulativo de aberturas simultâneas (massa crítica
        atingida ⇒ todas as denúncias depositadas para a firma se abrem
        ao mesmo tempo). Sob `usar_escrow_explicito=False`, sempre 0."""
        return getattr(self.autoridade, "n_aberturas_simultaneas_acum", 0)

    def _contar_depositos_expirados(self) -> int:
        """R27-ii: total cumulativo de depósitos removidos por expiração via
        `janela_escrow_tiques`. Sob `usar_escrow_explicito=False` ou
        `janela_escrow_tiques=0`, sempre 0 (compat)."""
        return getattr(self.autoridade, "n_depositos_expirados_acum", 0)

    def _contar_aderentes_pos_abertura(self) -> int:
        """R29: total cumulativo de adesões pós-abertura via janela de
        desconto progressivo. Sob `janela_adesao_pos_abertura=0`, sempre 0."""
        return getattr(self.autoridade, "n_aderentes_pos_abertura_acum", 0)

    def _contar_blocos_em_janela_adesao(self) -> int:
        """R29: total cumulativo de blocos que entraram em janela de adesão
        (firmas em que massa crítica disparou e a janela foi aberta). Sob
        `janela_adesao_pos_abertura=0`, sempre 0."""
        return getattr(self.autoridade, "n_blocos_em_janela_adesao_acum", 0)

    def _contar_ex_funcionarios(self) -> int:
        """Total de trabalhadores com `status='ex_funcionario'` (R19)."""
        return sum(
            sum(1 for t in ws if t.status == "ex_funcionario")
            for ws in self.trabalhadores_por_empresa.values()
        )

    def _contar_fn(self) -> int:
        return sum(
            1
            for c in self.autoridade.historico_casos
            if c["eh_violadora_real"] and not c["classificada_violadora"]
        )

    # ---- criação ----
    def _sortear_fatias_mercado(self, n: int) -> list[float]:
        """Vetor de fatias de mercado, normalizado para soma 1.

        Três modos (R13a):
        - `uniforme`: `[1/n, ..., 1/n]` (default, compat).
        - `pareto`: `Pareto(α=alpha_pareto) + 1`, normalizado. Reflete a
          regra 80/20 e cauda longa típica de mercados digitais.
        - `lognormal`: `LogNormal(0, σ=sigma_lognormal)`, normalizado.

        O default uniforme preserva o comportamento histórico do modelo.
        """
        dist = self.params.distribuicao_fatia_mercado
        if dist == "pareto":
            raw = self.rng.pareto(self.params.alpha_pareto, size=n) + 1.0
        elif dist == "lognormal":
            raw = self.rng.lognormal(mean=0.0, sigma=self.params.sigma_lognormal, size=n)
        elif dist == "uniforme":
            return [1.0 / n] * n
        else:
            raise ValueError(
                f"distribuicao_fatia_mercado desconhecida: {dist!r}. "
                "Válidas: 'uniforme', 'pareto', 'lognormal'."
            )
        total = float(raw.sum())
        return [float(x) / total for x in raw]

    def _hhi(self) -> float:
        """Índice Herfindahl-Hirschman = Σ s_i² (concentração de mercado).

        Para n firmas uniformes: HHI = 1/n. Maior ⇒ mais concentrado.
        """
        return float(sum(e.fatia_mercado**2 for e in self.empresas))

    def _criar_empresas(self, n_empresas: int, tam_medio: int) -> None:
        fatias = self._sortear_fatias_mercado(n_empresas)
        for fid in range(n_empresas):
            tam = max(50, int(self.rng.normal(tam_medio, tam_medio * 0.3)))
            # R30-ii: aplica multiplicador de tamanho por firma (assimetria
            # entre jurisdições). Default None preserva comportamento histórico.
            if self.multiplicador_tamanho_por_firma is not None:
                tam = max(50, int(tam * self.multiplicador_tamanho_por_firma[fid]))
            # Atratividade de violar g_i = ganho ilícito / sanção esperada (R01).
            # A firma viola enquanto g_i > detecção percebida; _g_max calibra a
            # fração inicial de violadoras dado o prior de detecção.
            g_violacao = float(self.rng.uniform(0.0, self._g_max))
            sigma_potencial = float(self.rng.uniform(0.3, 0.9))
            eh_v = g_violacao > self.p_deteccao_prior
            sigma = sigma_potencial if eh_v else 0.0
            R = tam * self.R_por_trabalhador

            # R14: cultura de compliance sorteada por firma (U[0, 1]); a magnitude
            # do efeito sobre σ é controlada por `peso_cultura_compliance`.
            cultura = float(self.rng.uniform(0.0, 1.0))
            empresa = EmpresaAgent(
                self,
                id_empresa=fid,
                sigma=sigma,
                eh_violadora=eh_v,
                n_trabalhadores=tam,
                fatia_mercado=fatias[fid],
                R_receita=R,
                cultura_compliance=cultura,
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

            # Distribuição padrão dos arquétipos. O quinto slot — "fairminded"
            # (R16, Torsell 2026) — e o sexto slot — "oportunista" (R24, Cient.
            # Político v2 + Sociólogo v2) — recebem 0 por default para preservar
            # a calibração histórica de 4 tipos (Hokamp-Pickhardt 2010). Quando
            # `peso_inequity_aversion > 0` ou `fracao_oportunistas > 0`,
            # recomenda-se redistribuir via `params.distribuicao_arquetipos` —
            # cenários em `cenarios.py`.
            if self.params.distribuicao_arquetipos is None:
                probs_arq = [0.15, 0.35, 0.40, 0.10, 0.0, 0.0]
            else:
                probs_arq = [
                    self.params.distribuicao_arquetipos.get(a, 0.0)
                    for a in TrabalhadorAgent.ARQUETIPOS
                ]
            arquetipos = self.rng.choice(
                TrabalhadorAgent.ARQUETIPOS,
                size=tam,
                p=probs_arq,
            )
            papeis_keys = list(self.distribuicao_papeis.keys())
            papeis_probs = list(self.distribuicao_papeis.values())
            papeis = self.rng.choice(papeis_keys, size=tam, p=papeis_probs)
            ws = []
            for j in range(tam):
                w_a = max(60_000, self.rng.normal(self.w_a_base, self.w_a_base * 0.25))
                k_p = max(1, int(self.k_rel * tam + self.rng.normal(0, 1)))
                # R14: tempo de carreira (Exp média configurável, em anos),
                # truncado em [0, 8]. Derivado a fração vested individual.
                anos = float(self.rng.exponential(self.media_anos_carreira))
                anos = max(0.0, min(8.0, anos))
                # Tolerância individual à represália (multiplicador em torno de 1).
                # `sigma_tolerancia_represalia = 0` ⇒ todos iguais (compat).
                if self.sigma_tolerancia_represalia > 0:
                    tol = float(self.rng.normal(1.0, self.sigma_tolerancia_represalia))
                    tol = max(0.2, min(2.0, tol))
                else:
                    tol = 1.0
                t = TrabalhadorAgent(
                    self,
                    id_empresa=fid,
                    arquetipo=str(arquetipos[j]),
                    w_a=w_a,
                    k_pessoal=k_p,
                    papel=str(papeis[j]),
                    anos_carreira=anos,
                    tolerancia_represalia=tol,
                )
                t.observou = eh_v and (self.rng.random() < self.taxa_observacao)
                ws.append(t)
            empresa.trabalhadores = ws
            self.trabalhadores_por_empresa[fid] = ws
            self.historia_sinais_por_empresa[fid] = []
            # R20: cada firma tem sua fila intra-firma de cooperadores.
            from waas_antitrust.corrida import FilaInternaCooperacao

            self.filas_internas[fid] = FilaInternaCooperacao(empresa_id=fid)

    def _W_esperado(self, w_a: float) -> float:
        return self.W_mult * w_a

    # ---- R30: sinergia entre autoridades internacionais ----

    def _firmas_por_grupo(self) -> dict[int, list[int]]:
        """Indexa firmas por grupo econômico para reuso (R30)."""
        out: dict[int, list[int]] = {}
        for fid, grupo in enumerate(self.grupos_economicos):
            out.setdefault(grupo, []).append(fid)
        return out

    def _gatilho_grupo_atingido(self, fids: list[int]) -> bool:
        """Soma depósitos e trabalhadores; True se massa crítica consolidada."""
        if len(fids) < 2:
            return False
        total_deposito = sum(len(self.autoridade.escrow_denuncias.get(fid, [])) for fid in fids)
        total_trab = sum(self.empresas[fid].n_trabalhadores for fid in fids)
        if total_trab <= 0 or total_deposito <= 0:
            return False
        return total_deposito / total_trab >= self.q_min_cooperacao_interna

    def _abrir_escrow_consolidado_por_grupo(self) -> set[int]:
        """Dispara abertura simultânea no NÍVEL DO GRUPO ECONÔMICO.

        Para cada grupo, soma depósitos e trabalhadores de todas as firmas
        do grupo. Se `fracao_grupo = sum(depósitos) / sum(trabalhadores) >=
        q_min`, **todas as firmas do grupo** com depósito não-vazio têm seu
        escrow aberto simultaneamente — emula a abertura coordenada por
        MoU bilateral (CADE-DOJ-ATR 2019; DG-COMP-CADE 2009; ICN MoU 2001).

        Devolve o set de ids de firmas que foram abertas via gatilho de
        grupo (para o caller pular o passo individual).
        """
        abertas: set[int] = set()
        for fids in self._firmas_por_grupo().values():
            if not self._gatilho_grupo_atingido(fids):
                continue
            abertas_neste_grupo: set[int] = set()
            for fid in fids:
                if not self.autoridade.escrow_denuncias.get(fid):
                    continue
                abriu = self.autoridade.abrir_escrow_se_massa_critica(
                    id_empresa=fid,
                    q_min=0.0,  # gatilho já validado no nível do grupo
                    n_trabalhadores_firma=self.empresas[fid].n_trabalhadores,
                )
                if abriu:
                    abertas_neste_grupo.add(fid)
            if abertas_neste_grupo:
                abertas.update(abertas_neste_grupo)
                self.n_aberturas_consolidadas_grupo_acum += 1
        return abertas

    def _aplicar_coordenacao_internacional(self, abertas_via_grupo: set[int]) -> None:
        """Boost erga omnes da detecção percebida `p_perc` proporcional ao
        nº de aberturas no tique corrente (individuais + consolidadas).

        Captura o efeito ICN/OECD: cada caso aberto em qualquer jurisdição
        sob LCMC vira notícia e eleva a percepção de detecção em todas as
        firmas globalmente. O boost é multiplicativo sobre o gap residual
        de detecção (1 - p_perc) e capado pelo limite `_g_max` do R01.
        """
        n_aberturas_tique = sum(1 for e in self.empresas if e.notificada_no_periodo) + len(
            abertas_via_grupo
        )
        if n_aberturas_tique <= 0:
            return
        # Fator de boost: coordenação × log(1 + nº aberturas) — saturação
        # natural para evitar dominar a dinâmica.
        import math

        boost = self.coordenacao_internacional * math.log1p(n_aberturas_tique) * 0.05
        novo = min(self._g_max, self.p_perc + boost * (1 - self.p_perc))
        self.p_perc = novo
        self.n_boosts_coordenacao_intl_acum += 1

    # ---- step ----
    def step(self) -> None:  # noqa: C901 — orquestra as 5 fases do protocolo ODD
        self.tique += 1
        # R19 — Choques exógenos aplicados no tique corrente, antes de P0.
        for choque in self.choques:
            if choque.tique == self.tique:
                choques_mod.aplicar_choque(self, choque)
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
            # R14: cultura de compliance atenua a severidade efetiva σ. Canal
            # ortogonal ao R01 (dissuasão por detecção): mesmo violando, firma
            # com cultura forte viola menos pesadamente.
            sigma_efetiva = empresa.sigma_potencial * max(
                0.0, 1.0 - self.peso_cultura_compliance * empresa.cultura_compliance
            )
            empresa.sigma = sigma_efetiva if empresa.eh_violadora else 0.0
        self.n_violadoras_ativas = sum(1 for e in self.empresas if e.eh_violadora)
        self.dano_acumulado += self.n_violadoras_ativas
        # Categoria 3 (Eco B): dano ponderado pela fatia de mercado da violadora.
        # Sob fatias uniformes (1/n_empresas), colapsa em `dano_acumulado/n_empresas`;
        # com fatias heterogêneas (Pareto/lognormal — pendente em R03/E05), uma
        # violação de firma de 40% conta muito mais que uma de 2%.
        self.dano_economico_acum += sum(e.fatia_mercado for e in self.empresas if e.eh_violadora)
        # v2.D.1 (Eco B v2, R21): externalidade erga omnes do bem coletivo.
        # (p_perc_t - p_perc_0) > 0 indica que a aprendizagem do sistema sobre
        # detecção subiu — firmas não-notificadas se beneficiam dessa dissuasão
        # difusa. Calibrado contra Connor-Lande overcharge mediano 17-19%.
        # Mitigação double-counting: SÓ conta empresas que jamais foram notificadas.
        delta_p = max(0.0, self.p_perc - self.p_perc_0)
        n_nao_notificadas = sum(
            1 for e in self.empresas if e.unique_id not in self._empresas_ja_notificadas
        )
        overcharge_proxy = 0.18  # Connor-Lande mediana — calibrar em R03
        self.valor_dissuasao_difusa_acum += delta_p * n_nao_notificadas * overcharge_proxy
        # v2.B.4 (Sociólogo v2, R26): erosão do capital social residual.
        # Cada notificação nova no tique reduz `capital_social_residual` por
        # `alpha_erosao` aplicado sobre a fração de firmas notificadas. Proxy
        # do chilling effect Coleman: instrumentalização degrada substrato.
        # Quando `alpha_erosao = 0` (default), `capital_social_residual = 1.0`
        # constante — preserva comportamento histórico.
        if self.alpha_erosao > 0.0:
            n_notif_novas = self._contar_notificadas()
            fracao_erosao = n_notif_novas / max(1, len(self.empresas)) if n_notif_novas > 0 else 0.0
            self.capital_social_residual = max(
                0.0, self.capital_social_residual * (1.0 - self.alpha_erosao * fracao_erosao)
            )
        self.capital_social_residual_hist.append(self.capital_social_residual)
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
                # R19 — Ex-funcionário com memória preserva capacidade de
                # sinalizar (não depende de a firma estar violando agora).
                if t.status == "ex_funcionario" and t.historico_observou > 0:
                    t.observou = True
                    continue
                if not violando:
                    t.observou = False
                    continue
                fator = (
                    condutas_mod.observabilidade(t.papel, conduta) if conduta is not None else 1.0
                )
                t.observou = self.rng.random() < (self.taxa_observacao * fator)
                if t.observou:
                    t.historico_observou += 1

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
            # R20: registra cada cooperador na fila intra-firma (idempotente).
            if self.modo_corrida:
                fila_interna = self.filas_internas[fid]
                for idx, t in enumerate(ws):
                    if t.sinaliza_agora and t.posicao_corrida_interna is None:
                        pos = fila_interna.registrar(idx, self.tique)
                        t.posicao_corrida_interna = pos
                        t.tique_cooperou = self.tique

        # P2 · massa crítica
        for fid, ws in self.trabalhadores_por_empresa.items():
            empresa = self.empresas[fid]
            empresa.notificada_no_periodo = False
            n_sig = sum(1 for t in ws if t.sinaliza_agora)
            k_req = max(1, int(self.k_rel * empresa.n_trabalhadores))

            # R27: sob `usar_escrow_explicito=True`, cada sinal do tique vira
            # um DEPÓSITO CONDICIONAL no escrow do CADE (não notifica a firma
            # imediatamente). A abertura simultânea é decidida em P2.5 quando
            # massa crítica intra-firma for atingida.
            if W_ativo and self.usar_escrow_explicito:
                for t in ws:
                    if t.sinaliza_agora:
                        # Qualidade da prova varia por papel × conduta (já
                        # implícita na probabilidade de observação); aqui
                        # registramos depósito com qualidade base 0.5.
                        self.autoridade.depositar_condicional(
                            id_empresa=fid,
                            id_trabalhador=getattr(t, "unique_id", 0),
                            qualidade_prova=0.5,
                            tique=self.tique,
                        )

            if W_ativo and n_sig >= k_req:
                empresa.notificada_no_periodo = True
                empresa.n_denuncias_acum += 1  # R14: memória da firma

        # P2.5 · R20: massa crítica interna + posicionamento na fila de leniência
        if self.modo_corrida:
            from waas_antitrust.corrida import massa_critica_interna_atingida

            for fid in self.trabalhadores_por_empresa:
                empresa = self.empresas[fid]
                if empresa.massa_critica_interna_satisfeita:
                    continue
                fila_interna = self.filas_internas[fid]
                if massa_critica_interna_atingida(
                    n_cooperadores=len(fila_interna),
                    n_trabalhadores=empresa.n_trabalhadores,
                    q_min=self.q_min_cooperacao_interna,
                ):
                    empresa.massa_critica_interna_satisfeita = True
                    empresa.tique_atingiu_massa_critica = self.tique
                    empresa.posicao_fila_leniencia = self.fila_leniencia.registrar(
                        empresa.id_empresa, self.tique
                    )
                    self.n_firmas_atingiram_massa_critica_interna += 1

        # P2.5b · R27: abertura simultânea do escrow quando massa crítica é
        # atingida em uma firma. Sob `usar_escrow_explicito=False`, é no-op.
        if self.usar_escrow_explicito:
            # R27-ii: expira depósitos antigos ANTES da abertura — depósito
            # vencido não pode contar para a fração de massa crítica.
            self.autoridade.expirar_depositos_condicionais(
                tique_atual=self.tique,
                janela=self.janela_escrow_tiques,
            )
            # R30: sob `usar_escrow_consolidado_grupo=True`, primeiro tenta
            # abertura consolidada em nível de GRUPO ECONÔMICO. Grupos com
            # massa crítica consolidada disparam abertura simultânea em TODAS
            # as firmas do grupo (paralelo de cooperação inter-autoridades).
            # Firmas já abertas pelo gatilho consolidado ficam marcadas e o
            # passo individual seguinte as ignora.
            abertas_via_grupo: set[int] = set()
            if self.usar_escrow_consolidado_grupo:
                abertas_via_grupo = self._abrir_escrow_consolidado_por_grupo()
            # R30-iii: expõe o conjunto para a fase P3 (forum shopping).
            self._firmas_abertas_consolidado_neste_tique = abertas_via_grupo
            for fid in self.trabalhadores_por_empresa:
                if fid in abertas_via_grupo:
                    # Já aberta pelo gatilho consolidado.
                    if self.janela_adesao_pos_abertura > 0:
                        self.autoridade.registrar_bloco_em_adesao(
                            id_empresa=fid,
                            tique_abertura=self.tique,
                        )
                    continue
                empresa = self.empresas[fid]
                abriu = self.autoridade.abrir_escrow_se_massa_critica(
                    id_empresa=fid,
                    q_min=self.q_min_cooperacao_interna,
                    n_trabalhadores_firma=empresa.n_trabalhadores,
                )
                # R29: registra bloco em janela de adesão se acabou de abrir.
                if abriu and self.janela_adesao_pos_abertura > 0:
                    self.autoridade.registrar_bloco_em_adesao(
                        id_empresa=fid,
                        tique_abertura=self.tique,
                    )
            # R30: amplificação Schelling internacional. Cada abertura no
            # tique (individual + consolidada) eleva `p_perc` em todas as
            # OUTRAS firmas por um fator proporcional a `coordenacao_internacional`.
            if self.coordenacao_internacional > 0:
                self._aplicar_coordenacao_internacional(abertas_via_grupo)

        # P2.5c · R29: janela de adesão pós-abertura com desconto progressivo.
        # Para cada bloco aberto dentro da janela ativa, oferece adesão a
        # trabalhadores da MESMA firma que ainda não cooperaram. Desconto
        # decai conforme `descontos_faixas_adesao`. Sob `janela_adesao_pos_abertura=0`
        # é no-op (compat estrita).
        if self.usar_escrow_explicito and self.janela_adesao_pos_abertura > 0:
            self.autoridade.processar_adesao_pos_abertura(
                tique_atual=self.tique,
                janela=self.janela_adesao_pos_abertura,
                descontos=self.descontos_faixas_adesao,
                trabalhadores_por_empresa=self.trabalhadores_por_empresa,
                W_max=self._W_esperado(1.0),
                custo_represalia=self.r_represalia,
                estocastica_por_arquetipo=self.adesao_estocastica_por_arquetipo,
                rng=self.rng,
            )

        # P3 · decisão de pagamento (IC-F* ampliada por Hirschman, R07).
        # **Vetor de quebra A**: a IC-F* correta compara W contra o INCREMENTO
        # de desconto que o canal WaaS oferece (`D_extra = D_total − D_base`),
        # não contra o desconto total. Sem isso, o modelo superestima o
        # incentivo a pagar — porque o TCC clássico já oferece desconto.
        for empresa in self.empresas:
            if not empresa.notificada_no_periodo:
                continue
            # R30-iii: forum shopping. Se a firma foi notificada apenas
            # localmente (sem gatilho consolidado no grupo) e o flag está
            # ligado, ela tenta TCC clássico antes que o gatilho global feche
            # — captura o risco "firma corre para jurisdição amistosa".
            if self.forum_shopping_ativo and self.usar_escrow_consolidado_grupo:
                consolidados = getattr(self, "_firmas_abertas_consolidado_neste_tique", set())
                grupo_disparou_consolidado = empresa.id_empresa in consolidados
                if (
                    not grupo_disparou_consolidado
                    and self.rng.random() < self.prob_tcc_classico_pre_consolidado
                ):
                    # Foge: assina TCC clássico, desliga notificação, sai de
                    # cena para o resto do tique. Não usa instrumento WaaS.
                    empresa.tcc_assinado = True
                    self.n_forum_shopping_acum += 1
                    self.n_firmas_optaram_tcc_classico += 1
                    continue
            disparados = [t for t in empresa.trabalhadores if t.sinaliza_agora]
            S_esp = empresa.sancao_esperada()
            # R20 — Sob modo_corrida, recompensa por trabalhador e desconto da
            # firma são funções da posição na fila (calibradas contra Saito).
            if self.modo_corrida and empresa.massa_critica_interna_satisfeita:
                from waas_antitrust.corrida import decaimento_D, decaimento_W

                # W por trabalhador via decaimento por posição na fila intra.
                W_total = 0.0
                for t in disparados:
                    pos = t.posicao_corrida_interna or 1
                    W_total += decaimento_W(pos, self._W_esperado(t.w_a), self.perfil_decaimento)
                # D total via decaimento por posição inter-firma (Saito).
                pos_firma = empresa.posicao_fila_leniencia or 1
                d_frac = decaimento_D(pos_firma, self.perfil_decaimento)
                D_total = d_frac * S_esp if D_ativo else 0.0
                # Sob corrida, D_base = 0 (o desconto já vem do gradiente Saito).
                D_base = 0.0
                D_extra = D_total
            else:
                W_total = sum(self._W_esperado(t.w_a) for t in disparados)
                # R29-iv: sob recompensa coletiva, W total é dividido entre
                # depositantes originais + aderentes pós-abertura — Marwell &
                # Oliver 1993; Macy 1991. Desincentiva uso instrumental
                # individual; salvaguarda anti-erosão Coleman.
                if self.recompensa_coletiva_pos_abertura and self.usar_escrow_explicito:
                    reg = self.autoridade.blocos_em_janela_adesao.get(empresa.id_empresa)
                    n_partilhantes = len(disparados)
                    if reg is not None:
                        n_partilhantes += len(reg.get("aderentes_pos_abertura", []))
                    n_partilhantes = max(1, n_partilhantes)
                    W_total = W_total / n_partilhantes
                D_total = self.D_disc * S_esp if D_ativo else 0.0
                D_base = self.D_disc_base_tcc * S_esp if D_ativo else 0.0
                D_extra = max(0.0, D_total - D_base)  # incentivo marginal do WaaS
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
                aliquota_tributaria=self.aliquota_tributaria_vesting,
            )
            empresa.pagou_denunciantes = D_ativo and hirschman.deve_pagar_com_hirschman(
                W_total, D_extra, c_exodo
            )
            if empresa.pagou_denunciantes:
                empresa.tcc_assinado = True
                self.custo_recompensa_acum += W_total
                if self.modo_corrida and empresa.massa_critica_interna_satisfeita:
                    self.custo_recompensa_corrida_acum += W_total
                # **R18 — sanção catastrófica por descumprimento**: a firma
                # pode, após assinar e pagar W, descumprir o TCC. Sorteio com
                # `p_descumprimento_tcc`. Se sortear, sofre multa adicional
                # `multa_descumprimento_tcc · sancao_base` — "se não cumpre
                # depois de assinar, perde tudo". Captura o lado-firma do
                # commitment problem (simétrico ao trabalhador).
                if (
                    self.p_descumprimento_tcc > 0.0
                    and self.rng.random() < self.p_descumprimento_tcc
                ):
                    empresa.tcc_assinado = False
                    empresa.pagou_denunciantes = False
                    self.n_firmas_quebraram_tcc += 1
                    self.multa_descumprimento_acum += self.multa_descumprimento_tcc * S_esp
            else:
                # Firma decidiu não pagar W. Se há D_base > 0, ela ainda pode
                # optar pelo TCC clássico (Art. 85, sem ressarcimento WaaS) —
                # contado como vetor de quebra A materializado.
                if D_base > 0.0:
                    self.n_firmas_optaram_tcc_classico += 1
                if c_exodo > 0.0:
                    # Firma com cláusula que não pagou ⇒ êxodo materializa.
                    self.n_firmas_sob_ameaca_exodo += 1
                    self.custo_exodo_acum += c_exodo

        # P4 · intervenção da autoridade
        # R27: sob `usar_escrow_explicito=True`, os casos das firmas notificadas
        # já foram injetados via `abrir_escrow_se_massa_critica` em P2.5b.
        # P4 trata apenas dos canais residuais (auto-detecção + falso reporte).
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
            if self.usar_escrow_explicito:
                # Caso já foi injetado via escrow em P2.5b — não duplicar.
                continue
            qualidade = 0.9 if empresa.pagou_denunciantes else 0.6
            id_prot = not empresa.pagou_denunciantes
            self.autoridade.receber_caso(empresa, qualidade, id_prot)

        resultados_tique = self.autoridade.processar_casos()
        self.vp_tique = sum(
            1 for c in resultados_tique if c["eh_violadora_real"] and c["classificada_violadora"]
        )
        # Categoria 3 (Eco B): multa arrecadada pelo Estado nesse tique. VP que
        # assinou TCC paga apenas o residual (sanção · (1−D_disc)); VP sem TCC
        # paga a multa cheia. **Vetor de quebra B (R15)**: TCC-WaaS pode ser
        # anulado por contestação judicial (F6) — quando anulado, a empresa
        # paga a multa cheia.
        for c in resultados_tique:
            if not (c["eh_violadora_real"] and c["classificada_violadora"]):
                continue
            emp = self.empresas[c["id_empresa"]]
            sancao = emp.sancao_esperada()
            tcc_valido = emp.tcc_assinado and emp.pagou_denunciantes
            # Sorteia anulação judicial do TCC se ativo.
            if tcc_valido and self.p_anulacao_tcc > 0.0 and self.rng.random() < self.p_anulacao_tcc:
                tcc_valido = False
                emp.tcc_assinado = False
                self.n_tcc_anulados += 1
            fator = (1.0 - self.D_disc) if tcc_valido else 1.0
            self.multa_arrecadada_acum += sancao * fator
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
