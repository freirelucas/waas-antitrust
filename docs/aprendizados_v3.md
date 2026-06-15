# Reformulação radical — LCMC como canal de depósito condicional

Esta página registra a **correção estrutural** que o autor fez à
formulação da LCMC durante a sessão de fechamento, e serve como
roadmap para a revisão pesada que se segue.

## A correção, em uma frase

A formulação anterior dizia:

> "O atenuante regulatório (Art. 12 Res. 21/2018; analogia LAC Art. 7º
> VII-VIII) é concedido se e somente se a firma tiver recebido cooperação
> interna de ao menos uma fração `q_min`..."

Essa formulação **põe o gatilho no lado da firma e do CADE-julgador**: a
firma é a beneficiária, a massa crítica vira condição para o atenuante
regulatório. Está errada.

A formulação correta põe o gatilho num lugar completamente diferente:

!!! tip "LCMC — versão correta"

    O **CADE opera um canal de depósito condicional** de denúncias. O
    trabalhador entrega ao CADE uma denúncia com prova qualificada e
    uma **cláusula de abertura**: "esta denúncia só é instaurada se
    `≥ q_min · n` outros trabalhadores do mesmo setor/firma também
    depositarem denúncias compatíveis dentro de uma janela `Δt`". As
    denúncias ficam em *information escrow*. Quando o gatilho é
    atingido, **todas as denúncias se abrem simultaneamente** — e
    ninguém foi o primeiro isoladamente.

São dois mecanismos completamente distintos. O segundo é dramaticamente
melhor.

## Por que esta reformulação é radical

### 1. Resolve Olson direto no canal

A versão anterior precisava modelar free-riding e sub-iniciação como
fragilidades **a falsificar depois**. A versão correta **elimina
sub-iniciação por construção**: a denúncia individual nunca fica exposta
sozinha. Ou ela se acopla a outras e se abre coletivamente; ou
permanece em escrow. O problema Olson de "ninguém quer ser o primeiro"
é resolvido pela mecânica do canal.

### 2. Coleman vira caveat, não coração

R26 (erosão endógena por uso instrumental) foi construído assumindo
que o WaaS opera **sobre** o substrato de comunicação informal
intra-firma. Mas no mecanismo correto, o canal opera **fora** desse
substrato — o trabalhador deposita diretamente no CADE, anonimamente,
sem precisar conversar com colegas. O risco de chilling effect cai
dramaticamente. Coleman segue válido como caveat de pesquisa, mas não
é o núcleo da fragilidade. R26 fica reservado para o caso onde o
canal **publica taxas agregadas** de depósito (escrow-leakage) — um
sub-caso, não o caso geral.

### 3. Adv B fica resolvido sem mudança de lei

A versão anterior exigia construção dogmática nova ("atenuante por bem
público" / "interesse público em detecção"). Sob risco de F6 (anulação
judicial). A versão correta exige apenas **procedimento administrativo**:
o CADE pode regulamentar por Resolução **como recebe denúncias**
(Art. 4º, II e III da Lei 12.529, c/c Lei 9.784/99 Art. 5º e segs.).

Não cria categoria sancionatória nova; usa as existentes em sequência:
canal → instauração → procedimento administrativo → eventual TCC ou
condenação. O risco F6 cai materialmente porque o que está sob
controle judicial é o **procedimento de recepção**, não uma criação
de atenuante *ex novo*.

### 4. Os cinco instrumentos viram incrementos

Sob a reformulação correta:

- **WaaS (recompensa via TCC)**: incentivo financeiro à participação
  no canal. A firma paga via TCC quando o canal abre. **Incremental.**
- **Hirschman (vesting acelerado)**: ameaça crível à firma quando a
  massa crítica é atingida no canal. **Incremental.**
- **Crédito tributário**: financiamento estatal ao depositante.
  **Incremental.**
