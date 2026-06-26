# Quando a infração é unilateral, quem denuncia?

<p class="deck">Proposta acadêmica de um canal de depósito condicional (<em>information escrow</em>) operado pelo CADE para destravar a denúncia interna em mercados digitais — onde a infração é tipicamente de uma firma só, sem cúmplice externo a quem oferecer leniência clássica.</p>

<p class="byline"><em><a href="sobre/">L.</a></em> · <a href="sobre/">Rascunho v0.2.0</a> · jun/2026 · CC BY-SA 4.0</p>

<p class="lede">Programas de leniência transformaram o enforcement antitruste das últimas três décadas, mas operam sob uma premissa cada vez mais frágil: a existência de um cartel — coordenação entre firmas distintas cuja instabilidade interna a leniência explora. Em mercados digitais, parte central das condutas potencialmente anticompetitivas é unilateral. Não há cúmplice externo a quem oferecer imunidade; a informação relevante reside dentro da própria firma. Esta página apresenta uma proposta de mecanismo — a LCMC — desenhada para esse domínio.</p>

[Ato 2 · O mecanismo](mecanismo.md) · [Simulador in-browser](brincar.md) · [Paper](paper.md)

| R\$ 12,3 mi | 1.679 firmas | +1.363% | 364 testes |
|:---:|:---:|:---:|:---:|
| margem da firma sob TCC-WaaS para receita de R\$ 1 bi (cenário ilustrativo) | universo CADE implícito após calibração formal R03 (predição falsificável) | ΔW do Regime B sobre o A em bem-estar agregado (rodada multi-seed) | verdes em ~31 s · 23 figuras reproduzíveis · `mkdocs --strict` limpa |

> **Princípio LCMC.** O CADE recebe denúncias com cláusula de abertura condicional e as mantém em escrow até que uma fração mínima `q_min · n` de trabalhadores da mesma firma também tenha depositado denúncias compatíveis. Quando o gatilho é atingido, todas as denúncias se abrem simultaneamente; antes disso, nenhuma é exposta. O problema clássico de "ninguém quer ser o primeiro" (Olson 1965) é eliminado por construção.

<span class="kicker">Ato 1 · O problema</span>
## A leniência clássica acabou de bater num muro

Por quase trinta anos, programas de leniência foram a peça-mestre do enforcement antitruste. A lógica é simples: dois ou mais conspiradores fizeram um cartel; quem entregar primeiro escapa da multa. **O cartel se denuncia sozinho** — é a beleza do desenho.

Em mercados digitais, no entanto, o abuso costuma vir de **uma única empresa** — sem cúmplice externo para delatar. Quatro exemplos do noticiário recente:

- O Google rebaixando concorrentes em buscas para favorecer o próprio comparador de preços (*self-preferencing*).
- A Apple proibindo que o app Spotify mencione opções de pagamento fora da App Store (*anti-steering*).
- O iFood mantendo cláusulas de exclusividade que impedem restaurantes de operar com concorrentes.
- O Facebook (Meta) comprando o Instagram para neutralizar uma plataforma rival emergente (*killer acquisition* — aquisição cujo propósito é eliminar o concorrente, não absorvê-lo).

A informação sobre essas práticas existe **dentro da própria empresa** — em conversas no Slack, na ata da reunião do comitê de produto, no slide-deck do time de aquisições. Mas ela não chega ao CADE. No Brasil de hoje, o trabalhador que falaria arrisca emprego, carreira, tranquilidade — e ganha **nada de previsível** em troca.

Os quatro exemplos acima são caso individual de uma lista mais longa: o projeto cataloga 28 condutas digitais unilaterais com taxonomia, taxa de observabilidade e estimativa de massa crítica em [Catálogo de condutas digitais](condutas.md). Para a definição precisa de "canal", "escrow", "massa crítica" e "abertura simultânea", ver [Glossário](glossario.md) e [Terminologia canônica](TERMINOLOGIA.md).

> A leniência só funciona quando há cumplicidade entre firmas. Quando a infração é unilateral, é como esperar que o ladrão se entregue porque tem medo do espelho.

<span class="kicker">A tese</span>
## A resposta: LCMC como canal de depósito condicional

