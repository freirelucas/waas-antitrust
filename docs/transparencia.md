# Transparência epistêmica

Este anexo consolida, em uma página, o estado de evidência por trás de
**cada afirmação central** do projeto: o que está demonstrado, o que
está conjecturado, o que está aberto e em qual seed/configuração cada
figura empírica foi produzida. A intenção é dar ao leitor o que ele
precisa para **refutar** o projeto numericamente — não convencê-lo de
que tudo está fechado.

## Convenção visual nas figuras

Toda figura do site carrega chips de status para evitar leitura ambígua:

- Borda **tracejada cinza** + chip "Ilustrativo" — figura conceitual
  (Camada de argumentação visual; sem simulação).
- Borda **sólida verde** + chip "Resultado da simulação" — figura
  produzida pelo modelo; abaixo, um segundo chip pode aparecer:
    - **CALIBRADO** (verde escuro) — eixos ancorados em dado externo
      verificado (Saito 2021, RIG/TCU). Figura 14 é exemplo.
    - **DIRECIONAL** (amarelo) — multi-seed multi-cenário, mas a
      configuração não está calibrada formalmente; ler magnitude com
      reserva. Figuras 12 e 13 são exemplos.
    - **ACHADO NEGATIVO** (vermelho) — figura que **refuta** uma
      hipótese candidata declarada (não que ilustra o erro do modelo).
      Figura 10 é exemplo (falsifica a Prop. 5 forte).

A ausência de sub-chip indica figura empírica em configuração padrão,
sem alegação de calibração além das fontes primárias do modelo
(Brasscom 2024, RIG/TCU para capacidade, Saito 2021 para descontos).

## Status das proposições (por evidência)

| # | Proposição | Estado | Evidência primária | Onde |
|---|---|---|---|---|
| 1 | Viabilidade IC do "empresa paga" sob Regime B | **verificada pontualmente** | teste de regressão no ponto-alvo $D > W$ | `tests/test_model.py` |
| 2 | Unicidade do equilíbrio Morris-Shin $\tau \to 0$ | **verificada (homogeneidade)**; conjectura sob heterogeneidade (R02c) | módulo `jogo_global` + viz `multiplicidade_unicidade` | figura 09 |
| 3 | Dominância de bem-estar do Regime B sobre A | **suportada empiricamente** — IC bootstrap 95% multi-seed não cruza zero | `bootstrap.gerar_figura` + teste em `test_robustez.py` | figura 12 |
| 4 | Coordenação via canal de depósito condicional (LCMC) | **verificada por construção**: abertura simultânea elimina o equilíbrio de silêncio | `AutoridadeAgent.abrir_escrow_se_massa_critica` + cenário `apenas_canal_sem_instrumento` | figura 11 |
| 5 (forte) | Existe $\alpha^*$ tal que B colapsa em A | **refutada na grade** 10 seeds × 8 alphas × 40 tiques (estável até $\alpha=0,9$) | `scripts/varredura_alpha_erosao.py` | figura 10 |
| 5 (fraca) | Capital social residual decai com $\alpha_{\text{erosão}}$ | **verificada empiricamente** | mesma varredura | figura 10 (painel B) |

## Estado da calibração (por alvo)

| Alvo | Fonte primária | Estado | Resultado |
|---|---|---|---|
| **TCC/ano** (volume) | Saito 2021 (349 TCCs 2012-2019) | **calibrada** (Nelder-Mead, 5 seeds) | erro 6,65% no ponto $(0{,}323; 0{,}481)$; alvo dentro do IC; $N^\star \approx 1.679$ |
| **Fração interna DMZ 19%** | Dyck-Morse-Zingales 2010 | **removida da função objetivo** | não-identificável: o modelo tem canal único de detecção |
| **5 leniências/ano** | Comunicado CADE 2023 | em aberto — não foi alvo da calibração formal | varredura preliminar em `calibracao_r03_first_pass.parquet` |
| **Desconto base TCC** | Saito 2021 §3.7.7 (média Tribunal 15%) | **calibrada** | `_D_BASE_TCC = 0.15` em `cenarios.py` (helper `d_base_tcc_calibrado`) |
| **Capacidade institucional CADE** | RIG/TCU 2022-2024 | **calibrada** (180 servidores área-fim) | `transparencia_cade.N_SERVIDORES_AREA_FIM = 180`; figura 14 |
| **Distribuição de papéis** | LinkedIn/organogramas | em aberto (E05) | dois presets (`BIGTECH_MADURA`, `MARKETPLACE_BR`); figura 17 |
| **`taxa_capacidade` DOJ-ATR/DG-COMP** | orçamentos federais EUA/UE | em aberto (R28) | cenários EUA/UE usam defaults BR; comparações direcionais apenas |

