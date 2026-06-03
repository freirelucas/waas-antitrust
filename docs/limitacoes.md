<span class="ato-chip">Ato 4 de 5 · A honestidade</span>

# O que ainda não está sustentado

O Ato 3 fechou com evidência direcional para o canal de dissuasão. Mas seria desonesto parar aí. Este projeto é um **artigo em elaboração**, e existem pontos onde a alegação ainda não tem cobertura — alguns por calibração faltando, outros por escolha teórica que precisa de revisão, outros por restrição estrutural do desenho jurídico. Esta página enumera cada um deles e diz, na medida do possível, **o que faria a alegação sustentar-se**.

A postura é simples: **dizer onde o argumento ainda não fecha é mais útil ao leitor do que esconder a dobra**. O backlog técnico completo está em [Decisões e backlog](DECISIONS.md); o que segue é a versão para humanos.

## A fragilidade jurídica do Regime B é a mais séria

Esta é a charneira que oito revisores externos — convocados na [Crítica x10](critica_x10.md) — apontaram independentemente, e a que mais muda a leitura do projeto. Vale dizer com todas as letras.

O Regime B implementa o WaaS por **resolução do CADE**, sem alterar lei. Tem três vetores de fragilidade:

**(i) A re-caracterização da recompensa como "ressarcimento" é controvertida.** A jurisprudência sobre o Art. 12 da Resolução 21/2018 trata "vítimas" como categoria coletiva (consumidores, concorrentes, erário). O denunciante interno é, dogmaticamente, **testemunha qualificada** — não a coletividade lesada. Re-caracterizar o pagamento como ressarcimento dessas vítimas é construção finalística, e o Judiciário pode rejeitá-la em sede de controle (falsificador F6 do desenho). O modelo torna isto calibrável via `p_anulacao_tcc`.

**(ii) Resolução do CADE não pode impor cláusula contratual padrão.** A camada **Hirschman exit-with-equity** (R07) supõe cláusulas contratuais de vesting acelerado por gatilho de ação coletiva. Por **reserva de lei** (Art. 22, I, da Constituição), matéria contratual padrão e proteção trabalhista são competência exclusiva da União por **lei** — não cabem em resolução infralegal. Logo, R07 só é institucionalmente coerente sob **Regime C**, e o modelo agora reflete isso: o parâmetro `fracao_contratos_acelerados > 0` em Regime A ou B é forçado a 0 com aviso explícito.

**(iii) Há colisão com a leniência clássica.** Se o denunciante interno for **partícipe** da conduta — o engenheiro que codificou o algoritmo, o comercial que operou a exclusividade, o *growth* que instrumentou o *dark pattern* — o caminho institucional adequado é o Art. 86 (leniência clássica), não o WaaS. O Regime B pode criar **arbitragem regulatória** entre os dois canais.

A solução estrutural para os três é o **Regime C** — extensão da Lei 13.608/2018 ao antitruste, via Congresso. Mais robusto, custa voto político. O modelo cobre os dois regimes para deixar a escolha explícita.

## Os números ainda não estão calibrados

A simulação produz direção e magnitude, mas os parâmetros são **plausíveis, não ajustados**. Há três bancos de dados externos contra os quais o modelo precisa ser calibrado antes de qualquer alegação quantitativa:

- **Saito (2021)** — *Termo de Compromisso de Cessação na Lei nº 12.529/11*, CADE/PNUD. Cobre 349 TCCs em 7,5 anos com mediana de desconto. Calibrar $D_{\text{base}}$ contra esse universo é o item número um em R03.
- **DEE/CADE Documentos de Trabalho 003/2022 e 001/2024** — magnitudes de multa, vazão da autoridade, perfil de capacidade.
- **Wiedman & Zhu (2023, *CAR*)** — evidência empírica de redução de fraude após Dodd-Frank §922 nos EUA. Fornece um quarto alvo de calibração via mecanismo análogo (incentivo financeiro ao denunciante interno).

Calibração formal contra esses três alvos está em **R03** — a pendência mais importante do backlog.

## Os pesos do bem-estar são provisórios

O bem-estar social é definido como $-(\text{dano} + \beta \cdot \text{FP} + \gamma \cdot \text{custo recompensa} + \delta_{\text{ex}} \cdot \text{êxodo} - \delta_{\text{mu}} \cdot \text{multa arrecadada}) / w_a$. Os defaults usados nos gráficos — $\beta=1$, $\gamma=0$, $\delta_{\text{ex}}=0{,}5$, $\delta_{\text{mu}}=1$ — são **normativos**, não calibrados. Ancorar cada um requer:

