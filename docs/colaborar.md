# Como contribuir, discordar ou conversar

<p class="deck">Vias concretas pelas quais pesquisadoras, advogadas, autoridades e jornalistas podem entrar no projeto: contestar a calibração, falsificar uma proposição candidata, propor cenário adversarial, escrever sobre o desenho ou propor co-autoria em uma extensão. Tudo aberto sob CC BY-SA 4.0; tudo auditável por simulação multi-seed.</p>

<p class="byline"><em>Ato 5 de 5</em> · Colaborar · rascunho v0.2.0</p>

<p class="lede">O projeto é um rascunho de trabalho em elaboração, com pendências normativas e empíricas explícitas registradas em <a href="../DECISIONS/">decisões e backlog</a> e na lista de <a href="../limitacoes/">limitações</a>. Esta página enumera as formas concretas pelas quais alguém de fora pode contestar, estender ou se associar ao trabalho — preferencialmente em canal aberto (issues no GitHub), preservando a auditabilidade do processo.</p>

## Três comunidades com pontos de entrada explícitos

- **Sociólogos da coordenação coletiva** (Olson, Ostrom, Coleman, Elster, Chwe) — a Proposição 5 candidata (Coleman: erosão endógena do capital social) é falsificável via `tests/test_erosao_coleman.py`. Veja `docs/bem_publico.md`.
- **Cientistas políticos da regulação** (Stigler, Wilson, McCubbins-Schwartz, Carpenter-Moss) — `docs/viabilidade_regime_c.md` documenta a infactibilidade política do Regime C 2024-2027; o cenário `captura_processamento_cade` modela o gargalo de 180 servidores área-fim do CADE (RIG 2024).
- **Behavioral ethicists / psicometristas** — o arquétipo `oportunista` (R24) é primeira aproximação; calibração contra Dyck-Morse-Zingales 2010 e elaboração com Big Five / Dark Triad / Fehr-Schmidt α/β individual é pendência aberta.

## Reproduzir, verificar, derrubar

O caminho mais útil — e mais barato — é **rodar o modelo, contestar a calibração e tentar quebrar a conclusão**. Tudo está aberto sob CC BY-SA 4.0.

```bash
# Caminho rápido — sem instalar nada, no navegador:
# https://freirelucas.github.io/waas-antitrust/brincar/

# Caminho local — para mexer no código
git clone https://github.com/freirelucas/waas-antitrust.git
cd waas-antitrust
pip install -e ".[dev]"
pytest -x -q -m "not slow"                        # 385 testes (~31s)
python scripts/gerar_figura_dissuasao.py          # figura 03 do site
python scripts/run_sobol_full.py --n-base 1024    # varredura paramétrica
```

Os parâmetros adversariais — `D_disc_base_tcc`, `p_anulacao_tcc`, `custo_legal_uw`, `alpha_erosao`, `taxa_capacidade` — estão expostos em `WaaSParametros`. Calibrar com seus números preferidos é uma chamada de função.

### Receitas concretas de contestação

**Cético do Mecanismo (Eco A v1):** "se o TCC clássico já dá desconto, ninguém paga". Reproduzível:

```python
from waas_antitrust.model import WaaSModel, WaaSParametros

# Calibrar D_base contra a sua mediana empírica preferida
m = WaaSModel(WaaSParametros(
    n_empresas=20, n_tiques=40, seed=11, regime="B",
    D_disc=0.30,
    D_disc_base_tcc=0.20,   # ⇐ você escolhe; teste com 0.10, 0.20, 0.28
))
df = m.executar()
# Compare n_firmas_optaram_tcc_classico e n_pagou em função de D_disc_base_tcc
```

**Cético da Calibração (R03):** "Saito 2021 dá outra mediana, refaça a varredura". Reproduzível:

```python
# Edite src/waas_antitrust/calibracao/saito.py com sua mediana
# (mantenha fonte primária no docstring)
# Rode o pipeline:
python scripts/calibrar.py --metrica dano_acumulado --seeds 12
```

**Cético do Sociólogo (R26):** "WaaS destrói o capital social que tenta extrair". Reproduzível:

```python
# alpha_erosao calibra a velocidade de erosão Coleman
for alpha in (0.0, 0.2, 0.5, 0.8):
    m = WaaSModel(WaaSParametros(
        n_empresas=20, n_tiques=40, seed=11, regime="B",
        alpha_erosao=alpha,
    ))
    df = m.executar()
    print(f"α={alpha}: capital_social_final={df['capital_social_residual'].iloc[-1]:.3f}, "
          f"dano={df['dano_acumulado'].max()}")
```

Se a direção da Proposição 3 (ou 5) quebrar sob calibração que você considera realista, **abra uma issue com o output** — isto é exatamente o que o projeto precisa para sair do plausível e entrar no ajustado.

### Receita 4 — cético do canal (R27)

"O escrow explícito muda os resultados? Por que então a flag existe?"

