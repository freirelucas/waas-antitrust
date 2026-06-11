# Roadmap de figuras

Este documento mantém o backlog visual público — quais figuras existem,
quais estão em stub, e como cada uma se conecta aos cenários e às
Proposições. Atende ao Tier BAIXA #9 do balanço 360°.

## Convenção de selos

Toda figura no site recebe um dos dois selos via CSS:

- **`.figura-conceitual`** (chip "Ilustrativo", borda tracejada). Diagrama
  pedagógico — heurística, intuição, esquema. Não é resultado de
  simulação.
- **`.figura-empirica`** (chip "Resultado da simulação", borda verde
  sólida). Saída direta do modelo, gerada por um módulo
  `src/waas_antitrust/viz/<nome>.py` reprodutível pelo notebook ou pelo
  `scripts/gerar_figura_<nome>.py`.

A distinção é importante para que jornalista e jurista não confundam o
que é argumento pedagógico com o que é evidência de simulação.

## Figuras publicadas (9)

| # | Arquivo | Módulo gerador | Página de uso | Classe |
|---|---|---|---|---|
| 01 | `docs/img/01_inversao.png` | `viz/inversao.py` | `mecanismo.md` (Camada 4) | conceitual |
| 02 | `docs/img/02_fase.png` | `viz/fase.py` | `mecanismo.md` (Camada 2) | conceitual |
| 03 | `docs/img/03_dissuasao_bem_estar.png` | `scripts/gerar_figura_dissuasao.py` | `index.md`, `resultados.md` | empírica |
| 04 | `docs/img/04_cascata.png` | `viz/cascata.py` | `bem_publico.md` | conceitual |
| 05 | `docs/img/05_erosao_coleman.png` | `viz/erosao.py` | `bem_publico.md` | empírica |
| 06 | `docs/img/06_painel_macro.png` | `viz/painel_macro.py` | `modelagem_multiagente.md` | empírica |
| 07 | `docs/img/07_painel_micro.png` | `viz/painel_micro.py` | `modelagem_multiagente.md` | empírica |
| 08 | `docs/img/08_proposicao_5.png` | `viz/proposicao_5.py` | `bem_publico.md` | empírica |
| 09 | `docs/img/09_multiplicidade_unicidade.png` | `viz/multiplicidade_unicidade.py` | `ODD.md` | conceitual |

Cada PNG está abaixo de 200 KB e usa a paleta `cividis` cego-amigável
(`viz/paleta.py`). Todas as figuras seguem o padrão
`<figure markdown>...<figcaption>...</figcaption></figure>` com alt-text
abaixo de 125 caracteres (WCAG 2.1 AA).

## Stubs em backlog (8)

Cada stub é um módulo de 24 linhas em `src/waas_antitrust/viz/` que
levanta `NotImplementedError` ao ser chamado, com mensagem explícita
que a implementação canônica ainda vive no caderno
`notebooks/WaaS_caderno_v2.ipynb`. A migração desses módulos para o
pacote é a tarefa **T01** em `DECISIONS.md`.

| Stub | O que mostrará | Implementação canônica hoje |
|---|---|---|
| `viz/sankey.py` | Fluxos da corrida LCMC: trabalhadores → posição na fila → recompensa Saito (intra-firma) e firmas → posição na fila → desconto Saito (inter-firma). | Caderno §6 + `corrida.py` (lógica pura disponível). |
| `viz/painel.py` | Painel geral 3×3 do reframe v2 com massa crítica, instrumentos e robustez lado a lado (alvo: figura síntese para abstract). | Caderno §3 (agregação manual dos macro/micro hoje). |
| `viz/bootstrap.py` | Intervalos de confiança multi-seed (`robustez.bootstrap_ci`) para `dano_acumulado` e `bem_estar` por regime, com sombreamento. | Caderno §10 + `robustez.py`. |
| `viz/cade.py` | Série temporal CADE 2018-2024 da capacidade (`taxa_capacidade` calibrada contra RIG 2024) e dos TCCs assinados — ponte para a calibração R06. | Caderno §8 + `calibracao/cade.py`. |
| `viz/adversarial.py` | Tela do cenário `uso_adversarial_oportunista` (R24): FP por fração de oportunistas, com bandas multi-seed. | Caderno §7. |
| `viz/falsificacao.py` | Mapa F1–F7 dos falsificadores (Adv A v2 + autor) — qual cenário aciona qual flag, com hits/misses por tique. | Caderno §9 + `cenarios.py`. |
| `viz/internacional.py` | Comparação 3-jurisdições (BR, EUA-DOJ-ATR, UE-DMA) — dano evitado, bem-estar, capital social residual por jurisdição. | Caderno §11 + `cenarios.py` (R28). |
| `viz/variedade.py` | Curva de amplificação de variedade (Ashby/Beer) sob diferentes distribuições de papéis (`BIGTECH_MADURA` vs. `MARKETPLACE_BR`). | Caderno §5 + `condutas.py`. |

## Política de figuras

- **Tamanho**: PNG abaixo de 300 KB; idealmente abaixo de 200 KB.
  Comprimir com `pngquant` antes de commit se necessário.
- **Paleta**: usar `viz.PALETA` (`viz/paleta.py`) para consistência
  cromática entre os 17 módulos.
- **Acessibilidade**: alt-text descritivo abaixo de 125 caracteres
  (WCAG 2.1 AA); legenda longa vai em `<figcaption>`, não no atributo
  `alt`.
- **Selo**: toda figura empírica precisa ser reprodutível por um script
  ou módulo do pacote (não apenas pelo caderno) antes de migrar do stub
  para "publicada".

## Como contribuir

Migrar um stub para implementação completa:

1. Abrir `viz/<nome>.py` e substituir o `raise NotImplementedError(...)`
   por uma função `gerar_figura(...)` que retorna `(fig, ax)`.
2. Adicionar teste em `tests/test_viz.py` (remover o nome da lista do
   `test_viz_stubs_levantam_not_implemented` e adicionar um teste
   próprio análogo aos das 9 figuras existentes).
3. Integrar a figura em uma página com `<figure markdown>` + selo
   apropriado + alt-text < 125 car + figcaption rica.
4. Atualizar a tabela "Figuras publicadas" acima.

A migração das 8 figuras de uma só vez é a forma mais econômica;
migração parcial é aceita.
