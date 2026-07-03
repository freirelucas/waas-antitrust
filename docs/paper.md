# Leniency Conditional on Critical Mass: A Conditional-Deposit Channel for Unilateral Conduct in Digital Markets

<p class="deck">Versão web navegável do rascunho acadêmico. O PDF compilado a partir de <code>paper/main.tex</code> é o documento canônico para arbitragem; esta página apresenta o mesmo material na ordem do paper, preservando a estrutura argumentativa para revisão por pares.</p>

<p class="byline"><em>Paper</em> · rascunho v0.2.0 · jun/2026 · não citar como definitivo</p>

<p class="lede">Esta página acompanha <code>paper/main.tex</code> no repositório. A versão atual tem as dez seções escritas e coerentes entre si; o texto segue sujeito a revisão até o congelamento da versão de submissão, mas nenhuma seção está incompleta. O DOI Zenodo será emitido nesse congelamento (ver <a href="sobre/">Sobre</a> para a forma canônica provisória de citação). Para a leitura em cinco Atos no formato site (mais didática, com figuras embarcadas), começar pelo <a href="index/">Ato 1</a>.</p>

## Sumário

| § | Seção | Substância |
|---|---|---|
| 1 | Introdução | Problema, intuição central, posicionamento na literatura |
| 2 | Falha estrutural da leniência clássica em mercados digitais | Por que cartel-style não opera em conduta unilateral |
| 3 | Blocos construtivos | Spagnolo, Aubert-Rey-Kovacic, Dodd-Frank §922 |
| 4 | Análise comparada | SEC, DOJ-ATR, DMA Tool, Diretiva 2019/1937, CADE |
| 5 | O mecanismo LCMC | Canal + cinco fases P1-P4 + base normativa BR |
| 6 | Modelo baseado em agentes | 3 classes de agente, calibração formal |
| 7 | Enquadramento cibernético | Ashby, variedade requisitada |
| 8 | Pré-condição sociológica | Olson, Google Walkout, Haugen, NLRB |
| 9 | Tradução política para o Brasil | Regimes B vs C, coordenação CADE-CGU-MPF |
| 10 | Conclusão | Cinco resultados, três frentes de pesquisa futura |

---

## 1. Introdução

Programas de leniência transformaram o enforcement antitruste ao oferecer
imunidade ao primeiro membro de um cartel que coopera com a autoridade
(Spagnolo 2004; Harrington-Chang 2015). Sua eficácia, porém, pressupõe um
**cartel** — conduta coordenada entre concorrentes cuja instabilidade interna
a leniência explora. Em mercados digitais, parte central das condutas
potencialmente anticompetitivas é **unilateral**: autopreferência, venda
casada, recusa de acesso (Crémer-de Montjoye-Schweitzer 2019). Não há
co-conspirador externo a quem oferecer imunidade.

O núcleo do desenho proposto não é a recompensa: é o **canal de depósito
condicional** operado pela autoridade. Um trabalhador isolado não se
identifica antes de saber se outros se identificarão — problema clássico de
ação coletiva (Olson 1965; Granovetter 1978). O canal resolve isso
institucionalizando *information escrow* (Ayres & Unkovic 2012): o depósito
permanece selado até que massa crítica $q_{\min}\cdot n$ se concretize sobre
a mesma firma, e só então as identidades e provas são abertas
simultaneamente. O análogo prático direto é a plataforma Callisto, em
operação nos EUA desde 2015 para denúncias condicionais de assédio em
campus.

A aritmética da IC-F\* (condição de pagamento da firma) emerge **apenas
quando** instrumento de internalização é acoplado ao canal. Sob o
acoplamento recompensa-via-TCC, a firma maximiza a margem $D - W$, onde $D$
é o desconto sobre a contribuição pecuniária do Termo de Compromisso de
Cessação e $W$ é a recompensa total paga aos denunciantes internos. Quando
$D > W$, a firma tem incentivo a financiar a revelação. Os demais
acoplamentos (Hirschman, crédito tributário, leniência criminal individual)
atuam sobre regimes constitucionais distintos.

