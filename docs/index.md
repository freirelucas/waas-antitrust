# Quando a infração é unilateral, quem denuncia?

**Ato 1 de 5 · O problema**

A leniência clássica acabou de bater num muro. Em mercados digitais, a infração é **de uma firma só** — não há cúmplice para delatar. A informação existe nos times de produto, engenharia e *corp dev*, mas o trabalhador que falaria arrisca tudo e ganha nada. Esta é a história de uma proposta para destravá-la.

[**▶ Ato 2: O mecanismo**](mecanismo.md) ·
[🧪 Brincar com o modelo](brincar.md) ·
[📄 Paper](paper.md)

| R\$ 12,3 mi | 1.679 firmas | +1.363% | 343 testes |
|:---:|:---:|:---:|:---:|
| **margem da firma sob TCC-WaaS** para receita de R\$ 1 bi | **universo CADE implícito** após calibração formal R03 | **ΔW de Regime B sobre A** em bem-estar agregado | **verdes em ~25s** · 21 figuras reproduzíveis |

> *A resposta não está em incentivar a empresa nem em recompensar denúncia isolada. Está em dar ao CADE um **canal de depósito condicional** onde a denúncia individual só se abre quando há massa crítica de cooperadores — eliminando "ninguém quer ser o primeiro".*

## A leniência clássica acabou de bater num muro

Por quase trinta anos, programas de leniência foram a peça-mestre do enforcement antitruste. A lógica é simples: dois ou mais conspiradores fizeram um cartel; quem entregar primeiro escapa da multa. **O cartel se denuncia sozinho** — é a beleza do desenho.

Em mercados digitais, no entanto, o abuso costuma vir de **uma única empresa** — sem cúmplice externo para delatar. Quatro exemplos do noticiário recente:

- O Google rebaixando concorrentes em buscas para favorecer o próprio comparador de preços (*self-preferencing*).
- A Apple proibindo que o app Spotify mencione opções de pagamento fora da App Store (*anti-steering*).
- O iFood mantendo cláusulas de exclusividade que impedem restaurantes de operar com concorrentes.
- O Facebook (Meta) comprando o Instagram para neutralizar uma plataforma rival emergente (*killer acquisition* — aquisição cujo propósito é eliminar o concorrente, não absorvê-lo).

A informação sobre essas práticas existe **dentro da própria empresa** — em conversas no Slack, na ata da reunião do comitê de produto, no slide-deck do time de aquisições. Mas ela não chega ao CADE. No Brasil de hoje, o trabalhador que falaria arrisca emprego, carreira, tranquilidade — e ganha **nada de previsível** em troca.

<div class="pull-quote" markdown>
A leniência só funciona quando há cumplicidade entre firmas. Quando a infração é unilateral, é como esperar que o ladrão se entregue porque tem medo do espelho.
</div>

## A resposta deste projeto: LCMC como canal de depósito condicional

Em mercados digitais com **fosso competitivo profundo** (uma plataforma dominante cercada de barreiras estruturais — efeitos de rede, dados acumulados, integração vertical — que tornam a entrada de concorrente quase impossível), a cumplicidade na infração existe **dentro da própria empresa**: entre os times de engenharia, produto, jurídico e aquisições. O problema central não é "como punir a firma" nem "como pagar o denunciante" — é **como resolver a coordenação dos trabalhadores que veem a conduta mas não querem brigar a luta sozinhos**.

A proposta deste projeto, em uma frase:

!!! tip "LCMC — canal de depósito condicional"

    O **CADE opera um canal qualificado de recepção de denúncias** com cláusula de abertura condicional. O trabalhador entrega ao CADE sua denúncia com prova específica e diz: *"esta denúncia só é instaurada se houver ao menos `q_min · n` outros trabalhadores do mesmo setor/firma que também depositarem denúncias compatíveis dentro de uma janela `Δt`"*. As denúncias ficam em **escrow** — não notificam a firma, não viram processo, não vazam — até que o gatilho de massa crítica seja atingido. Quando o é, **todas se abrem simultaneamente**: ninguém foi o primeiro isoladamente.