## Configuração das 19 figuras

Cada figura tem **seeds** explícitas, **horizonte** e **cenário de
referência** — para reprodução literal:

| Fig | Seeds | Tiques | Cenário | Reporter principal |
|---|---|---|---|---|
| 03 dissuasão e bem-estar | (0..11) | 40 | `regime` ∈ {A, B, C} | `dano_acumulado`, `bem_estar` |
| 04 cascata | (7) | 20 | LCMC analítico (sem modelo) | n/a (curva sigmoidal) |
| 05 erosão Coleman | (7) | 20 | `alpha_erosao` ∈ {0, 0.2, 0.5} | `capital_social_residual` |
| 06 painel macro | (default 11) | 30 | Regime B | 4 reporters |
| 07 painel micro | (11) | 30 | `modo_corrida=True` | reporters da firma 0 |
| 08 Proposição 5 | (11, 23, 37, 41, 59) | 40 | `alpha` ∈ {0, 0.1, 0.3, 0.7} | `capital_social_residual`, dano rel. |
| 09 multiplicidade × unicidade | n/a (analítico) | n/a | Morris-Shin $\tau$ ∈ {0, 0.1, 0.3, 0.5} | melhor-resposta $f(x)$ |
| 10 falsificação Prop. 5 forte | (11, 23, 37, 41, 53, 59, 71, 83, 97, 101) | 40 | `alpha` ∈ {0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9} | `dano_acumulado`, `capital_social_residual` |
| 11 Sankey LCMC | (2026) | 15 | `cenario_corrida_leniencia` + escrow explícito | fluxos agregados |
| 12 bootstrap regimes | (11, 23, 37, 41, 53, 59, 71, 83, 97, 101, 113, 127) | 20 | Regime A/B/C | `dano_acumulado`, `bem_estar` |
| 13 internacional | (11, 23, 37, 41, 53, 59, 71, 83) | 24 | status_quo / EUA / UE | `dano_acumulado` |
| 14 CADE (capacidade) | n/a (dados RIG/TCU) | n/a | n/a | série temporal externa |
| 15 adversarial | (11, 23, 37, 41, 53) | 12 | `oportunista` ∈ {0..30%} | `falsos_positivos_acum`, `dano_acumulado` |
| 16 falsificação dos vetores | (11, 23, 37) | 10 | Regime B + 5 vetores A-E | reporter de cada vetor |
| 17 variedade | (11, 23, 37, 41, 53) | 12 | BIGTECH_MADURA × MARKETPLACE_BR | `n_sinais`, `verdadeiros_positivos_acum` |
| 18 painel-síntese | (11, 23, 37) | 16 | A/B/C/EUA/UE + LCMC + erosão | 6 painéis |
| 19 mapa $\lambda \times$ Hirschman | (11, 23, 37) | 20 | Regime C + Hirschman universal | `dano_acumulado` |

## Pendências `[?]` — auditoria honesta

Itens marcados `[?]` no repositório que **ainda não foram verificados
contra a fonte primária**:

1. **Mungan-Klick 2014/2016** sobre leniência sob assimetria de informação — citado em `aprendizados_v3.md` e em comentários do código; URL primária não conferida.
2. **Mueller-Pereira 2002** sobre captura regulatória no BR — citado em `critica_x10.md`; verificação contra ProQuest/CrossRef pendente.
3. **Pacheco 2006** sobre coordenação CADE-MPF — citado em `INSTITUTIONAL.md`; documento não obtido.
4. **Cornell J. of Law and Public Policy 2025** sobre APIs como dispositivo antitruste — citado em `condutas.py`; volume/número não conferido.
5. **EC RFI 2024** sobre Microsoft-OpenAI — citado em `internacional.md`; verificação contra registro público pendente.
6. **DOJ-ATR Public Statements jan/2026** sobre o primeiro prêmio — citado em `internacional.md`; URL direta DOJ não anexada.
7. **DG-COMP orçamento 2024** — citado em R28; documento orçamentário EU não anexado.
8. **Décimo Primeiro Anuário OECD (2024)** sobre programas de denúncia — citado em `REFERENCES.md`; verificação contra OECD library pendente.
9. **Wiedman & Zhu 2023 (CAR)** sobre efeito Dodd-Frank — citado em `limitacoes.md`; DOI não conferido.
10. **CAARA 2019 EUA** texto integral — citado em `INSTITUTIONAL.md`; verificação contra US Government Publishing Office pendente.
11. **Reg. (UE) 2022/1925 Arts. 5/6/7** verbatim — citado em `internacional.md`; consolidado contra DOUE pendente.
12. **AlixPartners 2025 (40% das vagas não reabertas)** — citado em `choques.py`; documento não anexado.

Estes itens **não bloqueiam a tese** mas devem ser tratados antes da
submissão final do artigo. O resto das ~150 citações foi verificada
contra REFERENCES.md.

## Como falsificar o argumento (3 receitas)

Cada falsificador exige no máximo uma alteração de parâmetro. A
hipótese epistêmica que cada um derruba está entre parênteses:

### 1. Derrubar a Proposição 3 (B reduz dano vs A)

```python
from waas_antitrust.viz import bootstrap
fig, axes = bootstrap.gerar_figura(seeds=tuple(range(50)), n_tiques=40)
# Se as barras de B/C tocarem a barra de A com IC 95%, a Prop. 3 não
# sobrevive ao multi-seed expandido.
```

### 2. Forçar a Proposição 5 forte a aparecer

```python
from waas_antitrust.cenarios import aplicar_cenario
from waas_antitrust.model import WaaSModel, WaaSParametros
# Grade fina entre alpha=0.9 e alpha=1.0 — o limiar pode estar próximo
# do extremo do intervalo testado em jun/2026.
for alpha in [0.92, 0.95, 0.97, 0.99, 1.0]:
    p = aplicar_cenario(
        WaaSParametros(seed=11, n_tiques=80, alpha_erosao=alpha),
        "erosao_coleman_adversarial",
    )
    df = WaaSModel(p).executar()
    print(f"alpha={alpha}: dano={df['dano_acumulado'].iloc[-1]}")
```

### 3. Quebrar a Proposição 4 (canal coordena)

```python
# Cenário canônico com q_min impossível de atingir — se a Prop. 4 fosse
# falsa, a abertura simultânea ainda assim ocorreria.
from waas_antitrust.cenarios import aplicar_cenario
p = aplicar_cenario(
    WaaSParametros(seed=11, q_min_cooperacao_interna=0.99),
    "apenas_canal_sem_instrumento",
)
df = WaaSModel(p).executar()
# Esperado: n_aberturas_simultaneas_acum == 0
assert df["n_aberturas_simultaneas_acum"].iloc[-1] == 0
```

## Reprodutibilidade total

```bash
# 1. Reproduzir todas as 19 figuras do site
python scripts/regerar_todas_as_figuras.py

# 2. Reproduzir os 3 artefatos científicos da rodada
python scripts/varredura_alpha_erosao.py          # falsifica Prop. 5 forte
python scripts/identificabilidade_r03.py          # decompõe os 3 alvos
python scripts/calibrar_formal.py                 # calibração formal

# 3. Reproduzir o paper
python scripts/gerar_figs_paper.py
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Todas as seeds estão fixas; cada script aceita `--seeds` para que o
cético escolha as suas. Resultados gravados em `results/*.parquet` /
`results/*.json` permitem auditoria posterior sem re-execução.
