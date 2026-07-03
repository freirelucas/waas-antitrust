# Handoff de sessão — rumo ao camera-ready

Documento interno de passagem de bastão entre sessões de trabalho autônomo.
**Não faz parte do site publicado** (fica na raiz, fora de `docs/`, portanto o
MkDocs não o constrói). Escrito em português acadêmico, como o resto do
repositório. Leia isto primeiro ao abrir uma sessão nova.

- **Data do handoff:** 03/07/2026
- **Objetivo declarado pelo autor:** *"simplificar a jornada para ficar
  camera-ready em 5 horas de trabalho autônomo."*
- **Estado do git no fechamento:** `HEAD = origin/branch = main = origin/main
  = e24883c` (sincronia a quatro pontas mantida).
- **Ramo de trabalho:** `claude/happy-clarke-eseuu`.

---

## 1. Onde paramos exatamente (o único fio em aberto)

Todo o conteúdo — paper, site, modelo, testes — está **coerente e completo**
para *circulação pública*. Resta **um** bloqueador mecânico, já diagnosticado
com precisão nesta sessão mas **não corrigido** (o autor optou por encerrar e
registrar):

> **O CI `paper.yml` está vermelho.** O PDF camera-ready não compila no CI.

### Causa-raiz (confirmada por log do run 28679734682, sha `e24883c`)

`scripts/gerar_figuras.py` gera as quatro figuras que o `paper/main.tex`
inclui via `\includegraphics` (01, 02, 03, 04). A figura **03**
(`viz/alpha_erosao_limiar.py`) **lê um parquet de dados**:

```
FileNotFoundError: [Errno 2] No such file or directory:
'results/alpha_erosao_grade.parquet'
```

Esse parquet é produzido por `scripts/varredura_alpha_erosao.py` (varredura de
~3 min: 8 alphas × 10 seeds × 2 regimes × 40 tiques) e está **ignorado pelo
git** (`.gitignore:38 → results/*.parquet`). Logo, ele existe no laptop (onde
os testes locais passaram e me enganaram) mas **não existe no checkout limpo do
CI**. As figuras 01, 02 e 04 são autossuficientes; só a 03 depende de dado
externo.

> **Armadilha a memorizar:** "passou local" ≠ "passa no CI" sempre que uma
> figura ou teste depende de artefato em `results/` (gitignored). O CI parte de
> clone limpo. Cheguei a corrigir *outra* causa antes (só geravam 01/02;
> adicionei 03/04 ao `geradoras`) e a *terceira* (Unicode no LaTeX) — mas essa
> dependência de dado só apareceu quando o CI passou da geração da 01/02 e
> **quebrou na 03**. É a última camada da cebola.

### Como fechar (escolher UMA; recomendo a C)

- **C — comprometer o parquet (recomendada; ~2 min, risco mínimo).** O arquivo
  tem **8 KB**, é determinístico (seeds fixas em `DEFAULT_SEEDS`) e é o dado que
  sustenta uma figura *publicada* — arquivar dado de figura é boa prática, não
  dívida. **Há precedente no próprio repositório:** `results/calibracao_formal_r03.json`
  e `results/calibracao_r03_first_pass.json` **já são versionados** (o
  `.gitignore` bloqueia `*.parquet/*.csv/*.npz/*.pkl`, não `*.json`). Basta abrir
  a exceção e comprometer:

  ```bash
  # em .gitignore, logo após "!results/.gitkeep":
  #   !results/alpha_erosao_grade.parquet
  git add -f results/alpha_erosao_grade.parquet .gitignore
  ```

  Regenerar o parquet, se preciso, antes de comprometer:
  `python scripts/varredura_alpha_erosao.py` (grava em `results/`).

