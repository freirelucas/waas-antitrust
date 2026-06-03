<span class="ato-chip">Ato 2 de 5 · A hipótese</span>

# Como o mecanismo se sustenta

A pergunta natural — e a primeira que aparece quando alguém ouve o desenho do WaaS pela primeira vez — é uma versão mais educada de **"você é ingênuo?"**:

> Basta a empresa se recusar a pagar os denunciantes e ainda assim pegar o desconto para tudo ruir, não?

Esta página responde de frente. Em prosa primeiro, com aritmética em seguida, e com os três pontos onde o mecanismo pode realmente quebrar mapeados — porque o argumento honesto não é "isto sempre funciona", e sim **"isto funciona sob estas condições, falha sob estas outras, e ambas estão no modelo"**.

## A escolha da firma, em uma frase

A firma já foi denunciada — o gatilho de massa crítica disparou, o caso vai ao CADE. A partir daí, ela escolhe entre três caminhos. Em todos eles, paga **alguma coisa**; a diferença é a soma.

1. **Assinar um TCC com ressarcimento WaaS** — paga a recompensa $W$ aos denunciantes e ganha o desconto cheio $D_{\text{total}}$ no acordo.
2. **Assinar um TCC clássico** — não paga $W$, mas obtém apenas o desconto comum $D_{\text{base}}$ que o Art. 85 da Lei 12.529/2011 já oferece em qualquer TCC.
3. **Não assinar nada** — enfrenta a sanção cheia $S$, com a probabilidade de condenação que a investigação produz.

A diferença entre os dois primeiros — entre o TCC-WaaS e o TCC clássico — é a peça que sustenta o argumento. Não é o desconto **total** $D_{\text{total}}$ que move a firma a pagar a recompensa; é o **incremento** que o canal WaaS oferece sobre o que a firma teria de qualquer jeito.

<div class="pull-quote" markdown>
A firma paga os denunciantes não porque ganha um desconto. Paga porque ganha um desconto <strong>maior</strong> do que conseguiria sem isso — e maior o suficiente para cobrir a recompensa, com folga.
</div>

## A IC-F\*, em prosa antes da fórmula

A condição que define quando a firma escolhe pagar tem nome em economia institucional: **incentive compatibility da firma** — escrita aqui como **IC-F\***. Em prosa direta:

> A firma paga a recompensa $W$ se, e somente se, o **incremento** de desconto que o canal WaaS oferece for maior que a recompensa.

Em fórmula, com $S$ sendo a sanção esperada e $D_{\text{base}}$ o desconto que o TCC clássico já garante:

$$
W < D_{\text{extra}} \quad \text{onde} \quad D_{\text{extra}} = D_{\text{total}} - D_{\text{base}} = (D_{\text{disc}} - D_{\text{disc, base}}) \cdot S
$$

A versão simplificada $W < D_{\text{total}}$ — usada nos artigos teóricos de leniência clássica — só funciona se assumirmos $D_{\text{base}} = 0$. Quando o TCC clássico **já** dá desconto, ignorar isso é overclaim. O modelo computacional incorpora a forma correta (parâmetro `D_disc_base_tcc` em `WaaSParametros`).

## Uma firma, R$ 1 bilhão de receita, 30 minutos com a calculadora

Aritmética é o tipo de coisa que parece dura até virar familiar. Aqui está com nomes em reais.

Imagine uma firma com receita afetada $R = \text{R\$}\,1$ bilhão e severidade da conduta $\sigma = 0{,}5$ (no meio da escala). O CADE pratica multas-base na faixa de 0,1% a 20% da receita; usamos 5% como referência conservadora, e escalamos por $(1+\sigma)$:

$$
S = 0{,}05 \cdot R \cdot (1 + \sigma) = 0{,}05 \cdot 1\,000 \cdot 1{,}5 = \text{R\$}\,75\text{ milhões}.
$$

O desconto total a que ela teria direito num TCC com ressarcimento WaaS é, digamos, 30% — alinhado com o que o Art. 12 permite combinando com o Art. 85:

$$
D_{\text{total}} = 0{,}30 \cdot S = \text{R\$}\,22{,}5\text{ milhões}.
$$