A LCMC é **mecanismo de coordenação**, não de pagamento. Resolve diretamente um problema clássico estudado por Mancur Olson em 1965: em grupos pequenos, ninguém quer ser o primeiro a se expor; cada um prefere esperar o outro começar. O canal de depósito condicional **elimina esse impasse por construção** — a denúncia individual nunca fica exposta sozinha enquanto a massa crítica não se forma.

Para entender de onde vem essa ideia, três paralelos do cotidiano. Cada um descreve a mesma estrutura por um ângulo diferente:

=== ":material-rocket-launch: Kickstarter"

    Quando você apoia um projeto no Kickstarter, seu cartão **só é cobrado se o projeto atingir a meta** de apoiadores. Se a meta não é atingida, ninguém paga e nenhum projeto começa.

    A LCMC funciona igual, mas com denúncias: a sua denúncia só "cobra" — vira processo no CADE — se outros trabalhadores da mesma empresa também depositarem. Se não houver coincidência suficiente, ninguém é exposto e nenhum processo se abre.

    É o desenho *all-or-nothing*: ou todos cooperam e o projeto sai, ou ninguém é exposto financeiramente.

=== ":material-shield-account: Callisto"

    [Callisto](https://www.callisto.org) é uma plataforma americana em operação **desde 2015** onde estudantes universitárias registram denúncias de assédio sexual.

    O nome de uma vítima só é revelado se **outra** vítima identificar o **mesmo** agressor. Sem coincidência, o registro permanece anônimo. Coincidência libera; isolamento mantém anonimato.

    É a prova prática de que o desenho funciona em produção, não só em paper. A LCMC adapta o mesmo padrão para denúncia antitruste.

=== ":material-treasure-chest: Caixa-cofre"

    Imagine envelopes com denúncias entregues a uma caixa-cofre operada por uma instituição neutra — no nosso caso, o CADE.

    Cada envelope vem com a instrução: *"abra esta caixa apenas quando houver ao menos N envelopes parecidos contra a mesma empresa"*. A caixa pode esperar meses. Quando atinge N, **todos** os envelopes se abrem juntos.

    Ninguém foi o primeiro a se expor. A LCMC implementa esta caixa-cofre no procedimento administrativo do CADE.

O nome acadêmico desse desenho é **escrow de informação condicional** ou *information escrow* — formalizado por Ian Ayres e Cait Unkovic (Yale Law School) em artigo de 2012 na *Michigan Law Review*, vol. 111, p. 145. A LCMC aplica este desenho ao antitruste brasileiro, com o CADE como o "terceiro confiável" que opera a caixa-cofre.

## O que vem depois da abertura — instrumentos

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

## A figura central do projeto

A figura abaixo é a **saída literal** de uma execução do modelo computacional. Não é estilizada — vem do `WaaSModel.executar()`, *seed* 11, regimes A/B/C lado a lado.

<figure markdown>
  ![Dissuasão endógena e bem-estar — 3 regimes ao longo de 40 trimestres](img/03_dissuasao_bem_estar.png){ .figura-empirica }
  <figcaption>
    <strong>(A)</strong> Violadoras ativas ao longo do tempo. Regime A (cinza) cresce e estabiliza alto;
    regimes B/C (verde/roxo) caem a zero em ~17 tiques. <strong>(B)</strong> Bem-estar social agregado.
    ΔW (B sobre A) = +1363%. <br><br>
    <em>Leitura sob LCMC corrigida:</em> a queda de violadoras em B/C é resultado de <strong>denúncias coletivas
    abrindo do escrow</strong>. Cada vez que o canal abre, o sinal Schelling se propaga (detecção percebida
    sobe em todas as firmas). O instrumento WaaS está ativo nas curvas verdes/roxas como incentivo
    incremental à adesão ao canal — não é a causa primeira da queda.
  </figcaption>
</figure>

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
          "valor_dissuasao_difusa_acum", "capital_social_residual",
          "bem_estar"]].tail())

