<span class="ato-chip">Ato 1 de 5 · O problema</span>

# E se a empresa pagasse para ser delatada?

<div class="hero" markdown>

Em mercados digitais, a maior parte do abuso de poder é cometida por **uma empresa só**. Não há cúmplice para entregar; o conluio interno mora dentro do organograma. A leniência clássica — desenhada para cartéis de duas ou mais empresas — não tem como morder este tipo de conduta. Quem realmente vê o que acontece são os **próprios funcionários**, e hoje nada dá a eles motivo para falar.

Este projeto é uma tentativa de **inverter o cálculo**: e se, sob certas condições jurídicas brasileiras já existentes, a empresa investigada visse vantagem em **pagar uma recompensa** aos seus denunciantes internos — porque o desconto que ela receberia no acordo (TCC) seria maior do que essa recompensa?

</div>

![Saída real do modelo: com o canal WaaS (B/C) as firmas param de violar ao longo do tempo e o bem-estar social supera o cenário atual (A).](img/03_dissuasao_bem_estar.png){ .figura-empirica }

## A leniência clássica acabou de bater num muro

Por quase trinta anos, programas de leniência foram a peça-mestre do enforcement antitruste no mundo todo. A lógica é simples: dois ou mais conspiradores fizeram um cartel; quem entregar primeiro escapa da multa. Cada conspirador olha para o outro, calcula que ele pode entregá-lo a qualquer momento, e corre para a delação. O cartel **se denuncia sozinho** — é a beleza do desenho.

Mas o abuso de mercado digital costuma ter **uma única empresa**. A *self-preferencing* do Google, o *anti-steering* da Apple, o *vesting* exclusivo do iFood, o *killer acquisition* da Meta. Nenhum desses casos tem uma segunda empresa cúmplice para delatar — a conduta é executada pela própria firma dominante, pelos seus próprios times.

A informação existe. Está nos *commits* do engenheiro que codificou o algoritmo de ranking. Está nas *slides* da reunião onde o gerente comercial impôs a exclusividade. Está no *deck* do *corp dev* que comprou a startup-ameaça. Mas essa informação não circula porque os incentivos individuais estão errados — o trabalhador que fala arrisca o emprego, a carreira, a tranquilidade, e ganha o quê em troca? Nada de previsível, pelo menos no Brasil.

<div class="pull-quote" markdown>
A leniência só funciona quando há cumplicidade entre firmas. Quando a infração é unilateral, é como esperar que o ladrão se entregue porque tem medo do espelho.
</div>

## A oportunidade brasileira está dentro de uma regra que já existe

A maior parte do trabalho institucional para este projeto **já está feita** — só não foi conectada nestes termos.

O **Art. 12 da Resolução CADE nº 21/2018** autoriza considerar o ressarcimento das vítimas como circunstância atenuante no cálculo da contribuição pecuniária do Termo de Compromisso de Cessação (TCC). A jurisprudência interna do CADE entende esse ressarcimento como uma redução real e quantificável da multa que a empresa teria de pagar.

A hipótese deste projeto é direta: **a recompensa paga pela empresa aos seus denunciantes internos pode ser re-caracterizada como ressarcimento extrajudicial sob o Art. 12**. Se for, gera o atenuante. Se o atenuante for grande o suficiente, **a empresa prefere pagar a recompensa a esconder a infração** — porque o desconto que ela ganha no TCC é maior do que o cheque que assina para os denunciantes.

Esta re-caracterização não é pacífica — ela é a charneira controvertida do mecanismo, e a página de [Limitações](limitacoes.md) é honesta sobre isso. Mas é uma porta institucional **que já existe**, sem precisar passar pelo Congresso.

## Três cenários, do conservador ao ambicioso

| Regime | O denunciante interno é recompensado? | Como seria implementado |
|--------|---------------------------------------|-------------------------|
| **A** — hoje | Não | situação atual: sem canal de incentivo individual |
| **B** — via Resolução | Sim | nova resolução CADE complementar à 21/2018, **sem mudar a lei** |
| **C** — via Lei | Sim | extensão da Lei 13.608/2018 ao antitruste — mais robusto, exige o Congresso |

O **Regime B** é a aposta política deste projeto: usar o que o CADE pode fazer sozinho. O **Regime C** é a versão jurídicamente mais robusta — também simulada, e mais defensável em juízo. O **Regime A** é o contrafactual: o que continua acontecendo se nada mudar.

## Por onde seguir nesta história

<div class="grid cards" markdown>

-   **Sou cético — me convença**

    A pergunta direta — "mas o que impede a empresa de pegar o desconto sem pagar?" — respondida com fórmulas, exemplo numérico em reais e três vetores de quebra modelados.

    [Ato 2: Como o mecanismo se sustenta →](mecanismo.md)

-   **Quero ver os resultados**

    O que a simulação de 20 firmas e 40 trimestres mostra sob cada regime. Figuras, médias, intervalos de confiança 95% sobre múltiplas seeds.

    [Ato 3: Resultados →](resultados.md)

-   **Sou jurista / formulador(a)**

    Como o mecanismo caberia nas Leis 12.529 e 13.608, na Resolução 21/2018, e onde fica a fragilidade da reserva de lei (Art. 22, I, CF).

    [Análise institucional →](INSTITUTIONAL.md)

-   **Quero contribuir / discutir**

    O modelo é código aberto sob CC BY-SA 4.0. Há pendências de calibração e cinco decisões normativas em aberto. Convido a discussão.

    [Como usar](uso.md) · [Backlog](DECISIONS.md) · [Crítica x10](critica_x10.md)

</div>

<div class="ato-fim" markdown>
**Fim do Ato 1.** A pergunta está posta: existe um desenho jurídico-econômico que faça a empresa **escolher** ser denunciada? A resposta detalhada, com aritmética e nomes de variáveis, está no próximo ato.

[Ato 2: Como o mecanismo se sustenta →](mecanismo.md)
</div>

---

<small>
[![Licença: CC BY-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--SA%204.0-blue.svg)](https://github.com/freirelucas/waas-antitrust/blob/main/LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Mesa 3.x](https://img.shields.io/badge/mesa-3.x-green.svg)](https://mesa.readthedocs.io/)
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_demo.ipynb)

Este repositório acompanha um **artigo acadêmico em elaboração** —
*Rescaling Leniency Programs for Digital Markets: A Whistleblower-as-a-Service Mechanism*. Não citar como resultado final. Veja [Citação](#) no
`CITATION.cff` para metadados estruturados (Zenodo via release futura).
</small>