O desconto que ela teria **mesmo sem WaaS**, só com o TCC clássico, é o que precisamos calibrar contra os dados de Saito (2021). Para este exemplo, usamos uma estimativa intermediária — 10%:

$$
D_{\text{base}} = 0{,}10 \cdot S = \text{R\$}\,7{,}5\text{ milhões}.
$$

<div class="numero-callout" markdown>
<span class="valor">R$ 15 milhões</span>
<span class="legenda">O incremento $D_{\text{extra}}$ — exatamente quanto a firma ganha **a mais** ao escolher o caminho WaaS em vez do TCC clássico. É contra este número, não contra os R$ 22,5 milhões totais, que a recompensa total $W$ tem de ser menor para a firma pagar.</span>
</div>

Agora o outro lado. Suponha que 10 denunciantes internos atingiram a massa crítica. Cada um receberia uma recompensa de 1,5 salários anuais — calibrada para satisfazer a participação do trabalhador (IR-W), inclusive cobrindo o custo legal individual. Com $w_a = \text{R\$}\,180\,000$ e $W_{\text{indiv}} = 1{,}5 \cdot w_a$:

$$
W = 10 \cdot 1{,}5 \cdot 180\,000 = \text{R\$}\,2{,}7\text{ milhões}.
$$

A IC-F\* fica satisfeita com folga ampla:

<div class="numero-callout" markdown>
<span class="valor">R$ 12,3 milhões</span>
<span class="legenda">A margem que sobra na conta da firma quando ela escolhe o caminho WaaS. É o **preço** que o mecanismo extrai do bolso da empresa investigada e devolve ao bolso dos trabalhadores que falaram — uma transferência privada com efeito de prevenção pública.</span>
</div>

Tudo isso depende, evidentemente, de quanto $D_{\text{base}}$ realmente é na prática do CADE. Quando esse número aproxima-se de $D_{\text{total}}$, a margem encolhe. Quando ultrapassa, o mecanismo **deixa de funcionar** — e este é o primeiro dos três vetores que cobrimos a seguir.

## Os três vetores de quebra — onde o argumento pode mesmo ruir

### Vetor A: e se o TCC clássico já der desconto suficiente?

Este é o cético que diz "basta a empresa não pagar e pegar o desconto". A versão tecnicamente correta da crítica é: se $D_{\text{base}}$ já cobre uma fração significativa de $D_{\text{total}}$, a margem $D_{\text{extra}}$ encolhe e a IC-F\* deixa de motivar o pagamento.

O **desenho jurídico** se sustenta porque o Art. 12 da Res. 21/2018 é explícito ao tratar o ressarcimento das vítimas como **acréscimo** ao desconto genérico. A magnitude desse acréscimo é discricionária — depende da prática do CADE em cada caso. A calibração empírica desse parâmetro é precisamente o que falta em **R03** (calibração formal contra Saito 2021).

O **modelo** torna isto explícito: o parâmetro `D_disc_base_tcc` em `WaaSParametros` permite simular qualquer valor de $D_{\text{base}}$, inclusive o pior caso em que $D_{\text{base}} = D_{\text{total}}$. Quando isso acontece, $D_{\text{extra}} = 0$, ninguém paga a recompensa, e o contador `n_firmas_optaram_tcc_classico` registra a quebra. Testes em `tests/test_vetores_quebra.py` cobrem o caso direcionalmente.

### Vetor B: e se o Judiciário anular o TCC?

A re-caracterização da recompensa como "ressarcimento das vítimas" é uma construção jurídico-finalística. O Judiciário pode rejeitá-la — e a recusa pode vir anos depois do TCC ter sido assinado, **anulando-o retroativamente**. Quando isso acontece, a empresa perde o desconto e a multa cheia retorna como crédito ao erário.

Este é precisamente o **falsificador F6** declarado no desenho. A defesa institucional contra ele é dupla. Em primeiro lugar, o Regime C — extensão da Lei 13.608/2018 via Congresso — elimina a controvérsia legal, custando voto político. Em segundo, mesmo em Regime B, o risco de anulação é uma propriedade do desenho que precisa ser dimensionada, não escondida.

