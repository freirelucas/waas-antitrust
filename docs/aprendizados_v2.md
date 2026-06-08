# Aprendizados consolidados — sessão de reframe v2

Esta página registra os **aprendizados estruturais** da longa sessão que
levou o projeto da formulação original ("WaaS = recompensar denúncia interna")
ao reframe v2 ("massa crítica como capital social organizacional; WaaS é um
instrumento entre cinco"). Serve como memória institucional para sessões
futuras: o que ficou consolidado, o que ainda está aberto, e que padrões
de processo merecem ser preservados.

## A cronologia dos commits

A sessão produziu **20 commits do reframe v2** (mais 4 do trabalho LCMC
imediatamente anterior), todos sincronizados em `main` com gates verdes.
Em ordem cronológica:

| # | Hash | Conteúdo |
|---|---|---|
| 1 | `5a51f72` | Crítica x10 v2 com 10 personas (8 originais + sociólogo + cientista político) |
| 2 | `1945cf3` | Reposicionamento conceitual: Coleman > Samuelson; LAC Art. 7º VII-VIII |
| 3 | `99665d4` | Mat A — limiar Saito por posição $x^\star_k$ + arquétipo oportunista (R24) |
| 4 | `93d0b44` | UX visual — chip-instrumento + grid 4-instrumentos |
| 5 | `340e6ce` | 6 cenários novos v2 (9 → 15 no catálogo) |
| 6 | `1d06131` | `viz/cascata.py` implementado + figura 04 |
| 7 | `659fc5d` | Externalidade erga omnes — `valor_dissuasao_difusa_acum` (v2.D.1) |
| 8 | `5d9a5e6` | R26 erosão endógena Coleman + `capital_social_residual` |
| 9 | `edaa81b` | `viz/erosao.py` — Proposição 5 candidata visualizada |
| 10 | `9aaffc9` | Ato 2 ganha § "cooperação interna como capital social" |
| 11 | `5a73bec` | `instrumentos.py` declarativo (4 instrumentos canônicos) |
| 12 | `8d9cd21` | `viz/painel_macro.py` — tela 2×2 macro |
| 13 | `44e1225` | `viz/painel_micro.py` — tela 2×2 intra-firma |
| 14 | `7e2be49` | Ato 3 sublinha-tese + CHANGELOG consolidado |
| 15 | `b31d1b6` | Glossário +11 entradas v2 + Ato 4 sublinha-tese |
| 16 | `e694e1f` | Ato 5 + Modelagem multiagente atualizados |
| 17 | `8e06d91` | **Reescrita editorial pesada do Ato 1 + Ato 2** (LCMC ≠ WaaS; transparência ao código) |
| 18 | `c9859c1` | Reescrita editorial do Ato 3 (DataFrame literal + reporters em 3 categorias) |
| 19 | `6509230` | Ato 4 + Ato 5 com falsificadores em código |
| 20 | `6d904b0` | Reescrita operacional do "Como usar" |

## Os três aprendizados teóricos que mais importam

### 1. LCMC ≠ WaaS

A formulação anterior conflate dois conceitos distintos:

- **LCMC** (Leniência Condicionada à Massa Crítica) é **princípio
  regulatório**: cooperação interna de massa crítica como condição
  necessária para o atenuante.
- **WaaS** é **um instrumento** que pode (ou não) ser usado para
  operacionalizar LCMC: a firma paga recompensa monetária ao
  denunciante.

A versão correta admite **cinco configurações distintas**:

| Configuração | LCMC? | Pagamento? |
|---|---|---|
| LCMC sem instrumento monetário | Sim | Não |
| LCMC + WaaS | Sim | Firma → trabalhador |
| LCMC + Hirschman (vesting acelerado) | Sim | Firma → trabalhador (via equity) |
| LCMC + crédito tributário | Sim | Estado → trabalhador (R22 stub) |
| LCMC + leniência criminal individual | Sim | Não (imunidade) |
| WaaS sem LCMC | Não | Sim (modelo histórico questionado) |

Esta distinção é central na nova narrativa do site (Ato 1, Ato 2,
`bem_publico.md`).

### 2. Coleman > Samuelson

A leitura econômica clássica de massa crítica como "bem quase-público
à Samuelson" (rivalidade × excluibilidade) é **categoria errada**.
O Sociólogo da x10 v2 trouxe a correção:

- A categoria correta é **capital social organizacional** (Coleman 1990,
  *Foundations of Social Theory*, cap. 12).
- Capital social é bem coletivo **produzido como subproduto** de
  relações de obrigação entre pessoas que se conhecem.
- **Coleman previu que capital social pode ser destruído pela própria
  instrumentalização**.

Esta previsão virou **Proposição 5 candidata**: existe $\alpha^\star$
tal que para $\alpha_\text{erosão} > \alpha^\star$, o Regime B colapsa
em A após N tiques. Operacionalizada no modelo via `alpha_erosao`
(R26); falsificável em `tests/test_erosao_coleman.py`.

### 3. Captura desloca-se do gatilho para o processamento

O Cientista Político v2 (estreia na x10) trouxe:

- WaaS pulveriza o gatilho de notificação (cada empregado vira
  *fire alarm*, McCubbins-Schwartz 1984).
- Mas concentra captura no **funil estreito de processamento** — RIG
  2024 mostra 180 servidores área-fim no CADE.
- Sem expansão de quadro, a seleção discricionária de quais notificações
  investigar vira o novo ponto ótimo de captura (Stigler 1971).

Cenário `captura_processamento_cade` modela isso (`taxa_capacidade=0.10`).

## Aprendizados técnicos

### Arquitetura: opt-in via flag

Todas as novidades v2 obedecem ao padrão **opt-in via parâmetro com
default conservador**:

- `modo_corrida: bool = False` — LCMC só ativa explicitamente
- `alpha_erosao: float = 0.0` — erosão Coleman desliga por default
- `peso_inequity_aversion: float = 0.0` — fairminded degenera em
  racional sem ativar
- `epsilon_dissuasao_difusa: float = 0.0` — externalidade não entra no
  bem-estar sem ativar
- `usar_x_estrela_no_racional: bool = False` — Morris-Shin no ABM
  só sob flag

Resultado: 234 → 288 testes (+54) sem **nenhuma quebra de regressão**.
A backward compat é estrita; configurações antigas continuam
produzindo bit-a-bit a mesma saída.

### Reporters em três categorias semânticas

Em `model.py`, os 31 reporters foram agrupados em três blocos:

- `_REPORTERS_MASSA_CRITICA` — substrato LCMC (n_sinais,
  n_empresas_notif, n_firmas_atingiram_massa_critica_interna,
  dano_acumulado, valor_dissuasao_difusa_acum, capital_social_residual)
- `_REPORTERS_INSTRUMENTOS` — uso dos instrumentos (n_tcc_assinados,
  n_pagou, custo_recompensa_acum, custo_exodo_acum, ...)
- `_REPORTERS_ROBUSTEZ` — vetores de quebra (n_tcc_anulados,
  n_firmas_optaram_tcc_classico, n_firmas_quebraram_tcc, ...)

Sob o reframe v2, a primeira categoria é o que importa para a tese
central; as outras são consequência e diagnóstico.

### Decomposição do Regime C em três sub-regimes

O Adv B v2 trouxe correção dogmática material: "exigir lei" não é
categoria homogênea no direito constitucional brasileiro. Cada
instrumento tem reserva distinta:

- **Cₜ trabalhista** (Art. 22 I CF, lei ordinária comum) — hospeda
  Hirschman.
- **Cᵩ tributária-LC** (Art. 146 + Art. 150 §6º + LRF Art. 14) — hospeda
  crédito tributário (R22).
- **Cₚ penal estrita** (Art. 5º XXXIX CF) — hospeda leniência criminal
  individual (R23).

A analogia ao IRS Whistleblower (26 U.S.C. §7623) é **inaplicável** —
IRS opera sob federal taxing power exclusivo, sem reserva penal.

### Saito (2021) calibra duas escalas, não uma

O gradiente Saito de 349 TCCs CADE 2012-2019 (1ª=43,43%; 2ª=34,51%;
3ª=20,22%) é usado em duas escalas distintas:

- **Inter-firma**: `decaimento_D(posicao_firma)` em `corrida.py`
- **Intra-firma**: `decaimento_W(posicao_trabalhador) = W_base ·
  D_Saito(k)/D_Saito(1)`

Mat A v2 generalizou para limiar Morris-Shin **por posição**:
`limiar_switching_por_posicao(b, c, k_rel, posicao_trabalhador)`. A
oferta do bem coletivo é **escalonada**, não monolítica.

### Caveat formal Frankel-Morris-Pauzner / Angeletos-Hellwig-Pavan

A unicidade Morris-Shin clássica supõe **jogo estático**. Sob LCMC, a
fila inter-firma é sinal público correlacionado — Angeletos-Hellwig-
Pavan (2007) mostraram que isso pode restaurar multiplicidade. A
Proposição 2 reformulada "sequência $\{x^\star(t)\}$ decrescente é
única em cada instante" requer condições adicionais que **não são
satisfeitas no caso geral**. Tratamos como conjectura aberta.

## Aprendizados editoriais

### Empilhar tipograficamente, não substituir

O Designer v2 fez correção fundamental: manter a **punchline jornalística**
no H1 e adicionar **sublinha-tese acadêmica** em itálico cinza abaixo. Os
dois leitores (cético jornalístico e leitor analítico) continuam
servidos.

Implementado em `docs/stylesheets/extra.css`:

```css
.sublinha-tese {
  font-style: italic;
  color: #5d6d7e;
  margin-top: -0.4em;
  border-left: 3px solid #cfd8dc;
  padding-left: 0.6em;
}
```

### Transparência ao código nos 5 Atos

O reframe editorial inicial colocou as ideias certas (Coleman, LCMC,
instrumentos) mas **não mostrava código nenhum**. A reescrita pesada
dos commits 17-20 corrigiu:

- **Ato 1**: 3 comandos bash + bloco Python com `WaaSModel.executar()`
- **Ato 2**: 4 blocos de código em 3 camadas (LCMC, instrumentos, IC-F\*)
- **Ato 3**: DataFrame literal (tiques 36-40 lado a lado) + reporters
  em 3 categorias + `calcular_bem_estar` + multi-seed CI + 6 vetores
  de quebra com receita Python cada
- **Ato 4**: tabela 9 limitações × parâmetro × como rodar; 3 receitas
  Python concretas
- **Ato 5**: 3 "receitas concretas de contestação" em ≤ 10 linhas cada

A vantagem: **toda alegação textual está ligada a um caminho de
reprodução**. Cético tem caminho direto para falsificar.

### Bug visual: alt-text não aceita markdown

`![texto](img.png){ .classe }` quebra se o `texto` contiver bold ou
asterisco. A sintaxe attr_list não casa, e `{ .classe }` aparece
literal embaixo da figura. Solução:

```markdown
<figure markdown>
  ![alt curto](img.png){ .figura-empirica }
  <figcaption>caption longa com **bold** funciona aqui</figcaption>
</figure>
```

Requer extensão `md_in_html` no `mkdocs.yml`.

### `!!! tip` (admonition) para princípios destacados

Princípios centrais (como o enunciado do LCMC) ganham destaque visual
através do `admonition`:

```markdown
!!! tip "Princípio LCMC"

    O atenuante regulatório é concedido **se e somente se** ...
```

Cria caixa verde com título destacado. Material for MkDocs renderiza
nativamente.

## Aprendizados de processo

### x10 v1 → x10 v2

O padrão x10 (8 personas em paralelo + síntese de convergências) é
útil quando o projeto tem complexidade suficiente para sustentar
múltiplas lentes. A x10 v2 acrescentou duas personas críticas
(sociólogo, cientista político) e trouxe **três sinais mais fortes
estruturais** que mudaram o projeto:

1. Coleman > Samuelson (categoria conceitual)
2. Captura no processamento (RIG 2024)
3. Fechar antes de abrir (R09-R11 antes do reframe)

A v3 sugerida pelo PM (behavioral ethicist + econometrista) fica fora
do escopo desta sessão.

### Commit séries curtas + main sempre sincronizada

Padrão aplicado em todos os 20 commits da sessão:

1. Cada commit é **pequeno e tematizado** (≤ 200 linhas tipicamente).
2. **Gates verdes** sempre (pytest + ruff + black + mkdocs --strict).
3. **Sync 4-way imediato** após cada commit: HEAD =
   `claude/happy-clarke-eseuu` = origin = main local = origin/main.
4. **Mensagem de commit detalhada** com seções: O que mudou; Por quê;
   Verificação; Postura epistêmica.

Resultado: a história do projeto é legível commit a commit; rollback
é cirúrgico se necessário.

### Background research + main work em paralelo

Em uma das etapas, lancei pesquisa profunda (VC contratos, killer
acquisitions como jogo, condutas × job descriptions, traços
comportamentais) em background **enquanto** fazia trabalho de docs no
main. A pesquisa retornou conteúdo útil que alimentou o R24
(oportunista) e ficou disponível para referência futura sem bloquear.

## O que segue em aberto

### R-items abertos pós-sessão

- **R09 (Eco A v1)** — endogeneizar `g_i(t) = π·R/(p·S)` à la Becker.
  Altera Prop. 3.
- **R10 (Eco A v1, agravado v2)** — IC-F\* completa como **matriz**
  condicionada a instrumento e posição na fila. Altera Prop. 1.
- **R11 (Eco A v1)** — Hirschman como elevação de `W_esperado` em vez
  de subtração de `g_i_efetivo`.
- **R21** — Operacionalizar bem coletivo: 3 testes empíricos (não-
  rivalidade, excluibilidade, externalidade).
- **R22** — Crédito tributário implementado de fato (não stub).
  Pendência D08 (estimativa LRF).
- **R23** — Leniência criminal individual: análise dogmática colisão
  Art. 86 + Lei 8.137. Decisão do autor.
- **R24** — Free-riding e tragédia reversa: arquétipo `oportunista`
  está em primeira aproximação; falta calibração contra Dyck-Morse-
  Zingales 2010 e elaboração com Big Five / Dark Triad.
- **R25** — Jurisdição concorrente (CADE × MPF × MPT × CGU) como
  módulo de fato (não só cenário).
- **R26** — Erosão endógena por uso: Proposição 5 candidata. Calibração
  formal de `alpha_erosao*` contra dados empíricos (Titmuss, Frey-Jegen,
  Bénabou-Tirole).

### Fora do escopo desta sessão (Fase 4)

- Refator estrutural completo do P3 (FirmaIncentivoDecision como
  classe).
- Paper `main.tex` reescrito (escopo restrito a alterações narrativas).
- Crítica x10 v3 com behavioral ethicist + econometrista aplicado.
- Implementação real de R22 e R23 (saem do estado stub).
- VC investidor como agente próprio (`InvestidorVCAgent`).
- Killer acquisitions como jogo estratégico em vez de conduta.

### Pesquisas externas pendentes (pendentes em R03)

- Mediana de desconto em TCCs CADE 2020-2025 (estender Saito 2021).
- Número de funcionários em subsidiárias brasileiras de big tech
  (RAIS/CAGED via MTE).
- Custos legais médios em ações trabalhistas + representações ao CADE.
- Verbatim do Art. 12 da Resolução 21/2018 contra DOU (E04 segue
  aberto).

## Recomendações para sessões futuras

1. **Fechar R09, R10 ou R11** antes de qualquer reframe v3. O PM v2 foi
   explícito: "feche 1 decisão normativa pendente antes de abrir nova
   camada interpretativa".
2. **Preservar opt-in via flag** para qualquer extensão. A backward
   compat estrita é o que permite a coexistência de paradigmas.
3. **Empilhar tipograficamente** continua sendo a regra editorial: não
   substituir punchline jornalística por reframe acadêmico.
4. **Toda alegação textual ligada a caminho de reprodução em código**.
   A transparência é o principal ativo editorial do projeto.
5. **Caveats formais explícitos** quando matemática herda condições
   (Frankel-Morris-Pauzner / Angeletos-Hellwig-Pavan para Morris-Shin
   dinâmico).
6. **Coleman > Samuelson** deve ser preservado como leitura primária.
   Samuelson permanece como ponte didática.

## Estatística final

- **Commits** desta sessão (reframe v2): 20
- **Testes pytest**: 234 → 288 (+54)
- **Cenários canônicos**: 9 → 15
- **Arquétipos**: 5 → 6 (+ oportunista)
- **Módulos novos em `src/`**: 5 (`instrumentos.py`, `viz/{cascata,
  erosao, painel_macro, painel_micro}.py`)
- **Páginas docs novas**: 4 (`bem_publico.md`, `viabilidade_regime_c.md`,
  `critica_x10_v2.md`, `aprendizados_v2.md` — esta página)
- **Referências bibliográficas novas**: 16 (Olson, Ostrom, Coleman,
  Hardin, Heller, Samuelson, Titmuss, Frey-Jegen, Bénabou-Tirole,
  Stigler, Wilson, McCubbins-Schwartz, Carpenter-Moss, Frankel-
  Morris-Pauzner, Angeletos-Hellwig-Pavan, Chwe)
- **R-items abertos**: R21-R26 (6 novos) + R09-R11 (3 herdados v1)

**Goal invariante mantido em todos os 20 commits**: pytest + ruff +
black + mkdocs --strict verdes; main sincronizada 4-way após cada
commit.
