# Auditoria completa — 16/07/2026

Documento interno de auditoria. **Não faz parte do site publicado** (fica na
raiz, fora de `docs/`, portanto o MkDocs não o constrói). Escrito em português
acadêmico. Cobre quatro dimensões: reprodutibilidade técnica, coerência de
metadados, integridade científica e integridade jurídica.

- **Escopo solicitado:** auditoria completa nas quatro dimensões.
- **Entregável:** relatório + correções seguras e inequívocas aplicadas; juízos
  científicos e jurídicos deixados como recomendações ao autor.
- **Ambiente:** venv Python 3.12 recriado do zero (`pip install -e ".[dev]"`),
  gates do CI replicados localmente.

---

## 1. Sumário executivo

O repositório está **substancialmente saudável**: os quatro portões do CI
(`ruff`, `black`, `pytest`+cobertura, `nbval` do demo) passam, e o paper está
livre de citações órfãs. A auditoria encontrou, no essencial, **deriva de
números entre metadados** (já corrigida) e **um bug real no orquestrador de
figuras** (já corrigido), além de **um risco jurídico de verbatim** que
permanece como recomendação por exigir juízo do autor.

| Dimensão | Veredicto | Ação |
|---|---|---|
| Reprodutibilidade técnica | Verde, com 1 bug corrigido | corrigido |
| Coerência de metadados | Deriva de números confirmada | corrigido |
| Integridade científica | Sólida e honesta | nenhuma (positivo) |
| Integridade jurídica | Risco E04 (verbatim) em aberto | recomendação |

---

## 2. Reprodutibilidade técnica (verdade medida)

Gates replicados do `.github/workflows/tests.yml` num checkout limpo:

| Gate | Resultado medido |
|---|---|
| `ruff check src/ tests/` | **passou** (0 violações) |
| `black --check src/ tests/` | **passou** (80 arquivos) |
| `pytest -m "not slow" --cov` | **384 passaram, 1 desmarcado (slow)** — 385 no total |
| Cobertura | **94,31%** (piso do CI 85%) |
| `nbval` `WaaS_demo.ipynb` | **7 passaram** (~12 s) |
| `scripts/gerar_figuras.py` (4 figuras do paper) | **geradas** (01, 02, 03, 04) |
| `driver.py` (modelo · Sobol · jogo global · viz) | **saída 0** |

**Contagens de verdade** (medidas, não presumidas):

| Grandeza | Valor real | Como medido |
|---|---|---|
| Testes | **385** (384 rápidos + 1 `slow`) | `pytest --co` |
| Cobertura | **94%** | `pytest --cov` |
| Cenários | **27** | `CATALOGO_CENARIOS` em `cenarios.py` |
| Figuras do site | **23** | `docs/img/*.png` |
| Reporters | **39 chaves** (38 excluindo o índice `tique`) | `DataCollector` em `model.py` |

### 2.1 [CORRIGIDO] Bug em `scripts/regerar_todas_as_figuras.py`

O orquestrador que "regera todas as figuras do site a partir do código"
**quebrava na figura 10**. `_gerar_script` anexava `sys.executable` a um comando
que já continha o literal `python` (`"... && python -m waas_antitrust.viz.
alpha_erosao_limiar"`), produzindo `['.../python', 'python', '-m', ...]` →
`can't open file '.../python'`. Correção: remover um token `python`/`python3`
inicial antes de anexar o interpretador do venv. Após a correção, as figuras
03, 10 e 19 (as três geradas por script) regeneram com saída 0. É uma via de
reprodutibilidade documentada no docstring do próprio script — o CI não a
exercita (usa `gerar_figuras.py`, que gera as 4 figuras do paper e é
independente).

### 2.2 [CORRIGIDO] Débito de formatação em `scripts/calibrar_formal_multitarget.py`

O arquivo estava **não-conforme com `black`** sob a configuração original
(py310) *e* sob py312 — invisível porque o CI só roda `black --check src/
tests/`, enquanto o alvo `make format`/`lint` e o hook `pre-commit` incluem
`scripts/`. Aplicado `black` (formatação canônica). `src/`, `tests/` e
`scripts/` ficam limpos.

### 2.3 Compilação do paper — não executada localmente (limite de ambiente)

O binário do Tectonic não instalou: o download do release no GitHub retorna
**403 pelo proxy** (limite de rede do ambiente, não defeito do repositório). A
compilação é um gate verde conhecido do CI (`paper.yml`). Verificações estáticas
de prontidão foram feitas em §4.2.

### 2.4 `nbval` do caderno é impraticavelmente lento

`WaaS_demo.ipynb` (validado no CI) roda em ~12 s. Já o comando documentado no
CLAUDE.md `pytest --nbval-lax notebooks/` e o alvo `make caderno`
(`WaaS_caderno_v2.ipynb`) **não completaram em >7 min** numa sessão limitada.
Não é defeito, mas o comando documentado engana quanto ao custo.
**Recomendação:** documentar o tempo esperado do caderno didático, ou marcá-lo
como `slow`/opcional, mantendo apenas o demo como validação prática.