O **modelo** torna esse risco calibrável via `p_anulacao_tcc`. Em P4, todo TCC assinado é sorteado contra essa probabilidade; quando anulado, o contador `n_tcc_anulados` registra, a multa cheia volta ao erário, e o sistema perde a coordenação que o mecanismo construía. Em testes, $p_{\text{anulação}}$ alta faz o Regime B convergir para o Regime A — um falsificador quantitativo, não verbal.

### Vetor C: e os advogados dos denunciantes?

Esta é uma crítica que custumeiramente passa em branco e merece resposta direta. **Sim**, o denunciante terá custos legais: advogado para reivindicar a recompensa, defesa em eventual ação trabalhista por represália, e — em hipótese pior — defesa criminal se for caracterizado como **partícipe** da conduta (a colisão dura com o Art. 86 da Lei 12.529/2011, território de leniência clássica).

Três cenários institucionais são possíveis, e implicam calibrações diferentes:

1. **O denunciante paga.** Eleva o piso da IR-W — a recompensa precisa ser maior para compensar. Estimativas conservadoras no Brasil colocariam o custo legal entre **10% e 50% de um salário anual**.
2. **A empresa cobre via TCC.** Análogo ao programa Dodd-Frank §922 da SEC americana, em que o pagamento bruto pode incluir margem para honorários do advogado do denunciante. Requer cláusula explícita na proposta de TCC e aprovação do CADE.
3. **O Estado financia via fundo.** Análogo ao IRS Whistleblower Office. Exige lei (Regime C) e dotação orçamentária — politicamente custoso, mas estruturalmente robusto.

O **modelo** torna isto calibrável via `custo_legal_uw` (em unidades de $w_a$). O parâmetro entra na IR-W do arquétipo "racional" — quando o custo legal é alto, a recompensa $W$ precisa subir para o trabalhador racional ainda denunciar.

## O break-even ético coletivo (R16)

Até aqui o argumento foi inteiramente financeiro — IC-F\* da firma, IR-W
do trabalhador, contas em reais. Mas há uma intuição forte que a versão
puramente racional não captura: **a partir de uma certa massa crítica,
algo muda na lógica individual**. O trabalhador que vê dez colegas falando
não decide pelo mesmo cálculo de quem está sozinho.

O modelo agora incorpora isso explicitamente, baseado em **Torsell (2026,
*Theory and Decision*)** e na teoria de inequity aversion de **Fehr &
Schmidt (1999)**. Um quinto arquétipo — `"fairminded"` — entra ao lado dos
quatro de Hokamp-Pickhardt (ético, imitativo, racional, aleatório). O FM
agente computa o payoff racional clássico **e** adiciona um prêmio ético
proporcional à fração de pares já sinalizando:

$$
\text{ganho}_{\text{FM}} = W_{\text{efetivo}} + \alpha \cdot \phi_{\text{vizinhos}} \cdot w_a - \text{custos}
$$

onde $\phi_{\text{vizinhos}}$ é a fração de vizinhos da rede intra-firma
que sinalizaram no tique anterior, e $\alpha$ é o peso da inequity
aversion (parâmetro `peso_inequity_aversion`).

**A consequência emergente é o break-even ético**: enquanto $\phi$ é
baixa, FM se comporta como racional puro; quando $\phi$ ultrapassa um
limiar tácito, o prêmio ético inverte o sinal da decisão — calar passa a
ser desigualdade moral mais custosa do que falar. Não é hardcoded; é
propriedade emergente do mesmo agente Fehr-Schmidt que a literatura usa
em jogos de barganha.

