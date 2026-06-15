# Terminologia canônica

Esta página unifica o vocabulário do projeto. Termos que aparecem com
frequência em múltiplas páginas (Atos, Anexos, código) são listados
aqui em sua **forma canônica**, com sinônimos aceitos e proibidos.

A unidade terminológica é importante porque o projeto atravessou três
reformulações conceituais (v1 LCMC → v2 capital social Coleman → v3
information escrow Ayres-Unkovic). Em cada rodada, novos termos
entraram, e alguns antigos ganharam sentido secundário. Esta página
evita que o leitor curioso encontre três palavras para a mesma coisa
sem saber qual é a "oficial".

## Termos centrais do mecanismo

### Canal de depósito condicional (forma canônica)

- **Termo canônico em português**: *canal de depósito condicional
  operado pelo CADE*
- **Precedente teórico em inglês**: *information escrow*
  (Ayres & Unkovic 2012, *Michigan Law Review* 111:145)
- **Análogo prático**: *Callisto* ([callisto.org](https://www.callisto.org)) — plataforma de denúncia
  condicional de assédio sexual em campus universitário
- **Metáfora pedagógica**: *Kickstarter all-or-nothing* (pledge só
  cobra se a meta de apoiadores é atingida)
- **Sinônimos aceitos**: "canal", "escrow do CADE",
  "depósito condicional"
- **Sinônimo não recomendado**: "atenuante condicional" (carrega o
  framing v1 errado — a condição está no *canal de recepção*, não no
  *atenuante regulatório*)
- **Parâmetros no código**: `usar_escrow_explicito: bool` (ativa o
  caminho v3 do canal explícito; default `False` preserva o caminho
  histórico); `janela_escrow_tiques: int` (Δt da definição LCMC — quantos
  tiques um depósito permanece no escrow antes de expirar; default `0` =
  escrow eterno, leitura Callisto)

### LCMC (sigla)

- **Forma canônica**: *Leniência Condicionada à Massa Crítica*
- **Expandida sob v3**: *Leniência via canal de depósito condicional
  operado pelo CADE com gatilho de massa crítica intra-firma*
- **Não é**: "Leniência Coletiva" (genérico), "Leniência Compartilhada"
  (incorreto), "Leniência Cooperativa" (ambíguo)
- **Crase obrigatória**: "Condicionada **à** Massa Crítica" — não "a"

### WaaS (sigla)

- **Forma canônica em português**: *Whistleblower-as-a-Service*
  (preserva-se o anglicismo porque é a sigla técnica do paper)
- **Em pt-BR contextual**: *recompensa via TCC* (quando se fala do
  instrumento)
- **Status no reframe v3**: WaaS é **um instrumento incremental**
  dentre cinco; não é o mecanismo central. Confundir LCMC com WaaS
  é o erro editorial mais comum do projeto pré-v3.

## Termos do mecanismo de coordenação

### Massa crítica interna

- **Significado canônico**: fração `q_min` × `n_trabalhadores` de
  depósitos compatíveis dentro de janela `Δt`
- **Quem decide a massa crítica?** O **CADE** verifica, no canal de
  depósito condicional. **Não** é a firma que decide receber
  cooperação.
- **Parâmetro no código**: `q_min_cooperacao_interna` em
  `WaaSParametros` (default `0.10` = 10% dos trabalhadores)

### Depósito condicional

- **Significado canônico**: ato do trabalhador entregar ao CADE sua
  denúncia com cláusula de abertura: "esta denúncia só é instaurada
  se ≥ `q_min · n` outros depósitos compatíveis ocorrerem em `Δt`".
- **Não é**: "denúncia anônima" (anonimato é compatível mas não
  define); "denúncia coletiva" (a coletividade é resultado, não pré-
  requisito).

### Abertura simultânea

- **Significado canônico**: quando o gatilho de massa crítica é
  atingido, **todas as denúncias depositadas no escrow se abrem ao
  mesmo tempo**, eliminando "ninguém quer ser o primeiro".
- **Sob v1-v2**: "notificação da firma" — terminologia abandonada sob
  v3 porque concentrava a leitura no lado da firma; o canal abre
  *para o CADE*, e a firma é notificada como consequência.

### Sinergia entre autoridades internacionais (R30)

- **Significado canônico**: adoção COORDENADA da LCMC por múltiplas
  autoridades antitruste, operando como **mecanismo único distribuído**.
  Duas alavancas: (i) consolidação cross-jurisdicional do escrow via
  grupos econômicos (paralelo MoU bilateral); (ii) amplificação Schelling
  internacional (paralelo ICN/OECD).
- **Sinônimos aceitos**: "LCMC global", "LCMC inter-autoridades",
  "canal distribuído".
- **Parâmetros no código**: `grupos_economicos: tuple | None = None`,
  `usar_escrow_consolidado_grupo: bool = False`,
  `coordenacao_internacional: float = 0.0`.
- **Cenários canônicos**: `lcmc_global_coordenada` (sinergia ligada);
  `lcmc_global_descoordenada` (contrafactual, cada autoridade isolada).
- **Reporters**: `n_aberturas_consolidadas_grupo_acum`,
  `n_boosts_coordenacao_intl_acum`.

### Janela de adesão pós-abertura (R29)

- **Significado canônico**: janela de `janela_adesao_pos_abertura`
  tiques (default 10) que se abre quando uma firma atinge massa
  crítica e o escrow é aberto. Durante a janela, trabalhadores da
  mesma firma que ainda não cooperaram podem **aderir à classe dos
  lenientes** e receber **desconto progressivo por ordem de chegada**
  (`descontos_faixas_adesao`, default faixas 100/70/50/30/10%).
- **Sinônimos aceitos**: "janela de cascata pós-coordenação",
  "fila pós-abertura", "classes de leniência por adesão".
- **Análogo**: fila clássica do Art. 86 da Lei nº 12.529/2011
  (Spagnolo 2004 *J. Eur. Econ. Assoc.* 2(1)) operada **dentro** da
  firma já aberta, em vez de entre firmas cúmplices.
- **Parâmetros no código**: `janela_adesao_pos_abertura: int = 0`
  (opt-in estrito), `descontos_faixas_adesao: tuple = (1.0, 0.7, 0.5, 0.3, 0.1)`.
- **Cenário canônico**: `cascata_adesao_progressiva`.
- **Reporters**: `n_aderentes_pos_abertura_acum`,
  `n_blocos_em_janela_adesao_acum` no DataFrame de saída.

## Termos do bem coletivo (lentes analíticas secundárias)

### Capital social organizacional (Coleman 1990)

- **Status sob v3**: *moldura analítica secundária* para examinar
  fragilidade de erosão endógena (R26). **Não é** o mecanismo.
- **Significado**: bem coletivo produzido como subproduto de relações
  de obrigação intra-firma (Coleman, *Foundations of Social Theory*,
  cap. 12).
- **Aplicação ao projeto**: motiva a Proposição 5 candidata (existe
  $\alpha_\text{erosão}^\star$ tal que o regime colapsa). Falsificável
  via parâmetro `alpha_erosao` no modelo.

### Bem quase-público (Samuelson 1954)

- **Status sob v3**: *moldura analítica secundária* — ponte didática
  para leitor com background em economia clássica. **Não é** o
  mecanismo.
- **Por que persiste no site**: ajuda a explicar por que cooperação
  interna é difícil de internalizar via mercados (não-excluível
  parcialmente, não-rival entre autoridades). Mas a estrutura
  *operacional* do mecanismo é information escrow, não
  bem-quase-público.

### Anti-commons (Heller 1998)

- **Status sob v3**: *moldura analítica secundária* para o vetor de
  quebra "sobre-denúncia frívola" (tragédia reversa).
- **Aplicação ao projeto**: motiva o arquétipo `oportunista` (R24).

## Termos institucionais brasileiros

### Sub-regimes Cₜ / Cᵩ / Cₚ

- **Cₜ trabalhista** — Art. 22 I CF (lei ordinária comum). Hospeda
  vesting Hirschman.
- **Cᵩ tributária-LC** — Art. 146 + Art. 150 §6º CF + LRF Art. 14
  (lei complementar). Hospeda crédito tributário (R22).
- **Cₚ penal estrita** — Art. 5º XXXIX CF (lei penal). Hospeda
  leniência criminal individual (R23).
- **Como ler em sequência**: `Cₜ ⊂ Cᵩ ⊂ Cₚ` em ordem crescente de
  reserva constitucional. Cada sub-regime habilita um instrumento
  incremental adicional.

### Vetores de quebra

- **Vetor A**: $D_\text{base} \ge D_\text{total}$ — TCC clássico já
  dá o desconto. Parâmetro: `D_disc_base_tcc`.
- **Vetor B**: $p_\text{anulação} = 1$ — Judiciário anula TCC-WaaS
  (falsificador F6). Parâmetro: `p_anulacao_tcc`.
- **Vetor C**: custo legal alto — denunciante racional desiste.
  Parâmetro: `custo_legal_uw`.
- **Vetor D (LCMC)**: nenhuma firma atinge `q_min` na janela.
- **Vetor D (R18)**: firma assina TCC e descumpre. Parâmetro:
  `p_descumprimento_tcc`.
- **Vetor E (R26 Coleman)**: `alpha_erosao` alto — substrato
  cooperativo seca.

## Vocabulário CLAUDE.md (reforço)

Sigla `[V]` = vocabulário canônico definido em
[`CLAUDE.md`](https://github.com/freirelucas/waas-antitrust/blob/main/CLAUDE.md):

- *denunciante interno* `[V]` — não *whistleblower*
- *recompensa* `[V]` — não *bounty*
- *conformidade* `[V]` — não *compliance* (exceto jurídico BR)
- *cenários adversariais* / *análise de resistência* `[V]` — não
  *stress tests*
- *varredura* `[V]` — não *sweep*
- *reamostragem* (bootstrap) `[V]`
- *pequeno-mundo* `[V]` — não *small-world*
- *contágio complexo* `[V]` (Centola-Macy)
- *jogo global* `[V]` (Morris-Shin)
- *massa crítica* `[V]`
- *conhecimento comum* `[V]`
- *variedade requisitada* `[V]`

Anglicismos *toleráveis* (siglas técnicas): WaaS, ABM, IC, IR, ODD,
SOBOL, MCMC, NLP. **Toleráveis em contexto**: *information escrow*
(precedente Ayres-Unkovic, intraduzível sem perda); *all-or-nothing*
(em metáfora Kickstarter).

## Mapa de equivalência

Para o autor evitar inconsistências em edições futuras, esta tabela
mapeia cada conceito à sua forma canônica e às formas a evitar:

| Conceito | Canônico | Aceitável | Não use |
|---|---|---|---|
| O mecanismo central | canal de depósito condicional | escrow do CADE, depósito condicional | atenuante condicional |
| Quem opera o mecanismo | CADE | autoridade antitruste, regulador | "o sistema", "a plataforma" |
| O ato do trabalhador | depositar (denúncia condicional) | submeter, entregar | denunciar (sozinho) |
| O ato do canal | abrir simultaneamente | instaurar coletivamente | notificar a firma |
| O macroconceito | LCMC | Leniência Condicionada à Massa Crítica | Leniência Coletiva |
| O instrumento monetário | WaaS, recompensa via TCC | Whistleblower-as-a-Service | bounty, prêmio |
| O substrato cooperativo | capital social organizacional | (caveat) bem quase-público | (não use como mecanismo) |
| O risco de erosão | erosão endógena Coleman | chilling effect | morte do mecanismo |

## Onde ler mais

- [Aprendizados v3](aprendizados_v3.md) — memória institucional da
  correção radical (canal de depósito condicional).
- [Bem coletivo](bem_publico.md) — anexo conceitual, com Coleman/
  Samuelson como molduras secundárias.
- [Mecanismo](mecanismo.md) — Ato 2 com a estrutura em camadas
  (canal → coordenação → instrumentos → aritmética).
- [Análise institucional](INSTITUTIONAL.md) — fundamentos jurídicos
  do canal sob Art. 4º Lei 12.529 + Lei 9.784/99.