# Inspeção micro: arquétipos sorteados, papéis, posições na fila intra-firma
for t in m.trabalhadores_por_empresa[0][:5]:
    print(f"  {t.arquetipo:13s} · papel={t.papel:9s} · sinalizou={t.sinaliza_agora}")
```

A simulação produz 288 reporters em 40 colunas de pandas. Tudo é inspecionável; nada está escondido em variáveis privadas opacas. Ver [Modelagem multiagente](modelagem_multiagente.md) para a anatomia das três classes (`TrabalhadorAgent`, `EmpresaAgent`, `AutoridadeAgent`).

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

## Por onde seguir — entrada por papel profissional

<div class="grid cards" markdown>

-   :material-newspaper-variant-outline:{ .lg .middle } **Jornalista**

    ---

    O lead em 30s, comparação BR × EUA × UE em uma figura, autor e contato. Sem jargão jurídico em primeira linha.

    [:octicons-arrow-right-24: Kit de imprensa](imprensa.md) · [Generalidade EUA/UE](internacional.md)

-   :material-scale-balance:{ .lg .middle } **Advogado · advogada**

    ---

    Litígio: vetores atacáveis (F6, reserva de lei, custo legal). Público: base autônoma Art. 4º + Lei 9.784/99. Compliance: implicações corporativas.

    [:octicons-arrow-right-24: Análise institucional](INSTITUTIONAL.md) · [Limitações §jurídica](limitacoes.md)

-   :material-calculator-variant-outline:{ .lg .middle } **Economista**

    ---

    IC-F\* nas 3 formas, bem-estar, calibração formal R03 em $(0{,}323; 0{,}481)$. Reprodução com seeds explícitas e bootstrap CI.

    [:octicons-arrow-right-24: Formulário matemático](formulario.md) · [Transparência](transparencia.md)

-   :material-shield-key-outline:{ .lg .middle } **Autoridade**

    ---

    Decisor (CADE/PFE): tabela A/B/C com status normativo e base autônoma. Operacional (SG): fluxograma processual. Técnico (DEE): calibração com sensibilidade a N\*.

    [:octicons-arrow-right-24: Análise institucional](INSTITUTIONAL.md) · [Procedimento (CADE)](procedimento_cade.md)

-   :material-domain:{ .lg .middle } **Big Tech**

    ---

    Aritmética em R\$ por receita da empresa, arquitetura do modelo, exposição esperada. Cenário canônico EUA DOJ-ATR para comparação direta com Dodd-Frank §922.

    [:octicons-arrow-right-24: Mecanismo](mecanismo.md) · [Compliance corporativo](compliance_corporativo.md) · [Brincar](brincar.md)

-   :material-school-outline:{ .lg .middle } **Academia · sociedade civil**

    ---

    LCMC sob lente Ostrom-Coleman-Olson. Falsificação numérica da Prop. 5 forte. 19 figuras com seeds reproduzíveis. Como contestar em código.

    [:octicons-arrow-right-24: Bem coletivo](bem_publico.md) · [Como contestar](colaborar.md)

</div>

<div class="ato-fim" markdown>
**Fim do Ato 1.** A tese está posta: a cooperação interna é o bem coletivo; LCMC é o princípio; existem cinco instrumentos para internalizá-la, e o WaaS é apenas um. O Ato 2 destrincha cada um com aritmética em reais e os vetores onde o argumento pode quebrar.

[Ato 2: O mecanismo →](mecanismo.md)
</div>

---

<small>
[![Licença: CC BY-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--SA%204.0-blue.svg)](https://github.com/freirelucas/waas-antitrust/blob/main/LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Mesa 3.x](https://img.shields.io/badge/mesa-3.x-green.svg)](https://mesa.readthedocs.io/)
[![331 testes](https://img.shields.io/badge/pytest-331%20passed-brightgreen)](https://github.com/freirelucas/waas-antitrust/actions)
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_demo.ipynb)

Este repositório acompanha um **artigo acadêmico em elaboração** —
*Critical Mass as a Quasi-Public Good in Antitrust Enforcement of Digital Markets*. Não citar como resultado final. Veja `CITATION.cff` para metadados estruturados (Zenodo via release futura).
</small>
