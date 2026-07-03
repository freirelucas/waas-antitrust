# Auditoria de clareza e coerência estrutural

<p class="deck">Inspeção sistemática da estrutura do site enquanto produto: hierarquia do nav, padrão de abertura entre páginas, sequência narrativa dos cinco Atos, mapa de cross-links e detecção de páginas pouco linkadas. Complementa as auditorias anteriores (<a href="/waas-antitrust/brainstorm_revisao/">brainstorm de revisão</a>: tom; <a href="/waas-antitrust/revisao_personas/">revisão por personas</a>: leitura por perfil) com foco em coerência estrutural.</p>

<p class="byline"><em>Auditoria interna</em> · jun/2026 · clareza e coerência estrutural</p>

## 1 · Hierarquia do nav

A árvore atual de navegação (em `mkdocs.yml`) tem três níveis lógicos que **não estão visualmente diferenciados**:

1. **Narrativa principal (5 Atos):** `index.md` → `mecanismo.md` → `resultados.md` → `limitacoes.md` → `colaborar.md`.
2. **Aprofundamentos técnicos (top-level, sem numeração):** `modelo_abm.md`, `brincar.md`, `paper.md`, `sobre.md`.
3. **Anexos:** `Como usar`, `Comandos`, `Transparência`, `Imprensa`, `Formulário` (5 itens diretos) + sub-grupos `Teoria e modelo`, `Direito e instituições`, `Referência` (mais 14 itens em sub-níveis).

### Achados estruturais

- **Mistura de itens diretos e sub-grupos sob "Anexos".** Sob `Anexos` há 5 entradas diretas (Como usar, Comandos, Transparência, Imprensa, Formulário) e 3 sub-grupos (Teoria/Direito/Referência). O leitor que clica em "Anexos" vê uma lista heterogênea — mistura *guias de uso* com *aprofundamento teórico*.
- **"Modelo ABM" e "Brincar" estão como itens top-level sem ato.** Aparecem entre os 5 Atos e os Anexos, mas não fazem parte da narrativa numerada — soltam-se. Recomendação: mover para um sub-grupo "Aprofundamento técnico" ou colocá-los após `Sobre`, com agrupamento visual.
- **"Paper" também é top-level mas é mirror do LaTeX.** Para leitor que chega no site, "Paper" parece quinto Ato — não é.

### Sugestão de reorganização (não aplicada nesta rodada — discussão)

```
- Ato 1 · O problema           (index.md)
- Ato 2 · O mecanismo          (mecanismo.md)
- Ato 3 · Resultados           (resultados.md)
- Ato 4 · Limitações           (limitacoes.md)
- Ato 5 · Colaborar            (colaborar.md)
- ─────
- Aprofundamento técnico:
    - Modelo ABM em detalhe    (modelo_abm.md)
    - Simulador in-browser     (brincar.md)
    - Paper (LaTeX mirror)     (paper.md)
- Sobre                        (sobre.md)
- Guias operacionais:
    - Como usar                (uso.md)
    - Comandos e scripts       (comandos.md)
    - Transparência epistêmica (transparencia.md)
    - Kit de imprensa          (imprensa.md)
    - Formulário matemático    (formulario.md)
- Teoria e modelo:             (sub-grupo atual mantido)
- Direito e instituições:      (sub-grupo atual mantido)
- Referência:                  (sub-grupo atual mantido)
- Desenvolvimento:             (sub-grupo atual mantido)
```

A justificativa para não aplicar agora: mexer no nav exige avaliar impacto em SEO interno e em links externos que possam apontar para slugs estáveis. Fica como decisão.

## 2 · Padrão de abertura entre páginas

A rodada editorial estabeleceu um padrão estável: **`<p class="deck">` (subtítulo descritivo) + `<p class="byline">` (autor · ato · versão) + `<p class="lede">` (parágrafo introdutório, opcional para páginas técnicas)**. Hoje, 22/06/2026, a coerência está parcial:

### Páginas no padrão novo (deck/byline/lede)

`index.md`, `mecanismo.md`, `resultados.md`, `limitacoes.md`, `colaborar.md`, `modelo_abm.md`, `bem_publico.md`, `modelagem_multiagente.md`, `ODD.md`, `transparencia.md`, `internacional.md`, `sobre.md`, `brincar.md` (parcial), `uso.md` (parcial), `comandos.md` (parcial).

### Páginas ainda no padrão antigo (`sublinha-tese`)

`normas.md`, `choques.md`, `condutas.md`, `paper.md`, `plano_melhorias.md`.

### Pendência

Migrar as 5 páginas restantes para o padrão `deck`/`byline`/`lede`. Vícios prováveis a corrigir junto:

- **`paper.md`** — provável tom de press release inicial; sub-tese descritiva em italic provavelmente terá os mesmos defeitos.
- **`normas.md`** — sub-página técnica do módulo `normas/`; sub-tese pode ser descritiva legal seca; baixo risco.
- **`condutas.md`** e **`choques.md`** — catálogos; sub-tese provavelmente OK; baixo risco.
- **`plano_melhorias.md`** — documento histórico de processo; eventualmente ganha banner igual ao `aprendizados_v2`.

## 3 · Sequência narrativa dos cinco Atos

Cada Ato deve terminar com remissão clara ao próximo. Verificação:

