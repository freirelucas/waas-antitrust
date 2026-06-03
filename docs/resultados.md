<span class="ato-chip">Ato 3 de 5 · O teste</span>

# O que a simulação mostra

O Ato 2 apresentou um desenho. Equações, exemplos numéricos, três vetores de quebra. Tudo isso vive no papel — bonito, possivelmente coerente, mas que não diz se **funciona**. Para responder, precisamos de uma máquina que rode o jogo institucional vezes seguidas, com agentes que decidem por conta própria, e meça o que sai.

É o que o modelo `waas-antitrust` faz: 20 firmas, populadas por trabalhadores heterogêneos (éticos, imitativos, racionais e aleatórios), conectados por redes intra-firma do tipo *pequeno-mundo*, observados por uma autoridade tipo CADE com capacidade limitada. Rodamos esse sistema por 40 tiques (10 anos em trimestres) em cada um dos três regimes — A, B e C — e olhamos para duas perguntas:

1. **As empresas param de violar?** (Canal de dissuasão, Proposição 3.)
2. **O bem-estar social sobe?** (Canal de prevenção do dano, R05.)

A figura abaixo é a saída literal do modelo. Não é estilizada, não é ilustrativa — é o que o `WaaSModel.executar()` produziu quando rodamos com a *seed* 11 e os parâmetros declarados em `scripts/gerar_figura_dissuasao.py`.

## A evidência principal

![Dissuasão endógena e bem-estar por regime.](img/03_dissuasao_bem_estar.png){ .figura-empirica }

### Painel (A) — o que acontece com o número de empresas violando

No **Regime A** — o cenário atual, sem canal de incentivo — o número de empresas violando ao longo do tempo **cresce**. Não há ninguém para denunciar, a probabilidade percebida de detecção fica baixa, e firmas que não violavam no começo começam a violar conforme entendem que o custo esperado é baixo. É a inversão clássica: violar é o que minimiza a sanção esperada, e o sistema converge para essa estratégia.

Nos **Regimes B e C** — com canal WaaS — o desenho do mecanismo se reverte. Como existe a possibilidade real de denúncia, a detecção percebida sobe. Firmas que antes preferiam o risco passam a não violar. Em poucos tiques, **o número de violadoras ativas cai a zero**. Isto não é imposto à mão: emerge da decisão individual de cada firma comparando $g_i$ (sua atratividade de violar) com $p$ (a detecção percebida que ela atualiza por expectativa adaptativa).

### Painel (B) — o bem-estar social

O bem-estar é medido como o **negativo do custo social total** — dano causado pelas violações em curso, mais custos de erro (falsos positivos), mais custo da recompensa privadamente paga, menos a multa que retorna ao erário. Os pesos exatos seguem provisórios; estão rastreados em R05.

Os Regimes B e C ficam claramente acima do Regime A. **Não por punirem mais, mas por prevenirem o dano.** É um ponto importante: se medíssemos sucesso por "número de infrações detectadas", o Regime A pareceria *melhor* — afinal, há mais crime para detectar quando ninguém é dissuadido. A perversidade dessa métrica é o que motivou a redefinição do bem-estar em R05.

<div class="pull-quote" markdown>
A direção da Proposição 3 é robusta: em 12 seeds independentes, o intervalo de confiança 95% da diferença entre Regime B e Regime A não cruza zero.
</div>

## Por que a evidência é robusta

Há um pecado clássico em ABM, apontado por dois dos matemáticos da [Crítica x10](critica_x10.md): apresentar resultado de **uma única seed** como se fosse propriedade do mecanismo. Variância de seed pode produzir gráficos bonitos que não sobrevivem à reamostragem.

A defesa aqui é direta. Para a comparação central — "Regime B reduz violadoras em relação ao Regime A?" — o teste `test_dissuasao_endogena_robusta_a_multi_seed` executa o modelo em 12 seeds independentes, calcula a diferença entre B e A em cada uma, e constrói um intervalo de confiança 95% via bootstrap percentílico. **O intervalo não cruza zero.** A direção da Proposição 3 não é artefato de seed.

Em paralelo, a estimativa de detecção percebida `p_perc` passou por **suavização Beta-Binomial** com prior $\text{Beta}(\alpha=1, \beta=5)$ — eliminando a singularidade clássica do estimador frequencista `vp/n_violadoras` em $n=0$ e estabilizando a variância em $n$ pequeno. Estes são detalhes técnicos: a página de [Limitações](limitacoes.md) os apresenta de forma acessível.

## O que muda quando ativamos os vetores de quebra

Toda a evidência acima usa parâmetros conservadores: $D_{\text{base}}=0$ (todo o desconto é WaaS-específico), $p_{\text{anulação}}=0$ (nenhum TCC anulado), $c_{\text{legal}}=0$ (denunciante não paga advogado). É a calibração mais favorável ao mecanismo — e mesmo assim a evidência é direcional, não dramática.

A simulação também roda nos **regimes adversariais**:

- Quando $D_{\text{base}} \ge D_{\text{total}}$, a IC-F\* nunca é satisfeita. O contador `n_firmas_optaram_tcc_classico` cresce, ninguém paga recompensa, e o canal WaaS é silenciado. Em testes, $D_{\text{base}}$ intermediário reduz pagamentos proporcionalmente — propriedade desejável.
- Quando $p_{\text{anulação}} = 1$, todo TCC-WaaS assinado é anulado. A multa cheia retorna ao erário; o Regime B colapsa para a estrutura do Regime A. O teste `test_vetor_b_p_anulacao_um_anula_todos_os_tcc` confirma.
- Quando $c_{\text{legal}}$ é alto (5 salários anuais, por exemplo), o arquétipo racional deixa de denunciar. A sinalização cai.

Estes não são bugs do mecanismo; são as condições que **falsificam** o desenho. O modelo as expõe, calibra, e mede. Esta é a postura epistêmica que o projeto adota — **dizer onde o argumento quebra é mais valioso do que esconder a quebra**.

## Como reproduzir

O caminho mais rápido é o **[caderno-demo no Colab](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_demo.ipynb)** — instala dependências automaticamente, roda os três regimes e gera a figura em aproximadamente um minuto. Para regenerar a figura principal localmente:

```bash
pip install -e ".[dev]"
python scripts/gerar_figura_dissuasao.py
```

Para a análise de sensibilidade paramétrica completa (Sobol multi-seed, escala paper-grade):

```bash
python scripts/run_sobol_full.py --n-base 1024 --jobs -1 \
  --out results/sobol_full.parquet
```

Mais opções em [Como usar](uso.md).

<div class="ato-fim" markdown>
**Fim do Ato 3.** A evidência da simulação é direcional, multi-seed, e robusta a falsificações triviais. Mas o argumento honesto também precisa enumerar o que **ainda não está sustentado** — pesos provisórios, calibração faltando, proposições que seguem como conjecturas. O Ato 4 vai a fundo nisso.

[Ato 4: O que ainda falta →](limitacoes.md)
</div>