- **B — gerar no CI antes das figuras (~3 min a mais de CI; sem binário).**
  Inserir em `.github/workflows/paper.yml`, **antes** do passo
  `gerar_figuras.py` (linha 31), um passo
  `run: python scripts/varredura_alpha_erosao.py`. Determinístico (seeds fixas),
  mantém a filosofia "regenerável da fonte, zero binário versionado". Custa
  tempo de CI a cada build que toca `paper/`.

- **A — figura autogeradora (mais código, mais frágil).** Fazer
  `alpha_erosao_limiar.gerar_figura` rodar a varredura em processo quando o
  parquet faltar. Rejeitada: acopla lógica de varredura à de plotagem e infla o
  tempo silenciosamente.

**Recomendação:** **C**, por consistência com o precedente dos JSON já
versionados e por ser o caminho mais curto e determinístico ao verde. Depois de
qualquer opção: confirmar o run `paper.yml` verde e baixar o artifact
`paper/main.pdf` — *esse* PDF é o entregável camera-ready.

### Gates que JÁ estão verdes (não regrediram)

`pytest` (385 testes, 94% cobertura, piso 85%), `ruff`, `black`,
`mkdocs build --strict`, e o **deploy do site** (GitHub Pages). O vermelho é
**exclusivo** do `paper.yml` (compilação do PDF). O site publicado está no ar e
íntegro.

---

## 2. O que "camera-ready" significa aqui (duas barras)

Registrado em detalhe em `CHECKLIST_CAMERA_READY.md`. Resumo:

| Meta | Barra | Estado |
|---|---|---|
| **Circulação pública** (SSRN, seminário, público hostil informal) | coerência interna completa, sem buracos de redação, predições enquadradas com rigor | **atingida** (só falta o PDF do CI compilar — item §1) |
| **Submissão a periódico com referee** (JCLE, Antitrust LJ, RIO) | + calibração contra dado real + DOI | **bloqueada por 2 itens de ação humana** (§4) |

A descoberta que *simplificou a jornada*: o LaTeX do paper (§3 e §4) **já estava
completo** — o "primeira redação" era resíduo desatualizado apenas no espelho do
site (`docs/paper.md`), já corrigido. Não havia seção a escrever; havia um
espelho a sincronizar e um CI a consertar.

---

## 3. Aprendizados técnicos (duráveis — poupam horas na próxima sessão)

1. **Link `.md` em HTML embutido vira 404 no MkDocs.** `<a href="pagina.md">`
   dentro de um `.md` **não** passa pelo processador de links do MkDocs — vai
   literal para o navegador e quebra. Use `<a href="pagina/">`. Foi a causa do
   404 da home e do `/sobre.md`. Markdown puro `[x](pagina.md)` é convertido
   normalmente; só o HTML cru escapa.

2. **O container é efêmero; o `.venv` não sobrevive.** Recriar quando sumir:
   ```bash
   python3.12 -m venv .venv && . .venv/bin/activate
   pip install -e ".[dev,docs]" && pip install pytest-mpl
   ```
   `mesa >= 3.5` **não** instala em 3.10/3.11 — exige Python 3.12.

3. **Tectonic é rígido com Unicode.** Caracteres que quebram/avisam no
   `main.tex`: `✓` (usar `\checkmark`), subscritos como `Cᵩ`/`Cₚ` (usar
   `$C_\varphi$`/`$C_p$`), e cedilha/til dentro de modo matemático (tirar do
   `$...$` e escrever como texto). Rodar o CI é a única prova real — o
   compilador local pode divergir.

4. **Dependência figura→dado é a armadilha do `paper.yml`.** Ver §1. Toda figura
   nova incluída no paper via `\includegraphics` **precisa** de uma entrada no
   dicionário `geradoras` de `scripts/gerar_figuras.py` **e** ou é
   autossuficiente (roda com defaults, como 01/02/04) **ou** tem seu dado
   versionado/gerado no CI (como 03 precisa passar a ser).