```python
from waas_antitrust.model import WaaSModel, WaaSParametros

base = dict(
    n_empresas=20, tam_medio_empresa=200, n_tiques=20,
    seed=29, regime="B", fracao_violadoras=0.7,
)
for explicito in (False, True):
    df = WaaSModel(WaaSParametros(**base, usar_escrow_explicito=explicito)).executar()
    print(
        f"escrow_explicito={explicito}: "
        f"em_escrow={df['n_denuncias_em_escrow'].max()}, "
        f"aberturas={df['n_aberturas_simultaneas_acum'].max()}, "
        f"dano={df['dano_acumulado'].iloc[-1]:.1f}"
    )

# Sub-receita 4b: varrer a janela de expiração (Δt) e medir
# quantos depósitos morrem antes da massa crítica.
for janela in (0, 2, 4, 8):
    df = WaaSModel(WaaSParametros(
        **base, usar_escrow_explicito=True, janela_escrow_tiques=janela
    )).executar()
    print(
        f"janela={janela}: expirados={df['n_depositos_expirados_acum'].max()}, "
        f"aberturas={df['n_aberturas_simultaneas_acum'].max()}"
    )
```

Sob a leitura v3 (Ayres-Unkovic 2012; análogo Callisto), o caminho histórico (escrow implícito em `EmpresaAgent`) e o caminho explícito (`AutoridadeAgent.escrow_denuncias`) devem produzir resultados muito próximos em P0/P1/P2 — diferenças significativas no horizonte longo indicam acoplamento não documentado que vale investigação. A varredura de `janela_escrow_tiques` é o canal de falsificação para a hipótese "janela curta como salvaguarda anti-erosão" (limitação Coleman, R26).

## Contribuir com calibração ou texto

Há três bancos de dados externos contra os quais o modelo precisa ser ajustado, e o autor não conseguiu acesso a todos sozinho:

- **Mediana de desconto em TCCs CADE pós-Saito (2021).** Cobrir o intervalo 2020–2025 fecharia $D_{\text{base}}$ — a peça central da IC-F\* corrigida.
- **Número de funcionários em subsidiárias brasileiras de big tech.** Permitiria reescalonar a capacidade da autoridade (`taxa_capacidade`) ao universo real (R06).
- **Custos legais médios em ações trabalhistas e em representações ao CADE.** Calibraria `custo_legal_uw` contra a faixa empírica brasileira.

Se você tem esses dados ou trabalha com quem tem, abra uma issue ou um PR contra o módulo `src/waas_antitrust/calibracao/`. Toda calibração externa precisa ter fonte primária verificável no docstring — não há margem para citação não-verificável.

Há também trabalho jurídico-dogmático em aberto, particularmente a **D06** (análise dogmática "vítima-empregado" no Art. 12) e a calibração de risco de anulação (F6). Quem tenha formação em direito antitruste brasileiro encontra material para escrever — e a co-autoria é negociável.

## Discordar do desenho

Algumas decisões deste projeto são deliberadamente discutíveis. As cinco principais estão em [DECISIONS.md](DECISIONS.md) como **R09–R13**. Cada uma alteraria material e Proposições; cada uma exige conversa explícita, não execução por piloto automático.

- **R09 (Eco A):** endogeneizar $g_i(t) = \pi R / (p S)$. Eu não fiz porque mudaria a Prop. 3.
- **R10 (Eco A):** IC-F\* completa $W + p_{\text{pago}}(S-D) < p_{\text{não pago}}S$. Não fiz porque mudaria a Prop. 1.
- **R11 (Eco A):** Hirschman como elevação de $W_{\text{esperado}}$, não subtração de $g_i$. Equivalência analítica é alegada mas não testada.
- **R12 (Mat B):** substituir o arquétipo racional pelo limiar de switching $x^*$ do jogo global. Integraria a Prop. 2 ao ABM.
- **R13 (PM, Designer, Eco B, Adv A):** distribuição Pareto/lognormal de fatia de mercado; sankey real do mecanismo; três condutas-piloto com fixtures; `p_anulacao_tcc` como variável de varredura Sobol.

Se você acha que uma dessas decisões é errada — ou se você tem um argumento que invalida o desenho como um todo — abra uma issue **com o argumento**, não só com a discordância. Texto é mais barato de discutir do que código.

## A história institucional do projeto

A hipótese original deste projeto surgiu numa conversa de 06 de setembro de 2022 com **Felipe Roquete**, Superintendente-Adjunto do CADE e doutorando em Direito da Regulação na FGV. A possibilidade de co-autoria está rastreada em **D04**; o repositório é mantido independentemente, mas a origem intelectual é explícita.

O autor — eu — trabalha no IPEA (DIEST/COGIT). Este repositório **não vincula o IPEA**. As posições aqui defendidas são minhas, e a intenção é submeter o artigo a revista internacional indexada (*Journal of Competition Law & Economics* ou similar) com aprovação prévia da chefia institucional.

## Citação, licença, contato

Veja [`CITATION.cff`](https://github.com/freirelucas/waas-antitrust/blob/main/CITATION.cff) para metadados estruturados (Zenodo via release futura). Código e documentação sob **Creative Commons CC BY-SA 4.0**. Issues e PRs no [repositório no GitHub](https://github.com/freirelucas/waas-antitrust). Para contato direto sobre co-autoria ou discussão acadêmica, o e-mail está no `CITATION.cff`.

<div class="ato-fim" markdown>
**Fim dos cinco atos.** Se você chegou até aqui, o sistema funcionou — para o que ele era: um convite a entrar num argumento que precisa ser apertado por mãos diferentes da do autor.

[Voltar ao Ato 1 →](index.md)
</div>
