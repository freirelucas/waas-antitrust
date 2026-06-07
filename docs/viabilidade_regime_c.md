# Viabilidade política do Regime C (2024-2027)

Esta página responde a uma crítica direta do **Cientista Político** na
[Crítica x10 v2](critica_x10_v2.md): a premissa do projeto de que o
Regime C tem "custo político mais alto, mas viável" subestima
materialmente o custo no horizonte 2024-2027.

## A configuração política em 2024-2026

Três fatos institucionais convergem para tornar a janela legislativa
estreita:

1. **PL 2768/2022 parado.** O análogo brasileiro ao DMA europeu (regulação
   econômica concorrencial de plataformas digitais) está sem movimentação
   desde 2023. A última audiência pública foi em maio/2023; pareceres de
   relatoria não tramitaram. O projeto está em quatro comissões da Câmara
   sem cronograma definido.
2. **Agenda econômica concentrada.** A pauta dominante na Câmara em
   2024-2026 é reforma tributária (LC 214/2025), arcabouço fiscal,
   desoneração e (em 2026) ajustes pós-eleitorais. Antitruste digital é
   matéria periférica; concorre por slots de comissão com temas que
   mobilizam mais bases.
3. **Fragmentação partidária.** A Câmara 2023-2026 tem 19 partidos com
   representação; agenda específica de antitruste digital não tem
   partido-padrinho claro. Sem campeão político, projetos técnicos
   tendem a ser arquivados.

## O que isso implica para o paper

A linguagem atual do projeto trata Regime C como **caminho
institucionalmente sólido com custo político maior** — sugerindo que é
desejável mas atingível com esforço político médio. A crítica do
Cientista Político recoloca o quadro: Regime C **provavelmente é
infactível** no horizonte 2024-2027, salvo crise reputacional de grande
escala. O Apple Brasil TCC (dez/2025) pode mover marginalmente, mas não
abrir janela.

Implicações:

- O cenário `lei_waas_pura` em `cenarios.py` (Regime C) precisa ganhar
  um caveat narrativo: "exploratório, condicional a janela política
  futura". Não é mudança de código — é honestidade documental.
- A comparação Regime B vs Regime C nos resultados (figura
  `03_dissuasao_bem_estar.png`) passa a ler-se como **comparação entre
  o que pode ser feito agora (B, com fragilidade jurídica F6) e o que
  seria desejável** (C, condicional a abertura de janela).
- A advocacy política natural do projeto se desloca: em vez de
  "convencer o Congresso a estender a Lei 13.608", vira "convencer
  o CADE de que B é institucionalmente defensável até C virar
  factível".

## Adv B v2 — Regime C não é monolítico

A crítica do Adv B v2 acrescenta uma dimensão: os instrumentos novos
(crédito tributário R22, leniência criminal individual R23) exigem
reservas constitucionais distintas. O Regime C precisa decompor em
sub-regimes:

- **Cₜ trabalhista** — lei ordinária Art. 22 I para cláusula contratual
  de vesting acelerado padrão. Hospeda instrumento Hirschman.
- **Cᵩ tributária-LC** — lei complementar Art. 146 + lei ordinária
  específica Art. 150 §6º + LRF Art. 14 para crédito tributário ao
  denunciante. Tramitação mais complexa que C ordinária.
- **Cₚ penal** — lei ordinária com reserva penal estrita Art. 5º XXXIX
  para leniência criminal individual. Conflito imediato com Art. 86
  da Lei 12.529/2011 (que protege empresa+colaboradores-do-acordo,
  não empregado-terceiro).

A janela política de Cₜ é mais aberta que Cᵩ ou Cₚ — vesting acelerado
toca o discurso de "proteção do trabalhador" e pode encontrar relatoria
em comissões trabalhistas. Cᵩ e Cₚ são casos mais difíceis: o primeiro
exige consenso fiscal; o segundo exige debate criminal sensível.

## Conclusão epistêmica

A viabilidade política do Regime C é uma **conjectura aberta** que o
projeto trata com cautela. A simulação serve para mostrar **o que
acontece se** o Regime C ocorrer; **se** ocorrer, é decisão política
que excede o escopo do paper. Marca-se como limitação no
[Ato 4 (Limitações)](limitacoes.md) e como caveat narrativo nos
cenários de Regime C.
