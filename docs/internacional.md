# Generalidade do mecanismo · EUA e UE como variantes paramétricas

A pesquisa de fundo de janeiro de 2026 verificou três marcos institucionais
que **não existiam quando o modelo foi escrito** e que confirmam, de fora,
a generalidade da LCMC. Cada marco aparece aqui como **variante paramétrica
do mesmo agente-modelo** — não como teoria distinta. A leitura primária
permanece a do canal de depósito condicional operado pela autoridade
(Ayres-Unkovic 2012; Callisto); a leitura institucional brasileira (Art. 12
da Res. CADE 21/2018; Cₜ/Cᵩ/Cₚ) permanece em [`INSTITUTIONAL.md`](INSTITUTIONAL.md).

## Sumário dos três marcos

| Jurisdição | Marco | Data | Recompensa? | Hospedagem no modelo |
|---|---|---|---|---|
| EUA (federal) | **DOJ-ATR Whistleblower Rewards Program** (parceria USPS) | jul/2025 | Sim, 15–30% sobre multas ≥ US$ 1 mi | Regime C + `prob_pagamento_perc=0.225` |
| EUA (universitário) | **Callisto** (`callisto.org`) | desde 2015 | Não | precedente operacional do escrow (R27) |
| UE | **DMA Whistleblower Tool** | abr/2024 | Não | Regime A + `r_represalia` baixo |

As três peças, lidas em conjunto, suportam três proposições institucionais:

1. **A regulamentação administrativa é via viável.** Tanto o DOJ-ATR (jul/2025)
   quanto o DMA Tool (abr/2024) foram instituídos por autoridade administrativa,
   sem necessidade de lei nova. O paralelo direto no Brasil é a hipótese de
   `regulamentação infralegal sob a Resolução CADE 21/2018` (Regime B).
2. **Proteção horizontal sem incentivo monetário tem limite.** A Diretiva
   (UE) 2019/1937 cobre o canal e a represália; o DMA Tool entrega o canal
   anônimo. Mas a literatura não documenta volume comparável ao Dodd-Frank
   §922 da SEC — sinaliza que a coordenação intra-firma exige **mais que
   proteção**: exige internalização (R28 v3).
3. **A LCMC é (b)/(c) generalizável.** A combinação `canal de depósito +
   massa crítica + leniência condicional` aparece em três jurisdições com
   três desenhos institucionais distintos — sugere que o mecanismo é
   transponível, não específico ao desenho jurídico-administrativo brasileiro.

## Os dois cenários paramétricos

### `eua_doj_atr_rewards_2025`

Variante calibrada contra o DOJ-ATR Whistleblower Rewards Program:

- **Regime C** porque a base estatutária do desenho (Dodd-Frank §922 da SEC,
  precedente direto para recompensa 10–30%) torna o pagamento **juridicamente
  robusto** — sem F6 (`p_anulacao_tcc=0`).
- `prob_pagamento_perc=0.225` reflete a média aritmética da faixa 15–30%
  divulgada pelo DOJ.
- `modo_corrida=True` porque o DOJ-ATR opera lógica de fila com gradiente
  por posição (descontos similares ao gradiente Saito 2021 capturado em
  `corrida.py`).
- `custo_legal_uw=0.15` reflete que o USPS faz a coleta da denúncia mas
  não financia a defesa do denunciante (diferente de fundo público de
  honorários).

