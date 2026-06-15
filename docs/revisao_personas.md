# Revisão por personas — sessões simuladas

<p class="deck">Seis personas navegam pelo site a partir do hero do Ato 1 e relatam o que entenderam, o que confundiu e qual decisão tomariam. Documento usado para validar a atenuação editorial de jun/2026 e identificar pontos onde o argumento ainda não chega — ou chega de forma controversa.</p>

<p class="byline"><em>Revisão interna</em> · jun/2026 · simulações de leitura</p>

Cada persona descreve, em primeira pessoa, uma sessão típica: por onde
entrou, em quais páginas se demorou, o que registrou como compreensão e
o que ficou pendente. Não é teste com usuários reais — é exercício de
leitura crítica contra os perfis declarados em `docs/index.md` (linha
129-137). A finalidade é flagrar pontos onde o tom ou a estrutura ainda
falham.

## 📰 Jornalista — pauteira de Política, redação de Brasília

> Cheguei na home pela URL que alguém me mandou. O título "Quando a
> infração é unilateral, quem denuncia?" me prendeu — não é um título
> de paper, é uma pergunta jornalística. O lead acadêmico no parágrafo
> de abertura é mais sóbrio que esperava: cita Spagnolo-Harrington em
> tom indireto, situa o problema digital sem hiperbolizar. Os KPIs em
> cards brancos (R\$ 12,3 mi · 1.679 firmas · +1.363% · 364 testes) me
> deram dúvida no primeiro olhar porque o "+1.363%" parece propaganda;
> a legenda abaixo ("rodada multi-seed", "predição falsificável") salva
> o número. Anotei: **a percentagem precisa de uma fonte clicável**.
>
> Cliquei em [Kit de imprensa](imprensa.md) pelo menu. As três leads
> oferecidas funcionam: Política regulatória brasileira (CADE pode
> sozinho, sem nova lei), Comparação internacional (DOJ-ATR 2025 +
> DMA Tool 2024), e Política industrial (Big Tech vs PMEs). Achei o
> "transparencia.md" linkado no rodapé do KI uma jogada honesta —
> mostra os números e como recriá-los.
>
> **O que ficou pendente:** quem é "L."? A byline diz só a inicial. Pra
> citar em matéria preciso de nome completo, vinculação institucional
> (mesmo que ausente, dizer "pesquisador independente"), e foto. Isso
> tá no CITATION.cff mas não no site. Também queria uma quote pronta de
> 1 linha — "tese central" que dá pra encaixar em ombro de matéria.
>
> **Decisão:** publicaria. Mas como **proposta acadêmica**, não como
> "Brasil prestes a adotar". O tom da página ajuda — ninguém aqui
> promete que o CADE vai mexer.

## ⚖️ Advogada antitruste — escritório full-service, atende Big Tech

> Entrei direto em [INSTITUTIONAL.md](INSTITUTIONAL.md) pelo persona
> card. A página foi construída exatamente do meu jeito de ler: lista
> de fontes primárias verbatim (Lei 12.529, Res. 21/2018, Lei 9.784,
> Lei 13.608), depois separa "v3 lege lata" (Regime B) de
> "v3 lege ferenda" (Regime C). Fiquei satisfeita que separaram o
> que o CADE pode fazer hoje do que precisa de lei.
>
> O ponto sensível pra mim — e que eu testaria em juízo se cliente
> me pedisse — é o **falsificador F6**: a re-caracterização da
> recompensa do Art. 12 como ressarcimento. O paper e o site reconhecem
> que isso é controvertível e que a base autônoma (Art. 4º II/III)
> é o que sobrevive se F6 cair. Isso é honesto.
>
> Em [limitacoes.md](limitacoes.md) o "Caveat F6 explícito" e
> "Caveat reserva de lei" aparecem sem retoricar — apenas listam os
> riscos. Bom sinal.
>
> **O que ficou pendente:** a doutrina brasileira citada é magra. Só
> menção indireta. Onde está Forgioni, Salomão Filho, Calixto Salomão
> sobre Art. 4º? Cadê o Ferraz Junior sobre reserva legal? Sem isso,
> não posso usar a página como referência em razões finais.
>
> **Decisão:** **utilizo como insumo**, não como autoridade. Citaria
> em parecer interno indicando "proposta acadêmica que merece
> consideração". Levaria ao sócio de Concorrencial.

## 📐 Economista — pesquisador em economia industrial

