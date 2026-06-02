# Como o mecanismo se sustenta (passo a passo)

Esta página responde de frente às perguntas que um leitor cético faz ao ouvir
o desenho do WaaS pela primeira vez:

1. **"Basta a empresa se recusar a pagar os denunciantes e pegar o desconto
   para tudo ruir?"**
2. **"Como vocês quantificam essa coisa?"**
3. **"E quem paga o advogado do denunciante?"**

Cada seção abaixo responde a uma. Quando há um modelo computacional por trás,
a fórmula é exposta com a aritmética em um exemplo numérico.

## 1 · O argumento, em uma linha

> **A empresa só obtém o desconto se ressarcir os denunciantes; o "ressarcir"
> precisa ser comprovado; e o incremento de desconto é maior que a recompensa
> total, dentro da faixa do Art. 12 da Resolução CADE nº 21/2018.**

Tudo o que segue é uma quantificação cuidadosa dessas três condições, e uma
discussão honesta dos pontos onde o argumento pode ruir — e por que cada um
desses pontos é (ou não) compensado no desenho.

## 2 · A IC-F* — o incentivo da firma a pagar

A firma decide *pagar* (assinar TCC com ressarcimento WaaS) ou *não pagar*
(seguir caminhos alternativos). O custo de cada caminho é:

| Caminho | Custo total da firma |
|---|---|
| **TCC-WaaS** (paga W, assina TCC com ressarcimento, Art. 12) | $S - D_{\text{total}} \cdot S + W = S(1 - D_{\text{total}}) + W$ |
| **TCC clássico** (não paga W, assina TCC sem ressarcimento, Art. 85) | $S(1 - D_{\text{base}})$ |
| **Sem TCC** (enfrenta o processo cheio) | $S$ (com probabilidade de condenação) |

onde $S$ é a sanção esperada, $D_{\text{total}}$ é o desconto total elegível
sob Art. 12 (TCC com ressarcimento WaaS), $D_{\text{base}}$ é o desconto que
o TCC clássico (Art. 85, sem ressarcimento) já oferece, e $W$ é a recompensa
total paga aos denunciantes.

**A firma prefere TCC-WaaS a TCC clássico quando:**

$$
S(1 - D_{\text{total}}) + W < S(1 - D_{\text{base}})
$$

$$
\iff W < (D_{\text{total}} - D_{\text{base}}) \cdot S = D_{\text{extra}}
$$

**Esta é a IC-F\* correta**: a recompensa $W$ tem de ser menor que o
**incremento** $D_{\text{extra}}$ que o canal WaaS oferece sobre o TCC
clássico, **não** que o desconto total. O modelo computacional foi
atualizado para usar essa formulação (parâmetro `D_disc_base_tcc` em
`WaaSParametros`, default 0 para preservar a IC-F* simplificada
historicamente usada nos testes; ativar para o regime adversarial).

### Aritmética em um exemplo

Suponha uma firma com receita afetada $R = \text{R\$}\,1$ bilhão e severidade
$\sigma = 0{,}5$.

- Sanção-base do CADE: $S_0 = 0{,}05 \cdot R = \text{R\$}\,50$ milhões.
- Sanção esperada escalada: $S = S_0 \cdot (1 + \sigma) = \text{R\$}\,75$
  milhões.
- Desconto WaaS total: $D_{\text{total}} = 30\% \cdot S = \text{R\$}\,22{,}5$
  milhões.
- Desconto do TCC clássico (estimativa): $D_{\text{base}} = 10\% \cdot S =
  \text{R\$}\,7{,}5$ milhões.
- **Incremento WaaS**: $D_{\text{extra}} = D_{\text{total}} - D_{\text{base}} =
  \text{R\$}\,15$ milhões.

Para 10 denunciantes a $W_{\text{indiv}} = 1{,}5 \cdot w_a$ com
$w_a = \text{R\$}\,180\,000$, a recompensa total é
$W = 10 \cdot 1{,}5 \cdot 180\,000 = \text{R\$}\,2{,}7$ milhões.