---

## 3. Coerência de metadados (deriva de números)

Confirmada deriva ampla de números entre documentos — em um caso, **dentro do
mesmo arquivo** (`docs/modelo_abm.md` afirmava "27 cenários" no cabeçalho do §5
e "22 cenários" no corpo). Reconciliados ao valor **medido** na §2.

| Grandeza | Valor canônico | Ocorrências stale corrigidas |
|---|---|---|
| Testes | **385** | `.zenodo.json`, `CITATION.cff` (diziam 364) |
| Cenários | **27** | `.zenodo.json`, `CITATION.cff`, `docs/modelo_abm.md` (heading + âncora do sumário + corpo; diziam 22/23) |
| Versão do pacote | **0.2.0** | `pyproject.toml` (dizia 0.1.0) |

Notas:
- A âncora do sumário em `modelo_abm.md` foi ajustada junto do cabeçalho
  (`#5-atalho-cenarios-canonicos-23` → `-27`) para não quebrar o link interno
  sob `mkdocs --strict`.
- `pyproject.toml` recebeu `0.2.0` (não `0.2.0-draft`): PEP 440 não aceita o
  sufixo `-draft`; o estado de rascunho continua rotulado em `.zenodo.json`
  (`0.2.0-draft`) e `CITATION.cff`. Direção da correção segue o consenso desses
  dois metadados (o `pyproject` era o único outlier em 0.1.0).
- **Não alterados (por serem registros históricos datados):** menções a
  "364 testes", "22 cenários", "20 no catálogo", "18 figuras" em
  `CHANGELOG.md`, `docs/DECISIONS.md`, `docs/brainstorm_revisao.md` e
  `docs/revisao_personas.md` são estados pontuais de rodadas passadas;
  reescrevê-los falsificaria o log. `docs/DECISIONS.md` T05 (93%) idem.

### 3.1 [CORRIGIDO] Alvo de cobertura no CLAUDE.md

CLAUDE.md dizia "Cobertura-alvo: 80%" enquanto o CI impõe piso 85%
(`--cov-fail-under=85`) e a cobertura real é ~94%. Reconciliado para 85%
(com nota do valor atual).

### 3.2 Configuração alinhada ao Python 3.12 [CORRIGIDO]

`requires-python >= 3.12`, mas `ruff.target-version` e `black.target-version`
apontavam para py310/py311. Alinhados para `py312`. Reverificado: `ruff` e
`black --check src/ tests/` seguem verdes (o único arquivo afetado por py312 já
era o débito pré-existente da §2.2, também corrigido).

---

## 4. Integridade científica

**Veredicto: sólida e honesta.** Nenhuma correção necessária.

- **Proposições 1–3** estão declaradas com transparência em `docs/ODD.md` como
  **conjecturas abertas** com testes direcionais (`test_model.py`,
  `test_jogo_global*.py`, `test_corrida.py`), e o ODD é explícito (§2, linha 53)
  em que o código usa **limiares heurísticos**, não o equilíbrio formal do jogo
  global nem um modelo formal de contágio.
- **Calibração**: os quatro módulos de `calibracao/` (`saito`, `brasscom`,
  `cade`, `transparencia_cade`) **citam fonte primária** no docstring, com
  caveats explícitos do que a fonte não reporta (ex.: Saito não reporta mediana
  → marcada `None`).
- **Vocabulário canônico (CLAUDE.md)**: sem anglicismos proibidos em `src/`
  (nenhum `bounty`, `small-world`, `stress test`, `sweep`). "compliance" aparece
  só em `cultura_compliance` — cabe na exceção da literatura jurídica brasileira.

### 4.1 Citações do paper — sem órfãs (positivo)

26 chaves `\cite*` no `paper/main.tex`, **todas** presentes em `paper/refs.bib`
(32 entradas; 6 não citadas, o que é benigno). **Nenhuma** marcação `[?]` no
corpo do paper. Confirma a alegação do CHECKLIST.

### 4.2 Prontidão de compilação (estática) e observações menores

- `\bibliographystyle{plainnat}` com `natbib` author-year — correto (a correção
  do handoff persiste). Sem Unicode problemático no `main.tex`.
- **Menor:** o paper inclui via `\includegraphics` apenas as figuras **02, 03,
  04**; `gerar_figuras.py` ainda gera a **01** (`inversao_utilidade`), que o
  paper não usa. Inofensivo (figura gerada e não incluída), mas a afirmação do
  handoff de "quatro figuras incluídas (01–04)" está desatualizada.
- **Menor:** dois `\label` de seção (`sec:cibernetica`, `sec:sociologia`) são
  definidos e nunca referenciados. Compila normalmente.

---

## 5. Integridade jurídica

### 5.1 [RECOMENDAÇÃO] Risco E04 — verbatim do Art. 12 da Res. CADE 21/2018