Em mercados digitais com **fosso competitivo profundo** (uma plataforma dominante cercada de barreiras estruturais — efeitos de rede, dados acumulados, integração vertical — que tornam a entrada de concorrente quase impossível), a cumplicidade na infração existe **dentro da própria empresa**: entre os times de engenharia, produto, jurídico e aquisições. O problema central não é "como punir a firma" nem "como pagar o denunciante" — é **como resolver a coordenação dos trabalhadores que veem a conduta mas não querem brigar a luta sozinhos**.

A proposta deste projeto, em uma frase:

> 🔑 **LCMC — canal de depósito condicional.** O CADE opera um canal qualificado de recepção de denúncias com cláusula de abertura condicional. O trabalhador entrega ao CADE sua denúncia com prova específica e diz: *"esta denúncia só é instaurada se houver ao menos `q_min · n` outros trabalhadores do mesmo setor/firma que também depositarem denúncias compatíveis dentro de uma janela `Δt`"*. As denúncias ficam em **escrow** — não notificam a firma, não viram processo, não vazam — até que o gatilho de massa crítica seja atingido. Quando o é, **todas se abrem simultaneamente**: ninguém foi o primeiro isoladamente.

A LCMC é **mecanismo de coordenação**, não de pagamento. Resolve diretamente um problema clássico estudado por Mancur Olson em 1965: em grupos pequenos, ninguém quer ser o primeiro a se expor; cada um prefere esperar o outro começar. O canal de depósito condicional **elimina esse impasse por construção** — a denúncia individual nunca fica exposta sozinha enquanto a massa crítica não se forma.

### Três paralelos do cotidiano

Cada um descreve a mesma estrutura por um ângulo diferente.

**🎯 Kickstarter.** Quando você apoia um projeto no Kickstarter, seu cartão **só é cobrado se o projeto atingir a meta** de apoiadores. Se a meta não é atingida, ninguém paga e nenhum projeto começa. A LCMC funciona igual, mas com denúncias: a sua denúncia só "cobra" — vira processo no CADE — se outros trabalhadores da mesma empresa também depositarem. Se não houver coincidência suficiente, ninguém é exposto e nenhum processo se abre. É o desenho *all-or-nothing*: ou todos cooperam e o projeto sai, ou ninguém é exposto.

