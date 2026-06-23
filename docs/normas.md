# Módulo `normas/` — parsing programático de normas brasileiras

<p class="deck">Parser programático de normas jurídicas brasileiras (540 linhas de Python, 24 testes) que permite citar Art./§/Inciso/Alínea/Item verbatim a partir do corpus local, identificado por URN-LEX padrão LexML BR. Foi construído depois de pesquisa de metodologia que não encontrou parser pt-BR maduro disponível; o projeto criou o seu próprio, disciplinado pela LC 95/1998 (regras de elaboração legislativa).</p>

<p class="byline"><em>Anexo técnico</em> · módulo <code>normas/</code> · rascunho v0.2.0</p>

## Por que isso existe

A análise jurídica do projeto cita constantemente Lei 12.529/2011 Arts. 4º, 85, 86; Lei 13.608/2018 Art. 4º-C; Resolução CADE 21/2018 Art. 12; Lei 9.784/99 Art. 24. Citar de memória é frágil — o módulo `normas/` substitui memória por **recuperação programática a partir do corpus local versionado em git**.

A decisão crítica: **não fetch em tempo de execução**. A integridade do texto vem do Git, não de chamada HTTP a portal externo. Os textos vivem em `data/normas/*.txt` e são versionados como qualquer outro código.

## Arquitetura

```
src/waas_antitrust/normas/
├── urn.py              # URN-LEX (padrão LexML BR) + 4 URNs canônicas
├── articulacao.py      # Parser regex disciplinado por LC 95/1998
├── remissoes.py        # Extrator de remissões cruzadas
├── corpus.py           # Carrega data/normas/*.txt por URN
└── cite.py             # citar(urn, dispositivo) — API de superfície
```

## URN-LEX — identificadores persistentes

`URNLex` é dataclass frozen com 5 campos: `jurisdicao` (`br`), `autoridade` (`federal`/`cade`/`tjsp`), `tipo` (`lei`/`resolucao`), `data` (ISO YYYY-MM-DD), `numero`. A representação canônica é a string `urn:lex:br:federal:lei:2011-11-30;12529`.

Quatro URNs canônicas pré-definidas:

| Constante | URN | Norma |
|---|---|---|
| `URN_LEI_12529` | `urn:lex:br:federal:lei:2011-11-30;12529` | Lei 12.529/2011 (SBDC) |
| `URN_LEI_13608` | `urn:lex:br:federal:lei:2018-01-10;13608` | Lei 13.608/2018 (recompensa a informante) |
| `URN_LEI_13964` | `urn:lex:br:federal:lei:2019-12-24;13964` | Lei 13.964/2019 (Pacote Anticrime — alterou 13.608) |
| `URN_RESOLUCAO_CADE_21_2018` | `urn:lex:br:cade:resolucao:2018-12-13;21` | Resolução CADE 21/2018 (TCC) |

`URNLex.url_resolutor` devolve a URL pública do resolutor LexML — `https://www.lexml.gov.br/urn/<urn>`.

## Parser de articulação (LC 95/1998)

`parse_articulacao(texto: str) -> list[Dispositivo]` lê o texto da norma e devolve árvore de `Dispositivo`s. Cada nó carrega: `tipo` (`art`/`paragrafo`/`inciso`/`alinea`/`item`), `numero` (`85`/`1º`/`I`/`a`/`1`), `texto` (verbatim), `filhos`.

A heurística regex segue as **regras de elaboração da LC 95/1998**: artigo abre com `Art. N.` numeração arábica; parágrafo único é `Parágrafo único.`; parágrafo numerado é `§ Nº`; inciso é romano em maiúsculas; alínea é letra minúscula com `)`; item é arábica com `-`. O parser refere LC 95/1998 inline para auditoria.

`buscar_dispositivo(raizes, caminho) -> Dispositivo | None` navega a árvore por caminho dot-notado: `"art:85"`, `"art:85.par:1"`, `"art:85.par:1.inc:I"`.

## Corpus local

Três normas no corpus em `data/normas/`:

- `lei_12529_2011_arts_85_a_87.txt` — Lei 12.529/2011, Arts. 85-87 (TCC + leniência clássica).
- `lei_13608_2018_arts_4a_a_4c.txt` — Lei 13.608/2018, Arts. 4º-A a 4º-C (recompensa a informante).
- `resolucao_cade_21_2018_art_12.txt` — Resolução CADE 21/2018, Art. 12 (atenuante por ressarcimento).