[Primeiro prêmio: US$ 1 milhão em 29 de janeiro de 2026.](https://www.justice.gov)
(Referência empírica preliminar; primária a verificar contra DOJ-ATR
public statements em R03.)

### `ue_dma_whistleblower_tool_2024`

Variante calibrada contra o DMA Whistleblower Tool:

- **Regime A** porque a UE regulou o canal **sem componente de recompensa**.
  Hospedagem em Regime A mantém `D_disc=0` (sem instrumento de internalização
  monetária via desconto na multa).
- `r_represalia=0.05` reflete a proteção horizontal anti-represália da
  Diretiva (UE) 2019/1937 — substancialmente robusta em relação à proteção
  trabalhista brasileira.
- A `p_perc` (probabilidade percebida de detecção) opera por publicidade
  ex post da DG-COMP, não por incentivo ex ante ao denunciante.
- O vetor empírico que o modelo permite testar: **proteção horizontal sem
  recompensa é suficiente?** Cruzar com a Proposição 2 (massa crítica)
  responde por simulação.

## A comparação em figura

O módulo `viz/internacional.py` materializa a comparação direcional em
multi-seed:

<figure markdown>
  ![Painel 1x2 da comparação de dano acumulado entre BR status quo, EUA DOJ-ATR 2025 e UE DMA Tool 2024](img/13_internacional_3jurisdicoes.png){ .figura-empirica }
  <figcaption>
    Comparação direcional 3 jurisdições, 8 seeds × 24 tiques. <strong>(A)</strong> Trajetória mediana de <code>dano_acumulado</code> com banda interquartílica. <strong>(B)</strong> Dano final com IC bootstrap 95%. A variante EUA (DOJ-ATR: recompensa 15–30% + LCMC ativa) domina; a variante UE (DMA Tool: proteção sem recompensa) fica entre o status quo BR e a variante EUA — consistente com a tese substantiva de que proteção sem incentivo é insuficiente. <strong>Caveat</strong>: capacidade institucional NÃO calibrada (pendência R28); leituras de volume absoluto não são confiáveis, apenas direcionais.
  </figcaption>
</figure>

## Como rodar

```python
from waas_antitrust.cenarios import aplicar_cenario
from waas_antitrust.model import WaaSModel, WaaSParametros

p_base = WaaSParametros(n_empresas=20, tam_medio_empresa=200, n_tiques=40, seed=2026)

# Comparação 3-jurisdições
for nome in ("status_quo", "eua_doj_atr_rewards_2025", "ue_dma_whistleblower_tool_2024"):
    p = aplicar_cenario(p_base, nome)
    df = WaaSModel(p).executar()
    print(f"{nome:38s}  dano_acum={df['dano_acumulado'].iloc[-1]:.2f}  "
          f"n_tcc={df['n_tcc_assinados'].iloc[-1]:.0f}  "
          f"bem_estar={df['bem_estar'].iloc[-1]:.2f}")
```

## Caveats da transposição

1. **Capacidade institucional não calibrada.** `taxa_capacidade` para o DOJ-ATR
   e a DG-COMP não estão calibradas contra orçamento real (pendência R28
   ação 5). Os cenários usam o default brasileiro; comparações de **volume
   absoluto** não são confiáveis, apenas direcionais.
2. **Regime C ≠ desenho Dodd-Frank.** O Regime C do modelo é o agregado
   "regime via lei robusta"; o desenho institucional americano é distinto
   no detalhe (SEC ≠ DOJ-ATR ≠ IRS WBO). A hospedagem é estilizada.
3. **Gradiente Saito como proxy.** O perfil de decaimento `saito` em
   `corrida.py` foi calibrado contra TCCs do CADE 2012-2019 (Saito 2021).
   Sua aplicação ao DOJ-ATR é **extrapolação** — corrigir quando dados do
   DOJ-ATR estiverem disponíveis (R03b).
4. **Callisto não aparece como cenário paramétrico.** Aparece como
   **precedente operacional do escrow** (R27): canal de depósito condicional
   funcionando há ~10 anos no contexto universitário, validando a
   exequibilidade do desenho v3.

## Próximos passos (R28 em DECISIONS)

O R28 está **parcialmente fechado**. As ações restantes:

1. Generalizar `WaaSParametros.regime` para aceitar `"EUA"` e `"UE"` como
   tags explícitas (hoje, os cenários reaproveitam A/B/C com sobrescritas).
2. Calibrar `taxa_capacidade` para o DOJ-ATR e DG-COMP contra orçamentos
   públicos (FY2025 e 2024 respectivamente).
3. Documentar em [`INSTITUTIONAL.md`](INSTITUTIONAL.md) uma decomposição
   EUA/UE análoga ao Cₜ/Cᵩ/Cₚ brasileiro.
4. Abrir publicações comparadas (paper extension) com simulações 3-jurisdições.

## Bibliografia institucional

- **Lei 12.529/2011** Art. 86 — leniência clássica para empresas (BR).
- **Lei 13.608/2018** + **Lei 13.964/2019** Art. 4º-C — recompensa a informante
  em "crimes contra administração pública" (BR; extensão analógica ao
  antitruste é hipótese, não jurisprudência).
- **Resolução CADE nº 21/2018** Art. 12 — TCC e atenuante coletivo (BR).
- **Dodd-Frank §922** (15 U.S.C. §78u-6) — SEC Whistleblower Program 10–30%.
- **DOJ-ATR Whistleblower Rewards Program** (parceria USPS) — instituído
  administrativamente em jul/2025.
- **DMA Whistleblower Tool** (`digital-markets-act.ec.europa.eu`) — canal
  anônimo da Comissão Europeia para violações do Regulamento (UE) 2022/1925.
- **Diretiva (UE) 2019/1937** — proteção horizontal anti-represália para
  denunciantes; sem componente de recompensa.
- **Ayres, I. & Unkovic, C. (2012)** "Information Escrows", *Michigan Law
  Review* 111:145–196.
- **Callisto** (`callisto.org`) — escrow operacional desde 2015.