- $\beta$ contra Polinsky-Shavell (custo social do erro tipo I em enforcement);
- $\gamma$ contra a interpretação econômica do desconto como transferência privada (provavelmente $0$);
- $\delta_{\text{ex}}$ contra a literatura de capital humano em transição (custo de substituição + perda transitória de produtividade);
- $\delta_{\text{mu}}$ contra a valoração marginal de receita pública (provavelmente $\approx 1$).

A consolidação está rastreada em **R05**.

## As proposições teóricas seguem em parte como conjecturas

A **Proposição 1** — viabilidade da IC-F\* no ponto-alvo do Regime B — está demonstrada **pontualmente** por teste de regressão, mas as faixas jurídicas do esboço (multa entre 1% e 20% da receita, $D \le 50\%$ da multa) seguem ilustrativas. A Proposição é honesta sobre isso.

A **Proposição 2** — unicidade do equilíbrio de coordenação no limite $\tau \to 0$ do subjogo de Morris-Shin — está implementada em forma fechada no módulo `jogo_global` e verificada numericamente em testes. Mas **não está integrada à dinâmica completa do ABM** (R02a), o **contraste numérico com multiplicidade sob conhecimento comum não foi feito** (R02b), e a unicidade sob heterogeneidade de arquétipos × papéis é **conjectura aberta** (R02c) — Morris-Shin supõe homogeneidade que não temos.

A **Proposição 3** — dominância de bem-estar de B sobre A — está sustentada direcionalmente por simulação multi-seed com CI 95% que não cruza zero. **A prova formal segue como esboço**, não como teorema fechado.

## Cinco decisões normativas em aberto

Há cinco pontos onde a literatura crítica converge mas o autor ainda não decidiu — porque cada decisão **altera Proposições** e exige conversa explícita, não execução automática:

- **R09** — endogeneizar $g_i(t) = \pi \cdot R / (p \cdot S)$ como função do estado, à la Becker. Altera Prop. 3.
- **R10** — IC-F\* completa $W + p_{\text{pago}} \cdot (S - D) < p_{\text{não pago}} \cdot S$. Altera Prop. 1.
- **R11** — modelar Hirschman como elevação de $W_{\text{esperado}}$ em vez de subtração de $g_i$. Altera o microfundamento de R07.
- **R12** — substituir o arquétipo "racional" pela estratégia-limiar $s_i \ge x^*$ do jogo global. Integra Prop. 2 ao ABM e fecha R02a.
- **R13** — distribuição Pareto/lognormal de fatia de mercado (em digital, o dano é cauda longa, não uniforme).

Estão registrados em [DECISIONS.md](DECISIONS.md). Cada um tem origem, autor crítico, e arquivos-alvo.

## O que já está sustentado

Em respeito à simetria, vale dizer o que **não** está nesta lista — o que sobreviveu à pressão da crítica e à reamostragem:

- A **inversão de incentivo** ($D > W$ no ponto-alvo) é verificável e tem teste automatizado pontual.
- A **dissuasão** (empresas param de violar) é produzida pelo próprio modelo, multi-seed, com CI 95% não cruzando zero.
- O **bem-estar substantivo** credita a prevenção (incorpora custo do dano, custo de êxodo de Hirschman, multa arrecadada pelo Estado), em vez de premiar detecção.
- A **coordenação tipo jogo global** tem versão analítica fechada e testada (limiar único de switching em $\tau \to 0$).
- O **gating jurídico do R07** está implementado — o modelo recusa $\text{fracao\_contratos\_acelerados} > 0$ em Regimes A e B.
- O **catálogo de 9 condutas** com gradiente 3-níveis (Near & Miceli) inclui casos brasileiros (iFood marketplace, Apple anti-steering).

<div class="ato-fim" markdown>
**Fim do Ato 4.** A honestidade não destrói o argumento; encurta o caminho para sustentá-lo. Há trabalho de calibração, trabalho jurídico e cinco decisões normativas em aberto. Se você quer ajudar — discordar, calibrar, escrever, criticar — o Ato 5 mostra como.

[Ato 5: Como contribuir →](colaborar.md)
</div>