A IC-F\* é satisfazível *de lege lata* sob a Resolução CADE n.º 21/2018
(Regime B), permitindo implementação por via infralegal. O Regime C
(extensão da Lei n.º 13.608/2018, com a redação da Lei n.º 13.964/2019) é juridicamente mais robusto mas exige
Congresso. O canal em si tem base autônoma no Art. 4º, II e III, da Lei n.º
12.529/2011 c/c a Lei n.º 9.784/99 — o CADE pode disciplinar procedimento
sem nova lei e sem depender da re-caracterização do Art. 12.

---

## 2. Falha estrutural da leniência clássica em mercados digitais

A leniência clássica é tecnologia de ruptura de cartéis: explora a
instabilidade interna do dilema do prisioneiro entre conspiradores externos.
Mas as condutas prioritárias em mercados digitais — autopreferência,
restrições verticais, recusa de acesso a dados, predação algorítmica,
vinculação — são predominantemente unilaterais. Não há co-conspirador
externo a quem oferecer imunidade. A informação relevante reside em pequenos
núcleos técnicos da firma (engenharia de produto, ranking, ad-tech,
acquisitions), tipicamente 2–3 papéis primários.

A intuição-chave do canal é **trocar de jogo**: se a coordenação simultânea
não emerge espontaneamente, o canal a fabrica como serviço público. Marcos
contemporâneos confirmam a transponibilidade: o DMA Whistleblower Tool da UE
(abr/2024) oferece canal anônimo sem recompensa; a Diretiva 2019/1937
fornece proteção horizontal anti-represália; o DOJ-ATR Whistleblower Rewards
Program (jul/2025) institui o primeiro programa federal antitruste de
recompensa, com primeiro prêmio pago em jan/2026 — precedente direto para o
caminho infralegal-recompensado análogo ao Regime B.

---

## 3. Blocos construtivos de desenho de mecanismos

A LCMC combina três blocos distintos da literatura:

- **Leniência ótima de Spagnolo (2004)**: descontos progressivos por
  posição na fila sustentam delação em equilíbrio com população finita.
  Transpomos o gradiente para a fila intra-firma calibrada por Saito (2021):
  1ª posição 43,43%; 2ª 34,51%; 3ª 20,22%; piso 15% a partir da 9ª.
- **Blocos analíticos de Aubert-Rey-Kovacic (2006)**: formalizam
  coexistência de programa de leniência com recompensa direta ao
  denunciante. Emprestamos a estrutura do payoff mas substituímos delação
  unilateral por *depósito condicional*.
- **Template institucional do Dodd-Frank §922**: pagamento de 10–30% sobre
  multas SEC ≥ US\$ 1 milhão; gerou jurisprudência robusta sobre
  re-caracterização do pagamento como ressarcimento (paralelo *relator-style*
  da False Claims Act). Transposição ao antitruste digital exige adaptação:
  a SEC opera sob *taxing power* federal sem reserva penal; o CADE atravessa
  três competências constitucionais (concorrencial, tributária Cᵩ, penal
  Cₚ), cada uma com sua reserva.

A novidade não está nos blocos individualmente, mas no acoplamento sob
**escrow institucional**: a fila ordenada à la Spagnolo só dispara quando a
massa crítica à la Ayres-Unkovic é atingida no escrow. Recompensas à la
Aubert-Rey-Kovacic decaem com a posição via gradiente Saito, mas o
pagamento ao k-ésimo só existe se $k \geq q_{\min}\cdot n$.

---

## 4. Análise comparada de programas existentes

| Programa | Canal | Recompensa | Base normativa |
|---|---|---|---|
| SEC Whistleblower (EUA, 2010) | ✓ | 10–30% | Dodd-Frank §922 |
| DOJ-ATR Rewards (EUA, 2025) | ✓ | 15–30% | Resolução administrativa |
| DMA Whistleblower Tool (UE, 2024) | ✓ | — | Reg. (UE) 2022/1925 |
| Diretiva (UE) 2019/1937 | — | — | Diretiva supranacional |
| CADE leniência (BR) | — | — (imunidade) | Lei 12.529 Art. 86 |
| **LCMC proposta (BR)** | **✓ (escrow)** | **opcional** | **Resolução CADE (Art. 4º Lei 12.529 + Lei 9.784)** |

Quatro observações estratégicas:

1. Apenas dois programas oferecem canal qualificado *e* recompensa — SEC e
   DOJ-ATR — ambos em jurisdição com *taxing power* federal robusto.
2. A arquitetura UE separa proteção (Diretiva, horizontal) e canal (DMA
   Tool, setorial) — preserva proteção mesmo onde recompensa não é
   institucionalmente viável.