É o achado jurídico central e permanece **pendência do autor** (exige juízo e
verificação contra fonte oficial; a regra "não inventar" impede correção
automática).

1. **Duas redações internas divergentes** para o mesmo dispositivo, ambas
   **não verificadas contra o DOU**:
   - `paper/main.tex:180-185` cita, dentro de `\begin{quote}`, um texto que
     começa *"A vantagem auferida ou pretendida e o efetivo prejuízo causado
     serão considerados..."* — redação que se assemelha mais ao Art. 45/caput do
     que ao Art. 12 da Resolução;
   - `data/normas/resolucao_cade_21_2018_art_12.txt:24` traz redação **diferente**
     — *"Será considerada, como circunstância atenuante para o cálculo da
     contribuição pecuniária, a comprovação, pelo Compromissário, de
     ressarcimento..."* — e o próprio arquivo marca STATUS = "redação
     consolidada de teste", com E04 explicitamente ABERTO.
2. O paper apresenta a sua versão como **"O texto vigente do Art.~12 é o
   seguinte:"** — asserção de autoridade **sem caveat**, apesar de E04 aberto.
3. **`docs/DECISIONS.md` (E04) afirma que o paper carrega "rodapé TODO em
   §Mecanismo"** reconhecendo que cita o Art. 12 "de memória". **Isso é falso:**
   `paper/main.tex` não contém **nenhum** `\footnote`. O documento de decisões
   superestima a honestidade do paper nesse ponto.

**Recomendação:** verificar o texto integral do Art. 12 contra a fonte oficial
(o PDF canônico do CADE já está referenciado em
`data/normas/resolucao_cade_21_2018_art_12.txt`), reconciliar as duas redações
internas ao verbatim verdadeiro e — enquanto E04 estiver aberto — suavizar a
asserção "texto vigente" no paper (ou reintroduzir de fato o caveat que o
DECISIONS.md alega existir).

### 5.2 Demais fontes primárias — status honesto

- Lei 12.529/2011: Art. 85 caput é **verbatim verificado**; §§, Art. 86/87 são
  "redação de teste" com nota explícita.
- Lei 13.608/2018 (Arts. 4-A/4-B/4-C): **paráfrase**, marcada como tal; o Art.
  4-C §3º embasa o caveat de escopo do R07.

### 5.3 Atribuição institucional — conforme

O repositório **divulga** o vínculo do autor com o IPEA (DIEST/COGIT) mas
**desassocia** a publicação de forma consistente (README, `docs/sobre.md`,
`docs/colaborar.md`, `INSTITUTIONAL.md`); `docs/sobre.md:19` documenta que uma
atribuição indevida anterior foi **removida** na v0.2.0-draft. Sem inferência de
posições do CADE: o paper enquadra a re-caracterização do Art. 12 como
"construção controvertível, sujeita a anulação judicial" — hipótese do projeto,
não posição institucional atribuída.

---

## 6. Observações menores (sem ação / registro)

- **`pre-commit` roda `ruff-format` E `black`** (`.pre-commit-config.yaml`
  linhas 19 e 24). São dois formatadores sobre os mesmos arquivos; convivem hoje,
  mas podem disputar formatação no futuro. Escolha de configuração do autor.
- **`pytest-mpl`**: `mpl-baseline-path = tests/baseline_images` aponta para
  diretório **inexistente**. Como `--mpl` não é passado no CI, a config fica
  dormente. Fechar exige gerar baselines (`--mpl-generate`) — trabalho do autor —
  ou remover a config dormente.
- **`regerar_todas_as_figuras.py`** cobre as figuras 03–19 (docstring diz "19
  figuras"); as figuras 01, 02 e 20–23 não estão em seu catálogo. Extensão de
  cobertura fica como melhoria opcional.

---

## 7. Resumo das correções aplicadas

| Arquivo | Mudança |
|---|---|
| `scripts/regerar_todas_as_figuras.py` | Corrige bug de subprocess (figura 10) |
| `scripts/calibrar_formal_multitarget.py` | `black` (débito de formatação pré-existente) |
| `.zenodo.json` | 364→385 testes; 22→27 cenários |
| `CITATION.cff` | 364→385 testes; 22→27 cenários |
| `docs/modelo_abm.md` | 22→27 cenários (heading + âncora do sumário + corpo) |
| `pyproject.toml` | versão 0.1.0→0.2.0; `ruff`/`black` target-version →py312 |
| `CLAUDE.md` | cobertura-alvo 80→85% (com nota do ~94% atual) |

**Recomendações não aplicadas (juízo do autor):** verbatim do Art. 12 (E04) e
reconciliação das duas redações internas; suavizar "texto vigente" no paper;
baselines do `pytest-mpl`; runtime/marcação do caderno no `nbval`.

**Verificação final:** `ruff`, `black --check src/ tests/ scripts/` e `pytest -m
"not slow" --cov-fail-under=85` seguem verdes após as correções.