- **Leniência criminal individual**: imunidade ao partícipe que
  deposita. **Incremental.**
- **Sem instrumento monetário**: o canal **ainda funciona** — basta
  a coordenação acontecer. **Esse é o caso base; é elegante.**

O coração é o **information escrow**. Os instrumentos aumentam a
probabilidade de adesão, mas não são o mecanismo.

## A analogia conceitual correta

A analogia certa **não é** Olson + Coleman + Samuelson como categorias
primárias. É:

- **Information escrows** (Ayres & Unkovic, 2012, *Michigan Law Review*
  111:145) — depósito de informação revelada condicionalmente.
- **Callisto** (callisto.org) — plataforma real de denúncia condicional
  de assédio sexual em campus universitário. Identidade da vítima
  só é revelada ao mesmo agressor se duas ou mais denúncias coincidirem.
  **Paralelo direto** que faltava na narrativa antiga.
- **Mungan & Klick** (2014, 2016) — escrows em direito penal.
- **Kickstarter all-or-nothing** — metáfora simples: o pledge só
  cobra se a meta de apoiadores é atingida.

Olson e Coleman continuam relevantes como **lente analítica** (por que
o mecanismo é necessário; o que poderia dar errado), mas o **desenho
do mecanismo** é information escrow, não Ostrom-Coleman.

## Implicações para o desenho da norma

A norma proposta muda de natureza:

**Antes**: nova Resolução CADE complementar à 21/2018, criando categoria
nova de atenuante por contribuição a bem público / interesse de
detecção. Construção dogmática constitutiva, alta exposição a F6.

**Depois**: nova Resolução CADE regulamentando **procedimento de
recepção condicional** de denúncias qualificadas. Não cria atenuante
novo; estrutura *como o CADE recebe* informação que pode levar a
procedimento administrativo ordinário. Baixa exposição dogmática.

Os instrumentos monetários (WaaS, Hirschman, tributário, criminal)
continuam a exigir suas próprias bases legais — mas como **opcionais
e separáveis**, não como o coração do desenho. O canal pode existir
sem nenhum deles.

## O que muda no projeto (revisão a fazer)

| Onde | O que muda |
|---|---|
| `docs/index.md` (Ato 1) | Pergunta-tese refundida: "como o CADE pode receber denúncias coletivas sem expor ninguém individualmente?". Mecanismo central = canal de depósito condicional, não atenuante. |
| `docs/mecanismo.md` (Ato 2) | Reorganização das camadas: Camada 1 (canal escrow), Camada 2 (a coordenação resolvida), Camada 3 (instrumentos opcionais). |
| `docs/resultados.md` (Ato 3) | A queda de violadoras em B/C é resultado do **canal abrindo denúncias coletivas**, não da firma decidindo pagar. |
| `docs/limitacoes.md` (Ato 4) | R26 (erosão Coleman) recategorizado para sub-caso. Nova fragilidade central: **denúncias presas em escrow indefinidamente** (massa crítica que nunca se forma). |
| `docs/bem_publico.md` | Reescrita: Ayres-Unkovic + Callisto como precedentes principais. Capital social vira moldura analítica secundária. |
| `docs/INSTITUTIONAL.md` | Reescrita do § "Art. 12 como reconhecimento de bem público": substituir por procedimento de recepção (Art. 4º Lei 12.529 + Lei 9.784/99). |
| `docs/critica_x10_v2.md` | Status do Sociólogo v2 (Coleman): correção principal foi absorvida, mas o sinal mais forte ficou diferente — não é "Coleman > Samuelson", é "Ayres-Unkovic > qualquer leitura econômica clássica de bem público". |
| `src/waas_antitrust/model.py` | Phase P2 já existe (massa crítica como gatilho). Mas precisa migrar de "gatilho na firma" para "gatilho no canal CADE": o `AutoridadeAgent` (ou um novo `CanalAgent`) mantém um escrow de denúncias condicionais; abre coletivamente quando q_min·n é atingido. A firma é reagente. |
| `src/waas_antitrust/instrumentos.py` | Já está no caminho correto (taxonomia declarativa de 4 instrumentos). Adicionar 5º: **canal_deposito_condicional** como instrumento *básico/canal*, dos quais os outros 4 são acoplamentos opcionais. |
| `docs/DECISIONS.md` | Novo R27 — Canal de depósito condicional como mecanismo central. |
| `docs/REFERENCES.md` | Acrescentar Ayres-Unkovic 2012; Callisto (URL + documento técnico); Mungan-Klick. |