O resultado central de Torsell (2026) — que FM **proliferaria** em
populações HE+FM sob qualquer dinâmica payoff-monotone, com aprendizado
intra-geracional via *fictitious play* — sugere que o canal ético não é
uma curiosidade marginal; pode ser **a peça dominante** quando a massa
crítica se forma. Modelar isto endogenamente é o trabalho de R16, e o
catálogo de [cenários normativos](#) (R17) já oferece presets que ativam
o canal.

## Cenários normativos como variantes paramétricas (R17)

Uma das primeiras objeções honestas a um modelo deste tipo é "**e se
mudar a lei?**". A resposta tradicional — escrever um parágrafo no paper
descrevendo a alteração — não é boa o suficiente. A versão deste projeto
trata cada alteração normativa como um **cenário comparável**: um conjunto
nomeado de sobrescritas de parâmetros, executável e reportável.

O catálogo (módulo `waas_antitrust.cenarios`) contém sete cenários
canônicos:

| Cenário | Hipótese institucional |
|---|---|
| `status_quo` | Brasil hoje — sem canal de incentivo individual. |
| `resolucao_pura` | Regime B — Art. 12 da Res. 21/2018; F6 calibrado em 10%. |
| `resolucao_mais_portaria_mte` | Regime B + portaria MTE com proteção trabalhista reforçada — `r_represalia` cai a 8%, `custo_legal` a 15%. |
| `lei_waas_pura` | Regime C — Lei 13.608/2018 estendida; F6 = 0. |
| `lei_waas_com_fundo_honorarios` | Regime C + fundo público para honorários (análogo IRS Whistleblower Office). |
| `lei_waas_com_vesting_padrao` | Regime C + cláusula padrão de vesting acelerado (Hirschman R07 universal); haircut IRPF+INSS realista. |
| `cenario_sancao_dura` | Regime C + multa por descumprimento de TCC = 2× sanção base (R18). |

Cada cenário roda como uma chamada de função:

```python
from waas_antitrust import cenarios
from waas_antitrust.model import WaaSModel, WaaSParametros

base = WaaSParametros(n_empresas=20, n_tiques=40, seed=42)
for nome in cenarios.listar_cenarios():
    params = cenarios.aplicar_cenario(base, nome)
    df = WaaSModel(params).executar()
    print(nome, df["dano_acumulado"].max())
```

Comparar regimes vira **trabalho computacional reprodutível**, não
exercício retórico.

## Os outros três incentivos compatíveis

Além da IC-F\* da firma, o desenho precisa satisfazer simultaneamente:

| Sigla | Quem | Condição | Onde no modelo |
|---|---|---|---|
| **IR-W** | trabalhador | $W \ge \text{custo esperado de represália} + \text{custo legal}$ | `agents.py::decidir_sinal` (arquétipo racional) |
| **IC-T** | trabalhador | $W$ deve compensar penalidade por falso reporte | `agents.py` (mesma função, parcela $F_{\text{falso}}$) |
| **IC-F\*** | firma | $W < D_{\text{extra}}$ (vide acima) | `model.py` (P3) |

A camada **Hirschman exit-with-equity** (R07) acrescenta um quarto incentivo opcional, válido apenas sob Regime C: cláusulas contratuais de vesting acelerado por gatilho de ação coletiva. Quando ativas, ampliam a IC-F\* para $W < D_{\text{extra}} + \text{custo de êxodo coletivo}$ — a firma também ganha por **não perder capital humano**, e isso ajuda a fechar o cálculo em casos marginais.

## O que ainda pode ruir mesmo assim

Há pendências que o modelo, sozinho, não resolve. Estão rastreadas em [Decisões e backlog](DECISIONS.md), e a lista curta é:

- **R03** — calibração formal contra Saito (2021), DEE/CADE (2022, 2024), Wiedman & Zhu (2023, Dodd-Frank §922). Em particular, $D_{\text{base}}$ precisa de mediana empírica brasileira.
- **R09** — endogeneizar $g_i(t)$ (atratividade de violar como função do estado). Hoje é sorteio uniforme estático.
- **R10** — IC-F\* completa $W + p_{\text{pago}} \cdot (S - D) < p_{\text{não pago}} \cdot S$, em vez da forma simplificada.
- **R13** — distribuição Pareto/lognormal de fatia de mercado (hoje uniforme; em digital, o dano é cauda longa).

A página de [Limitações](limitacoes.md) sintetiza isso em linguagem acessível; a [Crítica x10](critica_x10.md) detalha o que oito revisores externos apontaram.

<div class="ato-fim" markdown>
**Fim do Ato 2.** Temos um desenho — com fórmula, exemplo numérico e três vetores de quebra calibráveis. Mas até aqui é tudo papel e equação. **Será que funciona em simulação?** O Ato 3 mostra o que acontece quando rodamos o modelo nos três regimes, em 20 firmas, ao longo de 40 trimestres.

[Ato 3: Resultados →](resultados.md)
</div>
