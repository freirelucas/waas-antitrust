# Implicações para compliance corporativo

Página para a persona **compliance corporativo** (A2/B3 da auditoria UX): se a LCMC
for adotada no Brasil — pela Resolução CADE complementar à 21/2018 (Regime B) ou
por extensão da Lei 13.608/2018 (Regime C) — o que muda na conformidade da empresa.

!!! danger "Leitura especulativa, não-aconselhamento"
    Este apêndice é **leitura especulativa** sob a hipótese de adoção do mecanismo.
    Não constitui aconselhamento jurídico, parecer técnico, ou recomendação de
    governança. O autor não é advogado da empresa do leitor; o autor não tem
    relação contratual com nenhuma firma; o autor mantém o repositório
    independentemente de qualquer think tank, escritório ou consultoria. Use por
    sua conta e risco; consulte aconselhamento jurídico próprio.

---

## Em uma frase

Sob LCMC adotada, o vetor de risco antitruste de uma firma com **conduta
unilateral potencial** em mercado digital deixa de depender de **detecção
externa** (ação de oficio do CADE, denúncia de concorrente) e passa a depender de
**resistência interna ao depósito condicional** — uma função do número e do papel
funcional dos trabalhadores que observam a conduta, não da capacidade
investigativa da autoridade.

A consequência operacional: a função de compliance migra de **filtrar comunicação
externa** (M&A, mídia, autoridade) para **gerir o ambiente interno de informação**
sob condições de assimetria reversa — a firma sabe quem **pode** depositar, mas não
quem **depositou**, até que a massa crítica dispare.

---

## Quatro vetores corporativos materiais

### 1. Contratos de trabalho e cláusulas de confidencialidade

**Hoje**: cláusulas amplas de confidencialidade ("informação sobre o negócio") podem
operar como dissuasor de depósito condicional, mas sob a LCMC com base autônoma no
Art. 4º Lei 12.529 + Lei 9.784/99, o depósito ao CADE não constitui violação
trabalhista — é exercício de canal administrativo formal. Cláusulas que tentem
inviabilizar o depósito são **nulas por objeto**.

**Sob LCMC adotada**: cláusulas de confidencialidade precisam carve-out explícito
para "comunicação a autoridade competente" — bom para a empresa do ponto de vista
de litígio (evita arguição posterior de "cláusula nula"); ruim para o efeito
dissuasor original. Empresas estrangeiras já operam sob esse padrão por força do
Dodd-Frank §922 (SEC) e da Diretiva 2019/1937 (UE) — o ponto cego brasileiro é
recente.

### 2. Cláusulas de vesting e desligamento

**Hoje**: cláusulas de "aceleração de vesting por desligamento sem causa" são
comuns em empresas com equity-based comp; "aceleração por gatilho coletivo"
(`fracao_contratos_acelerados` no modelo) **não existe** no padrão brasileiro —
exigiria lei nova (Art. 22 I CF, reserva ordinária comum federal trabalhista).

**Sob Regime C com Hirschman implementado**: a cláusula vira **padrão de mercado**
para empresas em mercados regulados pelo CADE. Implicação corporativa: revisão
das fórmulas de cap table, modelagem de cenário de "êxodo coletivo gatilhado"
(`peso_hirschman` no modelo dá a magnitude esperada), provisionamento contábil
em FAS 718/IFRS 2 sob novo padrão.

### 3. Programas de integridade (Lei 12.846/2013, LAC Art. 7º VII-VIII)

**Hoje**: programas de integridade são **atenuante na dosimetria** sob a LAC,
incluindo "canais internos de denúncia". A LCMC propõe um canal **externo**
(operado pelo CADE), não interno.

**Sob LCMC adotada**: surge tensão entre dois canais — o interno (LAC) e o externo
(LCMC). A empresa precisa decidir se o canal interno se torna **redundante** ou
se se torna **preferencial** para o trabalhador (proteção menor, mas resolução
mais rápida e sem expor a empresa ao CADE). Decisão econômica: incentivar o
canal interno via prêmio retrospectivo ao denunciante? Tornar o canal interno
inútil para não cooptar com o LCMC? Não há resposta única; depende do apetite
ao risco antitruste vs reputacional.