> Entrei em [formulario.md](formulario.md) procurando a IC-F\* e
> achei rápido. As três formas (simplificada / Hirschman / LCMC) estão
> com derivação curta e calibração contra Saito 2021. O §4.1 "Desconto
> progressivo por classe na janela de adesão (R29)" estabelece
> $\mathbb{E}[W \mid \text{aderir em } k] = W_{\max} \cdot f_W^{\text{adesão}}(k)$
> e mostra o corte endógeno $k^\star$. Coerente.
>
> Em [transparencia.md](transparencia.md), o que mais me impressionou
> foi a tabela de **alvos de calibração** com status (R03 fechou alvo
> único; alvos 2 e 3 abertos por identificabilidade). Honestidade
> empírica acima da média do que costumo ver em paper de ABM.
>
> Rodei o [simulador in-browser](brincar.md) — não pra obter número,
> mas pra checar se o gradient W_mult faz o que prediz. Funciona: com
> W_mult=0 e canal ligado, a curva de violadoras ainda cai (cooperação
> ética dos arquétipos). Isso confirma a leitura "canal de coordenação
> ≠ canal de pagamento".
>
> **O que ficou pendente:** o bem-estar agregado é construído como
> $-(\text{dano} + \beta \cdot FP)$ com $\beta$ ainda provisório. Quero
> ver a análise de sensibilidade a $\beta$ — está em algum lugar?
> O `pyproject.toml` não menciona `pytest-cov`, então a cobertura
> linha-a-linha do `model.step()` não está medida.
>
> **Decisão:** rodaria o Sobol full localmente (1024 base) antes de
> usar os números em paper meu. O simulador in-browser serve para
> apresentação, não para citação.

## 🏛️ Conselheiro do CADE — Tribunal Administrativo

> Entrei em [procedimento_cade.md](procedimento_cade.md) buscando o
> fluxograma. Está lá: 7 etapas do recebimento ao TCC, com referência
> ao Art. 4º II/III da Lei 12.529 como base. A sensibilidade ao $N^\star$
> ≈ 1.679 firmas é uma predição empírica testável contra nosso
> universo de jurisdicionados — número plausível, ordem de grandeza
> correta.
>
> O que me incomoda: a página assume que **uma Resolução do CADE basta**
> para implementar o canal. Talvez. Mas o procedimento de denúncia
> condicional, com prazo, sigilo e *escrow*, não está endereçado pelo
> regramento atual. Precisaria de uma Resolução específica — não da
> 21/2018 — e da CGAA assinaria que o canal cabe dentro da estrutura
> administrativa atual sem prejudicar a celeridade.
>
> Em [internacional.md](internacional.md), o R30 (sinergia entre
> autoridades) chamou minha atenção como leitura, mas é prematura
> politicamente. Não estamos em condições de MoU operacional novo com
> DOJ-ATR no ciclo 2024-2027. A consolidação cross-jurisdicional
> presume coordenação que hoje não existe.
>
> **O que ficou pendente:** **dosimetria**. Como o gradiente Saito da
> R20 dialoga com a dosimetria do Art. 45 da Lei 12.529? O texto fala
> em "calibração" mas não em "compatibilidade dosimétrica". Sem isso,
> a Coordenação de Dosimetria não compra a proposta.
>
> **Decisão:** vale **leitura técnica** pela Superintendência Geral.
> Não vejo decisão administrativa no horizonte 2024-2027, mas como
> insumo de estudo da casa, sim.

## 🏢 Compliance Officer — Big Tech, área-fim antitruste

> Entrei em [compliance_corporativo.md](compliance_corporativo.md) e a
> primeira coisa que vi foi o aviso vermelho "Leitura especulativa, não
> aconselhamento jurídico". Bom: define expectativa.
>
> A aritmética em R\$ 1 bilhão de receita está bem feita — assume
> sanção esperada $p \cdot S$ vs custo de pagamento $W$ e mostra IC-F\*
> com margem D−W. O argumento "TCC com ressarcimento é margem
> positiva para a firma" funciona sob a hipótese ($p$ subiu via canal),
> mas isso requer que o canal **funcione** — pressuposto que minha
> firma não controla.
>
> O cenário [`uso_adversarial_oportunista`](compliance_corporativo.md)
> me preocupa profissionalmente. Quem garante que ex-funcionário com
> rancor não usa o canal pra forjar denúncia? O modelo cobre isso (R24
> + arquétipo oportunista), mas o resultado de simulação mostra
> "densidade de FP cresce quando >20% são oportunistas". Em compliance
> isso vira política de retenção crítica.
>
> Em [mecanismo.md](mecanismo.md) Camada 5 (R29 janela de adesão), a
> cascata pós-abertura é o que **mais me preocupa**: se 10% da
> engenharia depositar, mais 20% adere na janela. Trinta porcento dos
> engenheiros falando contra a empresa em 10 trimestres — isso
> reorganiza todo o programa de integridade interno.
>
> **O que ficou pendente:** **resposta jurídica defensiva**. Se a
> proposta passa, quais cláusulas contratuais (anti-disparagement,
> arbitragem obrigatória, acordo de confidencialidade) ficam
> juridicamente frágeis? O `compliance_corporativo.md` não responde —
> deveria.
>
> **Decisão:** **monitorar**. Levar à reunião mensal do comitê de
> antitruste. Não é alarme imediato; é mudança de cenário de fundo.