3. **DOJ-ATR (jul/2025) é o paralelo institucional mais próximo do Regime B
   brasileiro proposto**: ambos operam canal por ato infralegal sob
   autoridade preexistente. Sucesso do DOJ-ATR (primeiro prêmio jan/2026)
   sugere via infralegal viável quando adotada com decisão administrativa
   firme.
4. Nenhum programa atual combina canal de depósito condicional com massa
   crítica intra-firma como gatilho. Callisto é o análogo operacional
   mais próximo mas domínio (assédio em campus) é estruturalmente distinto.

A LCMC ocupa **nicho ainda vazio na taxonomia**.

---

## 5. O mecanismo LCMC

O canal de depósito condicional opera em cinco fases sequenciais. A
recompensa via TCC (instrumento *Whistleblower-as-a-Service*) é apenas
o acoplamento monetário opcional da fase P3 — o canal funciona sem ele.

1. **Sinalização (P1)**: cada empregado que observa indício de violação
   recebe sinal privado ruidoso e decide, segundo seu arquétipo, se reporta.
2. **Depósito condicional (P2)**: empregado que decide reportar não envia
   denúncia tradicional — deposita denúncia condicional no escrow operado
   pela autoridade (à la Ayres-Unkovic 2012); depósito é selado, firma não
   é notificada.
3. **Abertura simultânea (P2.5)**: canal verifica, a cada ciclo, se fração
   de co-depósitos sobre a mesma firma atingiu o gatilho $q_{\min}\cdot n$;
   se sim, todos os depósitos da firma se abrem simultaneamente
   (*all-or-nothing*), colapsando em caso único de prova qualificada.
4. **Decisão da firma (P3)**: aberto o caso, sob acoplamento monetário, a
   firma compara o desconto $D$ com a recompensa total $W$ e paga quando
   IC-F\* ($D > W$) é satisfeita.
5. **Autoridade (P4)**: caso é instaurado, sujeito a restrição de
   capacidade $\kappa$ e acurácia que cresce com a qualidade da prova.

A charneira jurídica do Regime B, para o acoplamento monetário, é o **Art.
12 da Resolução CADE n.º 21/2018**:

> *"Art. 12. A vantagem auferida ou pretendida e o efetivo prejuízo causado
> serão considerados, entre outros fatores, na fixação do valor da
> contribuição pecuniária, observado o disposto no art. 85 da Lei nº 12.529,
> de 2011. §1º Será considerada como circunstância atenuante, para fins do
> disposto no caput deste artigo, o efetivo ressarcimento extrajudicial ou
> judicial das vítimas pelo representado, na forma do art. 45, V e VI da
> Lei nº 12.529, de 2011."*

A recompensa paga pela firma aos denunciantes *pode ser* re-caracterizada
como ressarcimento extrajudicial sob este dispositivo — controvertido,
sujeito à validação posterior pelo Judiciário (o risco de anulação judicial da re-caracterização) — gerando o
desconto $D$ sem mudança legal. **Crucialmente**: o canal em si dispensa o
Art. 12, com base autônoma no Art. 4º da Lei 12.529 c/c Lei 9.784/99.

---

## 6. Modelo baseado em agentes e teste de estresse

A análise empírica usa ABM com três classes em Mesa 3.x: `TrabalhadorAgent`
(observa conduta segundo papel, decide via seis arquétipos comportamentais),
`EmpresaAgent` (cultura de conformidade, conduta potencial, decisão de
cooperação), `AutoridadeAgent` (mantém escrow e processa casos sob
restrição de capacidade). Dinâmica em horizonte discreto com seis fases por
tique (P0 atualização de detecção; P1–P4 acima).

Calibração formal:
- Gradiente Saito intra/inter-firma verbatim contra Saito (2021), 349 TCCs.
- Capacidade institucional contra RIG/TCU 2022–2024 (180 servidores área-fim).
- **Ponto ótimo da calibração formal (Nelder-Mead, 5 seeds, 19 avaliações)**:
  $(f_v^\star, t_c^\star) = (0{,}323;\, 0{,}481)$ produz 0,56 TCC/ano
  contra alvo normalizado 0,60 — **erro relativo 6,65%**, alvo dentro do IC
  bootstrap 95% $[0{,}200;\, 0{,}900]$. $N^\star$ implícito: 1.679 firmas
  (predição falsificável; sobrevive ao teste de sanidade — 73 investigações
  instauradas em 2024 sobre N\* = 4,3% de cobertura anual, ordem plausível).