### 4. Diligência em M&A e estruturação de operações

**Hoje**: due diligence antitruste em M&A foca em (i) sobreposição horizontal, (ii)
fechamento vertical, (iii) histórico de prática anticompetitiva da target. Conduta
unilateral em curso é detectada via revisão documental e entrevistas — sob risco de
ocultação.

**Sob LCMC adotada**: surge um novo vetor de diligência — o **escrow latente**.
Trabalhadores da target podem ter depositado denúncias condicionais que ainda não
dispararam por insuficiência de co-depositantes. Uma transação que altera o número de
trabalhadores (downsizing, integração) pode **disparar** a massa crítica
post-closing, expondo o comprador a procedimento antitruste herdado. Implicação:
representations & warranties precisam de cobertura específica ("a target não tem
depósitos condicionais pendentes do conhecimento da administração"), embora a
verificação seja impossível pelo desenho (sigilo do escrow).

---

## Cinco perguntas que o comitê de auditoria precisa responder antes da adoção

Não são perguntas ao autor; são perguntas que o autor sugere que sejam levantadas
internamente, com aconselhamento jurídico próprio:

1. **Política de aceleração de vesting**: existe cláusula contratual padrão de
   aceleração por gatilho coletivo? Se não, é viável adotá-la sob Regime C
   sem prejuízo do equity dos sócios fundadores?
2. **Canal interno de denúncia**: o canal interno atual da empresa cobre conduta
   antitruste especificamente, ou apenas fraude/corrupção sob a LAC? Há
   incentivo retrospectivo ao depositante? Existe linha direta da função
   compliance ao CEO sem intermediação?
3. **Mapeamento de papéis sensíveis**: quem na empresa, por papel funcional, tem
   acesso a informação que viabilizaria denúncia condicional? Esses funcionários
   estão sob contratos que comportam carve-out para "comunicação a autoridade
   competente"?
4. **Provisão para passivo antitruste**: o modelo financeiro provisiona para
   passivo antitruste? Sob qual cenário-base (probabilidade de detecção)? Como
   essa provisão se altera sob a hipótese de LCMC adotada?
5. **R&W em transações em curso**: M&A em discussão ou closing programado cobre
   "ausência de depósito condicional pendente"? Como o seller representa algo que
   por desenho não pode conhecer?

---

## Posição honesta do autor

O autor **não recomenda** que a empresa do leitor altere sua estratégia de
compliance hoje, antes de qualquer movimento institucional brasileiro concreto.
Adoção de LCMC sob Regime B exige Resolução complementar do CADE (não anunciada
nem em consulta pública); adoção sob Regime C exige projeto de lei (não
tramitando). A aposta substantiva do projeto é que **a via B é viável e
provavelmente é o caminho** se houver vontade institucional — mas esta é tese
acadêmica, não previsão.

O que o autor recomenda: que o leitor que se interessa por esta página leia também
[`limitacoes.md`](limitacoes.md) (onde os 5 vetores de quebra do modelo estão
nomeados) e [`transparencia.md`](transparencia.md) (onde os achados negativos
estão listados, incluindo a forma forte da Proposição 5 que foi **falsificada**
pela varredura multi-seed). Quando uma proposição candidata é refutada
explicitamente, o leitor sabe que o autor não esconde resultado adverso —
isso vale mais que qualquer afirmação positiva.

---

## Disclaimer adicional

- Conteúdo desta página: **especulação estruturada**, não consultoria.
- O autor **não tem relação contratual** com nenhuma empresa em mercado regulado
  pelo CADE.
- O autor **não tem agenda corporativa** declarada nem oculta.
- Comentários, correções e críticas são bem-vindas via
  [GitHub Issues](https://github.com/freirelucas/waas-antitrust/issues).