Como $W = 2{,}7\text{M} \ll D_{\text{extra}} = 15\text{M}$, **a firma prefere
pagar**: a IC-F* é satisfeita.

A **margem** $D_{\text{extra}} - W = 12{,}3$ milhões é o "preço" que o WaaS
extrai do bolso da firma e devolve aos denunciantes — uma transferência
privada, com efeito de prevenção pública.

## 3 · "E se a empresa não pagar?" — três vetores de quebra

A pergunta do leitor cético tem três formas concretas. Cada uma é modelada e
testada no repositório.

### Vetor A — TCC clássico já dá desconto sem WaaS

**O problema.** O TCC tradicional (Lei 12.529/2011, Art. 85) **já oferece**
desconto, independentemente de WaaS. Se esse desconto base $D_{\text{base}}$
for próximo de $D_{\text{total}}$, o incremento $D_{\text{extra}}$ encolhe e
a IC-F* deixa de motivar o pagamento.

**Mitigação no desenho.** O Art. 12 da Resolução 21/2018 é explícito: o
atenuante por ressarcimento das vítimas é um **acréscimo** ao desconto
genérico do TCC. A magnitude de $D_{\text{extra}}$ depende da prática
discricionária do CADE — e essa é a calibração que falta (R03; alvo Saito
2021).

**Mitigação no modelo.** O parâmetro `D_disc_base_tcc` em `WaaSParametros`
permite simular o pior caso (ex.: $D_{\text{base}} = D_{\text{total}}$, em
que ninguém paga W). O contador `n_firmas_optaram_tcc_classico` registra
quando o vetor materializa. Falsificar essa condição equivale a perguntar
"qual é o $D_{\text{extra}}$ mínimo para o WaaS ainda dissuadir?".

### Vetor B — anulação judicial do TCC (F6 explicitado)

**O problema.** A re-caracterização da recompensa como "ressarcimento" é uma
construção jurisprudencial. O Judiciário pode rejeitá-la (controvérsia
dogmática — ver [Análise institucional § "Quem é vítima?"](INSTITUTIONAL.md));
se anular, a empresa fica sem o desconto e paga a sanção cheia.

**Mitigação no desenho.** Esse é precisamente o **falsificador F6**, listado
nas premissas do modelo. Mais robusto seria o **Regime C** (extensão da Lei
13.608/2018 via Congresso), que elimina a controvérsia legal e está coberto
no modelo como variante.

**Mitigação no modelo.** O parâmetro `p_anulacao_tcc` em `WaaSParametros`
permite calibrar a probabilidade de anulação por tique. O contador
`n_tcc_anulados` registra as ocorrências; a multa cheia retorna ao erário
quando o TCC é anulado. Calibrar $p_{\text{anulação}}$ falsifica F6
quantitativamente: com $p_{\text{anulação}}$ alta, o Regime B colapsa em
Regime A.

### Vetor C — custos legais do denunciante

**O problema.** O denunciante interno terá custos que o modelo histórico
**não cobria explicitamente**: honorários advocatícios para reivindicar a
recompensa, defesa em ação trabalhista se sofrer represália, e — em
hipótese pior — responsabilização criminal sob Art. 86 da Lei 12.529/2011
se for caracterizado como **partícipe** da conduta (colisão com leniência
clássica).

**Mitigação no desenho.** Três cenários institucionais distintos, e cada um
implica calibração diferente:

1. **O denunciante paga.** Cenário simples mas pouco realista; eleva o piso
   da IR-W e desmotiva trabalhadores de baixa/média renda. Estima-se entre
   10% e 50% de um salário anual em custas + honorários no Brasil.
2. **A empresa cobre via TCC.** Análogo ao programa Dodd-Frank §922 da SEC,
   em que o pagamento bruto inclui margem para o advogado. Requer cláusula
   explícita na proposta de TCC e validação do CADE.
