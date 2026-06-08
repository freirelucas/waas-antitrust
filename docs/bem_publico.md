# Bem coletivo, capital social, instrumentos de internalização

<div class="grid-instrumentos" markdown>

- <span class="chip-instrumento waas">WaaS</span> **Recompensa via TCC** — firma → trabalhador, sob Art. 12 da Res. 21/2018. Reserva ordinária. Implementado em `model.py` P3.

- <span class="chip-instrumento">Hirschman</span> **Vesting acelerado** — firma (via equity) → trabalhador. Reserva Cₜ trabalhista. Implementado em `hirschman.py`.

- <span class="chip-instrumento">Tributário</span> **Crédito tributário** — Estado → trabalhador (renúncia fiscal). Reserva Cᵩ tributária (LC + LRF). Stub declarativo (R22).

- <span class="chip-instrumento">Criminal</span> **Leniência criminal individual** — Estado → trabalhador (não-persecução). Reserva Cₚ penal estrita. Stub declarativo (R23).

</div>

Esta página é o **anexo conceitual** do projeto. Ela responde a uma
pergunta que o leitor curioso faz depois do [Ato 2](mecanismo.md): de
que tipo de coisa é "massa crítica de cooperação interna" — e por que
a recompensa via TCC é apenas **um** instrumento de internalização?

A resposta tem duas camadas, e é importante começar pela segunda — não
pela primeira.

![A cooperação interna emerge por cascata. A curva mostra a fração cumulativa de trabalhadores cooperando ao longo de 40 trimestres; quando ela cruza o gatilho `q_min` (LCMC, R20), a firma atinge massa crítica interna e ganha posição na fila de leniência. O pagamento via TCC vem **depois** desta cascata — não antes. Esta é a leitura sob reframe.](img/04_cascata.png){ .figura-conceitual }

## A primeira leitura — bem quase-público (Samuelson 1954)

A leitura econômica clássica é a mais óbvia. Samuelson (*Pure Theory of
Public Expenditure*, 1954) classifica bens em dois eixos:

- **Rivalidade no consumo** — o consumo por A reduz o disponível para B?
- **Excluibilidade** — é possível impedir B de consumir mesmo sem pagar?

Massa crítica de cooperação interna se posiciona como **bem quase-público**:
não-rival (o CADE pode reconhecer a cooperação sem reduzir a capacidade
de o MPF ou MPT também reconhecerem) e parcialmente excluível (só observável
a quem tem acesso à rede intra-firma, mas dentro dela a observação é
contínua entre pares).

Esta leitura é útil para enquadrar o problema na linguagem econômica
familiar. Ela tem **limites importantes**, que a segunda leitura expõe.

## A segunda leitura — capital social com risco de erosão (Coleman 1990)

![Trajetórias de `capital_social_residual` para três valores de `alpha_erosao` (R26). Sem erosão (preto, $\\alpha=0$), o capital social fica constante em 1.0. Com erosão moderada (verde, $\\alpha=0.2$), degrada lentamente. Com erosão forte (vermelho, $\\alpha=0.5$), colapsa em poucos tiques. A Proposição 5 candidata afirma que existe $\\alpha^\\star$ tal que para $\\alpha > \\alpha^\\star$, o Regime B colapsa em A após N tiques.](img/05_erosao_coleman.png){ .figura-empirica }


A crítica x10 v2 (Sociólogo) trouxe uma reformulação mais precisa.
Coleman (*Foundations of Social Theory*, 1990, cap. 12) define **capital
social** como bem coletivo **produzido como subproduto de relações de
obrigação** entre pessoas que se conhecem e dependem umas das outras.

A cooperação interna que o WaaS tenta liberar não é uma mercadoria
quase-pública — é capital social organizacional. A diferença é material
por uma razão central: Coleman previu que **o capital social pode ser
destruído pela sua própria instrumentalização**. Quando a confiança
horizontal entre colegas vira moeda regulatória, a moeda corrói a
confiança que a produziu.

Por isso o reframe correto não é "massa crítica é bem quase-público"
puro; é:

> **Massa crítica de cooperação interna é capital social organizacional cuja internalização institucional tem risco de erosão endógena.**

A consequência prática: qualquer instrumento de internalização (recompensa
via TCC, vesting acelerado, crédito tributário, leniência criminal) precisa
ser desenhado considerando o que sua *contínua aplicação* faz ao próprio
substrato que ele explora.