`corpus.carregar_norma(urn) -> str` devolve o texto integral; `corpus.listar_normas()` lista as URNs disponíveis.

!!! warning "Status de verificação verbatim"

    Apenas o **Art. 85 caput da Lei 12.529** é verbatim conferido contra `INSTITUTIONAL.md` (que cita do Diário Oficial). Os demais dispositivos são **"redação consolidada para teste interno do parser"** com nota explícita no topo de cada `data/normas/*.txt` e caveat persistente em **E04** (`DECISIONS.md`): verificação verbatim contra DOU pendente.

## API de citação

```python
from waas_antitrust.normas import (
    URN_LEI_12529,
    URN_RESOLUCAO_CADE_21_2018,
    citar,
    citar_com_subitens,
    carregar_norma,
    extrair_remissoes,
    parse_urn,
)

# Citar Art. 85 caput da Lei 12.529 — VERBATIM verificado
print(citar(URN_LEI_12529, "art:85"))
# → "Art. 85. Nos procedimentos administrativos mencionados nos arts. 48, ..."

# Citar Art. 12 §1º da Resolução CADE 21/2018 com subitens
print(citar_com_subitens(URN_RESOLUCAO_CADE_21_2018, "art:12.par:1"))

# Extrair remissões de um texto qualquer
remissoes = extrair_remissoes("Conforme o art. 45, V e VI da Lei 12.529/2011 ...")
for r in remissoes:
    print(f"  → {r.tipo} {r.numero}, incisos {r.incisos}")

# Parsear uma URN de string
urn = parse_urn("urn:lex:br:federal:lei:2011-11-30;12529")
print(urn.url_resolutor)
# → https://www.lexml.gov.br/urn/urn:lex:br:federal:lei:2011-11-30;12529
```

## Extrator de remissões

`remissoes.extrair_remissoes(texto)` devolve lista de `Remissao` (frozen dataclass com `tipo`, `numero`, `incisos`, `alineas`, `paragrafos`). Reconhece padrões brasileiros: `"art. 45, V e VI"`, `"art. 85, § 1º"`, `"art. 12 § 1º, I, a"`. A varredura é regex disciplinada por LC 95/1998 e não inclui jurisprudência (apenas remissões a artigos/parágrafos/incisos/alíneas/itens).

Útil para mapear a teia de citações dentro do corpus: qual artigo cita qual? Isso permite, futuramente, construir um **grafo NetworkX de remissões** entre normas (pendência em `DECISIONS.md` T07).

## Cobertura de testes

24 testes em `tests/test_normas.py` cobrindo:

- URN-LEX (construção, parsing, igualdade, URL resolutor).
- Articulação (parser de artigo simples, com parágrafo, com inciso, com alínea, com item).
- Busca por caminho dot-notado.
- Remissões (regex matches em texto realista).
- Corpus (carregar URNs canônicas, listar disponíveis, erro em URN desconhecida).
- API `citar` e `citar_com_subitens`.

## Pendências (em ordem de prioridade)

1. **Verificação verbatim contra DOU**: E04 em `DECISIONS.md`. Apenas Art. 85 caput está conferido; os demais 8 dispositivos precisam audit verbatim contra publicação oficial.
2. **Gerador inverso**: dado um `Dispositivo`, produzir XML LexML conforme XSD. Útil para integração com Câmara/Senado.
3. **Comparador entre versões consolidadas**: Lei 13.608 antes/após Lei 13.964/2019. Essencial para análise da redação atual do Art. 4º-C §3º.
4. **Grafo NetworkX de remissões**: visualização da teia de citações entre normas do corpus.

## Como contribuir

Adicionar uma norma ao corpus:

1. Salvar o texto em `data/normas/<norma>.txt` com **nota verbatim no topo** indicando fonte (DOU, edição, data) ou disclaimer "redação consolidada para teste interno".
2. Adicionar a URN canônica em `urn.py` (`URN_NOVA = URNLex(...)`).
3. Adicionar entrada em `corpus.py` mapeando a URN ao arquivo.
4. Acrescentar teste em `tests/test_normas.py` que carregue e cite ao menos um dispositivo.