## 🎓 Pesquisadora acadêmica — pós-doc, sociologia da regulação

> Vim por [bem_publico.md](bem_publico.md) (link do persona card) e
> achei a moldura Olson-Ostrom-Coleman bem trabalhada. A Proposição 5
> candidata (erosão Coleman) **falsificada na forma forte** com varredura
> 10 sementes × 8 alphas é a melhor parte do site para mim — falsificação
> empírica de uma proposição candidata é prática de Lakatos, raríssima
> em paper de ABM.
>
> Em [colaborar.md](colaborar.md) os pontos de entrada explícitos para
> três comunidades (sociólogos da coordenação, cientistas políticos,
> behavioral ethicists) abrem caminho concreto. As 4 receitas de
> contestação ("contestar a calibração de Saito", "elevar
> alpha_erosao", "implementar arquétipo adversarial", "rodar Sobol
> com seus parâmetros") são endereços de pesquisa real, não convite
> simbólico.
>
> A nota em [`brainstorm_revisao.md`](brainstorm_revisao.md) §5 lista
> três direções de pesquisa que pretendo perseguir: recompensa
> coletiva como salvaguarda anti-erosão, equilíbrio bayesiano-perfeito
> sob heterogeneidade, e uso adversarial coordenado.
>
> **O que ficou pendente:** **DOI Zenodo** — preciso citar formalmente.
> O `.zenodo.json` está como stub. Sem DOI, vai pro working paper
> draft, não pra publicação revisada por pares com referência.
>
> **Decisão:** **colaborar**. Escrevo ao autor pelo e-mail no
> CITATION.cff propondo co-autoria em uma extensão (recompensa
> coletiva + erosão Coleman acoplada).

## Síntese das 6 sessões

| Persona | Decisão | Maior obstáculo |
|---|---|---|
| 📰 Jornalista | Publicaria como proposta acadêmica | Identidade da autora (só inicial "L.") |
| ⚖️ Advogada | Insumo, não autoridade | Doutrina brasileira citada é magra |
| 📐 Economista | Roda Sobol full localmente | Sensibilidade a β do bem-estar |
| 🏛️ Conselheiro CADE | Leitura técnica pela SG | Compatibilidade dosimétrica Art. 45 |
| 🏢 Compliance Big Tech | Monitorar | Cláusulas contratuais defensivas |
| 🎓 Acadêmica | Colaborar | DOI Zenodo formal |

**Pontos convergentes entre 3+ personas:**

1. **Autoria** — Jornalista e Acadêmica registram explicitamente que
   a identificação só por "L." é obstáculo prático. Ver
   [CITATION.cff](https://github.com/freirelucas/waas-antitrust/blob/main/CITATION.cff)
   pode resolver, mas o site não expõe.
2. **Calibrações abertas** — Economista, Conselheiro e Compliance
   notam pontos de calibração faltante: β do bem-estar; capacidade
   institucional; gradiente Saito por conduta unilateral; ligação
   dosimétrica Art. 45.
3. **Aplicação operacional** — Conselheiro e Compliance ambos
   sinalizam que a passagem do "modelo formal" para "operação
   institucional concreta" tem gap: o que falta para o CADE realmente
   poder receber denúncia condicional amanhã? Quais cláusulas
   contratuais ficam afetadas?

Esses três pontos convergentes viram **entradas de gravidade média**
no [`brainstorm_revisao.md`](brainstorm_revisao.md):

- §6 → adicionar "**Autoria visível no site**" (rodapé do hero ou
  página /sobre).
- §5 → "**β do bem-estar como parâmetro com sensibilidade exposta**".
- §3 → "**Página `/operacional` — do modelo formal à Resolução CADE**"
  (pendência atual: `procedimento_cade.md` é leitura formal, não
  operacional).

---

Este documento é mais uma camada de revisão interna; não substitui
teste com usuários reais.
