# Plano de 5 horas — da leitura do handoff à versão *camera-ready*

Documento de planejamento operacional para uma sessão de trabalho autônomo
de **cinco horas**, com o objetivo declarado pelo autor: *"simplificar a
jornada para ficar camera-ready em 5 horas."* Fica na raiz (fora de `docs/`),
portanto o MkDocs **não** o constrói — é instrumento interno, como o
`HANDOFF_SESSAO.md`.

- **Base de leitura:** `HANDOFF_SESSAO.md` (§1 a §7) e
  `CHECKLIST_CAMERA_READY.md`.
- **Ramo de trabalho:** `claude/leniencia-condicionada-massa-5ccysm`.
- **Data:** 03/07/2026.

---

## 0. Diagnóstico de partida (verificado nesta leitura, não herdado)

Antes de planejar, confirmei o estado real contra o que o handoff afirma —
porque a armadilha registrada em `HANDOFF_SESSAO.md` §3.4 é justamente
"passou local ≠ passa no CI". Achados:

| Afirmação | Fonte | Verificação | Veredito |
|---|---|---|---|
| PDF do paper **não** compila no CI (fig. 03 sem dado) | Handoff §1 | `git ls-files results/` → só JSON; `ls results/*.parquet` → vazio; `.gitignore:38` bloqueia `*.parquet` | **Confirmado — bloqueador vivo** |
| "PDF compilável" | Checklist, linha `[x]` | Contradiz o achado acima | **Aspiracional, ainda falso** |
| Fig. 03 lê `results/alpha_erosao_grade.parquet` | Handoff §7 | `scripts/gerar_figuras.py:35` mapeia `03_...` → `alpha_erosao_limiar.gerar_figura`, que lê o parquet | **Confirmado** |
| `paper.yml` roda a cada push | implícito | `.github/workflows/paper.yml:4` → gatilho só em `push` a `main` **e** `workflow_dispatch` | **Parcial — não roda em ramo de feature** |

**Consequência de desenho para o plano:** o único bloqueador mecânico do
*camera-ready de circulação* é a dependência figura→dado da fig. 03. E
verificar a correção **exige** `workflow_dispatch` no ramo (ou merge a
`main`), porque o `paper.yml` ignora ramos de feature. Isso reordena a
sessão: a correção do CI é a **primeira** hora, não a última, para deixar o
ciclo de verificação longo (Tectonic ~2–3 min) rodando cedo.

**As duas barras de *camera-ready* (do checklist), reafirmadas:**

- **Circulação pública** (SSRN, seminário, público hostil informal): coerência
  interna completa + PDF que compila. **A 1 bloqueador de distância.**
- **Submissão a periódico com referee**: + calibração contra dado real + DOI.
  **A 2 itens de ação humana de distância** (não automatizáveis — §5 abaixo).

O escopo autônomo desta sessão fecha **integralmente a barra de circulação** e
**prepara ao máximo** a barra de periódico, deixando aos itens humanos apenas o
que exige credencial (Zenodo) ou dataset externo (RAIS/CNAE).

---

## 1. Regra de ouro da sessão

> **Fechar o verde do `paper.yml` primeiro, verificá-lo por
> `workflow_dispatch`, e só então tocar em conteúdo.** Tudo o mais é reversível;
> um PDF que não compila invalida o rótulo "camera-ready" inteiro.

Disciplina de sincronia herdada do handoff §3.6: a cada commit, conferir
`HEAD = branch = origin/branch` com `git rev-parse`. **Não** replicar a
sincronia-a-quatro-pontas com `main` sem autorização — a instrução de ramo
desta sessão proíbe empurrar para `main`. Merge a `main` é decisão do autor.

---

## 2. Cronograma (5 blocos de ~60 min)

### Hora 1 — Desbloquear o PDF (o único bloqueador de circulação)

**Meta:** `paper.yml` verde, PDF `paper/main.pdf` baixável como artifact.

Adotar a **opção C** do handoff §1 (comprometer o parquet), pela consistência
com o precedente dos JSON já versionados (`results/calibracao_formal_r03.json`)
e por ser determinística (seeds fixas em `DEFAULT_SEEDS`).

1. Regenerar o dado da fonte (garante que o binário corresponde ao código atual,
   ~3 min):
   ```bash
   python scripts/varredura_alpha_erosao.py   # grava results/alpha_erosao_grade.parquet
   ```
2. Abrir a exceção no `.gitignore` (logo após `!results/.gitkeep`):
   ```
   !results/alpha_erosao_grade.parquet
   ```
3. Comprometer com `-f` (o padrão glob ainda o ignoraria sem a exceção):
   ```bash
   git add -f results/alpha_erosao_grade.parquet .gitignore
   git commit -m "fix(paper): versiona parquet da fig. 03 — destrava compilação do PDF no CI"
   ```