3. **O Estado financia (fundo).** Análogo ao IRS Whistleblower Office. Exige
   lei (Regime C) e dotação orçamentária; politicamente custoso.

**Mitigação no modelo.** O parâmetro `custo_legal_uw` em `WaaSParametros`
(em unidades de $w_a$) entra na IR-W do arquétipo "racional":

$$
W \ge r \cdot \tau \cdot 2 \cdot w_a + c_{\text{legal}} \cdot w_a
$$

onde $\tau$ é a tolerância individual a represália (R14). Default 0
preserva a IR-W histórica; valores realistas no Brasil ficariam entre
**0,1 e 0,5** (10–50% de $w_a$). Calibrar contra dados de honorários
trabalhistas é tarefa de R03.

## 4 · Os outros incentivos compatíveis

Além da IC-F* da firma, o desenho precisa satisfazer três outras condições:

| Sigla | Quem | Condição | Onde no modelo |
|---|---|---|---|
| **IR-W** | trabalhador | $W \ge \text{custo esperado de represália} + \text{custo legal}$ | `agents.py` (`decidir_sinal` racional) |
| **IC-T** | trabalhador | $W$ deve compensar penalidade por falso reporte | `agents.py` (mesma função, parcela $F_{\text{falso}}$) |
| **IC-F\*** | firma | $W < D_{\text{extra}}$ (vide §2) | `model.py` (P3) e `agents.py` (`satisfaz_ic_f_estrela` legado) |

A camada **Hirschman** (R07) acrescenta um quarto incentivo opcional: quando
firmas têm cláusula contratual de vesting acelerado por gatilho de ação
coletiva (institucionalmente disponível **só sob Regime C**, ver
[gating jurídico](INSTITUTIONAL.md#limites-do-regime-b-reserva-de-lei)), a
IC-F* se amplia para $W < D_{\text{extra}} + \text{custo de êxodo}$.

## 5 · Onde isto ainda pode ruir

Mesmo com os três vetores acima cobertos, há **gaps de calibração** que o
modelo não resolve sozinho — e que estão rastreados em
[Decisões e backlog](DECISIONS.md):

- **R03** — calibração formal contra Saito (2021), Wiedman & Zhu (2023,
  Dodd-Frank §922) e DEE/CADE 003/2022. Em particular, $D_{\text{base}}$ do
  TCC clássico precisa de mediana empírica.
- **R09** — endogeneizar $g_i(t)$ (atratividade de violar como função do
  estado). Hoje é sorteio uniforme estático.
- **R10** — IC-F* completa $W + p_{\text{pago}} \cdot (S - D) <
  p_{\text{não pago}} \cdot S$, em vez da forma simplificada $W < D$.
- **R13** — distribuição Pareto/lognormal de fatia de mercado (hoje
  uniforme; em digital, dano é cauda longa) e três condutas-piloto com
  fixtures.

A página de [Limitações](limitacoes.md) sintetiza isso em linguagem
acessível; a [Crítica x10](critica_x10.md) detalha o que oito revisores
externos apontaram.

## 6 · Em resumo

O argumento **não é** "a firma sempre paga porque o desconto é grande". O
argumento **é**:

1. A firma só ganha o desconto WaaS-específico se comprovar o ressarcimento
   (Art. 12, condicional);
2. O incremento sobre o TCC clássico ($D_{\text{extra}}$) é o que entra na
   IC-F*, não o desconto total;
3. Os vetores de quebra (TCC clássico capturando o desconto; anulação
   judicial; custos legais do denunciante) **estão modelados e calibráveis**;
4. Sob calibração razoável, o mecanismo **dissuade** (verificado com
   bootstrap multi-seed, intervalo de confiança 95% que não cruza zero —
   ver [Resultados](resultados.md));
5. Sob calibração adversa, o mecanismo **degrada** — e isso é uma
   propriedade desejável para um falsificador honesto, não um defeito a
   ser escondido.
