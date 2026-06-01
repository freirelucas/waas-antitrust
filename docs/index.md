# waas-antitrust

[![Licença: CC BY-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--SA%204.0-blue.svg)](https://github.com/freirelucas/waas-antitrust/blob/main/LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Mesa 3.x](https://img.shields.io/badge/mesa-3.x-green.svg)](https://mesa.readthedocs.io/)
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_demo.ipynb)

## Em uma frase

**E se a própria empresa pagasse seus funcionários para denunciarem as infrações
que ela comete — e isso saísse mais barato para ela do que esconder?** Este
projeto desenha um mecanismo com esse incentivo e usa uma **simulação** para
testar se ele funciona no combate a abusos de poder de mercado (antitruste) no
Brasil.

!!! note "Quem deveria ler isto"
    - **Curioso(a):** comece por *[O problema](#o-problema)* e *[Resultados](resultados.md)*.
    - **Formulador(a) de política / jurista:** veja a *[Análise institucional](INSTITUTIONAL.md)* (como caberia na lei brasileira).
    - **Pesquisador(a):** vá ao *[modelo (protocolo ODD)](ODD.md)*, à *[API](api.md)* e às *[Limitações](limitacoes.md)*.
    - Termo desconhecido? Há um *[Glossário](glossario.md)*.

## O problema

Os **programas de leniência** clássicos combatem **cartéis** — combinações entre
empresas concorrentes. Eles funcionam porque oferecem perdão a quem delatar
primeiro: um conspirador entrega os outros. Mas, em **mercados digitais**, boa
parte do abuso é **unilateral** — uma única empresa grande prejudicando o
mercado sozinha. Não há concorrente-cúmplice para delatar. Quem realmente sabe
o que acontece são os **próprios funcionários**.

## A ideia: *Whistleblower-as-a-Service* (WaaS)

Em vez de esperar a fiscalização descobrir tudo sozinha, o mecanismo cria um
incentivo financeiro para o **denunciante interno** (o funcionário). A peça
central é uma **inversão de incentivo**: hoje a empresa calcula "vale a pena
arriscar, porque dificilmente serei pega". Sob o WaaS, se a empresa for
investigada, ela ganha um **desconto na multa** ao ressarcir as vítimas — e
pode usar a recompensa paga aos denunciantes como parte desse ressarcimento.
**Quando o desconto é maior que a recompensa, virou negócio para a empresa
colaborar.** O combate à infração deixa de depender só da capacidade do Estado.

![Inversão da função-utilidade da conformidade: à esquerda o cálculo clássico (minimizar a multa esperada); à direita, sob o WaaS, a empresa passa a buscar o desconto.](img/01_inversao.png){ .figura-conceitual }

## O que a simulação mostra

Construímos um **modelo baseado em agentes** (empresas, funcionários e a
autoridade tipo CADE) e o rodamos em três cenários. O principal resultado: onde
o canal WaaS existe (Regimes B e C), a chance de ser denunciado sobe, **as
empresas deixam de violar** (dissuasão) e o dano social cai — algo que o cenário
atual (Regime A) não produz.

![Saída real do modelo: com o canal WaaS (B/C) as firmas param de violar ao longo do tempo e o bem-estar social supera o cenário atual (A).](img/03_dissuasao_bem_estar.png){ .figura-empirica }

➡️ **[Veja os resultados narrados, figura por figura](resultados.md).**

## Três cenários ("regimes")

| Regime | O denunciante interno é recompensado? | Como seria implementado |
|--------|----------------------------------------|--------------------------|
| **A** — hoje | Não | situação atual: sem canal de incentivo |
| **B** — via Resolução | Sim | nova resolução do CADE (Art. 12 da Res. 21/2018), **sem mudar a lei** |
| **C** — via Lei | Sim | extensão da Lei 13.608/2018 (mais robusto, exige o Congresso) |

## A tese, em termos técnicos

O mecanismo **inverte a função-utilidade da conformidade**: em vez de minimizar a
sanção esperada $p \cdot S$ (probabilidade de detecção × sanção), a empresa passa
a maximizar a margem $D - W$ — o desconto $D$ no Termo de Compromisso de Cessação
(TCC) menos a recompensa total $W$ paga aos denunciantes. A condição $D > W$
(chamamos **IC-F\***) é satisfazível na Resolução CADE nº 21/2018, sustentando
implementação por via infralegal (Regime B).

A coordenação dos denunciantes dentro da firma tem um **limiar de massa crítica**:
abaixo dele, silêncio; acima, uma cascata de revelação.

![Diagrama de fase da coordenação intrafirma: a região clara indica alta probabilidade de uma cascata de denúncias.](img/02_fase.png){ .figura-conceitual }

!!! warning "Estado: rascunho de trabalho"
    Este repositório acompanha um **artigo em elaboração**. Vários resultados são
    direcionais e algumas proposições ainda são conjecturas — veja a página de
    **[Limitações](limitacoes.md)** (em linguagem acessível) ou o
    [backlog técnico](DECISIONS.md). **Não citar como resultado final.**

## Citação

Veja [`CITATION.cff`](https://github.com/freirelucas/waas-antitrust/blob/main/CITATION.cff)
para metadados estruturados (compatíveis com Zenodo). O arquivamento no Zenodo
(DOI) será vinculado em uma release futura.
