# waas-antitrust

[![Licença: CC BY-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--SA%204.0-blue.svg)](https://github.com/freirelucas/waas-antitrust/blob/main/LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Mesa 3.x](https://img.shields.io/badge/mesa-3.x-green.svg)](https://mesa.readthedocs.io/)
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/claude/happy-clarke-eseuu/notebooks/WaaS_caderno_v2.ipynb)

Núcleo computacional do artigo **"Rescaling Leniency Programs for Digital
Markets: A Whistleblower-as-a-Service Mechanism"** — um **modelo baseado em
agentes** (Mesa 3.x) e **análise de sensibilidade global** (Sobol/SALib) para o
mecanismo *Whistleblower-as-a-Service* (WaaS) aplicado ao enforcement antitruste
em mercados digitais no Brasil.

!!! warning "Estado: rascunho de trabalho"
    Este repositório acompanha um artigo em elaboração. As Proposições 1–3 têm
    notas de status no [protocolo ODD](ODD.md) e há um
    [backlog de pesquisa](DECISIONS.md) (R01–R06) com itens que ainda sustentam —
    e não apenas alegam — as teses. Não citar como resultado final.

## A tese em uma frase

O mecanismo **inverte a função-utilidade da conformidade**: em vez de minimizar a
sanção esperada $p \cdot S$, a empresa passa a maximizar a margem $D - W$ — o
desconto $D$ no Termo de Compromisso de Cessação menos a recompensa total $W$
paga aos denunciantes internos. A condição $D > W$ (IC-F\*) é satisfazível na
Resolução CADE nº 21/2018, sustentando implementação por via infralegal.

## Três regimes institucionais

| Regime | Canal de denúncia | Base institucional |
|--------|-------------------|--------------------|
| **A**  | inexistente (situação atual) | — |
| **B**  | WaaS via Resolução | Art. 12 da Res. CADE 21/2018 |
| **C**  | WaaS via Lei | extensão da Lei 13.608/2018 |

## Comece por aqui

- **[Uso](uso.md)** — instalar, rodar o modelo, varredura de Sobol, gerar figuras.
- **[Modelo (ODD)](ODD.md)** — protocolo ODD, entidades, processos e proposições.
- **[Análise institucional](INSTITUTIONAL.md)** — fontes jurídicas primárias.
- **[Referência da API](api.md)** — documentação gerada das docstrings.

## Citação

Veja [`CITATION.cff`](https://github.com/freirelucas/waas-antitrust/blob/main/CITATION.cff)
para metadados estruturados (compatíveis com Zenodo). O arquivamento no Zenodo
(DOI) será vinculado em uma release futura.