4. **Verificação obrigatória** (o passo que o handoff pulou): como o `paper.yml`
   não roda em ramo de feature, disparar manualmente:
   ```bash
   git push -u origin claude/leniencia-condicionada-massa-5ccysm
   # via MCP GitHub: actions_run_trigger em paper.yml, ref = o ramo (workflow_dispatch)
   ```
   Acompanhar o run; ao ficar verde, baixar o artifact `paper-pdf` e **abrir o
   PDF** — inspeção visual de que a fig. 03 aparece renderizada, não como caixa
   de erro. *Esse* PDF é o entregável.

**Gate de saída da Hora 1:** run `paper.yml` verde por dispatch + PDF inspecionado.
Se vermelho, ler o log **antes** de seguir — as camadas anteriores da cebola
(Unicode no Tectonic, dicionário `geradoras`) já foram descascadas, mas o log é a
única prova real (handoff §3.3).

> Contingência: se comprometer o parquet encontrar resistência (arquivo maior que
> o esperado, não-determinismo), cair para a **opção B** — inserir
> `run: python scripts/varredura_alpha_erosao.py` no `paper.yml` **antes** do
> passo `gerar_figuras.py`. Mantém "zero binário versionado" ao custo de ~3 min
> de CI por build. Não usar a opção A (figura autogeradora) — rejeitada no
> handoff por acoplar varredura à plotagem.

### Hora 2 — Sincronizar o espelho e auditar a coerência LCMC > WaaS

**Meta:** garantir que nenhuma edição futura reintroduziu a confusão que o
handoff §4.1 declara "inviolável", e que o site espelha o LaTeX.

1. `diff` conceitual entre `paper/main.tex` (§3, §4) e `docs/paper.md` — o
   handoff registra que o "primeira redação" era resíduo do espelho, já
   corrigido; **reconfirmar** que continua sincronizado após a Hora 1.
2. Varredura de regressão da hierarquia: `grep -rn -i "waas" docs/ paper/` e
   conferir que "WaaS" aparece **só** como um dos cinco instrumentos opcionais
   de internalização (recompensa via TCC, Art. 12 Res. 21/2018), nunca como
   sinônimo do mecanismo. A LCMC é o mecanismo; o WaaS é instrumento.
3. `mkdocs build --strict` limpo (gate já verde; confirmar que não regrediu).

**Gate de saída:** zero ocorrência de "WaaS = mecanismo"; `mkdocs --strict` limpo.

### Hora 3 — Enquadramento de predições e limitações (blindagem contra referee)

**Meta:** que cada afirmação forte sobreviva a leitura hostil. Sem inventar
dado (CLAUDE.md, restrição científica inviolável).

1. Reler §5.1 do paper (`\label{sec:nstar}`): confirmar que `N* ≈ 1.679` está
   enquadrado como **predição derivada** (não ajustada), com teste de
   falsificação especificado e o teste de sanidade que sobrevive (73
   investigações/2024 ≈ 4,3% de cobertura). Confirmar que o número do teste de
   sanidade é **citado e verificável**, não inventado.
2. Reconferir as limitações declaradas: Prop. 2 forte como conjectura aberta;
   Prop. 5 forte refutada empiricamente (sobrevive a fraca); calibração
   internacional pendente. Todas explícitas no paper **e** em
   `docs/limitacoes.md`.
3. Zero citações órfãs: reconferir que as 26 chaves de `paper/main.tex` têm
   entrada em `paper/refs.bib`, e que nenhuma das 12 referências `[?]`
   (não-verificadas) vazou da bibliografia estendida do site para o paper.

**Gate de saída:** nenhuma predição sem teste de falsificação; nenhuma citação
órfã ou `[?]` no paper.

### Hora 4 — Preparar o que é humano para ser instantâneo (§5)

**Meta:** reduzir os dois bloqueadores de periódico ao mínimo clique humano.
Não são automatizáveis, mas o atrito é.

1. **DOI Zenodo:** confirmar que as *release notes* v0.2.0 estão prontas no
   checklist e que `CITATION.cff`, `docs/sobre.md`, `README.md` têm o **local
   exato** onde o DOI será colado (marcador claro). Deixar o comando de tag
   pré-escrito no `DEPLOY.md` §"Arquivamento Zenodo". Assim o autor faz
   `git tag -a v0.2.0 && git push`, publica pela UI, e só cola o DOI em 3 lugares
   já marcados — ~10 min viram ~3.
2. **Cruzar N\* com RAIS/CNAE:** reconfirmar que `docs/calibracao_pendente.md`
   §1 tem a receita completa (filtrar CNAE 62/63 + faturamento ≥ R$ 75 mi,
   comparar com 1.679, intervalo de aceitação [~500, ~5.000]). Deixar um
   **script-esqueleto** parametrizado em `calibracao/` que aceite o dataset e
   rode o cruzamento, com docstring citando a fonte primária — pronto para o
   autor apontar ao arquivo RAIS quando o tiver. (Não inventar o dado.)

