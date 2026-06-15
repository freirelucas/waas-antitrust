# Formulário matemático — IC-F\*, bem-estar, calibração

Esta página consolida em uma tela a álgebra que sustenta o argumento. As três formas
da IC-F\*, a função de bem-estar do modelo, a calibração formal de R03 e o gradiente
Saito. Cada equação aponta para o arquivo e função onde está implementada.

---

## 1. A condição IC-F\* — três formas

A condição "individualmente racional da firma pagar a recompensa" tem três formas no
modelo, correspondendo a três acoplamentos institucionais distintos. Em todas, $S$ é a
sanção esperada (multa × probabilidade de detecção), $D$ é o desconto sobre $S$ via
TCC, $W$ é a recompensa paga ao denunciante.

### 1.1 Forma simplificada (Regime B, sem TCC clássico de base)

$$
\boxed{\;W \;<\; D_{\text{extra}} \cdot S \;}
\qquad \text{com}\qquad
D_{\text{extra}} \;=\; D_{\text{disc}} \;-\; D_{\text{disc, base, TCC}}
$$

A firma compara a recompensa total ao **incremento** de desconto que o canal WaaS dá
sobre o TCC clássico — não ao desconto total. O parâmetro `D_disc_base_tcc` (default
$0$) modela o desconto que o Art. 85 da Lei 12.529 **já** oferece sem o WaaS; o
**Vetor de quebra A** ocorre quando $D_{\text{disc, base, TCC}} \ge D_{\text{disc}}$.

*Implementado*: `src/waas_antitrust/agents.py:EmpresaAgent.decidir_pagamento`.

### 1.2 Forma Hirschman (Regime C, vesting acelerado)

$$
\boxed{\;W \;<\; D_{\text{extra}} \cdot S \;+\; c_{\text{êxodo}} \;}
$$

A ameaça crível de êxodo coletivo aumenta o custo da firma de **não** pagar — o canal
contratual entra no lado direito. $c_{\text{êxodo}}$ é o custo esperado (capital
humano perdido $\times$ peso de Hirschman $\times$ probabilidade de êxodo). O peso
$\beta_H$ vive em `peso_hirschman` (default $0{,}3$); o gating jurídico força
`fracao_contratos_acelerados=0` sob Regimes A/B (Art. 22 I CF).

*Implementado*: `src/waas_antitrust/hirschman.py:g_i_efetivo` e
`custo_exodo_esperado`.

### 1.3 Forma LCMC (acoplamento Saito por posição na fila)

$$
\boxed{\;\sum_{j=1}^{k} W_j \;<\; D_{\text{Saito}}\!\left(\text{pos}_{\text{firma}}\right) \cdot S \;}
\qquad \text{com}\qquad
W_j \;=\; w_a \cdot W_{\text{mult}} \cdot f_W\!\left(j\right)
$$

Sob `modo_corrida=True`, $k$ é o número de cooperadores que atingiram a massa crítica
intra-firma $q_{\min}\cdot n$; o desconto $D_{\text{Saito}}(\text{pos})$ decai com a
posição da firma na fila inter-firma (1ª: 43,43%; 2ª: 34,51%; 3ª: 20,22%; ≥9ª: 15% —
calibrado contra Saito 2021 §3.7.7). A recompensa do trabalhador $W_j$ decai com a
posição na fila intra-firma via $f_W(j) = D_{\text{Saito}}(j)/D_{\text{Saito}}(1)$.

*Implementado*: `src/waas_antitrust/corrida.py:decaimento_D`,
`decaimento_W`, `massa_critica_interna_atingida`.

---

## 2. A função de bem-estar do modelo

$$
\boxed{\;
\text{Bem-estar} \;=\; -\frac{D \;+\; \beta\,\mathrm{FP} \;+\; \gamma\,c_W \;+\; \delta_\text{ex}\,c_\text{exodo} \;-\; \delta_\text{mu}\,M \;-\; \varepsilon\,\Delta_\text{difusa}}{w_a}
\;}
$$

onde $D$ é o dano acumulado (R01: contagem ponderada de violadoras ativas), $\mathrm{FP}$
são os falsos positivos, $c_W$ é o custo de recompensa privado, $c_\text{exodo}$ é o
custo social de êxodo (R07), $M$ é a multa arrecadada pelo erário (sinal positivo),
e $\Delta_\text{difusa}$ é a externalidade Schelling sobre firmas não-notificadas (v2.D.1).

**Pesos provisórios** (calibração R03 ainda não fechou estes): $\beta=1$, $\gamma=0$,
$\delta_\text{ex}=0{,}5$, $\delta_\text{mu}=1$, $\varepsilon=0$. **Calibrar** $\beta$
contra Polinsky-Shavell (custo do erro tipo I em enforcement), $\delta_\text{ex}$
contra literatura de capital humano em transição.

*Implementado*: `src/waas_antitrust/sobol/execucao.py:calcular_bem_estar`.

---

## 3. A calibração formal (R03)

O problema reduzido depois da identificabilidade:

$$
\min_{\,(f_v,\,t_c) \in [0{,}01;\,0{,}99]^2}\;\;
\left| \;\overline{\mathrm{TCC}_{\text{ano}}}(f_v,t_c) \;-\; \mathrm{alvo}_{\text{normalizado}} \;\right|^2
$$

com $\mathrm{alvo}_{\text{normalizado}} = 47 \times (n_{\text{modelo}}/N^\star)$ — onde
$47$ é o volume anual de TCCs do universo CADE inteiro (Saito 2021) e $N^\star$ é o
universo CADE assumido (default $1\,567$ firmas — predição falsificável).