## A leitura jurídica — interesse público em detecção e cessação

A crítica x10 v2 (Adv A) acrescentou um ângulo dogmático brasileiro: no
direito sancionador administrativo BR, "bem público de detecção" não tem
ancoragem legal. A categoria disponível é **interesse público em detecção
e cessação** (Lei 9.784/99 Art. 2º, parágrafo único, IV e XIII) — princípio
de finalidade que pode sustentar atenuação sem criar categoria nova.

O **precedente brasileiro mais relevante**, que estava ausente nas
versões anteriores do projeto, é a **Lei 12.846/2013 (LAC), Art. 7º,
VII-VIII**: a existência de programa de integridade interno conta como
atenuante na dosimetria. Esse é exatamente o tipo de reconhecimento
institucional que o WaaS busca para a cooperação intra-firma. A LAC já
trata mecanismos de detecção interna como bem juridicamente relevante;
a tese do WaaS é uma extensão analógica defensável a partir desse
precedente.

## Os instrumentos de internalização

Sob a tese reformulada, o WaaS deixa de ser "a reforma" e passa a ser
**um instrumento entre vários** de internalização do capital social/
interesse público. Cada instrumento tem reserva constitucional distinta
e regime jurídico próprio.

| Instrumento | O que internaliza | Reserva constitucional | Regime mínimo | Status no código |
|---|---|---|---|---|
| **Recompensa via TCC (WaaS)** | parte do valor da cooperação como ressarcimento extrajudicial | Art. 22 I (lei ordinária) | B (Resolução) ou C | implementado em `model.py` P3 |
| **Vesting Hirschman** | custo de êxodo coletivo como ameaça crível pré-denúncia | Art. 22 I (cláusula contratual padrão exige lei) | **Cₜ trabalhista** | `hirschman.py` (R07) |
| **Crédito tributário** | retorno público ao denunciante via renúncia fiscal | Art. 146 LC (IRPJ/CSLL) + Art. 150 §6º (benefício) + LRF Art. 14 | **Cᵩ tributária-LC** | stub (R22, novo) |
| **Leniência criminal individual** | redução do risco de tipificação como partícipe | Art. 5º XXXIX (penal estrita) | **Cₚ penal** | stub (R23, novo) |

A decomposição do **Regime C** em três sub-regimes (Cₜ, Cᵩ, Cₚ) atende
à crítica do Adv B: "exigir lei" não é categoria homogênea no direito
constitucional brasileiro.

## Caveats — onde Olson e Ostrom falham para este caso

A crítica x10 v2 (Sociólogo) identificou cinco dos oito *design principles*
de Ostrom (*Governing the Commons*, 1990) que o WaaS **não** satisfaz:

- **P2 (congruência regras-condições locais)**: não há regra de proporcionalidade da recompensa ao dano sofrido pelo trabalhador individual.
- **P3 (arenas de escolha coletiva)**: trabalhadores não participam do desenho do mecanismo.
- **P6 (mecanismos baratos de resolução de conflito)**: denunciante v. firma é judicial-caro.
- **P7 (reconhecimento mínimo do direito de auto-organização)**: vedado por dever de lealdade contratual brasileira.
- **P8 (empreendimentos aninhados)**: coordenação CADE-MPF-MPT é institucionalmente inexistente.

O WaaS é, no vocabulário de Ostrom, um *commons imposto de cima*
(top-down), não governado de baixo. A teoria prevê degradação. O reframe
não esconde isso; explicita que esse é o eixo de pesquisa aberto e
documenta como falsificadores futuros.

## Onde ler mais

- [Mecanismo](mecanismo.md) — a aritmética dos instrumentos no Ato 2.
- [Modelo (ODD)](ODD.md) — diagnóstico Ostrom como subseção; Proposições reformuladas sob LCMC + bem coletivo.
- [Análise institucional](INSTITUTIONAL.md) — Lei 9.784/99 + LAC Art. 7º VII-VIII como precedente; decomposição Cₜ/Cᵩ/Cₚ.
- [Crítica x10 v2](critica_x10_v2.md) — Sociólogo e Cientista Político como personas que validaram o reframe.
- [Referências](REFERENCES.md) §"Coordenação coletiva e bens coletivos" — Olson, Ostrom, Coleman, Hardin, Heller.
