"""Cenários normativos como variantes paramétricas (R17, exploratório).

Cada cenário aqui é um **conjunto de alterações regulatórias** que altera
parâmetros do `WaaSModel`. A motivação vem da crítica do autor: tratar
alterações normativas como **cenários comparáveis**, não como notas de
rodapé textuais.

O catálogo cobre o espectro de:

- **Status quo BR** (Regime A, sem qualquer alteração);
- **Resolução pura** (Regime B atual — Art. 12 da Res. CADE 21/2018);
- **Resolução + portaria MTE** (B com proteção trabalhista reforçada);
- **Lei WaaS pura** (Regime C — extensão da Lei 13.608/2018);
- **Lei WaaS com fundo público de honorários** (Estado paga advogado);
- **Lei WaaS com cláusula padrão de vesting acelerado** (Hirschman R07);
- **Sanção catastrófica** (qualquer regime + multa por descumprimento do TCC);
- **Cenários v2 R21-R25** (massa crítica observável, dois instrumentos,
  crédito tributário, leniência criminal, captura processamento, uso
  adversarial);
- **Variantes EUA/UE R28** (DOJ-ATR Rewards Program 2025; DMA Whistleblower
  Tool 2024) — generalidade do mecanismo a partir da pesquisa de fundo 2026.
- **Canal puro R27-i + erosão Coleman R26** (`apenas_canal_sem_instrumento`,
  `erosao_coleman_adversarial`) — fechamento do backlog da correção v3:
  testar o canal sem instrumento monetário e medir erosão endógena.

Cada cenário é um dict de **sobrescritas** de parâmetros — aplicar via
`aplicar_cenario(params, cenario_id)` produz um novo `WaaSParametros` com
as alterações em vigor.

Referências teóricas que motivam essa modularidade:
- Torsell (2026) sobre inequity aversion e evolução de preferências;
- Skyrms (1996) sobre evolução do contrato social;
- Bolton & Ockenfels (2000) sobre ERC.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from waas_antitrust.calibracao.saito import d_base_tcc_calibrado

if TYPE_CHECKING:
    from waas_antitrust.model import WaaSParametros


# Fonte única para o desconto base do TCC clássico (Lei 12.529/2011, Art. 85).
# Consulta `calibracao/saito.py`: usa Saito (2021) se preenchido, ou cai para
# o default histórico documentado (0,10). Quando a extração manual da tabela
# principal de Saito for concluída, todos os cenários abaixo herdam o valor
# real sem mudança neste módulo.
_D_BASE_TCC: float = d_base_tcc_calibrado(default=0.10)


@dataclass(frozen=True)
class Cenario:
    """Alteração normativa pré-empacotada.

    `descricao` é a interpretação institucional do cenário; `sobrescritas`
    são os campos de `WaaSParametros` que mudam ao aplicar.
    """

    nome: str
    descricao: str
    sobrescritas: dict[str, object] = field(default_factory=dict)


#: Distribuição de arquétipos calibrada para ativar fairminded sob R16.
#: Mantém Hokamp-Pickhardt como núcleo (~75% do peso) e dá 20% ao FM.
DISTRIBUICAO_COM_FAIRMINDED: dict[str, float] = {
    "ético": 0.10,
    "imitativo": 0.30,
    "racional": 0.30,
    "fairminded": 0.20,
    "aleatório": 0.10,
}

#: Distribuição com fração calibrada de denunciantes oportunistas (R24,
#: Cient. Político v2 + Sociólogo v2). Dyck-Morse-Zingales (2010) reportam
#: ~17% de motivação financeira direta em denúncias SEC; usamos 20% como
#: limite superior para teste de robustez do mecanismo contra uso adversarial
#: (insider acionista, concorrente, chantagem pré-rescisão, hedge fund ativista).
DISTRIBUICAO_COM_OPORTUNISTAS: dict[str, float] = {
    "ético": 0.10,
    "imitativo": 0.30,
    "racional": 0.30,
    "fairminded": 0.10,
    "aleatório": 0.00,
    "oportunista": 0.20,
}


#: Sete cenários canônicos para varredura comparativa.
CATALOGO_CENARIOS: tuple[Cenario, ...] = (
    Cenario(
        nome="status_quo",
        descricao=(
            "Regime A — situação atual brasileira, sem canal de incentivo "
            "individual ao denunciante interno em antitruste."
        ),
        sobrescritas={"regime": "A"},
    ),
    Cenario(
        nome="resolucao_pura",
        descricao=(
            "Regime B — nova Resolução CADE complementar à 21/2018, sem "
            "mudar a lei. Re-caracterização da recompensa como ressarcimento "
            "extrajudicial sob Art. 12; risco F6 (anulação judicial) presente."
        ),
        sobrescritas={
            "regime": "B",
            "D_disc_base_tcc": _D_BASE_TCC,  # Saito 2021 quando disponível; senão 0,10
            "p_anulacao_tcc": 0.10,  # F6 calibrado moderadamente
        },
    ),
    Cenario(
        nome="resolucao_mais_portaria_mte",
        descricao=(
            "Regime B + portaria MTE que reforça proteção trabalhista contra "
            "represália por denúncia coletiva. Reduz tolerância à represália "
            "(trabalhador percebe ambiente mais seguro) e custo legal."
        ),
        sobrescritas={
            "regime": "B",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.10,
            "r_represalia": 0.08,  # caiu de 0.15 padrão
            "custo_legal_uw": 0.15,  # caiu por proteção trabalhista
        },
    ),
    Cenario(
        nome="lei_waas_pura",
        descricao=(
            "Regime C — extensão da Lei 13.608/2018 (com a redação da Lei "
            "13.964/2019) ao enforcement antitruste, com percentual explícito "
            "de recompensa. Robustez jurídica plena; sem risco F6."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,  # F6 eliminado: lei é robusta
            "custo_legal_uw": 0.30,  # ainda há custo, mas defesa legal facilitada
        },
    ),
    Cenario(
        nome="lei_waas_com_fundo_honorarios",
        descricao=(
            "Regime C + fundo público de honorários advocatícios (análogo ao "
            "IRS Whistleblower Office americano). Estado financia a defesa do "
            "denunciante; custo legal individual ~0. Politicamente custoso."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "custo_legal_uw": 0.05,  # quase zero — fundo cobre quase tudo
            "prob_pagamento_perc": 0.95,  # fundo aumenta credibilidade
        },
    ),
    Cenario(
        nome="lei_waas_com_vesting_padrao",
        descricao=(
            "Regime C + cláusula padrão de vesting acelerado por gatilho de "
            "ação coletiva (Hirschman exit-with-equity R07 universal). "
            "Acrescenta canal de êxodo coletivo à IC-F* da firma."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "custo_legal_uw": 0.20,
            "fracao_contratos_acelerados": 1.0,  # universal por desenho
            "aliquota_tributaria_vesting": 0.40,  # IRPF + INSS realistas
        },
    ),
    Cenario(
        nome="mercado_digital_br_pareto",
        descricao=(
            "Regime C com **fatia de mercado distribuída em Pareto** (α=1,16). "
            "Reflete a realidade de mercados digitais brasileiros: dano "
            "concentrado em uma cauda longa de plataformas dominantes "
            "(iFood, Mercado Livre, Apple/Google), não distribuído "
            "uniformemente. R13a do backlog."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "custo_legal_uw": 0.20,
            "distribuicao_fatia_mercado": "pareto",
            "alpha_pareto": 1.16,  # regra 80/20 clássica
        },
    ),
    Cenario(
        nome="cenario_sancao_dura",
        descricao=(
            "Regime C + sanção catastrófica por descumprimento do TCC: firma "
            "que assina e depois não cumpre paga multa adicional 2× a sanção "
            "base. Captura 'se a empresa não cumpre, perde tudo' e fortalece "
            "o commitment da firma (R18)."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "custo_legal_uw": 0.20,
            "multa_descumprimento_tcc": 2.0,  # 2× a sanção base como adicional
            "p_descumprimento_tcc": 0.0,  # firma não descumpre porque é severo
            "prob_pagamento_perc": 0.95,  # credibilidade alta
        },
    ),
    Cenario(
        nome="cenario_corrida_leniencia",
        descricao=(
            "Regime C + leniência coletiva interna condicionada (R20). "
            "A firma só ganha atenuante se q_min × n_trabalhadores cooperarem "
            "internamente; desconto da firma e recompensa do trabalhador decaem "
            "com a posição na fila — ambos calibrados contra Saito (2021). "
            "Cria DUAS corridas acopladas: intra-firma e inter-firma. Resposta "
            "à tese substantiva 'mercados digitais têm moat → condutas "
            "unilaterais → corrida só pode ser intra-firma'."
        ),
        sobrescritas={
            "regime": "C",
            "modo_corrida": True,
            "q_min_cooperacao_interna": 0.10,
            "janela_temporal_tiques": 4,
            "perfil_decaimento": "saito",
            "custo_legal_uw": 0.20,
            "prob_pagamento_perc": 0.95,
        },
    ),
    # ----- Cenários novos sob reframe v2 (R21-R25) -----
    Cenario(
        nome="apenas_massa_critica_observavel",
        descricao=(
            "Regime A + dispara `notificada` mas a firma não tem instrumento "
            "de pagar (D_disc=0). Testa a hipótese 'massa crítica sem "
            "instrumento de internalização se perde no caminho'. **Falsificador "
            "F7** (Eco A v2): se o sinal Schelling sobrevive à invisibilidade do "
            "instrumento, há valor próprio na cooperação coletiva — não é só "
            "decoração do incentivo monetário."
        ),
        sobrescritas={
            "regime": "A",
            "D_disc": 0.0,
            "fracao_violadoras": 0.5,
            "taxa_observacao": 0.5,  # capacidade de massa crítica forma
        },
    ),
    Cenario(
        nome="dois_instrumentos_acoplados",
        descricao=(
            "Regime C + WaaS + Hirschman simultâneos com `modo_corrida=True`. "
            "Mede substituição perversa (crowding out à la Frey-Jegen 2001): "
            "firmas adotam o instrumento mais barato e mata os outros, "
            "perdendo a sinalização pública? Convergência Eco A v2."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "fracao_contratos_acelerados": 1.0,
            "aliquota_tributaria_vesting": 0.40,
            "modo_corrida": True,
            "q_min_cooperacao_interna": 0.10,
            "perfil_decaimento": "saito",
        },
    ),
    Cenario(
        nome="credito_tributario_puro",
        descricao=(
            "Regime C + crédito tributário como instrumento principal (R22, "
            "exploratório). Stub: usa `aliquota_tributaria_vesting` baixa "
            "(0.10) como proxy de incentivo tributário ao trabalhador. **Cᵩ "
            "exige LC + LRF** — ver `INSTITUTIONAL.md` decomposição de Regime "
            "C. Apenas placeholder até R22 ser implementado de fato."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "fracao_contratos_acelerados": 1.0,  # Hirschman como veículo proxy
            "aliquota_tributaria_vesting": 0.10,  # baixa = subsídio tributário
            "prob_pagamento_perc": 0.95,
        },
    ),
    Cenario(
        nome="leniencia_criminal_individual",
        descricao=(
            "Regime C + leniência criminal individual (R23, exploratório, "
            "stub). Estado defende; custo legal individual ~0; F6 eliminado. "
            "**Cₚ exige reserva penal estrita** Art. 5º XXXIX CF; colisão com "
            "Art. 86 da Lei 12.529 e Art. 4º-C §3º da Lei 13.608. Apenas "
            "placeholder até R23 ser implementado."
        ),
        sobrescritas={
            "regime": "C",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,
            "custo_legal_uw": 0.02,  # quase zero — Estado defende
            "prob_pagamento_perc": 0.95,
        },
    ),
    Cenario(
        nome="captura_processamento_cade",
        descricao=(
            "Regime B com capacidade institucional do CADE estrangulada "
            "(R-Cient. Político v2). Reduz `kappa_relativa` da autoridade para "
            "modelar o gargalo de 180 servidores área-fim (RIG 2024); espera-se "
            "que a seleção discricionária vire ponto ótimo de captura. Resposta "
            "ao sinal mais forte do Cient. Político na x10 v2."
        ),
        sobrescritas={
            "regime": "B",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.10,
            "taxa_capacidade": 0.10,  # capacidade muito limitada (180 servidores RIG 2024)
        },
    ),
    Cenario(
        nome="uso_adversarial_oportunista",
        descricao=(
            "Regime B + 20% de trabalhadores oportunistas (R24, x10 v2). "
            "Testa robustez do mecanismo contra uso adversarial (insider "
            "acionista, concorrente, chantagem, hedge fund ativista). "
            "Calibração: Dyck-Morse-Zingales 2010 ~17% em SEC; 20% como limite "
            "superior. Espera-se aumento em `n_tcc_anulados` (falsos positivos) "
            "e queda em `bem_estar`."
        ),
        sobrescritas={
            "regime": "B",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.10,
            "distribuicao_arquetipos": DISTRIBUICAO_COM_OPORTUNISTAS,
            "taxa_falso_reporte": 0.15,  # oportunistas elevam FP base
        },
    ),
    # ----- Cenários R28 — generalidade EUA/UE (pesquisa de fundo 2026) -----
    Cenario(
        nome="eua_doj_atr_rewards_2025",
        descricao=(
            "**Variante EUA** — DOJ-ATR Whistleblower Rewards Program "
            "(jul/2025) em parceria com USPS, **instituído administrativamente** "
            "sem lei nova federal. Hospedagem em Regime C porque a base "
            "estatutária Dodd-Frank §922 (SEC) torna a recompensa juridicamente "
            "robusta (sem F6). Faixa 15-30% sobre multas ≥ US$ 1 milhão; "
            "primeiro prêmio US$ 1 milhão em 29/jan/2026. `prob_pagamento_perc` "
            "calibrado em 0.225 (média da faixa); `custo_legal_uw` moderado "
            "(USPS coleta mas não financia defesa); LCMC `modo_corrida` ATIVO "
            "porque DOJ-ATR opera lógica de fila. Pendência [?]: calibrar "
            "`taxa_capacidade` do DOJ contra orçamento ATR FY2025."
        ),
        sobrescritas={
            "regime": "EUA",  # tag R28: mecânica C via REGIME_EQUIVALENTE
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.0,  # robustez estatutária Dodd-Frank §922
            "custo_legal_uw": 0.15,  # USPS coleta; defesa por conta do denunciante
            "prob_pagamento_perc": 0.225,  # média da faixa 15-30%
            "modo_corrida": True,
            "q_min_cooperacao_interna": 0.10,
            "perfil_decaimento": "saito",  # extrapolado; calibrar contra DOJ-ATR
        },
    ),
    Cenario(
        nome="ue_dma_whistleblower_tool_2024",
        descricao=(
            "**Variante UE** — DMA Whistleblower Tool (30/abr/2024), canal "
            "anônimo para violações dos Arts. 5/6/7 do Reg. 2022/1925, **SEM "
            "componente de recompensa**. Hospedagem em Regime A porque a UE "
            "regulou via Diretiva 2019/1937 (proteção horizontal anti-represália) "
            "sem incentivo monetário. Vetor empírico contra o qual o BR pode ser "
            "comparado: proteção forte sem recompensa basta? `r_represalia` "
            "calibrado baixo (proteção horizontal robusta); `D_disc=0` (sem "
            "instrumento de internalização); `p_perc` moderada (Schelling via "
            "publicidade DG-COMP). Pendência [?]: calibrar `taxa_capacidade` "
            "DG-COMP contra orçamento DG-COMP 2024."
        ),
        sobrescritas={
            "regime": "UE",  # tag R28: mecânica A via REGIME_EQUIVALENTE
            "D_disc": 0.0,  # sem instrumento de internalização monetária
            "r_represalia": 0.05,  # proteção horizontal Diretiva 2019/1937
            "custo_legal_uw": 0.10,  # proteção facilita defesa
            "fracao_violadoras": 0.5,  # mantém termo de comparação com BR
        },
    ),
    # ----- R26/R27 — canal puro + erosão Coleman (fechamento do backlog v3) -----
    Cenario(
        nome="apenas_canal_sem_instrumento",
        descricao=(
            "**Caso base R27-i** (correção radical v3): o canal de depósito "
            "condicional do CADE opera SOZINHO, sem qualquer instrumento "
            "monetário acoplado. `W_mult=0` zera a recompensa e `D_disc=0` zera "
            "o desconto do TCC — a IR-W do arquétipo racional nunca fecha e a "
            "IC-F* da firma nunca fecha. Os depósitos vêm exclusivamente do "
            "arquétipo ético (sinaliza independentemente de W) e cascateiam "
            "via imitativos. Par comparável com `apenas_massa_critica_observavel` "
            "(F7, sinal sem canal em Regime A) — aqui há canal explícito em "
            "Regime B. Testa: 'o canal sozinho carrega o mecanismo?' "
            "(Ayres-Unkovic 2012; análogo Callisto)."
        ),
        sobrescritas={
            "regime": "B",
            "usar_escrow_explicito": True,
            "W_mult": 0.0,
            "D_disc": 0.0,
            "q_min_cooperacao_interna": 0.10,
            "fracao_violadoras": 0.5,
            "taxa_observacao": 0.5,
        },
    ),
    Cenario(
        nome="erosao_coleman_adversarial",
        descricao=(
            "**Falsificação R26 — Proposição 5 candidata**: `resolucao_pura` "
            "(Regime B padrão pós-Saito 2021) + erosão endógena Coleman "
            "(`alpha_erosao=0.5`). Cada notificação reduz multiplicativamente "
            "o `capital_social_residual` — captura a tese substantiva de que "
            "instrumentalizar a denúncia destrói o substrato cooperativo que a "
            "produz (Coleman 1990 *Foundations of Social Theory* cap. 12). "
            "Calibração α=0.5 alinhada à base de falsificação em "
            "`test_erosao_coleman.py` e `viz/proposicao_5.py`. Literatura: "
            "Titmuss 1970 *The Gift Relationship*; Frey-Jegen 2001 *motivation "
            "crowding*; Bénabou-Tirole 2003 *intrinsic-extrinsic crowding-out*."
        ),
        sobrescritas={
            "regime": "B",
            "D_disc_base_tcc": _D_BASE_TCC,
            "p_anulacao_tcc": 0.10,
            "alpha_erosao": 0.5,
        },
    ),
    # ----- R30 — Sinergia entre autoridades internacionais (LCMC global) -----
    Cenario(
        nome="lcmc_global_coordenada",
        descricao=(
            "**Caso base R30 — coordenação internacional plena**: 6 firmas "
            "em 2 grupos econômicos multinacionais (firmas 0/1/2 no grupo 0; "
            "3/4/5 no grupo 1). Cada grupo representa uma Big Tech operando "
            "em 3 jurisdições distintas. Sob `usar_escrow_consolidado_grupo="
            "True`, depósitos contra firmas do mesmo grupo são somados para o "
            "gatilho de massa crítica — paralelo direto de MoU bilateral "
            "(CADE-DOJ-ATR 2019; DG-COMP-CADE 2009) ou de coordenação via "
            "ICN MoU 2001. `coordenacao_internacional=0.6` amplifica o sinal "
            "Schelling erga omnes (cada abertura eleva `p_perc` globalmente "
            "— efeito notícia ICN/OECD). Hipótese central: adesão simultânea "
            "das jurisdições gera **dissuasão superlinear** comparado à "
            "adoção descoordenada (`lcmc_global_descoordenada`)."
        ),
        sobrescritas={
            "regime": "B",
            "usar_escrow_explicito": True,
            "usar_escrow_consolidado_grupo": True,
            "coordenacao_internacional": 0.6,
            "grupos_economicos": (0, 0, 0, 1, 1, 1),
            "n_empresas": 6,
            "q_min_cooperacao_interna": 0.08,
            "fracao_violadoras": 0.6,
            "taxa_observacao": 0.5,
        },
    ),
    Cenario(
        nome="lcmc_global_descoordenada",
        descricao=(
            "**Contrafactual R30 — adoção isolada por jurisdição**: mesma "
            "topologia que `lcmc_global_coordenada` (6 firmas, hipotéticas "
            "subsidiárias em 3 jurisdições para 2 multinacionais) mas com "
            "`usar_escrow_consolidado_grupo=False` e "
            "`coordenacao_internacional=0`. Cada autoridade roda seu canal "
            "LCMC localmente, sem MoU bilateral, sem ICN. Mede o GANHO "
            "MARGINAL da coordenação: ΔW(coordenada) − ΔW(descoordenada). "
            "Par de teste para a hipótese de sinergia superlinear."
        ),
        sobrescritas={
            "regime": "B",
            "usar_escrow_explicito": True,
            "usar_escrow_consolidado_grupo": False,
            "coordenacao_internacional": 0.0,
            "grupos_economicos": (0, 0, 0, 1, 1, 1),
            "n_empresas": 6,
            "q_min_cooperacao_interna": 0.08,
            "fracao_violadoras": 0.6,
            "taxa_observacao": 0.5,
        },
    ),
    # ----- R29 — Janela de adesão pós-abertura com desconto progressivo -----
    Cenario(
        nome="cascata_adesao_progressiva",
        descricao=(
            "**Caso base R29**: canal de depósito condicional + janela de "
            "adesão pós-abertura de 10 tiques + desconto progressivo por classe "
            "(faixas 100%/70%/50%/30%/10%). Quando uma firma atinge massa "
            "crítica e seu escrow é aberto, abre-se a oferta para os demais "
            "trabalhadores da MESMA firma aderirem à classe dos lenientes — "
            "quem chega primeiro recebe desconto maior; quem não aderir até o "
            "fim da janela permanece no escrow comum (sujeito a expiração "
            "R27-ii). Cascata pós-coordenação que espelha o Art. 86 da Lei "
            "12.529/2011 (fila de leniência) operada DENTRO da firma já aberta. "
            "Calibrado para firmas médias (q_min=0,10) e taxa de observação "
            "moderada; mede o sub-produto observável `n_aderentes_pos_abertura_acum`."
        ),
        sobrescritas={
            "regime": "B",
            "usar_escrow_explicito": True,
            "janela_escrow_tiques": 8,
            "janela_adesao_pos_abertura": 10,
            "descontos_faixas_adesao": (1.0, 0.7, 0.5, 0.3, 0.1),
            "q_min_cooperacao_interna": 0.10,
            "fracao_violadoras": 0.5,
            "taxa_observacao": 0.5,
        },
    ),
    Cenario(
        nome="cascata_adesao_saito_calibrada",
        descricao=(
            "**R29 calibrado contra Saito (2021)** — variante do "
            "`cascata_adesao_progressiva` em que as faixas pós-abertura "
            "deixam de ser arbitrárias e passam a refletir o gradiente "
            "empírico do Art. 86 da Lei 12.529/2011 calibrado por Saito "
            "2021 (§3.7.7): D_Saito(1)=43,43% (SG), D_Saito(2)=34,51%, "
            "D_Saito(3)=20,22%, piso 15% (≥9ª posição). A faixa 0 "
            "(depositantes originais que dispararam a massa crítica) "
            "mantém imunidade total (fator 1,0); as faixas 1..4 espelham "
            "o gradiente Saito normalizado pelo topo (= D_Saito(k+1)/"
            "D_Saito(1) para k=1,2,3 e piso para k≥4): "
            "`(1.0, 0.795, 0.466, 0.345, 0.345)`. Isso elimina a "
            "arbitrariedade das faixas do caso base e ancora a regra "
            "R29 no mesmo dado empírico que sustenta o R20 inter-firma. "
            "Demais parâmetros idênticos ao caso base para comparabilidade "
            "direta de ΔW(arbitrário) vs ΔW(Saito)."
        ),
        sobrescritas={
            "regime": "B",
            "usar_escrow_explicito": True,
            "janela_escrow_tiques": 8,
            "janela_adesao_pos_abertura": 10,
            "descontos_faixas_adesao": (1.0, 0.795, 0.466, 0.345, 0.345),
            "q_min_cooperacao_interna": 0.10,
            "fracao_violadoras": 0.5,
            "taxa_observacao": 0.5,
        },
    ),
)


def lookup_cenario(nome: str) -> Cenario:
    """Localiza um cenário por nome; KeyError se desconhecido."""
    for c in CATALOGO_CENARIOS:
        if c.nome == nome:
            return c
    nomes_validos = ", ".join(c.nome for c in CATALOGO_CENARIOS)
    raise KeyError(f"cenário desconhecido: {nome!r}. Válidos: {nomes_validos}")


def aplicar_cenario(params: WaaSParametros, cenario: str | Cenario) -> WaaSParametros:
    """Retorna um novo `WaaSParametros` com as sobrescritas do cenário.

    Aceita o objeto `Cenario` ou seu nome em string. Não muta o `params`
    original — devolve uma cópia modificada via `dataclasses.replace`.
    """
    from dataclasses import replace

    c = cenario if isinstance(cenario, Cenario) else lookup_cenario(cenario)
    return replace(params, **c.sobrescritas)


def listar_cenarios() -> list[str]:
    """Nomes dos cenários disponíveis, em ordem do catálogo."""
    return [c.nome for c in CATALOGO_CENARIOS]