**Ponto ótimo (Nelder-Mead, 5 seeds, 19 avaliações):**

$$
\boxed{\;
(f_v^\star,\,t_c^\star) \;=\; (0{,}323;\;0{,}481)
\qquad
\overline{\mathrm{TCC}_{\text{ano}}} \;=\; 0{,}560
\qquad
\mathrm{erro\;rel.} \;=\; 6{,}65\%
\;}
$$

O alvo está **dentro do IC bootstrap 95%** $[0{,}200;\;0{,}900]$ — calibração é
consistente com os dados disponíveis dado $N^\star$. **N\* implícito** depois do ajuste:
$1\,679$ firmas (predição falsificável contra o número real de firmas sob jurisdição
ativa do CADE — pendência empírica).

*Implementado*: `scripts/calibrar_formal.py`; resultado em
`results/calibracao_formal_r03.json`.

---

## 4. O gradiente Saito por posição

A função de decaimento do desconto por posição na fila inter-firma de leniência, calibrada
contra os 349 TCCs do CADE entre 2012 e 2019 (Saito 2021, §3.7.7):

| Posição | Desconto SG | Desconto Tribunal |
|---|---|---|
| 1ª | 43,43% | 15% (média) |
| 2ª | 34,51% | — |
| 3ª | 20,22% | — |
| ≥9ª | 15% (piso) | — |

O `_D_BASE_TCC` em `cenarios.py` usa 0,15 (média Tribunal, conservador) como base.
A função $f_W(j)$ da recompensa do trabalhador é a normalização $D(j)/D(1)$, garantindo
$f_W(1) = 1$ e queda monótona — preserva a corrida intra-firma (incentivo a chegar primeiro).

### 4.1 Desconto progressivo por classe na janela de adesão (R29)

A regra R29 instala um gradiente análogo **dentro da firma já aberta**. Seja $k$ a
posição na fila pós-abertura e $\mathbf{f}_W^{\text{adesão}} = (f_0, f_1, \ldots, f_{N-1})$
a tupla `descontos_faixas_adesao` (default `(1.0, 0.7, 0.5, 0.3, 0.1)`). A recompensa
esperada do trabalhador que adere na posição $k$ é

$$
\mathbb{E}[W \mid \text{aderir em } k] \;=\; W_{\max} \cdot f_W^{\text{adesão}}(\min(k, N-1)).
$$

A decisão individual no modelo é uma IR-W projetada para a faixa:

$$
\text{aderir} \iff f_W^{\text{adesão}}(k) \cdot W_{\max} \;>\; r \cdot w_a.
$$

O corte endógeno $k^\star$ aparece quando $f_W^{\text{adesão}}(k^\star) \cdot W_{\max}
\le r \cdot w_a$ — a partir daí ninguém adere mais. A janela $\Delta t =$
`janela_adesao_pos_abertura` controla o tempo máximo entre a abertura do bloco e
o fechamento da janela; após $\Delta t$ tiques o bloco sai do estado "em adesão" e
o gradiente apurado é consolidado para apuração da decisão da firma (P3).

*Implementado*: `src/waas_antitrust/calibracao/saito.py`,
`src/waas_antitrust/corrida.py:decaimento_D`.

---

## 5. Sensibilidade 1D (identificabilidade R03)

Da varredura de 175 rodadas 1D (`scripts/identificabilidade_r03.py`):

| Parâmetro | $\Delta$ TCC/ano | $\Delta$ fração interna | Veredicto |
|---|---|---|---|
| `fracao_violadoras` | 1,6 | 0,07 | **Dominante** para volume |
| `taxa_capacidade` | 0,8 | 0,05 | Dominante para volume |
| `k_rel` | 0,8 | **0,27** | Único que move a fração interna |
| `W_mult` | 0,4 | 0,05 | Secundário |
| `taxa_falso_reporte` | 0,1 | 0 | Secundário |
| `rho` | **0,00** | 0,00 | **Não-identificável** pelo alvo de volume; sai da função objetivo |

Conclusão operacional: a calibração reduz a $(f_v, t_c)$ porque `rho` é ortogonal ao
alvo (acurácia afeta precisão, não volume de assinatura) e o alvo de **composição** (DMZ
19%) é não-identificável pelo canal único de detecção do modelo.

---

## Onde cada equação vive no código

| Equação | Arquivo | Função/método |
|---|---|---|
| IC-F\* simplificada (1.1) | `agents.py` | `EmpresaAgent.decidir_pagamento` |
| IC-F\* Hirschman (1.2) | `hirschman.py` | `g_i_efetivo`, `custo_exodo_esperado` |
| IC-F\* LCMC (1.3) | `corrida.py` | `decaimento_D`, `decaimento_W` |
| Bem-estar (§2) | `sobol/execucao.py` | `calcular_bem_estar` |
| Função objetivo R03 (§3) | `scripts/calibrar_formal.py` | `objetivo()` interna a `main()` |
| Gradiente Saito (§4) | `calibracao/saito.py` | `_D_BASE_TCC`, `d_base_tcc_calibrado` |

Para os defaults numéricos de cada parâmetro citado aqui (`peso_hirschman`,
`taxa_capacidade`, `rho`, etc.), ver [`modelo_abm.md` §3](modelo_abm.md#3-tabela-completa-de-parametros-waasparametros)
— tabela completa com fonte de calibração de cada um.
