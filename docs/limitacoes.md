# Limitações

Este é um **artigo em elaboração**. A página resume, em linguagem acessível, o
que ainda **não** está plenamente sustentado — para que nada seja lido como
conclusão definitiva. O backlog técnico completo está em
[Decisões e backlog](DECISIONS.md); a curadoria de revisores externos está em
[Crítica x10](critica_x10.md).

## O que já está implementado e testado

- **A inversão de incentivo** ($D > W$) é verificável e tem teste automatizado.
- **A dissuasão** (empresas param de violar quando o canal existe) é produzida
  pelo próprio modelo, não imposta à mão; agora também verificada com
  **bootstrap multi-seed e intervalo de confiança 95%** que não cruza zero.
- **O bem-estar** é medido pelo dano evitado (e creditando a multa arrecadada
  pelo Estado), não pelo número de punições.
- **A coordenação tipo "jogo global"** tem versão analítica fechada e testada
  (limiar único de switching).
- **A camada Hirschman exit-with-equity** (R07) modela ameaça crível de êxodo
  coletivo com vesting acelerado, **agora restrita a Regime C** após o gating
  jurídico (reserva de lei).
- **Catálogo de 9 condutas anticompetitivas** com atores primários e
  adjacentes (gradiente 3-níveis Near & Miceli), incluindo casos
  brasileiros (iFood marketplace, Apple anti-steering).

## O que ainda é trabalho futuro

| # | Limitação | O que falta |
|---|-----------|-------------|
| **R02** | "Jogo global" tem solução analítica, mas **isolada** | integrá-la à dinâmica completa do modelo; partição em R02a/R02b/R02c (integração, contraste multiplicidade×unicidade, unicidade sob heterogeneidade) |
| **R03** | Os números **não estão calibrados** contra a realidade | ajustar parâmetros aos dados do CADE e à literatura; hoje as magnitudes são plausíveis, não ajustadas |
| **R05** | Os **pesos do bem-estar** seguem provisórios | ancorar custo de dano (Connor-Lande) e custo de erro (Polinsky-Shavell) em estimativas calibradas |
| **R06** | A **capacidade da autoridade** usa aproximação | precisa de dado empírico do CADE pós-2020 |
| **L-Jur1** | A **fragilidade jurídica do Regime B** | (i) a re-caracterização da recompensa como "ressarcimento" sob o Art. 12 da Resolução 21/2018 é juridicamente controvertida (falsificador **F6**); (ii) o Regime B é resolução infralegal e, por **reserva de lei** (Art. 22, I, da Constituição), **não pode** impor cláusula contratual padrão de vesting nem proteção trabalhista — o que `hirschman.py` modela só é coerente sob Regime C; (iii) o conceito de "vítima" do Art. 12 é coletivo na práxis do CADE, e o denunciante interno pode ser **partícipe** da conduta (colisão com Art. 86 — leniência clássica). Tratar como **conjectura jurídica otimista**, não tese pacificada |
| **R09–R13** | Pendências normativas pós-crítica | endogeneizar $g_i(t)$ (Eco A); IC-F* completa (Eco A); Hirschman como elevação de $W$ (Eco A); integrar arquétipo "racional" ao jogo global (Mat B); endgame do paper (Adv A + Designer + PM) |
| **R14** | Refinamentos do enriquecimento dos agentes | usar `fracao_vested_individual` por trabalhador em `custo_exodo_esperado` (granularidade); ativar canal de `poder_retaliacao` modulando `r_represalia` localmente |

## Em resumo

O modelo demonstra **direção e magnitude** do mecanismo de forma transparente e
reproduzível. O que ele **ainda não faz** é entregar números calibrados e
provas formais completas — e isso está marcado como tal em todo o repositório,
em vez de apresentado como resultado definitivo.