**Gate de saída:** ambos os itens humanos reduzidos a "colar credencial / apontar
dataset"; nada de raciocínio pendente.

### Hora 5 — Verificação total, atualização do checklist e handoff

**Meta:** fechar a sessão em estado auditável, com o checklist refletindo a
**verdade** (não a aspiração).

1. Bateria completa de gates locais:
   ```bash
   pytest -x -q tests/           # 385 testes, piso de cobertura 85%
   ruff check src/ tests/
   black --check src/ tests/
   mkdocs build --strict
   ```
2. Reconfirmar o `paper.yml` verde (o run da Hora 1 ou um novo dispatch após os
   commits de conteúdo, se algum tocou `paper/`, `src/.../viz/` ou
   `gerar_figuras.py` — esses são os *paths* que disparam o workflow).
3. **Corrigir o checklist:** trocar o `[x] PDF compilável` de aspiracional para
   verdadeiro — só depois de o run verde existir de fato. Registrar o número do
   run e o sha.
4. Atualizar `HANDOFF_SESSAO.md` §1: o "único fio em aberto" foi fechado;
   registrar o novo estado e o que resta (só os 2 itens humanos).
5. Commit final, `git push -u origin claude/leniencia-condicionada-massa-5ccysm`,
   conferir `HEAD = branch = origin/branch`.

**Gate de saída da sessão:** todos os gates verdes **incluindo** `paper.yml` por
prova de run; checklist honesto; handoff atualizado; ramo empurrado.

---

## 3. O que NÃO fazer nesta sessão (fronteiras de escopo)

Do handoff §6 (longo prazo) e do CLAUDE.md (decisões em aberto) — cada um
**altera material e Proposições** e **exige revisão explícita do autor**. Fora
de piloto automático:

- Formalizar a **Proposição 2 forte** (unicidade global sob heterogeneidade) —
  hoje conjectura aberta; mexer no modelo exige revisar o esboço em `docs/ODD.md`.
- **Doutrina brasileira de citação → engajamento** (Forgioni, Salomão Filho,
  Ferraz Jr.; reserva de lei vs. resolução infralegal) — é a defesa mais fraca
  hoje, mas é trabalho de argumentação jurídica que o autor deve conduzir.
- Modelar o **Advogado/Assessoria** como agente estratégico; instrumento
  empírico da topologia intra-firma; co-autoria com Felipe Roquete (D04). Tudo
  em `docs/DECISIONS.md` (R09–R13) — **conversa, não código**.
- **Empurrar para `main`** — a instrução de ramo desta sessão o proíbe sem
  permissão explícita. Merge é decisão do autor.

---

## 4. Riscos e contingências

| Risco | Sinal | Mitigação |
|---|---|---|
| `paper.yml` continua vermelho após a opção C | log do run | Ler o log; se for nova camada (Unicode, path), descascar; senão cair para opção B (§Hora 1) |
| Parquet não-determinístico entre execuções | `git diff` mostra bytes distintos ao regenerar | Fixar/registrar `DEFAULT_SEEDS`; se persistir, opção B (gerar no CI) elimina o binário |
| Espelho `docs/paper.md` diverge do LaTeX de novo | `diff` na Hora 2 | Sincronizar; anotar no handoff que o espelho é fonte recorrente de deriva |
| Sessão estoura 5 h | cronômetro | Prioridade estrita: Horas 1–2 fecham a **circulação** (a meta mínima). Horas 3–5 fortalecem, mas a barra de circulação já estará atingida ao fim da Hora 2 |

---

## 5. Definição de pronto (o que "camera-ready" significa ao fim das 5 h)

- **Circulação pública: ATINGIDA** — PDF compila no CI (provado por run verde +
  inspeção visual), coerência LCMC > WaaS íntegra, predições com teste de
  falsificação, zero citação órfã. *Pode ir para SSRN/seminário.*
- **Submissão a periódico: PREPARADA AO LIMITE AUTÔNOMO** — resta apenas (1)
  ligar Zenodo e colar o DOI em 3 lugares marcados (~3 min humanos) e (2) apontar
  o dataset RAIS/CNAE ao script-esqueleto (~meia diária humana). Nenhum
  raciocínio pendente; só credencial e dado externo.

**Resumo de uma linha:** *a Hora 1 fecha o único bloqueador de circulação
(parquet da fig. 03 → PDF verde, verificado por `workflow_dispatch`); as Horas
2–5 blindam o conteúdo e reduzem os 2 itens humanos a um clique — deixando o
trabalho camera-ready para circular e a um passo humano de submissível.*
