# Brainstorm de melhorias — junho/2026

Lista organizada de pontos identificados em revisão de tom e
arquitetura, separados em **dívida concreta** (resolvível em 1–2 commits)
e **direções de pesquisa abertas**. Cada item indica gravidade
(`baixa`/`média`/`alta`) e onde no repositório vive a evidência.

A lista não é roteiro — é um espelho do estado atual para próximas
sessões.

## 0 · Resumo executivo da rodada jun/2026

Resumo dos itens fechados ao longo das múltiplas iterações desta rodada:

**Editorial (concluído):**
- Migração para padrão `deck`/`byline`/`lede` em 14 páginas-âncora.
- Cross-links para 4 páginas órfãs (`condutas`, `choques`, `normas`,
  `glossario`).
- Reorganização do nav em 5 grupos top-level coerentes.
- Auditoria de tom + crítica editorial + auditoria estrutural
  (3 documentos de revisão interna).

**Substantivo (concluído):**
- **R29 calibrado contra Saito (2021)** — cenário canônico com
  faixas derivadas do gradiente do Art. 86.
- **R29-iii — adesão estocástica por arquétipo** (#9) — decisão
  modulada por arquétipo ético/imitativo/racional/fairminded/
  oportunista/aleatório.
- **R29 × R26 cruzado** (#13) — cascata + erosão Coleman testáveis
  no mesmo cenário.
- **R29-iv — recompensa coletiva** (#17) — Marwell-Oliver 1993 como
  salvaguarda anti-erosão Coleman, com cenário canônico próprio.
- **R30-ii — assimetria entre jurisdições** (#11) — multiplicador de
  tamanho por firma com cenário BR=0.3 / US=1.5 / EU=1.0.
- **R30-iii — forum shopping por firmas** (#12) — risco modelado em
  P3 com reporter `n_forum_shopping_acum`.
- **Página `/operacional`** atendendo conselheiro CADE + compliance.
- **Doutrina BR expandida** em `INSTITUTIONAL.md` (Forgioni / Calixto
  Salomão / Tércio Ferraz Jr.).
- **Página `/calibracao_pendente`** documentando metodologia de
  fechamento para N\* × CNAE (#15), capacidade DOJ-ATR/DG-COMP (#16),
  faixas R29 sob conduta unilateral e Mussler-Macy multi-seed (#17b).
- **Esboço estendido da Proposição 2** sob heterogeneidade (#18) em
  `ODD.md` — versão fraca (existência + unicidade local) provável;
  versão forte conjectura.

**Catálogo:** 22 → 27 cenários canônicos. **Testes:** 364 → 380.

Os itens marcados como pendentes abaixo são os que sobrevivem à
rodada como direções de pesquisa aberta de gravidade mais alta.

## 1 · Resíduos de versões anteriores ainda no site

### 1.1 Concluído nesta rodada
- [x] Promoção do **Colab** removida de `uso.md`, `colaborar.md`,
  `comandos.md`, `resultados.md` (caminho rápido agora é o simulador
  in-browser; o caderno continua no repositório como artefato).
- [x] Banner "Documento histórico (v1)" no topo de
  `critica_x10.md` e "v2" em `critica_x10_v2.md` análogo ao
  pré-existente em `aprendizados_v2.md`.

### 1.2 Aberto — gravidade média
- [ ] Em `docs/ODD.md:80` e `docs/bem_publico.md:251` ainda lê-se
  "O WaaS é, no vocabulário de Ostrom, um *commons imposto de cima*".
  Sob v3 (LCMC > WaaS), essa frase passa a referir à **LCMC** ou ao
  **canal de depósito condicional**, não ao instrumento monetário WaaS.
  Substituir mantendo o argumento; preservar contexto em comentário.
- [ ] `docs/ODD.md:150` tem "quando o canal WaaS opera" — substituir por
  "quando o canal LCMC opera".
- [ ] `notebooks/WaaS_demo.ipynb` e `WaaS_brincar.ipynb` ainda contêm
  cabeçalho que se refere ao Colab e à hierarquia v2 (WaaS como
  protagonista). Atualizar ou marcar como "caderno legado" em README.
- [ ] `docs/aprendizados_v3.md` foi escrito antes de R29 e R30. Acrescentar
  pós-script breve apontando que esses dois marcos vieram depois e
  remetem ao [`mecanismo.md` Camada 5] e [`internacional.md` R30].

### 1.3 Aberto — gravidade baixa
- [ ] **Contagens espalhadas pelo site** (testes, cenários, figuras,
  reporters) dessincronizam a cada rodada. Inventário atual:
  `23 figuras`, `22 cenários`, `38 reporters`, `364 testes`. Migrar
  para um único include em `mkdocs.yml` ou variável em `extra.yml`.

## 2 · Tom e linguagem — sobreviventes do banho de loja propaganda

### 2.1 Frases comerciais ainda em texto
- [ ] `index.md` linha 7: "Esta é a história de uma proposta para
  destravá-la" (Ato 1 da v3) — substituído por parágrafo acadêmico nesta
  rodada; verificar se outras páginas mantiveram o tom narrativo
  "história de…".
- [ ] `paper.md` e `paper/main.tex` Abstract: "rascunho de trabalho";
  verificar coerência de tom entre site e paper.
- [ ] **"+1.363%"** no KPI do hero é tecnicamente válido (ΔW multi-seed
  Regime B/A), mas o valor sozinho soa marketing. Adicionar nota de
  rodapé com método ("mediana de 10 sementes; IC bootstrap 95% em
  `results/`"). KPI lateral também precisa de fonte verificável.

### 2.2 Estética ainda forte em alguns lugares
- [ ] **Simulador in-browser** (`brincar.md`) usa cards verdes
  gradient nos painéis de controle. A atenuação de jun/2026 cobriu
  hero/personas/KPIs, mas o painel do simulador ainda está com a
  paleta saturada anterior. Decidir se mantém (para destacar a
  interatividade) ou alinha ao restante.
- [ ] Ícones emoji (📰 ⚖️ 📐 🏛️ 🏢 🎓) nas persona-cards. Material
  Icons (`material/account-tie-outline` etc.) seriam mais consistentes
  com a tipografia editorial.

## 3 · Arquitetura do site

### 3.1 Páginas com sobreposição
- [ ] **`uso.md` × `comandos.md`** se sobrepõem em ~60% do conteúdo
  (instalação, CLI, fluxos comuns). Fundir em uma página única
  "Guia operacional", deixando `comandos.md` como referência rápida
  da CLI apenas.
- [ ] **`glossario.md` × `TERMINOLOGIA.md`** se sobrepõem: o primeiro é
  dicionário de termos, o segundo é referência canônica com sinônimos
  aceitos. Migrar para 1 página com 2 seções e remover duplicações.
- [ ] **`critica_x10.md` × `critica_x10_v2.md` × `aprendizados_v2.md` ×
  `aprendizados_v3.md`** — quatro páginas históricas. Embora cada uma
  tenha valor distinto, juntá-las numa seção "Histórico" do nav (em
  vez de "Desenvolvimento") melhoraria a hierarquia.

### 3.2 Páginas que poderiam virar uma só
- [ ] **`procedimento_cade.md` × `INSTITUTIONAL.md`** — ambas tratam do
  arcabouço normativo. Avaliar fusão ou cross-link explícito.
- [ ] **`bem_publico.md` × `modelagem_multiagente.md`** — tese de bem
  coletivo separada do desenho dos agentes. Cross-link forte ou seção
  unificada em "Teoria e modelo".

### 3.3 Navegação
- [ ] Nav atual tem 5 atos + 6 anexos com 4 sub-grupos + 7 itens de
  desenvolvimento. O número de cliques para chegar em "Procedimento
  CADE" ou "Limitações §jurídica" é alto. Considerar elevar
  `procedimento_cade.md` e `limitacoes.md` ao nível dos Atos
  (são leitura primária para advogadas e autoridades).
- [ ] Falta página única "Status atual" — quem entra hoje precisa
  juntar pedaços de `DECISIONS.md` + `CHANGELOG.md` + `aprendizados_v3.md`
  para entender onde o projeto está.

## 4 · Código ABM e testes

### 4.1 R29 — janela de adesão (aprovada esta semana)
- [ ] Decisão de adesão é determinística (`fator × W > custo`). Modelo
  realista adicionaria estocasticidade (sorteio entre arquétipos com
  probabilidade modulada pelo desconto).
- [ ] Não há cenário de combinação `R29 × R26 (erosão Coleman)` — a
  cascata de adesão *poderia* acelerar a erosão (mais notificações em
  janelas curtas). Falsificável.
- [ ] Faixas de desconto `(1.0, 0.7, 0.5, 0.3, 0.1)` são arbitrárias.
  Calibrar contra Saito (2021) — o gradiente já está no projeto para
  a fila inter-firma.

### 4.2 R30 — sinergia internacional (aprovada esta semana)
- [ ] Grupos econômicos assumem **simetria perfeita** entre jurisdições.
  No mundo real, Google Brasil ≠ Google US ≠ Google EU em tamanho
  (n_trabalhadores) e cultura organizacional. Parametrizar.
- [ ] **Forum shopping por firmas** mencionado como risco mas não
  modelado. Implementar como decisão da firma em P3: "se notificada em
  jurisdição X, posso correr para TCC clássico em jurisdição Y antes
  do gatilho global fechar".
- [ ] Diretiva (UE) 2019/1937 está modelada como `r_represalia` baixo
  na variante UE, mas a Diretiva tem dispositivos específicos (canal
  externo + interno + retaliation reversal). Modelo grosso.

### 4.3 Cobertura de testes
- [ ] **Sobol full** (`run_sobol_full.py --n-base 1024`) não roda em CI
  por tempo (várias horas). Versão `--n-base 64` roda em ~25s e cobre
  diagnóstico básico — adicionar como step opcional em GitHub Actions.
- [ ] **Cobertura linha-a-linha** não está medida. `pytest-cov` pode
  detectar caminhos não-cobertos em `model.step()` (fases P0-P5).
  Alvo realista: 85% para `src/waas_antitrust/`.
- [ ] **Testes de regressão visual** das figuras: hashing de bytes do
  PNG produzido contra valor conhecido (`pytest-mpl` faz isso). Hoje
  só smoke tests existem.

### 4.4 Dívida estrutural
- [ ] `WaaSModel.step()` tem ~250 linhas e ~12 fases lógicas. Refatorar
  em métodos privados `_fase_p0`, `_fase_p1` etc. (já existe `_aplicar_coordenacao_internacional`;
  estender o padrão).
- [ ] `WaaSParametros` tem 60+ campos. Considerar agrupar em
  sub-dataclasses (`ParametrosMecanismo`, `ParametrosTopologia`,
  `ParametrosAdversarial`).

## 5 · Modelo substantivo — direções de pesquisa abertas

### 5.1 Calibração
- [ ] **R03** fechou alvo único (TCC/ano); alvos 2 e 3 (sinais/tique,
  dano agregado) ainda abertos por identificabilidade. Calibração
  multi-alvo via gradiente pondera (não Nelder-Mead) está sugerida
  mas não implementada.
- [ ] **N\*** ≈ 1.679 firmas — predição falsificável contra número real
  de firmas sob jurisdição ativa do CADE. Falta cruzar com CNAE +
  receita anual.
- [ ] **`taxa_capacidade` para DOJ-ATR e DG-COMP** — usar dado real
  (FY2025 budget DOJ; orçamento DG-COMP 2024). Hoje usam default BR.

### 5.2 Mecanismo
- [ ] **Recompensa coletiva** (Mussler-Macy 1997) como salvaguarda anti-
  erosão Coleman. Tensiona com `f_W(k)` da R20 (por posição). Modelar
  como opt-in.
- [ ] **Equilíbrio bayesiano-perfeito** (Myerson 1991) ainda como
  conjectura para Proposição 2 sob heterogeneidade. Esboço de prova
  com `jogo_global.py` já existe — falta formalização.
- [ ] **Análise adversarial coordenada**: o cenário
  `uso_adversarial_oportunista` (R24) considera oportunistas
  individuais; falta varrer "20% da firma é oportunista coordenado".

### 5.3 Pendências institucionais
- [ ] **Verbatim DOU** dos dispositivos centrais (Art. 4º II/III, Lei
  9.784 Art. 24, Res. 21/2018 Art. 12) em `src/waas_antitrust/normas/`
  está parcialmente implementado. Completar parser e cobrir
  Lei 13.608/2018 + Lei 13.964/2019.
- [ ] **Doutrina sobre Art. 4º II/III** — só duas referências
  doutrinárias citadas; expandir com Forgioni, Salomão Filho,
  Ferraz Junior.
- [ ] **DOI Zenodo** — release stub no `.zenodo.json` mas sem release
  formal. Bloqueia citação acadêmica externa.

## 6 · Distribuição e governança

- [ ] **CITATION.cff** existe mas não foi testado contra GitHub's
  citation widget. Verificar.
- [ ] **README.md** ainda tem hero "for-the-badge" estilo software
  comercial. Considerar variante mais acadêmica (logo + autor +
  abstract de 3 linhas).
- [ ] **Licença CC BY-SA 4.0** cobre código e docs. Paper precisa de
  licença CC BY 4.0 separada? Verificar com Zenodo.

---

## 7 · Convergências da simulação por personas (jun/2026)

A [revisão por personas](revisao_personas.md) flagra três pontos
convergentes entre 3+ perfis profissionais — gravidade média, ainda
abertos:

- **§7.1 Autoria visível no site (jornalista, acadêmica).** Identificação
  só por "L." no byline é obstáculo prático para citação. Página
  `/sobre` ou rodapé do hero deveria expor autor + vinculação +
  contato (sem depender do leitor abrir o CITATION.cff).
- **§7.2 Sensibilidade do `β` do bem-estar (economista, acadêmica).**
  $W = -(\text{dano} + \beta \cdot FP)$ com $\beta$ provisório.
  Adicionar varredura unidimensional de $\beta$ análoga à de
  `alpha_erosao` (`scripts/varredura_alpha_erosao.py`).
- **§7.3 Página `/operacional` (conselheiro CADE, compliance Big Tech).**
  Gap entre "modelo formal" e "operação institucional amanhã":
  cláusulas contratuais defensivas afetadas, compatibilidade
  dosimétrica Art. 45, fluxo de Resolução nova vs Res. 21/2018 atual,
  papel da CGAA. Hoje `procedimento_cade.md` é leitura formal, não
  operacional.

---

**Conexão com decisões:** este documento sintetiza pontos identificados
em revisão de tom (jun/2026). Itens com gravidade `alta` ou `média`
viram entradas no [`DECISIONS.md`](DECISIONS.md) quando engajados.
