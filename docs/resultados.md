# Resultados

Esta página narra, figura por figura, o que o modelo produz. As duas primeiras
figuras são **conceituais** (ilustram a lógica do mecanismo); a terceira é
**saída real da simulação** — o chip ao topo de cada imagem deixa explícito
qual é qual.

## 1 · A inversão de incentivo

![Inversão da função-utilidade da conformidade.](img/01_inversao.png){ .figura-conceitual }

**À esquerda**, o cálculo clássico: o custo esperado de ser punida é
"probabilidade de ser pega × tamanho da multa". Como a probabilidade de
detecção costuma ser baixa, a "conformidade ótima" fica numa **zona de
impunidade** — não vale a pena investir muito em não infringir.

**À direita**, sob o WaaS, o cálculo muda: a empresa compara o **desconto $D$**
na multa (por colaborar e ressarcir) com a **recompensa $W$** que paga aos
denunciantes. Na região clara, $D > W$ — colaborar é financeiramente melhor do
que esconder. A linha tracejada é a fronteira.

## 2 · A coordenação dentro da firma

![Diagrama de fase da coordenação intrafirma.](img/02_fase.png){ .figura-conceitual }

Um único funcionário raramente denuncia sozinho — há medo de represália. A
denúncia vira provável quando um número mínimo de colegas também está disposto
(uma **massa crítica**). O eixo horizontal é a gravidade da infração; o
vertical, quantos precisam aderir. Na região clara, a cascata de denúncias é
quase certa; na escura, prevalece o silêncio. As estrelas marcam onde os
Regimes B e C mirariam.

## 3 · Dissuasão e bem-estar — saída real do modelo

![Dissuasão endógena e bem-estar por regime.](img/03_dissuasao_bem_estar.png){ .figura-empirica }

A simulação roda nos três regimes (20 empresas, 40 trimestres).

**Painel (A)** — número de empresas violando ao longo do tempo. No Regime A
(sem WaaS), o número **cresce** — a detecção percebida é baixa e ninguém é
dissuadido. Nos Regimes B e C, a detecção percebida sobe e as violações **caem
a zero** em poucos tiques: é a **dissuasão**.

**Painel (B)** — bem-estar social, medido como o negativo do custo social
(dano causado + erros de classificação − multa arrecadada pelo Estado). Os
Regimes B e C ficam claramente acima do Regime A — não por punirem mais, mas
por **prevenirem** o dano.

!!! note "Por que medir bem-estar pelo dano, e não pelo número de punições?"
    Se medíssemos sucesso por "número de infrações detectadas", o Regime A
    pareceria *melhor* — afinal, há mais crime para detectar quando ninguém é
    dissuadido. Medir pelo **dano evitado** corrige essa perversidade e credita
    a prevenção. Os pesos exatos dessa conta seguem provisórios — ver
    [Limitações](limitacoes.md).

## Quer reproduzir?

O caminho mais rápido é o **[caderno-demo no Colab](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_demo.ipynb)**
(roda em ~1 minuto). Para rodar localmente, veja *[Como usar](uso.md)*.