5. **`gerar_figuras.py` só produz o que está em `geradoras`.** O paper referencia
   figuras por nome de arquivo (`01_...`, `02_...`, `03_...`, `04_...`); se o
   nome não está no dicionário, o arquivo não nasce e o LaTeX falha com
   `File '03_...' not found`. Mantê-los em espelho com os `\includegraphics`.

6. **Disciplina de sincronia a quatro pontas.** O padrão desta sessão foi manter
   `HEAD = branch = origin/branch = main = origin/main` a cada commit. Antes de
   declarar "sincronizado", conferir com `git rev-parse` nas quatro pontas.
   Cuidado com cache local de "unrelated histories" — foi um falso alarme; o
   `origin/main` real estava à frente e o merge era fast-forward.

---

## 4. Aprendizados de conteúdo e linguagem (princípios editoriais duráveis)

Estes são pedidos explícitos do autor ao longo da sessão. **Respeitar em toda
edição futura do site/paper:**

1. **Hierarquia LCMC > WaaS é inviolável.** A **LCMC** (Leniência Condicionada à
   Massa Crítica — canal de depósito condicional, Ayres-Unkovic 2012; análogo
   Callisto) é *o mecanismo*. O **WaaS** (recompensa via TCC, Art. 12 Res.
   21/2018) é **apenas um dos cinco instrumentos opcionais** de internalização,
   não sinônimo do mecanismo. Versões internas antigas confundiram os dois; o
   produto acabado **nunca** deve tratá-los como equivalentes.

2. **O site é produto acabado, não diário de desenvolvimento.** Remover do corpo
   das páginas de leitura primária: meta-narrativa de processo ("v1/v2/v3",
   "reframe", "correção radical", "literatura interna do projeto"), códigos de
   backlog (`R-XX`, `F6`, `v2.X`) e nomes de variável Python. Nas palavras do
   autor: *"lá é produto acabado, e não papo comigo ou contar história do
   desenvolvimento que só confunde."* (Nota: ainda há resíduo desse tipo em
   `docs/uso.md` e `docs/colaborar.md` — R20/R26/R27/R28/R29/R30, F6, nomes de
   variável — que são páginas de uso/contribuição, público mais técnico; se o
   autor quiser a mesma limpeza que fiz nas páginas de leitura primária, essa é
   uma tarefa opcional aberta.)

3. **Paleta sóbria, não comercial.** O verde saturado original lia como "produto
   de startup". Migrado para grafite/ardósia acadêmico em `viz/paleta.py`,
   `mkdocs.yml` (primary `black`, accent `indigo`) e no bloco "Atenuação
   acadêmica" de `docs/stylesheets/extra.css`. Manter esse registro visual.

4. **Nunca inventar referência nem dado** (CLAUDE.md, restrição científica). Toda
   citação deve ser verificável; toda calibração externa cita fonte primária no
   docstring. As 12 citações `[?]` não-verificadas vivem **só** na bibliografia
   estendida do site (`docs/REFERENCES.md`) — **nenhuma** está no paper.

5. **N\* enquadrado como predição derivada, não ajuste.** `N* ≈ 1.679` firmas é
   apresentado como predição *derivada* (não fitada), com teste de falsificação
   especificado (cruzar com firmas acima do limiar do Art. 88 — R$ 75 mi — em
   CNAE 62/63) e teste de sanidade que **sobrevive** (73 investigações/2024 ÷
   1.679 ≈ 4,3% de cobertura anual, ordem de grandeza plausível). Ver
   `\label{sec:nstar}` no paper. O teste de sanidade foi derivado de dado **já
   citado e verificável** — não inventei número.

---

## 5. Depende de ação humana (os 2 bloqueadores de submissão a periódico)

Nenhum é automatizável; ambos detalhados em `CHECKLIST_CAMERA_READY.md` §"Depende
de você".

1. **DOI Zenodo (~10 min).** Ligar integração Zenodo↔GitHub, `git tag -a v0.2.0`,
   publicar release pela UI (as *release notes* v0.2.0 já estão prontas no
   checklist). Colar o DOI em `CITATION.cff`, `docs/sobre.md`, `README.md`.