**🛡️ Callisto** ([callisto.org](https://www.callisto.org)). Plataforma americana em operação **desde 2015** onde estudantes universitárias registram denúncias de assédio sexual. O nome de uma vítima só é revelado se **outra** vítima identificar o **mesmo** agressor. Sem coincidência, o registro permanece anônimo. Coincidência libera; isolamento mantém anonimato. É a prova prática de que o desenho funciona em produção, não só em paper.

**📦 Caixa-cofre.** Imagine envelopes com denúncias entregues a uma caixa-cofre operada por uma instituição neutra — no nosso caso, o CADE. Cada envelope vem com a instrução: *"abra esta caixa apenas quando houver ao menos N envelopes parecidos contra a mesma empresa"*. A caixa pode esperar meses. Quando atinge N, **todos** os envelopes se abrem juntos. Ninguém foi o primeiro a se expor.

O nome acadêmico desse desenho é **escrow de informação condicional** ou *information escrow* — formalizado por Ian Ayres e Cait Unkovic (Yale Law School) em artigo de 2012 na *Michigan Law Review*, vol. 111, p. 145. A LCMC aplica este desenho ao antitruste brasileiro, com o CADE como o "terceiro confiável" que opera a caixa-cofre.

<span class="kicker">Os incrementos</span>
## O que vem depois da abertura — instrumentos opcionais

Quando o canal abre (massa crítica atingida), o procedimento administrativo se instaura: a firma é notificada com prova qualificada e coletiva; o CADE conduz a investigação; eventualmente assina um **TCC** (Termo de Compromisso de Cessação — espécie de acordo em que a firma admite cessar a conduta em troca de redução da multa) ou aplica a multa cheia. Esta parte usa o ferramental jurídico **já existente** na Lei 12.529/2011 — Art. 85 (regras do TCC), Art. 86 (leniência clássica para cartéis), Art. 45 (critérios para calcular a multa final, em jargão jurídico "dosimetria").

**Os instrumentos monetários abaixo são incrementos** ao canal — aumentam a probabilidade de adesão, não são o mecanismo central. Sem nenhum deles, o canal ainda funciona; com eles, opera com taxas de adesão maiores.

| Instrumento incremental | Quem paga | Para quem | Quando |
|---|---|---|---|
| **WaaS — recompensa via TCC** | Firma | Trabalhador | Ex-post: firma paga sob TCC; pagamento re-caracterizado como ressarcimento (Art. 12 Res. 21/2018) |
| **Hirschman — vesting acelerado** | Firma (via equity) | Trabalhador | Ex-ante: cláusula contratual dispara ao gatilho de ação coletiva |
| **Crédito tributário** | Estado (renúncia fiscal) | Trabalhador | Pós-instauração (R22 stub) |
| **Leniência criminal individual** | Estado (não-persecução) | Trabalhador-partícipe | Pós-instauração (R23 stub) |
| **Nenhum — só o canal** | — | — | O canal funciona pela coordenação per se |

A linha **"Nenhum — só o canal"** é a configuração mais conservadora juridicamente: o canal exige apenas uma Resolução do CADE regulamentando o **procedimento de como receber denúncias condicionais** (com base no Art. 4º, II e III da Lei 12.529/2011 combinado com a Lei 9.784/99, que rege o processo administrativo federal). Não cria nova categoria de punição; apenas estrutura *como o CADE recebe* informação. O risco de o Judiciário anular essa Resolução depois — que o projeto chama de **falsificador F6** e analisa em detalhe no [Ato 4 · Limitações](limitacoes.md) — cai materialmente.

<span class="kicker">Saída literal do modelo</span>
## A figura central

A figura abaixo é a **saída literal** de uma execução do modelo computacional. Não é estilizada — vem do `WaaSModel.executar()`, *seed* 11, regimes A/B/C lado a lado.

![Dissuasão endógena e bem-estar — 3 regimes ao longo de 40 trimestres](img/03_dissuasao_bem_estar.png)

**(A)** Violadoras ativas ao longo do tempo: regime A (cinza) cresce e estabiliza alto; regimes B/C (verde/roxo) caem a zero em ~17 tiques. **(B)** Bem-estar social agregado. ΔW (B sobre A) = +1363%.

<aside class="dado-destaque" markdown>
<strong>+1.363%</strong>
Ganho de bem-estar agregado do Regime B (Resolução CADE) sobre o status quo, em uma rodada multi-seed do modelo. O segundo degrau — sinergia internacional R30 — soma a esse ganho um adicional medido no [`internacional.md`](internacional.md).
</aside>

*Leitura sob LCMC corrigida:* a queda de violadoras em B/C é resultado de **denúncias coletivas abrindo do escrow**. Cada vez que o canal abre, o sinal Schelling se propaga (detecção percebida sobe em todas as firmas). O instrumento WaaS está ativo nas curvas verdes/roxas como incentivo incremental à adesão ao canal — não é a causa primeira da queda.

<span class="kicker">Reprodutibilidade</span>
## Reproduzir esta figura em três comandos

Toda a página acima é gerada por código aberto sob CC BY-SA 4.0. O leitor pode reproduzir a figura central em três passos:

```bash
# 1. Clonar e instalar
git clone https://github.com/freirelucas/waas-antitrust.git
cd waas-antitrust && pip install -e ".[dev]"

# 2. Rodar a varredura nos três regimes (60 segundos)
python scripts/gerar_figura_dissuasao.py

# 3. Saída em figuras/03_dissuasao_bem_estar.png
```

Para inspecionar o estado interno do modelo de forma direta:

```python
from waas_antitrust.model import WaaSModel, WaaSParametros

# Regime B padrão
m = WaaSModel(WaaSParametros(n_empresas=20, n_tiques=40, seed=11, regime="B"))
df = m.executar()

# Reporters macro (DataFrame com 40 linhas)
print(df[["n_sinais", "n_empresas_notif", "n_violadoras_ativas",
          "capital_social_residual"]].tail())

# Inspeção micro: arquétipos sorteados, papéis, posições na fila intra-firma
for t in m.trabalhadores_por_empresa[0][:5]:
    print(f"  {t.arquetipo:13s} · papel={t.papel:9s} · sinalizou={t.sinaliza_agora}")
```

A simulação produz 34 reporters em colunas de pandas. Tudo é inspecionável; nada está escondido em variáveis privadas opacas. Ver [Modelagem multiagente](modelagem_multiagente.md) para a anatomia das três classes (`TrabalhadorAgent`, `EmpresaAgent`, `AutoridadeAgent`).

<span class="kicker">Arquitetura institucional</span>
## Três regimes jurídicos, cinco instrumentos

A LCMC pode ser implementada em três regimes regulatórios distintos. Os instrumentos disponíveis dependem do regime — e cada instrumento exige reserva constitucional diferente (Art. 22 I, Art. 146 LC, Art. 5º XXXIX).

| Regime | Como implementado | Status normativo | Instrumentos disponíveis |
|---|---|---|---|
| **A** — status quo | Sem LCMC | — | Nenhum |
| **B** — Resolução CADE | Resolução complementar à 21/2018, **sem mudar a lei** | **de lege lata** (interpretação infralegal) | WaaS (recompensa via TCC sob Art. 12) |
| **C** — Lei ordinária federal | Extensão da Lei 13.608/2018 ao antitruste | **de lege ferenda** (lei nova) | WaaS + Hirschman (vesting acelerado) |
| **Cᵩ** — LC tributária | Lei complementar Art. 146 + LRF Art. 14 | **de lege ferenda** (LC + LRF) | + Crédito tributário (R22 stub) |
| **Cₚ** — Lei penal estrita | Reserva penal Art. 5º XXXIX | **de lege ferenda** (lei penal) | + Leniência criminal individual (R23 stub) |

O **Regime B** é a aposta política deste projeto: usar o que o CADE pode fazer sozinho com a Resolução 21/2018 vigente. O **Regime C** é mais robusto juridicamente mas exige Congresso — e a [viabilidade política 2024-2027](viabilidade_regime_c.md) é incerta. Os sub-regimes Cᵩ e Cₚ são exploratórios.

<span class="kicker">Editoria · roteiros</span>
## Por onde seguir — entrada por papel profissional

<div class="persona-grade" markdown>

<a class="persona-card jornalista" href="imprensa.md" markdown>
<span class="persona-icone">📰</span>
**Jornalista**
3 leads · 6 números com fonte · autor e contato
<span class="persona-cta">Kit de imprensa →</span>
</a>

<a class="persona-card advogado" href="INSTITUTIONAL.md" markdown>
<span class="persona-icone">⚖️</span>
**Advogada/o**
Base autônoma Art. 4º · vetores F6 e reserva de lei
<span class="persona-cta">Análise institucional →</span>
</a>

<a class="persona-card economista" href="formulario.md" markdown>
<span class="persona-icone">📐</span>
**Economista**
IC-F\* nas 3 formas · bem-estar · calibração R03
<span class="persona-cta">Formulário matemático →</span>
</a>

<a class="persona-card autoridade" href="procedimento_cade.md" markdown>
<span class="persona-icone">🏛️</span>
**Autoridade**
Tabela A/B/C · fluxograma processual · sensibilidade
<span class="persona-cta">Procedimento CADE →</span>
</a>

<a class="persona-card bigtech" href="compliance_corporativo.md" markdown>
<span class="persona-icone">🏢</span>
**Big Tech**
Aritmética R\$ · 4 vetores corporativos · DOJ-ATR
<span class="persona-cta">Compliance corporativo →</span>
</a>

<a class="persona-card academia" href="bem_publico.md" markdown>
<span class="persona-icone">🎓</span>
**Academia · sociedade civil**
LCMC sob Ostrom-Coleman-Olson · Prop. 5 refutada
<span class="persona-cta">Bem coletivo →</span>
</a>

</div>

---

**Fim do Ato 1.** A tese está posta: a cooperação interna é o bem coletivo; LCMC é o princípio; existem cinco instrumentos para internalizá-la, e o WaaS é apenas um. O Ato 2 destrincha cada um com aritmética em reais e os vetores onde o argumento pode quebrar.

[**▶ Ato 2: O mecanismo →**](mecanismo.md)

---

[![Licença: CC BY-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--SA%204.0-blue.svg)](https://github.com/freirelucas/waas-antitrust/blob/main/LICENSE) [![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/) [![Mesa 3.x](https://img.shields.io/badge/mesa-3.x-green.svg)](https://mesa.readthedocs.io/) [![364 testes](https://img.shields.io/badge/pytest-364%20passed-brightgreen)](https://github.com/freirelucas/waas-antitrust/actions) [![Brincar in-browser](https://img.shields.io/badge/brincar-in--browser-27AE60)](brincar.md)

Este repositório acompanha um **artigo acadêmico em elaboração** — *Leniency Conditional on Critical Mass: A Conditional-Deposit Channel for Unilateral Conduct in Digital Markets*. Não citar como resultado final. Veja `CITATION.cff` para metadados estruturados (Zenodo via release futura).