### Cinco proposições

**Proposição 1** (viabilidade IC): Sob Regime B com acoplamento monetário e
canal operante, existem parâmetros no interior do espaço factível em que
IC-F\* e IR-W são satisfeitas estritamente. — *Verificada por teste de
regressão.*

**Proposição 2** (unicidade Morris-Shin): No limite $\tau \to 0$, há
equilíbrio único de *switching* $s^*$ para cada $(k, W, r)$; sob
heterogeneidade de arquétipos e papéis, unicidade é conjectura aberta. —
*Verificada sob homogeneidade; aberta sob heterogeneidade.*

**Proposição 3** (dominância de bem-estar): Para conjunto de medida positiva
de $(W, D, \sigma)$, bem-estar social esperado é estritamente maior sob B
que sob A. — *Suportada empiricamente (IC bootstrap multi-seed não cruza
zero).*

**Proposição 4** (coordenação via canal — LCMC): Para qualquer regime, a
probabilidade de uma firma com violação real ser instaurada é estritamente
maior sob canal de depósito condicional do que sob denúncias individuais
isoladas. — *Verificada por construção.*

**Proposição 5** (erosão Coleman): Forma forte ("existe $\alpha^*$ tal que
B colapsa em A") **REFUTADA** pela varredura dedicada (10 seeds × 8 $\alpha$
× 40 tiques: dano em B fica ~8× abaixo do piso A estável até
$\alpha = 0{,}9$). Forma fraca (substrato decai com $\alpha$) verificada.

---

## 7. Enquadramento cibernético

A LCMC pode ser lida em termos de **variedade requisitada** (Ashby 1956).
Teorema de Conant-Ashby: regulador eficaz deve conter modelo do sistema
regulado; variedade do regulador precisa igualar ou exceder variedade do
regulado. No antitruste, a variedade interna da firma digital (centenas de
produtos, milhares de algoritmos) excede em ordens de magnitude a variedade
investigativa do CADE (180 servidores área-fim em 2024). Defasagem de
variedade explica a seleção subdeterminada de condutas instauradas.

A LCMC **amplifica** variedade do regulador recrutando sensores internos —
trabalhadores cujo conhecimento do produto, do ranking, do *corp dev* é, por
construção, equivalente ao do regulador externo. O canal é operador de
amplificação no sentido de Beer (1972): estrutura System 3 (controle
operacional) que importa variedade do System 1 (operação) sem destruir
autonomia. O escrow preserva autonomia individual (denúncia isolada não vira
processo); a abertura simultânea realiza a importação de variedade.

---

## 8. Pré-condição sociológica

A viabilidade empírica da LCMC depende de fenômeno sociológico
contemporâneo distinto do que sustentava a leniência clássica. Esta opera
sobre conspiradores externos em relação contratual cooperativa-criminosa.
A LCMC opera sobre **trabalhadores regulares**, cuja decisão de depositar
não é cooperação assimétrica em conspiração mas **abandono parcial da
lealdade institucional** em favor de norma externa.

O fenômeno emergiu visivelmente em 2018–2024 em empresas de tecnologia:
**Google Walkout** (nov/2018, ~20.000 trabalhadores em 50+ escritórios),
**Alphabet Workers Union** (jan/2021), denúncias de **Frances Haugen**
sobre Meta (2021). Todas exibem padrão de denúncia interna coletiva por
motivação principalmente ética, com proteção legal limitada e sem recompensa
associada.

Olson (1965) previu o fenômeno como ocorrência marginal em grupos pequenos
com interesse perceptível; a transposição contemporânea sugere número
absoluto pequeno (5–20 por firma) mas não-nulo — exatamente a faixa que o
$q_{\min}\cdot n$ pretende mobilizar. Os arranjos NLRB *Section 7* (EUA) e
CLT Art. 543 + Art. 462 §2º (BR) são o substrato normativo trabalhista
contemporâneo do qual a LCMC se beneficia sem dependência exclusiva.

---

## 9. Tradução política para o Brasil

Duas portas regulatórias:

- **Regime B** (infralegal): Resolução complementar à 21/2018
  institucionaliza procedimento de depósito condicional sob Art. 4º (II e
  III) Lei 12.529 c/c Lei 9.784/99. Depende exclusivamente de decisão
  administrativa do CADE.
- **Regime C** (lei nova): extensão da Lei 13.608/2018 ao antitruste,
  criando percentual estatutário explícito. Requer aprovação congressual.

Assimetria de viabilidade 2024–2027: Congresso BR tem agenda concentrada em
reforma tributária; PL 2768/2022 (telecomunicações) parado desde 2023.
Regime C é **provavelmente infactível** salvo crise reputacional grande.
Regime B depende de (i) prioridade interna no CADE, (ii) capacidade DEE/SG,
(iii) aceitação judicial da re-caracterização sob Art. 12 — todas sob
arbítrio administrativo.

**Coordenação inter-institucional CADE–CGU–MPF**: canal LCMC coexistiria com
canal CGU sob LAC 12.846/2013 e persecução criminal MPF sob Lei 8.137. A
proposta: não-concorrência, com cross-referral por matéria primária.

**Paralelo DOJ-ATR é instrutivo**: DOJ instituiu seu programa em jul/2025
sob Resolução administrativa em parceria com USPS — exatamente a estrutura
do Regime B proposto. Sucesso (primeiro prêmio jan/2026) sugere via
infralegal viável com decisão administrativa firme. DMA Whistleblower Tool
da CE é precedente complementar para canal-sem-recompensa — relevante se
re-caracterização do Art. 12 enfrentar resistência judicial.

---

## 10. Conclusão

**Cinco resultados** sustentam a proposta:

1. Leniência clássica é estruturalmente inadequada para condutas
   unilaterais, dominantes em plataformas digitais.
2. Canal de depósito condicional (*information escrow* de Ayres-Unkovic
   aplicado ao antitruste) resolve sub-iniciação coletiva por construção,
   eliminando equilíbrio de silêncio sem requerer recompensa monetária.
3. Sobre o canal, instrumentos de internalização (WaaS via TCC; Hirschman;
   crédito tributário; leniência criminal individual) são acoplamentos
   opcionais com reservas constitucionais distintas, analisáveis
   separadamente.
4. Implementação infralegal sob Regime B é viável *de lege lata* pela base
   autônoma Art. 4º Lei 12.529 + Lei 9.784/99, sem dependência da
   re-caracterização do Art. 12; paralelo DOJ-ATR confirma viabilidade da
   via administrativa.
5. ABM identifica cinco vetores de quebra mensuráveis (TCC clássico
   absorvente; anulação judicial; custo legal individual; massa crítica
   inalcançável; erosão Coleman); **forma forte da Prop. 5 explicitamente
   refutada** pela varredura multi-seed.

**Limites reconhecidos**: $N^\star \approx 1.679$ firmas é predição
falsificável a verificar contra cadastro CADE real; Prop. 2 sob
heterogeneidade segue conjectura aberta; viabilidade política do Regime C é
baixa no horizonte 2024–2027; viabilidade do Regime B depende de decisão
administrativa não anunciada nem em consulta pública.

**Três frentes futuras**:

- **Empírica**: confirmar/refutar $N^\star$; calibrar
  $\alpha_{\text{erosão}}$ contra evidência longitudinal (SEC, DOJ-ATR após
  2026, DMA).
- **Teórica**: fechar unicidade sob heterogeneidade (Prop. 2c); investigar
  não-bifurcação formal em $(\lambda, \beta_H)$.
- **Institucional**: redigir, em sede acadêmica colaborativa com
  pesquisadores de direito administrativo, minuta de Resolução complementar
  à 21/2018 articulando procedimento de depósito condicional — contribuição
  que este artigo declina por não-vinculação política do autor.

---

## Compilação do PDF

A versão LaTeX está em `paper/main.tex`. Para regerar PDF:

```bash
# Regerar as 4 figuras dos módulos viz/ → paper/figs/
python scripts/gerar_figs_paper.py

# Compilar com bibliografia
cd paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Como citar

Use `CITATION.cff` na raiz do repositório:

```
APA: L. (2026). Leniency Conditional on Critical Mass:
A Conditional-Deposit Channel for Unilateral Conduct in Digital Markets. Working paper.
URL: https://github.com/freirelucas/waas-antitrust
```

DOI Zenodo: emitido após congelamento da versão de submissão.