## Roadmap de execução

A revisão radical será feita em commits separados, cada um com gates
verdes + sync main:

1. **Este commit** — registro do entendimento corrigido em
   `aprendizados_v3.md`. Não toca código.
2. Reescrita do Ato 1 (`index.md`): canal de depósito condicional como
   mecanismo central.
3. Reescrita do Ato 2 (`mecanismo.md`): três camadas reorganizadas.
4. Atualização de `bem_publico.md`: Ayres-Unkovic + Callisto como
   precedentes principais.
5. Atualização de `INSTITUTIONAL.md`: procedimento administrativo via
   Art. 4º Lei 12.529 + Lei 9.784/99.
6. Ato 3/4/5: ajustes finos para alinhar narrativa.
7. `DECISIONS.md` R27 abre — mecanismo central operacionalizável em
   sub-rodada futura (não é refator de código nesta sessão).
8. `REFERENCES.md` ganha Ayres-Unkovic + Callisto.

O código do `WaaSModel` **não é refator estrutural nesta sessão**. A
Phase P2 atual continua válida em essência; o que muda é a **leitura
narrativa** do que ela representa. R27 fica aberto para refator futuro
quando o autor decidir migrar `AutoridadeAgent` → `CanalAgent` com
escrow explícito.

## A pergunta de confirmação do autor

> "Os outros aspectos é um incremento, o coração é criar a massa
> crítica, correto?"

**Sim, correto.** O coração é a criação da massa crítica via canal de
depósito condicional. WaaS, Hirschman, crédito tributário, leniência
criminal — todos são incrementos. Sem nenhum deles, o canal ainda
opera; com eles, opera com taxas de adesão maiores.

Esta página fica como referência canônica do entendimento corrigido.

## Pós-script (jun/2026) — R29 e R30

Após o fechamento desta página, duas extensões foram acopladas ao canal
de depósito condicional sem alterar o entendimento de fundo:

- **R29 — Janela de adesão pós-abertura com desconto progressivo por
  classe.** Quando uma firma atinge massa crítica e o escrow é aberto,
  abre-se uma janela de `janela_adesao_pos_abertura` tiques durante a
  qual trabalhadores da mesma firma que ainda não cooperaram podem
  aderir à classe dos lenientes e receber desconto progressivo por
  ordem de chegada. Espelha o Art. 86 da Lei 12.529/2011 (Spagnolo
  2004) operado dentro da firma já aberta. Detalhada na Camada 5 do
  [`mecanismo.md`](mecanismo.md).

- **R30 — Sinergia entre autoridades internacionais.** Modela "e se
  todas as autoridades adotassem LCMC ao mesmo tempo?" com duas
  alavancas: (i) consolidação cross-jurisdicional do escrow via grupos
  econômicos (paralelo MoU bilateral CADE-DOJ-ATR 2019, DG-COMP-CADE
  2009, ICN MoU 2001); (ii) coordenação internacional como
  amplificação do sinal Schelling erga omnes. Detalhada em
  [`internacional.md`](internacional.md).

Nenhuma das duas altera o coração — ambas são extensões do canal já
descrito. R29 estende o gradiente Saito *dentro* da firma aberta;
R30 estende a noção de "firma" para "grupo econômico" e o sinal
Schelling para o nível inter-jurisdicional.
