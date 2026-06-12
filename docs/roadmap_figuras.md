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

## Figuras publicadas (18)

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
| 10 | `docs/img/10_alpha_erosao_limiar.png` | `viz/alpha_erosao_limiar.py` | `bem_publico.md` | empírica |
| 11 | `docs/img/11_sankey_corrida_lcmc.png` | `viz/sankey.py` | `mecanismo.md` | empírica |
| 12 | `docs/img/12_bootstrap_regimes.png` | `viz/bootstrap.py` | `resultados.md` | empírica |
| 13 | `docs/img/13_internacional_3jurisdicoes.png` | `viz/internacional.py` | `internacional.md` | empírica |
| 14 | `docs/img/14_cade_capacidade.png` | `viz/cade.py` | `limitacoes.md` | empírica (dados RIG/TCU) |
| 15 | `docs/img/15_adversarial_oportunistas.png` | `viz/adversarial.py` | `limitacoes.md` | empírica |
| 16 | `docs/img/16_falsificacao_vetores.png` | `viz/falsificacao.py` | `resultados.md` | empírica |
| 17 | `docs/img/17_variedade_papeis.png` | `viz/variedade.py` | `modelagem_multiagente.md` | empírica |
| 18 | `docs/img/18_painel_sintese.png` | `viz/painel.py` | `resultados.md` | empírica |

Cada PNG está abaixo de 200 KB e usa a paleta `cividis` cego-amigável
(`viz/paleta.py`). Todas as figuras seguem o padrão
`<figure markdown>...<figcaption>...</figcaption></figure>` com alt-text
abaixo de 125 caracteres (WCAG 2.1 AA).

## Stubs em backlog (0) — T01 fechado

Em jun/2026 todos os 8 stubs originais foram migrados do caderno para
módulos do pacote: `sankey.py` (figura 11), `bootstrap.py` (12),
`internacional.py` (13), `cade.py` (14), `adversarial.py` (15),
`falsificacao.py` (16), `variedade.py` (17) e `painel.py` (18, a
figura-síntese 2×3). A tarefa **T01** de `DECISIONS.md` está fechada;
o caderno `WaaS_caderno_v2.ipynb` deixa de ser a referência canônica
de visualizações.

Nota sobre o `falsificacao.py`: a taxonomia que se materializou no
repositório são os **vetores de quebra A-E** (+F6/F7
jurídico-institucionais), não a numeração F1-F7 originalmente
imaginada para o stub — a figura 16 executa os 5 vetores contra
baseline.

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
