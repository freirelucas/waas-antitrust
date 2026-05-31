# Limitações

Este é um **artigo e um modelo em elaboração**. Esta página resume, em linguagem
acessível, o que ainda **não** está plenamente sustentado — para que nada seja
lido como conclusão final. O backlog técnico completo está em
[Decisões e backlog](DECISIONS.md).

## O que já está implementado e testado

- **A inversão de incentivo** ($D > W$) é verificável e tem teste automatizado.
- **A dissuasão** (empresas param de violar quando o canal existe) é produzida
  pelo próprio modelo, não imposta à mão.
- **O bem-estar** é medido pelo dano evitado, creditando a prevenção.
- **A coordenação tipo "jogo global"** tem uma versão matemática fechada e testada
  (o limiar de denúncia é único e se comporta como a teoria prevê).

## O que ainda é trabalho futuro

| # | Limitação | O que falta |
|---|-----------|-------------|
| **R02** | O "jogo global" tem solução analítica, mas **isolada** | integrá-la à dinâmica completa da simulação; a prova de unicidade da Proposição 2 segue como **conjectura** |
| **R03** | Os números **não estão calibrados** contra a realidade | ajustar os parâmetros aos dados do CADE (acordos de leniência, TCCs) e à literatura; hoje as magnitudes são plausíveis, não ajustadas |
| **R05** | Os **pesos do bem-estar** são provisórios | ancorar "quanto vale o dano evitado" em estimativas econômicas |
| **R06** | A **capacidade da autoridade** usa uma aproximação | precisa de dado empírico (quantos funcionários têm as subsidiárias de big techs no Brasil) |

## Em resumo

O modelo demonstra **a lógica e a direção** do mecanismo de forma transparente e
reproduzível. O que ele **ainda não faz** é entregar números calibrados e provas
formais completas — e isso está marcado como tal em todo o repositório, em vez de
ser apresentado como resultado definitivo.
