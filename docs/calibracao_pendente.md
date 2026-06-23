# Calibrações pendentes

<p class="deck">Inventário das calibrações empíricas que o modelo ainda não tem fechadas, com a metodologia de execução de cada uma. Lista o que falta para que afirmações numéricas do projeto possam ser citadas como predições verificadas, em vez de ordens de grandeza ilustrativas.</p>

<p class="byline"><em>Anexo de transparência</em> · calibrações pendentes · rascunho v0.2.0</p>

Esta página detalha quatro pontos onde o argumento numérico do projeto ainda depende de calibração externa não-fechada. A intenção é cumprir o duplo objetivo da [transparência epistêmica](transparencia.md): documentar onde a evidência ainda não fecha e fornecer ao leitor a receita para fechar.

## 1 · N\* ≈ 1.679 firmas × CNAE

A calibração formal R03 (Nelder-Mead em duas dimensões) entrega o ponto ótimo $(\text{fração de violadoras}, \text{taxa de capacidade}) = (0{,}323;\ 0{,}481)$, do qual decorre o **universo CADE implícito** de aproximadamente **1.679 firmas sob jurisdição ativa**. Este número é apresentado em [`index.md`](index.md) e em [`internacional.md`](internacional.md) como predição falsificável.

**O que está pendente.** O número 1.679 não foi cruzado com o cadastro real de firmas brasileiras por **CNAE (Classificação Nacional de Atividades Econômicas)** filtrado por critério de relevância antitruste (porte mínimo, mercado relevante digital, posição dominante presumida). Sem esse cruzamento, 1.679 é predição teórica — não tem comparação empírica.

**Receita de calibração.** A fonte primária é o cadastro IBGE-RAIS (Relação Anual de Informações Sociais) cruzado com a Receita Federal (CNPJ + atividade econômica). Os passos:

1. Filtrar firmas com CNAE em divisões 62 (atividades dos serviços de tecnologia da informação), 63 (atividades de prestação de serviços de informação), 73 (publicidade) e 47 (comércio varejista, para *marketplaces*).
2. Aplicar critério de relevância antitruste: receita anual ≥ R\$ 75 milhões (limiar de notificação de ato de concentração da Lei nº 12.529/2011, escalado proporcionalmente).
3. Cruzar com a lista de firmas com algum tipo de procedimento antitruste em curso na vigência da pesquisa (CADE 2023–2025).
4. Comparar o universo resultante com N\* = 1.679.

Se o universo real ficar dentro de uma ordem de grandeza (entre ~500 e ~5.000 firmas), a predição é confirmada; se ficar fora desse intervalo, a calibração R03 precisa de revisão substantiva. Esse cruzamento é registrado em [Brainstorm de revisão](brainstorm_revisao.md) §5 e em [Decisões e backlog](DECISIONS.md).

## 2 · Capacidade institucional DOJ-ATR e DG-COMP

Os cenários R28 (`eua_doj_atr_rewards_2025` e `ue_dma_whistleblower_tool_2024`) usam a `taxa_capacidade` calibrada contra o CADE como aproximação para as autoridades estadunidense e europeia. Essa aproximação é declaradamente conservadora — funciona para comparação direcional (ver Figura 13 do site), mas não para volume absoluto.

**O que está pendente.** Calibração da `taxa_capacidade` real do DOJ-ATR (FY 2025) e da DG Competition (orçamento 2024) para as variantes EUA e UE dos cenários.

**Receita de calibração.** Fontes primárias:

1. **DOJ-ATR FY 2025 Congressional Budget Justification** — relatório anual do *Justice Department* ao Congresso, em que a Antitrust Division detalha alocação orçamentária por atividade. O componente relevante é o pessoal-fim alocado a *enforcement* civil + criminal, dividido pelo universo de jurisdicionados ativos.
2. **European Commission DG Competition, Annual Activity Report 2024** — relatório institucional anual da DG-COMP que detalha alocação por unidade (anti-trust, mergers, state aid). O componente relevante é o pessoal-fim de *unit B* (anti-trust) dividido pelo universo de empresas sob jurisdição do TFUE.

Para cada autoridade, derivar a `taxa_capacidade` como `pessoal_fim_antitrust / universo_jurisdicionados`, e refazer as figuras 13 e 23 com os valores calibrados em vez do *default* brasileiro.

## 3 · Faixas R29 contra Saito 2021

**Status.** O cenário canônico `cascata_adesao_saito_calibrada` ([documentado em formulário §4.1](formulario.md)) já entrega a calibração contra o gradiente do Art. 86 da Lei nº 12.529/2011 conforme Saito (2021) §3.7.7: $\mathbf{f}_W^{\text{adesão,Saito}} = (1{,}0;\ 0{,}795;\ 0{,}466;\ 0{,}345;\ 0{,}345)$.

**Pendência residual.** O cenário entrega a calibração das **faixas de desconto**; está pendente o cruzamento com o *gradiente Saito real para conduta unilateral*, que não foi medido por Saito (2021) — o trabalho original cobre cartéis. A calibração R29 atual transporta o gradiente de cartel para o domínio de conduta unilateral como aproximação. O cruzamento empírico — quando o CADE acumular conjunto suficiente de TCCs em condutas unilaterais — fica como pesquisa aberta.

## 4 · Mussler-Macy contra a forma forte da Proposição 5

A R29-iv (recompensa coletiva pós-abertura) é implementada como salvaguarda anti-erosão Coleman conforme Marwell & Oliver (1993) e Macy (1991). O cenário canônico `recompensa_coletiva_anti_erosao` permite comparação direta com `cascata_adesao_com_erosao_coleman` (ambos sob α=0,5).

**Pendência.** A varredura multi-seed que mede se a recompensa coletiva efetivamente protege o substrato cooperativo sob erosão α elevada ainda não foi executada. Receita:

1. Rodar 10 sementes × 8 valores de α ∈ {0; 0,1; …; 0,9} para o cenário `cascata_adesao_com_erosao_coleman`.
2. Rodar 10 sementes × 8 valores de α para o cenário `recompensa_coletiva_anti_erosao`.
3. Comparar a trajetória de `capital_social_residual` final entre os dois cenários por valor de α.
4. Se a partilha coletiva reduz a derivada do declínio do capital social, a Proposição 5 candidata na forma forte fica falsificada também sob R29 (replicação do achado já documentado em [`limitacoes.md`](limitacoes.md)).

A execução fica como item explícito no [Brainstorm de revisão](brainstorm_revisao.md) §5.