| Ato | Termina com link para… | Verificado |
|---|---|---|
| Ato 1 `index.md` | "▶ Ato 2: O mecanismo →" linka `mecanismo.md` | ✓ |
| Ato 2 `mecanismo.md` | linka `brincar.md`, `modelo_abm.md`, `DECISIONS.md`, `limitacoes.md`, `resultados.md` | ✓ |
| Ato 3 `resultados.md` | linka `brincar.md`, `limitacoes.md` | ✓ |
| Ato 4 `limitacoes.md` | linka `bem_publico.md`, `viabilidade_regime_c.md`, `INSTITUTIONAL.md`, `DECISIONS.md`, `colaborar.md` | ✓ |
| Ato 5 `colaborar.md` | linka `DECISIONS.md`, `index.md` (retorno ao começo) | ✓ |

A sequência narrativa **funciona**; cada Ato fecha com chamada para o próximo. Único ponto frouxo: o Ato 3 → 4 não tem remissão explícita "▶ Ato 4: Limitações →" no final do `resultados.md`. Provavelmente vale verificar.

## 4 · Mapa de cross-links e páginas pouco linkadas

Contagem aproximada de páginas que linkam para cada destino (excluindo nav e auto-links):

| Página | Links recebidos | Categoria |
|---|---:|---|
| `mecanismo.md` | 8 | Ato 2, citado por toda parte ✓ |
| `limitacoes.md` | 7 | Ato 4 ✓ |
| `DECISIONS.md` | 6 | Backlog central ✓ |
| `brincar.md` | 5 | Simulador ✓ |
| `INSTITUTIONAL.md` | 4 | Direito ✓ |
| `modelagem_multiagente.md` | 3 | Teoria do modelo ✓ |
| `bem_publico.md` | 3 | Teoria do bem coletivo ✓ |
| `viabilidade_regime_c.md` | 3 | Direito ✓ |
| `transparencia.md` | 3 | Auditoria ✓ |
| `modelo_abm.md` | 3 | Aprofundamento técnico ✓ |
| `ODD.md` | 3 | Protocolo formal ✓ |
| `internacional.md` | 3 | Direito comparado ✓ |
| `colaborar.md` | 3 | Ato 5 ✓ |
| `compliance_corporativo.md` | 2 | Anexo direito |
| `paper.md` | 1 | Mirror LaTeX |
| **`condutas.md`** | **0 (orgânicos)** | **Catálogo de 28 condutas** |
| **`choques.md`** | **0 (orgânicos)** | **Catálogo R19** |
| **`normas.md`** | **0 (orgânicos)** | **Parser LexML** |
| **`api.md`** | **0 (orgânicos)** | **API reference** |
| **`roadmap_figuras.md`** | **1 (`comandos.md`)** | **Mapa figura → página** |
| **`imprensa.md`** | **2 (`index.md`, `revisao_personas.md`)** | Kit imprensa |
| **`formulario.md`** | **3** | Aritmética |
| **`glossario.md`** | **0 (orgânicos)** | **Dicionário** |
| **`TERMINOLOGIA.md`** | **1 (`glossario.md`)** | Canônica |

### Páginas materialmente órfãs (4)

- **`condutas.md`** — catálogo de 28 condutas digitais. Acessível só via nav. Seria útil ter link do `mecanismo.md` (Camada 2 ou na lista de condutas-exemplo do Ato 1) e do `INSTITUTIONAL.md`.
- **`choques.md`** — catálogo R19 (5 catálogos de choques institucionais). Acessível só via nav. Seria útil link do `mecanismo.md` ou `limitacoes.md` (cenários adversariais).
- **`normas.md`** — parser LexML BR. Acessível só via nav. Link óbvio: do `INSTITUTIONAL.md` (fontes primárias verbatim).
- **`glossario.md`** — dicionário. Praticamente nenhuma página linka pra ele. Seria útil mencioná-lo na primeira ocorrência de cada termo técnico — pelo menos no `index.md` e `mecanismo.md`.

### Página com fluxo de retorno fraco (1)

- **`api.md`** — referência da API gerada por `mkdocstrings`. Aceitável que receba zero links orgânicos.

## 5 · Achados consolidados — pendências

Por gravidade descendente:

1. **`paper.md`** — última página com `sublinha-tese`, e provavelmente o vício editorial mais visível para leitora acadêmica chegando do GitHub. Migrar para `deck/byline/lede`. Gravidade média.
2. **Cross-links para `condutas.md`, `choques.md`, `normas.md`, `glossario.md`** — 4 páginas materialmente órfãs com conteúdo de valor. Inserir links no corpo das páginas-âncora. Gravidade média.
3. **Reorganização do nav** — sub-grupo "Aprofundamento técnico" + sub-grupo "Guias operacionais" separa `modelo_abm`/`brincar`/`paper` dos atos numerados e separa `uso`/`comandos`/`transparencia` das páginas teóricas. Decisão pendente. Gravidade baixa a média.
4. **`resultados.md` sem `▶ Ato 4 →`** explícito no fechamento. Gravidade baixa.
5. **`normas.md`, `condutas.md`, `choques.md`, `plano_melhorias.md`** — sub-tese antiga ainda. Gravidade baixa.

Esta auditoria fecha o trabalho de revisão estrutural da rodada de jun/2026. Os fixes de gravidade média deste documento ficam para a próxima sessão.