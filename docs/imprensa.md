# Kit de imprensa

Página para jornalistas que precisam compreender o projeto em **dois minutos** e ter
um lead em **trinta segundos**. Os números têm fonte primária citada em
[`REFERENCES.md`](REFERENCES.md); a postura epistêmica está em
[`transparencia.md`](transparencia.md).

---

## Três leads (escolha pela editoria)

### Lead 1 — Política regulatória brasileira

> **O CADE pode criar um canal de denúncia premiada antitruste sem pedir nova lei
> ao Congresso.** Um projeto acadêmico independente argumenta que o Art. 4º da Lei
> 12.529/2011 c/c a Lei 9.784/99 (procedimento administrativo) basta como base legal
> para a autoridade operar um *information escrow* — onde o trabalhador deposita a
> denúncia que só se abre quando outros funcionários da mesma firma também depositarem
> (massa crítica). A recompensa monetária pode ser re-caracterizada como ressarcimento
> sob o Art. 12 da Resolução CADE 21/2018 — controvertido, mas defensável.

### Lead 2 — Comparação internacional

> **Os EUA criaram em julho de 2025 o primeiro programa federal de recompensa a
> denunciante antitruste, sem lei nova: o DOJ-ATR Whistleblower Rewards Program (em
> parceria com o USPS) paga 15% a 30% sobre multas acima de US\$ 1 milhão.** O
> primeiro prêmio — US\$ 1 milhão — foi pago em janeiro de 2026. A União Europeia
> lançou em abril de 2024 a DMA Whistleblower Tool, mas **sem** componente de
> recompensa. Um projeto acadêmico brasileiro defende que o desenho americano é
> transplantável ao Brasil sob a Resolução CADE 21/2018, sem necessidade de lei
> nova — replicando o caminho infralegal.

### Lead 3 — Mercados digitais e moat

> **A leniência clássica não funciona em condutas antitruste unilaterais — que são
> exatamente as que dominam mercados digitais.** Quando uma plataforma sozinha
> auto-preferencia seu produto, recusa interoperabilidade ou faz uma aquisição
> matadora, não há cartel para delatar: o conhecimento mora dentro da firma, em 2-3
> papéis técnicos. Um projeto acadêmico propõe um canal de depósito condicional
> operado pelo CADE — *information escrow* análogo ao Callisto (universitário, EUA,
> assédio sexual) — onde as denúncias só se abrem quando atingem massa crítica
> intra-firma, resolvendo o jogo de coordenação que mantém o silêncio.

---

## Os números

| Número | Origem |
|---|---|
| **109** acordos de leniência em 20 anos do CADE | Comunicado CADE, out/2023 |
| **47** TCCs assinados por ano em média (2012–2019) | Saito 2021 §3.7.7 (349 TCCs) |
| **43,43%** desconto médio para 1º cooperador no SG/CADE | Saito 2021 §3.7.7 |
| **180** servidores na área-fim do CADE (2024) | RIG/TCU 2024 |
| **15–30%** recompensa do DOJ-ATR sobre multas ≥ US\$ 1 mi | DOJ-ATR Rewards Program, jul/2025 |
| **1.679** firmas — universo CADE implícito após calibração | Calibração formal R03 do projeto (predição falsificável) |

---

## Aritmética em reais (para o leitor não-técnico)

Para uma plataforma com **receita anual de R\$ 1 bilhão** no Brasil, em uma conduta
unilateral típica (auto-preferência, p. ex.), com multa esperada de 5% da receita
($\sigma = 0{,}05$):

- **Sanção esperada:** R\$ 50 milhões.
- **Desconto WaaS via TCC (D = 30%):** R\$ 15 milhões (firma economiza).
- **Recompensa do denunciante (W = 1,5 × salário anual × ~10 trabalhadores):**
  R\$ 2,7 milhões.
- **Margem para a firma:** R\$ 12,3 milhões (vale a pena assinar o TCC).

O cálculo detalhado, com os 3 cenários de quem paga o custo legal e os 3 vetores de
quebra (TCC clássico já dá o desconto; Judiciário anula; custo legal proíbe), está
em [`mecanismo.md` Camada 4](mecanismo.md#camada-4-a-aritmetica-da-ic-f-sob-instrumento-waas).

---

## O que perguntar

Para uma matéria mais aprofundada:

1. **Sobre o autor.** O projeto é mantido **independentemente** por L., sem
   vinculação institucional formal a CADE, IPEA, ou Big Tech. Resposta em
   [`colaborar.md`](colaborar.md) e em `CITATION.cff` (raiz do repositório).
2. **Sobre a viabilidade política.** A página
   [`viabilidade_regime_c.md`](viabilidade_regime_c.md) diagnostica em
   detalhe o cenário 2024-2027 — Regime C ("via lei nova") provavelmente é
   infactível sem crise reputacional grande; Regime B ("via Resolução") é a aposta.
3. **Sobre a falsificação.** [`limitacoes.md`](limitacoes.md) lista os
   5 vetores de quebra do modelo com parâmetro e teste de regressão — incluindo o
   achado negativo de jun/2026: a Proposição 5 candidata (sobre erosão Coleman)
   foi **falsificada na forma forte** na simulação multi-seed.

---

## Contato + licença + citação

- **Licença**: código e documentação sob CC BY-SA 4.0; código sob MIT no `pyproject.toml`.
- **Citação**: ver `CITATION.cff` na raiz do repositório (release Zenodo pendente).
- **Contato**: via [GitHub Issues](https://github.com/freirelucas/waas-antitrust/issues) ou pull request.
  Email institucional não publicado por desenho — o canal preferido é público.

---

## Disclaimer

O autor **não é** porta-voz do CADE nem de qualquer outra autoridade brasileira. O
projeto é proposição acadêmica, não documento institucional. Citações verbatim da
Resolução 21/2018 estão sujeitas à verificação contra o Diário Oficial (pendência
empírica E04 em [`DECISIONS.md`](DECISIONS.md)).