2. **Cruzar N\* com dado real (~meia diária, requer dataset).** Filtrar IBGE-RAIS
   por CNAE 62/63 + faturamento ≥ R$ 75 mi e comparar com 1.679. Dataset **não
   está no repositório**. Receita em `docs/calibracao_pendente.md` §1. O teste de
   sanidade já feito é suficiente para *circular*; o definitivo é o que
   *periódico com referee* exige.

---

## 6. Visão de futuro (o que fortalece o trabalho, em ordem de alavancagem)

**Curto prazo (fecha o camera-ready pleno):**
- Consertar o `paper.yml` (§1, opção C) → PDF verde.
- Os 2 itens de ação humana (§5) → submissível a periódico.

**Médio prazo (blinda contra público hostil qualificado):**
- **Doutrina brasileira de citação → engajamento.** Forgioni, Salomão Filho,
  Ferraz Jr. hoje aparecem citados por nome; um parecer jurídico adversário
  exige que o argumento *dialogue* com eles (reserva de lei vs. resolução
  infralegal, Art. 4º II/III da Lei 12.529 como base autônoma). É a defesa mais
  fraca hoje.
- **Fechar as 12 citações `[?]`** da bibliografia estendida do site, ou removê-las
  se não-verificáveis (a regra "nunca inventar" vale para as duas direções).
- **Formalizar a Proposição 2 forte** (unicidade global do equilíbrio sob
  heterogeneidade) — hoje conjectura aberta declarada. Esboço de prova em
  `docs/ODD.md`; qualquer mudança no modelo que a afete exige revisar o esboço.

**Longo prazo (decisões de desenho rastreadas, exigem conversa — não piloto
automático):** ver `docs/DECISIONS.md`, R09–R13 e as decisões em aberto do
CLAUDE.md — reserva de lei vs. resolução infralegal; modelar o Advogado/Assessoria
como agente estratégico; instrumento empírico para a topologia de rede intra-firma;
co-autoria com Felipe Roquete (origem da hipótese, 06/09/2022) rastreada em D04.
Cada uma alteraria material e Proposições; **cada uma exige revisão explícita do
autor.**

---

## 7. Mapa de arquivos-chave (para orientar a sessão nova)

| Arquivo | Papel |
|---|---|
| `CHECKLIST_CAMERA_READY.md` | Estado de prontidão + release notes v0.2.0 prontas |
| `HANDOFF_SESSAO.md` | Este documento |
| `paper/main.tex` | O paper (10 seções, completo). Fig. 03 em `:342` |
| `scripts/gerar_figuras.py` | Gera 01–04 para o paper; dicionário `geradoras` |
| `scripts/varredura_alpha_erosao.py` | Produz `results/alpha_erosao_grade.parquet` (fig. 03) |
| `src/waas_antitrust/viz/alpha_erosao_limiar.py` | Fig. 03 — **lê o parquet** (a dependência) |
| `.github/workflows/paper.yml` | CI do PDF (vermelho — passo `gerar_figuras.py:31`) |
| `docs/paper.md` | Espelho do paper no site (sincronizado com o LaTeX) |
| `docs/calibracao_pendente.md` | Receita do teste definitivo de N\* (RAIS/CNAE) |
| `docs/DECISIONS.md` | Decisões de desenho em aberto (R09–R13, D04–D06) |
| `docs/ODD.md` | Proposições 1–5 com esboços de prova |
| `CLAUDE.md` | Contrato de estilo/idioma/restrições — reler sempre |

---

**Resumo de uma linha para a próxima sessão:** *tudo pronto para circular; falta
compilar o PDF no CI (comprometer `results/alpha_erosao_grade.parquet`, 8 KB,
opção C do §1) e, para periódico, os 2 itens de ação humana do §5.*
